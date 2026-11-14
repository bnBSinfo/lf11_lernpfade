# Flutter-Lernpfad LF11 – Ihre erste eigene App

Sie programmieren in **8 Leveln** echte Flutter-Apps: vom Grundgerüst über eine
Login-Maske bis zur fertigen ToDo-Liste. Jedes Level hat

- einen **Auftrag** in `docs/level_0X.md` (mit Tipps zum Aufklappen),
- eine **Code-Datei mit `TODO`-Stellen** in `lib/level_0X/`,
- einen **automatischen Test** in `test/level_0X_test.dart`, der Ihnen sagt,
  ob alles stimmt – und wenn nicht, einen **Hinweis** gibt.

Jedes Level startet mit einem funktionierenden Stand des vorherigen Levels.
Wenn Sie in einem Level festhängen, verlieren Sie also nicht den Anschluss.

## So arbeiten Sie

1. Projekt öffnen (Android Studio: *File → Open*, VS Code: *Ordner öffnen*).
2. Einmalig im Terminal: `flutter pub get`
3. Auftrag lesen: `docs/level_01.md`
4. Die `TODO`-Stellen in `lib/level_01/…` bearbeiten.
5. **App ansehen:** In `lib/main.dart` `aktivesLevel` auf die Levelnummer setzen
   und die App starten (Emulator, Chrome oder Desktop). Nach Änderungen: Hot Reload.
6. **Prüfen:** Test ausführen – bei Grün weiter zum nächsten Level.

### Tests ausführen

| Wo | Wie |
|---|---|
| Terminal | `flutter test test/level_01_test.dart` |
| Android Studio | Rechtsklick auf die Testdatei → *Run 'tests in level_01_test'* |
| VS Code | Seitenleiste *Testing* (Reagenzglas) → Test starten, oder ▶ über `main()` |

### Wo stehe ich?

```
dart run tool/fortschritt.dart
```

zeigt alle Level mit ✅ / ⬜, das nächste Level und den ersten Hinweis.

## Die Level

| Level | Thema | Skript-Kapitel |
|---|---|---|
| 1 | Das Grundgerüst: MaterialApp und Scaffold | 3, 4a |
| 2 | Widget im Widget: Padding, ColoredBox, Center | 4a |
| 3 | Das erste Stateful Widget, eigene Datei | 4b |
| 4 | Die Login-Maske mit setState | Beispiel 1 |
| 5 | Ein Widget für ein ToDo-Listenelement | Beispiel 2a |
| 6 | Die ToDo-Liste mit Dialog | Beispiel 2b |
| 7 | Löschen – Funktionen als Parameter | Beispiel 2c |
| 8 | Abhaken – von der List zur Map | Beispiel 2d |
| ★ | Bonus-Aufgaben | `docs/bonus.md` |

## Spielregeln

- Erst selbst probieren, dann Tipp 1 aufklappen, dann Tipp 2 …
- Die Tests nicht verändern – sie sind Ihr Prüfer.
- Rot ist normal! Lesen Sie den **Hinweis** in der Testausgabe.
