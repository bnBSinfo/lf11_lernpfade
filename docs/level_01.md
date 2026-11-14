# Level 1 – Das Grundgerüst

**Ziel:** Sie bauen mit nur zwei Widgets – `MaterialApp` und `Scaffold` – das
Grundgerüst einer App im Material Design.

**Datei:** `lib/level_01/my_first_app.dart` · **Skript:** Kapitel 3 und 4a

## Vorher verstehen: `main()` und `runApp()`
Öffnen Sie `lib/main.dart`. In der Methode `main()` läuft die App: Das Start-Widget
wird an `runApp()` übergeben. Hier ist das Ihre Klasse `MyFirstApp`.

## Auftrag
`MyFirstApp` ist ein **Stateless Widget** – es ändert sich zur Laufzeit nicht.
Seine `build`-Methode gibt zurück, was angezeigt wird.

1. Geben Sie statt `const Placeholder()` eine `MaterialApp` zurück.
2. Weisen Sie `home` ein `Scaffold` zu.
3. Der `body` des Scaffold ist `Text('Das ist mein Grundgerüst')`.

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

Probieren Sie im **Baukasten** auf der Webseite zur Flutter-Einführung aus, welche Bereiche ein Scaffold hat. Sie füllen davon nur, was Sie brauchen – in Level 1 nur `body`.

**Warum steht der Text oben links unter der Statusleiste?** Ein `Text` ist nur so groß wie sein Inhalt und steht ohne weitere Anweisung oben links. Ohne `AppBar` beginnt der `body` ganz oben. Ausrichtung und Abstand sind in Flutter eigene Widgets – das lernen Sie in Level 2.

## Prüfen
`flutter test test/level_01_test.dart` · Ansehen: `aktivesLevel = 1` in `lib/main.dart`

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
