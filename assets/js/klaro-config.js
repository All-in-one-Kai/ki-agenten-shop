/**
 * Klaro! Consent Manager — ki-agenten.shop (Extended)
 * Replaces: consent-banner/klaro-config.js (from CULA-22)
 * Adds: LinkedIn Insight Tag + Google Ads (Marketing category)
 * Issue: CULA-47
 *
 * SETUP REQUIRED before going live:
 *   1. Replace LINKEDIN_PARTNER_ID_PLACEHOLDER with actual LinkedIn Partner ID
 *      → LinkedIn Campaign Manager → Account Assets → Insight Tag → Partner ID
 *   2. Replace AW-GOOGLE_ADS_ID_PLACEHOLDER with actual Google Ads Tag ID
 *      → Google Ads → Tools → Tag → Google tag ID (format: AW-XXXXXXXXXX)
 *   3. Meta Pixel: uncomment the meta-pixel service block after CULA-17 P2.3 setup
 *
 * Must load BEFORE klaro.min.js and AFTER the gtag consent defaults script.
 */

var KI_PIXEL_CONFIG = {
  linkedInPartnerId: 'LINKEDIN_PARTNER_ID_PLACEHOLDER',
  googleAdsTagId: 'AW-GOOGLE_ADS_ID_PLACEHOLDER'
};

var klaroConfig = {
  version: 1,
  elementID: 'klaro',
  storageMethod: 'localStorage',
  storageName: 'klaro',
  htmlTexts: false,
  cookieExpiresAfterDays: 365,
  default: false,
  mustConsent: false,
  acceptAll: true,
  hideDeclineAll: false,
  lang: 'de',

  translations: {
    de: {
      privacyPolicyUrl: '/datenschutz/',
      consentNotice: {
        description:
          'Wir verwenden Cookies und ähnliche Technologien. ' +
          'Analyse-Cookies helfen uns, die Website zu verbessern. ' +
          'Marketing-Cookies ermöglichen relevante Werbung auf anderen Plattformen. ' +
          'Sie entscheiden, welche Kategorien Sie zulassen.',
        learnMore: 'Einstellungen'
      },
      consentModal: {
        title: 'Datenschutz&shy;einstellungen',
        description:
          'Hier können Sie einsehen und anpassen, welche Informationen wir über Sie sammeln. ' +
          'Einträge als "Immer aktiv" sind für den Website-Betrieb erforderlich.',
        privacyPolicy: {
          name: 'Datenschutzerklärung',
          text: 'Weitere Informationen finden Sie in unserer {privacyPolicy}.'
        }
      },
      accept: 'Akzeptieren',
      decline: 'Nur notwendige',
      close: 'Schließen',
      acceptAll: 'Alle akzeptieren',
      acceptSelected: 'Auswahl bestätigen',
      poweredBy: 'Realisiert mit Klaro!',
      service: {
        disableAll: {
          title: 'Alle Dienste',
          description: 'Alle optionalen Dienste aktivieren oder deaktivieren.'
        },
        optOut: { title: '(Opt-Out)', description: 'Standardmäßig geladen, jederzeit deaktivierbar.' },
        required: { title: '(Immer aktiv)', description: 'Für den Website-Betrieb erforderlich.' },
        purposes: 'Zwecke',
        purpose: 'Zweck'
      },
      purposes: {
        analytics: {
          title: 'Analyse',
          description: 'Anonymisierte Daten über Seitenaufrufe und Verhalten zur Website-Verbesserung.'
        },
        marketing: {
          title: 'Marketing',
          description:
            'Ermöglicht relevante Werbung auf LinkedIn und Google sowie die Messung des Kampagnenerfolgs. ' +
            'Diese Dienste können Ihnen auf anderen Plattformen Anzeigen zeigen.'
        }
      }
    }
  },

  services: [

    // ── Analytics ────────────────────────────────────────────────────────────
    {
      name: 'google-analytics',
      title: 'Google Analytics 4',
      purposes: ['analytics'],
      cookies: [
        [/^_ga$/, '/', '.ki-agenten.shop'],
        [/^_ga_/, '/', '.ki-agenten.shop'],
        [/^_gid$/, '/', '.ki-agenten.shop'],
        [/^_gat/, '/', '.ki-agenten.shop']
      ],
      callback: function (consent, service) {
        if (typeof window.gtag !== 'function') return;
        if (consent) {
          window.gtag('consent', 'update', { analytics_storage: 'granted' });
        } else {
          window.gtag('consent', 'update', { analytics_storage: 'denied' });
          var cookieNames = ['_ga', '_gid', '_gat'];
          var domains = ['.ki-agenten.shop', 'ki-agenten.shop'];
          cookieNames.forEach(function (name) {
            domains.forEach(function (domain) {
              document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + domain + ';';
            });
          });
          document.cookie.split(';').forEach(function (c) {
            var name = c.trim().split('=')[0];
            if (/^_ga_/.test(name)) {
              domains.forEach(function (domain) {
                document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + domain + ';';
              });
            }
          });
        }
      },
      required: false,
      optOut: false,
      onlyOnce: false
    },

    // ── Marketing ─────────────────────────────────────────────────────────────
    {
      name: 'linkedin-insight',
      title: 'LinkedIn Insight Tag',
      purposes: ['marketing'],
      // LinkedIn cookies live on linkedin.com domain — listed for transparency
      cookies: [
        [/^li_fat_id/, '/', '.ki-agenten.shop'],
        [/^li_/, '/', '.linkedin.com'],
        [/^lidc/, '/', '.linkedin.com'],
        [/^AnalyticsSyncHistory/, '/', '.linkedin.com'],
        [/^UserMatchHistory/, '/', '.linkedin.com']
      ],
      callback: function (consent, service) {
        if (!consent) {
          // Revoke ad consent when user withdraws
          if (typeof window.gtag === 'function') {
            window.gtag('consent', 'update', {
              ad_storage: 'denied',
              ad_user_data: 'denied',
              ad_personalization: 'denied'
            });
          }
          return;
        }
        if (window._linkedInInsightLoaded) return;
        window._linkedInInsightLoaded = true;

        var partnerId = KI_PIXEL_CONFIG.linkedInPartnerId;
        if (!partnerId || partnerId.indexOf('PLACEHOLDER') !== -1) {
          console.warn('[ki-agenten] LinkedIn Partner ID not configured — Insight Tag not loaded.');
          return;
        }

        window._linkedin_partner_id = partnerId;
        window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
        window._linkedin_data_partner_ids.push(partnerId);

        (function (l) {
          if (!l) { window.lintrk = function (a, b) { window.lintrk.q.push([a, b]); }; window.lintrk.q = []; }
          var s = document.getElementsByTagName('script')[0];
          var b = document.createElement('script');
          b.type = 'text/javascript'; b.async = true;
          b.src = 'https://snap.licdn.com/li.lms-analytics/insight.min.js';
          s.parentNode.insertBefore(b, s);
        })(window.lintrk);

        if (typeof window.gtag === 'function') {
          window.gtag('consent', 'update', {
            ad_storage: 'granted',
            ad_user_data: 'granted',
            ad_personalization: 'granted'
          });
        }
      },
      required: false,
      optOut: false,
      onlyOnce: true
    },

    {
      name: 'google-ads',
      title: 'Google Ads',
      purposes: ['marketing'],
      cookies: [
        [/^_gcl_au/, '/', '.ki-agenten.shop'],
        [/^_gcl_aw/, '/', '.ki-agenten.shop'],
        [/^_gcl_dc/, '/', '.ki-agenten.shop']
      ],
      callback: function (consent, service) {
        if (!consent) {
          if (typeof window.gtag === 'function') {
            window.gtag('consent', 'update', {
              ad_storage: 'denied',
              ad_user_data: 'denied',
              ad_personalization: 'denied'
            });
          }
          return;
        }
        if (window._googleAdsLoaded) return;
        window._googleAdsLoaded = true;

        var tagId = KI_PIXEL_CONFIG.googleAdsTagId;
        if (!tagId || tagId.indexOf('PLACEHOLDER') !== -1) {
          console.warn('[ki-agenten] Google Ads Tag ID not configured — tag not loaded.');
          return;
        }

        if (typeof window.gtag === 'function') {
          window.gtag('consent', 'update', {
            ad_storage: 'granted',
            ad_user_data: 'granted',
            ad_personalization: 'granted'
          });
          // Google Ads tag reuses the existing gtag.js — just config the additional ID
          window.gtag('config', tagId);
        } else {
          var s = document.createElement('script');
          s.async = true;
          s.src = 'https://www.googletagmanager.com/gtag/js?id=' + tagId;
          document.head.appendChild(s);
        }
      },
      required: false,
      optOut: false,
      onlyOnce: true
    }

    // ── Meta Pixel (WARTEN — CULA-17 P2.3 + CULA-22 required) ────────────────
    // Uncomment after Meta-Setup in CULA-17 is complete.
    // Replace META_PIXEL_ID_PLACEHOLDER with actual Pixel ID.
    //
    // , {
    //   name: 'meta-pixel',
    //   title: 'Meta Pixel (Facebook)',
    //   purposes: ['marketing'],
    //   cookies: [
    //     [/^_fbp/, '/', '.ki-agenten.shop'],
    //     [/^_fbc/, '/', '.ki-agenten.shop']
    //   ],
    //   callback: function (consent, service) {
    //     if (!consent || window._metaPixelLoaded) return;
    //     window._metaPixelLoaded = true;
    //     var pixelId = 'META_PIXEL_ID_PLACEHOLDER';
    //     !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    //       n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    //       n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    //       t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
    //       (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    //     fbq('init', pixelId);
    //     fbq('track', 'PageView');
    //   },
    //   required: false,
    //   optOut: false,
    //   onlyOnce: true
    // }
  ]
};
