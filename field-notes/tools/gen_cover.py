from sketch import *

W, H = 1920, 1080
r = rng(11)
b = []

# --- title ---
b.append(highlight(r, 145, 108, 245, 86))
b.append(text(150, 190, "k9s", size=132, fill=INK, weight="bold"))
b.append(text(150, 300, "the keys the cheat sheets", size=76, fill=INK))
b.append(text(150, 384, "get wrong", size=76, fill=INK))
b.append(line(r, 150, 424, 1120, 424, w=4, amt=3))
b.append(text(152, 480, "verified against v0.51.0  ~  read from the source, run on a live cluster",
              size=36, fill="#5a6b78"))

# --- sketched terminal window ---
tx, ty, tw, th = 150, 540, 1050, 430
b.append(rect(r, tx, ty, tw, th, sw=4, fill="#ffffff"))
b.append(line(r, tx, ty+54, tx+tw, ty+54, w=3, amt=2))
for i, c in enumerate((ACC, HILI, ACC2)):
    b.append(f'<circle cx="{tx+38+i*38}" cy="{ty+27}" r="10" fill="{c}" opacity="0.85"/>')
b.append(text(tx+150, ty+38, "k9s  —  pods", size=26, fill="#5a6b78"))

rows = [
    ("NAMESPACE", "NAME", "STATUS", None),
    ("demo", "api-7c9d4f-2xk", "Running", ACC2),
    ("demo", "worker-55b8-qq7", "CrashLoopBackOff", ACC),
    ("demo", "cache-0", "Running", ACC2),
    ("kube-system", "coredns-559f-sltqx", "Running", ACC2),
]
for i, (ns, nm, st, col) in enumerate(rows):
    yy = ty + 108 + i*62
    fill = "#5a6b78" if col is None else INK
    sz = 24 if col is None else 28
    b.append(text(tx+42, yy, ns, size=sz, fill=fill))
    b.append(text(tx+280, yy, nm, size=sz, fill=fill))
    b.append(text(tx+660, yy, st, size=sz, fill=col or fill))
    if st == "CrashLoopBackOff":
        b.append(rect(r, tx+642, yy-32, 322, 44, stroke=ACC, sw=2.5, passes=1))

# --- the three keys ---
kx = 1330
b.append(text(kx, 600, "the ones nobody", size=36, fill="#5a6b78"))
b.append(text(kx, 646, "tells you about:", size=36, fill="#5a6b78"))
for i, (lab, sub) in enumerate((("[", "go back"), ("]", "go forward"), ("-", "last view"))):
    yy = 700 + i*98
    b.append(key(r, kx, yy, 84, 84, lab, size=46))
    b.append(text(kx+108, yy+56, sub, size=34, fill=INK))

open("cover.svg","w").write(svg(W, H, "".join(b)))
