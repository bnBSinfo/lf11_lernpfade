import 'package:flutter/material.dart';

import 'todo_item.dart';

class ToDoList extends StatefulWidget {
  const ToDoList({super.key});

  @override
  State<ToDoList> createState() => _ToDoListState();
}

class _ToDoListState extends State<ToDoList> {
  Map<String, bool> todos = {};

  void addItem(String item) {
    setState(() {
      todos[item] = false;
    });
    Navigator.of(context).pop();
  }

  void deleteItem(String key) {
    setState(() {
      todos.remove(key);
    });
  }

  void checkBoxDone(String key) {
    setState(() {
      todos.update(key, (bool done) => !done);
    });
  }

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
          var key = todos.keys.elementAt(i);
          return ToDoItem(
            key, // Titel
            todos.values.elementAt(i), // Checkboxstatus
            () => deleteItem(key), // Löschfunktion
            () => checkBoxDone(key), // Checkboxfunktion
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: newEntry,
        child: const Icon(Icons.add),
      ),
    );
  }
}
