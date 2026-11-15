import 'package:flutter/material.dart';

// LEVEL 4 – Die Login-Maske
// Auftrag: docs/level_04.md   ·   Prüfen: flutter test test/level_04_test.dart

class MyLogin extends StatefulWidget {
  const MyLogin({super.key});

  @override
  State<MyLogin> createState() => _MyLoginState();
}

class _MyLoginState extends State<MyLogin> {
  // TODO 1: Variablen des State anlegen:
  //   String _username, String _password, bool _canLogin

  // TODO 2: Methode _checkCanLogin() – setzt in setState(...) _canLogin auf
  //   true, wenn Benutzername UND Passwort nicht leer sind, sonst auf false.

  // TODO 3: Zwei Methoden, die den eingegebenen Text in _username bzw.
  //   _password speichern und danach _checkCanLogin() aufrufen.

  @override
  Widget build(BuildContext context) {
    // TODO 4: Bauen Sie die Maske (Center -> SizedBox(width: 300) -> Column):
    //   Text 'Willkommen', TextField 'Benutzername', TextField 'Passwort'
    //   (versteckt!), TextButton 'Login' – nur aktiv, wenn _canLogin true ist.
    return const Center(
      child: Text('Willkommen im Stateful Widget'),
    );
  }
}
