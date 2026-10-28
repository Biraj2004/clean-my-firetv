# Fire TV Optimization & Stremio Setup Guide

## Device Overview
- **Device Model**: Amazon Fire TV Stick (3rd Gen, 2020) — `AFTSSS` (Codename: `sheldonp`)
- **Firmware**: Fire OS 7.7.1.5 (`PS7715/5586`) based on Android 9 (API Level 28)
- **RAM**: 1 GB (~900 MB usable)

---

## What Has Been Done

### 1. Pre-Clean State Backup
A full device snapshot was created in `backup/` containing:
- All package states (enabled, disabled, third-party)
- Complete device properties (`getprop`)
- Full settings dumps (`global`, `secure`, `system`)
- Standalone emergency recovery script: `backup/snapshot_*/emergency_restore.py`

### 2. Debloated & Freed System Resources (51 Packages)
- **Ads & Shopping**: `com.amazon.hybridadidservice`, `com.amazon.privacypassservice`, `com.amazon.shoptv.client`, `com.amazon.shoptv.firetv.client`, `com.amazon.sneakpeek`, `com.amazon.media.recommendations`, `com.amazon.systemnotices`, `com.amazon.tv.website_launcher`
- **ACR & Tracking**: `com.amazon.tv.acr` (screen content fingerprinting), `com.amazon.hedwig`
- **Telemetry & Logging**: `com.amazon.tv.fw.metrics`, `com.amazon.wirelessmetrics.service`, `com.amazon.perfc`, `com.amazon.perfcollection`, `com.amazon.dp.logger`, `com.amazon.logan`, `com.amazon.ceviche`, `com.amazon.connectivitydiag`, `com.amazon.tigris`, `com.amazon.tv.developer.dataservice`
- **Alexa Daemons**: `com.amazon.aca`, `com.amazon.alexa.datastore.app`, `com.amazon.alexamediaplayer.runtime.ftv`, `com.amazon.whad`, `com.amazon.whasettings`, etc.
- **Stubs & Demos**: `com.amazon.tv.democontent.provider`, `com.amazon.storm.lightning.tutorial`, `com.android.traceur`, and all dummy app stubs.

### 3. Soft OTA Update Block
- Disabled `com.amazon.tv.forcedotaupdater.v2` and `com.amazon.tv.easyupgrade`.
- Restricted background appops execution (`RUN_ANY_IN_BACKGROUND ignore`) for `com.amazon.device.software.ota` and `com.amazon.device.software.ota.override`.
- Manual software updates remain accessible in Fire OS Settings if ever desired in the future.

### 4. System Settings Optimization
- Ad tracking disabled across Amazon and third-party networks.
- Autoplay promotional videos and trailer audio completely disabled on Home.
- Window and transition animation scales tuned to `0.5x` for a snappy, responsive feel.
- `alarm_manager_constants min_futurity=0` configured to eliminate the artificial 5-second Home key delay.

### 5. Launchers & Custom Grid Setup
- **DumbTV Home (Enhanced 4-Chip Edition)**: Configured as the exclusive launcher. Featuring a custom forest wallpaper with a 95% dark overlay (`dim=95`), real-time memory monitor, and 4 dedicated navigation chips:
  - `[ Options ]`: App visibility and display options.
  - `[ Wi-Fi ]`: Direct network connectivity toggle and SSID selection.
  - `[ Bluetooth ]`: Direct Bluetooth device and controller pairing.
  - `[ Settings ]`: Fire OS system settings dashboard.
- **24-App Curated Grid**: Ordered from SmartTube, JioHotstar, YuppTV, Vzy, Stremio, Sony LIV, Hoichoi, Zee5, Nuvio, Prime Video, discovery+, MX Player TV, TizenTube Cobalt, BitChord TV, FanCode, VLC, Downloader, Ace Stream, Send Files to TV, File Explorer, Steam Link, Xiaomi TV+, Screen Saver, through Amazon Appstore at the very end.
- **Dynamic App Lifecycle**: Newly installed apps automatically surface; long-pressing any app tile provides `Move`, `Rename`, `Hide`, and `App info` (for instant uninstall/cache clearing). Unhiding is available in `[ Options ] -> Apps on home screen`.
- **Airtight Amazon Home Suppression**: Multi-action boot receiver (`BOOT_COMPLETED`, `QUICKBOOT_POWERON`, `LOCKED_BOOT_COMPLETED` at priority 999) + persistent accessibility guard (`tv.dumbtv.home/.Guard`) prevent Amazon stock home from appearing on boot, wake, or app exit.

---

## Remote Navigation Shortcuts

| Action | Result |
|---|---|
| **Press HOME** | Instantly opens your clean DumbTV Home grid (zero ads, <150ms) |
| **Top Right [ Wi-Fi ]** | Opens Fire OS Network Settings with on/off toggle and Wi-Fi networks |
| **Top Right [ Bluetooth ]** | Opens Fire OS Remotes & Bluetooth Devices page |
| **Top Right [ Settings ]** | Opens Fire OS All Settings dashboard |
| **Hold OK on Any Tile** | Opens menu: **Move**, **Rename**, **Hide**, **App info** (Uninstall / Clear Cache) |
| **Top Right [ Options ] > Apps on home screen** | Check/uncheck apps to easily hide or unhide any app |
| **Hold HOME (3 sec)** | Opens Fire OS Quick Settings overlay (Sleep, Mirroring, Settings) |
| **Select App (OK)** | Launches the app |

---

## How to Rollback / Undo

All actions are logged in `logs/journal.jsonl`. You can undo anytime:

### 1. Revert Everything back to Stock:
```bash
python scripts/rollback.py --all
```

### 2. Re-enable Alexa Voice Remote only:
```bash
python scripts/rollback.py --category alexa
```

### 3. Revert OTA update blocks:
```bash
python scripts/rollback.py --category ota
```
