#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnoseskript für Offline-Transcriber
"""

import os
import sys
import shutil
import platform
from pathlib import Path

def main():
    print("\n" + "=" * 70)
    print(" OFFLINE-TRANSCRIBER DIAGNOSE ".center(70, "="))
    print("=" * 70 + "\n")
    
    # Überprüfe FFmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print("✓ FFmpeg gefunden:", ffmpeg_path)
    else:
        print("✗ FFmpeg nicht gefunden!")
        print("  Bitte installiere FFmpeg mit install_ffmpeg.bat oder manual_ffmpeg_install.md")
    
    # Überprüfe Audiodateien im Verzeichnis
    audio_dir = Path("audio")
    if audio_dir.exists():
        audio_files = list(audio_dir.glob("*.*"))
        if audio_files:
            print(f"✓ {len(audio_files)} Audiodatei(en) im audio/ Verzeichnis gefunden:")
            for file in audio_files:
                print(f"  - {file.name}")
        else:
            print("✗ Keine Audiodateien im audio/ Verzeichnis gefunden")
            print("  Kopiere deine Audiodateien mit: copy \"C:\\Pfad\\zur\\Datei.mp3\" audio\\")
    else:
        print("✗ audio/ Verzeichnis nicht gefunden")
    
    # Hilfestellung
    print("\nZum Transkribieren verwende:")
    print("  transcribe audio/deine-datei.mp3")
    
    print("\nBei Problemen:")
    print("  1. Installiere FFmpeg mit install_ffmpeg.bat")
    print("  2. Stelle sicher, dass Audiodateien im audio/-Ordner sind")
    print("  3. Prüfe die Dokumentation in README.md")

if __name__ == "__main__":
    main() 