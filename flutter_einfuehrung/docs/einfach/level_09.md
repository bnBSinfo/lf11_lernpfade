# Level 9 – Login öffnet die ToDo-Liste

**Ziel:** Aus 2 Teilen wird 1 App. Zuerst kommt die Login-Maske. Nach dem Login kommt die ToDo-Liste. Alle Daten bleiben in der App. Es gibt keine Datenbank.

**Du änderst:** `lib/main.dart` und `lib/my_login.dart` · **Skript:** Beispiel 1 und Beispiel 2

## Auftrag
1. **✏️ Ändern** `lib/main.dart`. Die App startet wieder mit der Login-Maske. Ersetze 2 Zeilen.
   {{code 0}}
2. **✏️ Ändern** `lib/my_login.dart`. Hole die ToDo-Liste mit `import`. Die Zeile steht oben unter dem 1. Import.
   {{code 1}}
3. **✏️ Ändern** `lib/my_login.dart`. Ganz unten in `build` steht der `TextButton`. Er hat eine leere Funktion `() {}`. Ersetze sie. Die neue Funktion öffnet die `ToDoList`.
   {{code 2}}
4. **▶️ Ausprobieren:** Logge dich ein. Lege ToDos an. Geh mit dem Pfeil zurück. Logge dich wieder ein.

## Profi-Auftrag
- Die App startet mit der Login-Maske (`MyFirstApp`).
- „Login“ öffnet die `ToDoList` als **neue Seite**. Der Pfeil in der AppBar führt zurück zur Login-Maske.
- Keine Datenbank: Alle Daten bleiben im State.
- Lies danach den *Ausblick*: Warum brauchst du bald eine Datenbank?

*Kommst du nicht weiter? Schalte oben auf **🧭 Begleitet** um.*

## Erklärt – was passiert hier?

**Der Navigator ist ein Stapel von Seiten.** Jede `MaterialApp` hat einen `Navigator`. Er legt Seiten übereinander. Wie Karten auf einem Stapel. Du siehst immer die oberste Karte.

| Befehl | was passiert | kennst du aus |
|---|---|---|
| `Navigator.of(context).push(route)` | Eine neue Seite kommt oben drauf. | neu |
| `Navigator.of(context).pop()` | Die oberste Seite geht weg. | Level 6 (Dialog schließen) |

So sieht der Login-Button jetzt aus:

{{code 3}}

- `MaterialPageRoute` ist die Karte für den Stapel. `builder` baut das Widget auf der Karte.
- Die Liste liegt **über** der Login-Seite. Darum zeigt ihre `AppBar` einen **Pfeil zurück**. Der Pfeil ruft `pop()` auf. Das musst du nicht programmieren.
- Ist ein Feld leer? Dann bleibt der Login-Button grau. Das kommt von `_canLogin` aus Level 4.

**Die Daten bleiben in der App.** Die ToDos stehen in der Map `todos`. Die Map ist im State der `ToDoList`. Der State liegt nur im Arbeitsspeicher vom Handy.

- Du drückst den Pfeil zurück. Die Seite geht vom Stapel. Ihr State ist weg. Die ToDos sind auch weg.
- Du startest die App neu. Die Liste ist leer.
- Das Passwort wird nicht geprüft. Jeder Name mit Passwort kommt hinein.

Eine echte App speichert Benutzer und ToDos auf einem Server oder in einer Datenbank. Das machen wir hier noch nicht.

<details><summary>Tipp – „Undefined name 'ToDoList'“?</summary>

Der Import fehlt. Schreibe oben in `my_login.dart`: `import 'todo_list.dart';`
</details>

<details><summary>Tipp – Nach dem Login fehlt der Pfeil zurück?</summary>

Hast du `pushReplacement` geschrieben? Dann ist die Login-Seite weg. Es gibt nichts, wohin du zurück kannst. Schreibe `push`.
</details>

## Ausblick – warum als Nächstes eine Datenbank?

Deine App läuft. Aber nur, solange sie offen ist. Probiere es aus. Du findest 4 Probleme. Eine Datenbank löst sie.

| Problem | Grund | Lösung mit Datenbank |
|---|---|---|
| Nach dem Pfeil zurück sind die ToDos weg. Nach dem Neustart auch. | Die Map `todos` ist nur im Arbeitsspeicher. | Die ToDos werden **gespeichert**. Beim Start werden sie geladen. |
| Jeder Name mit jedem Passwort kommt hinein. | Es gibt keine Liste mit Benutzern. | Benutzer und Passwörter stehen in einer Tabelle. Der Login **prüft** sie. Die Passwörter sind verschlüsselt. |
| Anna und Ben sehen dieselbe leere Liste. | Die ToDos gehören niemandem. | Jedes ToDo **gehört einem Benutzer**. Das regelt ein Fremdschlüssel. |
| Auf dem Tablet fehlen die ToDos vom Handy. | Die Daten sind nur auf 1 Gerät. | Die Datenbank ist auf einem Server. Die Daten sind **überall da**. |

Darum kommt als Nächstes die **Datenbankanbindung**. Die App schreibt neue ToDos in die Datenbank. Beim Start liest sie die ToDos aus. Der Login prüft die Benutzer. Die Oberfläche bleibt fast gleich. Es ändern sich vor allem `addItem`, `deleteItem`, `checkBoxDone` und der Login-Button.

> **Das lernst du in einem späteren Lernpfad.** Dort verbindest du deine App mit einer Datenbank. Behalte dein Projekt `meine_app`. Du baust darauf auf.

**Merke:** `push` legt eine Seite auf den Stapel. `pop` nimmt sie weg. Die Daten im State leben nur so lange wie ihre Seite.

**Denkfrage:** Du loggst dich ein. Du legst 3 ToDos an. Du gehst zurück. Du loggst dich wieder ein. Warum ist die Liste leer?
