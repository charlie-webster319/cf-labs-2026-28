"""Independent financial checks for the teaching notebooks.

Run with ``uv run python tests/validate_finance.py`` or call ``validate_lab1`` /
``validate_lab2`` with an executed notebook's globals. The reference calculations
use raw Excel prices, NumPy formulas and SciPy SLSQP, not PyPortfolioOpt routines.
"""

from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]


def reference_data():
    prices = pd.read_excel(
        ROOT / "downloading_stock_prices.xlsx", sheet_name="Data download", skiprows=7
    )
    dates = pd.to_datetime(prices.pop("date"), unit="D", origin="1899-12-30")
    prices.index = dates
    prices = prices.sort_index().sort_index(axis=1)
    values = prices.to_numpy(dtype=float)
    # Explicit division, independent of pandas pct_change and library estimators.
    monthly = values[1:] / values[:-1] - 1
    valid = np.isfinite(monthly).all(axis=1)
    monthly = monthly[valid]
    return prices, prices.index[1:][valid], monthly


def validate_lab1(ns):
    prices, dates, monthly = reference_data()
    amazon = monthly[:, prices.columns.get_loc("AMZN")]
    assert len(ns["amazon_data"]) == len(dates)
    np.testing.assert_allclose(ns["amazon_data"]["ret"], amazon, atol=1e-14)
    np.testing.assert_allclose(ns["var_95"], -np.quantile(amazon, 0.05))
    expected = np.column_stack((monthly.mean(axis=0) * 12,
                                monthly.std(axis=0, ddof=1) * np.sqrt(12)))
    np.testing.assert_allclose(ns["annualized_stats"].loc[prices.columns],
                               np.round(expected, 3), atol=1e-12)
    np.testing.assert_allclose((1 + np.array([0.1, -0.1])).prod() - 1, -0.01)
    return {"observations": len(dates), "amazon_monthly_var_95": float(-np.quantile(amazon, 0.05))}


def independent_optimum(mu, covariance, lower, objective, target=None):
    """A separate solver and explicit textbook objective check the notebook."""
    constraints = [{"type": "eq", "fun": lambda w: w.sum() - 1}]
    if target is not None:
        constraints.append({"type": "ineq", "fun": lambda w: w @ mu - target})
    if objective == "variance":
        function = lambda w: w @ covariance @ w
    else:
        function = lambda w: -(w @ mu - 0.02) / np.sqrt(w @ covariance @ w)
    result = minimize(
        function, np.repeat(1 / len(mu), len(mu)), method="SLSQP",
        bounds=[(lower, 1)] * len(mu), constraints=constraints,
        options={"ftol": 1e-12, "maxiter": 2000},
    )
    assert result.success, result.message
    return result.x, result.fun


def validate_lab2(ns):
    prices, dates, monthly = reference_data()
    mu = monthly.mean(axis=0) * 12
    covariance = np.cov(monthly, rowvar=False, ddof=1) * 12
    assert ns["risk_free_rate"] == 0.02
    assert ns["returns_wide"].index.equals(dates), "Return dates differ from original price changes"
    assert ns["returns_wide"].columns.equals(prices.columns)
    np.testing.assert_allclose(ns["returns_wide"], monthly, atol=1e-14)
    np.testing.assert_allclose(ns["mu"], mu, atol=1e-14)
    np.testing.assert_allclose(ns["cov_matrix"], covariance, atol=1e-14)
    assert (ns["summary_stats"]["count"] == len(monthly)).all()
    assets = ns["asset_summary"].set_index("symbol").loc[prices.columns]
    np.testing.assert_allclose(assets["mu"], mu, atol=1e-14)
    np.testing.assert_allclose(assets["sigma"], np.sqrt(np.diag(covariance)), atol=1e-14)

    portfolios = [
        ("max_sharpe_weights", "max_sharpe_perf", 0, "sharpe", None),
        ("min_vol_weights", "min_vol_perf", 0, "variance", None),
        ("target_weights", "target_perf", 0, "variance", ns["target_return"]),
        ("bounded_short_sharpe_weights", "bounded_short_sharpe_perf", -1, "sharpe", None),
        ("bounded_short_minvol_weights", "bounded_short_minvol_perf", -1, "variance", None),
        ("long_only_sharpe_weights", "long_only_sharpe_perf", 0, "sharpe", None),
        ("long_only_minvol_weights", "long_only_minvol_perf", 0, "variance", None),
    ]
    for weight_name, performance_name, lower, objective, target in portfolios:
        weights = np.array([ns[weight_name][symbol] for symbol in prices.columns])
        np.testing.assert_allclose(weights.sum(), 1, atol=1e-6)
        assert weights.min() >= lower - 1e-6 and weights.max() <= 1 + 1e-6
        ret, vol = weights @ mu, np.sqrt(weights @ covariance @ weights)
        np.testing.assert_allclose(ns[performance_name], [ret, vol, (ret - 0.02) / vol], atol=1e-8)
        if target is not None:
            assert ret >= target - 1e-6
        _, optimum = independent_optimum(mu, covariance, lower, objective, target)
        actual = vol ** 2 if objective == "variance" else -(ret - 0.02) / vol
        np.testing.assert_allclose(actual, optimum, atol=2e-6, err_msg=weight_name)

    # Check all 100 frontier points independently, including both endpoints.
    for frame, lower in [(ns["frontier_bounded_short"], -1), (ns["frontier_long_only"], 0)]:
        assert len(frame) == 50
        assert np.all(np.diff(frame["expected_return"]) >= -1e-6)
        assert np.all(np.diff(frame["volatility"]) >= -1e-6)
        for point in frame.itertuples():
            weights, variance = independent_optimum(mu, covariance, lower, "variance", point.target_return)
            np.testing.assert_allclose(point.volatility ** 2, variance, atol=2e-6)
            np.testing.assert_allclose(point.expected_return, weights @ mu, atol=2e-6)
            np.testing.assert_allclose(point.sharpe_ratio, (point.expected_return - .02) / point.volatility)
    assert ns["bounded_short_sharpe_perf"][2] >= ns["long_only_sharpe_perf"][2] - 1e-6
    assert ns["bounded_short_minvol_perf"][1] <= ns["long_only_minvol_perf"][1] + 1e-6

    allocation = ns["allocation"]
    assert all(isinstance(n, (int, np.integer)) and n >= 0 for n in allocation.values())
    np.testing.assert_allclose(ns["latest_prices"].loc[prices.columns], prices.iloc[-1])
    invested = sum(n * float(prices[symbol].iloc[-1]) for symbol, n in allocation.items())
    assert 0 <= invested <= ns["portfolio_value"] + 1e-7
    np.testing.assert_allclose(invested + ns["leftover_cash"], ns["portfolio_value"], atol=1e-7)
    return {"observations": len(monthly), "annual_means": dict(zip(prices.columns, mu)),
            "allocation": allocation, "invested": invested, "cash": ns["leftover_cash"]}


def main():
    # Full rich-output execution is tested separately with nbclient in CI.
    os.environ["MPLBACKEND"] = "Agg"
    os.chdir(ROOT)
    for stem, validate in [("lab1", validate_lab1), ("lab2", validate_lab2)]:
        notebook = json.loads((ROOT / f"{stem}-notebook.ipynb").read_text(encoding="utf-8"))
        namespace = {"__name__": "__main__"}
        with redirect_stdout(StringIO()):
            for index, cell in enumerate(notebook["cells"]):
                if cell["cell_type"] == "code":
                    exec(compile("".join(cell["source"]), f"{stem}:cell{index}", "exec"), namespace)
        print(stem, json.dumps(validate(namespace), indent=2))


if __name__ == "__main__":
    main()
