import 'package:flutter/material.dart';

// LEVEL 5 – Ein Widget für ein Listenelement
// Auftrag: docs/level_05.md   ·   Prüfen: flutter test test/level_05_test.dart
// Ansehen: in lib/main.dart aktivesLevel = 5 setzen.

class ToDoItem extends StatelessWidget {
  final String title;

  const ToDoItem(this.title, {super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: Ordnen Sie in einer Row nebeneinander an:
    //   - eine Checkbox (value: false, onChanged: null -> noch inaktiv)
    //   - den Titel als Text (Tipp: in Expanded packen)
    //   - einen IconButton mit Icons.delete (onPressed: null -> noch inaktiv)
    return Text(title);
  }
}
