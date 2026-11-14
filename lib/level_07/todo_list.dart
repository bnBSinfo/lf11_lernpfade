import 'package:flutter/material.dart';

import 'todo_item.dart';

class ToDoList extends StatefulWidget {
  const ToDoList({super.key});

  @override
  State<ToDoList> createState() => _ToDoListState();
}

class _ToDoListState extends State<ToDoList> {
  List<String> todos = [];

  void addItem(String item) {
    setState(() {
      todos.add(item);
    });
    Navigator.of(context).pop();
  }

  // TODO 1: Methode deleteItem(int i): entfernt in setState das Element an
  //   Position i aus der Liste (Tipp: removeAt).

  void newEntry() {
    showDialog<AlertDialog>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          content: TextField(
            autofocus: true,
            onSubmitted: addItem,
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ToDo Liste')),
      body: ListView.builder(
        itemCount: todos.length,
        itemBuilder: (context, i) {
          // TODO 4: Übergeben Sie dem ToDoItem zusätzlich die Löschfunktion:
          //   () => deleteItem(i)
          return ToDoItem(todos[i]);
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: newEntry,
        child: const Icon(Icons.add),
      ),
    );
  }
}
