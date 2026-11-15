import 'package:flutter/material.dart';
import 'package:flutter_lernpfad/level_09/my_first_app.dart';
import 'package:flutter_lernpfad/level_09/todo_list.dart';
import 'package:flutter_test/flutter_test.dart';

import 'hilfen.dart';

void main() {
  testWidgets('Level 9: Login öffnet die ToDo-Liste', (tester) async {
    await tester.pumpWidget(const MyFirstApp());
    final felder = find.byType(TextField);
    expect(felder, findsNWidgets(2),
        reason: 'Hinweis: Die App muss mit der Login-Maske starten – main.dart startet '
            'wieder MyFirstApp (body: MyLogin()).');
    await tester.enterText(felder.at(0), 'anna');
    await tester.enterText(felder.at(1), 'geheim');
    await tester.pump();
    await tester.tap(buttonMitText('Login'));
    await tester.pumpAndSettle();
    expect(find.byType(ToDoList), findsOneWidget,
        reason: 'Hinweis: Nach dem Login muss die ToDo-Liste erscheinen. Im onPressed des '
            'Login-Buttons: Navigator.of(context).push(MaterialPageRoute('
            'builder: (context) => const ToDoList()));');

    await eintragAnlegen(tester, 'Milch kaufen');
    expect(find.text('Milch kaufen'), findsOneWidget,
        reason: 'Hinweis: Die ToDo-Liste aus Level 8 muss nach dem Login weiter funktionieren.');

    final zurueck = find.byType(BackButton);
    expect(zurueck, findsOneWidget,
        reason: 'Hinweis: In der AppBar der Liste fehlt der Zurück-Pfeil. Verwenden Sie push '
            '(nicht pushReplacement).');
    await tester.tap(zurueck);
    await tester.pumpAndSettle();
    expect(find.byType(ToDoList), findsNothing,
        reason: 'Hinweis: Der Zurück-Pfeil soll wieder zur Login-Maske führen.');
    expect(buttonMitText('Login'), findsOneWidget,
        reason: 'Hinweis: Nach dem Zurück muss die Login-Maske wieder zu sehen sein.');
  });
}
