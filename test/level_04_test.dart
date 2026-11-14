import 'package:flutter/material.dart';
import 'package:flutter_lernpfad/level_04/my_login.dart';
import 'package:flutter_test/flutter_test.dart';

import 'hilfen.dart';

void main() {
  testWidgets('Level 4a: Aufbau der Login-Maske', (tester) async {
    await tester.pumpWidget(testRahmen(const MyLogin()));

    expect(find.text('Willkommen'), findsOneWidget,
        reason: "Hinweis: Ganz oben in der Column steht Text('Willkommen').");
    expect(find.byType(TextField), findsNWidgets(2),
        reason: 'Hinweis: Die Maske braucht genau zwei TextFields (Benutzername, Passwort).');
    expect(find.text('Benutzername'), findsOneWidget,
        reason: "Hinweis: Beschriften Sie das erste Feld mit decoration: "
            "InputDecoration(labelText: 'Benutzername').");
    expect(find.text('Passwort'), findsOneWidget,
        reason: "Hinweis: Beschriften Sie das zweite Feld mit labelText: 'Passwort'.");
    final pw = tester.widget<TextField>(find.byType(TextField).at(1));
    expect(pw.obscureText, isTrue,
        reason: 'Hinweis: Das Passwort soll verdeckt sein: obscureText: true.');
    expect(buttonMitText('Login'), findsOneWidget,
        reason: "Hinweis: Es fehlt ein TextButton mit child: Text('Login').");
  });

  testWidgets('Level 4b: Login-Button erst aktiv, wenn beide Felder gefüllt sind',
      (tester) async {
    await tester.pumpWidget(testRahmen(const MyLogin()));
    final login = buttonMitText('Login');
    expect(login, findsOneWidget, reason: "Hinweis: Es fehlt der Button 'Login'.");
    final felder = find.byType(TextField);

    expect(istAktiv(tester, login), isFalse,
        reason: 'Hinweis: Am Anfang muss der Button inaktiv sein (onPressed: null, '
            'solange _canLogin false ist).');

    await tester.enterText(felder.at(0), 'anna');
    await tester.testTextInput.receiveAction(TextInputAction.done);
    await tester.pump();
    expect(istAktiv(tester, login), isFalse,
        reason: 'Hinweis: Nur Benutzername eingegeben – der Button muss noch inaktiv sein.');

    await tester.enterText(felder.at(1), 'geheim');
    await tester.testTextInput.receiveAction(TextInputAction.done);
    await tester.pump();
    expect(istAktiv(tester, login), isTrue,
        reason: 'Hinweis: Beide Felder gefüllt – jetzt muss der Button aktiv sein. '
            'Speichern die Felder ihre Werte (onChanged/onSubmitted) und rufen Sie '
            '_checkCanLogin mit setState auf?');

    await tester.enterText(felder.at(0), '');
    await tester.testTextInput.receiveAction(TextInputAction.done);
    await tester.pump();
    expect(istAktiv(tester, login), isFalse,
        reason: 'Hinweis: Benutzername wieder gelöscht – der Button muss wieder inaktiv '
            'werden (else-Zweig: _canLogin = false).');
  });
}
