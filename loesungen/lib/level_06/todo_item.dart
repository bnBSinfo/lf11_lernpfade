import 'package:flutter/material.dart';

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
