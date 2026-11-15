import 'package:flutter/material.dart';

import 'my_login.dart';

class MyFirstApp extends StatelessWidget {
  const MyFirstApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Meine erste App')),
        body: const MyLogin(),
      ),
    );
  }
}
