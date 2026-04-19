#!/usr/bin/env python3
"""Inject Schema.org JSON-LD into ki-agenten.shop HTML files."""
import json, re, os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── 1. Organization schema (homepage only) ────────────────────────────────
ORGANIZATION = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://ki-agenten.shop/#organization",
  "name": "Culturetek Pte. Ltd.",
  "legalName": "Culturetek Pte. Ltd.",
  "url": "https://ki-agenten.shop",
  "logo": {
    "@type": "ImageObject",
    "url": "https://ki-agenten.shop/logo.png",
    "width": 512,
    "height": 512
  },
  "description": "DSGVO-konforme KI-Orchestrierung fuer den DACH-Mittelstand. Wir entwickeln und deployen Multi-Agent-Systeme, die Geschaeftsprozesse vollstaendig automatisieren.",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "6 Raffles Quay #14-02",
    "addressLocality": "Singapore",
    "postalCode": "048580",
    "addressCountry": "SG"
  },
  "areaServed": [
    {"@type": "Country", "name": "Germany"},
    {"@type": "Country", "name": "Austria"},
    {"@type": "Country", "name": "Switzerland"}
  ],
  "founder": [
    {"@type": "Person", "name": "Kai Zimmer", "jobTitle": "Co-Founder"},
    {"@type": "Person", "name": "Pallavi Sharma", "jobTitle": "Co-Founder"},
    {"@type": "Person", "name": "Riya Kalra", "jobTitle": "Co-Founder"}
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "sales",
    "availableLanguage": ["German", "English"],
    "areaServed": ["DE", "AT", "CH"]
  },
  "sameAs": [
    "https://www.linkedin.com/company/ai-in-life/"
  ],
  "knowsAbout": [
    "KI-Orchestrierung",
    "Multi-Agent-Systeme",
    "DSGVO-konforme KI",
    "EU AI Act Compliance",
    "Prozessautomatisierung",
    "Agentic AI"
  ]
}

# ── 2. FAQPage schema (homepage — 3 core compliance Q&As) ────────────────
FAQ_PAGE = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Ist ki-agenten.shop NIS2-konform?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ja. Culturetek entwickelt alle KI-Agenten-Systeme für den deutschen/europäischen Regulierungsrahmen: NIS2 (EU 2022/2555) — Logging, Incident-Reporting-Workflows, Zugriffskontrolle; EU AI Act (VO 2024/1689) — Risikoklassifizierung Art. 6–9, Human-Oversight, vollständige Dokumentation; DSGVO — Datenverarbeitung auf deutschen/EU-Servern, keine US-Cloud ohne SCCs. Kostenloses Compliance-Briefing: https://ki-agenten.shop/potenzialanalyse/"
      }
    },
    {
      "@type": "Question",
      "name": "Erfüllen Ihre KI-Agenten den EU AI Act?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ja. Unsere KI-Agenten werden nach EU AI Act (VO 2024/1689) entwickelt: Risikoklassifizierung gemäß Art. 6–9, obligatorisches Human-Oversight für Hochrisiko-Systeme und vollständige technische Dokumentation. Alle Systeme sind auditierbar und nachvollziehbar."
      }
    },
    {
      "@type": "Question",
      "name": "Wo werden meine Unternehmensdaten gespeichert?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ihre Daten werden ausschließlich auf deutschen und EU-Servern verarbeitet. Wir nutzen keine US-Cloud-Dienste ohne Standard-Vertragsklauseln (SCCs) und halten alle DSGVO-Anforderungen ein. Auf Wunsch können wir vollständig On-Premise oder in Ihrer eigenen Cloud-Infrastruktur deployen."
      }
    }
  ]
}

# ── 3. Service schemas (homepage pricing section) ──────────────────────────
SERVICE_KICKSTART = {
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://ki-agenten.shop/#kickstart",
  "name": "KI-Orchestrierung Kickstart",
  "description": "Einstieg in die KI-Automatisierung: Strategie-Workshop, Orchestrator-Blueprint und 1-3 live Produktionsprozesse. Ideal fuer Mittelstaendler (50-500 Mitarbeiter) in DACH.",
  "serviceType": "KI-Orchestrierung",
  "provider": {"@id": "https://ki-agenten.shop/#organization"},
  "areaServed": [
    {"@type": "Country", "name": "Germany"},
    {"@type": "Country", "name": "Austria"},
    {"@type": "Country", "name": "Switzerland"}
  ],
  "audience": {
    "@type": "BusinessAudience",
    "audienceType": "Mittelstand (50-500 Mitarbeiter), DACH-Region, COO / CDO / Head of Operations"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "EUR",
    "price": "0",
    "description": "Preis auf Anfrage",
    "eligibleRegion": ["DE", "AT", "CH"],
    "availability": "https://schema.org/InStock"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Kickstart Leistungsumfang",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Strategie-Workshop + Use-Case-Priorisierung"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Orchestrator-Blueprint"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "1-3 live Produktionsprozesse"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Monitoring-Dashboard"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "E-Mail & WhatsApp Support"}}
    ]
  }
}

SERVICE_SCALE = {
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://ki-agenten.shop/#scale",
  "name": "KI-Orchestrierung Scale",
  "description": "Multi-Agent-Workforce fuer alle Geschaeftsbereiche: unbegrenzte Agent-Rollen, Enterprise-Governance, Priority-Support. Fuer DACH-Unternehmen nach erfolgreicher MVP-Phase.",
  "serviceType": "KI-Orchestrierung",
  "provider": {"@id": "https://ki-agenten.shop/#organization"},
  "areaServed": [
    {"@type": "Country", "name": "Germany"},
    {"@type": "Country", "name": "Austria"},
    {"@type": "Country", "name": "Switzerland"}
  ],
  "audience": {
    "@type": "BusinessAudience",
    "audienceType": "Wachstumsunternehmen, Series B+, DACH-Mittelstand mit validiertem KI-MVP"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "EUR",
    "price": "0",
    "description": "Preis auf Anfrage",
    "eligibleRegion": ["DE", "AT", "CH"],
    "availability": "https://schema.org/InStock"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Scale Leistungsumfang",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Alle Kickstart-Leistungen"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Unbegrenzte Agent-Rollen"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Monitoring & QA-Framework"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Governance & Kostenkontrolle"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Enterprise-Integrationen (CRM, ERP, Slack, n8n, Make)"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Priority-Support"}}
    ]
  }
}

SERVICE_ENTERPRISE = {
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://ki-agenten.shop/#enterprise",
  "name": "KI-Orchestrierung Enterprise",
  "description": "Enterprise-KI-Orchestrierung mit SSO/RBAC, Audit-Logging, Custom Connectors und SLA-gesichertem Support. Fuer Grossunternehmen (500+ Mitarbeiter) in regulierten Branchen.",
  "serviceType": "KI-Orchestrierung",
  "provider": {"@id": "https://ki-agenten.shop/#organization"},
  "areaServed": [
    {"@type": "Country", "name": "Germany"},
    {"@type": "Country", "name": "Austria"},
    {"@type": "Country", "name": "Switzerland"}
  ],
  "audience": {
    "@type": "BusinessAudience",
    "audienceType": "Grossunternehmen 500+ Mitarbeiter, regulierte Branchen (Finanz, Versicherung, Gesundheit, Logistik), DACH"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "EUR",
    "price": "0",
    "description": "Preis auf Anfrage",
    "eligibleRegion": ["DE", "AT", "CH"],
    "availability": "https://schema.org/InStock"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Enterprise Leistungsumfang",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Alle Scale-Leistungen"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "SSO / RBAC"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Audit-Logging & Custom-Policies"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Custom Connectors"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Dedizierte Umgebungen"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "SLA + dediziertes Support-Team"}}
    ]
  }
}

# ── Helpers ────────────────────────────────────────────────────────────────

def make_ld_tag(schema):
    return f'<script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n</script>'

def make_breadcrumb(items):
    """items: list of (name, url) tuples"""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": name, "item": url}
            for i, (name, url) in enumerate(items)
        ]
    }

OLD_ORG_PATTERN = re.compile(
    r'<!-- Schema\.org structured data -->\s*<script type="application/ld\+json">.*?</script>',
    re.DOTALL
)

# Matches any lone <script type="application/ld+json">...</script> block
LD_BLOCK_PATTERN = re.compile(
    r'<script type="application/ld\+json">.*?</script>',
    re.DOTALL
)

def replace_breadcrumb_or_inject(html, breadcrumb_tag):
    """For subpages: replace ALL existing BreadcrumbList blocks with the new one,
    keeping other schemas (Article, Service…) in place."""
    import json as _json

    new_scripts = []
    breadcrumb_placed = False

    for m in LD_BLOCK_PATTERN.finditer(html):
        raw = m.group()
        try:
            d = _json.loads(raw[len('<script type="application/ld+json">'):raw.rfind('</script>')])
            if d.get('@type') == 'BreadcrumbList':
                if not breadcrumb_placed:
                    new_scripts.append((m.start(), m.end(), breadcrumb_tag))
                    breadcrumb_placed = True
                else:
                    # Remove duplicate — replace with empty string
                    new_scripts.append((m.start(), m.end(), ''))
            # else: keep as-is (no replacement needed)
        except Exception:
            pass  # keep as-is

    if not new_scripts:
        # No BreadcrumbList existed — inject before </head>
        return html.replace("</head>", breadcrumb_tag + "\n</head>", 1)

    # Apply replacements in reverse order so offsets stay valid
    result = html
    for start, end, replacement in reversed(new_scripts):
        result = result[:start] + replacement + result[end:]
    return result

def inject_into_head(html, *ld_tags):
    """Replace existing schema block or inject before </head>. (Homepage use)"""
    combined = "\n<!-- Schema.org structured data -->\n" + "\n".join(ld_tags) + "\n"
    if OLD_ORG_PATTERN.search(html):
        html = OLD_ORG_PATTERN.sub(combined.strip(), html, count=1)
    else:
        html = html.replace("</head>", combined + "</head>", 1)
    return html

def process_homepage(filepath, *ld_tags):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    html = inject_into_head(html, *ld_tags)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {os.path.relpath(filepath, BASE)}")

def process_subpage(filepath, breadcrumb_tag):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    html = replace_breadcrumb_or_inject(html, breadcrumb_tag)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {os.path.relpath(filepath, BASE)}")

# ── 3. BreadcrumbList definitions per page ────────────────────────────────

BREADCRUMBS = {
    "ki-orchestrierung/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("KI-Orchestrierung", "https://ki-agenten.shop/ki-orchestrierung/")
    ],
    "ki-agenten-fuer-unternehmen/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("KI-Agenten fuer Unternehmen", "https://ki-agenten.shop/ki-agenten-fuer-unternehmen/")
    ],
    "multi-agenten-systeme/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("Multi-Agenten-Systeme", "https://ki-agenten.shop/multi-agenten-systeme/")
    ],
    "roi-ki-agenten-berechnen/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("ROI KI-Agenten berechnen", "https://ki-agenten.shop/roi-ki-agenten-berechnen/")
    ],
    "ki-agenten-operations/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("KI-Agenten Operations", "https://ki-agenten.shop/ki-agenten-operations/")
    ],
    "potenzialanalyse/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("KI-Potenzialanalyse", "https://ki-agenten.shop/potenzialanalyse/")
    ],
    "roi-rechner/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("ROI-Rechner", "https://ki-agenten.shop/roi-rechner/")
    ],
    "impressum/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("Impressum", "https://ki-agenten.shop/impressum/")
    ],
    "datenschutz/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("Datenschutz", "https://ki-agenten.shop/datenschutz/")
    ],
    "dsgvo-konforme-ki-agenten/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("DSGVO-konforme KI-Agenten", "https://ki-agenten.shop/dsgvo-konforme-ki-agenten/")
    ],
    "ki-agenten-finance/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("KI-Agenten Finance", "https://ki-agenten.shop/ki-agenten-finance/")
    ],
    "ki-agenten-compliance/index.html": [
        ("Startseite", "https://ki-agenten.shop"),
        ("KI-Agenten Compliance", "https://ki-agenten.shop/ki-agenten-compliance/")
    ],
}

# ── Main ───────────────────────────────────────────────────────────────────

print("=== Injecting Schema.org JSON-LD ===\n")

print("Homepage (Organization + FAQPage + 3 Service schemas):")
process_homepage(
    os.path.join(BASE, "index.html"),
    make_ld_tag(ORGANIZATION),
    make_ld_tag(FAQ_PAGE),
    make_ld_tag(SERVICE_KICKSTART),
    make_ld_tag(SERVICE_SCALE),
    make_ld_tag(SERVICE_ENTERPRISE),
)

print("\nSubpages (BreadcrumbList — replace existing, keep other schemas):")
for relpath, crumbs in BREADCRUMBS.items():
    filepath = os.path.join(BASE, relpath)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        process_subpage(filepath, make_ld_tag(make_breadcrumb(crumbs)))
    else:
        print(f"  ⚠ SKIP {relpath} (empty or missing)")

print("\nDone.")
