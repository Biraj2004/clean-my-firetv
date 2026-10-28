# Restore script for uninstalled applications via Amazon Appstore Intent or APK
$DEVICE_IP = if ($env:FIRETV_IP) { $env:FIRETV_IP } else { "192.168.1.100" } # Set $env:FIRETV_IP or pass your Fire TV IP
$DEVICE = "$DEVICE_IP:5555"

if (Test-Path "$env:LOCALAPPDATA\Android\Sdk\platform-tools") {
    $env:PATH = "$env:LOCALAPPDATA\Android\Sdk\platform-tools;" + $env:PATH
}

adb connect $DEVICE

# To restore any of the uninstalled news channels via the official Amazon Appstore:
# 1. Aaj Tak TV
# adb -s $DEVICE shell "am start -a android.intent.action.VIEW -d 'amzn://apps/android?p=com.aajtak.firetv'"
# 2. ABP Live
# adb -s $DEVICE shell "am start -a android.intent.action.VIEW -d 'amzn://apps/android?p=com.abp.firetv'"
# 3. News18
# adb -s $DEVICE shell "am start -a android.intent.action.VIEW -d 'amzn://apps/android?p=com.news18.ftv'"
# 4. TV9 Bharatvarsh
# adb -s $DEVICE shell "am start -a android.intent.action.VIEW -d 'amzn://apps/android?p=com.tv9live.tv9livetv'"
# 5. Republic World
# adb -s $DEVICE shell "am start -a android.intent.action.VIEW -d 'amzn://apps/android?p=com.republicworld.fire.tv'"
# 6. Republic Bharat
# adb -s $DEVICE shell "am start -a android.intent.action.VIEW -d 'amzn://apps/android?p=com.republicworld.firetv.rbharat'"
# 7. Zee News
# adb -s $DEVICE shell "am start -a android.intent.action.VIEW -d 'amzn://apps/android?p=com.zeenews.tv'"
# 8. Esto IPTV
# adb -s $DEVICE shell "am start -a android.intent.action.VIEW -d 'amzn://apps/android?p=com.onnet.systems.iptv.esto'"
