"""Selbstkontrolle in „Sprache einfach“. Gleiche Reihenfolge wie kontrolle.py:
gleiche Haken, gleiche Fragen, gleiche Antworten. Richtig oder falsch steht nur in kontrolle.py."""

KONTROLLE_EINFACH = {
    1: {"check": [
        "Die App startet ohne roten Fehler.",
        "Oben links steht *Das ist mein Grundgerüst*.",
        "In `main.dart` steht nur `main()` mit `runApp(const MyFirstApp())`. Die Klasse steht in `my_first_app.dart`.",
    ], "fragen": [
        ("Was bekommt `runApp()`?", [
            ("Das Start-Widget. Hier: `MyFirstApp()`.", "runApp zeichnet dieses Widget. Es ist die Wurzel vom Widget-Baum."),
            ("Den Namen der Datei. Zum Beispiel `'my_first_app.dart'`.", "Dateien holst du mit import. runApp bekommt ein Widget."),
            ("Die Farbe der App.", "Farben stehen im Theme der MaterialApp."),
        ]),
        ("Welches Widget hat die Bereiche `appBar`, `body` und `floatingActionButton`?", [
            ("`Scaffold`", "Das Scaffold ist das Gerüst für 1 Seite."),
            ("`MaterialApp`", "MaterialApp ist die App. Die Seite steht bei home."),
            ("`Text`", "Text zeigt nur einen Text."),
        ]),
    ]},
    2: {"check": [
        "Ein grauer Kasten füllt den Bildschirm. Rundum sind 50 Pixel Rand.",
        "Der Text steht genau in der Mitte vom grauen Kasten.",
        "Ich kann erklären: `Padding` → `ColoredBox` → `Center` → `Text`.",
    ], "fragen": [
        ("Wie setzt du einen Text in die Mitte?", [
            ("Ich packe ihn in ein `Center`-Widget.", "In Flutter ist die Mitte ein eigenes Widget."),
            ("Mit `Text('…', textAlign: TextAlign.center)`.", "textAlign ordnet nur die Zeilen im Text. Der Text bleibt oben links."),
            ("Mit `Scaffold(center: true)`.", "Das gibt es nicht."),
        ]),
        ("`ColoredBox` ist außen. `Padding` ist innen. Was ändert sich?", [
            ("Der Rand wird auch grau. Der Abstand ist dann in der Farbe.", "Die Reihenfolge bestimmt das Aussehen."),
            ("Nichts. Die Reihenfolge ist egal.", "Probiere es aus. Die Reihenfolge ist wichtig."),
            ("Die App stürzt ab.", "Beides geht. Es sieht nur anders aus."),
        ]),
    ]},
    3: {"check": [
        "Oben ist eine AppBar. Darin steht *Meine erste App*.",
        "In der Mitte steht *Willkommen im Stateful Widget*.",
        "`MyLogin` steht in der Datei `my_login.dart`. Ich hole sie mit `import 'my_login.dart';`.",
    ], "fragen": [
        ("Wo steht bei einem Stateful Widget die Methode `build`?", [
            ("Im State. Also in `_MyLoginState`.", "Nur der State kennt die aktuellen Daten."),
            ("Im Widget `MyLogin`.", "Das Widget hat nur createState()."),
            ("In `createState()`.", "createState baut nur 1-mal den State."),
        ]),
        ("Was macht der `_` in `_MyLoginState`?", [
            ("Nur diese Datei kennt die Klasse. Sie ist privat.", "In Dart ist der _ eine echte Regel."),
            ("Die Klasse ist abstrakt.", "Dafür gibt es das Wort abstract."),
            ("Nichts. So schreibt man das nur.", "In Dart wirkt der _ wirklich."),
        ]),
    ]},
    4: {"check": [
        "Ist ein Feld leer? Dann ist der Login-Button grau.",
        "Sind beide Felder voll? Dann ist Login aktiv. Ist ein Feld wieder leer, wird er wieder grau.",
        "Das Passwort zeigt nur Punkte.",
    ], "fragen": [
        ("Wozu ist `setState(() { … })` da?", [
            ("Es meldet: Daten sind neu. Dann ruft Flutter `build` auf.", "Ohne setState ändert sich die Variable. Aber du siehst es nicht."),
            ("Es speichert die Variable für immer.", "Nach dem Neustart sind die Werte weg. setState speichert nichts."),
            ("Ohne setState kann man nicht ins TextField tippen.", "Tippen geht immer. Nur der Button reagiert nicht."),
        ]),
        ("Was macht `onPressed: null` bei einem Button?", [
            ("Der Button ist grau. Man kann ihn nicht drücken.", "Darum: onPressed: _canLogin ? () {} : null"),
            ("Die App meldet einen Fehler.", "null ist hier erlaubt."),
            ("Der Button verschwindet.", "Er bleibt da. Er ist nur grau."),
        ]),
    ]},
    5: {"check": [
        "Ich sehe 3 Zeilen: *Einkaufen*, *Hausaufgaben LF11*, *Sport*.",
        "Jede Zeile: links Checkbox, dann Titel, ganz rechts Mülleimer.",
        "Checkbox und Mülleimer sind grau. Sie tun noch nichts.",
    ], "fragen": [
        ("Warum steht der Text in `Expanded`?", [
            ("Er nimmt den Rest-Platz. Dann steht der Mülleimer ganz rechts.", "Expanded verteilt den freien Platz."),
            ("Der Text wird größer.", "Die Schrift bleibt gleich groß."),
            ("Ohne Expanded stürzt die App ab.", "Ohne Expanded steht der Mülleimer direkt neben dem Text."),
        ]),
        ("Wie kommt der Titel in ein `ToDoItem`?", [
            ("Über den Konstruktor: `ToDoItem('Einkaufen')`.", "So wird das Widget zur Schablone."),
            ("Mit `setState`.", "ToDoItem ist Stateless. Es hat keinen State."),
            ("Es liest ihn selbst aus einer Liste.", "Die Daten kommen immer von außen."),
        ]),
    ]},
    6: {"check": [
        "Ich tippe auf +. Ein Dialog mit Textfeld geht auf.",
        "Ich drücke Enter. Der Dialog geht zu. Der Eintrag steht in der Liste.",
        "Viele Einträge stehen untereinander. Ich kann die Liste scrollen.",
    ], "fragen": [
        ("Wozu ist `Navigator.of(context).pop()` in `addItem`?", [
            ("Es schließt den Dialog.", "Der Dialog liegt oben wie eine Seite. pop nimmt ihn weg."),
            ("Es löscht den letzten Eintrag.", "Die Liste ändern nur todos.add und remove."),
            ("Es springt zur Startseite.", "pop nimmt nur das Oberste weg. Hier: den Dialog."),
        ]),
        ("Was macht `ListView.builder(itemCount: todos.length, itemBuilder: …)`?", [
            ("Es ruft `itemBuilder` für jeden Index auf. Von 0 bis `length - 1`.", "Jeder Aufruf baut 1 ToDoItem."),
            ("Es kopiert die Liste in das Widget.", "Es baut nur Widgets. Die Daten bleiben im State."),
            ("Es zeigt nur den 1. Eintrag.", "itemCount sagt: So viele Einträge werden gebaut."),
        ]),
    ]},
    7: {"check": [
        "Jeder Mülleimer löscht genau seinen Eintrag.",
        "Nach dem Löschen rücken die anderen Einträge nach oben.",
        "Ich kann weiter neue Einträge anlegen.",
    ], "fragen": [
        ("Warum bekommt `ToDoItem` eine Funktion? Warum löscht es nicht selbst?", [
            ("Die Liste ist im State von `ToDoList`. Nur dort kann man sie ändern.", "Das Kind meldet: Ich soll weg. Die Eltern ändern die Daten."),
            ("Stateless Widgets dürfen keine Buttons haben.", "Buttons gehen überall. Nur ändern kann ein Stateless Widget nichts."),
            ("Funktionen sind schneller.", "Es geht darum, wer zuständig ist. Nicht um Tempo."),
        ]),
        ("Was ist ein `VoidCallback`?", [
            ("Eine Funktion ohne Werte und ohne Ergebnis.", "Zum Beispiel () => deleteItem(i)."),
            ("Eine Variable vom Typ bool.", "Ein VoidCallback ist eine Funktion."),
            ("Ein Widget.", "Ein Widget wird gezeichnet. Eine Funktion wird aufgerufen."),
        ]),
    ]},
    8: {"check": [
        "Ein Haken bleibt. Auch wenn ich neue Einträge anlege.",
        "Löschen und Abhaken treffen den richtigen Eintrag.",
        "Ich habe 2-mal denselben Titel eingegeben. Ich weiß, was passiert.",
    ], "fragen": [
        ("Warum wird aus der `List<String>` eine `Map<String, bool>`?", [
            ("Jeder Titel braucht noch einen Wert: abgehakt oder nicht.", "Schlüssel = Titel. Wert = erledigt."),
            ("Eine Map ist von selbst sortiert.", "Sie ist nicht sortiert. Sie behält die Reihenfolge beim Eintragen."),
            ("Aus einer Liste kann man nichts löschen.", "removeAt geht. Das hast du in Level 7 benutzt."),
        ]),
        ("Was macht `todos.update(key, (bool done) => !done)`?", [
            ("Es dreht den Wert um. Aus `false` wird `true`. Aus `true` wird `false`.", "! heißt: nicht."),
            ("Es fügt einen neuen Eintrag hinzu.", "update ändert nur einen Schlüssel, den es schon gibt."),
            ("Es löscht den Eintrag.", "Löschen geht mit remove."),
        ]),
    ]},
    9: {"check": [
        "Meine App startet mit der Login-Maske.",
        "Nach dem Login sehe ich die ToDo-Liste. Ich kann anlegen, abhaken und löschen.",
        "Der Pfeil zurück führt zur Login-Maske.",
    ], "fragen": [
        ("Was macht `Navigator.of(context).push(...)`?", [
            ("Es legt eine neue Seite oben auf den Stapel.", "Du siehst immer die oberste Seite."),
            ("Es speichert die ToDos in einer Datenbank.", "Nichts wird gespeichert. Die Daten bleiben im State."),
            ("Es schließt die App.", "Eine Seite schließt du mit pop()."),
        ]),
        ("Du gehst zurück und loggst dich neu ein. Warum ist die Liste leer?", [
            ("Die ToDos sind im State der Seite. Beim Zurück ist die Seite mit ihrem State weg.", "Ohne Datenbank sind die Daten nur im Arbeitsspeicher."),
            ("Das Passwort war falsch.", "Die App prüft das Passwort gar nicht."),
            ("setState fehlt.", "setState zeichnet neu. Es speichert nichts."),
        ]),
    ]},
}
