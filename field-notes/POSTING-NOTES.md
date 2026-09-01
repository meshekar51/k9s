# Posting notes

## What is here

| File | What it is |
|---|---|
| `linkedin-article.md` | **The article.** 556 words, four images. For LinkedIn's long-form editor. |
| `images/` | Cover (1920x1080) + three inline PNGs (1200x628). |
| `README.md` | The long reference version, with a file:line citation on every claim. |
| `linkedin-post.txt` | A short feed-post variant, 2,278 chars, if you want a post instead. |
| `k9s-carousel.pdf` | **The carousel.** 10 square slides, upload as a document post. |
| `tools/` | The scripts that generate the images and the carousel. Re-runnable. |

## Three formats, three different posts

- **Article** (`linkedin-article.md`) — the long-form editor. Real formatting,
  inline images, no character ceiling. The main deliverable.
- **Carousel** (`k9s-carousel.pdf`) — a document post. LinkedIn renders the PDF
  as swipeable slides. Best reach of the three for reference material.
- **Post** (`linkedin-post.txt`) — the plain feed post. 3,000-char cap, no
  markdown, no inline images. A fallback.

These are three separate posts, not one thing in three formats. Space them out —
a week or two apart — and have the later one point back at the earlier.

## Publishing the carousel

1. Start a normal post, then choose **Add document** (not Add photo).
2. Upload `k9s-carousel.pdf`. LinkedIn asks for a document title — that title
   shows above the deck, so use something like
   `k9s: the keys the cheat sheets get wrong`.
3. Write 2-3 lines of post copy above it. The opening line of
   `linkedin-post.txt` works as-is.
4. Slide 10 asks the closing question and carries the repo link.

The deck is 10 pages at 810x810 pt, which is 1080x1080 px — LinkedIn's square
document format. 120 KB total, well inside any limit.

## Publishing the article

1. LinkedIn → Write article.
2. **Headline:** `k9s: the keys the cheat sheets get wrong` — 40 characters,
   inside the 100-character limit.
3. **Cover:** upload `images/cover.png` (1920x1080).
4. Paste the body from `linkedin-article.md`, dropping the `#` heading line.
   LinkedIn's editor has its own H1/H2 buttons — apply them to the three
   section headings rather than leaving the `##` characters in.
5. Insert the three inline images at the marked points. They are already
   1200x628 and PNG, which is what LinkedIn wants for graphics with text.
6. The GitHub link near the end can stay inline — link penalties apply to feed
   posts, not to articles.

## Before you publish

- The article claims no war stories, because none were verified. **If you have a
  real incident where one of these keys mattered, add a line about it.** That is
  the strongest thing you can put in, and it has to be yours.
- The closing question is genuine. Swap it if it does not sound like you.
- Everything is version-qualified to v0.51.0 on purpose. If you publish months
  from now, re-check section 3 and the popeye claim first — the whole point of
  the piece is that this content ages.

## If it does well

The three inline images are already a carousel in everything but format: one
idea each, large type, square-ish. Re-render them at 1080x1080 from `tools/`
and add a title and CTA slide.
