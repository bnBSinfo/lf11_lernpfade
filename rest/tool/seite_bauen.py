#!/usr/bin/env python3
"""Baut docs/index.html (GitHub-Pages-Seite) aus docs/level_*.md und docs/bonus.md.

Aufruf im Projektordner:  python3 tool/seite_bauen.py   (braucht pandoc und openssl)
Passwort für die Musterlösungen: Eingabe oder Umgebungsvariable LOESUNG_PASSWORT.
Vorschau ohne Lösungen:   python3 tool/seite_bauen.py --ohne-loesungen
Stil: docs/css/stil.css (Lernpaket-Kompass, Welt "technik") + tool/seite.css (wie Flutter-Einführung).
"""
import base64
import datetime as _dt
import getpass
import hashlib
import html
import json
import os
import pathlib
import re
import secrets
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from datenfluss import CSS as DATENFLUSS_CSS, datenfluss_svg  # noqa: E402
import lernpfad_bausteine as bausteine  # noqa: E402
from kontrolle import KONTROLLE  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO = "bnBSinfo/lf11_lernpfade"
PAGES = "https://bnbsinfo.github.io/lf11_lernpfade/rest/"  # Downloads (api.php) liegen dort
ITERATIONEN = 600_000
VERSION = re.search(r"^version:\s*([\d.]+)", (ROOT / "pubspec.yaml").read_text(encoding="utf-8"), re.M).group(1)
STAND = _dt.date.today().strftime("%d.%m.%Y")
MARKER = "LOESUNG-OK\n"
NAME = "Pi-Server & REST-API"
e = html.escape

# ---------------------------------------------------------------- Server-Stack (unten → oben)
STACK = [
    ("Raspberry Pi + Ubuntu", "Hardware, Betriebssystem, apt"),
    ("SSH-Server", "Fernzugriff, Port 22"),
    ("Apache", "Webserver, Port 80, /var/www/html"),
    ("PHP", "führt .php-Dateien aus, mysqli"),
    ("MySQL + phpMyAdmin", "Datenbankserver, Port 3306 (nur localhost)"),
    ("flutterDB", "flutterUser, flutterTB, ToDoTB"),
    ("benutzer.php", "eigene Schnittstelle → JSON"),
    ("php-crud-api", "REST für alle Tabellen"),
    ("Dart: TodoApi", "Client – später in der Flutter-App"),
]

# ---------------------------------------------------------------- Inhalte je Level
# ziel: (Art, Kopfzeile, Inhalt)  Art: terminal | browser
LEVEL = {
    1: dict(titel="Den Pi in Betrieb nehmen", stich="SD-Karte, Benutzer, Updates, IP-Adresse",
            ziele=[("terminal", "administrator@pi: ~", "root@pi:~# hostname -I\n10.36.13.76\nroot@pi:~# apt upgrade -y\n0 aktualisiert, 0 neu installiert …")],
            kette=[("PC", "kennt die IP des Pi"), ("Netz", "LAN im pädagogischen Netz"), ("Pi", "antwortet unter 10.36.13.76")]),
    2: dict(titel="Fernzugriff mit SSH", stich="openssh-server, ssh, scp",
            ziele=[("terminal", "PC – Terminal", "C:\\> ssh administrator@10.36.13.76\nadministrator@10.36.13.76's password:\nWelcome to Ubuntu 24.04 LTS\nadministrator@pi:~$ hostname\npi")],
            bilder=[("moba_ssh", "MobaXterm: Session → SSH, IP und Benutzer eintragen")],
            kette=[("PC: ssh", "Tastatureingaben verschlüsselt"), ("Port 22", "sshd auf dem Pi"), ("Shell auf dem Pi", "führt Befehle aus")]),
    3: dict(titel="Der Webserver Apache", stich="apache2, Port 80, /var/www/html",
            ziele=[("browser", "http://10.36.13.76/", "<b>Apache2 Ubuntu Default Page</b>\nIt works!")],
            kette=[("Browser", "GET /"), ("Apache", "Port 80"), ("/var/www/html/index.html", "wird unverändert geschickt")]),
    4: dict(titel="PHP auf dem Webserver", stich="php, libapache2-mod-php, php-mysql, info.php",
            ziele=[("browser", "http://10.36.13.76/info.php", "<b>PHP Version 8.3</b>\n…\nmysqli\nClient API library version  mysqlnd 8.3")],
            kette=[("Browser", "GET /info.php"), ("Apache", "erkennt .php"), ("PHP", "führt phpinfo() aus"), ("Browser", "bekommt nur die Ausgabe")]),
    5: dict(titel="MySQL und phpMyAdmin", stich="mysql-server, phpmyadmin, Leertaste!",
            ziele=[("browser", "http://10.36.13.76/phpmyadmin/", "<b>Willkommen bei phpMyAdmin</b>\nBenutzername: [          ]\nPasswort:     [          ]\n[ OK ]")],
            bilder=[("pma_login", "Anmeldeseite von phpMyAdmin")],
            kette=[("Browser", "GET /phpmyadmin"), ("Apache + PHP", "phpMyAdmin"), ("MySQL", "localhost:3306")]),
    6: dict(titel="Datenbank und Tabellen anlegen", stich="CREATE USER, GRANT, PRIMARY KEY, AUTO_INCREMENT",
            ziele=[("terminal", "Pi – mysql", "mysql> USE flutterDB; SHOW TABLES;\n+---------------------+\n| Tables_in_flutterDB |\n+---------------------+\n| ToDoTB              |\n| flutterTB           |\n+---------------------+")],
            kette=[("flutterdb.sql", "auf dem PC schreiben"), ("scp", "auf den Pi kopieren"), ("mysql < …", "auf dem Pi ausführen"), ("flutterDB", "Benutzer + 2 Tabellen")]),
    7: dict(titel="Eine eigene PHP-Schnittstelle", stich="mysqli, SELECT, json_encode",
            ziele=[("browser", "http://10.36.13.76/benutzer.php", '[\n  {"id": 1, "name": "berno"},\n  {"id": 2, "name": "stoll"}\n]')],
            kette=[("Browser", "GET /benutzer.php"), ("PHP", "new mysqli(…)"), ("MySQL", "SELECT id, name …"), ("PHP", "json_encode → JSON")]),
    8: dict(titel="Die fertige REST-API", stich="php-crud-api, GET/POST/PUT/DELETE, curl",
            ziele=[("browser", "…/php-crud-api/api.php/records/ToDoTB", '{"records": [\n  {"id": 1, "name": "Pi einrichten", "checkbox": true},\n  {"id": 2, "name": "API testen", "checkbox": false}\n]}')],
            bilder=[("api_json", "Firefox zeigt die JSON-Antwort der API")],
            kette=[("HTTP-Methode", "GET · POST · PUT · DELETE"), ("Adresse", "/records/ToDoTB/3"), ("php-crud-api", "erzeugt SQL"), ("Antwort", "JSON")]),
    9: dict(titel="Die REST-API aus Dart nutzen", stich="package:http, async/await, jsonDecode",
            ziele=[("terminal", "PC – todo_client", "> dart run bin/todo_client.dart 10.36.13.76 neu \"Milch kaufen\"\nNeu angelegt mit id 3\n[x] 1: Pi einrichten\n[ ] 2: API testen\n[ ] 3: Milch kaufen")],
            kette=[("TodoApi.alle()", "Dart auf dem PC/Handy"), ("http.get", "GET …/records/ToDoTB"), ("jsonDecode", "Text → Map"), ("List<ToDo>", "fertig für die App")]),
}
ANZAHL = len(LEVEL)


# ---------------------------------------------------------------- Bausteine
def md_zu_html(pfad: pathlib.Path) -> str:
    text = re.sub(r"^# .*\n", "", pfad.read_text(encoding="utf-8"), count=1)
    out = subprocess.run(["pandoc", "-f", "gfm", "-t", "html", "--no-highlight"],
                         input=text, capture_output=True, text=True, check=True).stdout
    out = out.replace("<h2", "<h3").replace("</h2>", "</h3>")
    out = out.replace("<img ", '<img loading="lazy" ')
    return re.sub(r'(<h3 id="auftrag">.*?)(?=<h3 |\Z)',
                  r'<div class="auftrags-kasten">\1</div>', out, count=1, flags=re.S)


def kette(schritte):
    teile = []
    for i, (t, text) in enumerate(schritte):
        if i:
            teile.append('<span class="pfeil" aria-hidden="true">→</span>')
        teile.append(f'<div class="schritt-box"><b>{e(t)}</b><span>{e(text)}</span></div>')
    return f'<div class="kette">{"".join(teile)}</div>'


def ziel_html(art, kopf, inhalt):
    # Inhalt darf <b> enthalten, sonst wird escaped
    text = e(inhalt).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    if art == "terminal":
        return f'<figure class="term"><figcaption>{e(kopf)}</figcaption><pre>{text}</pre></figure>'
    return (f'<figure class="browser"><div class="leiste"><span></span><span></span><span></span>'
            f'<code>{e(kopf)}</code></div><pre>{text}</pre></figure>')


def stack_html(nr):
    zeilen = []
    for i, (name, info) in reversed(list(enumerate(STACK, 1))):
        klasse = "neu" if i == nr else ("da" if i < nr else "spaeter")
        marke = '<em class="neu-marke">neu</em>' if i == nr else ""
        zeilen.append(f'<li class="{klasse}"><b>{e(name)}</b><small>{e(info)}</small>{marke}</li>')
    return f'<ol class="stack">{"".join(zeilen)}</ol>'


def level_ansicht(nr: int, d: dict) -> str:
    ziele = "".join(ziel_html(*z) for z in d["ziele"])
    bilder = "".join(f'<figure class="foto"><img src="bilder/{b}.png" alt="{e(t)}" loading="lazy">'
                     f'<figcaption>{e(t)}</figcaption></figure>' for b, t in d.get("bilder", []))
    zurueck = f'<a class="knopf" href="#level-{nr-1}">◀ Level {nr-1}</a>' if nr > 1 else '<a class="knopf" href="#start">◀ Start</a>'
    weiter = f'<a class="knopf primaer" href="#level-{nr+1}">Level {nr+1} ▶</a>' if nr < ANZAHL else '<a class="knopf primaer" href="#bonus">Bonus ▶</a>'
    return f"""
<section class="ansicht level" id="level-{nr}" data-level="{nr}">
  <div class="card level-kopf">
    <span class="nummer" aria-hidden="true">{nr}</span>
    <div><h2>Level {nr} – {e(d['titel'])}</h2><p class="stich">{e(d['stich'])}</p></div>
  </div>
  <div class="level-raster">
    <div class="card lp-auftrag">{md_zu_html(DOCS / f"level_0{nr}.md")}
      <details class="loesung" data-loesung="{nr}" hidden><summary>🔓 Musterlösung Level {nr}</summary></details>
    </div>
    <aside class="lp-seite">
      <div class="card ziel"><h3>So soll es aussehen</h3>{ziele}{bilder}</div>
      <div class="card"><h3>Ihr Server-Stack</h3>{stack_html(nr)}
        <p class="legende"><span class="knoten da"><b>schon da</b></span><span class="knoten neu"><b>neu</b></span>
        <span class="knoten spaeter"><b>kommt noch</b></span></p></div>
    </aside>
  </div>
  {bausteine.selbstkontrolle_html(nr, KONTROLLE[nr])}
  <div class="card grafik"><h3>Wo sind wir im Datenfluss?</h3>{datenfluss_svg(nr)}
    <p class="legende"><span class="knoten neu"><b>neu / im Einsatz in diesem Level</b></span><span class="knoten da"><b>schon da</b></span>
    <span class="knoten spaeter"><b>kommt noch</b></span></p>
    <h3>Schritt für Schritt</h3>{kette(d['kette'])}</div>
  <div class="card lp-fuss">
    {zurueck}
    <div class="pruefen"><button class="erledigt" data-level="{nr}" disabled>Level geschafft</button></div>
    {weiter}
  </div>
</section>"""


def loesungen_verschluesseln(passwort: str) -> str:
    """Musterlösungen als JSON, AES-256-CBC, Schlüssel per PBKDF2-SHA256 aus dem Passwort."""
    zuordnung = {"6": ["server/sql/flutterdb.sql"], "7": ["server/php/benutzer.php"],
                 "9": ["lib/todo_api.dart", "bin/todo_client.dart"]}
    daten = {nr: [{"datei": p, "code": (ROOT / "loesungen" / p).read_text(encoding="utf-8")} for p in pfade]
             for nr, pfade in zuordnung.items()}
    klartext = (MARKER + json.dumps(daten, ensure_ascii=False)).encode("utf-8")
    salt, iv = secrets.token_bytes(16), secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", passwort.encode("utf-8"), salt, ITERATIONEN, 32)
    geheim = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-K", key.hex(), "-iv", iv.hex()],
                            input=klartext, capture_output=True, check=True).stdout
    b64 = lambda b: base64.b64encode(b).decode()
    return json.dumps({"salt": b64(salt), "iv": b64(iv), "iter": ITERATIONEN, "daten": b64(geheim)})


def passwort_holen() -> str:
    pw = os.environ.get("LOESUNG_PASSWORT", "")
    if not pw and sys.stdin.isatty():
        pw = getpass.getpass("Passwort für die Lösungen: ")
        if pw and pw != getpass.getpass("Passwort wiederholen: "):
            sys.exit("Die Passwörter stimmen nicht überein – abgebrochen.")
    if not pw:
        sys.exit("Kein Passwort angegeben (Eingabe oder LOESUNG_PASSWORT) – abgebrochen.")
    if len(pw) < 10:
        sys.exit("Bitte mindestens 10 Zeichen – die Seite ist öffentlich und kann durchprobiert werden.")
    return pw


CSS_EXTRA = """
.auftrags-kasten pre code{background:transparent}
.start-pi{display:flex;gap:24px;align-items:center}
.start-pi img{width:300px;max-width:40%;height:auto;flex:none}
.start-pi h2{margin-top:0}
@media (max-width:700px){.start-pi{flex-direction:column;align-items:flex-start}.start-pi img{width:220px;max-width:70%}}
.term,.browser{margin:0 0 10px;border-radius:12px;overflow:hidden;border:1px solid var(--line);font-size:.8rem}
.term figcaption{background:#2d3442;color:#cfd6e4;padding:5px 10px;font-family:ui-monospace,Consolas,monospace}
.term pre{margin:0;background:#141922;color:#d6f5d6;padding:10px 12px;white-space:pre-wrap;border-radius:0}
.browser .leiste{display:flex;gap:5px;align-items:center;background:#e9edf3;padding:6px 8px}
.browser .leiste span{width:9px;height:9px;border-radius:50%;background:#c4ccd8}
.browser .leiste code{flex:1;margin-left:6px;background:#fff;border-radius:8px;padding:2px 8px;font-size:.74rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.browser pre{margin:0;background:#fff;color:#1d2533;padding:10px 12px;white-space:pre-wrap;border-radius:0}
.foto{margin:0 0 8px}.foto img{width:100%;border-radius:10px;border:1px solid var(--line)}
.foto figcaption{font-size:.8rem;color:var(--ink-soft)}
.lp-auftrag img{max-width:100%;border-radius:10px;border:1px solid var(--line)}
.stack{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}
.stack li{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px;padding:5px 10px;border-radius:9px;border:1px solid var(--line)}
.stack small{color:var(--muted);font-size:.78rem}
.stack li.da,.knoten.da{background:#e3eefc;border-color:#9fc0ef}
.stack li.neu{background:#fde7dc;border-color:#f0a98a;box-shadow:0 0 0 2px var(--accent)}
.stack li.spaeter,.knoten.spaeter{opacity:.45;border-style:dashed}
.rest-bk{display:grid;grid-template-columns:260px minmax(0,1fr);gap:16px;align-items:start}
.rest-bk label{display:block;font-weight:600;margin:.6rem 0 .2rem}
.rest-bk select,.rest-bk input,.rest-bk textarea{font:inherit;width:100%;padding:6px 10px;border-radius:10px;border:1px solid var(--line);box-sizing:border-box}
.rest-bk .ausgabe h4{margin:.8rem 0 .3rem}.rest-bk .ausgabe h4:first-child{margin-top:0}
.rest-bk pre{white-space:pre-wrap;word-break:break-all}
@media (max-width:760px){.rest-bk{grid-template-columns:minmax(0,1fr)}}
"""

JS = r"""
document.documentElement.classList.add("js");
(function(){
  var KEY = "rest-lernpfad-lf11", stand = {}, ANZAHL = %d;
  try { stand = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
  var ansichten = document.querySelectorAll(".ansicht");
  function route(){
    var ziel = document.getElementById((location.hash || "#start").slice(1));
    var ansicht = ziel && ziel.closest(".ansicht");
    if (!ansicht) { ansicht = document.getElementById("start"); ziel = null; }
    var id = ansicht.id;
    ansichten.forEach(function(a){ a.hidden = a.id !== id; });
    document.querySelectorAll("[data-ziel]").forEach(function(c){ c.classList.toggle("aktiv", c.dataset.ziel === id); });
    if (ziel && ziel !== ansicht) ziel.scrollIntoView(); else window.scrollTo(0, 0);
  }
  function zeigen(){
    var n = 0;
    document.querySelectorAll(".level").forEach(function(s){
      var nr = s.dataset.level, ok = !!stand[nr];
      if (ok) n++;
      s.classList.toggle("fertig", ok);
      var b = s.querySelector("button.erledigt");
      b.textContent = ok ? "✓ Geschafft (zurücksetzen)" : "Level geschafft";
      b.setAttribute("aria-pressed", ok);
      document.querySelectorAll('[data-ziel="level-' + nr + '"]').forEach(function(c){ c.classList.toggle("ok", ok); });
    });
    document.getElementById("zaehler").textContent = n + " / " + ANZAHL;
  }
  document.querySelectorAll("button.erledigt").forEach(function(b){
    b.addEventListener("click", function(){
      stand[b.dataset.level] = !stand[b.dataset.level];
      try { localStorage.setItem(KEY, JSON.stringify(stand)); } catch (e) {}
      zeigen();
    });
  });
  window.addEventListener("hashchange", route);
  route(); zeigen();
})();
""" % ANZAHL

JS_LOESUNG = r"""
(function(){
  if (typeof GEHEIM === "undefined" || !GEHEIM) return;
  var b = function(s){ return Uint8Array.from(atob(s), function(c){ return c.charCodeAt(0); }); };
  var status = document.getElementById("pw-status");
  async function entschluesseln(pw){
    var basis = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveKey"]);
    var key = await crypto.subtle.deriveKey(
      {name: "PBKDF2", salt: b(GEHEIM.salt), iterations: GEHEIM.iter, hash: "SHA-256"},
      basis, {name: "AES-CBC", length: 256}, false, ["decrypt"]);
    var klar = await crypto.subtle.decrypt({name: "AES-CBC", iv: b(GEHEIM.iv)}, key, b(GEHEIM.daten));
    var text = new TextDecoder().decode(klar);
    if (text.indexOf(MARKER) !== 0) throw new Error("falsch");
    return JSON.parse(text.slice(MARKER.length));
  }
  function einfuegen(daten){
    Object.keys(daten).forEach(function(nr){
      var box = document.querySelector('[data-loesung="' + nr + '"]');
      if (!box) return;
      box.querySelectorAll("div").forEach(function(d){ d.remove(); });
      daten[nr].forEach(function(f){
        var div = document.createElement("div");
        var h = document.createElement("h3"); h.textContent = f.datei;
        var pre = document.createElement("pre"), code = document.createElement("code");
        code.textContent = f.code; pre.appendChild(code);
        div.appendChild(h); div.appendChild(pre); box.appendChild(div);
      });
      box.hidden = false;
    });
  }
  document.getElementById("entsperren").addEventListener("submit", async function(ev){
    ev.preventDefault();
    status.textContent = "Prüfe …";
    try {
      einfuegen(await entschluesseln(document.getElementById("pw").value));
      status.textContent = "✓ Freigeschaltet – die Lösungen stehen in Level 6, 7 und 9 unten im Auftrag.";
    } catch (err) { status.textContent = "✗ Passwort falsch."; }
  });
})();
"""


def main() -> None:
    ohne = "--ohne-loesungen" in sys.argv
    geheim = "null" if ohne else loesungen_verschluesseln(passwort_holen())
    css = (ROOT / "tool" / "seite.css").read_text(encoding="utf-8") + CSS_EXTRA + DATENFLUSS_CSS + bausteine.CSS
    navi = ('<a class="chip" href="#start" data-ziel="start">Start</a>'
            + "".join(f'<a class="chip" href="#level-{n}" data-ziel="level-{n}">{n}</a>' for n in LEVEL)
            + '<a class="chip" href="#wissen" data-ziel="wissen" title="Wissen: REST">📘 Wissen</a>'
            + '<a class="chip" href="#bonus" data-ziel="bonus">★</a>'
            + '<a class="chip" href="#loesungen" data-ziel="loesungen" title="Musterlösungen">🔒</a>'
            + f'<span class="chip zaehler" id="zaehler">0 / {ANZAHL}</span>')
    uebersicht = "".join(
        f'<a href="#level-{n}" data-ziel="level-{n}"><b>{n} · {e(d["titel"])}</b><span class="klein">{e(d["stich"])}</span>'
        f'<span class="fertig-marke">✓ geschafft</span></a>' for n, d in LEVEL.items())
    ansichten = "".join(level_ansicht(n, d) for n, d in LEVEL.items())
    seite = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(NAME)} LF11</title>
<meta name="version" content="{VERSION}">
<meta name="description" content="In 9 Leveln vom Raspberry Pi zum Datenbankserver mit REST-API – alles selbst getippt, mit Selbstkontrolle.">
<link rel="stylesheet" href="css/stil.css">
<style>{css}</style>
</head>
<body data-thema="technik">
<div class="app">
  <header class="card kopf">
    <div class="titel">
      <h1>{e(NAME)} <span class="version">LF11 · Version {VERSION}</span></h1>
      <div class="unter">In 9 Leveln vom Raspberry Pi zum Datenbankserver, den Ihre App über REST anspricht.</div>
    </div>
    <nav class="fortschritt" aria-label="Level">{navi}</nav>
  </header>

  <section class="ansicht" id="start">
    <div class="card start-pi">
      <img src="bilder/raspberry_pi.png" alt="Raspberry Pi 4: Platine mit USB-, LAN- und HDMI-Anschlüssen" width="480" height="308">
      <div><h2>Ihr Server im Taschenformat</h2>
      <p><b>Gearbeitet wird am echten Raspberry Pi und in Ihrer eigenen Entwicklungsumgebung</b> – Terminal, SSH, Webserver,
      Datenbank und Dart, genau wie im Betrieb. Es gibt <b>keine Vorlagen zum Herunterladen</b>: Jede Zeile tippen Sie selbst.</p>
      <p>Diese Seite ist Ihr Wegweiser: Auftrag, Zielbild, Datenfluss, Hilfen und Selbstkontrolle.</p></div></div>
    <div class="card"><h2>So geht's</h2>
      <div class="start-raster">
        <div><h3>1 · Bereitlegen</h3>
          <p>Raspberry Pi mit SD-Karte, Netzteil und LAN-Kabel, dazu Ihr PC mit Terminal (ab Level 9 mit Dart).</p></div>
        <div><h3>2 · Auftrag lesen</h3>
          <p>Der rote Kasten sagt, was zu tun ist. <i>Erklärt</i> sagt, warum. Die Tipps öffnen Sie nur, wenn Sie nicht weiterkommen.</p></div>
        <div><h3>3 · Abtippen</h3>
          <p>Befehle und Code werden <b>abgetippt</b> – Kopieren ist auf dieser Seite gesperrt. Wer tippt, liest jede Zeile
          und versteht die Fehlermeldungen.</p></div>
        <div><h3>4 · Selbstkontrolle</h3>
          <p>Unter jedem Level: Haken setzen, was wirklich funktioniert, Kontrollfragen beantworten – dann ist das Level geschafft.</p></div>
      </div>
    </div>
    <div class="card"><h2>Grundlagen zum Nachschlagen</h2>
      <p><a href="#wissen">📘 Wissen: REST</a> – HTTP-Methoden, Statuscodes, JSON und ein Baukasten, der Ihnen zu jeder
      Anfrage die Adresse, den curl-Befehl, den Dart-Code und das SQL dahinter zeigt.</p></div>
    <div class="card"><h2>Ihr Weg in 9 Leveln</h2><div class="uebersicht">{uebersicht}</div>
      <p style="margin-top:14px"><a class="knopf primaer" href="#level-1">Los geht's mit Level 1 ▶</a></p></div>
  </section>
{ansichten}
  <section class="ansicht" id="wissen">
{(ROOT / "tool" / "wissen.html").read_text(encoding="utf-8").replace("<!--DATENFLUSS-->", datenfluss_svg())}
    <div class="card lp-fuss"><a class="knopf" href="#start">◀ Start</a><a class="knopf primaer" href="#level-8">Zu Level 8 ▶</a></div>
  </section>

  <section class="ansicht" id="bonus">
    <div class="card level-kopf"><span class="nummer" aria-hidden="true">★</span>
      <div><h2>Bonus – Server absichern und App anbinden</h2><p class="stich">für alle, die fertig sind</p></div></div>
    <div class="card">{md_zu_html(DOCS / "bonus.md")}</div>
    <div class="card lp-fuss"><a class="knopf" href="#level-{ANZAHL}">◀ Level {ANZAHL}</a><a class="knopf" href="#start">Zum Start</a></div>
  </section>

  <section class="ansicht" id="loesungen">
    <div class="card"><h2>🔒 Musterlösungen</h2>
      <p>Die Lösungen zu Level 6, 7 und 9 sind verschlüsselt. Mit dem Passwort Ihrer Lehrkraft erscheinen sie im
      jeweiligen Level unten im Auftrag. Erst selbst probieren – Fehlermeldungen lesen und die Tipps nutzen bringt mehr als jede Lösung!</p>
      <form id="entsperren" class="pruefen">
        <label for="pw" class="sr">Passwort</label>
        <input id="pw" type="password" autocomplete="off" placeholder="Passwort"
          style="font:inherit;padding:8px 12px;border-radius:12px;border:1px solid var(--line);min-height:42px">
        <button class="primaer" type="submit">Lösungen anzeigen</button>
        <span id="pw-status" role="status"></span>
      </form></div>
  </section>

  <footer class="druckfuss"><small>{e(NAME)} LF11 · Version {VERSION} vom {STAND} · BS Info · Ihr Fortschritt auf dieser Seite wird nur in Ihrem Browser gespeichert.</small></footer>
</div>
<script>var LP_KEY = "rest-lernpfad-lf11";{JS}</script>
<script>{bausteine.JS}</script>
<script>{(ROOT / "tool" / "rest_baukasten.js").read_text(encoding="utf-8")}</script>
<script>var GEHEIM = {geheim}; var MARKER = {json.dumps(MARKER)};{JS_LOESUNG}</script>
</body>
</html>
"""
    seite = seite.replace('href="downloads/', f'href="{PAGES}downloads/')
    (DOCS / "index.html").write_text(bausteine.einbetten(seite, DOCS), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print("Erstellt:", DOCS / "index.html", "(ohne Lösungen)" if ohne else "")


if __name__ == "__main__":
    main()
