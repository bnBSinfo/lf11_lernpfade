# Level 5 – MySQL und phpMyAdmin

**Ziel:** Auf dem Pi läuft ein Datenbankserver. Mit phpMyAdmin verwaltest du ihn im Browser.

**Skript:** MySQL-Server installieren, PHP-MyAdmin installieren

## Auftrag
1. **⌨️ Terminal** Installiere den Datenbankserver. Teste ihn:
   {{code 0}}
2. **⌨️ Terminal** Installiere phpMyAdmin und die fehlenden PHP-Pakete:
   {{code 1}}
   - Webserver: **apache2** mit der **Leertaste** markieren. Dann siehst du ein Sternchen. Dann mit **Tab** auf *Ok*.
   - *dbconfig-common* einrichten: **Ja**
   - Passwort für phpMyAdmin: `Pa$$w0rd`
3. **🌐 Browser** Tippe `systemctl restart apache2`. Öffne dann `http://<IP>/phpmyadmin`.

## Profi-Auftrag
- MySQL läuft. `SELECT VERSION();` zeigt eine Version.
- `http://<IP>/phpmyadmin` zeigt die Anmeldung. Passwort `Pa$$w0rd`. Achtung: Leertaste!

## Erklärt – was passiert hier?

![Apache mit der Leertaste markieren](bilder/pma_apache.png)

Der häufigste Fehler: Enter statt Leertaste. Dann ist kein Webserver gewählt. phpMyAdmin bleibt unsichtbar.

**Wer ist root?** In MySQL darf root nur rein, wenn er auch auf dem Pi root ist. Darum geht `mysql` nach `sudo -i` ohne Passwort. In phpMyAdmin geht root nicht. In Level 6 legst du einen **eigenen Benutzer** an.

| Teil | Aufgabe |
|---|---|
| **MySQL-Server** | speichert die Daten. Nur auf dem Pi erreichbar. |
| **phpMyAdmin** | verwaltet die Datenbank im Browser |
| **mysql** im Terminal | SQL direkt eintippen |

<details><summary>Tipp 1 – 404 bei /phpmyadmin</summary>

Tippe `dpkg-reconfigure phpmyadmin`. Markiere jetzt apache2 mit der Leertaste.
</details>

<details><summary>Tipp 2 – Die Seite bleibt weiß</summary>

Es fehlen PHP-Pakete. Installiere die Liste aus Schritt 2. Starte Apache neu. Hilft das nicht? Leere den Browser-Cache.
</details>

> **Merke:** MySQL ist nur auf dem Pi selbst erreichbar. Von außen kommst du nur über Programme an die Daten.

**Denkfrage:** Warum ist es sicherer, dass MySQL nicht direkt im Netz hängt?
