"""Selbstkontrolle je Level: Checkliste und Kontrollfragen (Falschantworten = typische Fehler)."""

KONTROLLE = {
    1: {"check": [
        "Der Pi startet mit Ubuntu, ich bin als `administrator` angemeldet.",
        "`apt update` und `apt upgrade` laufen ohne Fehlermeldung durch.",
        "Ich habe die IP-Adresse meines Pi notiert (`hostname -I`).",
        "Vom PC aus antwortet der Pi auf `ping <IP>`.",
    ], "fragen": [
        ("Was macht `apt update`?", [
            ("Es lädt die Liste der verfügbaren Pakete neu und installiert nichts.", True,
             "Erst die Liste aktualisieren, dann mit apt upgrade installieren."),
            ("Es installiert neuere Versionen aller Programme.", False, "Das macht apt upgrade."),
            ("Es aktualisiert Ubuntu auf die nächste Hauptversion.", False,
             "Dafür gibt es do-release-upgrade – apt update lädt nur die Paketliste."),
        ]),
        ("Woran erkennen Sie, dass Sie nach `sudo -i` als root arbeiten?", [
            ("Die Eingabezeile endet mit `#`.", True, "# = root, $ = normaler Benutzer."),
            ("Die Eingabezeile endet mit `$`.", False, "$ zeigt einen normalen Benutzer."),
            ("Vor jedem Befehl muss weiter `sudo` stehen.", False, "Genau das entfällt nach sudo -i."),
        ]),
    ]},
    2: {"check": [
        "`systemctl status ssh` zeigt *active (running)*.",
        "Ich kann mich vom PC aus mit `ssh administrator@<IP>` (oder MobaXterm) anmelden.",
        "`hostname` im SSH-Fenster zeigt den Namen meines Pi, nicht den des PC.",
    ], "fragen": [
        ("Auf welchem Port wartet ein SSH-Server standardmäßig?", [
            ("22", True, "SSH = Port 22."),
            ("80", False, "Port 80 ist HTTP – der Webserver aus Level 3."),
            ("3306", False, "3306 ist MySQL."),
        ]),
        ("Was bewirkt `systemctl enable --now ssh`?", [
            ("Der Dienst startet sofort und bei jedem Hochfahren.", True, "enable = beim Booten, --now = sofort."),
            ("Der Dienst startet nur jetzt, nach einem Neustart nicht mehr.", False, "Das wäre systemctl start ssh."),
            ("SSH wird installiert.", False, "Installiert wird mit apt install openssh-server."),
        ]),
    ]},
    3: {"check": [
        "Im Browser des PC erscheint unter `http://<IP>` die *Apache2 Ubuntu Default Page*.",
        "`systemctl status apache2` zeigt *active (running)*.",
        "`ls /var/www/html` zeigt die Datei `index.html`.",
    ], "fragen": [
        ("Wo muss die Datei liegen, damit sie unter `http://<IP>/test.html` erreichbar ist?", [
            ("`/var/www/html/test.html`", True, "/var/www/html ist das Wurzelverzeichnis (DocumentRoot)."),
            ("`/home/administrator/test.html`", False, "Das Home-Verzeichnis liefert Apache nicht aus."),
            ("`/etc/apache2/test.html`", False, "In /etc/apache2 liegt die Konfiguration, keine Webseiten."),
        ]),
        ("Was antwortet der Webserver, wenn die angefragte Datei nicht existiert?", [
            ("404 Not Found", True, "404 = nicht gefunden."),
            ("200 OK", False, "200 heißt: alles gut, Inhalt kommt."),
            ("500 Internal Server Error", False, "500 bedeutet einen Fehler im Programm auf dem Server."),
        ]),
    ]},
    4: {"check": [
        "`http://<IP>/info.php` zeigt die bunte PHP-Infoseite – nicht den Quelltext.",
        "Auf der Infoseite gibt es einen Abschnitt `mysqli`.",
        "Nach dem Installieren der Pakete habe ich `systemctl restart apache2` ausgeführt.",
    ], "fragen": [
        ("Der Browser zeigt `<?php phpinfo(); ?>` als Text an. Was ist die Ursache?", [
            ("Apache führt kein PHP aus – `libapache2-mod-php` fehlt.", True,
             "Ohne das Modul behandelt Apache .php wie eine Textdatei."),
            ("Die Datei heißt falsch.", False, "Dann käme 404 – die Datei wurde ja gefunden."),
            ("MySQL ist noch nicht installiert.", False, "phpinfo() braucht keine Datenbank."),
        ]),
        ("Wozu dient das Paket `php-mysql`?", [
            ("Es bringt die Erweiterung mysqli, damit PHP mit MySQL sprechen kann.", True,
             "Ohne mysqli kann benutzer.php in Level 7 keine Verbindung öffnen."),
            ("Es installiert den MySQL-Server.", False, "Der Server kommt mit mysql-server (Level 5)."),
            ("Es installiert phpMyAdmin.", False, "phpMyAdmin ist ein eigenes Paket (Level 5)."),
        ]),
    ]},
    5: {"check": [
        "`mysql -e \"SELECT VERSION();\"` zeigt eine Versionsnummer.",
        "`http://<IP>/phpmyadmin` zeigt die Anmeldeseite von phpMyAdmin.",
        "Ich kann mich in phpMyAdmin als `phpmyadmin` mit dem vergebenen Passwort anmelden.",
    ], "fragen": [
        ("Bei der Installation von phpMyAdmin erscheint die Webserver-Auswahl. Wie wählen Sie apache2 richtig aus?", [
            ("Mit der Leertaste markieren (Sternchen), dann mit Tab auf Ok.", True,
             "Nur mit Sternchen wird phpMyAdmin im Apache eingebunden."),
            ("Mit Enter.", False, "Enter bestätigt – ohne dass etwas markiert ist. Dann gibt es 404."),
            ("Mit den Pfeiltasten auf apache2 gehen genügt.", False, "Der Balken allein markiert nichts."),
        ]),
        ("Warum klappt `mysql` als root im Terminal ohne Passwort, die Anmeldung als root in phpMyAdmin aber nicht?", [
            ("MySQL-root darf sich nur anmelden, wenn er auch auf dem Pi root ist (auth_socket).", True,
             "Deshalb legen Sie in Level 6 einen eigenen Benutzer für Programme an."),
            ("Das root-Passwort wurde falsch eingegeben.", False, "root hat gar kein Passwort – er meldet sich über das Betriebssystem an."),
            ("phpMyAdmin ist noch nicht fertig installiert.", False, "Dann käme die Anmeldeseite gar nicht."),
        ]),
    ]},
    6: {"check": [
        "`mysql < flutterdb.sql` läuft ohne Fehlermeldung durch.",
        "`SHOW TABLES;` in flutterDB zeigt `ToDoTB` und `flutterTB`.",
        "`SELECT * FROM ToDoTB;` zeigt *Pi einrichten* (1) und *API testen* (0).",
        "Ich kann mich in phpMyAdmin als `flutterUser` anmelden und sehe nur die Datenbank flutterDB.",
    ], "fragen": [
        ("Was bedeutet `.*` in `GRANT ALL PRIVILEGES ON flutterDB.* TO …`?", [
            ("Alle Tabellen der Datenbank flutterDB.", True, "Ohne .* meint MySQL eine Tabelle namens flutterDB."),
            ("Alle Benutzer.", False, "Der Benutzer steht hinter TO."),
            ("Alle Datenbanken.", False, "Alle Datenbanken wären *.* – viel zu viele Rechte."),
        ]),
        ("Warum steht die `id` beim `INSERT INTO ToDoTB (name, checkbox) …` nicht dabei?", [
            ("AUTO_INCREMENT vergibt die nächste Nummer selbst.", True, "Die Datenbank kennt die letzte Nummer am besten."),
            ("Die id darf leer (NULL) bleiben.", False, "Ein Primärschlüssel ist nie NULL."),
            ("Primärschlüssel werden beim Einfügen ignoriert.", False,
             "Man darf eine id angeben – sie muss dann aber eindeutig sein."),
        ]),
    ]},
    7: {"check": [
        "`http://<IP>/benutzer.php` zeigt eine JSON-Liste mit *berno* und *stoll*.",
        "In der Antwort steht kein `passwordLogin`.",
        "Firefox zeigt die Antwort im Reiter *JSON* an – der Content-Type stimmt.",
    ], "fragen": [
        ("Warum fragt benutzer.php nur `SELECT id, name` ab und nicht `SELECT *`?", [
            ("Mit `*` würde auch das Passwort für jeden im Netz lesbar.", True,
             "Eine API gibt nur heraus, was der Empfänger wirklich braucht."),
            ("`SELECT *` ist in PHP nicht erlaubt.", False, "Erlaubt ist es – aber gefährlich."),
            ("`SELECT *` funktioniert nur in phpMyAdmin.", False, "SQL ist überall gleich."),
        ]),
        ("benutzer.php zeigt eine weiße Seite bzw. HTTP 500. Wo finden Sie die Ursache?", [
            ("In `/var/log/apache2/error.log`.", True, "Dort steht z. B. Access denied oder Table doesn't exist."),
            ("In `info.php`.", False, "info.php zeigt die Konfiguration, keine Fehler Ihres Programms."),
            ("In phpMyAdmin unter Benutzerkonten.", False, "Dort sehen Sie Benutzer, aber nicht den PHP-Fehler."),
        ]),
    ]},
    8: {"check": [
        "`…/api.php/records/flutterTB` zeigt `{\"records\": […]}` mit den Benutzern.",
        "`…/api.php/records/flutterTB/1` zeigt genau einen Datensatz.",
        "Ich habe mit curl ein ToDo angelegt (POST), abgehakt (PUT) und gelöscht (DELETE).",
    ], "fragen": [
        ("Mit welcher Anfrage haken Sie das ToDo mit der id 3 ab?", [
            ("`PUT …/records/ToDoTB/3` mit `{\"checkbox\": true}`", True, "PUT ändert den Datensatz unter seiner Adresse."),
            ("`POST …/records/ToDoTB/3` mit `{\"checkbox\": true}`", False,
             "POST legt neue Datensätze an – und zwar an der Tabelle, ohne id."),
            ("`GET …/records/ToDoTB/3?checkbox=1`", False, "GET liest nur, es ändert nie etwas."),
        ]),
        ("Was antwortet die php-crud-api auf ein erfolgreiches `POST`?", [
            ("Die id des neuen Datensatzes.", True, "Damit kann die App den Eintrag später ändern oder löschen."),
            ("Den kompletten neuen Datensatz als JSON.", False, "Dafür müssten Sie ihn mit GET …/id holen."),
            ("Immer `1`.", False, "1 (= Anzahl geänderter Zeilen) kommt bei PUT und DELETE."),
        ]),
    ]},
    9: {"check": [
        "`dart run` zeigt die ToDos von meinem Pi an.",
        "Ein in Dart angelegtes ToDo erscheint auch im Browser unter `…/records/ToDoTB`.",
        "Abhaken und Löschen aus Dart funktionieren.",
        "Ist der Pi aus, erscheint eine verständliche Fehlermeldung statt eines Absturzes mit Stacktrace.",
    ], "fragen": [
        ("Warum steht `await` vor `http.get(…)`?", [
            ("Die Antwort kommt erst nach einer Weile über das Netz – `await` wartet auf das Future.", True,
             "Ohne await hätten Sie nur ein Future, noch keine Antwort."),
            ("`await` macht die Anfrage schneller.", False, "await wartet nur – schneller wird nichts."),
            ("`await` wird für `jsonDecode` gebraucht.", False, "jsonDecode arbeitet sofort, es ist nicht asynchron."),
        ]),
        ("Was liefert `jsonDecode('{\"records\": [ … ]}')` in Dart?", [
            ("Eine `Map<String, dynamic>` – die Liste steht unter dem Schlüssel `records`.", True,
             "Geschweifte Klammern = Map, eckige Klammern = List."),
            ("Eine `List` mit den ToDos.", False, "Die Liste steckt erst darin, unter records."),
            ("Einen `String`.", False, "Ein String ist es vor jsonDecode."),
        ]),
    ]},
}
