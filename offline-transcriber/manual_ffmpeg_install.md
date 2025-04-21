# Manuelle Installation von FFmpeg

Wenn das automatische Installationsskript nicht funktioniert, folge dieser Anleitung zur manuellen Installation von FFmpeg.

## Windows

1. Besuche die offizielle FFmpeg-Download-Seite:
   https://ffmpeg.org/download.html

2. Unter "Windows Packages" klicke auf "Windows builds from gyan.dev"

3. Lade die aktuelle Version herunter (ffmpeg-release-essentials.zip)

4. Entpacke die ZIP-Datei an einen permanenten Speicherort (z.B. C:\ffmpeg)

5. Füge den Pfad zu den FFmpeg-Binärdateien zur Umgebungsvariable PATH hinzu:
   - Rechtsklick auf "Dieser PC" > Eigenschaften > Erweiterte Systemeinstellungen
   - Klicke auf "Umgebungsvariablen"
   - Wähle unter "Systemvariablen" die Variable "Path" und klicke auf "Bearbeiten"
   - Klicke auf "Neu" und füge den Pfad zum bin-Verzeichnis hinzu (z.B. C:\ffmpeg\bin)
   - Klicke auf "OK", um alle Dialogfelder zu schließen

6. Starte PowerShell oder die Eingabeaufforderung neu

7. Überprüfe die Installation mit:
   ```
   ffmpeg -version
   ```

## macOS

1. Installiere Homebrew, falls noch nicht vorhanden:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Installiere FFmpeg mit Homebrew:
   ```
   brew install ffmpeg
   ```

## Linux (Ubuntu/Debian)

```
sudo apt update
sudo apt install ffmpeg
```

## Überprüfung der Installation

Nach der Installation kannst du überprüfen, ob FFmpeg korrekt installiert wurde:

```
ffmpeg -version
```

Sollte die Version und Konfigurationsinformationen anzeigen. 