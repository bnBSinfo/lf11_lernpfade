import 'package:flutter/material.dart';
import 'package:flutter_lernpfad/level_05/todo_item.dart';
import 'package:flutter_test/flutter_test.dart';

import 'hilfen.dart';

void main() {
  testWidgets('Level 5: ToDoItem mit Checkbox, Titel und Mülleimer', (tester) async {
    await tester.pumpWidget(testRahmen(const ToDoItem('Einkaufen')));

    expect(tester.widget(find.byType(ToDoItem)), isA<StatelessWidget>(),
        reason: 'Hinweis: ToDoItem bleibt ein Stateless Widget.');
    expect(find.text('Einkaufen'), findsOneWidget,
        reason: 'Hinweis: Der Titel (title) muss als Text angezeigt werden.');
    expect(find.byType(Row), findsWidgets,
        reason: 'Hinweis: Ordnen Sie die Teile mit einer Row nebeneinander an.');
    expect(find.byType(Checkbox), findsOneWidget,
        reason: 'Hinweis: Links fehlt die Checkbox (value: false, onChanged: null).');
    expect(loeschIcon, findsOneWidget,
        reason: 'Hinweis: Rechts fehlt ein IconButton mit Icon(Icons.delete).');
    expect(find.ancestor(of: loeschIcon, matching: find.byType(IconButton)), findsOneWidget,
        reason: 'Hinweis: Das Mülleimer-Icon gehört in einen IconButton.');

    final links = tester.getCenter(find.byType(Checkbox)).dx;
    final mitte = tester.getCenter(find.text('Einkaufen')).dx;
    final rechts = tester.getCenter(loeschIcon).dx;
    expect(links < mitte && mitte < rechts, isTrue,
        reason: 'Hinweis: Reihenfolge in der Row: Checkbox, Text, Mülleimer.');
  });
}
