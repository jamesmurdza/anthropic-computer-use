from e2b_desktop import Sandbox
from pathlib import Path


class DesktopSandbox(Sandbox):
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
