# Level 2 – Widget im Widget

**Ziel:** Sie verstehen, dass es in Flutter für jede Funktion ein eigenes Widget gibt –
auch für Abstand, Farbe und Ausrichtung.

**Sie ändern:** `lib/my_first_app.dart` · **Skript:** Kapitel 4a

## Auftrag
In HTML/CSS würden Sie `padding`, `background` und `text-align` als Eigenschaften
setzen. In Flutter verpacken Sie stattdessen Widgets ineinander.

Bauen Sie den `body` von außen nach innen:

1. `Padding` mit `padding: EdgeInsets.all(50)`
2. darin eine `ColoredBox` mit `color: Colors.grey`
3. darin ein `Center`
4. darin `Text('hier ist das zentrale Feld der App')`

## Erklärt – was passiert hier?

In HTML/CSS hängen Sie Eigenschaften an ein Element (`padding`, `background`, `text-align`). In Flutter gibt es dafür **eigene Widgets**, die Sie ineinanderstecken. Jedes kann genau eine Sache:

| Widget | kann genau eine Sache | wichtigste Eigenschaft |
|---|---|---|
| `Padding` | Abstand nach innen | `padding: EdgeInsets.all(50)` |
| `ColoredBox` | Fläche einfärben | `color: Colors.grey` |
| `Center` | Kind mittig ausrichten | – |
| `Text` | Text anzeigen | der Text |

**Lesen Sie den Code von außen nach innen:** Das `Padding` bekommt den ganzen `body` und lässt 50 Pixel Rand. In den Rest legt es sein `child`, die `ColoredBox`. Die färbt diese Fläche grau und gibt sie an ihr `child` weiter, das `Center`. Das setzt den `Text` in die Mitte.

**`child` oder `children`?** Widgets mit **einem** Kind haben `child:`, Widgets mit **mehreren** Kindern (z. B. `Column`, `Row`) haben `children: [ … ]` – eine Liste.

**`EdgeInsets`** beschreibt Abstände: `.all(50)` rundherum, `.symmetric(horizontal: 20)` nur links und rechts, `.only(top: 10)` nur oben.

Im **Baukasten** unten können Sie Padding, Farbe, Center und sogar Column und Row live ausprobieren – der passende Code entsteht daneben.

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
