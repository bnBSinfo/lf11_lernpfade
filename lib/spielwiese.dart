// SPIELWIESE – hier dürfen Sie alles ausprobieren!
//
// 1. Auf der Webseite zur Flutter-Einführung im Baukasten "Ganzen Quellcode zeigen" einschalten
//    und auf "Kopieren" klicken.
// 2. Den GESAMTEN Inhalt dieser Datei markieren und durch den kopierten Code ersetzen.
// 3. Starten:
//    - Android Studio: Rechtsklick auf spielwiese.dart → Run 'spielwiese.dart'
//    - VS Code / Terminal: flutter run -t lib/spielwiese.dart
// 4. Code verändern, speichern → Hot Reload zeigt die Änderung sofort.
//
// Diese Datei wird von keinem Test geprüft.

import 'package:flutter/material.dart';

void main() {
  runApp(const MyFirstApp());
}

class MyFirstApp extends StatelessWidget {
  const MyFirstApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        body: Center(
          child: Text('Spielwiese – fügen Sie hier Code aus dem Baukasten ein'),
        ),
      ),
    );
  }
}
