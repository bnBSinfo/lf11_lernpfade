# Level 7 – Löschen: Funktionen als Parameter

**Ziel:** Der Mülleimer ist im `ToDoItem`. Die Liste ist aber in `ToDoList`. Darum gibst du dem `ToDoItem` eine **Funktion**.

**Du änderst:** `lib/todo_list.dart` und `lib/todo_item.dart` · **Skript:** Beispiel 2c

## Auftrag
1. **✏️ Ändern** `lib/todo_list.dart`. Füge die Methode `deleteItem` ein. Sie steht **zwischen** `addItem` und `newEntry`.
   {{code 0}}
2. **✏️ Ändern** `lib/todo_item.dart`. Füge ein Feld hinzu. Ersetze den Konstruktor.
   {{code 1}}
3. **✏️ Ändern** `lib/todo_item.dart`. Der `IconButton` wird aktiv. Lösche das `const` davor. `remove` steht erst beim Start fest.
   {{code 2}}
4. **✏️ Ändern** `lib/todo_list.dart`. Im `itemBuilder` bekommt jedes `ToDoItem` seine Lösch-Funktion.
   {{code 3}}

## Profi-Auftrag
- Der Mülleimer löscht **genau sein** ToDo.
- `ToDoItem` bleibt **Stateless**. Gelöscht wird im State der Liste. Das `ToDoItem` bekommt die Lösch-Funktion als 2. Wert im Konstruktor (`VoidCallback`).

*Kommst du nicht weiter? Schalte oben auf **🧭 Begleitet** um.*

## Erklärt – was passiert hier?

**Das Problem:** Der Mülleimer ist im `ToDoItem`. Die Liste `todos` ist im State von `ToDoList`. Ein Stateless Widget hat kein `setState`. Es kennt die Liste nicht. Es kann nicht selbst löschen.

**Die Lösung:** Die Liste gibt dem Eintrag eine Funktion mit. Wie eine Fernbedienung.

{{code 4}}

{{code 5}}

**Du tippst auf den Mülleimer von „LF11 lernen“. Das ist Platz 1.**

1. `IconButton` ruft `remove()` auf.
2. `remove` ist die Funktion `() => deleteItem(1)`.
3. `deleteItem(1)` löscht in `setState` den Eintrag auf Platz 1.
4. `build` von `ToDoList` läuft neu. Die Liste zeigt nur noch die anderen Einträge.

**`() => deleteItem(i)`** ist eine Funktion ohne Namen. Sie läuft nicht sofort. Sie läuft erst bei `remove()`. Jeder Eintrag hat seine eigene Funktion. Jede Funktion hat ihr eigenes `i`.

**`VoidCallback`** ist eine Funktion ohne Werte und ohne Ergebnis.

> Das Muster heißt **„State nach oben heben“**. Die Daten liegen oben im Eltern-Widget. Die Kinder melden sich über Funktionen.

<details><summary>Tipp 1 – Was ist VoidCallback?</summary>

`VoidCallback` ist eine Funktion ohne Werte und ohne Ergebnis. Im Skript steht `Function`. `VoidCallback` ist genauer. Die IDE findet Fehler dann früher.
</details>

<details><summary>Tipp 2 – Rote Fehler nach Schritt 2</summary>

Du hast den Konstruktor geändert. Jetzt meldet die IDE einen Fehler im `itemBuilder`. Dort fehlt der 2. Wert. Das machst du in Schritt 4.
</details>

> **Merke:** Funktionen, die den State ändern, stehen im Stateful Widget. Das Stateless Widget bekommt nur einen „Knopf“. Damit löst es die Funktion aus.
