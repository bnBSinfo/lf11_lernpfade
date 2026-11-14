# Hinweise für die Lehrkraft

Dieses Repo ist **privat** (Musterlösungen, Tests, Werkzeuge). Die Schüler bekommen nur die Lernpfad-Seite –
über mebis oder https://bnbsinfo.github.io/flutter_lernpfad_schueler/.

## Grundsatz: alles wird getippt
- **Kein Projekt zum Importieren.** In Level 1 legen die Schüler mit `flutter create meine_app` ein eigenes
  Projekt an und bauen diese eine App bis Level 8 aus. Ihre Dateien: `lib/main.dart`, `lib/my_first_app.dart`,
  `lib/my_login.dart` (L3/4), `lib/todo_item.dart`, `lib/todo_app.dart` (L5), `lib/todo_list.dart` (L6–8).
  Ab Level 5 startet `main.dart` die `ToDoApp` – die Login-App bleibt im Projekt (→ Bonus 5).
- Der Auftrag beschreibt, **was** gebaut wird; Code steht in *Erklärt*, in den Tipps und im Baukasten.
- Auf der Seite ist Kopieren von Code gesperrt (nicht markierbar, Kopieren/Rechtsklick abgefangen, Hinweis
  „Bitte abtippen“, kein Kopier-Knopf mehr im Baukasten). Ganz verhindern lässt sich das in keinem Browser.

## Selbstkontrolle statt automatischer Tests
Je Level unter dem Auftrag: Checkliste „Das muss jetzt funktionieren“ (beobachtbar in der eigenen App) und
2 Kontrollfragen mit Feedback; die Falschantworten sind typische Fehler. Erst wenn alles abgehakt und richtig
beantwortet ist, lässt sich „Level geschafft“ setzen. Der Stand wird nur im Browser gespeichert (localStorage).
Inhalte: `tool/kontrolle.py`; Baustein (identisch im REST-Lernpfad): `tool/lernpfad_bausteine.py`.

## Für mebis
`python3 tool/seite_bauen.py` (fragt das Lösungs-Passwort) erzeugt `docs/index.html`: **eine einzige Datei**,
Stylesheet, Schriften und Bilder sind eingebettet (ca. 0,9 MB). In mebis als *Datei* hochladen oder auf die
GitHub-Pages-Adresse verlinken. Vorschau ohne Lösungen: `python3 tool/seite_bauen.py --ohne-loesungen`.

## Aufbau des Repos
| Ordner | Inhalt |
|---|---|
| `docs/level_0X.md`, `docs/bonus.md` | Auftrag, Erklärung, Tipps, Merke, Denkfrage |
| `tool/kontrolle.py` | Checklisten und Kontrollfragen je Level |
| `tool/seite_bauen.py`, `tool/baukasten.js`, `tool/wissen.html` | Seite, Baukasten, Wissen-Seite (braucht pandoc) |
| `loesungen/lib/level_0X/` | Musterlösungen (auf der Seite verschlüsselt, mit Dateinamen wie im Schülerprojekt) |
| `lib/level_0X/`, `test/level_0X_test.dart` | nur noch für Sie: frühere Starter-Fassung und Widget-Tests, mit denen `tool/loesungen_pruefen.sh` die Musterlösungen prüft |
| `tool/bilder_erzeugen.sh` | Zielbilder = Screenshots der Musterlösungen |
| `tool/schueler_repo_aktualisieren.sh` | baut die Seite und überträgt nur `docs/` ins öffentliche Repo |

Die Widget-Tests eignen sich auch zur **Abnahme**: Schülerdateien nach `lib/level_0X/` kopieren
(Dateinamen anpassen) und `flutter test test/level_0X_test.dart` ausführen.

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
2. Lernpfad-Seite in mebis öffnen, Level 1: eigenes Projekt anlegen.
3. Je Level: Skript-Kapitel lesen → Auftrag abtippen → Selbstkontrolle.
4. Stundenende: Screenshot der Startseite (Fortschritt) oder kurze Vorführung der App als Nachweis.

## Prüfen nach Änderungen
```
./tool/loesungen_pruefen.sh     # muss "All tests passed!" zeigen
```

## Schüler-Repo und Webseite
- Privat (dieses Repo, mit Lösungen): https://github.com/bnBSinfo/flutter_lernpfad
- Öffentlich (nur die Seite `docs/`): https://github.com/bnBSinfo/flutter_lernpfad_schueler
- Webseite (GitHub Pages): https://bnbsinfo.github.io/flutter_lernpfad_schueler/

Nach Änderungen: `./tool/schueler_repo_aktualisieren.sh` (fragt das Lösungs-Passwort; `--ohne-loesungen` für eine Seite ohne Lösungen)

## Bilder auf der Webseite
- Zielbilder (`docs/bilder/*.png`) sind echte Screenshots der Musterlösungen.
  Nach Änderungen an den Lösungen neu erzeugen: `./tool/bilder_erzeugen.sh`
- Widget-Bäume und Ablaufgrafiken stehen in `tool/seite_bauen.py` (`LEVEL`, `GRAFIK`).
- Lokal ansehen: `python3 tool/seite_bauen.py` und dann `python3 -m http.server -d docs`.

## Versionsnummer
Steht in `pubspec.yaml` (z. B. `version: 1.6.0+7`) und erscheint auf der Webseite (Kopf und Fußzeile, mit Datum)
Vor dem Veröffentlichen erhöhen:
kleine Korrektur → `1.5.1`, neue Inhalte → `1.6.0`; die Zahl nach `+` jeweils um 1.
So sehen Sie und die Schüler sofort, ob der neueste Stand geladen ist.
