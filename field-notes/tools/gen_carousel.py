"""10-slide square carousel, 1080x1080, for LinkedIn document upload."""
from sketch import *

S = 1080
OUT = []

def slide(n, build, seed):
    r = rng(seed)
    b = []
    build(r, b)
    # footer: slide number + handle
    b.append(line(r, 70, S-96, S-70, S-96, w=2, amt=1.5))
    b.append(text(70, S-56, "k9s field notes  ~  v0.51.0", size=24, fill="#8a99a5"))
    b.append(text(S-70, S-56, f"{n} / 10", size=24, fill="#8a99a5", anchor="end"))
    OUT.append((n, svg(S, S, "".join(b))))

def title(b, r, t, size=68, y=200):
    for i, ln in enumerate(t.split("\n")):
        b.append(text(70, y + i*int(size*1.15), ln, size=size, fill=INK))
    return y + len(t.split("\n"))*int(size*1.15)

# ---- 1 hook ----
def s1(r, b):
    b.append(highlight(r, 66, 268, 214, 78))
    b.append(text(70, 344, "k9s", size=122, weight="bold"))
    title(b, r, "the keys\nthe cheat sheets\nget wrong", size=74, y=470)
    b.append(line(r, 70, 742, 700, 742, w=4, amt=3))
    b.append(text(70, 800, "verified against v0.51.0", size=36, fill="#5a6b78"))
    b.append(text(70, 848, "read from the source, run on a live cluster", size=32, fill="#5a6b78"))
    b.append(text(70, 940, "swipe  ->", size=34, fill=ACC))
slide(1, s1, 3)

# ---- 2 popeye ----
def s2(r, b):
    title(b, r, "Every cheat sheet\ntells you to press", size=52, y=180)
    b.append(rect(r, 70, 330, 460, 96, sw=3, fill="#ffffff"))
    b.append(text(100, 394, ":popeye", size=56, fill=ACC))
    b.append(text(70, 510, "Occurrences of \"popeye\" in", size=40))
    b.append(text(70, 564, "the v0.51.0 source tree:", size=40))
    b.append(text(540, 800, "0", size=180, fill=ACC, anchor="middle", weight="bold"))
    b.append(f'<circle cx="540" cy="742" r="108" fill="none" stroke="{ACC}" '
             f'stroke-width="4" opacity="0.85"/>')
    b.append(text(70, 916, "The integration is gone. The CLI still exists.", size=30, fill="#5a6b78"))
slide(2, s2, 5)

# ---- 3 history keys ----
def s3(r, b):
    title(b, r, "k9s has\nbrowser history", size=66, y=190)
    for i, (k, lab) in enumerate((("[", "go back"), ("]", "go forward"), ("-", "last view"))):
        y = 420 + i*150
        b.append(key(r, 80, y, 110, 110, k, size=58))
        b.append(text(230, y+72, lab, size=52, fill=INK))
    b.append(text(70, 908, "Three global keys. Nobody uses them.", size=30, fill="#5a6b78"))
slide(3, s3, 7)

# ---- 4 the dash ----
def s4(r, b):
    title(b, r, "Jump straight back", size=64, y=180)
    views = ["deployments", "pods", "logs"]
    for i, v in enumerate(views):
        y = 300 + i*112
        b.append(rect(r, 90, y, 420, 88, sw=3, fill="#ffffff"))
        b.append(text(300, y+56, v, size=38, anchor="middle"))
        if i < 2:
            b.append(arrow(r, 300, y+96, 300, y+106, w=3, amt=1))
    b.append(f'<path d="M560,700 C820,660 820,380 560,344" fill="none" '
             f'stroke="{ACC}" stroke-width="4" stroke-linecap="round"/>')
    b.append(arrow(r, 600, 352, 556, 344, stroke=ACC, w=3, amt=1))
    b.append(key(r, 840, 480, 90, 90, "-", size=50, stroke=ACC))
    b.append(text(70, 800, "One key. Back to where you were,", size=38))
    b.append(text(70, 852, "without retyping  :deploy  —  like  cd -", size=38))
slide(4, s4, 11)

# ---- 5 ctrl-z ----
def s5(r, b):
    title(b, r, "Ctrl-Z\nshows only\nwhat is broken", size=66, y=190)
    rows = [("api-7c9d4f", "Running", "#b9c4cc"), ("worker-55b8", "CrashLoop", ACC),
            ("cache-0", "Running", "#b9c4cc"), ("web-2f9a", "ImagePullErr", ACC)]
    b.append(rect(r, 70, 560, 940, 268, sw=3, fill="#ffffff"))
    for i, (nm, st, col) in enumerate(rows):
        y = 620 + i*62
        b.append(text(110, y, nm, size=34, fill=col))
        b.append(text(560, y, st, size=34, fill=col))
        if col == ACC:
            b.append(rect(r, 545, y-38, 340, 52, stroke=ACC, sw=2, passes=1))
    b.append(text(70, 890, "It keeps rows where a hidden VALID column is set.", size=30, fill="#5a6b78"))
slide(5, s5, 13)

# ---- 6 ctrl-z gotcha ----
def s6(r, b):
    b.append(text(70, 170, "The catch", size=48, fill=ACC))
    title(b, r, "No VALID column\non the view?", size=62, y=270)
    b.append(rect(r, 70, 430, 940, 240, sw=3, fill="#ffffff"))
    b.append(text(540, 570, "( nothing )", size=52, fill="#b9c4cc", anchor="middle"))
    b.append(highlight(r, 66, 716, 800, 46))
    b.append(text(70, 754, "Ctrl-Z returns an EMPTY set.", size=44))
    b.append(text(70, 830, "The table goes blank. That is not a hang", size=34, fill="#5a6b78"))
    b.append(text(70, 876, "and not a dropped connection. Press it again.", size=34, fill="#5a6b78"))
slide(6, s6, 17)

# ---- 7 filters ----
def s7(r, b):
    title(b, r, "The  /  filter is\nfour languages", size=64, y=190)
    rows = [("/nginx", "regex", INK), ("/!nginx", "everything EXCEPT", ACC),
            ("/-l app=web", "label selector", ACC2), ("/-f nginx", "fuzzy", ACC2)]
    for i, (q, m, col) in enumerate(rows):
        y = 420 + i*128
        b.append(rect(r, 70, y, 400, 84, sw=2.5, fill="#ffffff", passes=1))
        b.append(text(96, y+56, q, size=38, fill=col))
        b.append(text(510, y+56, m, size=36, fill=INK))
slide(7, s7, 19)

# ---- 8 anchor trap ----
def s8(r, b):
    b.append(text(70, 170, "The trap", size=48, fill=ACC))
    title(b, r, "Prefixes only work\nat the START", size=62, y=270)
    b.append(rect(r, 70, 430, 940, 110, sw=3, fill="#ffffff"))
    b.append(text(100, 500, "/pods -l app=web", size=48, fill=ACC))
    b.append(text(880, 500, "X", size=54, fill=ACC, anchor="middle"))
    b.append(text(70, 610, "is NOT a label filter.", size=44))
    b.append(text(70, 672, "It is a regex, and it will quietly", size=38, fill="#5a6b78"))
    b.append(text(70, 720, "find nothing at all.", size=38, fill="#5a6b78"))
    b.append(rect(r, 70, 780, 940, 110, sw=3, fill="#ffffff"))
    b.append(text(100, 850, "/-l app=web", size=48, fill=ACC2))
    b.append(text(880, 850, "OK", size=44, fill=ACC2, anchor="middle"))
slide(8, s8, 23)

# ---- 9 method ----
def s9(r, b):
    title(b, r, "How this was\nverified", size=64, y=190)
    lines = [
        "Source read at the v0.51.0 tag",
        "Re-checked against current master",
        "Binary run on a live kind cluster",
        "Every claim cites a file and line",
    ]
    for i, ln in enumerate(lines):
        y = 420 + i*92
        b.append(text(76, y, "-", size=44, fill=ACC2))
        b.append(text(130, y, ln, size=38, fill=INK))
    b.append(highlight(r, 66, 812, 880, 44))
    b.append(text(70, 848, "What I could not verify, I left out.", size=36))
    b.append(text(70, 906, "I do not know which release dropped popeye. So I did not guess.",
                  size=27, fill="#5a6b78"))
slide(9, s9, 29)

# ---- 10 CTA ----
def s10(r, b):
    title(b, r, "Long version,\nwith citations", size=64, y=230)
    b.append(rect(r, 70, 420, 940, 120, sw=3, fill="#ffffff"))
    b.append(text(100, 494, "github.com/meshekar51/k9s", size=40, fill=ACC2))
    b.append(text(70, 620, "field-notes/", size=36, fill="#5a6b78"))
    b.append(line(r, 70, 700, 1010, 700, w=3, amt=2))
    b.append(text(70, 776, "Which k9s key do you wish", size=44))
    b.append(text(70, 832, "you had learned a year earlier?", size=44))
    b.append(text(70, 906, "Tell me in the comments.", size=32, fill=ACC))
slide(10, s10, 31)

for n, s in OUT:
    open(f"slide{n:02d}.svg", "w").write(s)
print(f"{len(OUT)} slides")
