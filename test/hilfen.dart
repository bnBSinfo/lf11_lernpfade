import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

/// Packt ein Widget in MaterialApp + Scaffold, damit es getestet werden kann.
Widget testRahmen(Widget kind) => MaterialApp(home: Scaffold(body: kind));

/// Findet einen Button (TextButton, ElevatedButton, FilledButton, ...) mit Text.
Finder buttonMitText(String text) =>
    find.ancestor(of: find.text(text), matching: find.byWidgetPredicate((w) => w is ButtonStyleButton));

bool istAktiv(WidgetTester tester, Finder button) =>
    tester.widget<ButtonStyleButton>(button.first).enabled;

final Finder loeschIcon = find.byWidgetPredicate((w) =>
    w is Icon &&
    (w.icon == Icons.delete ||
        w.icon == Icons.delete_outline ||
        w.icon == Icons.delete_forever));

/// Legt in der ToDo-Liste über den +-Button und den Dialog einen Eintrag an.
Future<void> eintragAnlegen(WidgetTester tester, String titel) async {
  final plus = find.byType(FloatingActionButton);
  expect(plus, findsOneWidget,
      reason: 'Hinweis: Es fehlt der FloatingActionButton zum Hinzufügen.');
  await tester.tap(plus);
  await tester.pumpAndSettle();
  expect(find.byType(AlertDialog), findsOneWidget,
      reason: 'Hinweis: Nach dem Tippen auf + soll sich ein AlertDialog öffnen '
          '(showDialog in newEntry).');
  final feld = find.descendant(
      of: find.byType(AlertDialog), matching: find.byType(TextField));
  expect(feld, findsOneWidget,
      reason: 'Hinweis: Der AlertDialog braucht als content ein TextField.');
  await tester.enterText(feld, titel);
  await tester.testTextInput.receiveAction(TextInputAction.done);
  await tester.pumpAndSettle();
}
