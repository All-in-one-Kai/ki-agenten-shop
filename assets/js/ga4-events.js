/**
 * GA4 Conversion Event Tracking — ki-agenten.shop
 * Issue: CULA-47
 *
 * Events:
 *   ki_analyse_start     — Calendly link clicked on /potenzialanalyse/   (value: 0 EUR)
 *   ki_analyse_complete  — Calendly booking confirmed (postMessage)        (value: 80 EUR)
 *   roi_calculator_start — First input interaction on /roi-rechner/       (value: 0 EUR)
 *   newsletter_signup    — form[data-ki-form="newsletter"] submitted       (value: 20 EUR)
 *   contact_form_submit  — form[data-ki-form="contact"] submitted          (value: 60 EUR)
 *   calendly_booked      — Calendly booking confirmed (any page)           (value: 100 EUR)
 *
 * Depends on:
 *   - utm-parser.js loaded first (window.kiUTM)
 *   - gtag function from GA4 snippet (consent-gated via CULA-22)
 *
 * To mark events as Conversions: GA4 Admin → Events → toggle "Mark as conversion"
 * for: ki_analyse_complete, contact_form_submit, calendly_booked, newsletter_signup
 */
(function () {

  function utmParams() {
    var utm = (window.kiUTM && window.kiUTM.session) || {};
    var p = {};
    if (utm.source)   p.utm_source   = utm.source;
    if (utm.medium)   p.utm_medium   = utm.medium;
    if (utm.campaign) p.utm_campaign = utm.campaign;
    if (utm.content)  p.utm_content  = utm.content;
    return p;
  }

  function send(name, params) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', name, Object.assign({ page_location: window.location.href }, utmParams(), params || {}));
  }

  var _fired = {};
  function once(name, params) {
    if (_fired[name]) return;
    _fired[name] = true;
    send(name, params);
  }

  var path = window.location.pathname;

  // ── ki_analyse_start ───────────────────────────────────────────────────────
  // Fires when user clicks any Calendly link on the Potenzialanalyse page.
  // Calendly is the only CTA — clicking it IS starting the analysis.
  if (path.indexOf('potenzialanalyse') !== -1 || path.indexOf('ki-potenzialanalyse') !== -1) {
    document.addEventListener('click', function (e) {
      var el = e.target && e.target.closest('a[href*="calendly"]');
      if (el) once('ki_analyse_start', { currency: 'EUR', value: 0 });
    });
  }

  // ── roi_calculator_start ───────────────────────────────────────────────────
  // Fires on first focus/change of any input or select on the ROI calculator page.
  if (path.indexOf('roi-rechner') !== -1 || path.indexOf('roi-calculator') !== -1) {
    function roiStart() { once('roi_calculator_start', { currency: 'EUR', value: 0 }); }
    document.addEventListener('focus', function (e) {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT')) roiStart();
    }, true);
    document.addEventListener('change', function (e) {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT')) roiStart();
    });
  }

  // ── contact_form_submit ────────────────────────────────────────────────────
  // Requires form to have data-ki-form="contact" attribute (added in CULA-15).
  document.addEventListener('submit', function (e) {
    if (e.target && e.target.closest('form[data-ki-form="contact"]')) {
      send('contact_form_submit', { currency: 'EUR', value: 60 });
    }
  });

  // ── newsletter_signup ──────────────────────────────────────────────────────
  // Requires form to have data-ki-form="newsletter" attribute.
  document.addEventListener('submit', function (e) {
    if (e.target && e.target.closest('form[data-ki-form="newsletter"]')) {
      send('newsletter_signup', { currency: 'EUR', value: 20 });
    }
  });

  // ── calendly_booked + ki_analyse_complete ──────────────────────────────────
  // Calendly fires a postMessage event when a booking is confirmed.
  // Spec: https://help.calendly.com/hc/en-us/articles/223195488
  window.addEventListener('message', function (e) {
    if (!e.data || typeof e.data !== 'object') return;
    if (e.data.event !== 'calendly.event_scheduled') return;

    send('calendly_booked', { currency: 'EUR', value: 100 });

    // On Potenzialanalyse pages a Calendly booking = analysis complete
    if (path.indexOf('potenzialanalyse') !== -1 || path.indexOf('ki-potenzialanalyse') !== -1) {
      send('ki_analyse_complete', { currency: 'EUR', value: 80 });
    }
  });

})();
