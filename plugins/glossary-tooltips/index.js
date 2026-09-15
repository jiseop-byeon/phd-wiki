import { h } from "preact"

// Terms come from quartz/static/glossary/terms.json, which
// scripts/build_glossary_index.py generates from content/glossary.md.

const css = `
.gloss-term {
  text-decoration: underline dotted var(--gray);
  text-underline-offset: 3px;
  text-decoration-thickness: 1px;
  cursor: help;
}
.gloss-term:hover, .gloss-term:focus-visible, .gloss-term[aria-expanded="true"] {
  text-decoration-color: var(--secondary);
  outline: none;
}
.gloss-card {
  position: fixed;
  z-index: 1000;
  max-width: min(22rem, calc(100vw - 2rem));
  padding: 0.7rem 0.85rem;
  border: 1px solid var(--lightgray);
  border-radius: 8px;
  background: var(--light);
  color: var(--darkgray);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.14);
  font-size: 0.86rem;
  line-height: 1.45;
}
.gloss-card[hidden] { display: none; }
.gloss-card .gloss-name { font-weight: 600; color: var(--dark); margin: 0 0 0.25rem 0; }
.gloss-card .gloss-name small { font-weight: 400; color: var(--gray); margin-left: 0.35rem; }
.gloss-card .gloss-def { margin: 0; }
.gloss-card .gloss-links { margin: 0.45rem 0 0 0; display: flex; flex-wrap: wrap; gap: 0.3rem 0.8rem; }
.gloss-card .gloss-links a { color: var(--secondary); text-decoration: none; font-weight: 500; }
.gloss-card .gloss-links a:hover { text-decoration: underline; }
.gloss-card .gloss-links a.gloss-all { color: var(--gray); font-weight: 400; }
`

const afterDOMLoaded = `
(() => {
  const MAX_PER_PAGE = 120
  const SKIP = "h1,h2,h3,h4,h5,h6,a,code,pre,kbd,.katex,svg,.mermaid,button,script,style,.gloss-term,.gloss-card,.read-log,nav,.callout-title"
  const HANGUL = /[\\uac00-\\ud7a3]/

  const esc = (s) => s.replace(/[.*+?^\${}()|[\\]\\\\]/g, "\\\\$&")
  let dataPromise = null
  const loadData = (root) => {
    if (!dataPromise) {
      dataPromise = fetch(root + "static/glossary/terms.json")
        .then((r) => (r.ok ? r.json() : { entries: [] }))
        .catch(() => ({ entries: [] }))
    }
    return dataPromise
  }

  function compile(entries) {
    const ci = new Map(), cs = new Map(), ko = new Map()
    entries.forEach((e, i) => {
      for (const n of e.match_en || []) {
        // names with two or more capitals (acronyms, proper names) match case-sensitively
        const caps = (n.match(/[A-Z]/g) || []).length
        const target = caps >= 2 || n.length <= 3 ? cs : ci
        const key = target === ci ? n.toLowerCase() : n
        if (!target.has(key)) target.set(key, i)
      }
      for (const n of e.match_ko || []) if (!ko.has(n)) ko.set(n, i)
    })
    const alt = (m) => [...m.keys()].sort((a, b) => b.length - a.length).map(esc).join("|")
    const mk = (m, flags, pre, post) => (m.size ? new RegExp(pre + "(" + alt(m) + ")" + post, flags) : null)
    return {
      ci, cs, ko,
      reCi: mk(ci, "gi", "(?<![A-Za-z0-9])", "(?![A-Za-z0-9])"),
      reCs: mk(cs, "g", "(?<![A-Za-z0-9])", "(?![A-Za-z0-9])"),
      reKo: mk(ko, "g", "(?<![\\uac00-\\ud7a3])", ""),
    }
  }

  function textNodes(root) {
    const out = []
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (!node.nodeValue || node.nodeValue.trim().length < 2) return NodeFilter.FILTER_REJECT
        const el = node.parentElement
        if (!el || el.closest(SKIP)) return NodeFilter.FILTER_REJECT
        return NodeFilter.FILTER_ACCEPT
      },
    })
    let n
    while ((n = walker.nextNode())) out.push(n)
    return out
  }

  // Which half of the page a node sits in: the wiki's pages have "## English" and
  // "## 한국어" sections; pages without them fall back to the paragraph's script.
  function langOf(node, markers) {
    let lang = null
    for (const m of markers) {
      if (m.el.compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING) lang = m.lang
      else break
    }
    if (lang) return lang
    const block = node.parentElement.closest("p,li,td,blockquote,div") || node.parentElement
    return HANGUL.test(block.textContent || "") ? "ko" : "en"
  }

  function annotate(article, data, root) {
    if (article.dataset.glossDone) return
    article.dataset.glossDone = "1"
    const entries = data.entries || []
    if (!entries.length) return
    const c = compile(entries)
    const markers = [...article.querySelectorAll("h2")]
      .map((el) => {
        const t = (el.textContent || "").trim().toLowerCase()
        return { el, lang: t.startsWith("english") ? "en" : t.startsWith("한국어") ? "ko" : null }
      })
      .filter((m) => m.lang)
    const seen = { en: new Set(), ko: new Set() }
    let count = 0

    for (const node of textNodes(article)) {
      if (count >= MAX_PER_PAGE) break
      const lang = langOf(node, markers)
      const text = node.nodeValue
      const hits = []
      const scan = (re, map, lower) => {
        if (!re) return
        re.lastIndex = 0
        let m
        while ((m = re.exec(text))) {
          const key = lower ? m[1].toLowerCase() : m[1]
          const idx = map.get(key)
          if (idx !== undefined) hits.push({ start: m.index, end: m.index + m[1].length, idx })
        }
      }
      if (lang === "ko") scan(c.reKo, c.ko, false)
      scan(c.reCs, c.cs, false)
      scan(c.reCi, c.ci, true)
      if (!hits.length) continue
      hits.sort((a, b) => a.start - b.start || b.end - a.end)

      const frag = document.createDocumentFragment()
      let pos = 0, used = false
      for (const hit of hits) {
        if (hit.start < pos || seen[lang].has(hit.idx) || count >= MAX_PER_PAGE) continue
        seen[lang].add(hit.idx)
        count++
        used = true
        frag.append(text.slice(pos, hit.start))
        const span = document.createElement("span")
        span.className = "gloss-term"
        span.tabIndex = 0
        span.dataset.gi = String(hit.idx)
        span.dataset.gl = lang
        span.setAttribute("role", "button")
        span.setAttribute("aria-expanded", "false")
        span.textContent = text.slice(hit.start, hit.end)
        frag.append(span)
        pos = hit.end
      }
      if (!used) continue
      frag.append(text.slice(pos))
      node.parentNode.replaceChild(frag, node)
    }
    article.dataset.glossRoot = root
  }

  let card = null, current = null, hideTimer = null
  function ensureCard() {
    if (card) return card
    card = document.createElement("div")
    card.className = "gloss-card"
    card.hidden = true
    card.setAttribute("role", "tooltip")
    card.addEventListener("mouseenter", () => clearTimeout(hideTimer))
    card.addEventListener("mouseleave", () => scheduleHide())
    document.body.appendChild(card)
    return card
  }

  function slugAnchor(a) {
    return a ? "#" + a.trim().toLowerCase().replace(/\\s+/g, "-") : ""
  }

  function show(span, data, root) {
    const e = data.entries[+span.dataset.gi]
    if (!e) return
    const ko = span.dataset.gl === "ko"
    const el = ensureCard()
    el.innerHTML = ""
    const name = document.createElement("p")
    name.className = "gloss-name"
    name.textContent = ko && e.ko ? e.ko : e.term
    const alt = ko ? e.term : e.ko
    if (alt) {
      const s = document.createElement("small")
      s.textContent = alt
      name.appendChild(s)
    }
    const def = document.createElement("p")
    def.className = "gloss-def"
    def.textContent = ko && e.kodef ? e.kodef : e.en || e.kodef
    el.append(name, def)
    const links = document.createElement("p")
    links.className = "gloss-links"
    for (const l of e.links || []) {
      const a = document.createElement("a")
      a.href = root + l.path + slugAnchor(l.anchor)
      a.textContent = "→ " + l.label
      links.appendChild(a)
    }
    const all = document.createElement("a")
    all.href = root + "glossary"
    all.className = "gloss-all"
    all.textContent = ko ? "용어집" : "Glossary"
    links.appendChild(all)
    el.appendChild(links)

    el.hidden = false
    const r = span.getBoundingClientRect()
    const w = el.offsetWidth, hgt = el.offsetHeight
    const vw = document.documentElement.clientWidth
    const left = Math.max(8, Math.min(r.left, vw - w - 8))
    let top = r.bottom + 6
    if (r.bottom + hgt + 12 > window.innerHeight && r.top > hgt + 12) top = r.top - hgt - 6
    el.style.left = left + "px"
    el.style.top = top + "px"
    if (current && current !== span) current.setAttribute("aria-expanded", "false")
    current = span
    span.setAttribute("aria-expanded", "true")
  }

  function hide() {
    if (card) card.hidden = true
    if (current) current.setAttribute("aria-expanded", "false")
    current = null
  }
  function scheduleHide() {
    clearTimeout(hideTimer)
    hideTimer = setTimeout(hide, 180)
  }

  function rootFor() {
    const holder = document.querySelector(".gloss-root")
    return holder ? holder.dataset.root : "./"
  }

  async function setup() {
    const holder = document.querySelector(".gloss-root")
    if (!holder || holder.dataset.skip === "1") return
    const article = document.querySelector("article")
    if (!article) return
    const root = rootFor()
    const data = await loadData(root)
    annotate(article, data, root)
  }

  if (!window.__glossWired) {
    window.__glossWired = true
    const withData = (fn) => loadData(rootFor()).then((d) => fn(d, rootFor()))
    const hoverable = window.matchMedia("(hover: hover)").matches
    document.addEventListener("mouseover", (ev) => {
      if (!hoverable) return
      const span = ev.target.closest && ev.target.closest(".gloss-term")
      if (!span) return
      clearTimeout(hideTimer)
      withData((d, root) => show(span, d, root))
    })
    document.addEventListener("mouseout", (ev) => {
      if (!hoverable) return
      if (ev.target.closest && ev.target.closest(".gloss-term")) scheduleHide()
    })
    document.addEventListener("focusin", (ev) => {
      const span = ev.target.closest && ev.target.closest(".gloss-term")
      if (span) withData((d, root) => show(span, d, root))
    })
    document.addEventListener("click", (ev) => {
      const span = ev.target.closest && ev.target.closest(".gloss-term")
      if (span) {
        ev.preventDefault()
        if (current === span && card && !card.hidden) hide()
        else withData((d, root) => show(span, d, root))
        return
      }
      if (card && !card.hidden && !(ev.target.closest && ev.target.closest(".gloss-card"))) hide()
    })
    document.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape") hide()
      if ((ev.key === "Enter" || ev.key === " ") && document.activeElement && document.activeElement.classList.contains("gloss-term")) {
        ev.preventDefault()
        const span = document.activeElement
        if (current === span && card && !card.hidden) hide()
        else withData((d, root) => show(span, d, root))
      }
    })
    document.addEventListener("scroll", () => { if (card && !card.hidden) hide() }, { capture: true, passive: true })
    document.addEventListener("nav", () => { hide(); setup() })
  }

  if (document.readyState !== "loading") setup()
  else document.addEventListener("DOMContentLoaded", setup)
})()
`

export const GlossaryTooltips = () => {
  const Component = ({ fileData }) => {
    const slug = fileData?.slug ?? ""
    const depth = slug.split("/").length - 1
    const root = depth > 0 ? "../".repeat(depth) : "./"
    const skip = slug === "glossary" ? "1" : "0"
    return h("span", { class: "gloss-root", hidden: true, "data-root": root, "data-skip": skip })
  }
  Component.css = css
  Component.afterDOMLoaded = afterDOMLoaded
  return Component
}

export default GlossaryTooltips
