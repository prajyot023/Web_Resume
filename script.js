(function () {
  /* Always land on the top of the page on refresh / reload instead of
     restoring the previous scroll position. */
  if ("scrollRestoration" in history) {
    history.scrollRestoration = "manual";
  }
  try {
    window.scrollTo(0, 0);
  } catch (e) {
    /* no-op */
  }
  window.addEventListener("beforeunload", () => {
    try {
      window.scrollTo(0, 0);
    } catch (e) {
      /* no-op */
    }
  });
  window.addEventListener("load", () => {
    try {
      window.scrollTo(0, 0);
    } catch (e) {
      /* no-op */
    }
  });

  const progress = document.querySelector(".scroll-progress");
  const reveals = document.querySelectorAll(".reveal");
  const metricCards = document.querySelectorAll(".metric-card");
  const rotatingRole = document.querySelector("[data-rotating-role]");
  const navLinks = document.querySelectorAll(".primary-nav a");
  const portraitRail = document.querySelector(".portrait-rail");
  const heroContent = document.querySelector(".editorial-hero .hp-content");
  const scrollHint = document.querySelector(".hp-scroll-hint");
  const dearVisitor = document.querySelector("[data-dear-visitor]");
  const backToTopLink = document.querySelector('.site-footer a.footer-link[href="#top"]');
  const themeToggle = document.querySelector("[data-theme-toggle]");
  const contactForm = document.getElementById("contact-form");
  const formStatus = document.getElementById("form-status");
  const leadSource = document.getElementById("lead-source");
  const cookieBanner = document.getElementById("cookie-banner");
  const acceptCookiesButton = document.getElementById("accept-cookies");

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const prefersLightScheme = window.matchMedia("(prefers-color-scheme: light)").matches;

  function applyTheme(theme) {
    if (theme === "light") {
      document.documentElement.dataset.theme = "light";
    } else {
      delete document.documentElement.dataset.theme;
    }

    if (themeToggle) {
      const isLight = theme === "light";
      themeToggle.setAttribute("aria-pressed", isLight ? "true" : "false");
      themeToggle.setAttribute("aria-label", isLight ? "Switch to dark mode" : "Switch to light mode");
      themeToggle.title = isLight ? "Dark mode" : "Light mode";
    }
  }

  function initTheme() {
    const saved = window.localStorage.getItem("pf-theme");
    if (saved === "light" || saved === "dark") {
      applyTheme(saved);
      return;
    }
    applyTheme(prefersLightScheme ? "light" : "dark");
  }

  initTheme();

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const current = document.documentElement.dataset.theme === "light" ? "light" : "dark";
      const next = current === "light" ? "dark" : "light";
      window.localStorage.setItem("pf-theme", next);
      applyTheme(next);
    });
  }

  const sections = [...navLinks]
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  const roles = [
    "Playwright Expert",
    "Cypress Expert",
    "Selenium Engineer",
    "AI-Driven Testing",
    "API Automation",
    "CI/CD Pipelines"
  ];
  let roleIndex = 0;

  function desktopMq() {
    return window.matchMedia("(min-width: 901px)").matches;
  }

  function railEndWidthPx() {
    const iw = window.innerWidth;
    return Math.min(Math.max(330, iw * 0.35), 720);
  }

  function clearDesktopRailStyles() {
    if (!portraitRail) return;
    portraitRail.style.width = "";
    portraitRail.style.borderLeftColor = "";
    portraitRail.classList.remove("is-collapsed");
  }

  function applyReducedMotionLayout() {
    if (!portraitRail || !desktopMq()) return;
    portraitRail.style.width = `${railEndWidthPx()}px`;
    portraitRail.style.borderLeftColor = "rgba(255, 255, 255, 0.08)";
    portraitRail.classList.add("is-collapsed");
    if (heroContent) heroContent.style.transform = "";
  }

  window.addEventListener(
    "resize",
    () => {
      if (!desktopMq()) {
        clearDesktopRailStyles();
        if (heroContent) heroContent.style.transform = "";
      } else if (prefersReducedMotion) {
        applyReducedMotionLayout();
      }
    },
    { passive: true }
  );

  /** Full-screen portrait → narrows into right rail; hero copy slides left (-X). */
  (function scrollSplitHero() {
    if (!portraitRail) return;

    if (prefersReducedMotion) {
      applyReducedMotionLayout();
      return;
    }

    let current = 0;

    function heroProgress() {
      const span = Math.max(1, window.innerHeight * 0.92);
      return Math.min(1, window.scrollY / span);
    }

    function tick() {
      if (!desktopMq()) {
        requestAnimationFrame(tick);
        return;
      }

      const target = heroProgress();
      current += (target - current) * 0.085;

      const fullW = window.innerWidth;
      const endW = railEndWidthPx();
      const w = fullW - current * (fullW - endW);

      portraitRail.style.width = `${w}px`;
      portraitRail.style.borderLeftColor =
        current > 0.04 ? "rgba(255, 255, 255, 0.08)" : "transparent";

      portraitRail.classList.toggle("is-collapsed", current > 0.42);

      if (heroContent) {
        heroContent.style.transform = `translateX(${-current * 56}px)`;
      }

      if (scrollHint) {
        scrollHint.style.opacity = String(Math.max(0, 1 - current * 12));
      }

      requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }());

  function updateScrollProgress() {
    if (!progress) return;
    const pageHeight = document.documentElement.scrollHeight - window.innerHeight;
    const percentage = pageHeight > 0 ? (window.scrollY / pageHeight) * 100 : 0;
    progress.style.width = `${percentage}%`;
  }

  function setActiveNav() {
    const marker = window.scrollY + window.innerHeight * 0.35;
    let activeId = sections[0]?.id;

    sections.forEach((section) => {
      if (section.offsetTop <= marker) {
        activeId = section.id;
      }
    });

    navLinks.forEach((link) => {
      link.classList.toggle("is-active", link.getAttribute("href") === `#${activeId}`);
    });
  }

  function animateMetric(card) {
    if (card.dataset.animated === "true") {
      return;
    }

    card.dataset.animated = "true";

    const value = card.querySelector(".metric-value");
    const target = Number(card.dataset.count || 0);
    const duration = 1050;
    const start = performance.now();

    function tickMetric(now) {
      const progressValue = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progressValue, 3);
      value.textContent = Math.round(target * eased);

      if (progressValue < 1) {
        requestAnimationFrame(tickMetric);
      } else if (target === 95) {
        value.textContent = "95+";
      }
    }

    requestAnimationFrame(tickMetric);
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.target.classList.contains("skill-bars")) {
          entry.target.classList.toggle("is-visible", entry.isIntersecting);
          entry.target.closest(".pf-stack")?.classList.toggle("is-visible", entry.isIntersecting);
          return;
        }

        if (!entry.isIntersecting) {
          return;
        }

        entry.target.classList.add("is-visible");
        entry.target.closest(".pf-stack")?.classList.add("is-visible");

        if (entry.target.classList.contains("metric-card")) {
          animateMetric(entry.target);
        }

        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.18 }
  );

  reveals.forEach((element) => observer.observe(element));
  metricCards.forEach((card) => observer.observe(card));

  if (!prefersReducedMotion && rotatingRole) {
    setInterval(() => {
      roleIndex = (roleIndex + 1) % roles.length;
      rotatingRole.animate(
        [
          { opacity: 1, transform: "translateY(0)" },
          { opacity: 0, transform: "translateY(-8px)" },
          { opacity: 0, transform: "translateY(8px)" },
          { opacity: 1, transform: "translateY(0)" }
        ],
        { duration: 480, easing: "ease", fill: "both" }
      );
      window.setTimeout(() => {
        rotatingRole.textContent = roles[roleIndex];
      }, 210);
    }, 2400);
  }

  document.querySelectorAll("[data-tilt]").forEach((card) => {
    card.addEventListener("pointermove", (event) => {
      if (prefersReducedMotion) {
        return;
      }

      const bounds = card.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width - 0.5;
      const y = (event.clientY - bounds.top) / bounds.height - 0.5;
      card.style.transform = `perspective(900px) rotateX(${y * -3}deg) rotateY(${x * 4}deg)`;
    });

    card.addEventListener("pointerleave", () => {
      card.style.transform = "";
    });
  });

  (function scrollDearVisitor() {
    if (!dearVisitor) return;

    const left = dearVisitor.querySelector(".dear-visitor-left");

    if (!left) return;

    const shell = dearVisitor.closest(".dear-visitor-shell");
    if (!shell) return;

    /* Split the message body into word spans so each word can
       blur/fade in with a stagger driven by --i in CSS. */
    const message = left.querySelector(".dear-visitor-message");
    if (message && !message.dataset.split) {
      const text = message.textContent.trim().replace(/\s+/g, " ");
      const words = text.split(" ");
      message.textContent = "";
      words.forEach((word, index) => {
        const span = document.createElement("span");
        span.className = "dv-word";
        span.style.setProperty("--i", String(index));
        span.textContent = word;
        message.appendChild(span);
        if (index < words.length - 1) {
          message.appendChild(document.createTextNode(" "));
        }
      });
      message.dataset.split = "true";
    }

    /* Trigger the staggered letter reveal every time the section
       scrolls into view. When it leaves the viewport we strip the
       class (and briefly disable transitions) so the next entry
       replays the animation from the beginning — both on scroll
       down and scroll back up. */
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            left.classList.remove("dv-reset");
            left.classList.add("is-revealed");
          } else {
            if (left.classList.contains("is-revealed")) {
              left.classList.add("dv-reset");
              left.classList.remove("is-revealed");
              /* Force reflow so the reset state is applied before
                 we drop the dv-reset class, otherwise the browser
                 would batch the class changes and we'd see the
                 transition animate back to zero. */
              // eslint-disable-next-line no-unused-expressions
              left.offsetWidth;
              requestAnimationFrame(() => {
                left.classList.remove("dv-reset");
              });
            }
          }
        });
      },
      { threshold: 0.25 }
    );
    revealObserver.observe(left);

    if (prefersReducedMotion) {
      left.classList.add("is-revealed");
      left.style.opacity = "";
      return;
    }

    const contact = document.getElementById("contact");

    let current = 0;

    /* Drive the reveal off the Contact section's midpoint so the letter
       starts fading in once the visitor is halfway through Contact, and
       finishes by the time the dear-visitor shell reaches the viewport top. */
    function dvProgress() {
      if (contact) {
        const contactRect = contact.getBoundingClientRect();
        const shellRect = shell.getBoundingClientRect();
        const contactMid = contactRect.top + contactRect.height / 2;

        /* Distance (in px) from the current scroll position to:
             - start: contact midpoint hits the viewport center
             - end:   dear-visitor shell hits the viewport top */
        const distToStart = contactMid - window.innerHeight / 2;
        const distToEnd = shellRect.top;
        const span = distToEnd - distToStart;

        if (span <= 0) return distToEnd <= 0 ? 1 : 0;
        return Math.min(1, Math.max(0, -distToStart / span));
      }

      const rect = shell.getBoundingClientRect();
      const span = Math.max(1, shell.offsetHeight - window.innerHeight);
      return Math.min(1, Math.max(0, (0 - rect.top) / span));
    }

    function tick() {
      const target = dvProgress();
      current += (target - current) * 0.09;

      /* Keep copy aligned with page padding; fade in as the letter scrolls into view. */
      left.style.transform = "";
      left.style.opacity = String(Math.min(1, Math.max(0, current * 1.15)));

      requestAnimationFrame(tick);
    }

    left.style.opacity = "0";
    requestAnimationFrame(tick);
  }());

  window.addEventListener("scroll", () => {
    updateScrollProgress();
    setActiveNav();
    if (backToTopLink) {
      backToTopLink.classList.toggle("is-hidden", window.scrollY < window.innerHeight * 0.4);
    }
  }, { passive: true });

  window.addEventListener("resize", updateScrollProgress);

  updateScrollProgress();
  setActiveNav();
  if (backToTopLink) {
    backToTopLink.classList.toggle("is-hidden", window.scrollY < window.innerHeight * 0.4);
  }

  if (leadSource) {
    const source = new URLSearchParams(window.location.search).get("utm_source") || "direct";
    leadSource.value = source;
  }

  if (contactForm) {
    contactForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(contactForm);
      if (formStatus) formStatus.textContent = "Sending...";
      try {
        const response = await fetch(contactForm.action, {
          method: "POST",
          body: formData
        });
        if (!response.ok) {
          throw new Error("Submission failed");
        }
        contactForm.reset();
        if (leadSource) {
          const source = new URLSearchParams(window.location.search).get("utm_source") || "direct";
          leadSource.value = source;
        }
        if (formStatus) formStatus.textContent = "Thanks! I got your message.";
      } catch (error) {
        if (formStatus) formStatus.textContent = "Could not send right now. Please email me directly.";
      }
    });
  }

  if (cookieBanner && acceptCookiesButton) {
    const consentGiven = window.localStorage.getItem("pf-cookie-consent") === "yes";
    if (!consentGiven) {
      cookieBanner.classList.add("is-visible");
    }
    acceptCookiesButton.addEventListener("click", () => {
      window.localStorage.setItem("pf-cookie-consent", "yes");
      cookieBanner.classList.remove("is-visible");
    });
  }

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("./sw.js").catch(() => {
        /* no-op */
      });
    });
  }

  /* ── Cursor code-sprinkle particles ───────────────────── */
  (function cursorSprinkle() {
    if (prefersReducedMotion) return;

    const codeChars = ["{", "}", "<", ">", "/", ";", "=", "(", ")", "//", "=>", "++", "&&", "||", "::", "[]", "!=", "0", "1"];
    const fgMixPercents = ["95%", "82%", "68%"];

    let particles = [];
    const MAX_PARTICLES = 140;
    let lastSpawn = 0;
    const THROTTLE_MS = 16;
    const PARTICLE_GAP_PX = 12; /* lower = more density */
    /* pointer events already report the cursor hotspot */
    const TIP_OFFSET_X = 0;
    const TIP_OFFSET_Y = 0;

    let lastX = null;
    let lastY = null;
    let lastT = null;

    function spawnParticle(x, y, vx = 0, vy = 0) {
      if (particles.length >= MAX_PARTICLES) return;

      const el = document.createElement("span");
      el.className = "cursor-particle";
      el.textContent = codeChars[Math.floor(Math.random() * codeChars.length)];

      /* Flow trajectory: trail follows cursor movement direction. */
      const speed = Math.hypot(vx, vy);
      const nx = speed > 0.001 ? vx / speed : 0;
      const ny = speed > 0.001 ? vy / speed : 1;

      /* Particles should stream *behind* the cursor. */
      const trailX = -nx;
      const trailY = -ny;

      /* Add subtle sideways jitter so the stream has volume. */
      const perpX = -trailY;
      const perpY = trailX;
      const spread = (Math.random() - 0.5) * 22;

      const baseDistance = 34 + Math.random() * 52;
      const distance = baseDistance + Math.min(70, speed * 0.22);

      const dx = trailX * distance + perpX * spread;
      const dy = trailY * distance + perpY * spread;

      const rot = Math.atan2(trailY, trailX) * (180 / Math.PI) + (Math.random() - 0.5) * 35;
      const duration = 600 + Math.random() * 500;
      const size = 10 + Math.random() * 6;

      el.style.left = `${x}px`;
      el.style.top = `${y}px`;
      el.style.fontSize = `${size}px`;
      el.style.setProperty(
        "--particle-fg",
        fgMixPercents[Math.floor(Math.random() * fgMixPercents.length)]
      );
      el.style.setProperty("--dx", `${dx}px`);
      el.style.setProperty("--dy", `${dy}px`);
      el.style.setProperty("--rot", `${rot}deg`);
      el.style.setProperty("--particle-duration", `${duration}ms`);

      document.body.appendChild(el);
      particles.push(el);

      const cleanupMs = duration + 120;
      const cleanupTimer = window.setTimeout(() => {
        if (!el.isConnected) return;
        el.remove();
        particles = particles.filter((p) => p !== el);
      }, cleanupMs);

      el.addEventListener("animationend", () => {
        window.clearTimeout(cleanupTimer);
        el.remove();
        particles = particles.filter((p) => p !== el);
      }, { once: true });
    }

    function onMove(e) {
      if (document.visibilityState === "hidden") return;

      const now = performance.now();
      if (now - lastSpawn < THROTTLE_MS) return;
      lastSpawn = now;

      /* Shift to cursor "tip" (arrow point) */
      const x = e.clientX + TIP_OFFSET_X;
      const y = e.clientY + TIP_OFFSET_Y;

      if (lastX == null || lastY == null || lastT == null) {
        lastX = x;
        lastY = y;
        lastT = now;
        spawnParticle(x, y, 0, 1);
        return;
      }

      const dx = x - lastX;
      const dy = y - lastY;
      const dist = Math.hypot(dx, dy);
      const dt = Math.max(1, now - lastT);
      const vx = dx / dt;
      const vy = dy / dt;

      /* Spawn more particles on faster moves */
      const count = Math.min(6, Math.max(1, Math.round(dist / PARTICLE_GAP_PX)));
      for (let i = 0; i < count; i += 1) {
        const t = count === 1 ? 1 : i / (count - 1);
        spawnParticle(lastX + dx * t, lastY + dy * t, vx, vy);
      }

      lastX = x;
      lastY = y;
      lastT = now;
    }

    document.addEventListener("pointermove", onMove, { passive: true });

    window.addEventListener("blur", () => {
      /* Avoid “stuck” particles if the tab loses focus mid-animation */
      particles.forEach((p) => p.remove());
      particles = [];
      lastX = null;
      lastY = null;
      lastT = null;
    });
  }());

})();
