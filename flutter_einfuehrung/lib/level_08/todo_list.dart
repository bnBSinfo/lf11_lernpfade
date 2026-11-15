import 'package:flutter/material.dart';

import 'todo_item.dart';

class ToDoList extends StatefulWidget {
  const ToDoList({super.key});

  @override
  State<ToDoList> createState() => _ToDoListState();
}

class _ToDoListState extends State<ToDoList> {
  // TODO 1: Wandeln Sie die Liste in eine Map um: Map<String, bool> todos = {};
  //   Schlüssel = Titel, Wert = abgehakt ja/nein
  List<String> todos = [];

  void addItem(String item) {
    setState(() {
      todos.add(item);
    });
    Navigator.of(context).pop();
  }

  void deleteItem(int i) {
    setState(() {
      todos.removeAt(i);
    });
  }

  // TODO 2: Passen Sie addItem und deleteItem an die Map an
  //   (todos[item] = false;  bzw.  todos.remove(key);)

  // TODO 3: Neue Methode checkBoxDone(String key): dreht in setState den Wert
  //   um: todos.update(key, (bool done) => !done);

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
          // TODO 6: Holen Sie den Schlüssel: var key = todos.keys.elementAt(i);
          //   und übergeben Sie Titel, Status, Lösch- und Checkboxfunktion.
          return ToDoItem(todos[i], () => deleteItem(i));
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: newEntry,
        child: const Icon(Icons.add),
      ),
    );
  }
}
