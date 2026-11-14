import 'package:flutter/material.dart';
import 'package:flutter_lernpfad/level_07/todo_item.dart';
import 'package:flutter_lernpfad/level_07/todo_list.dart';
import 'package:flutter_test/flutter_test.dart';

import 'hilfen.dart';

void main() {
  testWidgets('Level 7: Einträge mit dem Mülleimer löschen', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: ToDoList()));
    for (final t in ['A-Aufgabe', 'B-Aufgabe', 'C-Aufgabe']) {
      await eintragAnlegen(tester, t);
    }
    expect(find.byType(ToDoItem), findsNWidgets(3),
        reason: 'Hinweis: Das Hinzufügen aus Level 6 funktioniert nicht mehr.');

    final muell = find.descendant(
        of: find.widgetWithText(ToDoItem, 'B-Aufgabe'), matching: loeschIcon);
    expect(muell, findsOneWidget, reason: 'Hinweis: Der Mülleimer im ToDoItem fehlt.');
    await tester.tap(muell);
    await tester.pumpAndSettle();

    expect(find.text('B-Aufgabe'), findsNothing,
        reason: 'Hinweis: Nach dem Tippen auf den Mülleimer muss der Eintrag verschwinden. '
            'Ist onPressed des IconButtons mit remove() verbunden, und übergeben Sie im '
            'itemBuilder () => deleteItem(i)? deleteItem braucht setState!');
    expect(find.text('A-Aufgabe'), findsOneWidget,
        reason: 'Hinweis: Es wurde der falsche Eintrag gelöscht – prüfen Sie den Index i.');
    expect(find.text('C-Aufgabe'), findsOneWidget,
        reason: 'Hinweis: Es wurde der falsche Eintrag gelöscht – prüfen Sie den Index i.');
  });
}
