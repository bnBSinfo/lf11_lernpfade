# Hinweise für die Lehrkraft

**Nicht an die Schüler weitergeben** – zusammen mit `loesungen/` und
`tool/*.sh`. Die Schülerversion erzeugt `tool/schuelerversion_erstellen.sh`.

## Aufbau
| Ordner | Inhalt |
|---|---|
| `lib/level_0X/` | Starter-Code mit `TODO`s (Stand = Lösung des Vorlevels) |
| `test/level_0X_test.dart` | Widget-Tests mit deutschen `Hinweis:`-Meldungen |
| `docs/level_0X.md` | Auftrag, gestufte Tipps, Merke, Denkfrage |
| `loesungen/lib/` | Musterlösungen, gleiche Struktur wie `lib/` |
| `tool/fortschritt.dart` | Fortschrittsanzeige für Schüler |
| `tool/loesungen_pruefen.sh` | prüft, ob alle Lösungen die Tests bestehen |
| `tool/schuelerversion_erstellen.sh` | ZIP ohne Lösungen für die Schüler |
| `tool/schueler_repo_aktualisieren.sh` | baut die Webseite und überträgt alles ohne Lösungen ins öffentliche Schüler-Repo |
| `tool/seite_bauen.py` | erzeugt `docs/index.html` aus den Level-Anleitungen (braucht pandoc) |

Die Tests prüfen Verhalten und Aufbau, nicht den exakten Code: z. B. sind beim
Login `onChanged` **und** `onSubmitted` erlaubt, beim Button `TextButton`,
`ElevatedButton` oder `FilledButton`, beim Mülleimer mehrere Delete-Icons.

## Änderungen gegenüber dem Skript (03_AP_LF11_BN_STO_Flutter)
Der Code wurde auf aktuelles Flutter (3.x, Null-Safety, `flutter_lints`) gebracht.
Vorschläge für die Überarbeitung des Skripts:

- `const`-Konstruktoren mit `{super.key}` und `@override` vor `build`/`createState`
  fehlen im Skript – der Linter meldet das sonst.
- `createState` gibt `State<MyLogin>` zurück (Skript: `_MyLoginState`, ohne `@override`).
- Funktionsparameter als `VoidCallback` statt `Function` (typsicher).
- Beispiel 2b: Liste heißt einmal `products`, sonst `todos`.
- Kürzel heißt `stful` (Skript an einer Stelle `stfull`); „Statefull“ → „Stateful“.
- Passwortfeld: `onSubmitted` erfordert Enter – für Schüler verwirrend, daher
  in der Musterlösung `onChanged`.
- Map mit Titel als Schlüssel: doppelte Titel überschreiben sich (→ Bonus 1).
- Kapitel 5 „State – Was bin ich?“ ist im Skript noch leer (→ Bonus 6 als Einstieg).
- Merke-Kästen und Codeblöcke sind im .docx teils doppelt vorhanden.

## Ablauf-Vorschlag
1. Installation nach `02_AP_LF11_BN_STO_Installationsanleitung`.
2. Schüler erhalten das ZIP (oder klonen das Repo ohne Lösungen).
3. Je Level: Skript-Kapitel lesen → Auftrag → Test grün.
4. Stundenende: `dart run tool/fortschritt.dart` – Ausgabe als Nachweis/Screenshot.

## Prüfen nach Änderungen
```
./tool/loesungen_pruefen.sh     # muss "All tests passed!" zeigen
flutter test                    # mit Starter-Code: alle Tests rot
```

## Schüler-Repo und Webseite
- Privat (dieses Repo, mit Lösungen): https://github.com/bnBSinfo/flutter_lernpfad
- Öffentlich für Schüler (ohne Lösungen): https://github.com/bnBSinfo/flutter_lernpfad_schueler
- Webseite (GitHub Pages): https://bnbsinfo.github.io/flutter_lernpfad_schueler/

Nach Änderungen an Anleitungen oder Starter-Code: `./tool/schueler_repo_aktualisieren.sh`

## Bilder auf der Webseite
- Zielbilder (`docs/bilder/*.png`) sind echte Screenshots der Musterlösungen.
  Nach Änderungen an den Lösungen neu erzeugen: `./tool/bilder_erzeugen.sh`
- Widget-Bäume und Ablaufgrafiken stehen in `tool/seite_bauen.py` (`LEVEL`, `GRAFIK`).
- Lokal ansehen: `python3 tool/seite_bauen.py` und dann `python3 -m http.server -d docs`.

## Versionsnummer
Steht in `pubspec.yaml` (`version: 1.5.0+6`) und erscheint auf der Webseite (Kopf und Fußzeile, mit Datum)
und in `dart run tool/fortschritt.dart`. Vor dem Veröffentlichen erhöhen:
kleine Korrektur → `1.5.1`, neue Inhalte → `1.6.0`; die Zahl nach `+` jeweils um 1.
So sehen Sie und die Schüler sofort, ob der neueste Stand geladen ist.
