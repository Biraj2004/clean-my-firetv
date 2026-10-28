# DumbTV Enhanced Home v1.0.1 (Universal Edition)

The official v1.0.1 release of **DumbTV Enhanced Home** for Amazon Fire TV devices, providing an ultra-lightweight, zero-advertisement, privacy-hardened alternative home screen.

---

### Key Architectural Enhancements

- **Universal Fire OS Compatibility (`minSdkVersion: 21`, `targetSdkVersion: 28`)**:
  - Full native support spanning Android 5.0 (Fire OS 5) through Android 11+ (Fire OS 8).
  - Validated across all generations of Fire TV Stick (2nd Gen, 3rd Gen, 4K, 4K Max), Fire TV Cube (1st-3rd Gen), and Xiaomi Fire TV Edition smart displays.
- **Android 11+ Inter-Package Discovery (`QUERY_ALL_PACKAGES`)**:
  - Eliminates Fire OS 8 package filtering. Sideloaded streaming apps (SmartTube, Stremio, TizenTube Cobalt) and local utilities surface dynamically on the home grid.
- **Resilient Home Key Capture (`Guard.smali`)**:
  - Broadened bytecode pattern matching (`contains("HomeActivity")` within `com.amazon.tv.launcher`), delivering instant <150ms interception across every Fire OS generation without home exposure.
- **Hardware Remote Settings Key Handler (`Home.smali`)**:
  - Native handler for `KEYCODE_SETTINGS` (`0xb0` / Keycode 176) to summon the Fire OS settings HUD directly from physical remote buttons.
- **3-Tier Fallback Settings Navigation (`WifiClickListener` & `BtClickListener`)**:
  - Seamless navigation to Fire OS v2 settings, legacy settings, and standard Android settings without crash risks.

---

### Release Assets & Checksums

| File Name | Size | SHA-256 Checksum |
|---|---|---|
| `dumbtv-enhanced-home-v1.0.1.apk` | 57,940 bytes (56.6 KB) | `cc33b64cbc4b4cc34a46245602c8fa3621a42b710a25ffac7a7aa07c7ff4a424` |
| `home.conf` | 2,752 bytes | Curated 24-app layout and dark afterglow styling configuration |
| `wallpaper-dark-ambient.jpg` | 559,951 bytes | High-resolution true-black ambient background wallpaper |

---

### Quick Installation

```bash
# Sideload via ADB
adb install -r dumbtv-enhanced-home-v1.0.1.apk

# Push layout configuration and wallpaper
adb shell mkdir -p /sdcard/Android/data/tv.dumbtv.home/files
adb push home.conf /sdcard/Android/data/tv.dumbtv.home/files/home.conf
adb push wallpaper-dark-ambient.jpg /sdcard/Android/data/tv.dumbtv.home/files/wallpaper.jpg

# Set zero-lag Home response and enable Guard accessibility service
adb shell "settings put global alarm_manager_constants min_futurity=0"
adb shell "settings put secure enabled_accessibility_services tv.dumbtv.home/.Guard"
adb shell "settings put secure accessibility_enabled 1"

# Launch DumbTV Home
adb shell am start -n tv.dumbtv.home/.Home
```
