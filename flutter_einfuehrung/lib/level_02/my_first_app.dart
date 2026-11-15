import 'package:flutter/material.dart';

// LEVEL 2 – Widget im Widget
// Auftrag: docs/level_02.md   ·   Prüfen: flutter test test/level_02_test.dart

class MyFirstApp extends StatelessWidget {
  const MyFirstApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        // TODO: Verschachteln Sie den body von außen nach innen:
        //   Padding (50 rundherum) -> ColoredBox (grau) -> Center -> Text
        // Der Text lautet: 'hier ist das zentrale Feld der App'
        body: Text('Das ist mein Grundgerüst'),
      ),
    );
  }
}
