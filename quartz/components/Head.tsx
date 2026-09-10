import { i18n } from "../i18n"
import { FullSlug, getFileExtension, joinSegments, pathToRoot } from "../util/path"
import { CSSResourceToStyleElement, JSResourceToScriptElement } from "../util/resources"
import { googleFontHref, googleFontSubsetHref } from "../util/theme"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { unescapeHTML } from "../util/escape"
import { CustomOgImagesEmitterName } from "../../.quartz/plugins"
export default (() => {
  const Head: QuartzComponent = ({
    cfg,
    fileData,
    externalResources,
    ctx,
  }: QuartzComponentProps) => {
    const titleSuffix = cfg.pageTitleSuffix ?? ""
    const title =
      (fileData.frontmatter?.title ?? i18n(cfg.locale).propertyDefaults.title) + titleSuffix
    const description =
      fileData.frontmatter?.socialDescription ??
      fileData.frontmatter?.description ??
      unescapeHTML(fileData.description?.trim() ?? i18n(cfg.locale).propertyDefaults.description)

    const { css, js, additionalHead } = externalResources

    const url = new URL(`https://${cfg.baseUrl ?? "example.com"}`)
    const path = url.pathname as FullSlug
    const baseDir = fileData.slug === "404" ? path : pathToRoot(fileData.slug!)
    const iconPath = joinSegments(baseDir, "static/icon.png")

    // Url of current page
    const socialUrl =
      fileData.slug === "404" ? url.toString() : joinSegments(url.toString(), fileData.slug!)

    const usesCustomOgImage = ctx.cfg.plugins.emitters.some(
      (e) => e.name === CustomOgImagesEmitterName,
    )
    const ogImageDefaultPath = `https://${cfg.baseUrl}/static/og-image.png`

    const coreStylesheet = css[0]?.content
    const coreScript = js.find(
      (r) => r.loadTime === "beforeDOMReady" && r.contentType === "external",
    )

    return (
      <head>
        <title>{title}</title>
        <meta charSet="utf-8" />
        {coreStylesheet && <link rel="preload" href={coreStylesheet} as="style" />}
        {coreScript && coreScript.contentType === "external" && (
          <link rel="preload" href={coreScript.src} as="script" />
        )}
        {cfg.theme.cdnCaching && cfg.theme.fontOrigin === "googleFonts" && (
          <>
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" />
            <link rel="stylesheet" href={googleFontHref(cfg.theme)} />
            {/* Half this wiki is Korean and none of the three configured faces
                carries a Hangul glyph, so every Korean paragraph was being set in
                whatever the reader's OS happened to substitute. */}
            <link
              rel="stylesheet"
              href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700&display=swap"
            />
            {/* Paper only. Loaded at print priority so screen readers never wait on it. */}
            <link
              rel="stylesheet"
              media="print"
              href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=Noto+Serif+KR:wght@400;600&display=swap"
            />
            {cfg.theme.typography.title && (
              <link rel="stylesheet" href={googleFontSubsetHref(cfg.theme, cfg.pageTitle)} />
            )}
          </>
        )}
        <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossOrigin="anonymous" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

        <meta name="og:site_name" content={cfg.pageTitle}></meta>
        <meta property="og:title" content={title} />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />
        <meta property="og:description" content={description} />
        <meta property="og:image:alt" content={description} />

        {!usesCustomOgImage && (
          <>
            <meta property="og:image" content={ogImageDefaultPath} />
            <meta property="og:image:url" content={ogImageDefaultPath} />
            <meta name="twitter:image" content={ogImageDefaultPath} />
            <meta
              property="og:image:type"
              content={`image/${getFileExtension(ogImageDefaultPath) ?? "png"}`}
            />
          </>
        )}

        {cfg.baseUrl && (
          <>
            <meta property="twitter:domain" content={cfg.baseUrl}></meta>
            <meta property="og:url" content={socialUrl}></meta>
            <meta property="twitter:url" content={socialUrl}></meta>
          </>
        )}

        <link rel="icon" href={iconPath} />
        <meta name="description" content={description} />
        <meta name="generator" content="Quartz" />

        {css.map((resource) => CSSResourceToStyleElement(resource, true))}
        {js
          .filter((resource) => resource.loadTime === "beforeDOMReady")
          .map((res) => JSResourceToScriptElement(res, true))}
        {additionalHead.map((resource) => {
          if (typeof resource === "function") {
            return resource(fileData)
          } else {
            return resource
          }
        })}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              var __LANG_KEY = "wiki-read-lang";

              function __tagLangs() {
                var host = document.querySelector("article .markdown-preview-view") ||
                           document.querySelector("article > div");
                if (!host) return false;
                var kids = host.children, lang = null, seen = {}, ids = {};
                for (var i = 0; i < kids.length; i++) {
                  var el = kids[i];
                  if (el.tagName === "H2") {
                    var t = (el.textContent || "").trim();
                    if (t === "English") { lang = "en"; el.classList.add("lang-heading"); }
                    else if (t === "\\ud55c\\uad6d\\uc5b4") { lang = "ko"; el.classList.add("lang-heading"); el.classList.add("lang-heading-ko"); }
                  }
                  if (lang) {
                    var tag = lang;
                    if (lang === "en" && !el.classList.contains("lang-heading")) {
                      // Bilingual callouts and embedded widgets are authored once, in the
                      // English half. Mark them "both" so neither filter hides them.
                      var isCallout = el.matches("blockquote") || el.classList.contains("callout");
                      var isWidget = el.matches("iframe") || !!el.querySelector("iframe");
                      if (isWidget || (isCallout && /[\uac00-\ud7a3]/.test(el.textContent || ""))) {
                        tag = "both";
                      }
                    }
                    el.setAttribute("data-lang", tag);
                    seen[lang] = true;
                    var hs = el.matches("h1,h2,h3,h4,h5,h6") ? [el] : el.querySelectorAll("h1,h2,h3,h4,h5,h6");
                    for (var j = 0; j < hs.length; j++) {
                      if (hs[j].id) ids[hs[j].id] = { lang: lang, divider: hs[j].classList.contains("lang-heading") };
                    }
                  }
                }
                var links = document.querySelectorAll(".toc-content a[data-for]");
                for (var k = 0; k < links.length; k++) {
                  var info = ids[links[k].getAttribute("data-for")];
                  var li = links[k].closest("li");
                  if (info && li) {
                    li.setAttribute("data-lang", info.lang);
                    if (info.divider) li.classList.add("lang-heading-item");
                  }
                }
                return !!(seen.en && seen.ko);
              }

              function __applyLang(lang) {
                document.body.classList.remove("lang-en", "lang-ko");
                if (lang) document.body.classList.add("lang-" + lang);
                var box = document.getElementById("pdf-controls");
                if (box) {
                  var bs = box.querySelectorAll("button[data-lang-btn]");
                  for (var i = 0; i < bs.length; i++) {
                    bs[i].setAttribute("aria-pressed", bs[i].getAttribute("data-lang-btn") === lang ? "true" : "false");
                  }
                }
              }

              function __readLang() {
                try { return localStorage.getItem(__LANG_KEY) || ""; } catch (e) { return ""; }
              }

              function __setLang(lang) {
                try { lang ? localStorage.setItem(__LANG_KEY, lang) : localStorage.removeItem(__LANG_KEY); } catch (e) {}
                __applyLang(lang);
              }

              function __addRunningHead() {
                var h = document.getElementById("print-running-head");
                if (!h) {
                  h = document.createElement("div");
                  h.id = "print-running-head";
                  document.body.insertBefore(h, document.body.firstChild);
                }
                var t = document.querySelector("article h1");
                h.textContent = (t ? t.textContent : document.title).trim();
              }

              function __addPdfBtn() {
                var old = document.getElementById("pdf-controls");
                if (old) old.remove();
                var bilingual = __tagLangs();
                __addRunningHead();
                var box = document.createElement("div");
                box.id = "pdf-controls";
                if (bilingual) {
                  [["EN", "en", "Show the English half only"],
                   ["\\ud55c", "ko", "Show the Korean half only"]].forEach(function (it) {
                    var b = document.createElement("button");
                    b.textContent = it[0];
                    b.title = it[2] + " \\u2014 click again for both";
                    b.setAttribute("data-lang-btn", it[1]);
                    b.setAttribute("aria-pressed", "false");
                    b.addEventListener("click", function () {
                      __setLang(__readLang() === it[1] ? "" : it[1]);
                    });
                    box.appendChild(b);
                  });
                }
                var pdf = document.createElement("button");
                pdf.textContent = "PDF \\u2913";
                pdf.title = bilingual ? "Save what is shown as PDF" : "Save this page as PDF";
                pdf.addEventListener("click", function () { window.print(); });
                box.appendChild(pdf);
                document.body.appendChild(box);
                __applyLang(bilingual ? __readLang() : "");
              }

              window.addEventListener("DOMContentLoaded", __addPdfBtn);
              document.addEventListener("nav", __addPdfBtn);
            `,
          }}
        />
      </head>
    )
  }

  return Head
}) satisfies QuartzComponentConstructor
