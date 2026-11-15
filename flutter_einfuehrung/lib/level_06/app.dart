import 'package:flutter/material.dart';

import 'todo_list.dart';

// Diese Datei ist fertig – sie startet Ihre ToDoList.
class ToDoApp extends StatelessWidget {
  const ToDoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: ToDoList());
  }
}
