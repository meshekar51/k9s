"""Hand-drawn SVG primitives: seeded jitter so output is deterministic."""
import random

PAPER = "#fbf7ef"
INK   = "#22303c"
ACC   = "#d1495b"   # red accent
ACC2  = "#2a9d8f"   # teal accent
HILI  = "#f6c667"   # highlighter
FONT  = "Humor Sans"

def rng(seed):
    return random.Random(seed)

def wob(r, amt=2.0):
    return r.uniform(-amt, amt)

def line(r, x1, y1, x2, y2, stroke=INK, w=3, amt=2.0, passes=2):
    """A hand-drawn line: a couple of slightly-off strokes."""
    out = []
    for p in range(passes):
        mx, my = (x1+x2)/2 + wob(r, amt*2), (y1+y2)/2 + wob(r, amt*2)
        d = (f"M{x1+wob(r,amt):.1f},{y1+wob(r,amt):.1f} "
             f"Q{mx:.1f},{my:.1f} {x2+wob(r,amt):.1f},{y2+wob(r,amt):.1f}")
        op = 0.95 if p == 0 else 0.45
        out.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" '
                   f'stroke-linecap="round" opacity="{op}"/>')
    return "".join(out)

def rect(r, x, y, w, h, stroke=INK, sw=3, amt=2.2, fill="none", passes=2):
    """A hand-drawn rectangle."""
    out = []
    if fill != "none":
        out.append(f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y+h} L{x},{y+h} Z" '
                   f'fill="{fill}" stroke="none"/>')
    pts = [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]
    for p in range(passes):
        segs = []
        for i in range(4):
            x1,y1 = pts[i]; x2,y2 = pts[i+1]
            mx,my = (x1+x2)/2 + wob(r,amt*1.6), (y1+y2)/2 + wob(r,amt*1.6)
            if i == 0:
                segs.append(f"M{x1+wob(r,amt):.1f},{y1+wob(r,amt):.1f}")
            segs.append(f"Q{mx:.1f},{my:.1f} {x2+wob(r,amt):.1f},{y2+wob(r,amt):.1f}")
        op = 0.95 if p == 0 else 0.4
        out.append(f'<path d="{" ".join(segs)}" fill="none" stroke="{stroke}" '
                   f'stroke-width="{sw}" stroke-linecap="round" opacity="{op}"/>')
    return "".join(out)

def key(r, x, y, w, h, label, size=30, stroke=INK, fill="#ffffff"):
    """A sketched keycap."""
    s  = rect(r, x, y, w, h, stroke=stroke, sw=3, fill=fill)
    s += rect(r, x+3, y+3, w-6, h-6, stroke=stroke, sw=1.2, passes=1)
    s += text(x+w/2, y+h/2 + size*0.34, label, size=size, anchor="middle", fill=stroke)
    return s

def text(x, y, s, size=26, fill=INK, anchor="start", weight="normal", op=1.0, rot=0):
    s = (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}, Comic Neue, sans-serif" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" opacity="{op}"{tr}>{s}</text>')

def arrow(r, x1, y1, x2, y2, stroke=INK, w=3, amt=1.8):
    """Hand-drawn arrow with a sketched head."""
    import math
    s = line(r, x1, y1, x2, y2, stroke=stroke, w=w, amt=amt)
    ang = math.atan2(y2-y1, x2-x1)
    for a in (ang + 2.6, ang - 2.6):
        hx, hy = x2 + 20*math.cos(a), y2 + 20*math.sin(a)
        s += line(r, x2, y2, hx, hy, stroke=stroke, w=w, amt=1.2, passes=1)
    return s

def highlight(r, x, y, w, h, colour=HILI):
    """A marker-pen swipe behind text."""
    return (f'<path d="M{x},{y+h*0.55} Q{x+w*0.5},{y+h*0.2+wob(r,4):.1f} {x+w},{y+h*0.5}" '
            f'stroke="{colour}" stroke-width="{h}" fill="none" stroke-linecap="round" '
            f'opacity="0.5"/>')

def paper(w, h):
    return (f'<rect width="{w}" height="{h}" fill="{PAPER}"/>'
            f'<rect width="{w}" height="{h}" fill="none" stroke="#e6ddcc" stroke-width="1"/>')

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{paper(w,h)}{body}</svg>')
