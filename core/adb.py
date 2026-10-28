import os
import subprocess
import time
from typing import List, Tuple, Optional

class ADBClient:
    """
    Robust ADB client for Fire TV management over Wi-Fi or USB.
    Handles device targeting, auto-detection, auto-reconnect, and error checking.
    """
    def __init__(self, device_ip: Optional[str] = None, port: int = 5555):
        # Allow specifying device IP via parameter or FIRETV_IP environment variable
        self._explicit_ip = device_ip is not None
        self.device_ip = device_ip or os.environ.get("FIRETV_IP", "192.168.0.236")
        self.port = port
        self.device_serial = f"{self.device_ip}:{port}" if ":" not in self.device_ip else self.device_ip
        self.adb_bin = self._find_adb()
        self._connected = False

    def _find_adb(self) -> str:
        # Check custom environment variable
        if os.environ.get("ADB_PATH") and os.path.exists(os.environ["ADB_PATH"]):
            return os.environ["ADB_PATH"]

        # Prioritize modern official Android SDK platform-tools over legacy PATH entries
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        home = os.path.expanduser("~")
        preferred_sdk_paths = [
            os.path.join(local_app_data, "Android", "Sdk", "platform-tools", "adb.exe") if local_app_data else "",
            os.path.join(home, "Android", "Sdk", "platform-tools", "adb"),
            os.path.join(home, "Library", "Android", "sdk", "platform-tools", "adb"),
            r"C:\platform-tools\adb.exe",
        ]
        for candidate in preferred_sdk_paths:
            if candidate and os.path.exists(candidate):
                return candidate

        # Fall back to PATH
        import shutil
        adb_path = shutil.which("adb")
        if adb_path:
            return adb_path

        # Fall back to other common locations
        fallback_candidates = [
            r"C:\adb\adb.exe",
            "/usr/bin/adb",
            "/usr/local/bin/adb",
            "/opt/homebrew/bin/adb",
        ]
        for candidate in fallback_candidates:
            if candidate and os.path.exists(candidate):
                return candidate

        raise RuntimeError("ADB executable not found. Please install Android Platform Tools or set ADB_PATH.")

    def run(self, args: List[str], timeout: int = 30) -> Tuple[int, str, str]:
        cmd = [self.adb_bin] + args
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return res.returncode, res.stdout, res.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def connect(self, force: bool = False) -> bool:
        """Connect to device and ensure state is 'device'."""
        if self._connected and not force:
            return True

        # Check existing devices first (e.g. USB or pre-connected Wi-Fi)
        code, out, _ = self.run(["devices"])
        active_devices = []
        for line in out.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1] == "device":
                active_devices.append(parts[0])

        # If our specified serial is already attached and ready
        if self.device_serial in active_devices:
            self._connected = True
            return True

        # If user hasn't explicitly specified a custom IP and exactly 1 device is attached
        if not os.environ.get("FIRETV_IP") and not self._explicit_ip and len(active_devices) == 1:
            self.device_serial = active_devices[0]
            self._connected = True
            return True

        # Attempt to connect to specified serial over network
        self.run(["connect", self.device_serial], timeout=10)
        code, out, _ = self.run(["devices"])
        for line in out.splitlines():
            if self.device_serial in line and "device" in line and "unauthorized" not in line:
                self._connected = True
                return True
        self._connected = False
        return False

    def shell(self, cmd_str: str, timeout: int = 30) -> Tuple[int, str, str]:
        """Execute a shell command on the target Fire TV."""
        if not self._connected:
            self.connect()
        code, out, err = self.run(["-s", self.device_serial, "shell", cmd_str], timeout=timeout)
        if code != 0 and any(msg in err for msg in ["device not found", "device offline"]):
            self.connect(force=True)
            return self.run(["-s", self.device_serial, "shell", cmd_str], timeout=timeout)
        return code, out, err

    def get_prop(self, prop: str) -> str:
        _, out, _ = self.shell(f"getprop {prop}")
        return out.strip()

    def get_installed_packages(self) -> List[str]:
        _, out, _ = self.shell("pm list packages")
        packages = []
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("package:"):
                packages.append(line[len("package:"):])
        return sorted(packages)

    def get_disabled_packages(self) -> List[str]:
        _, out, _ = self.shell("pm list packages -d")
        packages = []
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("package:"):
                packages.append(line[len("package:"):])
        return sorted(packages)

    def is_package_installed(self, pkg: str) -> bool:
        code, out, _ = self.shell(f"pm path {pkg}")
        return "package:" in out
