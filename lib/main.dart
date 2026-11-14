import 'package:flutter/material.dart';

import 'level_01/my_first_app.dart' as level1;
import 'level_02/my_first_app.dart' as level2;
import 'level_03/my_first_app.dart' as level3;
import 'level_04/my_first_app.dart' as level4;
import 'level_05/app.dart' as level5;
import 'level_06/app.dart' as level6;
import 'level_07/app.dart' as level7;
import 'level_08/app.dart' as level8;
import 'level_09/my_first_app.dart' as level9;

// ┌──────────────────────────────────────────────────────────────┐
// │ Welches Level wollen Sie im Emulator / Browser sehen?        │
// │ Zahl ändern, speichern, dann "Hot Restart".                  │
// └──────────────────────────────────────────────────────────────┘
const int aktivesLevel = 1;

// In der main läuft die App: das Start-Widget wird an runApp() übergeben.
void main() {
  runApp(switch (aktivesLevel) {
    1 => const level1.MyFirstApp(),
    2 => const level2.MyFirstApp(),
    3 => const level3.MyFirstApp(),
    4 => const level4.MyFirstApp(),
    5 => const level5.ToDoApp(),
    6 => const level6.ToDoApp(),
    7 => const level7.ToDoApp(),
    8 => const level8.ToDoApp(),
    _ => const level9.MyFirstApp(),
  });
}
