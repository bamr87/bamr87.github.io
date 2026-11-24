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
    window.matchMedia('(min-width: 901px)').addEventListener('change', function (m) { if (m.matches) setNav(false); });
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
    }, { rootMargin: '-160px 0px -60% 0px' });
    doc.querySelectorAll('.menu-card').forEach(function (s) { io.observe(s); });
  }

  /* ---------- featured carousel: previous / next ---------- */
  doc.querySelectorAll('[data-carousel]').forEach(function (car) {
    var track = car.querySelector('.carousel-track');
    var prev = car.querySelector('.carousel-prev');
    var next = car.querySelector('.carousel-next');
    if (!track || !prev || !next) return;
    function step(dir) {
      var slide = track.querySelector('.slide');
      var by = slide ? slide.getBoundingClientRect().width + 20 : track.clientWidth * 0.8;
      track.scrollBy({ left: dir * by, behavior: 'smooth' });
    }
    function edges() {
      prev.disabled = track.scrollLeft <= 4;
      next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    }
    prev.hidden = false; next.hidden = false; // the buttons exist only for visitors with JavaScript
    prev.addEventListener('click', function () { step(-1); });
    next.addEventListener('click', function () { step(1); });
    track.addEventListener('scroll', edges, { passive: true });
    edges();
  });

  /* ---------- message forms: compose a WhatsApp message or an email ----------
     The destinations come from window.BEIT_CONTACT, a constant the build writes into the page,
     never from HTML attributes. Each filled-in field becomes a "Label: value" line, and everything
     the visitor typed is URI-encoded before it goes into a link. */
  var contact = window.BEIT_CONTACT;
  var MAIL_OK = /^[^\s@<>"'()]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
  var WA_OK = /^https:\/\/wa\.me\/\d{6,15}$/;
  var SUBJECTS = { 'catering-form': 'Party tray request', 'contact-form': 'Message' };
  if (contact && MAIL_OK.test(contact.mail) && WA_OK.test(contact.wa)) {
    doc.querySelectorAll('[data-composer]').forEach(function (form) {
      var out = form.querySelector('.form-status');
      form.addEventListener('submit', function (e) {
        e.preventDefault(); // without this script the form falls back to its mailto: action
        if (!form.reportValidity()) return;
        var via = (e.submitter && e.submitter.value) || 'whatsapp';
        var lines = [], name = '';
        Array.prototype.forEach.call(form.elements, function (el) {
          if (!el.name || el.type === 'submit' || !String(el.value).trim()) return;
          var value = String(el.value).trim();
          if (el.name === 'name') { name = value; return; }
          var text = el.labels && el.labels[0] ? el.labels[0].textContent.replace(/\s*\(optional\)\s*$/i, '').trim() : el.name;
          lines.push(text + ': ' + value);
        });
        var message = 'Hi Beit Shawarma, this is ' + name + '.\n\n' + lines.join('\n');
        if (via === 'email') {
          var subject = (SUBJECTS[form.id] || 'Message') + ' from ' + name;
          window.location.href = 'mailto:' + contact.mail +
            '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(message);
          if (out) out.textContent = 'Opening your email app with your message filled in.';
        } else {
          window.open(contact.wa + '?text=' + encodeURIComponent(message), '_blank', 'noopener');
          if (out) out.textContent = 'Opening WhatsApp with your message filled in.';
        }
      });
    });
  }

  /* ---------- map: load Google Maps only when asked ----------
     The iframe sits inert in a <template> until the visitor asks; it is cloned, never rebuilt
     from attribute text. */
  doc.querySelectorAll('.map-frame').forEach(function (frame) {
    var btn = frame.querySelector('[data-load-map]');
    var tpl = frame.querySelector('template[data-map-template]');
    if (!btn || !tpl) return;
    btn.hidden = false; // the button only exists for visitors with JavaScript
    btn.addEventListener('click', function () {
      frame.replaceChildren(tpl.content.cloneNode(true));
      var iframe = frame.querySelector('iframe');
      if (iframe) iframe.focus();
    });
  });

  /* ---------- footer year ---------- */
  doc.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
})();
