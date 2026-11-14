# Level 1 – Das Grundgerüst

**Ziel:** Sie bauen mit nur zwei Widgets – `MaterialApp` und `Scaffold` – das
Grundgerüst einer App im Material Design.

**Sie schreiben:** ein neues Projekt `meine_app` – `lib/main.dart`, `lib/my_first_app.dart` · **Skript:** Kapitel 3 und 4a

## Vorher verstehen: `main()` und `runApp()`
In der Methode `main()` startet jedes Dart-Programm. Eine Flutter-App übergibt dort ihr Start-Widget an
`runApp()` – bei Ihnen die Klasse `MyFirstApp`. Diese App bauen Sie in allen 8 Leveln Schritt für Schritt aus.

## Auftrag
1. Legen Sie ein neues Flutter-Projekt an – in Android Studio (*New Flutter Project*, Name `meine_app`) oder im Terminal:
   ```bash
   flutter create meine_app
   ```
2. Löschen Sie den **gesamten** Inhalt von `lib/main.dart` und die Datei `test/widget_test.dart` (sie passt nicht mehr zu Ihrer App).
3. Legen Sie die Datei `lib/my_first_app.dart` an (Rechtsklick auf `lib` → *New → Dart File*). Schreiben Sie darin:
   - `import 'package:flutter/material.dart';`
   - die Klasse `MyFirstApp` als **Stateless Widget** mit Konstruktor `const MyFirstApp({super.key});`
   - eine `build`-Methode, die eine `MaterialApp` zurückgibt. Deren `home` ist ein `Scaffold`, dessen `body` ist
     `Text('Das ist mein Grundgerüst')`.
4. Schreiben Sie in `lib/main.dart` die beiden Imports (`material.dart` und `my_first_app.dart`) und
   `void main() { runApp(const MyFirstApp()); }`
5. Starten Sie die App (Emulator oder Chrome). Nach jeder Änderung genügt **Hot Reload** (Blitz-Symbol bzw. `r`).

Tipp: Tippen Sie `stless` und drücken Sie Tab – die IDE erzeugt das Grundgerüst eines Stateless Widgets.

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
