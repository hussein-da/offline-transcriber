# PowerShell-Skript zum Herunterladen und Einrichten von FFmpeg

# Funktion zur Überprüfung von Admin-Rechten
function Test-Administrator {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent();
    $principal = New-Object Security.Principal.WindowsPrincipal $user
    return $principal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

# Konfiguration
$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$tempPath = Join-Path $env:TEMP "ffmpeg_download.zip"
$extractPath = Join-Path $env:TEMP "ffmpeg_extract"
$installPath = "C:\ffmpeg"

Write-Host "*** FFmpeg Setup für Offline-Transcriber ***" -ForegroundColor Green
Write-Host "Dieses Skript lädt FFmpeg herunter und richtet es für die Verwendung mit Offline-Transcriber ein." -ForegroundColor Cyan
Write-Host ""

# Prüfen, ob FFmpeg bereits installiert ist
if (Get-Command "ffmpeg" -ErrorAction SilentlyContinue) {
    Write-Host "FFmpeg ist bereits installiert und im Pfad verfügbar." -ForegroundColor Green
    ffmpeg -version
    exit 0
}

# Admin-Rechte prüfen
if (-not (Test-Administrator)) {
    Write-Host "Bitte führe dieses Skript als Administrator aus!" -ForegroundColor Red
    Write-Host "Rechtsklick auf PowerShell und 'Als Administrator ausführen' wählen." -ForegroundColor Yellow
    exit 1
}

# FFmpeg herunterladen
Write-Host "Lade FFmpeg herunter..." -ForegroundColor Cyan
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $ffmpegUrl -OutFile $tempPath
} catch {
    Write-Host "Fehler beim Herunterladen von FFmpeg: $_" -ForegroundColor Red
    exit 1
}

# Verzeichnis erstellen und vorhandenes löschen, falls vorhanden
if (Test-Path $extractPath) {
    Remove-Item -Recurse -Force $extractPath
}
New-Item -ItemType Directory -Path $extractPath | Out-Null

# Zip-Datei entpacken
Write-Host "Entpacke FFmpeg..." -ForegroundColor Cyan
try {
    Expand-Archive -Path $tempPath -DestinationPath $extractPath
} catch {
    Write-Host "Fehler beim Entpacken von FFmpeg: $_" -ForegroundColor Red
    exit 1
}

# FFmpeg-Verzeichnis finden
$ffmpegDir = Get-ChildItem -Path $extractPath -Directory | Select-Object -First 1

# Zielverzeichnis erstellen
if (Test-Path $installPath) {
    Remove-Item -Recurse -Force $installPath
}
New-Item -ItemType Directory -Path $installPath | Out-Null

# Dateien kopieren
Write-Host "Installiere FFmpeg in $installPath..." -ForegroundColor Cyan
Copy-Item -Path "$($ffmpegDir.FullName)\bin\*" -Destination $installPath -Recurse

# Zur PATH-Umgebungsvariable hinzufügen
$path = [Environment]::GetEnvironmentVariable("Path", "Machine")
if (-not ($path.Split(";") -contains $installPath)) {
    [Environment]::SetEnvironmentVariable("Path", "$path;$installPath", "Machine")
    Write-Host "FFmpeg wurde zur PATH-Umgebungsvariable hinzugefügt." -ForegroundColor Green
}

# Aufräumen
Remove-Item -Force $tempPath
Remove-Item -Recurse -Force $extractPath

Write-Host ""
Write-Host "FFmpeg wurde erfolgreich installiert!" -ForegroundColor Green
Write-Host "Bitte starte PowerShell neu, um die Änderungen zu übernehmen." -ForegroundColor Yellow
Write-Host ""
Write-Host "Anschließend kannst du Offline-Transcriber verwenden." -ForegroundColor Cyan 