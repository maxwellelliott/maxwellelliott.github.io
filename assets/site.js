// Theme switch: system preference by default, the visitor's choice remembered once made.
(function () {
  var root = document.documentElement;
  var system = window.matchMedia("(prefers-color-scheme: dark)");
  var buttons = document.querySelectorAll("[data-theme-toggle]");

  function active() {
    var chosen = root.getAttribute("data-theme");
    return chosen || (system.matches ? "dark" : "light");
  }
  function sync() {
    var theme = active();
    root.setAttribute("data-theme-active", theme);
    buttons.forEach(function (b) {
      b.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
    });
  }
  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      var next = active() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
      sync();
    });
  });
  system.addEventListener("change", sync);
  sync();
})();

// Home: on wide screens the plate follows whichever note is mid-screen.
// On phones the plate sits in the page once, with a two-way toggle instead.
(function () {
  var plate = document.querySelector("[data-plate]");
  var steps = document.querySelectorAll("[data-step]");
  if (!plate || !steps.length) return;

  var zoomed = { scan: 1, cluster: 1, year: 1, pace: 1 };
  var buttons = plate.querySelectorAll("[data-view]");
  var small = window.matchMedia("(max-width: 960px)");
  var current = null;
  var mobileView = "hero";
  var observer = null;

  function show(step) {
    if (step === current) return;
    current = step;
    plate.setAttribute("data-state", step);
    if (zoomed[step]) plate.setAttribute("data-zoom", "");
    else plate.removeAttribute("data-zoom");
  }

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      mobileView = btn.getAttribute("data-view");
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
      show(mobileView);
    });
  });

  function setup() {
    if (observer) { observer.disconnect(); observer = null; }
    if (small.matches) { show(mobileView); return; }
    if (!("IntersectionObserver" in window)) return;
    observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) show(entry.target.getAttribute("data-step"));
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach(function (s) { observer.observe(s); });
  }
  setup();
  small.addEventListener("change", setup);
})();

// Papers page: draw papers-per-year from the list itself, so adding a paper updates it.
(function () {
  var holder = document.querySelector("[data-year-axis]");
  if (!holder) return;
  var groups = Array.prototype.slice.call(document.querySelectorAll("[data-year]"));
  if (!groups.length) return;

  var counts = groups.map(function (g) {
    return { year: +g.getAttribute("data-year"), n: g.querySelectorAll(".paper").length, id: g.id };
  }).sort(function (a, b) { return a.year - b.year; });

  var first = counts[0].year, last = counts[counts.length - 1].year;
  var byYear = {};
  counts.forEach(function (c) { byYear[c.year] = c; });
  var max = Math.max.apply(null, counts.map(function (c) { return c.n; }));

  var W = 960, H = 150, top = 22, base = 118, span = last - first + 1;
  var step = W / span, barW = Math.min(46, step * 0.62);
  var ns = "http://www.w3.org/2000/svg";
  var svg = document.createElementNS(ns, "svg");
  svg.setAttribute("viewBox", "0 0 " + W + " " + H);
  svg.setAttribute("role", "img");
  var total = counts.reduce(function (s, c) { return s + c.n; }, 0);
  svg.setAttribute("aria-label", total + " papers from " + first + " to " + last + ", counted by year");

  function el(name, attrs, text) {
    var e = document.createElementNS(ns, name);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }

  for (var y = first; y <= last; y++) {
    var cx = step * (y - first) + step / 2;
    var c = byYear[y];
    if (c) {
      var h = (base - top) * (c.n / max);
      var a = el("a", { href: "#" + c.id, "class": "bar-link" });
      a.appendChild(el("title", {}, y + ": " + c.n + (c.n === 1 ? " paper" : " papers")));
      a.appendChild(el("rect", { "class": "bar", x: cx - barW / 2, y: base - h, width: barW, height: h }));
      a.appendChild(el("text", { x: cx, y: base - h - 7, "text-anchor": "middle" }, c.n));
      svg.appendChild(a);
    }
    svg.appendChild(el("text", { x: cx, y: base + 24, "text-anchor": "middle", "class": (last - y) % 2 ? "yr yr-alt" : "yr" }, String(y)));
  }
  svg.appendChild(el("line", { "class": "base", x1: 0, y1: base, x2: W, y2: base }));
  holder.appendChild(svg);
})();
