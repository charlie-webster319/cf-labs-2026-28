"""Execute the teaching notebooks and extract every plot for visual review."""

import base64
import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "validation"


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    # Keep plots deterministic and independent of a desktop display.
    os.environ["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"
    count = 0
    for source in sorted(ROOT.glob("lab*-notebook.ipynb")):
        notebook = nbformat.read(source, as_version=4)
        nbformat.validate(notebook)
        print(f"Executing {source.name}", flush=True)
        NotebookClient(
            notebook, timeout=300, kernel_name="cflabs",
            resources={"metadata": {"path": str(ROOT)}},
        ).execute()
        nbformat.write(notebook, OUTPUT / source.name)
        for cell_number, cell in enumerate(notebook.cells):
            for output_number, output in enumerate(cell.get("outputs", [])):
                if output.output_type == "error":
                    raise AssertionError(f"{source.name} cell {cell_number}: {output}")
                data = output.get("data", {})
                if "image/png" in data:
                    path = OUTPUT / f"{source.stem}-cell-{cell_number:02d}-{output_number}.png"
                    path.write_bytes(base64.b64decode(data["image/png"]))
                    count += 1
                if output.output_type == "stream" and output.get("name") == "stderr":
                    print(f"{source.name} cell {cell_number}: {output.text}", flush=True)
        print(f"Completed {source.name}", flush=True)
    print(f"Extracted {count} plots to {OUTPUT}", flush=True)


if __name__ == "__main__":
    main()
