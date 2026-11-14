# Level 5 – Ein Widget für ein Listenelement

**Ziel:** Sie bauen ein wiederverwendbares Stateless Widget, das ein ToDo darstellt.

**Datei:** `lib/level_05/todo_item.dart` · **Skript:** Beispiel 2a ·
Ansehen: `aktivesLevel = 5`

## Planung (Skript)
Die fertige App braucht: Liste von ToDos, Checkbox zum Abhaken, Löschbutton,
Button zum Hinzufügen. Wir beginnen mit **einem** Listenelement.

## Auftrag
`ToDoItem` bekommt seinen Titel über den Konstruktor: `const ToDoItem(this.title)`.
Bauen Sie in `build` eine `Row` mit

1. `Checkbox(value: false, onChanged: null)` – noch inaktiv
2. `Expanded(child: Text(title))`
3. `IconButton(icon: Icon(Icons.delete), onPressed: null)` – noch inaktiv

## Prüfen
`flutter test test/level_05_test.dart`

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
