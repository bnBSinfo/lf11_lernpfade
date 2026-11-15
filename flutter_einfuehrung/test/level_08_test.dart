import 'package:flutter/material.dart';
import 'package:flutter_lernpfad/level_08/todo_item.dart';
import 'package:flutter_lernpfad/level_08/todo_list.dart';
import 'package:flutter_test/flutter_test.dart';

import 'hilfen.dart';

bool? haken(WidgetTester tester, String titel) => tester
    .widget<Checkbox>(find.descendant(
        of: find.widgetWithText(ToDoItem, titel), matching: find.byType(Checkbox)))
    .value;

void main() {
  testWidgets('Level 8: Abhaken mit der Checkbox', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: ToDoList()));
    await eintragAnlegen(tester, 'Erstens');
    await eintragAnlegen(tester, 'Zweitens');
    expect(find.byType(ToDoItem), findsNWidgets(2),
        reason: 'Hinweis: Das Hinzufügen funktioniert nicht mehr – addItem an die Map '
            'anpassen: todos[item] = false;');

    expect(haken(tester, 'Erstens'), isFalse,
        reason: 'Hinweis: Neue ToDos sind nicht abgehakt (Wert false in der Map).');

    final box = find.descendant(
        of: find.widgetWithText(ToDoItem, 'Erstens'), matching: find.byType(Checkbox));
    await tester.tap(box);
    await tester.pumpAndSettle();
    expect(haken(tester, 'Erstens'), isTrue,
        reason: 'Hinweis: Nach dem Antippen muss die Checkbox einen Haken haben. '
            'Zeigt die Checkbox value: done an, und ruft onChanged checkBoxDone() auf? '
            'checkBoxDone(key) braucht setState und todos.update(...).');
    expect(haken(tester, 'Zweitens'), isFalse,
        reason: 'Hinweis: Es wurde das falsche ToDo abgehakt – prüfen Sie den key.');

    await tester.tap(box);
    await tester.pumpAndSettle();
    expect(haken(tester, 'Erstens'), isFalse,
        reason: 'Hinweis: Nochmal antippen muss den Haken wieder entfernen (=> !done).');

    await tester.tap(find.descendant(
        of: find.widgetWithText(ToDoItem, 'Erstens'), matching: loeschIcon));
    await tester.pumpAndSettle();
    expect(find.text('Erstens'), findsNothing,
        reason: 'Hinweis: Löschen funktioniert nicht mehr – deleteItem(String key) mit '
            'todos.remove(key).');
    expect(find.text('Zweitens'), findsOneWidget,
        reason: 'Hinweis: Es wurde das falsche ToDo gelöscht.');
  });
}
