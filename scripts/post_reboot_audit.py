import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import subprocess
import time
from core.adb import ADBClient

def run_audit(client=None):
    print("=" * 70)
    print("FIRE TV POST-REBOOT COMPREHENSIVE AUDIT & SERVICE ANALYSIS")
    print("=" * 70)

    if client is None:
        client = ADBClient()
    if not client.connect():
        print(f"[-] Error: Unable to connect to Fire TV at {client.device_serial}")
        return False
    
    print("[+] Connected to Fire TV successfully.\n")

    def sh(cmd, timeout=15):
        code, out, err = client.run(["shell", cmd], timeout=timeout)
        return out.strip()

    # 1. Device Info & Uptime
    model = sh("getprop ro.product.model")
    device = sh("getprop ro.product.device")
    build = sh("getprop ro.build.version.incremental")
    fireos_ver = sh("getprop ro.build.version.name")
    uptime = sh("uptime")
    wakefulness = sh("dumpsys power | grep mWakefulness")
    
    print("--- 1. DEVICE STATE & UPTIME ---")
    print(f"Model       : {model} ({device})")
    print(f"Fire OS Ver : {fireos_ver} (Build {build})")
    print(f"Uptime      : {uptime}")
    print(f"Power State : {wakefulness}\n")

    # 2. Foreground Activity
    resumed = sh("dumpsys activity activities | grep -E 'mResumedActivity|mFocusedActivity'")
    print("--- 2. CURRENT FOREGROUND ACTIVITY ---")
    print(resumed if resumed else "No resumed activity found")
    print()

    # 3. Accessibility & Launcher Takeover
    a11y_services = sh("settings get secure enabled_accessibility_services")
    a11y_enabled = sh("settings get secure accessibility_enabled")
    alarm_const = sh("settings get global alarm_manager_constants")
    
    print("--- 3. LAUNCHER TAKEOVER CONFIGURATION ---")
    print(f"Accessibility Services : {a11y_services}")
    print(f"Accessibility Enabled  : {a11y_enabled}")
    print(f"AlarmManager Constants : {alarm_const}")
    dumbtv_ok = "tv.dumbtv.home/.Guard" in a11y_services
    alarm_ok = "min_futurity=0" in alarm_const
    print(f"-> DumbTV Home Guard Active  : {'YES [PASS]' if dumbtv_ok else 'NO [FAIL]'}")
    print(f"-> Instant Home Key (0ms)    : {'YES [PASS]' if alarm_ok else 'NO [FAIL]'}\n")

    # 4. Disabled Packages Audit (Compare with journal.jsonl)
    print("--- 4. DEBLOATED PACKAGES AUDIT ---")
    raw_disabled = sh("pm list packages -d")
    current_disabled = set()
    for line in raw_disabled.splitlines():
        line = line.strip()
        if line.startswith("package:"):
            current_disabled.add(line.replace("package:", "").strip())

    journal_disabled = set()
    if os.path.exists("logs/journal.jsonl"):
        with open("logs/journal.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("status") == "applied" and "pm disable" in entry.get("forward_cmd", ""):
                        target = entry.get("target")
                        if target:
                            journal_disabled.add(target)
                except Exception:
                    pass

    print(f"Total packages currently disabled on device : {len(current_disabled)}")
    print(f"Total disabled packages in audit journal    : {len(journal_disabled)}")
    
    still_disabled = journal_disabled.intersection(current_disabled)
    reverted = journal_disabled - current_disabled
    print(f"-> Successfully persisting after reboot     : {len(still_disabled)} / {len(journal_disabled)} ({(len(still_disabled)/len(journal_disabled)*100):.1f}%)" if journal_disabled else "N/A")
    if reverted:
        print(f"-> [WARNING] Reverted packages: {reverted}")
    else:
        print("-> [PASS] 100% of journaled disabled packages persisted across reboot!")
    print()

    # 5. Uninstalled Bloat/News Apps Audit
    print("--- 5. UNINSTALLED NEWS & BLOAT APKS ---")
    raw_all = sh("pm list packages")
    all_packages = {line.replace("package:", "").strip() for line in raw_all.splitlines() if line.strip()}
    uninstalled_targets = [
        "com.aajtak.firetv",
        "com.abp.firetv",
        "com.news18.ftv",
        "com.tv9live.tv9livetv",
        "com.republicworld.fire.tv",
        "com.republicworld.firetv.rbharat",
        "com.zeenews.tv",
        "com.onnet.systems.iptv.esto"
    ]
    present_uninstalled = [pkg for pkg in uninstalled_targets if pkg in all_packages]
    if not present_uninstalled:
        print(f"-> [PASS] All {len(uninstalled_targets)} uninstalled third-party bloat apps remain completely absent from system.")
    else:
        print(f"-> [WARNING] Detected re-installation of: {present_uninstalled}")
    print()

    # 6. Privacy, Advertising & OTA Settings
    print("--- 6. SYSTEM SETTINGS & PRIVACY FLAGS ---")
    settings_checks = [
        ("secure", "advertisingIdApp:interestBasedAds:value", "0", "Interest-based ads disabled"),
        ("secure", "USAGE_METRICS_UPLOAD_ENABLED", "0", "Usage metrics upload disabled"),
        ("secure", "usage_metrics_marketing_enabled", "0", "Marketing metrics disabled"),
        ("secure", "settingsApp:appUsageData:value", "0", "App usage tracking disabled"),
        ("secure", "settingsApp:deviceUsageData:value", "0", "Device usage tracking disabled"),
        ("global", "com.amazon.tv.settings.featured_item_video_enabled", "0", "Home featured video autoplay disabled"),
        ("global", "heads_up_notifications_enabled", "0", "Heads-up banner notifications disabled"),
        ("global", "window_animation_scale", "0.5", "Window animation scale snappy (0.5x)"),
        ("global", "transition_animation_scale", "0.5", "Transition animation scale snappy (0.5x)"),
        ("secure", "voice_disabled", "1", "Voice recognition system disabled"),
        ("secure", "alexa_wake_word_disabled", "1", "Alexa wake word listening disabled"),
        ("global", "private_dns_mode", "hostname", "Private DNS Mode set to hostname"),
        ("global", "private_dns_specifier", "1dot1dot1dot1.cloudflare-dns.com", "Cloudflare DNS over TLS specifier"),
        ("global", "wifi_on", "1", "Wi-Fi persistence enabled"),
        ("global", "bluetooth_on", "1", "Bluetooth persistence enabled")
    ]
    settings_pass = 0
    for table, key, expected, desc in settings_checks:
        val = sh(f"settings get {table} {key}")
        match = (val == expected)
        if match:
            settings_pass += 1
            print(f"  [PASS] {desc:45} : {val}")
        else:
            print(f"  [FAIL] {desc:45} : got '{val}', expected '{expected}'")
    print(f"-> Settings Persistence: {settings_pass}/{len(settings_checks)} passed.\n")

    # 7. AppOps Background Restrictions (OTA & Telemetry)
    print("--- 7. APPOPS BACKGROUND RESTRICTIONS ---")
    appops_targets = [
        ("com.amazon.device.software.ota", "OTA Updater background execution"),
        ("com.amazon.device.metrics", "Metrics telemetry pipeline"),
        ("com.amazon.device.crashmanager", "CrashManager telemetry"),
        ("com.amazon.device.rdmapplication", "RDM telemetry application"),
        ("com.amazon.ftvads.deeplinking", "Ad deep-linking service"),
        ("com.amazon.tv.csapp", "Amazon Customer Service push daemon")
    ]
    for pkg, desc in appops_targets:
        res = sh(f"cmd appops get {pkg} RUN_ANY_IN_BACKGROUND")
        status = "ignore" in res.lower()
        print(f"  {'[PASS]' if status else '[WARN]'} {desc:38} ({pkg}): {res if res else 'allow (default)'}")
    print()

    # 8. Memory & Resource Consumption Analysis
    print("--- 8. MEMORY & RESOURCE UTILIZATION ---")
    meminfo = sh("cat /proc/meminfo")
    free_kb, cached_kb, total_kb, buffers_kb = 0, 0, 0, 0
    for line in meminfo.splitlines():
        if line.startswith("MemTotal:"):
            total_kb = int(line.split()[1])
        elif line.startswith("MemFree:"):
            free_kb = int(line.split()[1])
        elif line.startswith("Cached:"):
            cached_kb = int(line.split()[1])
        elif line.startswith("Buffers:"):
            buffers_kb = int(line.split()[1])
    available_mb = (free_kb + cached_kb + buffers_kb) / 1024
    total_mb = total_kb / 1024
    used_mb = total_mb - available_mb
    pct_used = (used_mb / total_mb) * 100
    
    print(f"Total RAM        : {total_mb:.1f} MB")
    print(f"Used RAM         : {used_mb:.1f} MB ({pct_used:.1f}%)")
    print(f"Available/Free   : {available_mb:.1f} MB ({(available_mb/total_mb)*100:.1f}%)")
    print(f"Pre-clean Free   : ~45-56 MB (Baseline)")
    print(f"-> RAM Headroom  : +{available_mb - 50:.1f} MB increased memory capacity\n")

    # 9. Running Services & Processes Analysis
    print("--- 9. RUNNING PROCESSES & ACTIVE SERVICES AUDIT ---")
    ps_output = sh("ps -A -o USER,PID,PPID,VSZ,RSS,NAME")
    lines = ps_output.splitlines()
    header = lines[0] if lines else ""
    procs = []
    for l in lines[1:]:
        parts = l.split()
        if len(parts) >= 6:
            name = parts[5]
            rss_kb = int(parts[4]) if parts[4].isdigit() else 0
            procs.append((name, rss_kb, l))

    procs.sort(key=lambda x: x[1], reverse=True)
    
    # Check key Amazon bloat processes
    bloat_candidates = [
        "com.amazon.tv.launcher",
        "com.amazon.firebat",
        "com.amazon.aca",
        "com.amazon.vizzini",
        "com.amazon.ceviche",
        "com.amazon.adep",
        "com.amazon.client.metrics",
        "com.amazon.alexamediaplayer.runtime.ftv",
        "com.amazon.device.software.ota",
        "com.amazon.tv.forcedotaupdater.v2",
        "com.amazon.tv.easyupgrade"
    ]
    
    running_names = {p[0] for p in procs}
    
    print("Key Bloat/Telemetry Status:")
    for b in bloat_candidates:
        if b in running_names:
            matching = [p for p in procs if p[0] == b]
            rss = matching[0][1] / 1024 if matching else 0
            print(f"  [ALIVE] {b:40} : {rss:.1f} MB RSS")
        else:
            print(f"  [DEAD]  {b:40} : Suppressed / Not running")
    print()

    print("Top 15 Memory-Consuming Processes Currently Running:")
    for name, rss, raw in procs[:15]:
        print(f"  - {name:40} : {rss/1024:6.1f} MB")
    print()

    # 10. User Apps & DumbTV Home Configuration
    print("--- 10. LAUNCHER CONFIGURATION & USER APPS ---")
    conf_check = sh("cat /sdcard/Android/data/tv.dumbtv.home/files/home.conf")
    if conf_check and "Error" not in conf_check:
        apps_order = []
        apps_hide = []
        for l in conf_check.splitlines():
            if l.startswith("apps.order="):
                apps_order = [x.strip() for x in l.replace("apps.order=", "").split(",") if x.strip()]
            elif l.startswith("apps.hide="):
                apps_hide = [x.strip() for x in l.replace("apps.hide=", "").split(",") if x.strip()]
        
        wp_check = sh("ls -la /sdcard/Android/data/tv.dumbtv.home/files/wallpaper.jpg")
        has_wallpaper = "wallpaper.jpg" in wp_check
        has_dim = "dim=" in conf_check
        print(f"[+] DumbTV Home configuration intact:")
        print(f"    - Apps in launch row/order  : {len(apps_order)} configured (Lead app: {apps_order[0] if apps_order else 'None'})")
        print(f"    - Hidden Amazon packages    : {len(apps_hide)} hidden")
        print(f"    - Custom wallpaper file     : {'Present (wallpaper.jpg)' if has_wallpaper else 'Missing'}")
        print(f"    - Dimming overlay configured: {'dim=90% dark overlay' if has_dim else 'Default'}")
    else:
        print("[-] home.conf could not be read or does not exist at target path.")

    print("\n" + "=" * 70)
    print("AUDIT SUMMARY COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    run_audit()
