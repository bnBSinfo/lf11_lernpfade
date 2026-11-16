# Level 3 – Das erste Stateful Widget

**Ziel:** Du baust ein Stateful Widget. Es bekommt eine eigene Datei. Du zeigst es in deiner App.

**Du änderst:** `lib/my_first_app.dart` · **Du schreibst neu:** `lib/my_login.dart` · **Skript:** Kapitel 4b

## Auftrag
1. **✏️ Ändern** `lib/my_first_app.dart`. Füge eine `appBar` hinzu. `AppBar` darf nicht in `const` stehen. Lösche darum das `const` vor `MaterialApp`. Schreibe `const` vor `Text`.
   {{code 0}}
2. **📄 Neue Datei** `lib/my_login.dart`. Darin steht das **Stateful Widget** `MyLogin`. Es hat **2 Klassen**.
   Tipp: Tippe `stful` und drücke Tab. Dann stehen beide Klassen da.
   {{code 1}}
3. **✏️ Ändern** `lib/my_first_app.dart`. Hole die neue Datei mit `import`. Lösche den ganzen `body` aus Level 2. Schreibe dafür `MyLogin` hin.
   {{code 2}}

Dateinamen schreibst du klein mit `_`: `my_login.dart`. Klassennamen schreibst du mit Großbuchstaben: `MyLogin`.

## Profi-Auftrag
- Die App bekommt eine AppBar. Der Titel ist „Meine erste App“.
- Neue Datei `lib/my_login.dart`. Darin: **Stateful Widget** `MyLogin`. Es zeigt in der Mitte „Willkommen im Stateful Widget“.
- `MyFirstApp` zeigt `MyLogin` im body.

*Kommst du nicht weiter? Schalte oben auf **🧭 Begleitet** um.*

## Erklärt – was passiert hier?

**Warum 2 Klassen?** Ein Widget kann sich nicht ändern. Manche Daten ändern sich aber. Zum Beispiel ein Text oder ein Haken. Diese Daten brauchen einen eigenen Platz. Dieser Platz heißt **State**.

{{code 3}}

1. **Das Widget** hat nur 1 Aufgabe: `createState()`.
2. `=>` ist eine kurze Schreibweise. Lang heißt es: `{ return _MyLoginState(); }`.
3. **Der State** gehört fest zu seinem Widget. Das zeigt `State<MyLogin>`.
4. Der `_` vor dem Namen macht die Klasse privat. Nur diese Datei kennt sie.
5. **`build` steht im State.** Nur der State kennt die aktuellen Daten.

Noch hat der State keine Daten. Die kommen in Level 4. Mehr dazu: **📘 Wissen** oben in der Leiste.

**Warum eine eigene Datei?** Große Apps haben viel Code. Eine Datei wird dann unübersichtlich. Darum bekommt jedes große Widget eine eigene Datei. Du holst sie mit `import 'my_login.dart';`.

**AppBar:** Die AppBar ist die Leiste oben. Der `body` steht jetzt **unter** der AppBar.

<details><summary>Tipp 1</summary>

Tippe in einer leeren Zeile `stful`. Drücke Tab oder Enter. Die IDE schreibt den Rahmen. Du änderst nur die Namen.
</details>

<details><summary>Tipp 2</summary>

{{code 4}}
</details>

<details><summary>Tipp 3 – Fehler mit „const“?</summary>

Lösche das `const` vor `MaterialApp`. Schreibe `const` nur vor `Text(...)` und vor `MyLogin()`.
</details>

> **Merke:** Das Stateful Widget ändert sich nicht. Die Daten, die sich ändern, liegen im **State**. Der `_` macht eine Klasse privat.
