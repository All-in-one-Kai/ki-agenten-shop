#!/usr/bin/env python3
"""Inject Open Graph + Twitter Card meta tags into ki-agenten.shop HTML files.

Mirrors inject_schema.py: declarative per-page config, idempotent inject/replace,
run from repo root.
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

SITE = "ki-agenten.shop"
SITE_URL = "https://ki-agenten.shop"
OG_IMAGE = f"{SITE_URL}/og-image.jpg"
OG_IMAGE_W = 1200
OG_IMAGE_H = 630
LOCALE = "de_DE"
TWITTER_CARD = "summary_large_image"

PAGES = {
    "index.html": {
        "url": f"{SITE_URL}/",
        "title": "KI-Orchestrator für Unternehmen | ki-agenten.shop",
        "description": "Wir bauen Ihre Master-KI, die Agenten, Tools und Prozesse zentral steuert. DSGVO-konform, skalierbar, für Mittelstand & Enterprise im DACH-Raum.",
        "type": "website",
    },
    "ki-orchestrierung/index.html": {
        "url": f"{SITE_URL}/ki-orchestrierung/",
        "title": "KI-Orchestrierung für Unternehmen | ki-agenten.shop",
        "description": "KI-Orchestrierung koordiniert KI-Agenten, Modelle und Tools zu einem produktiven System. Für Mittelstand & Enterprise im DACH-Raum.",
        "type": "article",
    },
    "ki-agenten-fuer-unternehmen/index.html": {
        "url": f"{SITE_URL}/ki-agenten-fuer-unternehmen/",
        "title": "KI-Agenten für Unternehmen | ki-agenten.shop",
        "description": "KI-Agenten automatisieren Geschäftsprozesse autonom: Vertrieb, Support, Operations, Finance. Für Mittelstand & Enterprise, DSGVO-konform.",
        "type": "article",
    },
    "multi-agenten-systeme/index.html": {
        "url": f"{SITE_URL}/multi-agenten-systeme/",
        "title": "Multi-Agenten-Systeme für produktive KI-Prozesse | ki-agenten.shop",
        "description": "Multi-Agenten-Systeme koordinieren mehrere spezialisierte KI-Agenten für komplexe Geschäftsprozesse. Architektur, Frameworks, Deployment.",
        "type": "article",
    },
    "roi-ki-agenten-berechnen/index.html": {
        "url": f"{SITE_URL}/roi-ki-agenten-berechnen/",
        "title": "ROI von KI-Agenten berechnen: Framework & Kalkulator | ki-agenten.shop",
        "description": "ROI von KI-Agenten berechnen: Framework mit konkreten Formeln, Benchmarks und Beispielen. Für Business Cases und Investitionsentscheidungen.",
        "type": "article",
    },
    "ki-agenten-operations/index.html": {
        "url": f"{SITE_URL}/ki-agenten-operations/",
        "title": "KI-Agenten für Operations | ki-agenten.shop",
        "description": "KI-Agenten für Operations: Prozessüberwachung, Anomalieerkennung, Report-Generierung. Für COOs und Operations Manager.",
        "type": "article",
    },
    "ki-agenten-finance/index.html": {
        "url": f"{SITE_URL}/ki-agenten-finance/",
        "title": "KI-Agenten für Finance | ki-agenten.shop",
        "description": "KI-Agenten für Finance: Rechnungsprüfung, Zahlungsabgleich, Budget-Monitoring, Compliance. Für CFOs und Finance-Teams.",
        "type": "article",
    },
    "ki-agenten-compliance/index.html": {
        "url": f"{SITE_URL}/ki-agenten-compliance/",
        "title": "KI-Agenten für Compliance | ki-agenten.shop",
        "description": "KI-Agenten für Compliance: DSGVO-Monitoring, Vertragsprüfung, Policy-Checks. Kontinuierliche Überwachung statt periodischer Audits.",
        "type": "article",
    },
    "dsgvo-konforme-ki-agenten/index.html": {
        "url": f"{SITE_URL}/dsgvo-konforme-ki-agenten/",
        "title": "DSGVO-konforme KI-Agenten | ki-agenten.shop",
        "description": "DSGVO-konforme KI-Agenten: Datenminimierung, Zweckbindung, Audit Trails, Betroffenenrechte. Compliance-Guide für Unternehmen.",
        "type": "article",
    },
    "potenzialanalyse/index.html": {
        "url": f"{SITE_URL}/potenzialanalyse/",
        "title": "Kostenlose KI-Potenzialanalyse | ki-agenten.shop",
        "description": "Kostenlose KI-Potenzialanalyse: In 15 Minuten identifizieren wir Ihre Top-3 KI-Use-Cases mit ROI-Schätzung.",
        "type": "website",
    },
    "roi-rechner/index.html": {
        "url": f"{SITE_URL}/roi-rechner/",
        "title": "ROI-Rechner für KI-Agenten | ki-agenten.shop",
        "description": "Berechnen Sie in 60 Sekunden den ROI Ihrer KI-Orchestrierung. Kosteneinsparung, Zeitersparnis und Amortisation — individuell für Ihr Unternehmen.",
        "type": "website",
    },
    "impressum/index.html": {
        "url": f"{SITE_URL}/impressum/",
        "title": "Impressum | ki-agenten.shop",
        "description": "Impressum und Anbieterkennzeichnung der ki-agenten.shop — Culturetek Pte. Ltd.",
        "type": "website",
    },
    "datenschutz/index.html": {
        "url": f"{SITE_URL}/datenschutz/",
        "title": "Datenschutzerklärung | ki-agenten.shop",
        "description": "Datenschutzerklärung der ki-agenten.shop nach DSGVO — Informationen zur Verarbeitung personenbezogener Daten.",
        "type": "website",
    },
}


BLOCK_START = "<!-- Open Graph / Twitter meta -->"
BLOCK_END = "<!-- /Open Graph / Twitter meta -->"
BLOCK_PATTERN = re.compile(
    re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END),
    re.DOTALL,
)


def escape_attr(value: str) -> str:
    return value.replace("&", "&amp;").replace('"', "&quot;")


def build_block(page: dict) -> str:
    title = escape_attr(page["title"])
    description = escape_attr(page["description"])
    url = escape_attr(page["url"])
    og_type = page.get("type", "website")
    image = escape_attr(OG_IMAGE)

    return (
        f'{BLOCK_START}\n'
        f'<meta property="og:type" content="{og_type}">\n'
        f'<meta property="og:site_name" content="{SITE}">\n'
        f'<meta property="og:locale" content="{LOCALE}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{description}">\n'
        f'<meta property="og:image" content="{image}">\n'
        f'<meta property="og:image:width" content="{OG_IMAGE_W}">\n'
        f'<meta property="og:image:height" content="{OG_IMAGE_H}">\n'
        f'<meta property="og:image:alt" content="{SITE} — DSGVO-konforme KI-Agenten">\n'
        f'<meta name="twitter:card" content="{TWITTER_CARD}">\n'
        f'<meta name="twitter:title" content="{title}">\n'
        f'<meta name="twitter:description" content="{description}">\n'
        f'<meta name="twitter:image" content="{image}">\n'
        f'{BLOCK_END}'
    )


def inject_meta_into_head(html: str, block: str) -> str:
    """Replace existing OG/Twitter block if present, otherwise insert before </head>."""
    if BLOCK_PATTERN.search(html):
        return BLOCK_PATTERN.sub(block, html, count=1)
    return html.replace("</head>", block + "\n</head>", 1)


def process(filepath: str, block: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    html = inject_meta_into_head(html, block)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {os.path.relpath(filepath, BASE)}")


if __name__ == "__main__":
    print("=== Injecting Open Graph / Twitter Card meta ===\n")
    for relpath, page in PAGES.items():
        filepath = os.path.join(BASE, relpath)
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            print(f"  ⚠ SKIP {relpath} (empty or missing)")
            continue
        process(filepath, build_block(page))
    print("\nDone.")
