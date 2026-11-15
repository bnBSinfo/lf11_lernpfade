import 'package:flutter/material.dart';

import 'todo_item.dart';

// Diese Datei ist fertig – sie zeigt Ihr ToDoItem dreimal an.
class ToDoApp extends StatelessWidget {
  const ToDoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('ToDo-Element (Vorschau)')),
        body: ListView(
          children: const [
            ToDoItem('Einkaufen'),
            ToDoItem('Hausaufgaben LF11'),
            ToDoItem('Sport'),
          ],
        ),
      ),
    );
  }
}
