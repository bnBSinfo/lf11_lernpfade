import 'package:flutter/material.dart';

// LEVEL 7 – Löschen
// Auftrag: docs/level_07.md   ·   Prüfen: flutter test test/level_07_test.dart
//
// TODO 2: Ergänzen Sie ein Feld  final VoidCallback remove;
//   und nehmen Sie es in den Konstruktor auf: const ToDoItem(this.title, this.remove, ...)
// TODO 3: Der IconButton ruft beim Drücken remove() auf.

class ToDoItem extends StatelessWidget {
  final String title;

  const ToDoItem(this.title, {super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8),
      child: Row(
        children: [
          const Checkbox(value: false, onChanged: null),
          Expanded(child: Text(title)),
          const IconButton(
            icon: Icon(Icons.delete),
            onPressed: null,
          ),
        ],
      ),
    );
  }
}
