# Bonus – Die App weiterentwickeln

Arbeiten Sie in `lib/level_08/` weiter (Ihre Tests sollen grün bleiben!).

1. **Doppelte Titel:** Eine Map hat jeden Schlüssel nur einmal. Verhindern Sie
   doppelte Einträge (Hinweis im Dialog) – oder bauen Sie eine Klasse `ToDo` mit
   `title` und `done` und verwenden Sie `List<ToDo>`.
2. **Leere Einträge:** Ein leerer Text soll nicht hinzugefügt werden.
3. **Durchgestrichen:** Abgehakte ToDos werden durchgestrichen und grau
   (`TextStyle(decoration: TextDecoration.lineThrough)`).
4. **Zähler:** Die AppBar zeigt „ToDo Liste (2 offen)“.
5. **Login → Liste:** Der Login-Button aus Level 4 öffnet die ToDo-Liste
   (`Navigator.of(context).push(MaterialPageRoute(builder: …))`).
6. **Lebenszyklus:** Überschreiben Sie in einem State `initState()` und `dispose()`
   und geben Sie mit `debugPrint` aus, wann sie aufgerufen werden.
   Wann wird `build` aufgerufen?
