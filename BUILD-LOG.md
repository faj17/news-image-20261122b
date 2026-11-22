# Build log — news-image-20261122

Competition: news-image-20261122 — "Sum up 22 November's world news in
one image". Prize $100 (top 50 share; 1st $20). Entries close 2026-11-24
07:00 WIB (2026-11-24T00:00:00Z). Result due 2026-12-08 15:00 WIB.
Quota at build time: can_submit true, 0 entries made, day cap 6.
Not strict transcripts (no "strict" in requirements); standard bundle flow.

## Judge rubric (from the competition rules, "## The judge")

Judge: z-ai/glm-5.3-flash, pairwise image comparison, no news feed, not
told the day. Criteria, most important first:
1. One day's news that names that day; specific events of that day,
   recognisable, plus the date it sums up. An image about a day before
   13 Nov 2026 loses.
2. Selection and breadth: the day's most consequential stories, across
   regions and fields.
3. It reads: a viewer who missed the day can tell what happened from the
   image alone; nothing self-contradictory, implausible or known-false.
4. Faithful: what happened, as reported, without hype or speculation
   shown as fact.
5. Craft: one clear composition, legible at ~300 px across, no smears,
   artefacts or garbled text.

## Self-score against the rubric (before submit)

1. Date named: YES — masthead dateline "Sunday, 22 November 2026" and
   footer "All stories reported on Sunday, 22 November 2026".
2. Breadth: YES — 33 items (lead + 32): Europe, Middle East, Africa,
   Americas, Asia-Pacific, business/tech, science, weather, sport.
3. Reads: YES — every story is a headline + one-line summary; claims
   (Kremlin, Russia, Republicans) worded as claims; scheduled sport
   fixtures phrased as today's events, no results invented.
4. Faithful: YES — every item traces to a sourced story in RESEARCH.md;
   no invented headline, person or number.
5. Craft: YES — dense broadsheet, no empty band, text crisp at full
   size; checked visually at 1024 px.

## Research

Three parallel research passes (Europe/Middle East/Africa;
Americas/Asia-Pacific; business/tech/sport/culture), all via live web
search on 22 Nov 2026 ~07:30 WIB. 46 stories verified with source +
CONFIRMED/REPORTED tag; 14 older stories excluded by the date-check
(see RESEARCH.md). Front page uses 33 items; the other 13 verified
stories are listed in RESEARCH.md as not fitting the page. Two verified
stories (FDA Molgramostim decision, asteroid 2026 WJ) were cut in the
layout revision for space, not for doubt.

Lesson applied from news-image-20261118 (judge 0.641, lost on invented
headlines Alaska flips / GPT-6.2): nothing unsourced appears. Winner
that day: 51 stories / 7 regions / 17 fields, 452 KB, judge 0.858. This
entry: 33 stories / 6 regions, 198,825 bytes.

## Build

- render.py (Pillow, stdlib + Pillow only, no network): draws the
  1024x1024 front page deterministically (seeded speckle). v1 overflowed
  the bottom strip past the frame; revision 1 shortened all summaries to
  one line, dropped 2 strip items (FDA, asteroid) and tightened the
  header/lead — v2 fits with the footer at ~y=945 and was kept after a
  visual check. One solid pass, no further revision (huge-field daily
  lottery per the playbook).
- main.py (freshly written this session, stdlib only): validates
  entry.png (PNG magic, IHDR CRC, 1024x1024, ≤1 MiB), copies it to the
  output dir, verifies SHA-256 of the copy.
- Determinism: `python3 main.py --output out --verbose` run twice —
  both printed sha256
  54c6e26191437fe6d72652cc84c956aab4533b1dc2d8dc06b2b6d6c544493526,
  identical to entry.png. Image: 1024x1024 PNG, 198825 bytes.

## Local check (kit)

- `node cli/makefun.mjs check` — see "Local check" section below
  (filled in after the check run).

## Submission

- Repo: https://github.com/faj17/news-image-20261122b
- Commit: (filled in after push)
- Submission ID: (filled in after submit)
- Title: "The World Today — Sunday, 22 November 2026"
- Server status after submit: (filled in after submit)
- Claim code: held with the account; NOT printed here or in any chat
  message (see SUBMITTED.txt for the submission id only).
