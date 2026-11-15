import 'package:flutter/material.dart';
import 'package:flutter_lernpfad/level_06/todo_item.dart';
import 'package:flutter_lernpfad/level_06/todo_list.dart';
import 'package:flutter_test/flutter_test.dart';

import 'hilfen.dart';

void main() {
  testWidgets('Level 6a: Aufbau der ToDo-Liste', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: ToDoList()));

    expect(find.descendant(of: find.byType(AppBar), matching: find.text('ToDo Liste')),
        findsOneWidget,
        reason: "Hinweis: Das Scaffold braucht appBar: AppBar(title: Text('ToDo Liste')).");
    expect(find.byType(ListView), findsOneWidget,
        reason: 'Hinweis: Der body ist ein ListView.builder.');
    expect(find.descendant(of: find.byType(FloatingActionButton), matching: find.byIcon(Icons.add)),
        findsOneWidget,
        reason: 'Hinweis: Es fehlt ein FloatingActionButton mit Icon(Icons.add).');
  });

  testWidgets('Level 6b: Einträge über den Dialog hinzufügen', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: ToDoList()));

    await eintragAnlegen(tester, 'Milch kaufen');
    expect(find.byType(AlertDialog), findsNothing,
        reason: 'Hinweis: Nach Enter soll sich der Dialog schließen: '
            'Navigator.of(context).pop(); in addItem.');
    expect(find.widgetWithText(ToDoItem, 'Milch kaufen'), findsOneWidget,
        reason: 'Hinweis: Der neue Eintrag muss als ToDoItem in der Liste erscheinen. '
            'Fügen Sie ihn in setState(...) mit todos.add(item) hinzu und bauen Sie im '
            'itemBuilder ein ToDoItem(todos[i]).');

    await eintragAnlegen(tester, 'LF11 lernen');
    expect(find.byType(ToDoItem), findsNWidgets(2),
        reason: 'Hinweis: Nach zwei Eingaben müssen zwei ToDoItems da sein '
            '(itemCount: todos.length).');
  });
}
