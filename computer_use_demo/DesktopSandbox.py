from e2b_desktop import Sandbox

class DesktopSandbox(Sandbox):
    def is_absolute(self, path: str) -> bool:
        """Check if the given path is absolute."""
        return path.startswith("/")

    def exists(self, path: str) -> bool:
        """Check if the given path exists."""
        result = self.commands.run(f"ls {path}")
        return result.exitCode == 0

    def is_dir(self, path: str) -> bool:
        """Check if the given path points to a directory."""
        result = self.commands.run(f"test -d {path}")
        return result.exitCode == 0
