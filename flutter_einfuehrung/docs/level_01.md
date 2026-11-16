# Level 1 – Das Grundgerüst

**Ziel:** Sie bauen mit nur zwei Widgets – `MaterialApp` und `Scaffold` – das
Grundgerüst einer App im Material Design.

**Sie schreiben:** ein neues Projekt `meine_app` – `lib/main.dart`, `lib/my_first_app.dart` · **Skript:** Kapitel 3 und 4a

## Vorher verstehen: `main()` und `runApp()`
In der Methode `main()` startet jedes Dart-Programm. Eine Flutter-App übergibt dort ihr Start-Widget an
`runApp()` – bei Ihnen die Klasse `MyFirstApp`. Diese App bauen Sie in allen 9 Leveln Schritt für Schritt aus.

## Auftrag
1. **📁 Projekt anlegen** – in Android Studio (*New Flutter Project*, Name `meine_app`) oder im Terminal:
   ```bash
   flutter create meine_app
   ```
2. **🗑️ Löschen**
   - In `lib/main.dart`: den **gesamten Inhalt** markieren (Strg/Cmd + A) und löschen – die Datei bleibt, ist aber leer.
   - Die Datei `test/widget_test.dart` **ganz** löschen (sie passt nicht mehr zu Ihrer App).
3. **📄 Neue Datei** `lib/my_first_app.dart` (Rechtsklick auf `lib` → *New → Dart File*). Die Datei ist leer – alles wird neu getippt.
   Tipp: `stless` + Tab erzeugt den Rahmen der Klasse, Sie ergänzen nur noch Namen und `build`-Inhalt.
   ```diff
   + import 'package:flutter/material.dart';
   +
   + class MyFirstApp extends StatelessWidget {
   +   const MyFirstApp({super.key});
   +
   +   @override
   +   Widget build(BuildContext context) {
   +     return const MaterialApp(
   +       home: Scaffold(
   +         body: Text('Das ist mein Grundgerüst'),
   +       ),
   +     );
   +   }
   + }
   ```
4. **✏️ Ändern** `lib/main.dart` – in die jetzt leere Datei tippen:
   ```diff
   + import 'package:flutter/material.dart';
   + import 'my_first_app.dart';
   +
   + void main() {
   +   runApp(const MyFirstApp());
   + }
   ```
5. **▶️ Starten** (Emulator oder Chrome). Nach jeder Änderung genügt **Hot Reload** (Blitz-Symbol bzw. `r`).

## Profi-Auftrag
Eine lauffähige Flutter-App mit eigenem Start-Widget.

- Neues Projekt `meine_app` anlegen; den Beispielcode aus `lib/main.dart` und die Datei `test/widget_test.dart` entfernen.
- `lib/my_first_app.dart`: Stateless Widget `MyFirstApp` → `MaterialApp` → `Scaffold`; der body zeigt „Das ist mein Grundgerüst“.
- `lib/main.dart` startet `MyFirstApp`.
- Die App läuft im Emulator oder in Chrome.

*Hängen Sie fest? Schalten Sie oben auf **🧭 Begleitet** um – dort steht jeder Schritt mit Code-Rahmen.*

## Erklärt – was passiert hier?

**Zeile für Zeile:**

- `import 'package:flutter/material.dart';` holt alle Material-Widgets (Text, Scaffold, …) in die Datei.
- `class MyFirstApp extends StatelessWidget` – eine eigene Klasse, die ein **Stateless Widget** ist. Sie zeigt immer dasselbe an und merkt sich nichts.
- `const MyFirstApp({super.key});` – der Konstruktor. Er bekommt hier keine Daten.
- `@override Widget build(BuildContext context)` – diese Methode ruft Flutter auf, wenn es Ihr Widget zeichnen will. Was sie zurückgibt, erscheint auf dem Bildschirm.

**Die drei Widgets:**

| Widget | Aufgabe | Eigenschaft im Code |
|---|---|---|
| `MaterialApp` | die App selbst: Design (Farben, Schriften), Navigation zwischen Seiten | `home:` = die Startseite |
| `Scaffold` | das Gerüst **einer Seite** mit festen Bereichen | `appBar:`, `body:`, `floatingActionButton:`, … |
| `Text` | zeigt eine Zeichenkette | der Text in Klammern |

Probieren Sie im **Baukasten** unten aus, welche Bereiche ein Scaffold hat. Sie füllen davon nur, was Sie brauchen – in Level 1 nur `body`.

**Warum steht der Text oben links unter der Statusleiste?** Ein `Text` ist nur so groß wie sein Inhalt und steht ohne weitere Anweisung oben links. Ohne `AppBar` beginnt der `body` ganz oben. Ausrichtung und Abstand sind in Flutter eigene Widgets – das lernen Sie in Level 2.

<details><summary>Tipp 1</summary>

Widgets werden ineinander gesteckt: `MaterialApp(home: …)` – an die Stelle der
Punkte kommt das nächste Widget.
</details>

<details><summary>Tipp 2</summary>

```dart
return const MaterialApp(
  home: Scaffold(
    body: /* hier Ihr Text-Widget */,
  ),
);
```
</details>

> **Merke:** `MaterialApp` bringt Navigation und Theme mit, `Scaffold` teilt die
> Oberfläche in AppBar, Body und BottomNavigationBar.

**Denkfrage:** Warum steht der Text ganz oben links – und sogar unter der Statusleiste?
