import 'package:flutter/material.dart';

import 'todo_item.dart';

// LEVEL 6 – Die ToDo-Liste
// Auftrag: docs/level_06.md   ·   Prüfen: flutter test test/level_06_test.dart

class ToDoList extends StatefulWidget {
  const ToDoList({super.key});

  @override
  State<ToDoList> createState() => _ToDoListState();
}

class _ToDoListState extends State<ToDoList> {
  // TODO 1: Liste für die ToDos anlegen: List<String> todos = [];

  // TODO 2: Methode addItem(String item): fügt in setState das item der Liste
  //   hinzu und schließt danach den Dialog: Navigator.of(context).pop();

  // TODO 3: Methode newEntry(): öffnet mit showDialog einen AlertDialog,
  //   dessen content ein TextField mit onSubmitted: addItem ist.

  @override
  Widget build(BuildContext context) {
    // TODO 4: Scaffold mit
    //   - appBar: AppBar mit Titel 'ToDo Liste'
    //   - body: ListView.builder, der für jedes ToDo ein ToDoItem baut
    //   - floatingActionButton mit Icon(Icons.add), der newEntry aufruft
    return const Scaffold(
      body: Center(child: Text('Hier entsteht die ToDo Liste')),
    );
  }
}

// ignore: unused_element
const _platzhalter = ToDoItem;
