# Level 2 – Widget im Widget

**Ziel:** In Flutter hat jede Aufgabe ein eigenes Widget. Auch Abstand, Farbe und Mitte.

**Du änderst:** `lib/my_first_app.dart` · **Skript:** Kapitel 4a

## Auftrag
In HTML gibst du einem Element Eigenschaften. In Flutter steckst du Widgets ineinander.

**✏️ Ändern** `lib/my_first_app.dart`. Du ersetzt nur die Zeile mit `body:`. Alles andere bleibt.

{{code 0}}

Baue den neuen `body` von außen nach innen. Jedes Widget kommt mit `child:` in das Widget davor.

1. `Padding` mit `padding: EdgeInsets.all(50)`
2. Darin: `ColoredBox` mit `color: Colors.grey`
3. Darin: `Center`
4. Darin: `Text('hier ist das zentrale Feld der App')`

Lösche am Ende den Kommentar `// hier hinein …`.

## Profi-Auftrag
- Der body zeigt „hier ist das zentrale Feld der App“.
- Der Text steht in der **Mitte**. Die Fläche ist **grau**.
- Rundum sind **50 Pixel** Abstand zum Rand.
- Nimm nur Widgets mit 1 Aufgabe. Nimm keinen `Container`.

*Kommst du nicht weiter? Schalte oben auf **🧭 Begleitet** um.*

## Erklärt – was passiert hier?

Jedes Widget kann genau 1 Sache:

| Widget | kann 1 Sache | wichtig |
|---|---|---|
| `Padding` | Abstand nach innen | `padding: EdgeInsets.all(50)` |
| `ColoredBox` | Fläche färben | `color: Colors.grey` |
| `Center` | Kind in die Mitte setzen | – |
| `Text` | Text zeigen | der Text |

**Lies den Code von außen nach innen:**

1. `Padding` lässt 50 Pixel Rand.
2. In den Rest kommt die `ColoredBox`. Sie färbt die Fläche grau.
3. In die Fläche kommt `Center`.
4. `Center` setzt den `Text` in die Mitte.

**`child` oder `children`?** 1 Kind: `child:`. Mehrere Kinder: `children: [ … ]`. Das ist eine Liste. Beispiele: `Column` und `Row`.

**`EdgeInsets`** ist der Abstand. `.all(50)`: rundum. `.symmetric(horizontal: 20)`: links und rechts. `.only(top: 10)`: nur oben.

Im **Baukasten** unten kannst du alles ausprobieren. Der Code steht daneben.

<details><summary>Tipp 1</summary>

Das innere Widget kommt immer in `child` vom äußeren Widget.
</details>

<details><summary>Tipp 2</summary>

{{code 1}}
</details>

> **Merke:** Das innere Widget steht bei `child`. So entsteht ein Baum aus Widgets. Er heißt **Widget-Tree**.

**Aufgabe auf Papier:** Zeichne den Widget-Tree. Von `MyFirstApp` bis zum `Text`.

**Experiment:** Tausche `Padding` und `ColoredBox`. Was ändert sich? Warum?
