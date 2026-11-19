#!/usr/bin/env python3
"""Baut docs/index.html: Lernpfad Flutter-Datenbankanbindung (Gestaltung wie Flutter-Einführung LF11).
Aufruf: python3 seite_bauen.py  – fragt das Lösungs-Passwort (oder LOESUNG_PASSWORT).
Braucht: pillow, cryptography."""
import base64, io, json, os, re, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inhalt import *
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'flutter_einfuehrung', 'tool'))
from lernpfad_bausteine import selbstkontrolle_html  # gleiche Selbstkontrolle wie die Einführung
from woerter_db import WOERTER
import ablauf_grafik
from ablauf_grafik import ablauf_html

HIER = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HIER, 'bilder') + '/'
VORLAGE = open(os.path.join(HIER, 'vorlage_einfuehrung.html'), encoding='utf-8').read()
VERSION = '2.0.5'
DATUM = '17.11.2026'
N = 6

def b64(f, w=900):
    im = Image.open(IMG + f + '.png').convert('RGBA')
    bg = Image.new('RGBA', im.size, 'white')
    im = Image.alpha_composite(bg, im).convert('RGB')
    if im.width > w:
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    if b.tell() > 140000:
        b = io.BytesIO(); im.save(b, 'JPEG', quality=84); m = 'jpeg'
    else:
        m = 'png'
    return f'data:image/{m};base64,' + base64.b64encode(b.getvalue()).decode()

def figur(f, alt, cap, breit=True):
    cls = 'handy breit' if breit else 'handy'
    return (f'<figure class="{cls}"><button class="rahmen" type="button" aria-label="Bild groß anzeigen: {e(cap)}">'
            f'<span class="bild"><img src="{b64(f)}" alt="{e(alt)}" loading="lazy"></span>'
            f'<span class="lupe" aria-hidden="true">🔍</span></button><figcaption>{cap}</figcaption></figure>')

def baum(knoten):
    # knoten: (name, klein, neu, kinder)
    def k(n):
        name, klein, neu, kinder = n
        c = 'knoten widget neu' if neu else 'knoten widget'
        s = f'<span class="{c}"><b>{name}</b>' + (f'<small>{klein}</small>' if klein else '') + \
            ('<em class="neu-marke">neu</em>' if neu else '') + '</span>'
        if kinder:
            s += '<ul>' + ''.join(f'<li>{k(x)}</li>' for x in kinder) + '</ul>'
        return s
    return '<ul class="baum"><li>' + k(knoten) + '</li></ul>'

# ---------------------------------------------------------------- Code-Rahmen (wie Flutter-Einführung)
def _vor(zeichen, code, n):
    return '\n'.join(zeichen + ((' ' * n + z) if z.strip() else '') for z in code.rstrip('\n').split('\n'))
def P(code, n=0): return _vor('+ ', code, n)   # neu eintippen (grün)
def M(code, n=0): return _vor('- ', code, n)   # löschen (rot)
def R(code, n=0): return _vor('  ', code, n)   # steht schon da (grau)
LUECKE = '  …'
def D(*teile): return '\n'.join(teile)

def rahmen(diff):
    if diff.startswith('<pre'):
        return diff
    zeilen = []
    for z in diff.split('\n'):
        art, zeichen = ('neu', '+') if z[:1] == '+' else ('weg', '−') if z[:1] == '-' else ('rahmen', '')
        inhalt = e(z[2:]) if len(z) >= 2 else ''
        zeilen.append(f'<span class="z {art}"><i>{zeichen}</i>{inhalt or "&#8203;"}</span>')
    return '<pre class="rahmen-code"><code>' + ''.join(zeilen) + '</code></pre>'

ARTEN = {'neu': '📄 Neue Datei', 'aendern': '✏️ Ändern', 'loeschen': '🗑️ Löschen', 'terminal': '⌨️ Terminal',
         'browser': '🌐 Browser', 'test': '▶️ Testen', 'pi': '🍓 Raspberry Pi'}
LEGENDE = {False: ('<p class="rahmen-legende"><b>So lesen Sie die Code-Kästen:</b> <span class="lg rahmen">grau</span> steht schon in Ihrer Datei – nur zur Orientierung, wo Sie sind · '
                   '<span class="lg neu">+ grün</span> neu eintippen · <span class="lg weg">− rot</span> löschen · <span class="lg rahmen">…</span> unveränderter Code dazwischen</p>'),
           True: ('<p class="rahmen-legende"><b>So liest du die Code-Kästen:</b> <span class="lg rahmen">grau</span> steht schon in deiner Datei · '
                  '<span class="lg neu">+ grün</span> neu eintippen · <span class="lg weg">− rot</span> löschen · <span class="lg rahmen">…</span> hier ändert sich nichts</p>')}

def auftrag_html(d, einfach):
    schritte = ''.join(f'<li><b>{ARTEN[art]}</b> {text}' + (rahmen(diff) if diff else '') + '</li>' for art, text, diff in d['schritte'])
    profi = ''.join(f'<li>{t}</li>' for t in d['profi'])
    tipps = ''.join(d['tipps'])
    du = einfach
    return (f'<p><strong>Ziel:</strong> {d["ziel"]}</p>\n'
            f'<p><strong>{"Du änderst" if du else "Sie ändern"}:</strong> {d["aendern"]} · <strong>Skript:</strong> {d["skript"]}</p>\n'
            f'<div class="auftrags-kasten nur-begleitet"><h3>Auftrag</h3>{LEGENDE[du]}<ol>{schritte}</ol></div>\n'
            f'<div class="auftrags-kasten profi-kasten nur-profi"><h3>Profi-Auftrag</h3>'
            f'<p>{"Das muss deine App danach können:" if du else "Anforderungen – den Weg wählen Sie selbst:"}</p><ul>{profi}</ul>'
            f'<p class="klein">{"Hilfe: Schalte oben auf 🧭 Begleitet. Dort steht jeder Schritt mit Code." if du else "Festhängen? Oben auf 🧭 Begleitet umschalten – dort steht jeder Schritt mit Code-Rahmen."}</p></div>\n'
            + (f'<div class="tipps"><h3>💡 Tipps, falls es hakt</h3>{tipps}</div>' if tipps else ''))

def woerter_html(liste):
    return ''.join(f'<dt>{e(w)}</dt><dd>{e(WOERTER[w])}</dd>' for w in liste)

def level(nr, titel, stich, ziel, grafik, weiter, S, E, sk, ske, woerter):
    zur = '<a class="knopf" href="#start">◀ Start</a>' if nr == 1 else f'<a class="knopf" href="#level-{nr-1}">◀ Level {nr-1}</a>'
    vor = f'<a class="knopf primaer" href="#{weiter[0]}">{weiter[1]} ▶</a>'
    erkl = lambda d: f'<div class="erklaert"><h3>Erklärt – was passiert hier?</h3>{d["erklaert"]}</div>'
    return f"""<section class="ansicht level" id="level-{nr}" data-level="{nr}">
  <div class="card level-kopf">
    <span class="nummer" aria-hidden="true">{nr}</span>
    <div><h2>Level {nr} – {titel}</h2><p class="stich">{stich}</p></div>
  </div>
  <nav class="schritt-reiter" role="tablist" aria-label="Teile von Level {nr}">
    <button type="button" role="tab" data-schritt="ziel">🎯 Ziel</button>
    <button type="button" role="tab" data-schritt="auftrag">🛠️ Auftrag</button>
    <button type="button" role="tab" data-schritt="hintergrund">💡 Hintergrund</button>
    <button type="button" role="tab" data-schritt="pruefen">✅ Prüfen</button>
  </nav>
  <div class="schritt" data-schritt="ziel" role="tabpanel">
    <div class="ziel-raster">{ziel}</div>
    <p class="schritt-weiter"><button type="button" class="knopf primaer" data-geh="auftrag">Weiter: 🛠️ Auftrag ▶</button></p>
  </div>
  <div class="schritt" data-schritt="auftrag" role="tabpanel">
    <div class="card lp-auftrag"><div class="sprache-standard">{auftrag_html(S, False)}</div>
      <div class="sprache-einfach">{auftrag_html(E, True)}
        <div class="woerter"><h3>📖 Wichtige Wörter</h3><dl>{woerter_html(woerter)}</dl></div></div>
      <details class="loesung" data-loesung="{nr}" hidden><summary>🔓 Musterlösung Level {nr}</summary></details>
    </div>
    <p class="schritt-weiter"><button type="button" class="knopf" data-geh="ziel">◀ 🎯 Ziel</button><button type="button" class="knopf primaer" data-geh="hintergrund">Weiter: 💡 Hintergrund ▶</button></p>
  </div>
  <div class="schritt" data-schritt="hintergrund" role="tabpanel">
    <div class="card lp-hintergrund"><div class="sprache-standard">{erkl(S)}</div><div class="sprache-einfach">{erkl(E)}</div></div>
    <div class="card grafik">{grafik}</div>
    <p class="schritt-weiter"><button type="button" class="knopf" data-geh="auftrag">◀ 🛠️ Auftrag</button><button type="button" class="knopf primaer" data-geh="pruefen">Weiter: ✅ Prüfen ▶</button></p>
  </div>
  <div class="schritt" data-schritt="pruefen" role="tabpanel">
  {selbstkontrolle_html('db' + str(nr), sk, ske).replace('data-sk-level="db' + str(nr) + '"', 'data-sk-level="' + str(nr) + '"')}
  </div>
  <div class="card lp-fuss">
    {zur}
    <div class="pruefen"><button class="erledigt" data-level="{nr}" disabled>Level geschafft</button></div>
    {vor}
  </div>
</section>
"""

def ziel(*figs):
    return '<div class="card ziel"><h3>So soll es aussehen</h3><div class="handys">' + ''.join(figs) + '</div></div>'

def baumkarte(titel, b, legende=''):
    return f'<div class="card"><h3>{titel}</h3>\n{b}\n' + (f'<p class="klein">{legende}</p>' if legende else '') + '</div>'

def dateien(liste):
    # liste: [(datei, info, neu)]
    return baum(('meine_app/lib', '', False, [(d, i, n, None) for d, i, n in liste]))

exec(open(os.path.join(HIER, 'level.py'), encoding='utf-8').read())

ZEILEN = ''.join(f'<span class="kh-zeile{" an" if an else ""}"><i></i><b style="width:{w}%"></b><u></u></span>' for an, w in ((1, 62), (0, 48), (1, 70), (0, 40)))
SCHALTER = '''    <div class="schalter-zeile">
    <div class="pfad-wahl" role="group" aria-label="Lernpfad wählen">
      <button type="button" data-modus="begleitet" aria-pressed="true">🧭 Begleitet</button>
      <button type="button" data-modus="profi" aria-pressed="false">🚀 Profi</button>
    </div>
    <div class="pfad-wahl sprach-wahl" role="group" aria-label="Sprache wählen">
      <button type="button" data-sprache="standard" aria-pressed="true">Standard</button>
      <button type="button" data-sprache="einfach" aria-pressed="false">Sprache einfach</button>
    </div>
    <button type="button" class="druck-kopf" data-drucken title="Druckt nur die Wissen-Seite – auch als PDF speichern">🖨️ Drucken</button>
    </div>
'''
LOGO = ('<img class="kopf-logo" alt="BS Info München" width="239" height="160" src="data:image/png;base64,'
        + base64.b64encode(open(os.path.join(HIER, '..', 'logo-bsinfo.png'), 'rb').read()).decode() + '">')
KOPF = f'''<header class="card kopf">
    <figure class="kopf-handy" aria-hidden="true"><span class="kh-kerbe"></span><span class="kh-app"><span class="kh-leiste">ToDo Liste</span>{ZEILEN}<span class="kh-plus">+</span></span><span class="kh-db">🗄️</span></figure>
    {LOGO}
    <div class="titel">
      <h1>Flutter-Datenbankanbindung <span class="version">LF11 · Version {VERSION}</span></h1>
      <div class="unter">In 6 Leveln von der lokalen App zur Datenbank: erst die Login-Maske, dann die ToDo-Liste.</div>
    </div>
    <nav class="fortschritt" aria-label="Level"><a class="chip" href="#start" data-ziel="start">Start</a>''' + ''.join(
    f'<a class="chip" href="#level-{i}" data-ziel="level-{i}">{i}</a>' for i in range(1, N + 1)) + \
    '<a class="chip" href="#wissen" data-ziel="wissen" title="Wissen: REST, JSON und async">📘 Wissen</a><a class="chip" href="#loesungen" data-ziel="loesungen" title="Musterlösungen">🔒</a>' \
    f'<span class="chip zaehler" id="zaehler">0 / {N}</span></nav>\n' + SCHALTER + '  </header>\n'

LOES = '''<section class="ansicht" id="loesungen">
    <div class="card"><h2>🔒 Musterlösungen</h2>
      <p>Die Lösungen sind verschlüsselt. Mit dem Passwort Ihrer Lehrkraft erscheinen sie in jedem Level
      unten im Auftrag unter <i>Musterlösung</i>. Erst selbst probieren – Fehlermeldungen lesen und die Tipps nutzen bringt mehr als jede Lösung!</p>
      <form id="entsperren" class="pruefen">
        <label for="pw" class="sr">Passwort</label>
        <input id="pw" type="password" autocomplete="off" placeholder="Passwort"
          style="font:inherit;padding:8px 12px;border-radius:12px;border:1px solid var(--line);min-height:42px">
        <button class="primaer" type="submit">Lösungen anzeigen</button>
        <span id="pw-status" role="status"></span>
      </form></div>
  </section>
''' + f'''  <footer class="druckfuss"><small>Flutter-Datenbankanbindung LF11 · Version {VERSION} vom {DATUM} · BS Info · Grafiken aus dem Skript „Flutter – Datenbankanbindung“ · Ihr Fortschritt auf dieser Seite wird nur in Ihrem Browser gespeichert.</small></footer>
</div>
<dialog id="gross" aria-label="Großansicht"><div class="gross-inhalt"></div>
  <form method="dialog"><button class="primaer">Schließen</button></form></dialog>
'''

EXTRA_CSS = '''<style>
.handy.breit{max-width:100%;flex:1 1 100%}
.handy.breit .rahmen{background:#fff;border:1px solid var(--line);border-radius:12px;padding:6px}
.handy.breit .rahmen:hover{background:#fff}
.handy.breit img{width:100%;height:auto;display:block;border-radius:8px}
.kh-db{position:absolute;right:-12px;bottom:-8px;font-size:22px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.4))}
.handy:not(.breit) img{width:100%;height:auto;display:block;border-radius:14px}
''' + ablauf_grafik.CSS + '''</style>
'''

def verschluesseln(pw, daten):
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes, padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    salt, iv, it = os.urandom(16), os.urandom(16), 600000
    key = PBKDF2HMAC(hashes.SHA256(), 32, salt, it).derive(pw.encode())
    klar = ('LOESUNG-OK\n' + json.dumps(daten, ensure_ascii=False)).encode()
    p = padding.PKCS7(128).padder(); klar = p.update(klar) + p.finalize()
    enc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    ct = enc.update(klar) + enc.finalize()
    b = lambda x: base64.b64encode(x).decode()
    return {'salt': b(salt), 'iv': b(iv), 'iter': it, 'daten': b(ct)}

def bauen(pw, ziel):
    v = VORLAGE
    head_end = v.index('<body')
    head = v[:head_end]
    head = re.sub(r'<title>.*?</title>', '<title>Flutter-Datenbankanbindung LF11</title>', head, flags=re.S)
    head = re.sub(r'<meta name="version" content="[^"]*">', f'<meta name="version" content="{VERSION}">', head)
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="In 6 Leveln Login-Maske und ToDo-Liste einer Flutter-App an eine Datenbank mit REST-API anbinden.">', head)
    head = head.replace('</head>', EXTRA_CSS + '</head>')
    i1 = v.index('<script>var LP_KEY')
    i_bauk = v.index('<script>/* Interaktive Baukästen')
    i_geh = v.index('<script>var GEHEIM')
    s_nav_sk = v[i1:i_bauk]
    s_nav_sk = s_nav_sk.replace('"flutter-lernpfad-lf11"', '"flutter-lernpfad-lf11-datenbank"').replace('n + " / 9"', f'n + " / {N}"')
    assert s_nav_sk.count('flutter-lernpfad-lf11-datenbank') == 2 and f'" / {N}"' in s_nav_sk
    i_begr = v.index('<script>var BEGRIFFE')
    s_begr = v[i_begr:i_geh]
    s_begr = re.sub(r'var BEGRIFFE = \{.*?\};', lambda m: 'var BEGRIFFE = ' + json.dumps(WOERTER, ensure_ascii=False) + ';', s_begr, count=1, flags=re.S)
    s_geh = v[i_geh:]
    s_geh = re.sub(r'var GEHEIM = \{.*?\};', 'var GEHEIM = ' + json.dumps(verschluesseln(pw, LOESUNGEN)) + ';', s_geh, count=1, flags=re.S)
    body = ('<body data-thema="technik">\n<div class="app">\n  ' + KOPF + START + ''.join(L) + WISSEN + LOES)
    out = head + body + '<script>' + ablauf_grafik.JS + '</script>' + s_nav_sk + s_begr + s_geh
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    open(ziel, 'w', encoding='utf-8').write(out)
    return out

if __name__ == '__main__':
    import getpass
    pw = os.environ.get('LOESUNG_PASSWORT', '')
    if not pw:
        pw = getpass.getpass('Passwort für die Lösungen (wie in der Flutter-Einführung): ')
        if pw != getpass.getpass('Passwort wiederholen: '):
            sys.exit('Die Passwörter stimmen nicht überein – abgebrochen.')
    if len(pw) < 10:
        sys.exit('Bitte mindestens 10 Zeichen.')
    ziel = os.path.join(HIER, 'docs', 'index.html')
    out = bauen(pw, ziel)
    print('Erstellt:', ziel, len(out) // 1024, 'KB')
