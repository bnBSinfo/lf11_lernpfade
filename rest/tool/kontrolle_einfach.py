"""Selbstkontrolle in einfacher Sprache. Gleiche Reihenfolge wie kontrolle.py:
gleiche Haken, gleiche Fragen, gleiche Antworten. Richtig oder falsch steht nur in kontrolle.py."""

KONTROLLE_EINFACH = {
    1: {"check": [
        "Der Pi startet mit Ubuntu. Ich bin als `administrator` angemeldet.",
        "`apt update` und `apt upgrade` laufen ohne Fehler.",
        "Ich habe die IP von meinem Pi aufgeschrieben (`hostname -I`).",
        "Der Pi antwortet auf `ping <IP>` vom PC.",
    ], "fragen": [
        ("Was macht `apt update`?", [
            ("Es lädt die Liste der Pakete neu. Es installiert nichts.", "Erst die Liste neu laden. Dann mit apt upgrade installieren."),
            ("Es installiert neue Versionen von allen Programmen.", "Das macht apt upgrade."),
            ("Es macht aus Ubuntu die nächste große Version.", "Dafür gibt es do-release-upgrade. apt update lädt nur die Liste."),
        ]),
        ("Woran siehst du nach `sudo -i`, dass du root bist?", [
            ("Die Zeile endet mit `#`.", "# heißt root. $ heißt normaler Benutzer."),
            ("Die Zeile endet mit `$`.", "$ heißt normaler Benutzer."),
            ("Vor jedem Befehl steht weiter `sudo`.", "Genau das fällt nach sudo -i weg."),
        ]),
    ]},
    2: {"check": [
        "`systemctl status ssh` zeigt *active (running)*.",
        "Ich komme vom PC mit `ssh administrator@<IP>` (oder MobaXterm) auf den Pi.",
        "`hostname` im SSH-Fenster zeigt den Namen von meinem Pi. Nicht den vom PC.",
    ], "fragen": [
        ("Auf welchem Port wartet SSH normalerweise?", [
            ("22", "SSH ist Port 22."),
            ("80", "Port 80 ist HTTP. Das ist der Webserver aus Level 3."),
            ("3306", "3306 ist MySQL."),
        ]),
        ("Was macht `systemctl enable --now ssh`?", [
            ("SSH startet sofort. Und bei jedem Hochfahren.", "enable heißt: beim Start. --now heißt: sofort."),
            ("SSH startet nur jetzt. Nach dem Neustart nicht mehr.", "Das wäre systemctl start ssh."),
            ("SSH wird installiert.", "Installieren geht mit apt install openssh-server."),
        ]),
    ]},
    3: {"check": [
        "Im Browser am PC sehe ich unter `http://<IP>` die *Apache2 Ubuntu Default Page*.",
        "`systemctl status apache2` zeigt *active (running)*.",
        "`ls /var/www/html` zeigt die Datei `index.html`.",
    ], "fragen": [
        ("Wo muss die Datei liegen, damit `http://<IP>/test.html` geht?", [
            ("`/var/www/html/test.html`", "/var/www/html ist der Ordner für Webseiten."),
            ("`/home/administrator/test.html`", "Diesen Ordner zeigt Apache nicht."),
            ("`/etc/apache2/test.html`", "In /etc/apache2 stehen Einstellungen. Keine Webseiten."),
        ]),
        ("Was antwortet der Webserver, wenn es die Datei nicht gibt?", [
            ("404 Not Found", "404 heißt: nicht gefunden."),
            ("200 OK", "200 heißt: alles gut."),
            ("500 Internal Server Error", "500 heißt: Fehler im Programm auf dem Server."),
        ]),
    ]},
    4: {"check": [
        "`http://<IP>/info.php` zeigt die bunte PHP-Seite. Nicht den Code.",
        "Auf der Seite gibt es einen Teil `mysqli`.",
        "Nach dem Installieren habe ich `systemctl restart apache2` getippt.",
    ], "fragen": [
        ("Der Browser zeigt `<?php phpinfo(); ?>` als Text. Warum?", [
            ("Apache führt kein PHP aus. `libapache2-mod-php` fehlt.", "Ohne dieses Paket ist .php für Apache nur Text."),
            ("Die Datei hat den falschen Namen.", "Dann käme 404. Die Datei wurde ja gefunden."),
            ("MySQL fehlt noch.", "phpinfo() braucht keine Datenbank."),
        ]),
        ("Wofür ist das Paket `php-mysql`?", [
            ("Damit PHP mit MySQL sprechen kann. Es bringt mysqli.", "Ohne mysqli geht benutzer.php in Level 7 nicht."),
            ("Es installiert den MySQL-Server.", "Der Server kommt mit mysql-server in Level 5."),
            ("Es installiert phpMyAdmin.", "phpMyAdmin ist ein eigenes Paket in Level 5."),
        ]),
    ]},
    5: {"check": [
        "`mysql -e \"SELECT VERSION();\"` zeigt eine Versionsnummer.",
        "`http://<IP>/phpmyadmin` zeigt die Anmeldeseite.",
        "Ich kann mich in phpMyAdmin als `phpmyadmin` mit meinem Passwort anmelden.",
    ], "fragen": [
        ("Bei phpMyAdmin kommt die Frage nach dem Webserver. Wie wählst du apache2?", [
            ("Mit der Leertaste markieren. Dann mit Tab auf Ok.", "Nur mit Sternchen ist apache2 gewählt."),
            ("Mit Enter.", "Enter bestätigt. Aber nichts ist markiert. Dann kommt 404."),
            ("Mit den Pfeiltasten auf apache2 gehen reicht.", "Der Balken markiert nichts."),
        ]),
        ("Im Terminal geht `mysql` als root ohne Passwort. In phpMyAdmin geht root nicht. Warum?", [
            ("MySQL-root darf nur rein, wenn er auch auf dem Pi root ist.", "Darum legst du in Level 6 einen eigenen Benutzer an."),
            ("Das root-Passwort war falsch.", "root hat kein Passwort. Er meldet sich über Ubuntu an."),
            ("phpMyAdmin ist noch nicht fertig.", "Dann gäbe es gar keine Anmeldeseite."),
        ]),
    ]},
    6: {"check": [
        "`mysql < flutterdb.sql` läuft ohne Fehler.",
        "`SHOW TABLES;` in flutterDB zeigt `ToDoTB` und `flutterTB`.",
        "`SELECT * FROM ToDoTB;` zeigt *Pi einrichten* (1) und *API testen* (0).",
        "Ich kann mich in phpMyAdmin als `flutterUser` anmelden. Ich sehe nur flutterDB.",
    ], "fragen": [
        ("Was heißt `.*` in `GRANT ALL PRIVILEGES ON flutterDB.* TO …`?", [
            ("Alle Tabellen in flutterDB.", "Ohne .* meint MySQL eine Tabelle mit dem Namen flutterDB."),
            ("Alle Benutzer.", "Der Benutzer steht hinter TO."),
            ("Alle Datenbanken.", "Das wäre *.*. Das sind viel zu viele Rechte."),
        ]),
        ("Warum fehlt die `id` bei `INSERT INTO ToDoTB (name, checkbox) …`?", [
            ("AUTO_INCREMENT gibt die nächste Nummer selbst.", "Die Datenbank kennt die letzte Nummer."),
            ("Die id darf leer bleiben.", "Ein Primärschlüssel ist nie leer."),
            ("Primärschlüssel werden beim Einfügen nicht beachtet.", "Du darfst eine id angeben. Sie muss dann neu sein."),
        ]),
    ]},
    7: {"check": [
        "`http://<IP>/benutzer.php` zeigt eine JSON-Liste mit *berno* und *stoll*.",
        "In der Antwort steht kein `passwordLogin`.",
        "Firefox zeigt die Antwort im Reiter *JSON*. Der Content-Type stimmt.",
    ], "fragen": [
        ("Warum fragt benutzer.php nur `SELECT id, name` ab? Warum nicht `SELECT *`?", [
            ("Mit `*` könnte jeder im Netz das Passwort lesen.", "Eine API gibt nur heraus, was gebraucht wird."),
            ("`SELECT *` ist in PHP verboten.", "Es ist erlaubt. Aber gefährlich."),
            ("`SELECT *` geht nur in phpMyAdmin.", "SQL ist überall gleich."),
        ]),
        ("benutzer.php zeigt eine weiße Seite oder HTTP 500. Wo findest du den Grund?", [
            ("In `/var/log/apache2/error.log`.", "Dort steht zum Beispiel Access denied."),
            ("In `info.php`.", "info.php zeigt Einstellungen. Keine Fehler von deinem Programm."),
            ("In phpMyAdmin bei den Benutzern.", "Dort siehst du Benutzer. Aber nicht den PHP-Fehler."),
        ]),
    ]},
    8: {"check": [
        "`…/api.php/records/flutterTB` zeigt `{\"records\": […]}` mit den Benutzern.",
        "`…/api.php/records/flutterTB/1` zeigt genau 1 Datensatz.",
        "Ich habe mit curl ein ToDo angelegt (POST), abgehakt (PUT) und gelöscht (DELETE).",
    ], "fragen": [
        ("Wie hakst du das ToDo mit der id 3 ab?", [
            ("`PUT …/records/ToDoTB/3` mit `{\"checkbox\": true}`", "PUT ändert den Datensatz an seiner Adresse."),
            ("`POST …/records/ToDoTB/3` mit `{\"checkbox\": true}`", "POST legt neue Datensätze an. Ohne id in der Adresse."),
            ("`GET …/records/ToDoTB/3?checkbox=1`", "GET liest nur. Es ändert nie etwas."),
        ]),
        ("Was antwortet die API, wenn `POST` geklappt hat?", [
            ("Die id vom neuen Datensatz.", "Damit kann die App ihn später ändern oder löschen."),
            ("Den ganzen neuen Datensatz als JSON.", "Dafür brauchst du GET …/id."),
            ("Immer `1`.", "1 kommt bei PUT und DELETE. Das ist die Zahl der geänderten Zeilen."),
        ]),
    ]},
    9: {"check": [
        "`dart run` zeigt die ToDos von meinem Pi.",
        "Ein ToDo aus Dart steht auch im Browser unter `…/records/ToDoTB`.",
        "Abhaken und Löschen aus Dart gehen.",
        "Ist der Pi aus, kommt eine klare Fehlermeldung. Kein Absturz.",
    ], "fragen": [
        ("Warum steht `await` vor `http.get(…)`?", [
            ("Die Antwort braucht Zeit. `await` wartet auf das Future.", "Ohne await hast du nur ein Future. Noch keine Antwort."),
            ("`await` macht die Anfrage schneller.", "await wartet nur. Schneller wird nichts."),
            ("`await` braucht man für `jsonDecode`.", "jsonDecode geht sofort. Es wartet nicht."),
        ]),
        ("Was gibt `jsonDecode('{\"records\": [ … ]}')` in Dart zurück?", [
            ("Eine `Map<String, dynamic>`. Die Liste steht unter `records`.", "Geschweifte Klammern sind eine Map. Eckige Klammern sind eine Liste."),
            ("Eine `List` mit den ToDos.", "Die Liste steckt erst darin. Unter records."),
            ("Einen `String`.", "Vor jsonDecode ist es ein String."),
        ]),
    ]},
}
