# Active Applications & Running Services Audit

**Device**: Amazon Fire TV Stick (3rd Gen, 2020) — Model `AFTSSS` (Codename: `sheldonp`)  
**Operating System**: Fire OS 7.7.1.5 (`PS7715/5586`), Android 9 (SDK 28)  
**Exclusive Launcher**: **DumbTV Home (Enhanced 4-Chip Edition)** (`tv.dumbtv.home`)  
**Audit Timestamp**: October 28, 2026  
**Memory Headroom**: **~370 MB free** (Surged from ~45 MB stock, ~700% increase)

---

## 1. Executive Summary

This document provides a complete, transparent inventory of every installed application, active home screen tile, and background system service running on your optimized Fire TV Stick. 

- **Single Sole Launcher**: [dumbtv-enhanced-home-v1.0.1.apk](file:///e:/01.%20GitHub%20Repo%20Projects/clean-my-firetv/dumbtv-enhanced-home-v1.0.1.apk) (`tv.dumbtv.home`) is established as the **only** launcher on the device. All secondary or test launchers (such as Plume Launcher) have been completely decommissioned and uninstalled.
- **Debloat & Telemetry Elimination**: 51 promotional, telemetry, and background ad packages remain disabled.
- **Wallpaper Integration**: Single background wallpaper (`assets/wallpaper-dark-ambient.jpg`) rendered with **95% dark dimming overlay** (`dim=95`).
- **Network Hardening**: Local `personalDNSfilter` packet filter running on `tun0` blackholing Amazon OTA and telemetry domains to `127.0.0.1` with Cloudflare upstream.

---

## 2. Complete Inventory of Installed User Applications

All installed media, utility, privacy, and streaming applications are accounted for and optimized:

| # | Application Name | Package Name | Category | Primary Function |
|---|---|---|---|---|
| 1 | **SmartTube** | `org.smarttube.stable` | Video Streaming | Ad-free YouTube client with SponsorBlock |
| 2 | **JioHotstar** | `in.startv.hotstar` | Regional OTT | Disney+ Hotstar India movies, series & sports |
| 3 | **YuppTV** | `com.yupptv.firetv` | Live TV / Regional | Live Indian TV channels & entertainment |
| 4 | **VZY** | `com.vzy.one.firestick` | Streaming | Fire TV media streaming player |
| 5 | **Stremio** | `com.stremio.one` | Core Media Center | Primary media aggregator & catalog |
| 6 | **Sony LIV** | `com.onemainstream.sonyliv.android` | Regional OTT | Official Fire TV India live TV & sports client |
| 7 | **Hoichoi** | `com.viewlift.hoichoiprod` | Regional OTT | Bengali regional entertainment platform |
| 8 | **Zee5** | `com.zee5.amazon` | Regional OTT | Indian originals, movies, and broadcast shows |
| 9 | **Nuvio TV** | `com.nuvio.tv` | Streaming Client | Modern open media streaming client |
| 10 | **Prime Video** | `com.amazon.firebat` | Official OTT | Amazon Prime Video streaming catalog |
| 11 | **discovery+** | `com.discoveryplus.tv.fire` | Documentaries | Discovery Channel documentaries & science |
| 12 | **TizenTube Cobalt** | `io.gh.reisxd.tizentube.cobalt` | Video Streaming | Native Cobalt-based YouTube client (v2.0.3) |
| 13 | **BitChord TV** | `com.music.bitchord.tv` | Music & Audio | High-fidelity ad-free music & audio player |
| 14 | **FanCode** | `com.fancode.tv` | Live Sports | Official Android TV live sports streaming |
| 15 | **SportzX** | `com.sportzx.live` | Live Sports & TV | Live sports events & television streaming |
| 16 | **VLC Media Player** | `org.videolan.vlc` | Utility Media Player | Universal codec video/audio playback engine |
| 17 | **Downloader** | `com.esaba.downloader` | System Utility | Direct web browser & APK downloader |
| 18 | **Send Files to TV** | `com.yablio.sendfilestotv` | File Transfer | Local Wi-Fi direct file transfer utility |
| 19 | **File Explorer** | `visnkmr.apps.filexplorer` | File Manager | Local and USB filesystem management |
| 20 | **Steam Link** | `com.valvesoftware.steamlink` | Gaming & Display | Low-latency PC game streaming to Fire TV |
| 21 | **Xiaomi TV+** | `com.mitv.tvhome.mitvplus` | Live TV | Free ad-supported streaming TV channels |
| 22 | **personalDNSfilter** | `dnsfilter.android` | DNS & Privacy | Local DNS packet filter & hard OTA/telemetry block |
| 23 | **Screen Saver** | `com.amazon.ftv.screensaver` | Ambient Display | Native Fire OS ambient screen saver |
| 24 | **Amazon Appstore** | `com.amazon.venezia` | Official Store | Official Amazon app installation & updates |
| 25 | **DumbTV Home** | `tv.dumbtv.home` | System Launcher | Sole exclusive launcher with 4-chip header |

---

## 3. Home Screen Visibility Matrix ([home.conf](file:///e:/01.%20GitHub%20Repo%20Projects/clean-my-firetv/home.conf))

Every application on the Fire TV Stick is strictly organized in the exact order requested, with Amazon bloat suppressed:

### A. Visible Tiles on Home Screen Grid (Exact Order - 24 Apps):
1. `org.smarttube.stable` (**SmartTube**) - Ad-free YouTube client with SponsorBlock
2. `in.startv.hotstar` (**JioHotstar**) - Disney+ Hotstar India movies, series & sports
3. `com.yupptv.firetv` (**YuppTV**) - Live Indian TV channels & entertainment
4. `com.vzy.one.firestick` (**VZY**) - Fire TV streaming client
5. `com.stremio.one` (**Stremio**) - Torrent & Debrid streaming hub
6. `com.onemainstream.sonyliv.android` (**Sony LIV**) - Official Fire TV India live sports & TV
7. `com.viewlift.hoichoiprod` (**Hoichoi**) - Bengali regional entertainment platform
8. `com.zee5.amazon` (**Zee5**) - Indian originals, movies, and broadcast shows
9. `com.nuvio.tv` (**Nuvio TV**) - Modern open streaming client
10. `com.amazon.firebat` (**Prime Video**) - Amazon Prime Video streaming catalog
11. `com.discoveryplus.tv.fire` (**discovery+**) - Discovery Channel documentaries & science
12. `io.gh.reisxd.tizentube.cobalt` (**TizenTube Cobalt**) - Native Cobalt-based YouTube client
13. `com.music.bitchord.tv` (**BitChord TV**) - High-fidelity ad-free music & audio player
14. `com.fancode.tv` (**FanCode**) - Official Android TV live sports streaming
15. `com.sportzx.live` (**SportzX**) - Live sports events & television streaming
16. `org.videolan.vlc` (**VLC Media Player**) - Universal codec video/audio engine
17. `com.esaba.downloader` (**Downloader**) - Direct web browser & APK downloader
18. `com.yablio.sendfilestotv` (**Send Files to TV**) - Wi-Fi direct file transfer utility
19. `visnkmr.apps.filexplorer` (**File Explorer**) - Local and USB filesystem management
20. `com.valvesoftware.steamlink` (**Steam Link**) - Low-latency PC game streaming to Fire TV
21. `com.mitv.tvhome.mitvplus` (**Xiaomi TV+**) - Free ad-supported streaming TV channels
22. `dnsfilter.android` (**personalDNSfilter**) - Local DNS packet filter & hard OTA blocker (placed before screensaver)
23. `com.amazon.ftv.screensaver` (**Screen Saver**) - Native Fire OS ambient screen saver
24. `com.amazon.venezia` (**Amazon Appstore**) - Preserved at the very end for official app updates

### B. Suppressed Bloatware Tiles (`apps.hide`):
- `com.amazon.ssm` (**System Status Monitor**) — Developer diagnostic HUD hidden from grid.
- `com.amazon.bueller.music` (**Amazon Music**) — Unused Amazon audio tile hidden.
- `com.amazon.bueller.photos` (**Amazon Photos**) — Cloud photo upload tile hidden.
- `com.amazon.minitv.android.app` (**miniTV**) — Ad-driven miniTV app hidden.
- `com.amazon.spiderpork` (**Silk Browser**) — Stock Amazon browser hidden.
- `com.amazon.firetv.troubleshooting` (**Help & Troubleshooting**) — Diagnostic nag hidden.
- `com.amazon.tahoe` & `com.amazon.cloud9` (**FreeTime / Kids**) — Kids profiles hidden.
- `com.amazon.gamehub` & `com.amazon.luna` (**Amazon Gaming**) — Luna cloud gaming tiles hidden.
- `com.amazon.tv.launcher` (**Amazon Stock Home**) — Stock promotional home screen intercepted.
- `com.amazon.ftv.profilepicker` (**Profile Switcher**) — Amazon profile picker hidden.
- `com.amazon.tv.livetv` (**Live TV Promo Aggregator**) — Amazon promo live TV hidden.
- `com.android.providers.downloads.ui` — Downloads UI hidden.

---

## 4. Newly Installed Apps & Tile Management

- **Automatic Surface**: Newly installed applications via Downloader, Appstore, or ADB are dynamically collected via `PackageManager` (`android.intent.category.LEANBACK_LAUNCHER` & `LAUNCHER`). Since new packages are not listed in `apps.hide`, they automatically appear on the home screen grid right after existing ordered apps.
- **Long-Press Menu Options**: Holding `OK` or pressing ` Menu` on any application tile opens a native dialog:
  - **Move**: Adjust the tile's position on the grid interactively.
  - **Rename**: Assign a custom display name to the tile.
  - **Hide**: Immediately removes the app from the grid (appends to `apps.hide`).
  - **App info**: Opens Fire OS system application settings with direct options to **Uninstall**, **Clear Cache**, or **Clear Data**.
- **Unhiding Applications**: Select the `[ Options ]` pill at the top of the home screen, click **"Apps on home screen"**, and check the box next to any hidden app to immediately unhide and restore it to the grid.

---

## 5. Airtight Amazon Stock Home Screen Prevention

To ensure the Fire TV stock home screen NEVER appears unexpectedly (even on reboot, wake, or app exit), two synchronized layers operate continuously:

1. **Multi-Action Boot Receiver (`BootReceiver`)**:
   - `android:maxSdkVersion="27"` restriction was eliminated from `RECEIVE_BOOT_COMPLETED`, enabling Android 9 (SDK 28) compatibility.
   - Listens for `BOOT_COMPLETED`, `QUICKBOOT_POWERON`, and `LOCKED_BOOT_COMPLETED` at maximum priority (`999`).
   - Automatically launches `tv.dumbtv.home.Home` upon startup with `FLAG_ACTIVITY_NEW_TASK | FLAG_ACTIVITY_RESET_TASK_IF_NEEDED`.
2. **Accessibility Guard Service (`tv.dumbtv.home/.Guard`)**:
   - Registered as a persistent accessibility service in `settings secure enabled_accessibility_services`.
   - Intercepts `com.amazon.tv.launcher.ui.HomeActivity_vNext` with 0ms notification timeout.
   - Instantly overlays a dark cover window to prevent any visual flicker of stock ads and brings DumbTV Home to the front within ~150ms.
   - **Intentional Navigation Preserved**: The stock Amazon home screen can still be explicitly accessed whenever needed via `[ Options ] -> Open Amazon's home screen`. Once you exit or press Home, Guard re-engages automatically.

## 6. Running Services Deep Audit

The running services on the Fire TV Stick have been trimmed down to only the essential low-level subsystems required for audio, video, remote control, and system stability:

### A. Launcher Interception & Navigation Service:
- **`tv.dumbtv.home/.Guard`**: Authoritative Accessibility Service. Continuously listens for `TYPE_WINDOW_STATE_CHANGED` to catch the remote HOME button and instant-redirect to DumbTV Home in <300ms.
- **`com.amazon.device.bluetooth/.BTEventReportingService`**: Required system service for physical remote button reporting.

### B. Bluetooth & Remote Subsystem:
- **`com.android.bluetooth`**:
  - `.btservice.AdapterService` (Main Bluetooth HAL adapter)
  - `.gatt.GattService` (BLE communication with Fire TV remote)
  - `.a2dp.A2dpService` (Advanced Audio Distribution Profile for Bluetooth headphones/soundbars)
  - `.hfp.HeadsetService` (Hands-Free audio profile)
  - `.hid.HidHostService` (Human Interface Device host for gamepads and keyboards)
  - `.avrcp.AvrcpTargetService` (Audio/Video Remote Control Profile for volume/play/pause)
- **`com.amazon.vizzini`**:
  - Handles physical BLE connection and key dispatch for the official Fire TV Voice Remote. Disabling this would permanently disconnect your remote.

### C. System Audio, Video & Display Subsystems:
- **`android.hardware.graphics.composer@2.1-service`**: Hardware display rendering pipeline.
- **`android.hardware.graphics.allocator@2.0-service`**: GPU frame allocation.
- **`android.hardware.tv.cec@1.0-service`**: HDMI CEC hardware controller for TV power & volume pass-through.
- **`android.hardware.keymaster@3.0-service`**: Hardware encryption and DRM master key store (required for Netflix/Hotstar/Prime Widevine L1 playback).
- **`com.android.systemui.SystemUIService`**: System status bar, volume bar HUD, and display overlays.
- **`com.amazon.whad.WhadService`**: Low-level audio synchronization HAL daemon.

### D. System Settings & Appstore:
- **`com.amazon.tv.settings.v2`**: Fire OS Settings engine backing the `[ Wi-Fi ]`, `[ Bluetooth ]`, and `[ Settings ]` buttons in the DumbTV Home header.
- **`com.amazon.venezia`**: Amazon Appstore background service backing app installations and official updates.

### E. Confirmed Dead / Non-Running Services (Debloated):
The following invasive services are **100% terminated and blocked from starting**:
-  `com.amazon.aca` (Alexa continuous mic listening service) — **STOPPED**
-  `com.amazon.tv.acr` (Automatic Content Recognition screen fingerprinting) — **STOPPED**
-  `com.amazon.ceviche` (Device usage telemetry pipeline) — **STOPPED**
-  `com.amazon.logan` (Continuous background log uploader) — **STOPPED**
-  `com.amazon.dp.logger` (Diagnostic data uploader) — **STOPPED**
-  `com.amazon.shoptv.client` (Shopping recommendation daemon) — **STOPPED**
-  `com.amazon.sneakpeek` (Autoplay video ad loader) — **STOPPED**
-  `com.amazon.tv.forcedotaupdater.v2` (OTA update nag prompt) — **STOPPED**

---

## 5. Network & Telemetry Hardening Summary

- **Private DNS Mode**: `hostname`
- **DNS-over-TLS Provider**: `1dot1dot1dot1.cloudflare-dns.com` (Cloudflare 1.1.1.1)
- **Wi-Fi Always-On**: `wifi_on = 1`, `wifi_sleep_policy = 2` (`WIFI_SLEEP_POLICY_NEVER` — Wi-Fi never turns off or sleeps on screen-off).
- **Bluetooth Always-On**: `bluetooth_on = 1` (Maintains continuous connection with remotes and paired headphones).
- **OTA Updates**: Background daemons starved of execution time (`RUN_ANY_IN_BACKGROUND ignore`), update nag dialogues disabled.
