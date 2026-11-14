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
