# Level 5 – Ein Widget für ein Listenelement

**Ziel:** Sie bauen ein wiederverwendbares Stateless Widget, das ein ToDo darstellt.

**Sie schreiben:** `lib/todo_item.dart` und `lib/todo_app.dart` neu, `lib/main.dart` ändern · **Skript:** Beispiel 2a

## Planung (Skript)
Die fertige App braucht: Liste von ToDos, Checkbox zum Abhaken, Löschbutton,
Button zum Hinzufügen. Wir beginnen mit **einem** Listenelement.

## Auftrag
1. Legen Sie `lib/todo_item.dart` an mit dem Stateless Widget `ToDoItem`. Es bekommt seinen Titel über den
   Konstruktor: Feld `final String title;`, Konstruktor `const ToDoItem(this.title, {super.key});`.
   Bauen Sie in `build` eine `Row` mit
   - `Checkbox(value: false, onChanged: null)` – noch inaktiv
   - `Expanded(child: Text(title))`
   - `IconButton(icon: Icon(Icons.delete), onPressed: null)` – noch inaktiv
2. Legen Sie `lib/todo_app.dart` an mit dem Stateless Widget `ToDoApp`, das zur Vorschau drei Einträge zeigt:
   `MaterialApp` → `home: Scaffold` mit `appBar: AppBar(title: Text('ToDo-Element (Vorschau)'))` und
   `body: ListView(children: [ToDoItem('Einkaufen'), ToDoItem('Hausaufgaben LF11'), ToDoItem('Sport')])`.
3. `lib/main.dart`: Starten Sie jetzt `ToDoApp()` statt `MyFirstApp()` (Import nicht vergessen).
   Ihre Login-App bleibt im Projekt – Sie können jederzeit zurückschalten.

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
