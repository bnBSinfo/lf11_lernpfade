// Liest pi.txt (IP und Ports Ihres Raspberry Pi).
import 'dart:io';

class PiKonfig {
  PiKonfig(this.ip, this.http, this.ssh);

  final String ip;
  final int http;
  final int ssh;

  bool get eingetragen => ip.isNotEmpty && ip != '0.0.0.0';

  /// Basisadresse des Webservers, z. B. http://10.36.13.76  (Port nur, wenn nicht 80)
  String get web => http == 80 ? 'http://$ip' : 'http://$ip:$http';

  static PiKonfig lesen([String pfad = 'pi.txt']) {
    final werte = <String, String>{};
    final datei = File(pfad);
    if (datei.existsSync()) {
      for (final zeile in datei.readAsLinesSync()) {
        final z = zeile.trim();
        if (z.isEmpty || z.startsWith('#') || !z.contains('=')) continue;
        final i = z.indexOf('=');
        werte[z.substring(0, i).trim().toLowerCase()] = z.substring(i + 1).trim();
      }
    }
    return PiKonfig(
      werte['ip'] ?? '',
      int.tryParse(werte['http'] ?? '') ?? 80,
      int.tryParse(werte['ssh'] ?? '') ?? 22,
    );
  }
}
