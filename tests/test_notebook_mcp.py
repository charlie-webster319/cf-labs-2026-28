"""Exercise the real optional MCP server without an AI account or lab edits."""

import asyncio
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
HAS_MCP = importlib.util.find_spec("the_notebook_mcp") is not None


@unittest.skipUnless(HAS_MCP, "Install the optional notebook-mcp group to test MCP")
class NotebookMCPTests(unittest.TestCase):
    def test_both_client_configs_read_edit_outputs_and_reject_outside_paths(self):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        import nbformat

        claude = json.loads((ROOT / ".mcp.json").read_text())["mcpServers"]["jupyter"]
        codex = tomllib.loads((ROOT / ".codex/config.toml").read_text())["mcp_servers"]["jupyter"]
        (ROOT / "outputs").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="MCP notebook with spaces ", dir=ROOT / "outputs") as folder, \
             tempfile.TemporaryDirectory(prefix="outside lab ") as outside:
            notebook = Path(folder) / "practice notebook.ipynb"
            forbidden = Path(outside) / "private.ipynb"
            original = nbformat.v4.new_notebook(cells=[
                nbformat.v4.new_markdown_cell("Keep the finance explanation."),
                nbformat.v4.new_code_cell("2 + 2", execution_count=1, outputs=[
                    nbformat.v4.new_output("execute_result", data={"text/plain": "4"}, execution_count=1)
                ]),
            ])
            nbformat.write(original, forbidden)
            forbidden_before = forbidden.read_bytes()

            async def exercise(config):
                nbformat.write(original, notebook)
                env = os.environ.copy()
                env["PATH"] = str(ROOT / ".tools/uv") + os.pathsep + env["PATH"]
                command = shutil.which(config["command"], path=env["PATH"])
                self.assertIsNotNone(command, "uv must be available to the MCP client")
                params = StdioServerParameters(command=command, args=config["args"], cwd=str(ROOT), env=env)
                with (Path(folder) / "server.log").open("w") as log:
                    async with stdio_client(params, errlog=log) as (reader, writer):
                        async with ClientSession(reader, writer) as session:
                            await session.initialize()
                            names = {tool.name for tool in (await session.list_tools()).tools}
                            self.assertTrue({"notebook_read", "notebook_edit_cell", "notebook_read_cell_output"} <= names)
                            self.assertNotIn("notebook_execute_cell", names)
                            read = await session.call_tool("notebook_read", {"notebook_path": str(notebook)})
                            self.assertFalse(read.isError, read)
                            self.assertIn("Keep the finance explanation", str(read.content))
                            output = await session.call_tool("notebook_read_cell_output", {
                                "notebook_path": str(notebook), "cell_index": 1})
                            self.assertFalse(output.isError, output)
                            self.assertIn("text/plain", str(output.content))
                            edit = await session.call_tool("notebook_edit_cell", {
                                "notebook_path": str(notebook), "cell_index": 1, "source": "3 + 3"})
                            self.assertFalse(edit.isError, edit)
                            changed = nbformat.read(notebook, as_version=4)
                            nbformat.validate(changed)
                            self.assertEqual(changed.cells[0], original.cells[0])
                            self.assertEqual(changed.cells[1].source, "3 + 3")
                            denied = await session.call_tool("notebook_edit_cell", {
                                "notebook_path": str(forbidden), "cell_index": 1, "source": "changed"})
                            self.assertTrue(denied.isError or "error" in str(denied.content).lower(), denied)
                            self.assertEqual(forbidden.read_bytes(), forbidden_before)

            for name, config in (("Claude Code", claude), ("Codex", codex)):
                with self.subTest(client=name):
                    asyncio.run(asyncio.wait_for(exercise(config), timeout=60))


if __name__ == "__main__":
    unittest.main()
