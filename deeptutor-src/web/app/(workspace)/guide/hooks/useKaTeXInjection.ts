/**
 * Hook for injecting KaTeX resources + render script into HTML content.
 *
 * Strategy: inject CDN resources into <head> + a small inline init script
 * that polls for renderMathInElement availability. HTMLViewer also has
 * a parent-window fallback in case the inline script gets corrupted by
 * page content containing "</script>" strings.
 */
export function useKaTeXInjection() {
  const injectKaTeX = (html: string): string => {
    const htmlLower = html.toLowerCase();
    const hasKaTeX =
      htmlLower.includes("katex.min.css") ||
      htmlLower.includes("katex.min.js") ||
      htmlLower.includes("katex@") ||
      htmlLower.includes("cdn.jsdelivr.net/npm/katex") ||
      htmlLower.includes("unpkg.com/katex");

    if (hasKaTeX) {
      console.log("[KaTeX] Already included, skipping injection");
      return html;
    }

    // CDN resources (no SRI hash to avoid mismatch)
    const katexResources = [
      '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" crossorigin="anonymous">',
      '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js" crossorigin="anonymous"><' + "/script>",
      '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" crossorigin="anonymous"><' + "/script>",
    ].join("\n  ");

    // Inline render script — placed in <head> with DOMContentLoaded listener.
    // Uses data-katex-init attr so sanitizer preserves it (contains "katex").
    // Polls every 100ms up to 5s for auto-render to load via defer.
    // eslint-disable-next-line no-template-curly-in-string
    const katexInit =
      '<script data-katex-init>' +
      'document.addEventListener("DOMContentLoaded",function(){var t=0,i=setInterval(function(){if(typeof renderMathInElement==="function"){clearInterval(i);try{renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false},{left:"\\\\(",right:"\\\\)",display:false},{left:"\\\\[",right:"\\\\]",display:true}],throwOnError:false});console.log("[KaTeX] Rendered "+document.querySelectorAll(".katex").length+" formulas")}catch(e){console.error("[KaTeX] Error:",e)}}else if(++t>50){clearInterval(i);console.warn("[KaTeX] Timeout")}},100)});' +
      "<" + "/script>";

    const headContent = katexResources + "\n  " + katexInit;

    // Inject into <head>
    if (html.includes("</head>")) {
      return html.replace("</head>", headContent + "\n</head>");
    }
    if (html.includes("<head>")) {
      return html.replace(/<head([^>]*)>/i, "<head$1>\n" + headContent);
    }
    if (html.includes("<html")) {
      return html.replace(
        /(<html[^>]*>)/i,
        "$1\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n" + headContent + "\n</head>",
      );
    }

    // Wrap bare content
    return (
      "<!DOCTYPE html>\n<html lang=\"zh\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n" +
      headContent +
      "\n</head>\n<body>\n" +
      html +
      "\n</body>\n</html>"
    );
  };

  return { injectKaTeX };
}
