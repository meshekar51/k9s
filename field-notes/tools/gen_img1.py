from sketch import *
W, H = 1200, 628
r = rng(23); b = []
b.append(text(60, 78, "k9s has browser history", size=48, fill=INK))
b.append(line(r, 58, 100, 1140, 100, w=3, amt=2.5))
b.append(text(60, 140, "three global keys, and almost nobody uses them", size=27, fill="#5a6b78"))

views = ["deployments", "pods", "logs"]
bx, by, bw, bh = 90, 210, 280, 92
for i, v in enumerate(views):
    x = bx + i*365
    b.append(rect(r, x, by, bw, bh, sw=3, fill="#ffffff"))
    b.append(text(x+bw/2, by+56, v, size=34, anchor="middle"))
    if i < 2:
        b.append(arrow(r, x+bw+14, by+bh/2, x+bw+66, by+bh/2, w=3))
        b.append(text(x+bw+40, by+bh/2-20, "enter", size=22, fill="#5a6b78", anchor="middle"))

# curved "go back" sweep under the row
b.append(f'<path d="M{bx+bw+300},{by+bh+20} C{bx+620},{by+bh+130} {bx+280},{by+bh+130} {bx+62},{by+bh+24}" '
         f'fill="none" stroke="{ACC}" stroke-width="3.5" stroke-linecap="round" opacity="0.9"/>')
b.append(arrow(r, bx+120, by+bh+62, bx+64, by+bh+26, stroke=ACC, w=3, amt=1))
b.append(key(r, 508, 452, 66, 66, "-", size=38, stroke=ACC))
b.append(text(596, 496, "like  cd -  in a shell", size=30, fill=ACC))

# compact legend, one row, aligned
for i, (k, lab) in enumerate((("[", "go back"), ("]", "go forward"), ("-", "last view"))):
    x = 90 + i*372
    b.append(key(r, x, 546, 46, 46, k, size=27))
    b.append(text(x+62, 580, lab, size=28, fill=INK))
b.append(text(1140, 176, "internal/view/app.go:259-261", size=21, fill="#8a99a5", anchor="end"))
open("img1.svg","w").write(svg(W, H, "".join(b)))
