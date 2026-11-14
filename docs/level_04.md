# Level 4 – PHP auf dem Webserver

**Ziel:** Apache führt PHP-Programme aus, statt sie nur auszuliefern. PHP kann mit MySQL sprechen.

**Skript:** PHP-MyAdmin installieren (Pakete), PHP-Info-Datei erstellen

## Auftrag
1. Installieren Sie PHP mit Apache-Modul und MySQL-Anbindung:
   ```bash
   apt install -y php libapache2-mod-php php-mysql
   systemctl restart apache2
   ```
2. Legen Sie die Datei `info.php` an:
   ```bash
   nano /var/www/html/info.php
   ```
   Inhalt: `<?php phpinfo(); ?>` – speichern mit **Strg+O**, Enter, beenden mit **Strg+X**.
3. Rufen Sie `http://<IP>/info.php` im Browser auf und suchen Sie (Strg+F) nach **mysqli**.

## Erklärt – was passiert hier?

Bei `.html` schickt Apache die Datei **unverändert**. Bei `.php` übergibt er sie erst an den **PHP-Interpreter** – zurück geht nur, was das Programm ausgibt:

```text
Browser ──GET /info.php──▶ Apache ──▶ PHP führt phpinfo() aus ──▶ HTML-Seite ──▶ Browser
```

Sieht der Browser `<?php phpinfo(); ?>` im Klartext, fehlt das Paket `libapache2-mod-php`.

| Paket | wofür |
|---|---|
| `php` | der PHP-Interpreter |
| `libapache2-mod-php` | verbindet Apache mit PHP |
| `php-mysql` | Erweiterung **mysqli** – damit PHP eine MySQL-Datenbank abfragen kann |

Das Skript installiert diese Pakete über *synaptic* („die 4 Ubuntu-Pakete“). Mit `apt` geht es schneller und nachvollziehbar.

## Prüfen
`dart run tool/pruefen.dart 4`

<details><summary>Tipp 1 – 404 Not Found</summary>

Die Datei heißt `info.php` (nicht `php.info`) und liegt in `/var/www/html`. Kontrolle: `ls /var/www/html`
</details>

<details><summary>Tipp 2 – mysqli fehlt</summary>

`apt install php-mysql` und danach unbedingt `systemctl restart apache2` – Apache lädt Erweiterungen nur beim Start.
</details>

> **Merke:** Der Webserver führt `.php`-Dateien aus und schickt nur die Ausgabe. Nach dem Installieren von PHP-Erweiterungen Apache neu starten.

**Denkfrage:** `info.php` verrät Versionen und Pfade Ihres Servers. Warum sollte man sie auf einem echten Server wieder löschen? (→ Bonus)
