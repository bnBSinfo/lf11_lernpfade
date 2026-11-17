# Level 4 – PHP auf dem Webserver

**Ziel:** Apache führt PHP-Programme aus. PHP kann mit MySQL sprechen.

**Skript:** PHP-MyAdmin installieren (Pakete), PHP-Info-Datei erstellen

## Auftrag
1. **⌨️ Terminal** Installiere PHP. Starte Apache neu:
   {{code 0}}
2. **📄 Neue Datei** `/var/www/html/info.php`. Öffne sie mit nano:
   {{code 1}}
   Tippe die grüne Zeile ein. Speichern: **Strg+O**, dann Enter. Beenden: **Strg+X**.
   {{code 2}}
3. **🌐 Browser** Öffne `http://<IP>/info.php`. Suche mit Strg+F nach **mysqli**.

## Profi-Auftrag
- Apache führt `.php`-Dateien aus. PHP kann MySQL ansprechen (*mysqli*).
- `http://<IP>/info.php` zeigt die PHP-Seite mit `mysqli`.

## Erklärt – was passiert hier?

Eine `.html`-Datei schickt Apache so, wie sie ist. Eine `.php`-Datei gibt Apache erst an PHP. PHP führt sie aus. Zurück geht nur das Ergebnis.

{{code 3}}

Siehst du `<?php phpinfo(); ?>` als Text? Dann fehlt `libapache2-mod-php`.

| Paket | wofür |
|---|---|
| `php` | PHP selbst |
| `libapache2-mod-php` | verbindet Apache mit PHP |
| `php-mysql` | bringt **mysqli**. Damit spricht PHP mit MySQL. |

<details><summary>Tipp 1 – 404 Not Found</summary>

Die Datei heißt `info.php`. Nicht `php.info`. Sie liegt in `/var/www/html`. Prüfe mit `ls /var/www/html`.
</details>

<details><summary>Tipp 2 – mysqli fehlt</summary>

Tippe `apt install php-mysql`. Dann unbedingt `systemctl restart apache2`.
</details>

> **Merke:** Apache führt `.php`-Dateien aus. Er schickt nur das Ergebnis. Nach neuen PHP-Paketen: Apache neu starten.

**Denkfrage:** `info.php` zeigt viel über deinen Server. Warum sollte man sie auf einem echten Server löschen?
