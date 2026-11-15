import 'package:flutter/material.dart';

class MyLogin extends StatefulWidget {
  const MyLogin({super.key});

  @override
  State<MyLogin> createState() => _MyLoginState();
}

class _MyLoginState extends State<MyLogin> {
  String _username = '';
  String _password = '';
  bool _canLogin = false;

  void _checkCanLogin() {
    setState(() {
      _canLogin = _username.isNotEmpty && _password.isNotEmpty;
    });
  }

  void _onChangedUsername(String username) {
    _username = username;
    _checkCanLogin();
  }

  void _onChangedPassword(String password) {
    _password = password;
    _checkCanLogin();
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: SizedBox(
        width: 300,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Willkommen'),
            TextField(
              onChanged: _onChangedUsername,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Benutzername',
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              onChanged: _onChangedPassword,
              obscureText: true,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Passwort',
              ),
            ),
            TextButton(
              onPressed: _canLogin ? () {} : null,
              child: const Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}
