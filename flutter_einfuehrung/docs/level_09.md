# Level 9 – Login öffnet die ToDo-Liste

**Ziel:** Aus zwei Teilen wird eine App: Erst kommt die Login-Maske aus Level 4, nach dem Login
die ToDo-Liste aus Level 8. Alle Daten bleiben lokal in der App – es gibt keine Datenbank.

**Sie ändern:** `lib/main.dart`, `lib/my_login.dart` · **Skript:** Beispiel 1 + Beispiel 2

## Auftrag
1. `lib/main.dart`: Starten Sie wieder `MyFirstApp` (die App mit der Login-Maske) statt `ToDoApp`.
2. `lib/my_login.dart`: Importieren Sie `todo_list.dart`.
3. Der Login-Button bekommt eine Aufgabe: Statt der leeren Funktion `() {}` öffnet er mit
   `Navigator.of(context).push(...)` die `ToDoList` als neue Seite.
4. Probieren Sie aus: einloggen, ToDos anlegen, mit dem Zurück-Pfeil zur Login-Maske, wieder einloggen.

## Erklärt – was passiert hier?

**Der Navigator – ein Stapel von Seiten.** Jede `MaterialApp` hat einen `Navigator`. Er verwaltet die
Seiten wie einen Stapel Karten: Sichtbar ist immer die oberste.

| Befehl | Wirkung | kennen Sie aus |
|---|---|---|
| `Navigator.of(context).push(route)` | legt eine neue Seite oben auf | neu |
| `Navigator.of(context).pop()` | nimmt die oberste Seite wieder weg | Level 6 (Dialog schließen) |

Der Login-Button aus Level 4 wird so ergänzt:

```dart
TextButton(
  onPressed: _canLogin
      ? () {
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (context) => const ToDoList(),
            ),
          );
        }
      : null,
  child: const Text('Login'),
),
```

- `MaterialPageRoute` ist die „Karte“ für den Stapel – `builder` baut das Widget, das darauf zu sehen ist.
- Weil die Liste **über** der Login-Seite liegt, zeigt ihre `AppBar` von selbst einen **Zurück-Pfeil**.
  Er ruft `pop()` auf – Sie müssen dafür nichts programmieren.
- Der Login-Button bleibt grau, solange ein Feld leer ist (`_canLogin` aus Level 4).

**Daten bleiben lokal.** Die ToDos stehen in der Map `todos` im State der `ToDoList` – also nur im
Arbeitsspeicher des Handys. Beim Zurück-Pfeil wird die Seite vom Stapel genommen, ihr State verschwindet
und mit ihm die ToDos. Auch nach einem Neustart der App ist die Liste leer. Ebenso wird das Passwort nicht
geprüft: Jeder Name mit Passwort wird angenommen. Eine echte App würde Benutzer und ToDos dafür auf einem
Server oder in einer Datenbank speichern – das ist hier bewusst nicht der Fall.

<details><summary>Tipp – „Undefined name 'ToDoList'“?</summary>

Es fehlt der Import oben in `my_login.dart`: `import 'todo_list.dart';`
</details>

<details><summary>Tipp – Nach dem Login fehlt der Zurück-Pfeil?</summary>

Haben Sie `pushReplacement` statt `push` verwendet? Dann wird die Login-Seite ersetzt statt überdeckt –
es gibt nichts mehr, wohin man zurück kann.
</details>

## Ausblick – warum als Nächstes eine Datenbank?

Ihre App funktioniert – aber nur, solange sie läuft. Probieren Sie es aus und Sie stoßen auf genau
die Grenzen, die eine Datenbank löst:

| Problem in Ihrer App | Ursache | Lösung mit Datenbank |
|---|---|---|
| Nach dem Zurück-Pfeil oder einem Neustart sind alle ToDos weg. | Die Map `todos` liegt nur im Arbeitsspeicher (im State). | Die ToDos werden **dauerhaft gespeichert** und beim Start wieder geladen. |
| Jeder Name mit irgendeinem Passwort kommt hinein. | Es gibt keine Liste der Benutzer, gegen die geprüft werden kann. | Benutzer und Passwörter (verschlüsselt) stehen in einer Tabelle – der Login **prüft** sie. |
| Anna und Ben sehen nach dem Login dieselbe leere Liste. | Die ToDos gehören zu niemandem. | Jedes ToDo wird einem **Benutzer zugeordnet** (Fremdschlüssel). |
| Auf dem Tablet fehlen die ToDos vom Handy. | Die Daten liegen nur auf einem Gerät. | Eine Datenbank auf einem Server macht die Daten **überall verfügbar**. |

Der nächste Schritt ist darum eine **Datenbankanbindung**: Die App schreibt neue ToDos in die Datenbank,
liest sie beim Start wieder aus und prüft den Login gegen gespeicherte Benutzer. Die Oberfläche, die Sie
gebaut haben, bleibt dabei fast unverändert – es ändern sich vor allem `addItem`, `deleteItem`,
`checkBoxDone` und der Login-Button.

> **Das ist Thema eines späteren Lernpfads.** Dort binden Sie Ihre App an eine Datenbank an. Behalten
> Sie Ihr Projekt `meine_app` – Sie bauen darauf auf.

**Merke:** `push` legt eine Seite auf den Stapel, `pop` nimmt sie herunter. Was im State einer Seite
gespeichert ist, lebt nur so lange wie diese Seite.

**Denkfrage:** Sie loggen sich ein, legen drei ToDos an, gehen zurück und loggen sich wieder ein. Warum
ist die Liste leer?
