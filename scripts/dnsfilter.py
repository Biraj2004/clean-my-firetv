import os
import sys
import tempfile
import urllib.request
import time

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.adb import ADBClient
from core.journal import ActionJournal

DNSFILTER_PKG = "dnsfilter.android"
DNSFILTER_ACTIVITY = "dnsfilter.android/dnsfilter.android.DNSFilterActivity"
DNSFILTER_DOWNLOAD_URL = "https://f-droid.org/repo/dnsfilter.android_1506105.apk"

AMAZON_OTA_DOMAINS = [
    # Dedicated Amazon OTA Update Servers
    "softwareupdates.amazon.com",
    "fota.amazon.com",
    "amzdigitaldownloads.edgesuite.net",
    "updates.amazon.com",
    "d1s31zyz7dcc2d.cloudfront.net",
    # Amazon Device Telemetry & ACR
    "device-metrics-us.amazon.com",
    "device-metrics-us-2.amazon.com",
    "unagi-na.amazon.com",
    "unagi.amazon.com",
    "fls-na.amazon.com",
    "aan.amazon.com",
    # Universal In-App Ad Networks (Unity Ads, AdMob, AppLovin, Wortise)
    "unityads.unity3d.com",
    "config.unityads.unity3d.com",
    "auction.unityads.unity3d.com",
    "webview.unityads.unity3d.com",
    "adserver.unityads.unity3d.com",
    "googleads.g.doubleclick.net",
    "pagead2.googlesyndication.com",
    "pubads.g.doubleclick.net",
    "adservice.google.com",
    "d.applovin.com",
    "a.applovin.com",
    "init.startappservice.com",
    "config.inmobi.com",
    "api.wortise.com",
    "sdk.cas.ai",
    "ads.vungle.com",
]

HAGEZI_AMAZON_TRACKER_URL = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/native.amazon-onlydomains.txt"

def setup_dnsfilter(adb: ADBClient, journal: ActionJournal):
    print("[*] Starting personalDNSfilter setup (Airtight OTA & Telemetry Blocker)...")
    if not adb.connect():
        print("[-] Device not connected.")
        return False

    # 1. Download personalDNSfilter APK if not installed
    is_installed = adb.is_package_installed(DNSFILTER_PKG)
    if is_installed:
        print(f"[*] {DNSFILTER_PKG} is already installed on the Fire TV.")
    else:
        print("[1/4] Downloading personalDNSfilter from official release...")
        tmp_dir = tempfile.gettempdir()
        apk_dest = os.path.join(tmp_dir, "personalDNSfilter.apk")
        try:
            req = urllib.request.Request(
                DNSFILTER_DOWNLOAD_URL,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp, open(apk_dest, "wb") as out_f:
                out_f.write(resp.read())
            print(f"    Downloaded successfully ({os.path.getsize(apk_dest)} bytes).")
        except Exception as e:
            print(f"[-] Failed to download personalDNSfilter: {e}")
            return False

        print("[2/4] Installing personalDNSfilter on Fire TV...")
        code, out, err = adb.run(["-s", adb.device_serial, "install", "-r", apk_dest])
        if "Success" in out:
            print("    [+] personalDNSfilter installed successfully.")
            journal.log_action(
                category="dnsfilter",
                target=DNSFILTER_PKG,
                forward_cmd=f"adb install -r {apk_dest}",
                reverse_cmd=f"pm uninstall {DNSFILTER_PKG}",
                description="Install personalDNSfilter (local DNS ad/OTA blocker)"
            )
        else:
            print(f"[!] Install output: {out} {err}")

        # Clean up temporary APK
        try:
            os.remove(apk_dest)
        except OSError:
            pass

    # 2. Configure VPN permission and disable competing DoT private DNS
    print("[3/5] Permitting VPN activation and harmonizing DNS routing...")
    adb.shell("cmd appops set dnsfilter.android ACTIVATE_VPN allow")
    adb.shell("settings put global private_dns_mode off")
    journal.log_action(
        category="dnsfilter",
        target="global:private_dns_mode",
        forward_cmd="settings put global private_dns_mode off",
        reverse_cmd="settings put global private_dns_mode hostname",
        description="Disable native DoT to prevent conflict with local personalDNSfilter VPN"
    )

    # 3. Push Custom Filter Configuration & Amazon Blocklist
    print("[4/5] Configuring Amazon OTA and Telemetry blocklists...")
    target_dirs = [
        "/sdcard/Android/data/dnsfilter.android/files",
        "/sdcard/Android/data/dnsfilter.android/files/PersonalDNSFilter",
        "/sdcard/personalDNSfilter"
    ]
    for d in target_dirs:
        adb.shell(f"mkdir -p {d}")

    # Build local additionalHosts.txt & filter.txt
    blocklist_content = "# DumbTV Amazon OTA & Telemetry Blocklist\n"
    for domain in AMAZON_OTA_DOMAINS:
        blocklist_content += f"{domain}\n"

    tmp_filter = os.path.join(tempfile.gettempdir(), "filter.txt")
    with open(tmp_filter, "w", encoding="utf-8") as f:
        f.write(blocklist_content)

    for d in target_dirs:
        adb.run(["-s", adb.device_serial, "push", tmp_filter, f"{d}/filter.txt"])
        adb.run(["-s", adb.device_serial, "push", tmp_filter, f"{d}/additionalHosts.txt"])
    print("    [+] Pushed OTA update domain blocklist to additionalHosts.txt.")

    # Build dnsfilter.conf
    conf_content = f"""# personalDNSfilter configuration for Fire TV
enableFilter = true
autoStart = true
detectDNS = false
filterUpdateInterval = 24
dnsServer = 1.1.1.1, 1.0.0.1
customDNS = 1.1.1.1, 1.0.0.1
filterSources = {HAGEZI_AMAZON_TRACKER_URL}
"""
    tmp_conf = os.path.join(tempfile.gettempdir(), "dnsfilter.conf")
    with open(tmp_conf, "w", encoding="utf-8") as f:
        f.write(conf_content)

    for d in target_dirs:
        adb.run(["-s", adb.device_serial, "push", tmp_conf, f"{d}/dnsfilter.conf"])
    print("    [+] Pushed configuration (dnsfilter.conf) with Cloudflare upstream and HaGeZi tracker list.")

    # 4. Clean up temp files
    try:
        os.remove(tmp_filter)
        os.remove(tmp_conf)
    except OSError:
        pass

    # 5. Launch personalDNSfilter to initialize
    print("[5/5] Starting personalDNSfilter background engine...")
    adb.shell(f"am start -n {DNSFILTER_ACTIVITY}")
    time.sleep(2)

    # Return to home
    adb.shell("input keyevent 3")
    print("\n[+] personalDNSfilter is deployed and active!")
    print("    Amazon OTA updates and background telemetry are now blocked at the DNS packet level.")
    return True

if __name__ == "__main__":
    client = ADBClient()
    jrnl = ActionJournal()
    setup_dnsfilter(client, jrnl)
