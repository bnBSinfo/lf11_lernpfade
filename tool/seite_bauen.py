#!/usr/bin/env python3
"""Baut docs/index.html (GitHub-Pages-Seite) aus docs/level_*.md und docs/bonus.md.

Aufruf im Projektordner:  python3 tool/seite_bauen.py   (braucht pandoc)
Stil: css/stil.css aus den Lernpaketen (Lernpaket-Kompass), Welt "technik".
"""
import base64
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

ITERATIONEN = 600_000
MARKER = "LOESUNG-OK\n"


def loesungen_verschluesseln(passwort: str) -> str:
    """Musterlösungen als JSON, AES-256-CBC, Schlüssel per PBKDF2-SHA256 aus dem Passwort.
    Ergebnis: JSON mit salt, iv, daten (Base64) – entschlüsselt wird im Browser (WebCrypto)."""
    daten = {}
    for ordner in sorted((ROOT / "loesungen" / "lib").glob("level_0*")):
        nr = ordner.name[-1]
        daten[nr] = [
            {"datei": f"lib/{ordner.name}/{f.name}", "code": f.read_text(encoding="utf-8")}
            for f in sorted(ordner.glob("*.dart"))
        ]
    klartext = (MARKER + json.dumps(daten, ensure_ascii=False)).encode("utf-8")
    salt, iv = secrets.token_bytes(16), secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", passwort.encode("utf-8"), salt, ITERATIONEN, 32)
    geheim = subprocess.run(
        ["openssl", "enc", "-aes-256-cbc", "-K", key.hex(), "-iv", iv.hex()],
        input=klartext, capture_output=True, check=True,
    ).stdout
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

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO = "bnBSinfo/flutter_lernpfad_schueler"

LEVEL = [
    (1, "Das Grundgerüst", "MaterialApp, Scaffold"),
    (2, "Widget im Widget", "Padding, ColoredBox, Center"),
    (3, "Das erste Stateful Widget", "StatefulWidget, State"),
    (4, "Die Login-Maske", "TextField, setState"),
    (5, "Ein ToDo-Element", "Row, Checkbox, IconButton"),
    (6, "Die ToDo-Liste", "ListView.builder, Dialog"),
    (7, "Löschen", "Funktionen als Parameter"),
    (8, "Abhaken", "Map statt List"),
]


def md_zu_html(pfad: pathlib.Path) -> str:
    text = pfad.read_text(encoding="utf-8")
    text = re.sub(r"^# .*\n", "", text, count=1)  # Überschrift setzt die Seite selbst
    out = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html", "--no-highlight"],
        input=text, capture_output=True, text=True, check=True,
    ).stdout
    return out.replace("<h2", "<h3").replace("</h2>", "</h3>")


def level_karte(nr: int, titel: str, stichworte: str) -> str:
    inhalt = md_zu_html(DOCS / f"level_0{nr}.md")
    return f"""
<section class="card level" id="level-{nr}" data-level="{nr}">
  <header class="level-kopf">
    <span class="nummer" aria-hidden="true">{nr}</span>
    <div><h2>Level {nr} – {html.escape(titel)}</h2>
    <p class="stich">{html.escape(stichworte)}</p></div>
  </header>
  <div class="level-inhalt">{inhalt}</div>
  <div class="pruefen">
    <code>flutter test test/level_0{nr}_test.dart</code>
    <button class="primaer erledigt" data-level="{nr}">Test ist grün – Level geschafft</button>
  </div>
  <details class="loesung" data-loesung="{nr}" hidden><summary>🔓 Musterlösung Level {nr}</summary></details>
</section>"""


def main() -> None:
    chips = "".join(
        f'<a class="chip" href="#level-{n}" data-chip="{n}">{n}</a>' for n, *_ in LEVEL
    )
    karten = "".join(level_karte(*l) for l in LEVEL)
    geheim = loesungen_verschluesseln(passwort_holen())
    bonus = md_zu_html(DOCS / "bonus.md")
    seite = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Flutter-Lernpfad LF11</title>
<meta name="description" content="In 8 Leveln zur ersten eigenen Flutter-App – mit automatischen Tests.">
<link rel="stylesheet" href="css/stil.css">
<style>
  .kopf{{padding:20px 22px}}
  .level-kopf{{display:flex;gap:14px;align-items:center}}
  .nummer{{flex:0 0 46px;height:46px;border-radius:12px;display:grid;place-items:center;
    font-family:var(--titel);font-weight:800;font-size:1.3rem;background:var(--accent-soft);color:var(--accent)}}
  .level.fertig .nummer{{background:var(--ok);color:#fff}}
  .level.fertig .nummer::after{{content:"✓";font-size:.8rem;margin-left:2px}}
  .level-kopf h2{{margin:0}}
  .stich{{margin:0;color:var(--muted);font-size:.9rem}}
  .level-inhalt{{max-width:78ch}}
  pre{{background:#1a2130;color:#e8ebf0;border-radius:12px;padding:12px 14px;overflow-x:auto;font-size:.88rem}}
  pre code{{background:none;border:0;color:inherit;padding:0}}
  blockquote{{margin:.8rem 0;padding:10px 14px;border-left:4px solid var(--deko);background:var(--accent-soft);border-radius:0 12px 12px 0}}
  blockquote p{{margin:0}}
  table{{border-collapse:collapse;margin:.6rem 0;width:100%}}
  td,th{{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}}
  th{{background:var(--card2)}}
  summary{{cursor:pointer;font-weight:700}}
  .pruefen{{display:flex;gap:12px;flex-wrap:wrap;align-items:center;justify-content:space-between;
    margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}}
  .level.fertig button.erledigt{{background:var(--ok);border-color:var(--ok)}}
  .raster{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}
  .schritt h3{{margin-top:0}}
  .kopf a.chip{{text-decoration:none}}
  .kopf a.chip.ok{{background:rgba(255,255,255,.95);color:var(--ok);border-color:#fff}}
  .zaehler{{font-weight:700}}
  a{{color:var(--accent)}}
  .sr{{position:absolute;left:-9999px}}
  details.loesung{{margin-top:12px}}
  @media (max-width:600px){{.app{{padding:10px}} .kopf{{padding:16px}}}}
</style>
</head>
<body data-thema="technik">
<div class="app">
  <header class="card kopf">
    <div class="titel">
      <h1>Flutter-Lernpfad <span class="version">LF11</span></h1>
      <div class="unter">In 8 Leveln zur ersten eigenen App – Sie programmieren echt, die Tests prüfen mit.</div>
    </div>
    <nav class="fortschritt" aria-label="Level">{chips}
      <span class="chip zaehler" id="zaehler">0 / 8</span></nav>
  </header>

  <section class="card">
    <h2>So geht's</h2>
    <p><b>Programmiert wird nicht im Browser, sondern in Ihrer echten Entwicklungsumgebung</b>
    (Android Studio oder VS Code) mit einem echten Flutter-Projekt, echtem Emulator und echten Tests –
    genau wie im Betrieb. Diese Seite ist Ihr Wegweiser.</p>
    <div class="raster">
      <div class="schritt"><h3>1 · Projekt holen</h3>
        <p><a href="https://github.com/{REPO}/archive/refs/heads/main.zip">ZIP herunterladen</a> und entpacken – oder:</p>
        <pre><code>git clone https://github.com/{REPO}.git</code></pre></div>
      <div class="schritt"><h3>2 · Öffnen</h3>
        <p>Ordner in Android Studio oder VS Code öffnen, einmalig im Terminal:</p>
        <pre><code>flutter pub get</code></pre></div>
      <div class="schritt"><h3>3 · Programmieren</h3>
        <p>Auftrag unten lesen, <code>TODO</code>s in <code>lib/level_0X/</code> lösen.
        Ansehen: in <code>lib/main.dart</code> <code>aktivesLevel</code> setzen und App starten.</p></div>
      <div class="schritt"><h3>4 · Prüfen</h3>
        <p>Test starten – bei Rot steht ein <b>Hinweis</b> in der Ausgabe. Gesamtstand:</p>
        <pre><code>dart run tool/fortschritt.dart</code></pre></div>
    </div>
    <details><summary>Tests in der IDE starten</summary>
      <p><b>Android Studio:</b> Rechtsklick auf die Testdatei → <i>Run 'tests in …'</i><br>
      <b>VS Code:</b> Seitenleiste <i>Testing</i> (Reagenzglas) oder ▶ über <code>main()</code></p>
    </details>
  </section>
{karten}
  <section class="card" id="bonus">
    <header class="level-kopf"><span class="nummer" aria-hidden="true">★</span>
      <div><h2>Bonus – Die App weiterentwickeln</h2><p class="stich">für alle, die fertig sind</p></div></header>
    <div class="level-inhalt">{bonus}</div>
  </section>

  <section class="card" id="loesungen">
    <h2>Musterlösungen</h2>
    <p>Die Lösungen sind verschlüsselt. Mit dem Passwort Ihrer Lehrkraft erscheinen sie in jedem Level
    unter <i>Musterlösung</i>. Erst selbst probieren – die Tests verraten Ihnen mehr als jede Lösung!</p>
    <form id="entsperren" class="pruefen" style="border:0;justify-content:flex-start">
      <label for="pw" class="sr">Passwort</label>
      <input id="pw" type="password" autocomplete="off" placeholder="Passwort"
        style="font:inherit;padding:8px 12px;border-radius:12px;border:1px solid var(--line);min-height:42px">
      <button class="primaer" type="submit">Lösungen anzeigen</button>
      <span id="pw-status" role="status"></span>
    </form>
  </section>

  <footer class="druckfuss"><small>Flutter-Lernpfad LF11 · BS Info · Ihr Fortschritt auf dieser Seite wird nur in Ihrem Browser gespeichert.</small></footer>
</div>
<script>
(function(){{
  var KEY = "flutter-lernpfad-lf11";
  var stand = {{}};
  try {{ stand = JSON.parse(localStorage.getItem(KEY)) || {{}}; }} catch (e) {{}}
  function zeigen(){{
    var n = 0;
    document.querySelectorAll(".level").forEach(function(s){{
      var nr = s.dataset.level, ok = !!stand[nr];
      if (ok) n++;
      s.classList.toggle("fertig", ok);
      var b = s.querySelector("button.erledigt");
      b.textContent = ok ? "✓ Geschafft (zurücksetzen)" : "Test ist grün – Level geschafft";
      b.setAttribute("aria-pressed", ok);
      var c = document.querySelector('[data-chip="' + nr + '"]');
      if (c) c.classList.toggle("ok", ok);
    }});
    document.getElementById("zaehler").textContent = n + " / 8";
  }}
  document.querySelectorAll("button.erledigt").forEach(function(b){{
    b.addEventListener("click", function(){{
      stand[b.dataset.level] = !stand[b.dataset.level];
      try {{ localStorage.setItem(KEY, JSON.stringify(stand)); }} catch (e) {{}}
      zeigen();
    }});
  }});
  zeigen();
}})();

(function(){{
  var GEHEIM = {geheim};
  var MARKER = {json.dumps(MARKER)};
  var b = function(s){{ return Uint8Array.from(atob(s), function(c){{ return c.charCodeAt(0); }}); }};
  var status = document.getElementById("pw-status");
  async function entschluesseln(pw){{
    var basis = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveKey"]);
    var key = await crypto.subtle.deriveKey(
      {{name: "PBKDF2", salt: b(GEHEIM.salt), iterations: GEHEIM.iter, hash: "SHA-256"}},
      basis, {{name: "AES-CBC", length: 256}}, false, ["decrypt"]);
    var klar = await crypto.subtle.decrypt({{name: "AES-CBC", iv: b(GEHEIM.iv)}}, key, b(GEHEIM.daten));
    var text = new TextDecoder().decode(klar);
    if (text.indexOf(MARKER) !== 0) throw new Error("falsch");
    return JSON.parse(text.slice(MARKER.length));
  }}
  function einfuegen(daten){{
    Object.keys(daten).forEach(function(nr){{
      var box = document.querySelector('[data-loesung="' + nr + '"]');
      if (!box) return;
      box.querySelectorAll("div").forEach(function(d){{ d.remove(); }});
      daten[nr].forEach(function(f){{
        var div = document.createElement("div");
        var h = document.createElement("h3"); h.textContent = f.datei;
        var pre = document.createElement("pre"), code = document.createElement("code");
        code.textContent = f.code; pre.appendChild(code);
        div.appendChild(h); div.appendChild(pre); box.appendChild(div);
      }});
      box.hidden = false;
    }});
  }}
  document.getElementById("entsperren").addEventListener("submit", async function(e){{
    e.preventDefault();
    status.textContent = "Prüfe …";
    try {{
      einfuegen(await entschluesseln(document.getElementById("pw").value));
      status.textContent = "✓ Lösungen sind in den Leveln freigeschaltet.";
    }} catch (err) {{
      status.textContent = "✗ Passwort falsch.";
    }}
  }});
}})();
</script>
</body>
</html>
"""
    (DOCS / "index.html").write_text(seite, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print("Erstellt:", DOCS / "index.html")


if __name__ == "__main__":
    main()
