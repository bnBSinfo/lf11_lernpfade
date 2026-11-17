# Level 2 – Fernzugriff mit SSH

**Ziel:** Du steuerst den Pi vom PC aus. Am Pi brauchst du keine Tastatur und keinen Bildschirm mehr.

**Skript:** SSH-Zugang einrichten, Zugriff auf den Pi

## Auftrag
1. **⌨️ Terminal (Pi)** Installiere den SSH-Server. Starte ihn für immer:
   {{code 0}}
2. **💻 PC** Verbinde dich vom **PC**. Nimm MobaXterm (*Session → SSH*, IP und Benutzer eintragen). Oder tippe im Terminal:
   {{code 1}}
3. **💻 PC** Beim 1. Mal fragt SSH nach dem Fingerabdruck. Tippe `yes`. Tippe dann `hostname`. Jetzt antwortet der Pi.

## Profi-Auftrag
- Auf dem Pi läuft ein SSH-Server. Er startet bei jedem Hochfahren.
- Du meldest dich vom PC als `administrator` an. `hostname` zeigt den Pi.

## Erklärt – was passiert hier?

**SSH** ist eine **verschlüsselte** Verbindung zum Terminal. Sie läuft über Port **22**. Was du tippst, läuft auf dem Pi.

**`systemctl enable --now ssh`:** `enable` heißt: bei jedem Start. `--now` heißt: sofort.

**Fingerabdruck:** Dein PC merkt sich den Schlüssel vom Pi. Ändert er sich, warnt SSH. Dann gibt sich vielleicht jemand als dein Pi aus.

**Dateien kopieren** geht mit `scp`. Zum Beispiel: `scp datei administrator@IP:/tmp/`. Das brauchst du in Level 7.

<details><summary>Tipp 1 – „Connection refused“</summary>

SSH läuft nicht. Tippe auf dem Pi: `systemctl status ssh`. Steht dort nicht *active*? Dann tippe noch mal `systemctl enable --now ssh`.
</details>

<details><summary>Tipp 2 – „Permission denied“</summary>

Name oder Passwort ist falsch. Beim Passwort siehst du keine Sternchen. Das ist normal.
</details>

> **Merke:** SSH ist ein sicherer Fernzugang zum Terminal. Port 22. Ab jetzt machst du alles vom PC aus.

**Denkfrage:** Warum ist SSH mit dem Passwort `Pa$$w0rd` im Internet gefährlich?
