# Level 2 – Widget im Widget

**Ziel:** Sie verstehen, dass es in Flutter für jede Funktion ein eigenes Widget gibt –
auch für Abstand, Farbe und Ausrichtung.

**Datei:** `lib/level_02/my_first_app.dart` · **Skript:** Kapitel 4a

## Auftrag
In HTML/CSS würden Sie `padding`, `background` und `text-align` als Eigenschaften
setzen. In Flutter verpacken Sie stattdessen Widgets ineinander.

Bauen Sie den `body` von außen nach innen:

1. `Padding` mit `padding: EdgeInsets.all(50)`
2. darin eine `ColoredBox` mit `color: Colors.grey`
3. darin ein `Center`
4. darin `Text('hier ist das zentrale Feld der App')`

## Prüfen
`flutter test test/level_02_test.dart`

<details><summary>Tipp 1</summary>

Das innere Widget wird immer der Eigenschaft `child` des äußeren zugewiesen.
</details>

<details><summary>Tipp 2</summary>

```dart
body: Padding(
  padding: EdgeInsets.all(50),
  child: ColoredBox(
    color: Colors.grey,
    child: /* Center mit Text */,
  ),
),
```
</details>

> **Merke:** Bei der Verschachtelung wird das untergeordnete Widget der Eigenschaft
> `child` des übergeordneten zugewiesen. So entsteht der **Widget-Tree**.

**Aufgabe auf Papier:** Zeichnen Sie den Widget-Tree von `MyFirstApp` bis zum `Text`.

**Experiment:** Tauschen Sie `Padding` und `ColoredBox`. Was ändert sich – und warum?
