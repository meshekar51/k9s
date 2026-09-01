from sketch import *
W, H = 1200, 628
r = rng(43); b = []
b.append(text(60, 78, "The  /  filter is four languages, not one", size=46, fill=INK))
b.append(line(r, 58, 100, 1140, 100, w=3, amt=2.5))
b.append(text(60, 140, "what you type after the slash is parsed four different ways", size=27, fill="#5a6b78"))
b.append(text(1140, 178, "internal/helpers.go:14-15", size=21, fill="#8a99a5", anchor="end"))

rows = [("/nginx",      "plain regular expression",        INK),
        ("/!nginx",     "INVERSE  —  all that do NOT match", ACC),
        ("/-l app=web", "label selector",                  ACC2),
        ("/-f nginx",   "fuzzy match",                     ACC2)]
for i, (q, meaning, col) in enumerate(rows):
    y = 240 + i*76
    b.append(rect(r, 80, y-42, 300, 58, sw=2.5, fill="#ffffff", passes=1))
    b.append(text(100, y, q, size=32, fill=col))
    b.append(arrow(r, 396, y-14, 448, y-14, w=2.5, amt=1.2))
    b.append(text(468, y, meaning, size=30, fill=INK))

b.append(highlight(r, 76, 528, 940, 42))
b.append(text(80, 560, "Both prefixes are anchored to the START of the string.", size=30))
b.append(text(80, 600, "So  /pods -l app=web  is a regex, not a label filter.", size=27, fill="#5a6b78"))
open("img3.svg","w").write(svg(W, H, "".join(b)))
