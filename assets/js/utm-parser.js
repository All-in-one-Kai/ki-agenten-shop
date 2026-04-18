/**
 * UTM Parameter Parser — ki-agenten.shop
 * Issue: CULA-47
 *
 * UTM schema: utm_source=<channel>&utm_medium=paid&utm_campaign=<slug>&utm_content=<ad_id>
 *
 * Attribution model:
 *   - session-touch: stored in sessionStorage (cleared when tab closes)
 *   - first-touch:   stored in localStorage  (persists across sessions)
 *
 * Pushes utm_captured event to window.dataLayer so GA4/GTM can map these
 * as Custom Dimensions (configure in GA4 Admin → Custom Definitions).
 *
 * Required GA4 Custom Dimensions (configure once in GA4 Admin):
 *   utm_source    — Event-scoped
 *   utm_medium    — Event-scoped
 *   utm_campaign  — Event-scoped
 *   utm_content   — Event-scoped
 *   utm_term      — Event-scoped
 */
(function () {
  var SESSION_KEY = 'ki_utm_session';
  var FIRST_TOUCH_KEY = 'ki_utm_first_touch';

  function parseUTMs() {
    var params = new URLSearchParams(window.location.search);
    var utm = {
      source: params.get('utm_source') || '',
      medium: params.get('utm_medium') || '',
      campaign: params.get('utm_campaign') || '',
      content: params.get('utm_content') || '',
      term: params.get('utm_term') || ''
    };
    return utm.source ? utm : null;
  }

  function safeGet(storage, key) {
    try { return JSON.parse(storage.getItem(key)); } catch (e) { return null; }
  }

  function safeSet(storage, key, value) {
    try { storage.setItem(key, JSON.stringify(value)); } catch (e) {}
  }

  function pushToDataLayer(utm, touchType) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'utm_captured',
      utm_source: utm.source,
      utm_medium: utm.medium,
      utm_campaign: utm.campaign,
      utm_content: utm.content,
      utm_term: utm.term,
      utm_touch_type: touchType
    });
  }

  var currentUTMs = parseUTMs();
  var sessionUTMs = safeGet(sessionStorage, SESSION_KEY);
  var firstTouchUTMs = safeGet(localStorage, FIRST_TOUCH_KEY);

  if (currentUTMs) {
    safeSet(sessionStorage, SESSION_KEY, currentUTMs);
    sessionUTMs = currentUTMs;
    if (!firstTouchUTMs) {
      safeSet(localStorage, FIRST_TOUCH_KEY, currentUTMs);
      firstTouchUTMs = currentUTMs;
    }
  }

  if (sessionUTMs) pushToDataLayer(sessionUTMs, 'session');
  if (firstTouchUTMs && (!sessionUTMs || firstTouchUTMs.source !== sessionUTMs.source)) {
    pushToDataLayer(firstTouchUTMs, 'first_touch');
  }

  // Expose for ga4-events.js enrichment
  window.kiUTM = {
    session: sessionUTMs,
    firstTouch: firstTouchUTMs
  };
})();
