from sketch import *
W, H = 1200, 628
r = rng(31); b = []
b.append(text(60, 78, "Ctrl-Z  —  show only what is broken", size=48, fill=INK))
b.append(line(r, 58, 100, 1140, 100, w=3, amt=2.5))
b.append(text(60, 140, "and the reason it sometimes shows you nothing at all", size=27, fill="#5a6b78"))

def mini(x, y, rows, w=450):
    o = [rect(r, x, y, w, 46+len(rows)*44, sw=3, fill="#ffffff")]
    for i, (nm, st, col) in enumerate(rows):
        yy = y + 46 + i*44
        o.append(text(x+22, yy, nm, size=25))
        o.append(text(x+238, yy, st, size=24, fill=col))
    return "".join(o)

left = [("api-7c9d4f", "Running", ACC2), ("worker-55b8", "CrashLoop", ACC),
        ("cache-0", "Running", ACC2), ("web-2f9a", "ImagePullErr", ACC)]
b.append(text(90, 200, "before", size=27, fill="#5a6b78"))
b.append(mini(90, 214, left))
b.append(text(690, 200, "after", size=27, fill="#5a6b78"))
b.append(mini(690, 214, [("worker-55b8", "CrashLoop", ACC), ("web-2f9a", "ImagePullErr", ACC)]))
b.append(arrow(r, 560, 300, 668, 300, stroke=ACC, w=4))
b.append(text(614, 278, "ctrl-z", size=30, fill=ACC, anchor="middle"))

b.append(text(90, 470, "It keeps every row whose hidden VALID column is not empty.", size=29))
b.append(highlight(r, 86, 496, 900, 42))
b.append(text(90, 528, "No VALID column? It returns an EMPTY set  —  table goes blank.", size=29))
b.append(text(90, 570, "Not a hang. Not a dropped connection. Press it again.", size=27, fill="#5a6b78"))
b.append(text(1140, 604, "internal/model1/table_data.go:221-235", size=21, fill="#8a99a5", anchor="end"))
open("img2.svg","w").write(svg(W, H, "".join(b)))
