# Connect Public — Site Improvement Suggestions

A practical, ranked list of upgrades for the resume site so you can:

- Know **how many people** visit, **where** they come from, and **what** they do.
- Capture **who wants to connect** with you (name, email, company, message).
- Turn visitors into meetings, conversations, and follow-ups.

> Companion to `design.md`. No code is changed by this document — it is a roadmap.

---

## 1. Quick summary

**Current state**

- Static site built with HTML + CSS + JS + Vite (`package.json`).
- Contact in `index.html` (`#contact` section, ~lines 305–321) is just a `mailto:` link, a `tel:` link, LinkedIn, and GitHub.
- No analytics, no form backend, no scheduler, no chat, no PDF download.

**Hard truth about "who viewed my profile"**

- A plain website (unlike LinkedIn) **cannot show the real name** of every visitor. Browsers do not give that info.
- What you *can* know:
  1. **How many** visitors, from **which country/city/device/source** (analytics).
  2. **What they did** on the page — scroll depth, clicks, recordings (Microsoft Clarity).
  3. **Who they are** — *only when they identify themselves* via a contact form, scheduler, chat, or gated download.
  4. **Which company** they came from — possible for B2B traffic via tools like Leadfeeder / RB2B (reveals company, not person).

The rest of this doc is how to add each of those.

---

## 2. Know who visits your profile (visitor analytics)

| Tool | Why pick it | Free tier | Effort |
|---|---|---|---|
| **Microsoft Clarity** | Heatmaps + **session recordings** — literally watch how visitors scroll and click | Unlimited free | 5 min |
| **Google Analytics 4** | Industry standard, full funnel, integrates with Google Search Console | Free | 10 min |
| **Plausible / Umami** | Privacy-friendly, lightweight (~1 KB), simple dashboard, GDPR-safe | Plausible paid, Umami self-host free | 10 min |
| **Vercel / Netlify / Cloudflare Web Analytics** | One-click if you host there, no cookies | Free | 1 min |

**Recommended combo:** Microsoft Clarity (qualitative) + GA4 or Plausible (quantitative).

**Where to add:** a `<script>` tag in the `<head>` of `index.html`, just before `</head>`.

---

## 3. Know who wants to connect with you (lead capture)

Replace the bare `mailto:` button with a real contact form. Visitors fill it in, you get an email + dashboard entry with their details.

**Form backends (no server needed)**

- **Web3Forms** — free, unlimited submissions, just an access key.
- **Formspree** — free 50 submissions/month, very polished.
- **Getform** / **Formsubmit** — similar, free tiers.
- **EmailJS** — send mail directly from `script.js`.
- **Netlify Forms** — free if you host on Netlify, zero config (`<form netlify>`).

**Suggested fields**

- Name *
- Email *
- Company / Organization
- Role (Recruiter, Founder, Engineer, Other)
- Message *
- "How did you find me?" (LinkedIn, Google, Referral, Other)
- Optional: phone or LinkedIn URL

**Auto-notify yourself the second someone submits**

- Email (default).
- **Telegram bot** webhook → instant phone ping.
- **Discord** / **Slack** webhook → desktop ping.
- Google Sheet append (via Zapier/Make/n8n) → permanent log.

**Where to add:** rewrite the `.contact-actions` block in `index.html` (~lines 313–319) into a `<form>`.

---

## 4. Schedule a call (turn visitors into meetings)

A "Book a 15-min intro call" button has the highest conversion of all CTAs for resume sites.

- **Cal.com** — open source, free, self-host option.
- **Calendly** — most recognized, free tier.
- **TidyCal** — one-time payment, no subscription.

Place a button next to the existing "Resume" / "LinkedIn" buttons in the header and the contact section. Embed inline or popup-on-click.

---

## 5. Live chat / DM

For visitors who do not want to fill a form but still have a question.

- **Tawk.to** — free forever, mobile app to reply on the go.
- **Crisp** — slicker UI, free tier with 2 seats.
- **WhatsApp Click-to-Chat** — `https://wa.me/917058774113` — most natural for an India-based audience and recruiters in your timezone.
- **Telegram link** — `https://t.me/yourusername`.

Add a small floating bubble bottom-right, or as another secondary button in `#contact`.

---

## 6. LinkedIn-style "who viewed me" alternatives

Since a static site cannot identify individual visitors by name, here is the closest you can get:

- **LinkedIn Insight Tag** — if you ever run LinkedIn ads, gives company-level visitor demographics.
- **Leadfeeder / RB2B / Albacross / Lead Forensics** — reveal the **company** (not person) of B2B visitors via IP lookup.
- **Gated resume PDF** — visitors must enter name + email before the download link unlocks. Captures recruiters cleanly.
- **UTM tagging** — share different links on LinkedIn / GitHub / email signature with `?utm_source=linkedin` so you can see which channel sent which traffic.
- **Custom short links** (Bitly, Dub.co) per audience to track click-throughs.

---

## 7. Newsletter / stay in touch

A soft connect path for people who are not hiring *today* but might in 6 months.

- **Buttondown** — minimal, dev-friendly, free up to 100 subs.
- **Beehiiv** — free up to 2,500 subs, great analytics.
- **Substack** — free, easy embed.
- **ConvertKit / Kit** — free up to 10,000 subs.

Pitch line: "Get notified when I publish QA automation tips, framework reviews, and AI-in-testing experiments."

---

## 8. Trust and credibility upgrades

These do not directly capture leads but they make people *want* to connect.

- **Testimonials / recommendations carousel** — pull 2–3 short quotes from your LinkedIn recommendations.
- **Live GitHub stats card** — `github-readme-stats`, contribution graph, language breakdown.
- **Case-study pages per project** — instead of cards-only, build `/projects/novon.html`, `/projects/myzenscribe.html` with screenshots, problem/solution, metrics ("cut post-release defects by 20%").
- **Short intro video** — 30–60 second Loom or YouTube embed in the hero or About section.
- **Downloadable PDF resume** — currently the header "Resume" link is `mailto:`. Replace with a real `Prajyot-Ingale-Resume.pdf` download.
- **Press / media logos** — if your work has been featured anywhere, add a "As seen on" strip.
- **Live availability badge** — "Open to roles · Surat / Remote" green dot in the hero.

---

## 9. Engagement and stickiness

- **Comments on project cards** — Giscus (uses GitHub Discussions, free, no DB).
- **Skill endorsements** — emoji reactions on the Skills section (Supabase + a row count).
- **Public guestbook** — visitors leave a name + short note; you see them all (Firebase / Supabase / Upstash Redis).
- **Visit counter / "You are visitor #1234"** — old-school but charming.
- **Like button** — heart icon on each project that anyone can tap (Upstash + IP rate-limit).

---

## 10. SEO and discoverability

So more people find the site in the first place.

- **Open Graph + Twitter Card** meta tags in `<head>` of `index.html` — controls the preview when the link is shared on LinkedIn/WhatsApp/Twitter. Currently missing.
- **JSON-LD `Person` schema** — gives Google a structured profile, can show rich results.
- **`sitemap.xml`** and **`robots.txt`** at the project root.
- **Custom domain** — e.g. `prajyot.dev`, `prajyotingale.com`. Costs ~$10–15/year, big trust boost over a `*.netlify.app` subdomain.
- **Google Search Console** — verify the site, watch which queries bring traffic.
- **Bing Webmaster Tools** + **DuckDuckGo** submission.
- **Canonical URL** + `lang="en"` already set, good.

---

## 11. Performance and PWA

A faster, installable site keeps visitors longer (and converts better).

- Convert `assets/hero-portrait.png` to **AVIF / WebP**, add `<picture>` fallback.
- Add `loading="lazy"` to all non-hero images.
- Add a `manifest.json` + service worker → site becomes **installable on phone home-screen**.
- Add a real **favicon set** (16, 32, 180, 512) — currently none.
- Target **Lighthouse 95+** on all four categories.
- Self-host fonts if you ever add Google Fonts (avoid layout shift).

---

## 12. Privacy and legal

Once analytics and forms are live, you legally need:

- A small **cookie / consent banner** if you use GA4 (cookies). Tools: Cookie Consent by Osano (free), Termly.
- A simple **`/privacy.html`** page listing what is collected (analytics, form submissions) and how to email you for deletion.
- A **`/terms.html`** if you ever sell or accept payment.
- Reference India's DPDP Act 2023 + GDPR if you receive EU traffic.

---

## 13. Suggested 1-week rollout order

| Day | Add | Outcome |
|---|---|---|
| 1 | Microsoft Clarity + GA4 | You can see traffic, devices, and recordings tomorrow |
| 2 | Web3Forms contact form + Telegram webhook | Real leads land in your phone |
| 3 | Cal.com / Calendly button + WhatsApp link | One-click booking + chat |
| 4 | Open Graph tags + JSON-LD + favicon set | Link previews and Google look professional |
| 5 | Gated PDF resume download + LinkedIn recommendations section | Capture recruiter emails |
| 6 | Testimonials + GitHub stats card + project case-study pages | Trust uplift |
| 7 | Deploy to custom domain on Netlify/Vercel; verify analytics + Search Console | Production-grade |

---

## 14. Tools cheat-sheet

| Goal | Tool | Free tier | Link |
|---|---|---|---|
| Heatmaps + recordings | Microsoft Clarity | Unlimited | clarity.microsoft.com |
| Web analytics | Google Analytics 4 | Free | analytics.google.com |
| Privacy analytics | Plausible | Paid | plausible.io |
| Self-host analytics | Umami | Free (self-host) | umami.is |
| Contact form | Web3Forms | Unlimited | web3forms.com |
| Contact form | Formspree | 50/mo | formspree.io |
| Email from JS | EmailJS | 200/mo | emailjs.com |
| Scheduler | Cal.com | Free | cal.com |
| Scheduler | Calendly | Free | calendly.com |
| Live chat | Tawk.to | Free | tawk.to |
| Live chat | Crisp | Free 2 seats | crisp.chat |
| WhatsApp deep-link | wa.me | Free | wa.me |
| B2B visitor reveal | Leadfeeder / RB2B | Trial | leadfeeder.com / rb2b.com |
| Newsletter | Buttondown | 100 subs | buttondown.email |
| Newsletter | Beehiiv | 2.5k subs | beehiiv.com |
| Comments | Giscus | Free | giscus.app |
| Realtime DB | Supabase / Firebase / Upstash | Generous free | supabase.com |
| Cookie banner | Osano Cookie Consent | Free | osano.com |
| Hosting + forms | Netlify | Free | netlify.com |
| Hosting + analytics | Vercel | Free | vercel.com |
| Domain | Namecheap / Cloudflare Registrar | ~$10/yr | cloudflare.com |
| Search Console | Google Search Console | Free | search.google.com/search-console |

---

## 15. What to do first (if you only do one thing this week)

**Add Microsoft Clarity + a Web3Forms contact form with a Telegram notification.**

- Clarity tells you who is looking and what they care about.
- The form turns those views into real names, emails, and messages on your phone.

Everything else in this document is upside on top of that foundation.
