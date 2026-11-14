# Level 2 – Fernzugriff mit SSH

**Ziel:** Sie steuern den Pi vom PC aus über das Netz – ohne Tastatur und Bildschirm am Pi.

**Skript:** SSH-Zugang einrichten, Zugriff auf den Pi

## Auftrag
1. Installieren Sie auf dem Pi den SSH-Server und starten Sie ihn dauerhaft:
   ```bash
   apt install -y openssh-server
   systemctl enable --now ssh
   ```
2. Verbinden Sie sich vom **PC** aus – mit MobaXterm (*Session → SSH*, IP und Benutzer eintragen) oder im Terminal:
   ```bash
   ssh administrator@10.36.13.76
   ```
3. Bestätigen Sie beim ersten Mal den Fingerabdruck mit `yes`. Geben Sie im SSH-Fenster `hostname` ein – es antwortet der Pi.

## Erklärt – was passiert hier?

**SSH** (*Secure Shell*) ist eine **verschlüsselte** Terminal-Verbindung. Alles, was Sie tippen, läuft verschlüsselt über Port **22** zum Pi und wird dort ausgeführt. So betreut man Server, die im Rechenzentrum ohne Bildschirm stehen.

**`systemctl enable --now ssh`** – `enable` startet den Dienst bei jedem Hochfahren, `--now` startet ihn sofort.

**Fingerabdruck:** Beim ersten Verbinden merkt sich Ihr PC den Schlüssel des Pi. Ändert er sich später, warnt SSH – jemand könnte sich als Ihr Pi ausgeben.

**Dateien kopieren** geht mit demselben Zugang: `scp datei administrator@IP:/tmp/` – das brauchen Sie in Level 7.

## Prüfen
`dart run tool/pruefen.dart 2`

<details><summary>Tipp 1 – „Connection refused“</summary>

Der SSH-Dienst läuft nicht. Auf dem Pi: `systemctl status ssh` – steht dort nicht *active*, `systemctl enable --now ssh` wiederholen.
</details>

<details><summary>Tipp 2 – „Permission denied“</summary>

Benutzername oder Passwort falsch. Achtung: Beim Tippen des Passworts erscheinen keine Sternchen – das ist normal.
</details>

> **Merke:** SSH = verschlüsselter Fernzugriff auf die Kommandozeile, Port 22. Ab jetzt können Sie alle weiteren Level vom PC aus erledigen.

**Denkfrage:** Warum ist es gefährlich, auf einem Server im Internet SSH mit dem Passwort `Pa$$w0rd` offen zu lassen?
