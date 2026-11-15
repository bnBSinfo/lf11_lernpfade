import 'package:flutter/material.dart';

import 'my_login.dart';

// LEVEL 3 – Das erste Stateful Widget
// Auftrag: docs/level_03.md   ·   Prüfen: flutter test test/level_03_test.dart

class MyFirstApp extends StatelessWidget {
  const MyFirstApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        // TODO 1: Fügen Sie eine appBar mit dem Titel 'Meine erste App' hinzu.
        // TODO 3: Ersetzen Sie den body durch Ihr Widget MyLogin().
        body: Center(
          child: Text('Willkommen'),
        ),
      ),
    );
  }
}

// Nur damit der Import oben nicht als unbenutzt gemeldet wird – darf weg,
// sobald Sie MyLogin im body verwenden.
// ignore: unused_element
const _platzhalter = MyLogin;
