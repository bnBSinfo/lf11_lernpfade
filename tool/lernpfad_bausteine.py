"""Gemeinsame Bausteine der Lernpfade (Flutter-Einführung, Pi-Server & REST-API).

- Selbstkontrolle je Level: Checkliste + Kontrollfragen mit Feedback (ersetzt automatische Tests)
- Kopierschutz für Code: Code wird abgetippt, nicht kopiert
- Eigenständige Seite: Stylesheet und Bilder werden eingebettet (für mebis)

Datenformat der Selbstkontrolle:
    {nr: {"check": ["…", …], "fragen": [("Frage", [("Antwort", richtig?, "Feedback"), …]), …]}}
"""
import base64
import html
import mimetypes
import pathlib
import re

e = html.escape


def selbstkontrolle_html(nr: int, daten: dict) -> str:
    checks = "".join(
        f'<li><label><input type="checkbox" data-sk="{nr}-c{i}"> {inline_code(t)}</label></li>'
        for i, t in enumerate(daten["check"]))
    fragen = []
    for i, (frage, antworten) in enumerate(daten["fragen"]):
        opts = "".join(
            f'<li><label><input type="radio" name="sk-{nr}-{i}" value="{j}" data-richtig="{1 if ok else 0}" '
            f'data-feedback="{e(fb)}"> {inline_code(a)}</label></li>'
            for j, (a, ok, fb) in enumerate(antworten))
        fragen.append(f'<div class="sk-frage" data-sk-frage="{nr}-{i}"><p><b>{i + 1}.</b> {inline_code(frage)}</p>'
                      f'<ul class="sk-optionen">{opts}</ul><p class="sk-feedback" role="status"></p></div>')
    return f"""<div class="card selbstkontrolle" data-sk-level="{nr}">
  <h3>✅ Selbstkontrolle</h3>
  <p class="klein">Haken Sie nur ab, was bei Ihnen <b>wirklich</b> funktioniert. Beantworten Sie dann die Kontrollfragen –
  sind alle Haken gesetzt und alle Fragen richtig, ist das Level geschafft.</p>
  <h4>Das muss jetzt funktionieren</h4><ul class="sk-liste">{checks}</ul>
  <h4>Kontrollfragen</h4>{"".join(fragen)}
</div>"""


def inline_code(text: str) -> str:
    """`code` → <code>code</code>, sonst escapen."""
    teile = re.split(r"`([^`]+)`", text)
    kursiv = lambda s: re.sub(r"\*([^*]+)\*", r"<i>\1</i>", e(s))
    return "".join(f"<code>{e(t)}</code>" if i % 2 else kursiv(t) for i, t in enumerate(teile))


def einbetten(seite: str, docs: pathlib.Path) -> str:
    """css/stil.css inline, bilder/*.png als data:-URI – die Seite braucht keine weiteren Dateien."""
    stil = docs / "css" / "stil.css"
    if stil.exists():
        def schrift(m):
            pfad = docs / "css" / m.group(1)
            if not pfad.exists():
                return m.group(0)
            return f"url(data:font/woff2;base64,{base64.b64encode(pfad.read_bytes()).decode()})"
        css = re.sub(r"url\((schrift/[^)]+)\)", schrift, stil.read_text(encoding="utf-8"))
        seite = seite.replace('<link rel="stylesheet" href="css/stil.css">', f"<style>{css}</style>")

    def bild(m):
        pfad = docs / m.group(2)
        if not pfad.exists():
            return m.group(0)
        typ = mimetypes.guess_type(pfad.name)[0] or "image/png"
        return f'{m.group(1)}"data:{typ};base64,{base64.b64encode(pfad.read_bytes()).decode()}"'

    return re.sub(r'(src=)"(bilder/[^"]+)"', bild, seite)


CSS = """
.selbstkontrolle h4{margin:.9rem 0 .4rem}
.sk-liste,.sk-optionen{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.sk-liste label,.sk-optionen label{display:flex;gap:10px;align-items:flex-start;padding:8px 12px;border:1px solid var(--line);border-radius:12px;background:#fff;cursor:pointer;line-height:1.35}
.sk-liste input,.sk-optionen input{margin-top:3px;flex:none;width:18px;height:18px;accent-color:var(--accent)}
.sk-liste input:checked+*,.sk-liste label:has(input:checked){background:#e7f6ec;border-color:#9bd3ad}
.sk-frage{margin:0 0 12px}
.sk-frage p{margin:.3rem 0}
.sk-feedback{min-height:1.2em;font-size:.92rem}
.sk-frage.richtig .sk-feedback{color:#166534}
.sk-frage.falsch .sk-feedback{color:#b42318}
.sk-frage.richtig label:has(input:checked){background:#e7f6ec;border-color:#9bd3ad}
.sk-frage.falsch label:has(input:checked){background:#fdecec;border-color:#f3b4b4}
button.erledigt:disabled{opacity:.55;cursor:not-allowed}
.sk-status{font-size:.9rem;color:var(--ink-soft)}
/* Kopierschutz: Code wird abgetippt */
pre,code,.kette,.term,.browser{-webkit-user-select:none;user-select:none}
.kopier-hinweis{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#1a2130;color:#fff;padding:10px 18px;border-radius:12px;box-shadow:0 6px 24px rgba(0,0,0,.25);z-index:50;font-size:.95rem}
"""

JS = r"""
(function(){
  var KEY = (window.LP_KEY || "lernpfad") + "-selbst", stand = {};
  try { stand = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
  function speichern(){ try { localStorage.setItem(KEY, JSON.stringify(stand)); } catch (e) {} }
  function frageAuswerten(div, zeigen){
    var gew = div.querySelector("input:checked"), fb = div.querySelector(".sk-feedback");
    div.classList.remove("richtig", "falsch");
    if (!gew) { fb.textContent = ""; return false; }
    var ok = gew.dataset.richtig === "1";
    if (zeigen !== false) {
      div.classList.add(ok ? "richtig" : "falsch");
      fb.textContent = (ok ? "✓ Richtig. " : "✗ Noch nicht. ") + gew.dataset.feedback;
    }
    return ok;
  }
  function levelPruefen(box){
    var nr = box.dataset.skLevel;
    var checks = box.querySelectorAll(".sk-liste input"), alleChecks = true, alleFragen = true;
    checks.forEach(function(c){ if (!c.checked) alleChecks = false; });
    box.querySelectorAll(".sk-frage").forEach(function(f){ if (!frageAuswerten(f)) alleFragen = false; });
    var fertig = alleChecks && alleFragen;
    var level = box.closest(".level"), knopf = level && level.querySelector("button.erledigt");
    if (knopf) {
      knopf.disabled = !fertig && !level.classList.contains("fertig");
      knopf.title = fertig ? "" : "Erst alle Punkte der Selbstkontrolle erfüllen";
    }
  }
  document.querySelectorAll(".selbstkontrolle").forEach(function(box){
    box.querySelectorAll("input").forEach(function(inp){
      var id = inp.dataset.sk || inp.name;
      var gesp = stand[id];
      if (inp.type === "checkbox") inp.checked = !!gesp;
      else if (gesp !== undefined && String(gesp) === inp.value) inp.checked = true;
      inp.addEventListener("change", function(){
        stand[id] = inp.type === "checkbox" ? inp.checked : inp.value;
        speichern(); levelPruefen(box);
      });
    });
    levelPruefen(box);
  });
  document.addEventListener("click", function(ev){
    if (ev.target.closest("button.erledigt")) setTimeout(function(){
      document.querySelectorAll(".selbstkontrolle").forEach(levelPruefen);
    }, 0);
  });
  // Kopierschutz
  var hinweis;
  function blocken(ev){
    var sel = window.getSelection && window.getSelection();
    var knoten = ev.target.closest ? ev.target : ev.target.parentElement;
    var imCode = (knoten && knoten.closest && knoten.closest("pre,code,.kette,.term,.browser")) ||
      (sel && sel.anchorNode && sel.anchorNode.parentElement && sel.anchorNode.parentElement.closest("pre,code"));
    if (!imCode) return;
    ev.preventDefault();
    if (!hinweis) { hinweis = document.createElement("div"); hinweis.className = "kopier-hinweis"; hinweis.setAttribute("role", "status"); document.body.appendChild(hinweis); }
    hinweis.textContent = "✍️ Bitte abtippen – so lernen Sie den Code wirklich kennen.";
    hinweis.hidden = false;
    clearTimeout(hinweis._t); hinweis._t = setTimeout(function(){ hinweis.hidden = true; }, 2500);
  }
  ["copy", "cut", "contextmenu", "dragstart"].forEach(function(t){ document.addEventListener(t, blocken); });
})();
"""
