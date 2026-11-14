"""Selbstkontrolle je Level: Checkliste und Kontrollfragen (Falschantworten = typische Fehler)."""

KONTROLLE = {
    1: {"check": [
        "Die App startet im Emulator oder Browser ohne rote Fehlermeldung.",
        "Oben links steht *Das ist mein Grundgerüst*.",
        "`main.dart` enthält nur `main()` mit `runApp(const MyFirstApp())` – die Klasse steht in `my_first_app.dart`.",
    ], "fragen": [
        ("Was übergeben Sie an `runApp()`?", [
            ("Das Start-Widget der App, hier `MyFirstApp()`.", True, "runApp zeichnet dieses Widget als Wurzel des Widget-Baums."),
            ("Den Namen der Datei, z. B. `'my_first_app.dart'`.", False, "Dateien werden mit import eingebunden – runApp bekommt ein Widget."),
            ("Die Farbe der App.", False, "Farben gehören in das Theme der MaterialApp."),
        ]),
        ("Welches Widget stellt die Bereiche `appBar`, `body` und `floatingActionButton` bereit?", [
            ("`Scaffold`", True, "Das Scaffold ist das Gerüst einer Seite."),
            ("`MaterialApp`", False, "MaterialApp ist die App selbst (Design, Navigation) – die Seite steht bei home."),
            ("`Text`", False, "Text zeigt nur eine Zeichenkette."),
        ]),
    ]},
    2: {"check": [
        "Ein grauer Kasten mit 50 Pixel Rand füllt den Bildschirm.",
        "Der Text steht genau in der Mitte des grauen Kastens.",
        "Ich kann die Verschachtelung `Padding` → `ColoredBox` → `Center` → `Text` erklären.",
    ], "fragen": [
        ("Wie zentrieren Sie in Flutter einen Text auf dem Bildschirm?", [
            ("Ich packe ihn in ein `Center`-Widget.", True, "Ausrichtung ist in Flutter ein eigenes Widget."),
            ("Mit `Text('…', textAlign: TextAlign.center)`.", False,
             "textAlign richtet nur die Zeilen innerhalb des Textes aus – der Text selbst bleibt oben links."),
            ("Mit `Scaffold(center: true)`.", False, "Diese Eigenschaft gibt es nicht."),
        ]),
        ("Was ändert sich, wenn `ColoredBox` außen und `Padding` innen steht?", [
            ("Der Rand wird auch grau – der Abstand liegt dann innerhalb der Farbe.", True,
             "Die Reihenfolge der Verschachtelung bestimmt das Aussehen."),
            ("Nichts – die Reihenfolge ist egal.", False, "Probieren Sie es aus: Die Reihenfolge macht den Unterschied."),
            ("Die App stürzt ab.", False, "Beide Varianten sind gültig, sie sehen nur anders aus."),
        ]),
    ]},
    3: {"check": [
        "Oben ist eine AppBar mit *Meine erste App*.",
        "In der Mitte steht *Willkommen im Stateful Widget*.",
        "`MyLogin` steht in der eigenen Datei `my_login.dart` und wird mit `import 'my_login.dart';` eingebunden.",
    ], "fragen": [
        ("Wo steht bei einem Stateful Widget die `build`-Methode?", [
            ("Im State, also in `_MyLoginState`.", True, "Nur der State kennt die aktuellen Daten."),
            ("Im Widget `MyLogin`.", False, "Das Widget hat nur createState()."),
            ("In `createState()`.", False, "createState erzeugt nur einmal das State-Objekt."),
        ]),
        ("Was bewirkt der Unterstrich in `_MyLoginState`?", [
            ("Die Klasse ist nur in dieser Datei sichtbar (privat).", True, "In Dart ist _ eine echte Regel, keine Schreibweise."),
            ("Die Klasse ist abstrakt.", False, "Abstrakt wird eine Klasse mit abstract."),
            ("Nichts, das ist nur eine Namenskonvention.", False, "In Dart wirkt der Unterstrich tatsächlich."),
        ]),
    ]},
    4: {"check": [
        "Der Login-Button ist grau, solange ein Feld leer ist.",
        "Sind beide Felder gefüllt, wird Login aktiv. Leere ich ein Feld wieder, wird er wieder grau.",
        "Das Passwort erscheint als Punkte.",
    ], "fragen": [
        ("Wozu dient `setState(() { … })`?", [
            ("Es meldet eine Änderung, damit Flutter `build` neu aufruft.", True, "Ohne setState ändert sich die Variable, aber nicht die Anzeige."),
            ("Es speichert die Variable dauerhaft.", False, "Nach einem Neustart sind die Werte weg – setState speichert nichts."),
            ("Ohne setState nimmt das TextField keine Eingaben an.", False, "Tippen geht immer – nur der Button reagiert nicht."),
        ]),
        ("Was bewirkt `onPressed: null` bei einem Button?", [
            ("Der Button ist inaktiv und grau.", True, "Deshalb: onPressed: _canLogin ? () {} : null"),
            ("Die App meldet einen Fehler.", False, "null ist hier ausdrücklich erlaubt."),
            ("Der Button wird ausgeblendet.", False, "Er bleibt sichtbar, nur grau."),
        ]),
    ]},
    5: {"check": [
        "Drei Zeilen: *Einkaufen*, *Hausaufgaben LF11*, *Sport*.",
        "Jede Zeile: Checkbox links, Titel, Mülleimer ganz rechts.",
        "Checkbox und Mülleimer sind grau – noch ohne Funktion.",
    ], "fragen": [
        ("Warum steht der Text in einem `Expanded`?", [
            ("Er nimmt den restlichen Platz ein, dadurch steht der Mülleimer ganz rechts.", True, "Expanded verteilt den freien Platz in Row und Column."),
            ("Der Text wird größer geschrieben.", False, "Die Schriftgröße bleibt gleich."),
            ("Ohne Expanded stürzt die App immer ab.", False, "Ohne Expanded steht der Mülleimer einfach direkt neben dem Text."),
        ]),
        ("Wie kommt der Titel in ein `ToDoItem`?", [
            ("Über den Konstruktor: `ToDoItem('Einkaufen')`.", True, "So wird ein Widget zur wiederverwendbaren Schablone."),
            ("Mit `setState`.", False, "ToDoItem ist Stateless – es hat gar keinen State."),
            ("Es liest ihn selbst aus einer globalen Liste.", False, "Die Daten kommen immer von außen hinein."),
        ]),
    ]},
    6: {"check": [
        "Tippen auf + öffnet einen Dialog mit Textfeld.",
        "Nach Enter schließt sich der Dialog, und der Eintrag steht in der Liste.",
        "Mehrere Einträge stehen untereinander; bei vielen Einträgen lässt sich die Liste scrollen.",
    ], "fragen": [
        ("Wozu dient `Navigator.of(context).pop()` in `addItem`?", [
            ("Es schließt den Dialog.", True, "Der Dialog liegt wie eine Seite oben auf – pop nimmt ihn weg."),
            ("Es löscht den letzten Eintrag der Liste.", False, "Die Liste ändert nur todos.add bzw. remove."),
            ("Es springt zur Startseite der App.", False, "pop entfernt nur das oberste Element – hier den Dialog."),
        ]),
        ("Was macht `ListView.builder(itemCount: todos.length, itemBuilder: …)`?", [
            ("Es ruft `itemBuilder` für jeden Index von 0 bis `length - 1` auf.", True, "Jeder Aufruf baut ein ToDoItem."),
            ("Es kopiert die Liste in das Widget.", False, "Es baut nur Widgets, die Daten bleiben im State."),
            ("Es zeigt immer nur den ersten Eintrag.", False, "itemCount sagt, wie viele Einträge gebaut werden."),
        ]),
    ]},
    7: {"check": [
        "Jeder Mülleimer löscht genau seinen eigenen Eintrag.",
        "Nach dem Löschen rutschen die übrigen Einträge nach.",
        "Neue Einträge lassen sich weiter hinzufügen.",
    ], "fragen": [
        ("Warum bekommt `ToDoItem` eine Funktion, statt selbst zu löschen?", [
            ("Die Liste liegt im State von `ToDoList` – nur dort kann sie geändert werden.", True,
             "Das Kind meldet „Ich soll weg“, die Eltern ändern die Daten."),
            ("Stateless Widgets dürfen keine Buttons enthalten.", False, "Buttons gehen überall – nur ändern kann ein Stateless Widget nichts."),
            ("Funktionen als Parameter sind schneller.", False, "Es geht um die Zuständigkeit, nicht um Tempo."),
        ]),
        ("Was ist ein `VoidCallback`?", [
            ("Eine Funktion ohne Parameter und ohne Rückgabewert.", True, "Zum Beispiel () => deleteItem(i)."),
            ("Eine Variable vom Typ bool.", False, "Ein VoidCallback ist eine Funktion."),
            ("Ein Widget.", False, "Ein Widget wird gezeichnet – ein Callback wird aufgerufen."),
        ]),
    ]},
    8: {"check": [
        "Ein Haken bleibt gesetzt, auch wenn ich weitere Einträge hinzufüge.",
        "Löschen und Abhaken betreffen jeweils den richtigen Eintrag.",
        "Ich habe ausprobiert, was passiert, wenn ich zweimal denselben Titel eingebe.",
    ], "fragen": [
        ("Warum wird aus der `List<String>` eine `Map<String, bool>`?", [
            ("Zu jedem Titel muss zusätzlich gespeichert werden, ob er abgehakt ist.", True, "Schlüssel = Titel, Wert = erledigt."),
            ("Eine Map ist automatisch sortiert.", False, "Sortiert ist sie nicht – sie behält die Einfügereihenfolge."),
            ("Aus einer Liste kann man nichts löschen.", False, "removeAt geht – das haben Sie in Level 7 benutzt."),
        ]),
        ("Was macht `todos.update(key, (bool done) => !done)`?", [
            ("Es kehrt den Wert um: aus `false` wird `true` und umgekehrt.", True, "! ist das logische Nicht."),
            ("Es fügt einen neuen Eintrag hinzu.", False, "update ändert nur einen vorhandenen Schlüssel."),
            ("Es löscht den Eintrag.", False, "Löschen geht mit remove."),
        ]),
    ]},
}
