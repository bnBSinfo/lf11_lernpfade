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
