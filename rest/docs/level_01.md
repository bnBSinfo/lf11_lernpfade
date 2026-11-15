# Level 1 – Den Pi in Betrieb nehmen

**Ziel:** Ihr Raspberry Pi läuft mit Ubuntu, ist aktuell und im Netz erreichbar. Sie kennen seine IP-Adresse.

**Skript:** Ubuntu – SD-Karte erstellen, Einrichten des Raspberry Pi

## Auftrag
1. Erstellen Sie mit dem **Raspberry Pi Imager** eine SD-Karte mit *Ubuntu Desktop (64-bit, LTS)*.
2. Starten Sie den Pi und legen Sie den Benutzer `administrator` mit dem Passwort `Pa$$w0rd` an.
3. Stecken Sie das LAN-Kabel ins **pädagogische Netz**.
4. Öffnen Sie das Terminal, werden Sie Administrator und bringen Sie das System auf den neuesten Stand:
   ```bash
   sudo -i
   apt update
   apt upgrade -y
   apt autoremove -y
   ```
5. Lesen Sie die IP-Adresse aus und notieren Sie sie – Sie brauchen sie in jedem weiteren Level:
   ```bash
   hostname -I
   ```

## Erklärt – was passiert hier?

**`sudo -i`** öffnet eine Shell als `root`. Danach steht vor jedem Befehl automatisch Admin-Recht – das `sudo` entfällt. Erkennbar am `#` statt `$` am Ende der Eingabezeile. Mit `exit` werden Sie wieder normaler Benutzer.

**`apt`** ist die Paketverwaltung von Ubuntu:

| Befehl | Was er tut |
|---|---|
| `apt update` | lädt die **Liste** der verfügbaren Pakete neu – installiert nichts |
| `apt upgrade` | installiert neuere Versionen aller Pakete |
| `apt install paket` | installiert ein Paket |
| `apt autoremove` | entfernt nicht mehr benötigte Pakete |

**IP-Adresse:** Jedes Gerät im Netz hat eine Adresse, z. B. `10.36.13.76`. Ihr PC braucht sie, um den Pi zu erreichen – per SSH, Browser und später aus der App. Das Skript nennt `ifconfig` (Paket `net-tools`); moderner und ohne Installation geht `hostname -I` oder `ip -4 a`.

<details><summary>Tipp 1 – Pi nicht erreichbar?</summary>

Pingen Sie den Pi vom PC aus: `ping 10.36.13.76`. Kommt keine Antwort: Kabel, Netz und IP prüfen. Bei mehreren Adressen aus `hostname -I` ist die erste meistens die richtige.
</details>

<details><summary>Tipp 2 – apt meldet „Sperre“ / lock</summary>

Direkt nach dem ersten Start sucht Ubuntu selbst nach Updates. Warten Sie ein paar Minuten und versuchen Sie es erneut.
</details>

> **Merke:** `apt update` aktualisiert nur die Paketliste, `apt upgrade` die Programme. Die IP-Adresse ist die „Hausnummer“ Ihres Servers im Netz.

**Denkfrage:** Warum kann sich die IP-Adresse Ihres Pi nach einem Neustart ändern – und was bedeutet das für eine App, die fest auf diese Adresse zugreift?
