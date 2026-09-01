# Image sources

The four PNGs in `../images/` are generated, not drawn by hand in an editor —
`sketch.py` fakes the hand-drawn look with seeded jitter on every path, so the
output is identical on every run.

Requirements: `rsvg-convert` (Ubuntu: `librsvg2-bin`) and the Humor Sans font
(`fonts-humor-sans`), with `fonts-comic-neue` as the fallback face.

```bash
python3 gen_cover.py && rsvg-convert -w 1920 -h 1080 -o ../images/cover.png cover.svg
python3 gen_img1.py  && rsvg-convert -w 1200 -h 628  -o ../images/01-history-keys.png img1.svg
python3 gen_img2.py  && rsvg-convert -w 1200 -h 628  -o ../images/02-ctrl-z-faults.png img2.svg
python3 gen_img3.py  && rsvg-convert -w 1200 -h 628  -o ../images/03-filter-languages.png img3.svg
```

Sizes follow LinkedIn's specs: 1920x1080 for the article cover, 1200x628 for
inline images, PNG, all well under the 2 MB limit.
