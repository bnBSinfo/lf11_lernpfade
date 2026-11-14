# Level 3 – Das erste Stateful Widget

**Ziel:** Sie legen ein Stateful Widget an, lagern es in eine eigene Datei aus und
binden es in das Stateless Widget ein.

**Dateien:** `lib/level_03/my_first_app.dart`, `lib/level_03/my_login.dart` ·
**Skript:** Kapitel 4b

## Auftrag
1. `my_first_app.dart`: Ergänzen Sie eine `appBar` mit `title: Text('Meine erste App')`.
2. `my_login.dart`: `MyLogin` ist noch ein Stateless Widget. Machen Sie daraus ein
   **Stateful Widget**. Es besteht aus zwei Klassen:
   - `MyLogin extends StatefulWidget` mit `createState()`
   - `_MyLoginState extends State<MyLogin>` mit der `build`-Methode
   Die `build`-Methode zeigt zentriert `'Willkommen im Stateful Widget'`.
3. `my_first_app.dart`: Setzen Sie `body: const MyLogin()` und löschen Sie die
   Platzhalter-Zeilen am Dateiende.

Die Datei `my_login.dart` ist schon in `snake_case` benannt und wird in
`my_first_app.dart` importiert – so lagert man Widgets aus.

## Prüfen
`flutter test test/level_03_test.dart`

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
