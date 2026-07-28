/* Goodness UI — tiny hash router. No dependencies, no build step. */
(function () {
  "use strict";

  // route key -> { title, src, bleed }
  var ROUTES = {
    "":                 { title: "Home",              src: "pages/hero.html",              bleed: true  },
    "home":             { title: "Home",              src: "pages/hero.html",              bleed: true  },

    "whitepaper":       { title: "White Paper",         src: "system/whitepaper.html",                bleed: true, subnav: "whitepaper" },
    "specimen":         { title: "Specimen",            src: "system/specimen.html",                  bleed: true, subnav: "specimen" },
    "sys-components":   { title: "Components Catalog",  src: "pages/system/components-catalog.html",  bleed: false },
    "sys-agents":       { title: "Agent Manual",        src: "pages/system/agent-manual.html",        bleed: false },
    "sys-enforcement":  { title: "Enforcement",         src: "pages/system/enforcement.html",         bleed: false },
    "sys-about":        { title: "About the System",    src: "pages/system/about.html",               bleed: false },

    "r-deep":           { title: "Deep Analysis",       src: "pages/system/research-deep-analysis.html", bleed: false },
    "r-theme":          { title: "Theme Parity",        src: "pages/system/research-theme-parity.html",  bleed: false },
    "r-brand":          { title: "Brand vs Semantics",  src: "pages/system/research-brand-color.html",   bleed: false },
    "r-forms":          { title: "Record Forms",        src: "pages/system/research-record-forms.html",  bleed: false },
    "r-editing":        { title: "Table Inline Editing",src: "pages/system/research-table-editing.html", bleed: false },
    "r-rowactions":     { title: "Row Actions",         src: "pages/system/research-row-actions.html",   bleed: false },
    "r-enter":          { title: "The Enter Key",       src: "pages/system/research-enter-key.html",     bleed: false },
    "r-theme-control":  { title: "The Appearance Control", src: "pages/system/research-theme-control.html", bleed: false },
    "r-selection":      { title: "Selection Controls",  src: "pages/system/research-selection-controls.html", bleed: false },
    "r-menus":          { title: "Menus",               src: "pages/system/research-menus.html", bleed: false },

    "get-started":      { title: "Get Started",       src: "pages/get-started.html",       bleed: false },
    "tokens":           { title: "Design Tokens",     src: "pages/tokens.html",            bleed: false },
    "components":       { title: "Components",         src: "pages/components.html",         bleed: false },
    "guidelines":       { title: "Logo Guidelines",   src: "pages/logo-guidelines.html",   bleed: false },
    "logo-exploration": { title: "Logo Exploration",  src: "pages/logo-exploration.html",  bleed: false },
    "node-explorations":{ title: "Node Explorations", src: "pages/node-explorations.html", bleed: false },
    "geometry-study":   { title: "Geometry Study",    src: "pages/geometry-study.html",    bleed: false },
    "geometry-midpoint":{ title: "Midpoint (node 9)", src: "pages/geometry-midpoint.html", bleed: false },
    "blueprint-plate":  { title: "Blueprint Plate",   src: "pages/blueprint-plate.html",   bleed: false },
    "motion":           { title: "Hero Animation",    src: "pages/hero.html",              bleed: true  }
  };

  var frame  = document.getElementById("doc");
  var loader = document.getElementById("loader");
  var tbTitle = document.getElementById("tbTitle");

  function keyFromHash() {
    var h = (location.hash || "").replace(/^#\/?/, "").trim();
    return ROUTES.hasOwnProperty(h) ? h : "";
  }

  function setActive(key) {
    var links = document.querySelectorAll(".nav a[data-route]");
    for (var i = 0; i < links.length; i++) {
      var r = links[i].getAttribute("data-route");
      links[i].classList.toggle("active", r === key || (key === "" && r === "home"));
    }
  }

  function render() {
    var key = keyFromHash();
    var route = ROUTES[key] || ROUTES[""];
    // show loader, swap src
    loader.classList.remove("hide");
    frame.setAttribute("src", route.src);
    document.title = "Goodness UI · " + route.title;
    if (tbTitle) tbTitle.textContent = route.title;
    setActive(key);
    document.body.classList.toggle("subnav-open", !!route.subnav);
    if (route.subnav) document.body.setAttribute("data-subnav", route.subnav);
    else document.body.removeAttribute("data-subnav");
    document.body.classList.remove("nav-open"); // close mobile nav on navigate
  }

  frame.addEventListener("load", function () {
    loader.classList.add("hide");
  });

  window.addEventListener("hashchange", render);
  window.addEventListener("DOMContentLoaded", render);

  // mobile nav toggle
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-burger]")) document.body.classList.toggle("nav-open");
    if (e.target.closest(".scrim"))        document.body.classList.remove("nav-open");
    // subnav: mark the clicked section link active
    var sublink = e.target.closest(".subnav a");
    if (sublink) {
      var links = document.querySelectorAll(".subnav a");
      for (var i = 0; i < links.length; i++) links[i].classList.remove("active");
      sublink.classList.add("active");
    }
  });

  render();
})();
