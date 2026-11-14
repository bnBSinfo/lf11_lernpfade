# Level 4 – Die Login-Maske

**Ziel:** Ihr State speichert Eingaben, und `setState` sorgt dafür, dass sich die
Oberfläche ändert: Der Login-Button wird erst aktiv, wenn beide Felder gefüllt sind.

**Datei:** `lib/level_04/my_login.dart` · **Skript:** Beispiel 1

## Auftrag
1. Variablen im State: `String _username = '';`, `String _password = '';`,
   `bool _canLogin = false;`
2. Methode `_checkCanLogin()`: setzt **in `setState(() { … })`** `_canLogin` auf
   `true`, wenn beide Strings nicht leer sind (`isNotEmpty`), sonst auf `false`.
3. Zwei Methoden `_onChangedUsername(String username)` und
   `_onChangedPassword(String password)`: Wert speichern, dann `_checkCanLogin()`.
4. `build`: `Center` → `SizedBox(width: 300)` → `Column(mainAxisSize: MainAxisSize.min)`
   mit den `children`:
   - `Text('Willkommen')`
   - `TextField` mit `onChanged: _onChangedUsername` und `labelText: 'Benutzername'`
   - `TextField` mit `onChanged: _onChangedPassword`, `obscureText: true`, `labelText: 'Passwort'`
   - `TextButton` mit `onPressed: _canLogin ? () {} : null` und `child: Text('Login')`

## Erklärt – was passiert hier?

**Die drei Variablen sind der Zustand (State) der Maske:**

| Variable | merkt sich | Startwert |
|---|---|---|
| `_username` | was im ersten Feld steht | `''` (leer) |
| `_password` | was im zweiten Feld steht | `''` |
| `_canLogin` | darf man auf Login drücken? | `false` |

Sie stehen **im State, außerhalb von `build`** – nur so bleiben sie erhalten, wenn `build` neu läuft. Stünden sie in `build`, würden sie bei jedem Neuzeichnen wieder auf `''` gesetzt.

**Was passiert beim Tippen?**

1. Sie tippen ein „a“ in das erste Feld.
2. Das `TextField` ruft seine Funktion `onChanged` auf und übergibt den ganzen Text: `_onChangedUsername('a')`.
3. Die Methode speichert ihn: `_username = 'a'` und ruft `_checkCanLogin()` auf.
4. `_checkCanLogin()` berechnet `_canLogin` neu – **innerhalb von `setState`**.
5. `setState` meldet Flutter: „Daten geändert“. Flutter ruft `build` erneut auf.
6. `build` baut den Button neu: `onPressed: _canLogin ? () {} : null`.

**Der Bedingungsoperator `? :`** – `bedingung ? wennJa : wennNein`. Ist `_canLogin` wahr, bekommt der Button eine (leere) Funktion und ist **aktiv**. Ist es falsch, bekommt er `null` und ist **grau**.

**Funktionen übergeben:** `onChanged: _onChangedUsername` übergibt die Methode **selbst** (ohne Klammern). Das TextField ruft sie später auf. Mit Klammern würde sie sofort beim Bauen ausgeführt.

## Prüfen
`flutter test test/level_04_test.dart` – zwei Tests: Aufbau und Verhalten.

<details><summary>Tipp 1 – Beschriftung und Rahmen</summary>

```dart
decoration: const InputDecoration(
  border: OutlineInputBorder(),
  labelText: 'Passwort',
),
```
</details>

<details><summary>Tipp 2 – Der Button bleibt grau</summary>

Ändern Sie `_canLogin` wirklich **innerhalb** von `setState`? Ohne `setState` wird
`build` nicht erneut ausgeführt – die Variable ändert sich, aber die Oberfläche nicht.
</details>

<details><summary>Tipp 3 – Bedingung</summary>

```dart
_canLogin = _username.isNotEmpty && _password.isNotEmpty;
```
ersetzt das ganze `if … else`.
</details>

> **Merke:** `onChanged` meldet jede Änderung sofort, `onSubmitted` erst nach Enter.
> `onPressed: null` deaktiviert einen Button.

**Experiment:** Nehmen Sie `setState` heraus und starten Sie die App. Was passiert?
