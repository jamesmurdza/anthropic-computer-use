from e2b import AsyncSandbox
from pathlib import Path

import uuid
from typing import Callable, Optional


class DesktopSandbox(AsyncSandbox):
    def screenshot(
        self,
        name: str,
        on_stdout: Optional[Callable[[str], None]] = None,
        on_stderr: Optional[Callable[[str], None]] = None,
    ):
        """
        Take a screenshot and save it to the given name.
        :param name: The name of the screenshot file to save locally.
        """
        screenshot_path = f"/home/user/screenshot-{uuid.uuid4()}.png"

        self.commands.run(
            f"scrot --pointer {screenshot_path}",
            on_stderr=on_stderr,
            on_stdout=on_stdout,
            cwd="/home/user",
        )

        with open(name, "wb") as f:
            file = self.files.read(screenshot_path, format="bytes")
            f.write(file)

    def is_absolute(self, path: Path) -> bool:
        """Check if the given path is absolute."""
        return path.is_absolute()

    def exists(self, path: Path) -> bool:
        """Check if the given path exists."""
        return self.files.exists(path.as_posix())

    def is_dir(self, path: Path) -> bool:
        """Check if the given path points to a directory."""
        try:
            self.commands.run(f"test -d {path}")
            return True
        except Exception:
            return False
