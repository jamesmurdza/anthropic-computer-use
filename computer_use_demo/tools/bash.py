import asyncio
from typing import ClassVar, Literal, Optional
from e2b.sandbox.commands.command_handle import PtySize
from anthropic.types.beta import BetaToolBash20241022Param
from DesktopSandbox import DesktopSandbox
from e2b import CommandHandle
from .base import BaseAnthropicTool, CLIResult, ToolError, ToolResult
import time


class _BashSession:
    """A session of a bash shell."""

    _started: bool
    sandbox: DesktopSandbox
    _timed_out: bool
    pty: CommandHandle | None
    _output_buffer: bytes
    _timeout: int = 120  # seconds

    def __init__(self, desktop: DesktopSandbox):
        self._started = False
        self._timed_out = False
        self.sandbox = desktop
        self.pty = None
        self._output_buffer = b""
        super().__init__()

    async def start(self):
        if self._started:
            return

        try:
            # Create PTY with specified size
            size = PtySize(rows=20, cols=80)
            self.pty: CommandHandle = await self.sandbox.pty.create(
                size=size,
                user="user",
                timeout=self._timeout,
                on_data=lambda data: self.on_data(data),
            )
            self._started = True

        except Exception as e:
            raise ToolError(f"Failed to start bash session: {str(e)}") from None

    async def stop(self):
        """Close the terminal, killing the PTY process."""
        if not self._started:
            raise ToolError("Session has not started.")
        if self.pty:
            try:
                await self.sandbox.pty.kill(self.pty.pid)
                self.pty = None
                self._started = False
                self._output_buffer = b""
            except Exception as e:
                print(f"Error closing PTY: {str(e)}")
        else:
            print("Cannot kill PTY because it is not initialized.")

    async def on_data(self, data: bytes):
        """Handle incoming data from the PTY."""
        try:
            # Process the incoming data as needed
            self._output_buffer += data
        except Exception as e:
            print(f"Error handling data: {str(e)}")

    async def run(self, command: str) -> CLIResult:
        """Execute a command in the bash shell using the sandbox."""
        if not self._started:
            await self.start()
        if self._timed_out:
            raise ToolError(
                f"timed out: bash has not returned in {self._timeout} seconds and must be restarted",
            )

        try:
            # Clear output buffer before new command
            self._output_buffer = b""

            # Add newline if not present
            if not command.endswith("\n"):
                command += "\n"

            # Send command to PTY
            if self.pty:
                await self.sandbox.pty.send_stdin(self.pty.pid, command.encode())

                # Allow time for command execution
                await asyncio.sleep(1.5)

                return CLIResult(output=self._output_buffer.decode(), error="")
            else:
                raise ToolError("PTY not initialized")

        except Exception as e:
            error_msg = f"Command execution failed: {str(e)}"
            return CLIResult(output="", error=error_msg)


class BashTool(BaseAnthropicTool):
    """
    A tool that allows the agent to run bash commands in a sandboxed environment.
    The tool parameters are defined by Anthropic and are not editable.
    """

    _session: Optional[_BashSession] = None
    name: ClassVar[Literal["bash"]] = "bash"
    api_type: ClassVar[Literal["bash_20241022"]] = "bash_20241022"
    desktop: DesktopSandbox

    def __init__(self, desktop: DesktopSandbox):
        self.desktop = desktop
        super().__init__()

    async def __call__(
        self, command: str | None = None, restart: bool = False, **kwargs
    ) -> ToolResult:
        if self._session is None:
            if BashTool._session:
                await BashTool._session.stop()
            print("CREATE NEWW ONE")
            self._session = _BashSession(self.desktop)
            BashTool._session = self._session

        if restart:
            if self._session:
                await self._session.stop()
            self._session = _BashSession(self.desktop)
            return ToolResult(system="tool has been restarted.")

        if command is not None:
            result = await self._session.run(command)
            return ToolResult(
                output=result.output, error=result.error if result.error else None
            )

        raise ToolError("no command provided.")

    def to_params(self) -> BetaToolBash20241022Param:
        return {
            "type": self.api_type,
            "name": self.name,
        }
