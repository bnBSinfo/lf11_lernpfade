# Level 3 – Der Webserver Apache

**Ziel:** Auf dem Pi läuft ein Webserver, den Sie vom PC aus im Browser aufrufen.

**Skript:** Webserver installieren

## Auftrag
1. Installieren Sie Apache:
   ```bash
   apt install -y apache2
   ```
2. Öffnen Sie auf dem **PC** im Browser `http://<IP Ihres Pi>` – es erscheint die *Apache2 Ubuntu Default Page*.
3. Finden Sie heraus, aus welcher Datei diese Seite kommt:
   ```bash
   ls -l /var/www/html
   ```

## Erklärt – was passiert hier?

Ein **Webserver** wartet auf Port **80** auf HTTP-Anfragen und schickt Dateien zurück. Der Browser fragt `GET /`, Apache antwortet mit `/var/www/html/index.html`.

| Adresse im Browser | Datei auf dem Pi |
|---|---|
| `http://IP/` | `/var/www/html/index.html` |
| `http://IP/info.php` | `/var/www/html/info.php` |
| `http://IP/php-crud-api/api.php` | `/var/www/html/php-crud-api/api.php` |

`/var/www/html` ist das **Wurzelverzeichnis** (*DocumentRoot*) – alles darin ist aus dem Netz erreichbar. Merken Sie sich das, es wird in Level 4, 7 und 8 wichtig.

<details><summary>Tipp – Seite lädt nicht</summary>

`systemctl status apache2` zeigt, ob Apache läuft. Achten Sie im Browser auf `http://` – nicht `https://`, dafür ist noch kein Zertifikat eingerichtet.
</details>

> **Merke:** Apache liefert Dateien aus `/var/www/html` über HTTP (Port 80) aus. Pfad in der URL = Pfad unter `/var/www/html`.

**Denkfrage:** Was würde passieren, wenn Sie eine Datei `passwoerter.txt` nach `/var/www/html` legen?
