import 'package:flutter/material.dart';

// LEVEL 8 – Abhaken mit Checkbox
// Auftrag: docs/level_08.md   ·   Prüfen: flutter test test/level_08_test.dart
//
// TODO 4: Ergänzen Sie die Felder  final bool done;  und
//   final VoidCallback checkBoxDone;  und nehmen Sie sie in den Konstruktor auf
//   (Reihenfolge: title, done, remove, checkBoxDone).
// TODO 5: Die Checkbox zeigt done an und ruft bei onChanged checkBoxDone() auf.

class ToDoItem extends StatelessWidget {
  final String title;
  final VoidCallback remove;

  const ToDoItem(this.title, this.remove, {super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8),
      child: Row(
        children: [
          const Checkbox(value: false, onChanged: null),
          Expanded(child: Text(title)),
          IconButton(
            icon: const Icon(Icons.delete),
            onPressed: () => remove(),
          ),
        ],
      ),
    );
  }
}
