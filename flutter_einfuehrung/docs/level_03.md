# Level 3 – Das erste Stateful Widget

**Ziel:** Sie legen ein Stateful Widget an, lagern es in eine eigene Datei aus und
binden es in das Stateless Widget ein.

**Sie schreiben:** `lib/my_first_app.dart` ändern, `lib/my_login.dart` neu ·
**Skript:** Kapitel 4b

## Auftrag
1. **✏️ Ändern** `lib/my_first_app.dart` – eine `appBar` **hinzufügen**. Weil `AppBar` nicht `const` sein kann,
   wird das `const` vor `MaterialApp` **gelöscht** und stattdessen vor `Text` geschrieben:
   ```diff
       Widget build(BuildContext context) {
   -     return const MaterialApp(
   +     return MaterialApp(
           home: Scaffold(
   +         appBar: AppBar(title: const Text('Meine erste App')),
             body: Padding(
               … (Ihr body aus Level 2 bleibt vorerst)
   ```
2. **📄 Neue Datei** `lib/my_login.dart` mit dem **Stateful Widget** `MyLogin`. Es besteht aus **zwei Klassen**.
   Tipp: `stful` + Tab erzeugt beide Klassen auf einmal.
   ```diff
   + import 'package:flutter/material.dart';
   +
   + class MyLogin extends StatefulWidget {
   +   const MyLogin({super.key});
   +
   +   @override
   +   State<MyLogin> createState() => _MyLoginState();
   + }
   +
   + class _MyLoginState extends State<MyLogin> {
   +   @override
   +   Widget build(BuildContext context) {
   +     return const Center(
   +       child: Text('Willkommen im Stateful Widget'),
   +     );
   +   }
   + }
   ```
3. **✏️ Ändern** `lib/my_first_app.dart` – die neue Datei einbinden und den **ganzen** `body` aus Level 2
   (das `Padding` mit allem darin) durch `MyLogin` **ersetzen**:
   ```diff
     import 'package:flutter/material.dart';
   + import 'my_login.dart';
     …
           appBar: AppBar(title: const Text('Meine erste App')),
   -       body: Padding(
   -         … (das ganze Padding mit ColoredBox, Center, Text)
   -       ),
   +       body: const MyLogin(),
   ```

Dateinamen schreibt man in `snake_case` (`my_login.dart`), Klassennamen in `UpperCamelCase` (`MyLogin`) –
so lagert man Widgets aus.

## Profi-Auftrag
- Die App bekommt eine AppBar mit dem Titel „Meine erste App“.
- Neue Datei `lib/my_login.dart` mit dem **Stateful Widget** `MyLogin`; es zeigt zentriert „Willkommen im Stateful Widget“.
- `MyFirstApp` zeigt `MyLogin` als body.

*Hängen Sie fest? Schalten Sie oben auf **🧭 Begleitet** um – dort steht jeder Schritt mit Code-Rahmen.*

## Erklärt – was passiert hier?

**Warum zwei Klassen?** Widgets sind in Flutter unveränderlich. Soll sich etwas ändern (Text, Haken, Liste), braucht man einen Ort, an dem die **veränderlichen Daten** liegen – das ist das **State-Objekt**.

```dart
class MyLogin extends StatefulWidget {          // ① das Widget – unveränderlich
  const MyLogin({super.key});

  @override
  State<MyLogin> createState() => _MyLoginState();  // ② erzeugt EINMAL den State
}

class _MyLoginState extends State<MyLogin> {    // ③ der State – merkt sich Daten
  @override
  Widget build(BuildContext context) {          // ④ build steht im State!
    return const Center(child: Text('Willkommen im Stateful Widget'));
  }
}
```

1. **Das Widget** hat nur eine Aufgabe: `createState()`.
2. `=>` ist die Kurzschreibweise für `{ return _MyLoginState(); }`.
3. **Der State** gehört über `State<MyLogin>` fest zu seinem Widget. Der `_` macht die Klasse privat für diese Datei.
4. **`build` steht im State**, nicht im Widget – denn nur der State kennt die aktuellen Daten.

Noch hat der State keine Daten – das kommt in Level 4. Ausführlich mit Vergleichstabelle und Lebenszyklus: **📘 Wissen: Stateless & Stateful** (oben in der Leiste).

**Warum eine eigene Datei?** Je größer die App, desto unübersichtlicher wird eine einzige `main.dart`. Jedes größere Widget bekommt deshalb eine eigene Datei in `snake_case` (`my_login.dart`) und wird mit `import 'my_login.dart';` eingebunden.

**AppBar:** Mit `appBar:` füllen Sie einen weiteren Bereich des Scaffold. Der `body` beginnt jetzt **unter** der AppBar. Probieren Sie es im Baukasten in Level 1 aus.

<details><summary>Tipp 1</summary>

Tippen Sie in einer leeren Zeile `stful` und drücken Sie Tab/Enter – die IDE erzeugt
das Grundgerüst. Danach müssen Sie nur noch die Namen anpassen.
</details>

<details><summary>Tipp 2</summary>

```dart
class MyLogin extends StatefulWidget {
  const MyLogin({super.key});

  @override
  State<MyLogin> createState() => _MyLoginState();
}

class _MyLoginState extends State<MyLogin> {
  @override
  Widget build(BuildContext context) {
    return /* Center mit Text */;
  }
}
```
</details>

<details><summary>Tipp 3 – Fehler „const“?</summary>

Ein `AppBar(...)` in einem `const`-Ausdruck ist erlaubt, solange alles darin auch
`const` sein kann. Meldet die IDE einen Fehler, entfernen Sie das äußere `const` vor
`MaterialApp` und setzen `const` nur vor `Text(...)` und `MyLogin()`.
</details>

> **Merke:** Das Stateful Widget selbst ist unveränderlich – der veränderliche
> Zustand liegt im **State-Objekt**. Der Unterstrich `_` macht die Klasse privat für
> diese Datei.
