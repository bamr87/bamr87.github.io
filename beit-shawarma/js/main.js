/* Beit Shawarma: small progressive enhancements. Every page works without this file. */
(function () {
  'use strict';
  var doc = document;
  var body = doc.body;

  /* ---------- mobile navigation ---------- */
  var toggle = doc.querySelector('.nav-toggle');
  var nav = doc.getElementById('site-nav');
  function setNav(open) {
    if (!toggle || !nav) return;
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setNav(toggle.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setNav(false); toggle.focus(); }
    });
    window.matchMedia('(min-width: 861px)').addEventListener('change', function (m) { if (m.matches) setNav(false); });
  }

  /* ---------- open / closed status, in the restaurant's time zone ---------- */
  var DAYS = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];
  var DAY_LONG = { Su: 'Sunday', Mo: 'Monday', Tu: 'Tuesday', We: 'Wednesday', Th: 'Thursday', Fr: 'Friday', Sa: 'Saturday' };
  function toMin(hhmm) { var p = hhmm.split(':'); return (+p[0]) * 60 + (+p[1]); }
  function label(min) {
    min = ((min % 1440) + 1440) % 1440;
    var h = Math.floor(min / 60), m = min % 60, ap = h < 12 ? 'AM' : 'PM';
    var h12 = h % 12 === 0 ? 12 : h % 12;
    return h12 + (m ? ':' + String(m).padStart(2, '0') : '') + ' ' + ap;
  }
  function nowIn(tz) {
    var parts = {};
    new Intl.DateTimeFormat('en-US', { timeZone: tz, weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
      .formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; });
    // "Mon" -> "Mo", "Thu" -> "Th": the first two letters match the codes in site.json.
    return { day: DAYS.indexOf(parts.weekday.slice(0, 2)), min: (+parts.hour % 24) * 60 + (+parts.minute) };
  }
  function spansFor(hours, dayIdx) {
    var code = DAYS[dayIdx], out = [];
    hours.forEach(function (h) {
      if (h.days.indexOf(code) === -1) return;
      var o = toMin(h.opens), c = toMin(h.closes);
      out.push({ open: o, close: c <= o ? c + 1440 : c });
    });
    return out;
  }
  function status(hours, tz) {
    var n = nowIn(tz), i, s;
    if (n.day < 0) return null;
    var today = spansFor(hours, n.day);
    var yest = spansFor(hours, (n.day + 6) % 7);
    for (i = 0; i < yest.length; i++) { // late-night spans that started yesterday
      if (yest[i].close > 1440 && n.min < yest[i].close - 1440) return { open: true, close: yest[i].close };
    }
    for (i = 0; i < today.length; i++) {
      s = today[i];
      if (n.min >= s.open && n.min < s.close) return { open: true, close: s.close, soon: s.close - n.min <= 60 };
    }
    for (i = 0; i < today.length; i++) if (n.min < today[i].open) return { open: false, next: today[i].open, when: 'today' };
    for (var d = 1; d <= 7; d++) {
      var spans = spansFor(hours, (n.day + d) % 7);
      if (spans.length) return { open: false, next: spans[0].open, when: d === 1 ? 'tomorrow' : DAY_LONG[DAYS[(n.day + d) % 7]] };
    }
    return null;
  }
  try {
    var hours = JSON.parse(body.getAttribute('data-hours') || '[]');
    var st = status(hours, body.getAttribute('data-tz') || 'America/Chicago');
    if (st) {
      var text = st.open
        ? (st.soon ? 'Closing soon · open until ' : 'Open now · until ') + label(st.close)
        : 'Closed now · opens ' + (st.when === 'today' ? 'today' : st.when) + ' at ' + label(st.next);
      doc.querySelectorAll('[data-open-status]').forEach(function (el) {
        el.classList.add(st.open ? 'is-open' : 'is-closed');
        var t = el.querySelector('.status-text');
        if (t) t.textContent = text;
      });
    }
  } catch (err) {
    /* Keep the static hours text that is already on the page. */
    if (window.console) console.warn('open-status:', err);
  }

  /* ---------- menu: highlight the section in view ---------- */
  var chipBar = doc.querySelector('.chips');
  if (chipBar && 'IntersectionObserver' in window) {
    var chips = {};
    chipBar.querySelectorAll('a').forEach(function (a) { chips[a.getAttribute('href').slice(1)] = a; });
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var a = chips[en.target.id];
        if (!a || a === current) return;
        if (current) current.removeAttribute('aria-current');
        a.setAttribute('aria-current', 'true');
        current = a;
        chipBar.scrollTo({ left: a.offsetLeft - chipBar.offsetLeft - 16, behavior: 'smooth' });
      });
    }, { rootMargin: '-140px 0px -60% 0px' });
    doc.querySelectorAll('.menu-section').forEach(function (s) { io.observe(s); });
  }

  /* ---------- contact: compose a WhatsApp message or an email ---------- */
  var form = doc.querySelector('[data-composer]');
  if (form) {
    var out = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var via = (e.submitter && e.submitter.value) || 'whatsapp';
      var name = form.elements.name.value.trim();
      var topic = form.elements.topic.value;
      var msg = form.elements.message.value.trim();
      var text = 'Hi Beit Shawarma, this is ' + name + '.\n\n[' + topic + ']\n' + msg;
      if (via === 'email') {
        var subject = topic + ' from ' + name;
        window.location.href = 'mailto:' + form.getAttribute('data-mail') +
          '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(text);
        if (out) out.textContent = 'Opening your email app with your message filled in.';
      } else {
        window.open(form.getAttribute('data-wa') + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
        if (out) out.textContent = 'Opening WhatsApp with your message filled in.';
      }
    });
  }

  /* ---------- map: load Google Maps only when asked ---------- */
  doc.querySelectorAll('.map-frame[data-map-src]').forEach(function (frame) {
    var btn = frame.querySelector('[data-load-map]');
    if (!btn) return;
    btn.hidden = false; // the button only exists for visitors with JavaScript
    btn.addEventListener('click', function () {
      var iframe = doc.createElement('iframe');
      iframe.src = frame.getAttribute('data-map-src');
      iframe.title = frame.getAttribute('data-map-title') || 'Map';
      iframe.setAttribute('allowfullscreen', '');
      iframe.referrerPolicy = 'no-referrer-when-downgrade';
      frame.replaceChildren(iframe);
      iframe.focus();
    });
  });

  /* ---------- footer year ---------- */
  doc.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
})();
