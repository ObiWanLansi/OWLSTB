# Raspberry Pi 5 – Bildschirmschoner steuern

## 1. Bildschirmschoner dauerhaft deaktivieren (X11 & LXDE)
Falls du die X11-Umgebung nutzt, kannst du den Bildschirmschoner über das Terminal oder ein Skript deaktivieren:

```bash
xset s off          # Bildschirmschoner deaktivieren
xset -dpms         # Energiesparmodus deaktivieren
xset s noblank     # Bildschirm nicht ausblenden
```

Falls du möchtest, dass diese Einstellungen nach jedem Neustart aktiv sind, kannst du sie in die Datei `~/.xsessionrc` oder `~/.bashrc` einfügen.

## 2. Deaktivieren über ein Skript
Erstelle eine Datei `disable_screensaver.sh` mit folgendem Inhalt:

```bash
#!/bin/bash
xset s off
xset -dpms
xset s noblank
```

Dann das Skript ausführbar machen und ausführen:

```bash
chmod +x disable_screensaver.sh
./disable_screensaver.sh
```

Falls du das Skript beim Booten automatisch starten möchtest, kannst du es in die `~/.bashrc` oder `~/.profile` einfügen.

## 3. Deaktivieren über die `lightdm.conf` (Für Raspberry Pi OS mit Pixel)
Falls du den `lightdm` Display Manager nutzt, kannst du die Datei bearbeiten:

```bash
sudo nano /etc/lightdm/lightdm.conf
```

Füge unter `[Seat:*]` folgende Zeile hinzu oder ändere sie:

```
xserver-command=X -s 0 -dpms
```

Speichern mit `CTRL + X`, `Y` und Enter. Danach den Raspberry Pi neu starten:

```bash
sudo reboot
```

## 4. Bildschirm wieder aktivieren
Falls der Bildschirm bereits durch den Bildschirmschoner oder den Energiesparmodus deaktiviert wurde und du ihn per Skript wieder aktivieren möchtest, kannst du folgendes Kommando nutzen:

```bash
xset dpms force on
```

Falls das nicht reicht, kannst du vorher ein paar Tasten simulieren, um sicherzustellen, dass der Bildschirm aufgeweckt wird:

```bash
xdotool key Shift
xset dpms force on
```

Falls `xdotool` nicht installiert ist, kannst du es mit folgendem Befehl nachinstallieren:

```bash
sudo apt install xdotool
```

## 5. Bildschirmschoner direkt einschalten
Falls du den Bildschirmschoner sofort aktivieren möchtest, kannst du dies mit folgendem Befehl tun:

```bash
xset s activate
```

Falls du den Bildschirm direkt ausschalten möchtest, kannst du dies mit:

```bash
xset dpms force off
```

### Skript zum Aktivieren des Bildschirmschoners
Falls du das als Skript speichern möchtest, erstelle eine Datei `enable_screensaver.sh`:

```bash
#!/bin/bash
xset s activate
```

Dann ausführbar machen und ausführen:

```bash
chmod +x enable_screensaver.sh
./enable_screensaver.sh
```

Falls du Wayland statt X11 nutzt, sind diese Befehle nicht verfügbar – dann brauchst du eine andere Lösung.
