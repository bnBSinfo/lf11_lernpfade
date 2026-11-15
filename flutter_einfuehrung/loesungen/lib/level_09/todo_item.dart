import 'package:flutter/material.dart';

class ToDoItem extends StatelessWidget {
  final String title;
  final bool done;
  final VoidCallback remove;
  final VoidCallback checkBoxDone;

  const ToDoItem(this.title, this.done, this.remove, this.checkBoxDone,
      {super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8),
      child: Row(
        children: [
          Checkbox(
            value: done,
            onChanged: (value) => checkBoxDone(),
          ),
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
