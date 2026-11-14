# Bonus – Server absichern und App anbinden

Für alle, die fertig sind. Ihre Prüfung (`dart run tool/pruefen.dart`) soll grün bleiben.

1. **Flutter-App anbinden:** Kopieren Sie `lib/todo_api.dart` in Ihr Projekt aus der Flutter-Einführung (`flutter pub add http`). Laden Sie die ToDos in `initState()` mit `TodoApi.alle()` und rufen Sie beim Hinzufügen, Abhaken und Löschen die passenden Methoden auf. Android: In `AndroidManifest.xml` sind unverschlüsselte HTTP-Verbindungen nur mit `android:usesCleartextTraffic="true"` erlaubt.
2. **Aufräumen:** Löschen Sie `info.php` – sie verrät Angreifern Versionen und Pfade.
3. **Passwort verstecken:** Die API zeigt `passwordLogin` an. Sorgen Sie dafür, dass die Spalte nicht mehr ausgegeben wird – z. B. mit der Middleware `authorization` und `authorization.columnHandler` in `$config` (Doku der php-crud-api).
4. **Passwörter hashen:** Speichern Sie statt des Klartextes einen Hash (`password_hash()` in PHP). Schreiben Sie eine `login.php`, die Name und Passwort per POST prüft (`password_verify()`) und nur `{"ok": true}` oder `{"ok": false}` antwortet.
5. **.git-Ordner:** Wer die API wie im Skript mit `git clone` installiert hat: Rufen Sie `http://<IP>/php-crud-api/.git/config` auf. Warum ist das ein Problem? Löschen Sie alles außer `api.php` – so wie beim Download.
6. **Firewall:** Erlauben Sie mit `ufw` nur SSH und HTTP: `ufw allow ssh`, `ufw allow http`, `ufw enable`. Was passiert mit phpMyAdmin?
7. **Fernsteuerung mit Desktop:** `apt install xrdp` und `systemctl enable --now xrdp` – dann mit *Remotedesktopverbindung* von Windows auf den Pi. Wer mag, installiert vorher `ubuntu-mate-desktop` (Skript: Optionale Softwareanpassungen).
8. **Feste IP:** Richten Sie mit `nmcli` eine feste IP ein – oder sprechen Sie mit der Netzwerkverwaltung über eine DHCP-Reservierung.
