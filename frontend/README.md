# KisanAI — Frontend

Frontend for **KisanAI**, an AI farming assistant for small and marginal farmers in India (Hackathon Problem Statement 5 — AI for Public Good).

Built with **React + Vite + Tailwind CSS v4**, matching the PRD's recommended stack (`frontend/` folder, React/Next.js, mobile-first, deployable to Vercel).

## Design direction

- **Palette:** deep forest green (`#2F5233`) as the primary brand color, fresh-leaf green (`#8BAA4B`) for secondary accents, husked-rice off-white (`#FAF8F2`) as the base background, and a marigold/turmeric warm tone (`#E0A537`) reserved for alerts, sun/weather icons, and highlights — colors drawn from the farm itself rather than a generic tech palette.
- **Type:** Baloo 2 (rounded, friendly) for headings, Inter for body text, with Noto Sans Devanagari as a fallback so Hindi renders cleanly in both.
- **Layout:** mobile-first, single column, bottom tab navigation with icon + label on every item (never icon-only), large tap targets (52px+ buttons), high-contrast focus rings, minimal steps per screen — per the PRD's accessibility and non-functional requirements (Sections 13–14).
- **Bilingual:** English / Hindi toggle in the top bar and Profile screen. All UI copy lives in `src/data/i18n.js` — add more languages by adding another key to the `dict` object.

## Pages (per PRD Section 16)

| Route | Page | Covers |
|---|---|---|
| `/` | Dashboard | Greeting, quick actions, alerts, today's action plan (F5) |
| `/ask` | Ask AI | Multilingual Q&A assistant (F1) |
| `/disease` | Disease Detection | Leaf image upload → prediction + confidence + next steps (F2) |
| `/weather` | Weather | Current conditions, 5-day forecast, AI recommendation (F3) |
| `/schemes` | Government Schemes | Searchable, expandable eligibility/documents/steps cards, grounded with a source (F4) |
| `/profile` | Profile & Settings | Language, location, crops |

## Mock data — replace with real APIs

Every screen currently runs on mock data so the UI is fully demo-able before the backend/AI/RAG pieces are ready:

- `src/data/mock.js` — weather, schemes, disease classes, chat replies, alerts, action plan
- `src/pages/AskAI.jsx` — `send()` has a `setTimeout` standing in for the RAG/LLM call
- `src/pages/DiseaseDetection.jsx` — `onFile()` has a `setTimeout` standing in for the crop-disease model inference call

Search for `Mocked` in the codebase to find every spot that needs a real `fetch()` to the FastAPI backend once it's ready. Each is intentionally isolated so swapping in a real call doesn't require touching the surrounding UI.

## Getting started

```bash
npm install
npm run dev       # local dev server
npm run build     # production build → dist/
```

## Project structure

```
src/
├── components/
│   ├── layout/       # TopBar, BottomNav, PageContainer
│   └── ui/            # Card, Button, Badge, SectionHeading
├── context/            # AppContext — language state
├── data/               # i18n dictionary + mock data (swap for real API calls)
├── pages/              # one file per screen
├── App.jsx             # routes
└── index.css           # design tokens (colors, fonts) as Tailwind v4 @theme
```

## Notes for the rest of the team

- All colors/fonts are defined once as CSS variables in `src/index.css` under `@theme` — change them there and they propagate everywhere via Tailwind's `bg-leaf-800`, `text-marigold-500`, etc. utility classes.
- Routing uses `HashRouter` so the built `dist/` folder works as static files on any host (Vercel, GitHub Pages, etc.) without server-side rewrite rules. Switch to `BrowserRouter` if the deployment target supports SPA rewrites.
- AI-generated content in the UI (disease prediction, chat answers) always carries a visible disclaimer / confidence indicator per PRD Section 15 ("do not claim diagnostic certainty").
