import { h } from "preact"

const css = `
.read-log {
  margin-top: 2rem;
  padding: 0.9rem 1rem;
  border: 1px solid var(--lightgray);
  border-radius: 6px;
  background: var(--light);
  font-size: 0.9rem;
}
.read-log .read-log-head {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}
.read-log .read-log-title {
  font-weight: 600;
  color: var(--dark);
  margin-right: 0.2rem;
}
.read-log button {
  width: 1.9rem;
  height: 1.9rem;
  line-height: 1;
  font-size: 1.15rem;
  border: 1px solid var(--lightgray);
  border-radius: 5px;
  background: transparent;
  color: var(--dark);
  cursor: pointer;
  padding: 0;
  transition: background 0.15s ease, border-color 0.15s ease;
}
.read-log button:hover:not(:disabled) {
  background: var(--lightgray);
  border-color: var(--gray);
}
.read-log .read-log-dates li button { background: transparent; }
.read-log button:disabled { opacity: 0.35; cursor: not-allowed; }
.read-log .read-log-count { font-variant-numeric: tabular-nums; color: var(--dark); }
.read-log .read-log-count strong { font-size: 1.05rem; }
.read-log .read-log-since { color: var(--gray); font-size: 0.82rem; }
.read-log .read-log-dates {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin: 0.6rem 0 0 0;
  padding: 0;
  list-style: none;
}
.read-log .read-log-dates li {
  font-variant-numeric: tabular-nums;
  font-size: 0.8rem;
  color: var(--darkgray);
  background: var(--lightgray);
  border-radius: 4px;
  padding: 0.1rem 0.45rem;
}
.read-log .read-log-dates li button {
  width: auto; height: auto; border: 0; background: none;
  font-size: 0.8rem; padding: 0 0 0 0.3rem; color: var(--gray);
}
.read-log .read-log-dates li button:hover { color: var(--secondary); background: none; }
.read-log .read-log-empty { color: var(--gray); font-size: 0.82rem; margin: 0.5rem 0 0 0; }
`

// Runs on every page load (and SPA navigation) in the browser.
const afterDOMLoaded = `
(() => {
  const KEY = (slug) => "readlog:" + slug

  const today = () => {
    const d = new Date()
    const p = (n) => String(n).padStart(2, "0")
    return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate())
  }

  const load = (slug) => {
    try {
      const raw = localStorage.getItem(KEY(slug))
      const arr = raw ? JSON.parse(raw) : []
      return Array.isArray(arr) ? arr.filter((x) => typeof x === "string") : []
    } catch {
      return []
    }
  }

  const save = (slug, dates) => {
    try {
      if (dates.length === 0) localStorage.removeItem(KEY(slug))
      else localStorage.setItem(KEY(slug), JSON.stringify(dates))
    } catch {}
  }

  const daysBetween = (iso) => {
    const then = new Date(iso + "T00:00:00")
    const now = new Date(today() + "T00:00:00")
    return Math.round((now - then) / 86400000)
  }

  const sinceText = (dates) => {
    if (dates.length === 0) return ""
    const d = daysBetween(dates[dates.length - 1])
    if (Number.isNaN(d)) return ""
    if (d === 0) return "오늘 읽음 · read today"
    if (d === 1) return "어제 읽음 · 1 day ago"
    return d + "일 전 · " + d + " days ago"
  }

  function render(root) {
    const slug = root.dataset.slug || location.pathname
    const dates = load(slug).slice().sort()

    const count = root.querySelector(".read-log-count")
    const since = root.querySelector(".read-log-since")
    const list = root.querySelector(".read-log-dates")
    const empty = root.querySelector(".read-log-empty")
    const minus = root.querySelector('[data-act="minus"]')

    count.innerHTML = "<strong>" + dates.length + "</strong>회차"
    since.textContent = sinceText(dates)
    minus.disabled = dates.length === 0
    empty.style.display = dates.length === 0 ? "" : "none"

    list.innerHTML = ""
    dates.forEach((date) => {
      const li = document.createElement("li")
      li.textContent = date
      const del = document.createElement("button")
      del.type = "button"
      del.textContent = "×"
      del.dataset.act = "del"
      del.dataset.date = date
      del.title = date + " 기록 지우기 · remove this date"
      del.setAttribute("aria-label", date + " 기록 지우기")
      li.appendChild(del)
      list.appendChild(li)
    })
  }

  // Listeners are delegated from the document once, so a repeated nav event or a
  // re-run of setup() can never stack handlers on the same buttons.
  function setup() {
    document.querySelectorAll(".read-log").forEach(render)
  }

  if (!window.__readLogWired) {
    window.__readLogWired = true

    document.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-act]")
      if (!btn) return
      const root = btn.closest(".read-log")
      if (!root) return
      const slug = root.dataset.slug || location.pathname
      const act = btn.dataset.act

      if (act === "plus") {
        const cur = load(slug)
        cur.push(today())
        save(slug, cur)
      } else if (act === "minus") {
        const cur = load(slug).slice().sort()
        cur.pop()
        save(slug, cur)
      } else if (act === "del") {
        const cur = load(slug)
        const i = cur.indexOf(btn.dataset.date)
        if (i >= 0) cur.splice(i, 1)
        save(slug, cur)
      }
      render(root)
    })

    document.addEventListener("nav", setup)
  }

  if (document.readyState !== "loading") setup()
  else document.addEventListener("DOMContentLoaded", setup)
})()
`

export const ReadLog = () => {
  const ReadLogComponent = ({ fileData, displayClass }) => {
    const slug = fileData?.slug ?? ""
    return h(
      "div",
      { class: ["read-log", displayClass].filter(Boolean).join(" "), "data-slug": slug },
      h("div", { class: "read-log-head" }, [
        h("span", { class: "read-log-title", key: "t" }, "읽은 기록 · Reading log"),
        h(
          "button",
          {
            key: "m",
            type: "button",
            "data-act": "minus",
            title: "가장 최근 기록 지우기 · remove the most recent date",
            "aria-label": "가장 최근 읽은 기록 지우기",
          },
          "−",
        ),
        h("span", { class: "read-log-count", key: "c" }, "0회차"),
        h(
          "button",
          {
            key: "p",
            type: "button",
            "data-act": "plus",
            title: "오늘 날짜로 한 번 더 기록 · record a read for today",
            "aria-label": "오늘 읽음으로 기록",
          },
          "+",
        ),
        h("span", { class: "read-log-since", key: "s" }, ""),
      ]),
      h("ul", { class: "read-log-dates" }),
      h(
        "p",
        { class: "read-log-empty" },
        "아직 기록 없음 — 다 읽었으면 + 를 눌러라 · No reads recorded yet — press + when you finish a pass.",
      ),
    )
  }

  ReadLogComponent.css = css
  ReadLogComponent.afterDOMLoaded = afterDOMLoaded
  return ReadLogComponent
}

export default ReadLog
