# Level 1 – Den Pi in Betrieb nehmen

**Ziel:** Dein Raspberry Pi läuft mit Ubuntu. Er ist auf dem neuesten Stand. Er ist im Netz. Du kennst seine IP-Adresse.

**Skript:** Ubuntu – SD-Karte erstellen, Einrichten des Raspberry Pi

## Auftrag
1. **🍓 Pi** Mach mit dem **Raspberry Pi Imager** eine SD-Karte. Wähle *Ubuntu Desktop (64-bit, LTS)*.
2. **🍓 Pi** Starte den Pi. Lege den Benutzer `administrator` an. Das Passwort ist `Pa$$w0rd`.
3. **🍓 Pi** Stecke das LAN-Kabel ins **pädagogische Netz**.
4. **⌨️ Terminal** Öffne das Terminal. Werde root. Bring das System auf den neuesten Stand:
   {{code 0}}
5. **⌨️ Terminal** Lies die IP-Adresse ab. Schreib sie auf. Du brauchst sie in jedem Level:
   {{code 1}}

## Profi-Auftrag
- Der Pi läuft mit Ubuntu. Benutzer `administrator`, Passwort `Pa$$w0rd`. Er hängt im pädagogischen Netz.
- Alles ist aktuell. Alte Pakete sind gelöscht.
- Du kennst die IP. Der PC erreicht den Pi mit `ping`.

## Erklärt – was passiert hier?

**`sudo -i`** macht dich zu `root`. Root darf alles. Am Ende der Zeile steht dann `#` statt `$`. Mit `exit` bist du wieder normal.

**`apt`** installiert Programme:

| Befehl | Was er macht |
|---|---|
| `apt update` | lädt die **Liste** der Pakete neu. Installiert nichts. |
| `apt upgrade` | installiert neue Versionen |
| `apt install paket` | installiert ein Paket |
| `apt autoremove` | löscht Pakete, die keiner mehr braucht |

**IP-Adresse:** Jedes Gerät im Netz hat eine Adresse. Zum Beispiel `10.36.13.76`. Dein PC braucht sie. Nur so findet er den Pi.

<details><summary>Tipp 1 – Der Pi antwortet nicht?</summary>

Tippe am PC: `ping 10.36.13.76`. Keine Antwort? Prüfe Kabel, Netz und IP. Zeigt `hostname -I` mehrere Adressen? Meist ist die erste richtig.
</details>

<details><summary>Tipp 2 – apt meldet „lock“</summary>

Ubuntu sucht nach dem Start selbst nach Updates. Warte ein paar Minuten. Versuch es dann noch mal.
</details>

> **Merke:** `apt update` lädt nur die Liste. `apt upgrade` installiert. Die IP ist die Hausnummer von deinem Server.

**Denkfrage:** Nach einem Neustart hat der Pi vielleicht eine neue IP. Was heißt das für eine App, die eine feste IP benutzt?
