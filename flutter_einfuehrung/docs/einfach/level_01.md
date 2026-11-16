# Level 1 – Das Grundgerüst

**Ziel:** Du baust das Grundgerüst einer App. Du brauchst dafür nur 2 Widgets: `MaterialApp` und `Scaffold`.

**Du schreibst:** ein neues Projekt `meine_app` mit `lib/main.dart` und `lib/my_first_app.dart` · **Skript:** Kapitel 3 und 4a

## Vorher verstehen: `main()` und `runApp()`
Jedes Dart-Programm startet in `main()`. Dort steht `runApp()`. `runApp()` bekommt das Start-Widget. Bei dir heißt es `MyFirstApp`. Diese App baust du in 9 Leveln aus.

## Auftrag
1. **📁 Projekt anlegen.** Nimm Android Studio: *New Flutter Project*. Der Name ist `meine_app`. Oder tippe im Terminal:
   {{code 0}}
2. **🗑️ Löschen**
   - Öffne `lib/main.dart`. Markiere alles mit Strg/Cmd + A. Lösche es. Die Datei bleibt leer da.
   - Lösche die Datei `test/widget_test.dart`. Du brauchst sie nicht.
3. **📄 Neue Datei** `lib/my_first_app.dart`. Rechtsklick auf `lib` → *New → Dart File*. Die Datei ist leer. Tippe alles neu.
   Tipp: Tippe `stless` und drücke Tab. Dann steht der Rahmen schon da.
   {{code 1}}
4. **✏️ Ändern** `lib/main.dart`. Die Datei ist leer. Tippe diese Zeilen:
   {{code 2}}
5. **▶️ Starten.** Starte die App im Emulator oder in Chrome. Nach jeder Änderung: **Hot Reload** (Blitz oder `r`).

## Profi-Auftrag
Baue eine App mit eigenem Start-Widget.

- Lege das Projekt `meine_app` an. Lösche den Beispiel-Code in `lib/main.dart`. Lösche `test/widget_test.dart`.
- `lib/my_first_app.dart`: Stateless Widget `MyFirstApp` → `MaterialApp` → `Scaffold`. Der body zeigt „Das ist mein Grundgerüst“.
- `lib/main.dart` startet `MyFirstApp`.
- Die App läuft im Emulator oder in Chrome.

*Kommst du nicht weiter? Schalte oben auf **🧭 Begleitet** um.*

## Erklärt – was passiert hier?

**Zeile für Zeile:**

- `import 'package:flutter/material.dart';` holt die Material-Widgets in die Datei. Zum Beispiel `Text` und `Scaffold`.
- `class MyFirstApp extends StatelessWidget` ist deine Klasse. Sie ist ein **Stateless Widget**. Es zeigt immer dasselbe. Es merkt sich nichts.
- `const MyFirstApp({super.key});` ist der Konstruktor. Er bekommt hier keine Daten.
- `Widget build(BuildContext context)` zeichnet dein Widget. Flutter ruft `build` auf. Was `build` zurückgibt, siehst du auf dem Bildschirm.

**Die 3 Widgets:**

| Widget | Aufgabe | im Code |
|---|---|---|
| `MaterialApp` | Das ist die App. Sie regelt Farben, Schrift und Seiten. | `home:` ist die Startseite. |
| `Scaffold` | Das ist das Gerüst für 1 Seite. | `appBar:`, `body:` … |
| `Text` | Das zeigt einen Text. | Der Text steht in Klammern. |

Probiere unten den **Baukasten** aus. Dort siehst du die Bereiche vom Scaffold. In Level 1 füllst du nur `body`.

**Der Text steht ganz oben links. Warum?** Ein `Text` ist nur so groß wie sein Inhalt. Ohne Anweisung steht er oben links. Es gibt noch keine `AppBar`. Darum beginnt der `body` ganz oben. Abstand und Mitte lernst du in Level 2.

<details><summary>Tipp 1</summary>

Du steckst Widgets ineinander. Beispiel: `MaterialApp(home: …)`. An die Stelle der Punkte kommt das nächste Widget.
</details>

<details><summary>Tipp 2</summary>

{{code 3}}
</details>

> **Merke:** `MaterialApp` ist die App. `Scaffold` ist 1 Seite. Die Seite hat Bereiche: AppBar, Body und mehr.

**Denkfrage:** Warum steht der Text ganz oben links?
