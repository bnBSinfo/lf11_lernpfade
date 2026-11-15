# Bonus – Die App weiterentwickeln

Arbeiten Sie in Ihrem Projekt `meine_app` weiter – alles aus Level 1–9 soll danach weiter funktionieren.

1. **Doppelte Titel:** Eine Map hat jeden Schlüssel nur einmal. Verhindern Sie
   doppelte Einträge (Hinweis im Dialog) – oder bauen Sie eine Klasse `ToDo` mit
   `title` und `done` und verwenden Sie `List<ToDo>`.
2. **Leere Einträge:** Ein leerer Text soll nicht hinzugefügt werden.
3. **Durchgestrichen:** Abgehakte ToDos werden durchgestrichen und grau
   (`TextStyle(decoration: TextDecoration.lineThrough)`).
4. **Zähler:** Die AppBar zeigt „ToDo Liste (2 offen)“.
5. **Abmelden-Knopf:** Ein `IconButton(icon: const Icon(Icons.logout), …)` in den `actions` der AppBar
   führt mit `Navigator.of(context).pop()` zurück zur Login-Maske.
6. **Lebenszyklus:** Überschreiben Sie in einem State `initState()` und `dispose()`
   und geben Sie mit `debugPrint` aus, wann sie aufgerufen werden.
   Wann wird `build` aufgerufen?
