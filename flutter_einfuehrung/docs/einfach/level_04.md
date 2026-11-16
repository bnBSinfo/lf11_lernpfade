# Level 4 – Die Login-Maske

**Ziel:** Dein State merkt sich Eingaben. `setState` zeichnet die Oberfläche neu. Der Login-Button wird erst aktiv, wenn beide Felder voll sind.

**Du änderst:** `lib/my_login.dart` · **Skript:** Beispiel 1

## Auftrag
Du arbeitest nur in `lib/my_login.dart`. Du arbeitest nur in der **2. Klasse**: `_MyLoginState`. Die 1. Klasse `MyLogin` bleibt gleich.

**✏️ Ändern** `lib/my_login.dart`. So sieht der Rahmen aus:

{{code 0}}

Fülle jetzt die Stellen mit den Kommentaren. Lösche danach die Kommentare.

1. Die 3 Variablen stehen oben im State. Sie sind das Gedächtnis der Login-Maske.
2. `_checkCanLogin()`: Schreibe `setState(() { … })`. Darin setzt du `_canLogin`. Sind beide Texte nicht leer? Dann `true`. Sonst `false`. Tipp: `isNotEmpty`.
3. `_onChangedUsername`: Speichere den Wert in `_username`. Rufe dann `_checkCanLogin()` auf. `_onChangedPassword` geht genauso mit `_password`.
4. In `children` der `Column` kommen 4 Widgets untereinander:
   - `Text('Willkommen')`
   - `TextField` mit `onChanged: _onChangedUsername` und `labelText: 'Benutzername'`
   - `TextField` mit `onChanged: _onChangedPassword`, `obscureText: true` und `labelText: 'Passwort'`
   - `TextButton` mit `onPressed: _canLogin ? () {} : null` und `child: Text('Login')`

## Profi-Auftrag
`MyLogin` wird zur Login-Maske:

- In der Mitte, höchstens 300 Pixel breit.
- Oben steht „Willkommen“. Dann 2 Textfelder: „Benutzername“ und „Passwort“. Das Passwort ist verdeckt. Unten steht der Button „Login“.
- Der Button ist **nur aktiv, wenn beide Felder voll sind**. Ist ein Feld wieder leer, wird er grau.
- Die Daten liegen im State. Die Oberfläche ändert sich mit `setState`.
- Der Button macht noch nichts.

*Kommst du nicht weiter? Schalte oben auf **🧭 Begleitet** um.*

## Erklärt – was passiert hier?

**Die 3 Variablen sind der State der Maske:**

| Variable | merkt sich | Start |
|---|---|---|
| `_username` | Text im 1. Feld | `''` (leer) |
| `_password` | Text im 2. Feld | `''` (leer) |
| `_canLogin` | Darf man Login drücken? | `false` |

Die Variablen stehen **im State**. Sie stehen **nicht in `build`**. `build` läuft oft neu. In `build` wären sie jedes Mal wieder leer.

**Was passiert beim Tippen?**

1. Du tippst „a“ in das 1. Feld.
2. Das `TextField` ruft `onChanged` auf: `_onChangedUsername('a')`.
3. Die Methode speichert: `_username = 'a'`.
4. Dann ruft sie `_checkCanLogin()` auf.
5. `_checkCanLogin()` rechnet `_canLogin` neu. Das passiert in `setState`.
6. `setState` sagt Flutter: Daten sind neu. Flutter ruft `build` auf.
7. `build` baut den Button neu.

**`? :` ist eine kurze Frage.** So geht es: `bedingung ? wennJa : wennNein`. Ist `_canLogin` wahr? Dann bekommt der Button eine Funktion. Er ist **aktiv**. Ist `_canLogin` falsch? Dann bekommt er `null`. Er ist **grau**.

**Funktion übergeben:** `onChanged: _onChangedUsername` hat keine Klammern. So gibst du die Funktion weiter. Das TextField ruft sie später auf. Mit Klammern läuft sie sofort.

<details><summary>Tipp 1 – Beschriftung und Rahmen</summary>

{{code 1}}
</details>

<details><summary>Tipp 2 – Der Button bleibt grau</summary>

Steht `_canLogin = …` wirklich **in** `setState`? Ohne `setState` läuft `build` nicht neu. Dann ändert sich die Variable. Aber du siehst es nicht.
</details>

<details><summary>Tipp 3 – Bedingung</summary>

{{code 2}}

Diese 1 Zeile ersetzt das ganze `if … else`.
</details>

> **Merke:** `onChanged` meldet jede Änderung sofort. `onSubmitted` meldet erst nach Enter. `onPressed: null` macht einen Button grau.

**Experiment:** Nimm `setState` heraus. Starte die App. Was passiert?
