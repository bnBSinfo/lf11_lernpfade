#!/usr/bin/env python3
"""Baut docs/index.html: Lernpfad Flutter-Datenbankanbindung (Gestaltung wie Flutter-Einführung LF11).
Aufruf: python3 seite_bauen.py  – fragt das Lösungs-Passwort (oder LOESUNG_PASSWORT).
Braucht: pillow, cryptography."""
import base64, io, json, os, re, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inhalt import *

HIER = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HIER, 'bilder') + '/'
VORLAGE = open(os.path.join(HIER, 'vorlage_einfuehrung.html'), encoding='utf-8').read()
VERSION = '1.0.0'
DATUM = '14.11.2026'
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

def selbst(nr, checks, fragen):
    c = ''.join(f'<li><label><input type="checkbox" data-sk="db{nr}-c{i}"> {t}</label></li>' for i, t in enumerate(checks))
    q = ''
    for i, (frage, opts) in enumerate(fragen):
        o = ''.join(f'<li><label><input type="radio" name="sk-db{nr}-{i}" value="{j}" data-richtig="{1 if ok else 0}" '
                    f'data-feedback="{e(fb)}"> {t}</label></li>' for j, (t, ok, fb) in enumerate(opts))
        q += (f'<div class="sk-frage" data-sk-frage="db{nr}-{i}"><p><b>{i+1}.</b> {frage}</p>'
              f'<ul class="sk-optionen">{o}</ul><p class="sk-feedback" role="status"></p></div>')
    return (f'<div class="card selbstkontrolle" data-sk-level="{nr}">\n  <h3>✅ Selbstkontrolle</h3>\n'
            '  <p class="klein">Haken Sie nur ab, was bei Ihnen <b>wirklich</b> funktioniert. Beantworten Sie dann die Kontrollfragen –\n'
            '  sind alle Haken gesetzt und alle Fragen richtig, ist das Level geschafft.</p>\n'
            f'  <h4>Das muss jetzt funktionieren</h4><ul class="sk-liste">{c}</ul>\n  <h4>Kontrollfragen</h4>{q}\n</div>')

def level(nr, titel, stich, auftrag, rechts, grafik, sk, weiter):
    zur = '<a class="knopf" href="#start">◀ Start</a>' if nr == 1 else f'<a class="knopf" href="#level-{nr-1}">◀ Level {nr-1}</a>'
    vor = f'<a class="knopf primaer" href="#{weiter[0]}">{weiter[1]} ▶</a>'
    return f'''<section class="ansicht level" id="level-{nr}" data-level="{nr}">
  <div class="card level-kopf">
    <span class="nummer" aria-hidden="true">{nr}</span>
    <div><h2>Level {nr} – {titel}</h2><p class="stich">{stich}</p></div>
  </div>
  <div class="level-raster">
    <div class="card lp-auftrag">{auftrag}
      <details class="loesung" data-loesung="{nr}" hidden><summary>🔓 Musterlösung Level {nr}</summary></details>
    </div>
    <aside class="lp-seite">{rechts}</aside>
  </div>
  <div class="card grafik">{grafik}</div>
  {sk}
  <div class="card lp-fuss">
    {zur}
    <div class="pruefen"><button class="erledigt" data-level="{nr}" disabled>Level geschafft</button></div>
    {vor}
  </div>
</section>
'''

def ziel(*figs):
    return '<div class="card ziel"><h3>So soll es aussehen</h3><div class="handys">' + ''.join(figs) + '</div></div>'

def baumkarte(titel, b, legende=''):
    return f'<div class="card"><h3>{titel}</h3>\n{b}\n' + (f'<p class="klein">{legende}</p>' if legende else '') + '</div>'

def dateien(liste):
    # liste: [(datei, info, neu)]
    return baum(('meine_app/lib', '', False, [(d, i, n, None) for d, i, n in liste]))

def auftrag(ziel_txt, aendern, skript, schritte, rest):
    li = ''.join(f'<li>{s}</li>' for s in schritte)
    return (f'<p><strong>Ziel:</strong> {ziel_txt}</p>\n<p><strong>Sie ändern:</strong> {aendern} · <strong>Skript:</strong> {skript}</p>\n'
            f'<div class="auftrags-kasten"><h3>Auftrag</h3>\n<ol type="1">{li}</ol>\n</div>{rest}')

exec(open(os.path.join(HIER, 'level.py'), encoding='utf-8').read())

KOPF = f'''<header class="card kopf">
    <div class="titel">
      <h1>Flutter-Datenbankanbindung <span class="version">LF11 · Version {VERSION}</span></h1>
      <div class="unter">In 6 Leveln von der lokalen App zur Datenbank: erst die Login-Maske, dann die ToDo-Liste.</div>
    </div>
    <nav class="fortschritt" aria-label="Level"><a class="chip" href="#start" data-ziel="start">Start</a>''' + ''.join(
    f'<a class="chip" href="#level-{i}" data-ziel="level-{i}">{i}</a>' for i in range(1, N + 1)) + \
    '<a class="chip" href="#wissen" data-ziel="wissen" title="Wissen: REST, JSON und async">📘 Wissen</a><a class="chip" href="#loesungen" data-ziel="loesungen" title="Musterlösungen">🔒</a>' \
    f'<span class="chip zaehler" id="zaehler">0 / {N}</span></nav>\n  </header>\n'

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
.lp-seite .handys{flex-direction:column;align-items:stretch}
.handy:not(.breit) img{width:100%;height:auto;display:block;border-radius:14px}
</style>
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
    s_geh = v[i_geh:]
    s_geh = re.sub(r'var GEHEIM = \{.*?\};', 'var GEHEIM = ' + json.dumps(verschluesseln(pw, LOESUNGEN)) + ';', s_geh, count=1, flags=re.S)
    body = ('<body data-thema="technik">\n<div class="app">\n  ' + KOPF + START + ''.join(L) + WISSEN + LOES)
    out = head + body + s_nav_sk + s_geh
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
