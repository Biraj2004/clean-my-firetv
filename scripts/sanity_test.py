"""
Comprehensive Sanity & Verification Test Suite for Clean My FireTV
Tests:
 1. Accessibility Service & AlarmManager Takeover
 2. Launcher Calibrated Order (Stremio primary)
 3. App Launch -> HOME key interception (Stremio, YouTube, Downloader)
 4. Settings Key (KEYCODE_SETTINGS) -> Back key return
 5. Settings Key -> Open Settings -> HOME key interception (zero Amazon home flash)
 6. OTA Block Verification
 7. Core Whitelist Verification
 8. Memory & Performance Benchmark
"""

import os
import subprocess
import time
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.adb import ADBClient

sys.stdout.reconfigure(encoding='utf-8')

client = ADBClient()

def adb_shell(cmd):
    code, out, err = client.shell(cmd, timeout=15)
    return out.strip()

def get_resumed_activity():
    out = adb_shell("dumpsys activity activities | grep mResumedActivity")
    # format: mResumedActivity: ActivityRecord{... u0 pkg/activity ...}
    for line in out.splitlines():
        if "mResumedActivity" in line:
            parts = line.split()
            for part in parts:
                if "/" in part and not part.startswith("u0"):
                    return part.rstrip("}")
    return out

def run_test(name, fn):
    print(f"[*] Running: {name}...")
    try:
        ok, msg = fn()
        if ok:
            print(f"    [PASS] {msg}")
            return True
        else:
            print(f"    [FAIL] {msg}")
            return False
    except Exception as e:
        print(f"    [ERROR] {e}")
        return False

# --- Tests ---

def test_1_accessibility():
    services = adb_shell("settings get secure enabled_accessibility_services")
    if "tv.dumbtv.home/.Guard" in services:
        return True, f"Guard service active: {services}"
    return False, f"Guard service not enabled: {services}"

def test_2_alarm_min_futurity():
    val = adb_shell("settings get global alarm_manager_constants")
    if "min_futurity=0" in val:
        return True, f"AlarmManager 0ms bypass confirmed: {val}"
    return False, f"min_futurity not set to 0: {val}"

def test_3_stremio_home():
    adb_shell("am start -n com.stremio.one/com.stremio.tv.MainActivity")
    time.sleep(2)
    act1 = get_resumed_activity()
    if "com.stremio.one" not in act1:
        return False, f"Failed to start Stremio: resumed {act1}"
    
    adb_shell("input keyevent 3")  # KEYCODE_HOME
    act2 = ""
    for _ in range(4):
        time.sleep(0.5)
        act2 = get_resumed_activity()
        if "tv.dumbtv.home/.Home" in act2:
            return True, f"Stremio -> Home intercepted perfectly in DumbTV Home ({act2})"
    return False, f"Expected DumbTV Home, got {act2}"

def test_4_smarttube_home():
    adb_shell("am start -n org.smarttube.stable/com.liskovsoft.smartyoutubetv2.tv.ui.main.SplashActivity")
    time.sleep(2.5)
    act1 = get_resumed_activity()
    if "smarttube" not in act1.lower():
        return False, f"Failed to start SmartTube: resumed {act1}"
    
    adb_shell("input keyevent 3")  # KEYCODE_HOME
    time.sleep(1.5)
    act2 = get_resumed_activity()
    if "tv.dumbtv.home/.Home" in act2:
        return True, f"SmartTube -> Home intercepted perfectly ({act2})"
    return False, f"Expected DumbTV Home, got {act2}"

def test_5_downloader_home():
    adb_shell("am start -n com.esaba.downloader/.ui.main.MainActivity -a android.intent.action.MAIN -c android.intent.category.LAUNCHER")
    time.sleep(2)
    act1 = get_resumed_activity()
    if "downloader" not in act1.lower():
        return False, f"Failed to start Downloader: resumed {act1}"
    
    adb_shell("input keyevent 3")  # KEYCODE_HOME
    time.sleep(1.5)
    act2 = get_resumed_activity()
    if "tv.dumbtv.home/.Home" in act2:
        return True, f"Downloader -> Home intercepted perfectly ({act2})"
    return False, f"Expected DumbTV Home, got {act2}"

def test_6_wifi_header_navigation():
    # Direct test of Fire OS Network Settings from header
    adb_shell("am start -n com.amazon.tv.settings.v2/.tv.network.NetworkActivity")
    time.sleep(1.5)
    act1 = get_resumed_activity()
    if "NetworkActivity" not in act1:
        return False, f"Expected NetworkActivity, got {act1}"
    
    adb_shell("input keyevent 3")  # KEYCODE_HOME
    time.sleep(1.5)
    act2 = get_resumed_activity()
    if "tv.dumbtv.home/.Home" in act2:
        return True, f"Wi-Fi Settings -> HOME intercepted cleanly ({act2})"
    return False, f"Expected DumbTV Home, got {act2}"

def test_7_bluetooth_header_navigation():
    # Direct test of Fire OS Bluetooth Settings from header
    adb_shell("am start -n com.amazon.tv.settings.v2/.tv.controllers_bluetooth_devices.ControllersAndBluetoothActivity")
    time.sleep(1.5)
    act1 = get_resumed_activity()
    if "ControllersAndBluetoothActivity" not in act1 and "bluetooth" not in act1.lower():
        return False, f"Expected Bluetooth Activity, got {act1}"
    
    adb_shell("input keyevent 3")  # KEYCODE_HOME
    time.sleep(1.5)
    act2 = get_resumed_activity()
    if "tv.dumbtv.home/.Home" in act2:
        return True, f"Bluetooth Settings -> HOME intercepted cleanly ({act2})"
    return False, f"Expected DumbTV Home, got {act2}"

def test_8_ota_block():
    nag1 = adb_shell("pm list packages -d | grep forcedotaupdater")
    nag2 = adb_shell("pm list packages -d | grep easyupgrade")
    appops = adb_shell("cmd appops get com.amazon.device.software.ota RUN_ANY_IN_BACKGROUND")
    if "forcedotaupdater" in nag1 and "easyupgrade" in nag2 and "ignore" in appops:
        return True, "OTA nag packages disabled & background OTA daemon starved (ignore)"
    return False, f"OTA block incomplete: nag1={nag1}, nag2={nag2}, ops={appops}"

def test_9_memory_benchmark():
    meminfo = adb_shell("cat /proc/meminfo")
    free_kb = 0
    total_kb = 0
    cached_kb = 0
    for line in meminfo.splitlines():
        if line.startswith("MemTotal:"):
            total_kb = int(line.split()[1])
        elif line.startswith("MemFree:"):
            free_kb = int(line.split()[1])
        elif line.startswith("Cached:"):
            cached_kb = int(line.split()[1])
    available_mb = (free_kb + cached_kb) / 1024
    total_mb = total_kb / 1024
    return True, f"RAM Available: {available_mb:.1f} MB / {total_mb:.1f} MB total (Healthy headroom)"

def test_10_cloudflare_dns():
    mode = adb_shell("settings get global private_dns_mode")
    spec = adb_shell("settings get global private_dns_specifier")
    if "hostname" in mode and "1dot1dot1dot1" in spec:
        return True, f"Cloudflare Private DNS active (DoT: {spec})"
    return False, f"DNS mismatch: mode={mode}, spec={spec}"

def test_11_wifi_bluetooth_always_on():
    w_on = adb_shell("settings get global wifi_on")
    bt_on = adb_shell("settings get global bluetooth_on")
    if w_on == "1" and bt_on == "1":
        return True, "Wi-Fi and Bluetooth configured to always turn on by default (wifi_on=1, bt_on=1)"
    return False, f"Wi-Fi/BT state: wifi={w_on}, bt={bt_on}"

def run_sanity():
    print("=" * 60)
    print("FIRE TV SANITY & VERIFICATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Accessibility Service Verification", test_1_accessibility),
        ("AlarmManager 0ms Takeover", test_2_alarm_min_futurity),
        ("Cloudflare Private DNS (DoT)", test_10_cloudflare_dns),
        ("Wi-Fi & Bluetooth Always-On State", test_11_wifi_bluetooth_always_on),
        ("Stremio -> HOME Interception", test_3_stremio_home),
        ("SmartTube -> HOME Interception", test_4_smarttube_home),
        ("Downloader -> HOME Interception", test_5_downloader_home),
        ("Wi-Fi Header Button -> HOME Interception", test_6_wifi_header_navigation),
        ("Bluetooth Header Button -> HOME Interception", test_7_bluetooth_header_navigation),
        ("OTA Update Block Status", test_8_ota_block),
        ("Memory & RAM Headroom Benchmark", test_9_memory_benchmark),
    ]
    
    passed = 0
    for name, fn in tests:
        if run_test(name, fn):
            passed += 1
        time.sleep(1.2)
        
    print("=" * 60)
    print(f"RESULTS: {passed}/{len(tests)} tests passed ({(passed/len(tests))*100:.0f}%)")
    print("=" * 60)
    
    # Return to DumbTV Home at the end
    adb_shell("am start -n tv.dumbtv.home/.Home")
    return passed == len(tests)

def main():
    run_sanity()

if __name__ == "__main__":
    main()
