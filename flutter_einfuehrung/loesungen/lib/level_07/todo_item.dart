import 'package:flutter/material.dart';

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
