"""Small SVG helpers shared by the chassis layout and the wiring schematic generators.

Nothing here knows about NEXUS. A drawing script builds a list of lines `o` and writes `'\\n'.join(o)`; each line is one or more
elements made by the functions below. Attribute names take underscores for hyphens (`stroke_width=1.2` -> `stroke-width="1.2"`) and
keep the order they are given in, so a script can reproduce an existing SVG byte for byte.

A `View` maps millimetres to pixels for one plan: `px = origin + scale * mm`, with y optionally flipped (the harness board is drawn
as seen from below). Coordinates and sizes that are geometry go through a view; sizes that are drawing symbols (radii of markers,
font sizes, stroke widths) are pixels and stay literal.
"""

SCALE = 1.7                                    # px per mm in every plan


def sv(v):
    """An attribute value: ints and strings as they are, floats as Python prints them."""
    return v if isinstance(v, str) else str(v)


def attrs(kw):
    return ''.join(f' {k.replace("_", "-")}="{sv(v)}"' for k, v in kw.items())


def px1(v):
    """A pixel coordinate: one decimal, always (`334.0`)."""
    return f'{v:.1f}'


class View:
    """One plan. `top` is the pixel row of the plate's front-right edge (y = 0), `left` the pixel column of x = 0."""

    def __init__(self, name, top=0.0, left=0.0, flip=False, scale=1.0):
        self.name, self.top, self.left, self.flip, self.scale = name, top, left, flip, scale

    def X(self, x):
        return px1(self.left + self.scale * x)

    def Y(self, y):
        return px1(self.top - self.scale * y if self.flip else self.top + self.scale * y)

    def W(self, w):
        return px1(self.scale * w)


PX = View('px')                                # pixels as they are
PLAN_X0 = 60.0                                 # pixel column of the front edge of every plan


def plan(name, top, flip=False):
    return View(name, top=top, left=PLAN_X0, flip=flip, scale=SCALE)


def _c(v):
    """A pixel value given in a PX view: numbers print as written, so pass strings for `600.0`-style values."""
    return sv(v)


def _x(view, v):
    return _c(v) if view is PX else view.X(v)


def _y(view, v):
    return _c(v) if view is PX else view.Y(v)


def _w(view, v):
    return _c(v) if view is PX else view.W(v)


def rect(view, x, y, w, h, **kw):
    """`y` is the edge nearest the top of the page; in a flipped view give the page-top edge in mm."""
    return f'<rect x="{_x(view, x)}" y="{_y(view, y)}" width="{_w(view, w)}" height="{_w(view, h)}"{attrs(kw)}/>'


def circle(view, cx, cy, r, **kw):
    return f'<circle cx="{_x(view, cx)}" cy="{_y(view, cy)}" r="{sv(r)}"{attrs(kw)}/>'


def line(view, x1, y1, x2, y2, **kw):
    return f'<line x1="{_x(view, x1)}" y1="{_y(view, y1)}" x2="{_x(view, x2)}" y2="{_y(view, y2)}"{attrs(kw)}/>'


def text(view, x, y, content, **kw):
    return f'<text x="{_x(view, x)}" y="{_y(view, y)}"{attrs(kw)}>{content}</text>'


def path(d, **kw):
    return f'<path d="{d}"{attrs(kw)}/>'


def outline(view, pts, **kw):
    """A closed polygon from (x, y) points in millimetres."""
    d = ' '.join(('M' if i == 0 else 'L') + f'{view.X(x)} {view.Y(y)}' for i, (x, y) in enumerate(pts)) + ' Z'
    return path(d, **kw)


def el(tag, content=None, **kw):
    """Any other element: `el('tspan', 'x', font_weight=700)`; no content makes a self-closing tag."""
    if content is None:
        return f'<{tag}{attrs(kw)}/>'
    return f'<{tag}{attrs(kw)}>{content}</{tag}>'


def gopen(**kw):
    return f'<g{attrs(kw)}>'


GCLOSE = '</g>'


def comment(s):
    return f'<!-- {s} -->'


def write(path_, lines):
    with open(path_, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
