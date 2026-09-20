"""Expose the pinned Notebook MCP file tools through current FastMCP 2 APIs.

Upstream 0.9.0's CLI banner fails for long project paths and its server uses
obsolete FastMCP constructor/registration arguments. Reuse its providers,
with standard tool registration and no separate-Jupyter execution tool.
"""

import argparse
import inspect
from pathlib import Path
import sys

from fastmcp import FastMCP
from loguru import logger
from the_notebook_mcp.core.config import ServerConfig
from the_notebook_mcp.tools import (
    CellToolsProvider, FileToolsProvider, InfoToolsProvider,
    MetadataToolsProvider, OutputToolsProvider,
)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    config = ServerConfig(argparse.Namespace(
        command="start", transport="stdio", allow_root_dirs=[str(root)],
        log_dir=str(root / ".tools/notebook-mcp/logs"), log_level="WARNING",
    ))
    logger.remove()
    logger.add(sys.stderr, level="WARNING")
    server = FastMCP("Corporate Finance Notebook Tools", instructions=(
        "Read and edit saved notebook files. Save in VS Code first and avoid "
        "simultaneous edits. This server has no access to the live VS Code "
        "kernel; students run cells in the notebook interface."
    ))
    for provider_class in (CellToolsProvider, FileToolsProvider, InfoToolsProvider,
                           MetadataToolsProvider, OutputToolsProvider):
        provider = provider_class(config)
        for name, method in inspect.getmembers(provider, inspect.iscoroutinefunction):
            if name.startswith("notebook_") and name != "notebook_execute_cell":
                server.tool()(method)
    server.run(transport="stdio", show_banner=False)
