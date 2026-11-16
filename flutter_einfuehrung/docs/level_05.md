# Level 5 – Ein Widget für ein Listenelement

**Ziel:** Sie bauen ein wiederverwendbares Stateless Widget, das ein ToDo darstellt.

**Sie schreiben:** `lib/todo_item.dart` und `lib/todo_app.dart` neu, `lib/main.dart` ändern · **Skript:** Beispiel 2a

## Planung (Skript)
Die fertige App braucht: Liste von ToDos, Checkbox zum Abhaken, Löschbutton,
Button zum Hinzufügen. Wir beginnen mit **einem** Listenelement.

## Auftrag
1. **📄 Neue Datei** `lib/todo_item.dart` mit dem Stateless Widget `ToDoItem` (`stless` + Tab). Den Titel bekommt es
   über den Konstruktor:
   ```diff
   + import 'package:flutter/material.dart';
   +
   + class ToDoItem extends StatelessWidget {
   +   final String title;
   +
   +   const ToDoItem(this.title, {super.key});
   +
   +   @override
   +   Widget build(BuildContext context) {
   +     return Row(
   +       children: [
   +         // hier die drei Widgets, siehe unten
   +       ],
   +     );
   +   }
   + }
   ```
   In die `children` der `Row` kommen:
   - `const Checkbox(value: false, onChanged: null)` – noch inaktiv
   - `Expanded(child: Text(title))`
   - `const IconButton(icon: Icon(Icons.delete), onPressed: null)` – noch inaktiv
2. **📄 Neue Datei** `lib/todo_app.dart` mit dem Stateless Widget `ToDoApp`. Es zeigt zur Vorschau drei Einträge:
   ```diff
   + import 'package:flutter/material.dart';
   + import 'todo_item.dart';
   +
   + class ToDoApp extends StatelessWidget {
   +   const ToDoApp({super.key});
   +
   +   @override
   +   Widget build(BuildContext context) {
   +     return MaterialApp(
   +       home: Scaffold(
   +         appBar: AppBar(title: const Text('ToDo-Element (Vorschau)')),
   +         body: ListView(
   +           children: const [
   +             ToDoItem('Einkaufen'),
   +             ToDoItem('Hausaufgaben LF11'),
   +             ToDoItem('Sport'),
   +           ],
   +         ),
   +       ),
   +     );
   +   }
   + }
   ```
3. **✏️ Ändern** `lib/main.dart` – zwei Zeilen **ersetzen**: Jetzt startet die `ToDoApp`.
   ```diff
     import 'package:flutter/material.dart';
   - import 'my_first_app.dart';
   + import 'todo_app.dart';

     void main() {
   -   runApp(const MyFirstApp());
   +   runApp(const ToDoApp());
     }
   ```
   Die Dateien `my_first_app.dart` und `my_login.dart` **bleiben** im Projekt – nicht löschen, Sie brauchen sie in Level 9 wieder.

## Profi-Auftrag
- `lib/todo_item.dart`: Stateless Widget `ToDoItem`; der Titel kommt als **positionaler** Konstruktor-Parameter.
  Eine Zeile zeigt: Checkbox (inaktiv) · Titel (füllt die Breite) · Mülleimer-Button (inaktiv).
- `lib/todo_app.dart`: `ToDoApp` zeigt zur Vorschau drei `ToDoItem`s (darunter „Einkaufen“) in einer `ListView`,
  AppBar „ToDo-Element (Vorschau)“.
- `main.dart` startet `ToDoApp`. Die Login-Dateien bleiben im Projekt.

*Hängen Sie fest? Schalten Sie oben auf **🧭 Begleitet** um – dort steht jeder Schritt mit Code-Rahmen.*

## Erklärt – was passiert hier?

**Warum ist `ToDoItem` Stateless?** Ein Listeneintrag soll nur **anzeigen**, was man ihm gibt. Die Daten (der Titel) kommen von außen über den Konstruktor:

```dart
final String title;                       // wird einmal übergeben, nie geändert
const ToDoItem(this.title, {super.key});  // ToDoItem('Einkaufen')
```

So kann man dasselbe Widget beliebig oft mit verschiedenen Titeln verwenden – wie eine Schablone. Später in der Liste entsteht aus jedem Eintrag ein `ToDoItem`.

**Der Aufbau der Zeile:**

- `Row` legt ihre `children` **nebeneinander** (Column: untereinander).
- `Checkbox(value: false, onChanged: null)` – `value` ist der Haken, `onChanged: null` macht sie inaktiv (grau). Wer den Haken später ändern darf, kommt in Level 8.
- `Expanded` sagt: „Nimm den ganzen restlichen Platz.“ Ohne `Expanded` stünde der Mülleimer direkt neben dem Text statt ganz rechts.
- `IconButton` ist ein Button mit Symbol. `Icons.delete` ist der Mülleimer aus der Material-Symbolsammlung.

**`const` oder nicht?** `const Checkbox(...)` geht, weil sich nichts darin ändert. `Text(title)` kann nicht `const` sein – `title` ist erst zur Laufzeit bekannt.

<details><summary>Tipp 1 – Wozu Expanded?</summary>

`Expanded` lässt den Text den restlichen Platz einnehmen – so wandert der Mülleimer
ganz nach rechts.
</details>

<details><summary>Tipp 2</summary>

```dart
return Row(
  children: [
    const Checkbox(value: false, onChanged: null),
    Expanded(child: Text(title)),
    /* IconButton */
  ],
);
```
</details>

> **Merke:** `final`-Felder + `const`-Konstruktor: Ein Stateless Widget bekommt seine
> Daten von außen und ändert sie nie selbst.
