# Level 3 – Der Webserver Apache

**Ziel:** Auf dem Pi läuft ein Webserver. Du öffnest ihn am PC im Browser.

**Skript:** Webserver installieren

## Auftrag
1. **⌨️ Terminal** Installiere Apache:
   {{code 0}}
2. **🌐 Browser** Öffne am **PC** `http://<IP von deinem Pi>`. Du siehst die *Apache2 Ubuntu Default Page*.
3. **⌨️ Terminal** Aus welcher Datei kommt die Seite? Schau nach:
   {{code 1}}

## Profi-Auftrag
- Apache läuft. `http://<IP>` zeigt am PC die Default Page.
- Du weißt, aus welcher Datei die Seite kommt.

## Erklärt – was passiert hier?

Ein **Webserver** wartet auf Port **80**. Der Browser fragt: `GET /`. Apache schickt die Datei `/var/www/html/index.html`.

| Adresse im Browser | Datei auf dem Pi |
|---|---|
| `http://IP/` | `/var/www/html/index.html` |
| `http://IP/info.php` | `/var/www/html/info.php` |
| `http://IP/php-crud-api/api.php` | `/var/www/html/php-crud-api/api.php` |

`/var/www/html` ist der Ordner für Webseiten. Alles darin kann jeder im Netz sehen. Das brauchst du in Level 4, 7 und 8.

<details><summary>Tipp – Die Seite lädt nicht</summary>

Tippe `systemctl status apache2`. Läuft Apache? Schreib im Browser `http://`. Nicht `https://`.
</details>

> **Merke:** Apache schickt Dateien aus `/var/www/html`. Der Pfad in der Adresse ist der Pfad im Ordner.

**Denkfrage:** Was passiert, wenn du eine Datei `passwoerter.txt` nach `/var/www/html` legst?
