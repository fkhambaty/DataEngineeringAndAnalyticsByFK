/*
  Meridian deck engine, shared by every episode (same behaviour as Episode 1).

  Page contract
    <body data-episode="e2" data-label="Episode 2"
          data-chapters="Name A|Name B" data-chapter-colors="#a78bfa|#2dd4bf">
    <div id="stage"> <section class="s" data-ch="0" data-steps="2" data-accent="#a,#b" data-notes="…" data-scene="name">…</section> </div>
    <script src="deck/logos.js"></script><script src="deck/deck.js"></script>
    <script>Deck.scene("name", (slide, step, entering, api) => { … });</script>

  Declarative behaviour (all replay when the slide or step is revisited)
    data-at="n"        visible from step n; gets .now on step n and .was after it
    data-until="n"     hidden from step n onwards (.off)
    data-logo="pg"     fills the element with an inline logo or icon (see logos.js)
    data-logo3d="sf"   extruded, rotating 3D logo
    data-orbit="a,b"   tools orbiting a core; data-core="pg" data-core-class="sf"
    data-to="5000000"  count up when visible (data-dec, data-pre, data-suf, data-ms)
    data-term          terminal: .typed[data-type] lines are typed, .out lines appear in order
    data-words         headline words fly in one by one
    data-go            receives .go when visible (bars, meters, planes)
    data-seq="520"     children .seq light up one after another (.lit then .done); data-bar="#id"
    data-typein        .in[data-val] fields are typed one after another
    data-rows="110"    child .rr rows slide in one after another
    data-ticker        number grows by data-step every data-every ms (data-from)
*/
(function(){
  const Deck = { scenes: {}, scene(name, fn){ this.scenes[name] = fn; } };
  window.Deck = Deck;

  const embedded = window.parent !== window;
  const presenter = new URLSearchParams(location.search).get("presenter") === "1";
  const fmt = (n, dec = 0) => Number(n).toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
  let slides = [], si = 0, step = 0, sceneTimers = [];

  function later(owner, fn, ms){ (owner._t = owner._t || []).push(setTimeout(fn, ms)); }
  function stopTimers(owner){ (owner._t || []).forEach(clearTimeout); owner._t = []; cancelAnimationFrame(owner._raf); }

  function countUp(el, to, ms = 1600, dec = 0, pre = "", suf = ""){
    cancelAnimationFrame(el._raf);
    const t0 = performance.now();
    (function f(t){ const p = Math.min((t - t0) / ms, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = pre + fmt(to * e, dec) + suf; if (p < 1) el._raf = requestAnimationFrame(f); })(t0);
  }

  /* ---------- declarative animations ---------- */
  const autos = [
    { sel: "[data-to]",
      play(el){ countUp(el, +el.dataset.to, +(el.dataset.ms || 1700), +(el.dataset.dec || 0), el.dataset.pre || "", el.dataset.suf || ""); },
      reset(el){ el.textContent = (el.dataset.pre || "") + fmt(+(el.dataset.from || 0), +(el.dataset.dec || 0)) + (el.dataset.suf || ""); } },
    { sel: "[data-term]",
      play(el){
        const rows = [...(el.querySelector(".body") || el).children];
        let delay = 300;
        rows.forEach(row => {
          const typed = row.classList.contains("typed") ? row : row.querySelector(".typed");
          if (row.classList.contains("out")){ later(el, () => row.classList.add("show"), delay); delay += typed ? 150 : +(row.dataset.wait || 240); }
          if (!typed) return;
          const text = typed.dataset.type;
          later(el, () => { const c = el.querySelector(".caret"); if (c) typed.after(c); }, delay);
          [...text].forEach((ch, n) => later(el, () => { typed.textContent = text.slice(0, n + 1); }, delay + n * 38));
          delay += text.length * 38 + 380;
        });
      },
      reset(el){ el.querySelectorAll(".typed").forEach(t => t.textContent = ""); el.querySelectorAll(".out").forEach(o => o.classList.remove("show"));
        const c = el.querySelector(".caret"), first = el.querySelector(".typed"); if (c && first) first.after(c); } },
    { sel: "[data-words],[data-go]", play(el){ el.classList.add("go"); }, reset(el){ el.classList.remove("go"); } },
    { sel: "[data-seq]",
      play(el){
        const items = [...el.querySelectorAll(".seq")], ms = +el.dataset.seq || 520, bar = el.dataset.bar && document.querySelector(el.dataset.bar);
        items.forEach((f, n) => later(el, () => { items.forEach(x => x.classList.remove("lit")); f.classList.add("lit");
          if (n) items[n - 1].classList.add("done"); if (bar) bar.style.width = ((n + 1) / items.length * 100) + "%"; }, 200 + n * ms));
        later(el, () => { items.forEach(f => { f.classList.remove("lit"); f.classList.add("done"); }); el.classList.add("complete"); }, 200 + items.length * ms);
      },
      reset(el){ el.querySelectorAll(".seq").forEach(f => f.classList.remove("lit", "done")); el.classList.remove("complete");
        const bar = el.dataset.bar && document.querySelector(el.dataset.bar); if (bar) bar.style.width = "0"; } },
    { sel: "[data-typein]",
      play(el){
        const ins = [...el.querySelectorAll(".in[data-val]")]; let delay = 400;
        ins.forEach(i => { const v = i.dataset.val;
          later(el, () => { ins.forEach(x => x.classList.remove("focus")); i.classList.add("focus"); }, delay);
          [...v].forEach((c, n) => later(el, () => { i.textContent = v.slice(0, n + 1); }, delay + 60 + n * 50));
          delay += 240 + v.length * 50; });
        later(el, () => ins.forEach(x => x.classList.remove("focus")), delay);
      },
      reset(el){ el.querySelectorAll(".in[data-val]").forEach(i => { i.textContent = ""; i.classList.remove("focus"); }); } },
    { sel: "[data-rows]",
      play(el){ const ms = +el.dataset.rows || 110; el.querySelectorAll(".rr").forEach((r, n) => later(el, () => r.classList.add("show"), 150 + n * ms)); },
      reset(el){ el.querySelectorAll(".rr").forEach(r => r.classList.remove("show")); } },
    { sel: "[data-ticker]",
      play(el){ let v = +el.dataset.from; const tick = () => { v += +el.dataset.step; el.textContent = fmt(v); later(el, tick, +el.dataset.every || 2000); };
        el.textContent = fmt(v); later(el, tick, 1200); },
      reset(el){ el.textContent = fmt(+el.dataset.from); } },
  ];

  function shown(el, s){
    if (!s.classList.contains("active")) return false;
    for (let n = el; n && n !== s; n = n.parentElement){
      if (n.hasAttribute("data-at") && !n.classList.contains("on")) return false;
      if (n.hasAttribute("data-until") && n.classList.contains("off")) return false;
    }
    return true;
  }
  function syncAutos(){
    slides.forEach(s => autos.forEach(a => s.querySelectorAll(a.sel).forEach(el => {
      const vis = shown(el, s);
      const key = "_on" + a.sel;
      if (vis && !el[key]){ el[key] = true; a.play(el); }
      else if (!vis && el[key]){ el[key] = false; stopTimers(el); a.reset(el); }
    })));
  }

  /* ---------- logos ---------- */
  function hexToRgb(h){ h = h.replace("#", ""); if (h.length === 3) h = [...h].map(c => c + c).join(""); const n = parseInt(h, 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
  function build3d(host){
    const key = host.dataset.logo3d, depth = +(host.dataset.depth || 26);
    if (key === "pg"){
      const vb = 'viewBox="-20 -20 472 486"';
      for (let n = depth; n >= 1; n--){
        const t = 1 - n / depth, c = `rgb(${Math.round(10 + 22*t)},${Math.round(24 + 44*t)},${Math.round(52 + 70*t)})`;
        const layer = document.createElement("div"); layer.className = "layer"; layer.style.transform = `translateZ(${-n * 1.5}px)`;
        layer.innerHTML = `<svg ${vb}><path d="${PG_OFFICIAL.sil}" fill="${c}" stroke="${c}" stroke-width="37.4"/></svg>`; host.appendChild(layer);
      }
      const face = document.createElement("div"); face.className = "layer face";
      face.innerHTML = `<svg ${vb}><defs><linearGradient id="pgbody" x1="0" y1="0" x2=".9" y2="1"><stop offset="0" stop-color="#6fa0e6"/><stop offset=".5" stop-color="#336791"/><stop offset="1" stop-color="#1f4470"/></linearGradient></defs><g style="fill:none;stroke:#FFFFFF;stroke-width:12.4651;stroke-linecap:round;stroke-linejoin:round">${PG_OFFICIAL.front}</g></svg>`;
      host.appendChild(face); return;
    }
    const src = LOGO[key], tmp = document.createElement("div"); tmp.innerHTML = src;
    const svg = tmp.querySelector("svg"), vb = svg.getAttribute("viewBox") || "0 0 24 24";
    const color = host.dataset.color || svg.getAttribute("fill") || "#7dd3fc";
    const [r, g, b] = hexToRgb(color.startsWith("#") ? color : "#7dd3fc");
    const inner = svg.innerHTML;
    for (let n = depth; n >= 1; n--){
      const t = 1 - n / depth, mix = (v, base) => Math.round(base + (v * .55 - base) * t);
      const c = `rgb(${mix(r, 8)},${mix(g, 14)},${mix(b, 30)})`;
      const layer = document.createElement("div"); layer.className = "layer"; layer.style.transform = `translateZ(${-n * 1.4}px)`;
      layer.innerHTML = `<svg viewBox="${vb}" fill="${c}" stroke="${c}" stroke-width=".35">${inner.replace(/fill="[^"]*"/g, "")}</svg>`; host.appendChild(layer);
    }
    const face = document.createElement("div"); face.className = "layer face";
    face.style.filter = `drop-shadow(0 0 26px rgba(${r},${g},${b},.6))`;
    face.innerHTML = src; host.appendChild(face);
    const halo = host.parentElement.querySelector(".halo");
    if (halo) halo.style.background = `radial-gradient(circle, rgba(${r},${g},${b},.45), transparent 62%)`;
  }
  function buildOrbit(host){
    const keys = host.dataset.orbit.split(","), sats = [];
    host.insertAdjacentHTML("afterbegin", `<div class="ring r1"></div><div class="ring r2"></div><div class="core ${host.dataset.coreClass || ""}">${host.dataset.core ? LOGO[host.dataset.core].replace(/fill="#[0-9A-Fa-f]+"/, 'fill="#ffffff"') : ""}</div>`);
    keys.forEach(k => { const d = document.createElement("div"); d.className = "sat"; d.innerHTML = `<div class="tile">${LOGO[k]}</div>`; host.appendChild(d); sats.push(d); });
    const t0 = performance.now(), rx = +(host.dataset.rx || 270), ry = +(host.dataset.ry || 80);
    (function f(t){
      const a0 = (t - t0) / 9000 * Math.PI * 2;
      sats.forEach((d, i) => { const a = a0 + i / sats.length * Math.PI * 2, z = Math.sin(a);
        d.style.transform = `translate(${Math.cos(a) * rx}px, ${z * ry}px) scale(${0.72 + 0.32 * (z + 1) / 2})`;
        d.style.zIndex = z > 0 ? 3 : 1; d.style.opacity = 0.55 + 0.45 * (z + 1) / 2; });
      requestAnimationFrame(f);
    })(t0);
  }

  /* ---------- chrome ---------- */
  function buildChrome(){
    const body = document.body, stage = document.getElementById("stage");
    const vp = document.createElement("div"); vp.id = "viewport"; stage.parentNode.insertBefore(vp, stage); vp.appendChild(stage);
    body.insertAdjacentHTML("afterbegin", '<div class="bg"><i class="orb o1"></i><i class="orb o2"></i><i class="grid"></i></div><canvas id="fx"></canvas>');
    const names = (body.dataset.chapters || "").split("|").filter(Boolean), cols = (body.dataset.chapterColors || "").split("|");
    let ch = `<div class="chapters"><span class="ep"><i></i>${body.dataset.label || ""}</span>`;
    names.forEach((n, i) => { ch += `<span class="sep"></span><span class="c" data-c="${i}" style="--chap:${cols[i] || "#2dd4bf"}">${n}</span>`; });
    stage.insertAdjacentHTML("afterbegin", ch + '</div><div class="count" id="count"></div><div class="progress"><i id="prog"></i></div>');
    body.insertAdjacentHTML("beforeend", '<div id="notes"></div><div class="nav"><button id="bk" aria-label="Back">←</button><button id="fw" aria-label="Next">→</button></div>');
  }
  function ambient(){
    const c = document.getElementById("fx"), x = c.getContext("2d"), dpr = Math.min(devicePixelRatio || 1, 2), dots = [];
    function size(){ c.width = innerWidth * dpr; c.height = innerHeight * dpr; c.style.width = innerWidth + "px"; c.style.height = innerHeight + "px"; x.setTransform(dpr,0,0,dpr,0,0); }
    size(); addEventListener("resize", size);
    for (let i = 0; i < 60; i++) dots.push({x:Math.random()*innerWidth, y:Math.random()*innerHeight, vx:(Math.random()-.5)*.2, vy:(Math.random()-.5)*.2, r:.8+Math.random()*1.6, a:.12+Math.random()*.3});
    (function draw(){ x.clearRect(0,0,innerWidth,innerHeight);
      dots.forEach((d,i) => { d.x += d.vx; d.y += d.vy; if (d.x < 0 || d.x > innerWidth) d.vx *= -1; if (d.y < 0 || d.y > innerHeight) d.vy *= -1;
        x.fillStyle = `rgba(190,225,255,${d.a})`; x.beginPath(); x.arc(d.x,d.y,d.r,0,7); x.fill();
        for (let j = i + 1; j < dots.length; j++){ const q = dots[j], dist = Math.hypot(d.x-q.x, d.y-q.y);
          if (dist < 140){ x.strokeStyle = `rgba(125,211,252,${(1-dist/140)*.12})`; x.beginPath(); x.moveTo(d.x,d.y); x.lineTo(q.x,q.y); x.stroke(); } } });
      requestAnimationFrame(draw); })();
  }

  /* ---------- render ---------- */
  const api = {
    later(fn, ms){ sceneTimers.push(setTimeout(fn, ms)); },
    countUp, fmt,
  };
  function render(entering){
    sceneTimers.forEach(clearTimeout); sceneTimers = [];
    const s = slides[si];
    slides.forEach((x, n) => { x.classList.toggle("active", n === si); x.classList.toggle("past", n < si); });
    s.querySelectorAll("[data-at]").forEach(el => { const a = +el.dataset.at;
      el.classList.toggle("on", a <= step); el.classList.toggle("now", a === step); el.classList.toggle("was", a < step); });
    s.querySelectorAll("[data-until]").forEach(el => el.classList.toggle("off", +el.dataset.until <= step));
    s.querySelectorAll(".steps").forEach(st => { const w = st.querySelector(".wire"); if (!w) return;
      const items = [...st.querySelectorAll(".st")], lit = items.filter(i => !i.hasAttribute("data-at") || i.classList.contains("on")).length;
      w.style.width = lit <= 1 ? "0" : ((lit - 1) / Math.max(items.length - 1, 1) * 88) + "%"; });
    const fn = Deck.scenes[s.dataset.scene];
    if (fn) fn(s, step, entering, api);
    syncAutos();
    const [a, b] = (s.dataset.accent || "#1f8a9b,#5b4bb5").split(",");
    document.documentElement.style.setProperty("--accent-a", a); document.documentElement.style.setProperty("--accent-b", b);
    document.querySelectorAll(".chapters .c").forEach(c => c.classList.toggle("on", c.dataset.c === s.dataset.ch));
    document.getElementById("count").textContent = String(si + 1).padStart(2, "0") + " / " + String(slides.length).padStart(2, "0");
    const total = slides.reduce((n, x) => n + 1 + +(x.dataset.steps || 0), 0);
    const done = slides.slice(0, si).reduce((n, x) => n + 1 + +(x.dataset.steps || 0), 0) + step + 1;
    document.getElementById("prog").style.width = (done / total * 100) + "%";
    document.getElementById("notes").textContent = s.dataset.notes || "";
    history.replaceState(null, "", "#" + (si + 1) + (step ? "." + step : ""));
  }
  function next(){
    const steps = +(slides[si].dataset.steps || 0);
    if (step < steps){ step++; render(false); return; }
    if (si < slides.length - 1){ si++; step = 0; render(true); return; }
    if (embedded) parent.postMessage({type:"meridian-complete", section:"technical", episode:document.body.dataset.episode}, "*");
  }
  function prev(){
    if (step > 0){ step--; render(false); return; }
    if (si > 0){ si--; step = +(slides[si].dataset.steps || 0); render(true); }
  }

  function copy(text, btn){
    const done = () => { btn.textContent = "Copied ✓"; btn.classList.add("done"); setTimeout(() => { btn.textContent = "Copy"; btn.classList.remove("done"); }, 1400); };
    const fallback = () => { const t = document.createElement("textarea"); t.value = text; document.body.appendChild(t); t.select(); document.execCommand("copy"); t.remove(); done(); };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback); else fallback();
  }

  function init(){
    buildChrome();
    slides = [...document.querySelectorAll(".s")];
    document.querySelectorAll("[data-logo]").forEach(el => { el.innerHTML = LOGO[el.dataset.logo] || ""; });
    document.querySelectorAll("[data-logo3d]").forEach(build3d);
    document.querySelectorAll("[data-orbit]").forEach(buildOrbit);
    document.querySelectorAll("[data-words]").forEach(el => {
      let i = 0;
      const walk = node => [...node.childNodes].forEach(n => {
        if (n.nodeType === 3){
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)){ frag.appendChild(document.createTextNode(part)); return; }
            const w = document.createElement("span"); w.className = "w"; w.style.setProperty("--i", i++); w.textContent = part; frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== "BR"){
          if (/grad/.test(n.className)){ n.classList.add("w"); n.style.setProperty("--i", i++); } else walk(n);
        }
      });
      walk(el);
    });
    document.querySelectorAll(".edge").forEach(p => p.style.setProperty("--len", Math.ceil(p.getTotalLength()) + 20));
    document.querySelectorAll(".copy").forEach(b => b.addEventListener("click", ev => {
      ev.stopPropagation();
      const host = b.closest(".cmd") || b.parentElement;
      copy(b.dataset.copy || (host.querySelector("code,pre") || host).textContent.trim(), b);
    }));
    slides.forEach(s => autos.forEach(a => s.querySelectorAll(a.sel).forEach(el => a.reset(el))));

    addEventListener("keydown", e => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const k = e.key;
      if (["ArrowRight","PageDown"," ","Enter"].includes(k)){ e.preventDefault(); next(); }
      else if (["ArrowLeft","PageUp","Backspace"].includes(k)){ e.preventDefault(); prev(); }
      else if ((k === "n" || k === "N") && presenter) document.body.classList.toggle("notes");
      else if (k === "c" || k === "C") document.body.classList.toggle("clean");
      else if (k === "f" || k === "F"){ document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
      else if (k === "Escape" && embedded) parent.postMessage({type:"meridian-home"}, "*");
    });
    document.getElementById("fw").onclick = next;
    document.getElementById("bk").onclick = prev;
    let mouseT;
    addEventListener("mousemove", () => { document.body.classList.add("mouse"); clearTimeout(mouseT); mouseT = setTimeout(() => document.body.classList.remove("mouse"), 1800); });
    addEventListener("click", () => window.focus());
    const fit = () => document.documentElement.style.setProperty("--k", Math.min(innerWidth/1600, innerHeight/900));
    addEventListener("resize", fit); fit();
    ambient();

    const m = location.hash.match(/^#(\d+)(?:\.(\d+))?/);
    if (m){ si = Math.min(Math.max(+m[1] - 1, 0), slides.length - 1); step = Math.min(+(m[2] || 0), +(slides[si].dataset.steps || 0)); }
    render(true);
    window.focus();
  }
  document.addEventListener("DOMContentLoaded", init);
})();
