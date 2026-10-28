"""
Classification of Fire OS 7 packages and system settings.
Curated from dumbtv, cleanyourtv, and verified on Fire TV Stick (AFTSSS, sheldonp).
"""

# CRITICAL SYSTEM PACKAGES - MUST NEVER BE DISABLED OR UNINSTALLED
NEVER_DISABLE = {
    # Home screen fallback and boot starter (kept intact; custom launcher takes over via Accessibility)
    "com.amazon.tv.launcher",
    "com.amazon.firehomestarter",
    
    # System settings & system UI
    "com.amazon.tv.settings.v2",
    "com.amazon.tv.settings.core",
    "com.android.systemui",
    "com.android.packageinstaller",
    "com.android.permissioncontroller",
    "android",
    
    # Remote control pairing, keys & input services
    "com.amazon.tv.keypolicymanager",
    "com.amazon.fireinputdevices",
    "com.amazon.autopairservice",
    "com.amazon.device.bluetoothpa",
    "com.amazon.device.blepa",
    "com.amazon.whisperjoin.middleware.np",
    "com.amazon.whisperplay.service.install",
    "com.amazon.tv.ime",  # On-screen keyboard
    
    # HDMI, TV input switching & CEC controls
    "com.amazon.tv.inputpreference.service",
    "com.amazon.tv.routing",
    "com.amazon.tv.devicecontrol",
    "com.amazon.tv.devicecontrolsettings",
    "com.amazon.tv.livetv",
    "com.amazon.franktvinput",
    "com.amazon.tifobserver",
    "com.mediatek.tis",
    "com.mediatek.dtv.tvinput.atsctuner",
    "com.amazon.mediatek.livetv",
    "com.amazon.tv.settings.mediatek",
    
    # Webview and App Store
    "com.amazon.webview.chromium",
    "com.amazon.venezia",
    
    # Amazon services that cause boot issues or persistent error dialogs if disabled
    "com.amazon.device.messaging",  # Prime Video & system boot dependency
    "com.amazon.vizzini",           # Draws un-dismissable 'Cannot find remote' modal if disabled
    "com.amazon.tv.oobe",           # First run setup
    "com.amazon.tv.ooberesource",
}

# SAFE TO DISABLE: ADS, PROMOS, TRACKING, TELEMETRY, SHOPPING & DEMOS
PACKAGES_DEBLOAT = [
    # Ads, shopping and promos
    ("com.amazon.hybridadidservice", "Advertising ID tracking service"),
    ("com.amazon.privacypassservice", "Ad-token service"),
    ("com.amazon.shoptv.client", "Shopping on TV"),
    ("com.amazon.shoptv.firetv.client", "Amazon Live Shopping tile"),
    ("com.amazon.sneakpeek", "Autoplaying promos and trailers"),
    ("com.amazon.media.recommendations", "Sponsored recommendation rows"),
    ("com.amazon.systemnotices", "Amazon promotional notifications"),
    ("com.amazon.tv.website_launcher", "Promotional web pages launcher"),
    
    # Tracking and ACR
    ("com.amazon.tv.acr", "Automatic Content Recognition (screen fingerprinting)"),
    ("com.amazon.hedwig", "Watch time & engagement tracker"),
    
    # Telemetry, logging & analytics
    ("com.amazon.tv.fw.metrics", "Framework metrics logger"),
    ("com.amazon.wirelessmetrics.service", "Wireless telemetry service"),
    ("com.amazon.perfc", "Performance profiling service"),
    ("com.amazon.perfcollection", "Performance metrics collection"),
    ("com.amazon.dp.logger", "Diagnostic performance logger"),
    ("com.amazon.logan", "Logan analytics service"),
    ("com.amazon.neo.minerva.logcat", "Minerva logcat upload service"),
    ("com.amazon.ceviche", "Ceviche telemetry upload pipeline"),
    ("com.amazon.connectivitydiag", "Diagnostic telemetry service"),
    ("com.amazon.tigris", "Tigris metrics service"),
    ("com.amazon.tv.developer.dataservice", "Developer data telemetry service"),
    
    # Experiments and remote config
    ("com.amazon.ale", "Amazon Lab experiments service"),
    ("com.amazon.katoch", "Feature flag experimentation service"),
    ("com.amazon.device_remote_config_sync_service", "Remote config sync service"),
    
    # Demos, tutorials & dummy stubs
    ("com.amazon.tv.democontent.provider", "Store demo content provider"),
    ("com.amazon.storm.lightning.tutorial", "Tutorial stub"),
    ("com.amazon.tmm.tutorial", "Tutorial stub"),
    ("com.amazon.tv.releasenotes", "Update release notes popup"),
    ("com.amazon.dummy.alarmclock", "Dummy stub"),
    ("com.amazon.dummy.calendar", "Dummy stub"),
    ("com.amazon.dummy.contacts", "Dummy stub"),
    ("com.amazon.dummy.gallery", "Dummy stub"),
    ("com.amazon.dummy.music", "Dummy stub"),
    ("com.amazon.dummy.settings", "Dummy stub"),
    ("com.android.traceur", "System tracing service"),
]

# ALEXA PACKAGES (User selected to disable for maximum RAM savings)
PACKAGES_ALEXA = [
    ("com.amazon.aca", "Alexa voice mic service"),
    ("com.amazon.alexa.datastore.app", "Alexa data store app"),
    ("com.amazon.alexadirectivebrokerservice", "Alexa directive broker"),
    ("com.amazon.alexamediaplayer.runtime.ftv", "Alexa media player runtime"),
    ("com.amazon.alexa.externalmediaplayer.fireos", "Alexa external media player"),
    ("com.amazon.tv.alexaalerts", "Alexa alert notifications"),
    ("com.amazon.tv.alexanotifications", "Alexa notifications"),
    ("com.amazon.vizzini.ftvcds", "Alexa CDS sync"),
    ("com.amazon.firetv.androidskillconnectioncapability", "Alexa skill connection capability"),
    ("com.amazon.audiohome", "Alexa audio home service"),
    ("com.amazon.rtcsessioncontroller", "Alexa calling session controller"),
    ("com.amazon.smarthomemapviewapp", "Alexa Smart Home dashboard"),
    ("com.amazon.spotify.mediabrowserservice", "Alexa Spotify media browser"),
    ("com.amazon.wha.mediabrowserservice", "Alexa multi-room audio browser"),
    ("com.amazon.aria", "Alexa visual cards overlay"),
    ("com.amazon.whad", "Alexa multi-room audio daemon"),
    ("com.amazon.whasettings", "Alexa multi-room audio settings"),
]

# SOFT OTA BLOCK PACKAGES
PACKAGES_OTA_SOFT = [
    ("com.amazon.tv.forcedotaupdater.v2", "Forced OTA updater popup service"),
    ("com.amazon.tv.easyupgrade", "Auto-upgrade nag service"),
]

# PROTECTED OTA & TELEMETRY APPS (Denied background execution & network data)
PROTECTED_LOCKDOWN = [
    ("com.amazon.device.software.ota", "OTA software updater core daemon"),
    ("com.amazon.device.software.ota.override", "OTA software updater override daemon"),
    ("com.amazon.device.metrics", "Amazon device metrics daemon"),
    ("com.amazon.device.crashmanager", "Amazon crash manager daemon"),
    ("com.amazon.device.rdmapplication", "Amazon RDM daemon"),
    ("com.amazon.ftvads.deeplinking", "Fire TV Ads deep-linking daemon"),
    ("com.amazon.tv.csapp", "Amazon CS app daemon"),
]

# SETTINGS OPTIMIZATIONS
SETTINGS_OPTIMIZATIONS = [
    # Privacy & Ad Tracking Off
    ("secure", "amz_limit_ad_tracking", "1", "0", "Limit Amazon ad tracking"),
    ("secure", "limit_ad_tracking", "1", "0", "Limit system ad tracking"),
    ("secure", "non_amz_limit_ad_tracking", "1", "0", "Limit third-party ad tracking"),
    ("secure", "advertisingIdApp:interestBasedAds:value", "0", "1", "Disable interest-based ads"),
    ("secure", "USAGE_METRICS_UPLOAD_ENABLED", "0", "1", "Disable usage metrics upload"),
    ("secure", "usage_metrics_marketing_enabled", "0", "1", "Disable marketing metrics"),
    ("secure", "settingsApp:appUsageData:value", "0", "1", "Disable app usage data collection"),
    ("secure", "settingsApp:deviceUsageData:value", "0", "1", "Disable device usage data collection"),
    
    # Video Ads & Trailer Autoplay Disabled (Stops background audio/video playback on home)
    ("global", "com.amazon.tv.settings.featured_item_video_enabled", "0", "1", "Disable home featured item video autoplay"),
    ("global", "com.amazon.tv.settings.featured_item_video_volume", "0.0", "1.0", "Mute home featured item video volume"),
    ("global", "heads_up_notifications_enabled", "0", "1", "Disable heads up banner notifications"),
    
    # UI Speedup / Snappier Animations (0.5x scale)
    ("global", "window_animation_scale", "0.5", "1.0", "Window animation scale (snappier)"),
    ("global", "transition_animation_scale", "0.5", "1.0", "Transition animation scale (snappier)"),
    
    # Voice Settings (Since Alexa is disabled)
    ("secure", "voice_disabled", "1", "0", "Disable voice recognition system"),
    ("secure", "alexa_wake_word_disabled", "1", "0", "Disable Alexa wake word"),
]
