"""TechLog 이미지 공통 도구 (Pillow).

README 6절 팔레트/레이아웃을 그대로 따르는 썸네일·다이어그램용 헬퍼.
macOS(AppleSDGothicNeo), Ubuntu(Noto Sans CJK), Windows(Malgun Gothic) 폰트를 자동 탐색한다.
"""
import os
from PIL import Image, ImageDraw, ImageFont

C = {
    'bg': '#D6E8FB', 'navy': '#1E3A5F', 'blue': '#5B8FD4', 'lblue': '#A8C9EF',
    'pale': '#C6DEF8', 'green': '#279866', 'red': '#CE4747', 'gray': '#788A9E',
    'paper': '#F9FBFE', 'white': '#FFFFFF',
}

_FONT_CANDIDATES = {
    True: [
        ('/System/Library/Fonts/AppleSDGothicNeo.ttc', 6),   # Bold
        ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 1),
        ('/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc', 1),
        ('C:/Windows/Fonts/malgunbd.ttf', 0),
    ],
    False: [
        ('/System/Library/Fonts/AppleSDGothicNeo.ttc', 0),   # Regular
        ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 1),
        ('/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc', 1),
        ('C:/Windows/Fonts/malgun.ttf', 0),
    ],
}


def font(size, bold=False):
    for path, idx in _FONT_CANDIDATES[bold]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size, index=idx)
    raise RuntimeError('한글 폰트를 찾을 수 없습니다 (fonts-noto-cjk 설치 필요)')


def canvas(w, h, bg):
    img = Image.new('RGB', (w, h), C.get(bg, bg))
    return img, ImageDraw.Draw(img)


def rrect(d, box, r, fill=None, outline=None, width=0):
    d.rounded_rectangle(box, r, fill=C.get(fill, fill), outline=C.get(outline, outline), width=width)


def text_c(d, cx, cy, s, size, color='navy', bold=False, spacing=0):
    """(cx, cy) 중심에 텍스트 배치. spacing>0 이면 자간을 벌린다."""
    f = font(size, bold)
    col = C.get(color, color)
    if spacing:
        widths = [d.textlength(ch, font=f) for ch in s]
        total = sum(widths) + spacing * (len(s) - 1)
        x = cx - total / 2
        for ch, w in zip(s, widths):
            d.text((x, cy), ch, font=f, fill=col, anchor='lm')
            x += w + spacing
    else:
        d.text((cx, cy), s, font=f, fill=col, anchor='mm')


def arrow(d, p1, p2, color='navy', width=6, head=16, dashed=False):
    import math
    col = C.get(color, color)
    x1, y1 = p1
    x2, y2 = p2
    ang = math.atan2(y2 - y1, x2 - x1)
    ex, ey = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    if dashed:
        L = math.hypot(ex - x1, ey - y1)
        n = int(L // 22)
        for i in range(n + 1):
            a, b = i * 22, min(i * 22 + 13, L)
            if a >= L:
                break
            d.line([(x1 + a * math.cos(ang), y1 + a * math.sin(ang)),
                    (x1 + b * math.cos(ang), y1 + b * math.sin(ang))], fill=col, width=width)
    else:
        d.line([p1, (ex, ey)], fill=col, width=width)
    left = (x2 - head * math.cos(ang - 0.5), y2 - head * math.sin(ang - 0.5))
    right = (x2 - head * math.cos(ang + 0.5), y2 - head * math.sin(ang + 0.5))
    d.polygon([p2, left, right], fill=col)


def cloud(d, x, y, s=1.0, color='pale'):
    col = C.get(color, color)
    d.ellipse((x, y + 30 * s, x + 90 * s, y + 100 * s), fill=col)
    d.ellipse((x + 50 * s, y, x + 170 * s, y + 100 * s), fill=col)
    d.ellipse((x + 140 * s, y + 35 * s, x + 210 * s, y + 100 * s), fill=col)
    d.rectangle((x + 5 * s, y + 65 * s, x + 200 * s, y + 102 * s), fill=col)


def plus(d, x, y, s=24, color='lblue', width=7):
    col = C.get(color, color)
    d.line([(x - s, y), (x + s, y)], fill=col, width=width)
    d.line([(x, y - s), (x, y + s)], fill=col, width=width)


def fit_size(d, s, max_w, size, bold=False, min_size=14, spacing=0):
    """max_w 안에 들어가도록 폰트 크기를 줄인다."""
    while size > min_size:
        f = font(size, bold)
        w = d.textlength(s, font=f) + spacing * max(len(s) - 1, 0)
        if w <= max_w:
            break
        size -= 2
    return size


def wrap_text(d, cx, cy, s, max_w, size, color='navy', bold=False, min_size=15, max_lines=2, line_gap=1.3):
    """max_w 안에 들어가도록 줄바꿈(최대 max_lines줄) + 축소, 그래도 넘치면 말줄임."""
    def split(sz):
        f = font(sz, bold)
        lines, cur = [], ''
        for word in s.split(' '):
            t = (cur + ' ' + word).strip()
            if d.textlength(t, font=f) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
        return lines, f
    sz = size
    while True:
        lines, f = split(sz)
        if (len(lines) <= max_lines and all(d.textlength(l, font=f) <= max_w for l in lines)) or sz <= min_size:
            break
        sz -= 1
    lines = lines[:max_lines]
    for k, l in enumerate(lines):
        while d.textlength(l, font=f) > max_w and len(l) > 1:
            l = l[:-2] + '…'
        lines[k] = l
    h = sz * line_gap
    y0 = cy - h * (len(lines) - 1) / 2
    for k, l in enumerate(lines):
        d.text((cx, y0 + k * h), l, font=f, fill=C.get(color, color), anchor='mm')


# ─────────────────────────── 썸네일 ───────────────────────────
# 레이아웃(5) × 테마(6) × 아이콘(16) 조합. auto_post.py는 글 개수로 레이아웃·테마를 순환시켜
# 연속한 글끼리 겹치지 않게 하고, 아이콘은 Gemini가 주제에 맞게 고른다.

THEMES = {
    'sky':      dict(bg='#D6E8FB', deco='#C6DEF8', deco2='#A8C9EF', ink='#1E3A5F', sub='#5B7596',
                     panel='#FFFFFF', panel_ink='#1E3A5F', accent='#5B8FD4', pill='#1E3A5F', pill_ink='#FFFFFF',
                     icon_fill='#A8C9EF', icon_line='#1E3A5F', bar='#A8C9EF'),
    'night':    dict(bg='#172E4D', deco='#1F3C62', deco2='#2E5584', ink='#FFFFFF', sub='#A8C9EF',
                     panel='#F9FBFE', panel_ink='#1E3A5F', accent='#7FB2F0', pill='#7FB2F0', pill_ink='#10243D',
                     icon_fill='#7FB2F0', icon_line='#0E1F36', bar='#A8C9EF'),
    'mint':     dict(bg='#DDF3E8', deco='#C9EBDA', deco2='#9FD8BD', ink='#17453A', sub='#4E7A6C',
                     panel='#FFFFFF', panel_ink='#17453A', accent='#279866', pill='#17453A', pill_ink='#FFFFFF',
                     icon_fill='#9FD8BD', icon_line='#17453A', bar='#9FD8BD'),
    'peach':    dict(bg='#FDEBDD', deco='#FADCC6', deco2='#F3BD98', ink='#3B2A20', sub='#8A6A57',
                     panel='#FFFFFF', panel_ink='#3B2A20', accent='#E07A3F', pill='#3B2A20', pill_ink='#FFFFFF',
                     icon_fill='#F6C7A5', icon_line='#3B2A20', bar='#F3BD98'),
    'lavender': dict(bg='#E9E5FB', deco='#DCD5F7', deco2='#BDB2EF', ink='#2A2660', sub='#6D679A',
                     panel='#FFFFFF', panel_ink='#2A2660', accent='#6C5BD4', pill='#2A2660', pill_ink='#FFFFFF',
                     icon_fill='#BDB2EF', icon_line='#2A2660', bar='#BDB2EF'),
    'ocean':    dict(bg='#4F84CC', deco='#5C8FD4', deco2='#78A5E0', ink='#FFFFFF', sub='#DDEAFB',
                     panel='#FFFFFF', panel_ink='#1E3A5F', accent='#FFD166', pill='#1E3A5F', pill_ink='#FFFFFF',
                     icon_fill='#D6E8FB', icon_line='#1E3A5F', bar='#A8C9EF'),
}
LAYOUTS = ['classic', 'split', 'editor', 'poster', 'emblem']
ICONS = ['devices', 'browser', 'phone', 'code', 'server', 'database', 'cloud', 'shield', 'chip', 'network',
         'gear', 'chat', 'bolt', 'chart', 'globe', 'layers']
_ICON_PARTNER = {'devices': 'browser', 'browser': 'code', 'phone': 'browser', 'code': 'browser',
                 'server': 'database', 'database': 'server', 'cloud': 'server', 'shield': 'browser',
                 'chip': 'chat', 'network': 'server', 'gear': 'code', 'chat': 'chip', 'bolt': 'chart',
                 'chart': 'bolt', 'globe': 'browser', 'layers': 'code'}
_OK = '#2FA56F'
_TRAFFIC = ['#FF6B6B', '#FFC857', '#4CC38A']
W, H = 1536, 1024


def pick_style(seed):
    """seed(보통 기존 글 수)로 레이아웃·테마를 고른다. 5와 6이 서로소라 30편 동안 조합이 겹치지 않는다."""
    names = list(THEMES)
    return LAYOUTS[seed % len(LAYOUTS)], names[seed % len(names)]


# ── 아이콘: (cx, cy) 중심, 한 변 약 s 크기 ──

def _lw(s):
    return max(4, int(s * 0.04))


def _blob(d, ellipses, fill, line, lw):
    """타원 합집합 도형을 외곽선과 함께 그린다 (외곽선 색으로 크게 → 채움색으로 원래 크기)."""
    for x0, y0, x1, y1 in ellipses:
        d.ellipse((x0 - lw, y0 - lw, x1 + lw, y1 + lw), fill=line)
    for e in ellipses:
        d.ellipse(e, fill=fill)


def _screen_bars(d, box, s, th, dot=True):
    x0, y0, x1, y1 = box
    bw, h = x1 - x0, y1 - y0
    for i, r in enumerate([0.75, 0.5, 0.65]):
        y = y0 + h * (0.18 + i * 0.2)
        d.rounded_rectangle((x0 + bw * 0.12, y, x0 + bw * (0.12 + 0.76 * r), y + s * 0.045), s * 0.02, fill=th['bar'])
    if dot:
        r = s * 0.035
        cx, cy = x0 + bw * 0.12 + r, y0 + h * 0.82
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=_OK)


def _ic_phone(d, cx, cy, s, th):
    lw, w, h = _lw(s), s * 0.52, s * 0.95
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), s * 0.09, fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    scr = (x0 + s * 0.06, y0 + s * 0.12, x0 + w - s * 0.06, y0 + h - s * 0.12)
    d.rounded_rectangle(scr, s * 0.03, fill='white')
    d.rounded_rectangle((cx - s * 0.07, y0 + s * 0.045, cx + s * 0.07, y0 + s * 0.07), s * 0.02, fill=th['icon_line'])
    r = s * 0.03
    d.ellipse((cx - r, y0 + h - s * 0.075 - r, cx + r, y0 + h - s * 0.075 + r), fill=th['icon_line'])
    _screen_bars(d, scr, s, th)


def _monitor(d, cx, cy, s, th):
    lw, w, h = _lw(s), s, s * 0.66
    x0, y0 = cx - w / 2, cy - s / 2
    d.rectangle((cx - s * 0.05, y0 + h, cx + s * 0.05, y0 + h + s * 0.2), fill=th['icon_line'])
    d.rounded_rectangle((cx - s * 0.22, y0 + h + s * 0.18, cx + s * 0.22, y0 + h + s * 0.25), s * 0.035, fill=th['icon_line'])
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), s * 0.07, fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    scr = (x0 + s * 0.07, y0 + s * 0.07, x0 + w - s * 0.07, y0 + h - s * 0.07)
    d.rounded_rectangle(scr, s * 0.03, fill='white')
    _screen_bars(d, scr, s, th)


def _ic_devices(d, cx, cy, s, th):
    _monitor(d, cx + s * 0.14, cy - s * 0.02, s * 0.78, th)
    _ic_phone(d, cx - s * 0.33, cy + s * 0.14, s * 0.62, th)


def _ic_browser(d, cx, cy, s, th):
    lw, w, h = _lw(s), s, s * 0.78
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), s * 0.07, fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + s * 0.16), s * 0.07, fill=th['icon_line'])
    d.rectangle((x0, y0 + s * 0.09, x0 + w, y0 + s * 0.16), fill=th['icon_line'])
    r = s * 0.028
    for i, c in enumerate(_TRAFFIC):
        x = x0 + s * 0.08 + i * s * 0.08
        d.ellipse((x - r, y0 + s * 0.08 - r, x + r, y0 + s * 0.08 + r), fill=c)
    scr = (x0 + s * 0.06, y0 + s * 0.22, x0 + w - s * 0.06, y0 + h - s * 0.06)
    d.rounded_rectangle(scr, s * 0.03, fill='white')
    sx0, sy0, sx1, sy1 = scr
    d.rounded_rectangle((sx0 + s * 0.05, sy0 + s * 0.05, sx0 + s * 0.36, sy1 - s * 0.05), s * 0.025, fill=th['bar'])
    for i, r2 in enumerate([1, 0.7, 0.85]):
        y = sy0 + s * (0.07 + i * 0.12)
        d.rounded_rectangle((sx0 + s * 0.42, y, sx0 + s * 0.42 + (sx1 - sx0 - s * 0.47) * r2, y + s * 0.045),
                            s * 0.02, fill=th['bar'])


def _ic_code(d, cx, cy, s, th):
    lw, w, h = _lw(s), s, s * 0.78
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), s * 0.08, fill='#16263D', outline=th['icon_line'], width=lw)
    r = s * 0.028
    for i, c in enumerate(_TRAFFIC):
        x = x0 + s * 0.09 + i * s * 0.08
        d.ellipse((x - r, y0 + s * 0.09 - r, x + r, y0 + s * 0.09 + r), fill=c)
    gy, gw, col, lw2 = cy + s * 0.06, s * 0.13, '#FFD166', max(6, int(s * 0.06))
    d.line([(cx - s * 0.2, gy - gw), (cx - s * 0.33, gy), (cx - s * 0.2, gy + gw)], fill=col, width=lw2, joint='curve')
    d.line([(cx + s * 0.2, gy - gw), (cx + s * 0.33, gy), (cx + s * 0.2, gy + gw)], fill=col, width=lw2, joint='curve')
    d.line([(cx + s * 0.06, gy - gw * 1.25), (cx - s * 0.06, gy + gw * 1.25)], fill='#7FD1AE', width=lw2)


def _ic_server(d, cx, cy, s, th):
    lw, w, uh = _lw(s), s * 0.86, s * 0.27
    x0 = cx - w / 2
    for i in range(3):
        y0 = cy - s * 0.45 + i * (uh + s * 0.05)
        d.rounded_rectangle((x0, y0, x0 + w, y0 + uh), s * 0.05, fill=th['icon_fill'], outline=th['icon_line'], width=lw)
        for k in range(3):
            lx = x0 + s * 0.1 + k * s * 0.07
            d.rounded_rectangle((lx, y0 + uh * 0.28, lx + s * 0.035, y0 + uh * 0.72), s * 0.015, fill=th['icon_line'])
        r = s * 0.035
        for k, c in enumerate([_OK, th['accent']]):
            lx = x0 + w - s * 0.12 - k * s * 0.1
            d.ellipse((lx - r, y0 + uh / 2 - r, lx + r, y0 + uh / 2 + r), fill=c)


def _ic_database(d, cx, cy, s, th):
    lw, eh = _lw(s), s * 0.24
    x0, x1, top, bot = cx - s * 0.36, cx + s * 0.36, cy - s * 0.4, cy + s * 0.4
    d.ellipse((x0, bot - eh / 2, x1, bot + eh / 2), fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    d.rectangle((x0, top, x1, bot), fill=th['icon_fill'])
    d.line([(x0 + lw / 2, top), (x0 + lw / 2, bot)], fill=th['icon_line'], width=lw)
    d.line([(x1 - lw / 2, top), (x1 - lw / 2, bot)], fill=th['icon_line'], width=lw)
    for y in (top + (bot - top) / 3, top + 2 * (bot - top) / 3):
        d.arc((x0, y - eh / 2, x1, y + eh / 2), 0, 180, fill=th['icon_line'], width=lw)
    d.ellipse((x0, top - eh / 2, x1, top + eh / 2), fill='white', outline=th['icon_line'], width=lw)
    r = s * 0.035
    d.ellipse((x1 - s * 0.14 - r, bot - s * 0.1 - r, x1 - s * 0.14 + r, bot - s * 0.1 + r), fill=_OK)


def _ic_cloud(d, cx, cy, s, th):
    lw = _lw(s)
    e = [(cx - s * 0.5, cy - s * 0.05, cx - s * 0.1, cy + s * 0.32),
         (cx - s * 0.28, cy - s * 0.35, cx + s * 0.18, cy + s * 0.1),
         (cx + s * 0.02, cy - s * 0.2, cx + s * 0.5, cy + s * 0.32),
         (cx - s * 0.32, cy + s * 0.02, cx + s * 0.3, cy + s * 0.32)]
    _blob(d, e, th['icon_fill'], th['icon_line'], lw)
    arrow(d, (cx, cy + s * 0.22), (cx, cy - s * 0.12), color=th['icon_line'], width=max(5, int(s * 0.05)), head=s * 0.1)


def _ic_shield(d, cx, cy, s, th):
    lw = _lw(s)
    pts = [(cx, cy - s * 0.48), (cx + s * 0.38, cy - s * 0.32), (cx + s * 0.34, cy + s * 0.12),
           (cx, cy + s * 0.48), (cx - s * 0.34, cy + s * 0.12), (cx - s * 0.38, cy - s * 0.32)]
    d.polygon(pts, fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    d.line([(cx - s * 0.16, cy), (cx - s * 0.03, cy + s * 0.13), (cx + s * 0.19, cy - s * 0.13)],
           fill=_OK, width=max(8, int(s * 0.08)), joint='curve')


def _ic_chip(d, cx, cy, s, th):
    lw, h = _lw(s), s * 0.3
    for k in range(4):
        o = -s * 0.2 + k * s * 0.133
        pw = s * 0.035
        d.rectangle((cx + o - pw, cy - s * 0.48, cx + o + pw, cy + s * 0.48), fill=th['icon_line'])
        d.rectangle((cx - s * 0.48, cy + o - pw, cx + s * 0.48, cy + o + pw), fill=th['icon_line'])
    d.rounded_rectangle((cx - h * 1.2, cy - h * 1.2, cx + h * 1.2, cy + h * 1.2), s * 0.06,
                        fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    d.rounded_rectangle((cx - h * 0.7, cy - h * 0.7, cx + h * 0.7, cy + h * 0.7), s * 0.03, fill='white',
                        outline=th['icon_line'], width=max(3, lw // 2))
    d.text((cx, cy), 'AI', font=font(int(s * 0.17), True), fill=th['icon_line'], anchor='mm')


def _ic_network(d, cx, cy, s, th):
    lw = _lw(s)
    outer = [(cx - s * 0.36, cy - s * 0.3), (cx + s * 0.38, cy - s * 0.34), (cx + s * 0.4, cy + s * 0.28),
             (cx - s * 0.3, cy + s * 0.36), (cx - s * 0.44, cy + s * 0.02)]
    for i, p in enumerate(outer):
        d.line([(cx, cy), p], fill=th['icon_line'], width=lw)
        d.line([p, outer[(i + 1) % len(outer)]], fill=th['icon_line'], width=max(3, lw // 2))
    for x, y in outer:
        r = s * 0.08
        d.ellipse((x - r, y - r, x + r, y + r), fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    r = s * 0.14
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=th['accent'], outline=th['icon_line'], width=lw)


def _ic_gear(d, cx, cy, s, th):
    import math
    ro, tw, n = s * 0.34, s * 0.09, 8
    for k in range(n):
        a = 2 * math.pi * k / n
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for dr, dt in [(ro * 0.8, -tw), (ro * 1.38, -tw * 0.8), (ro * 1.38, tw * 0.8), (ro * 0.8, tw)]:
            pts.append((cx + dr * ca - dt * sa, cy + dr * sa + dt * ca))
        d.polygon(pts, fill=th['icon_line'])
    d.ellipse((cx - ro * 1.1, cy - ro * 1.1, cx + ro * 1.1, cy + ro * 1.1), fill=th['icon_line'])
    d.ellipse((cx - ro * 0.85, cy - ro * 0.85, cx + ro * 0.85, cy + ro * 0.85), fill=th['icon_fill'])
    d.ellipse((cx - ro * 0.38, cy - ro * 0.38, cx + ro * 0.38, cy + ro * 0.38), fill='white',
              outline=th['icon_line'], width=_lw(s))


def _ic_chat(d, cx, cy, s, th):
    lw = _lw(s)
    b2 = (cx - s * 0.08, cy - s * 0.02, cx + s * 0.48, cy + s * 0.34)
    d.polygon([(b2[2] - s * 0.14, b2[3] - 2), (b2[2] - s * 0.02, b2[3] + s * 0.12), (b2[2] - s * 0.26, b2[3] - 2)],
              fill='white', outline=th['icon_line'], width=lw)
    d.rounded_rectangle(b2, s * 0.08, fill='white', outline=th['icon_line'], width=lw)
    b1 = (cx - s * 0.48, cy - s * 0.4, cx + s * 0.18, cy + s * 0.08)
    d.polygon([(b1[0] + s * 0.12, b1[3] - 2), (b1[0] + s * 0.04, b1[3] + s * 0.14), (b1[0] + s * 0.28, b1[3] - 2)],
              fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    d.rounded_rectangle(b1, s * 0.09, fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    r, my = s * 0.04, (b1[1] + b1[3]) / 2
    for k in range(3):
        x = (b1[0] + b1[2]) / 2 + (k - 1) * s * 0.14
        d.ellipse((x - r, my - r, x + r, my + r), fill=th['icon_line'])
    for i, rr in enumerate([0.7, 0.45]):
        y = b2[1] + s * (0.12 + i * 0.1)
        d.rounded_rectangle((b2[0] + s * 0.2, y, b2[0] + s * 0.2 + s * 0.3 * rr, y + s * 0.04), s * 0.02, fill=th['bar'])


def _ic_bolt(d, cx, cy, s, th):
    lw, r = _lw(s), s * 0.46
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    pts = [(cx + s * 0.06, cy - s * 0.36), (cx - s * 0.2, cy + s * 0.05), (cx - s * 0.01, cy + s * 0.05),
           (cx - s * 0.08, cy + s * 0.36), (cx + s * 0.2, cy - s * 0.06), (cx + s * 0.01, cy - s * 0.06)]
    d.polygon(pts, fill='#FFC857', outline=th['icon_line'], width=lw)


def _ic_chart(d, cx, cy, s, th):
    lw = _lw(s)
    x0, y0, x1, y1 = cx - s * 0.48, cy - s * 0.4, cx + s * 0.48, cy + s * 0.4
    d.rounded_rectangle((x0, y0, x1, y1), s * 0.06, fill='white', outline=th['icon_line'], width=lw)
    base = y1 - s * 0.1
    for k, hh in enumerate([0.2, 0.34, 0.26, 0.48]):
        bx = x0 + s * 0.12 + k * s * 0.19
        d.rounded_rectangle((bx, base - s * hh, bx + s * 0.12, base), s * 0.02,
                            fill=th['accent'] if k == 3 else th['bar'])
    d.line([(x0 + s * 0.08, base), (x1 - s * 0.08, base)], fill=th['icon_line'], width=max(3, lw // 2))
    arrow(d, (x0 + s * 0.12, y0 + s * 0.42), (x1 - s * 0.1, y0 + s * 0.08), color=_OK,
          width=max(5, int(s * 0.04)), head=s * 0.08)


def _ic_globe(d, cx, cy, s, th):
    import math
    lw, r = _lw(s), s * 0.46
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=th['icon_fill'], outline=th['icon_line'], width=lw)
    d.ellipse((cx - r * 0.45, cy - r, cx + r * 0.45, cy + r), outline=th['icon_line'], width=max(3, lw - 1))
    d.line([(cx, cy - r), (cx, cy + r)], fill=th['icon_line'], width=max(3, lw - 1))
    for dy in (-r * 0.5, 0, r * 0.5):
        hw = math.sqrt(r * r - dy * dy)
        d.line([(cx - hw, cy + dy), (cx + hw, cy + dy)], fill=th['icon_line'], width=max(3, lw - 1))


def _ic_layers(d, cx, cy, s, th):
    lw = _lw(s)
    for k, col in enumerate([th['icon_fill'], th['accent'], 'white']):
        y = cy + s * 0.22 - k * s * 0.2
        pts = [(cx, y - s * 0.2), (cx + s * 0.46, y), (cx, y + s * 0.2), (cx - s * 0.46, y)]
        d.polygon(pts, fill=col, outline=th['icon_line'], width=lw)


_ICON_FN = {'devices': _ic_devices, 'browser': _ic_browser, 'phone': _ic_phone, 'code': _ic_code,
            'server': _ic_server, 'database': _ic_database, 'cloud': _ic_cloud, 'shield': _ic_shield,
            'chip': _ic_chip, 'network': _ic_network, 'gear': _ic_gear, 'chat': _ic_chat, 'bolt': _ic_bolt,
            'chart': _ic_chart, 'globe': _ic_globe, 'layers': _ic_layers}


def icon(d, name, cx, cy, s, th):
    _ICON_FN.get(name, _ic_browser)(d, cx, cy, s, th)


# ── 공통 요소 ──

def _pill(d, x, cy, s, th, size=32, align='center', max_w=600):
    sp = 12 if len(s) <= 12 else 5
    size = fit_size(d, s, max_w - 70, size, True, spacing=sp)
    f = font(size, True)
    tw = sum(d.textlength(ch, font=f) for ch in s) + sp * (len(s) - 1)
    w, h = tw + 70, size + 30
    x0 = x - w / 2 if align == 'center' else x
    d.rounded_rectangle((x0, cy - h / 2, x0 + w, cy + h / 2), h / 2, fill=th['pill'])
    text_c(d, x0 + w / 2, cy, s, size, color=th['pill_ink'], bold=True, spacing=sp)


def _text_l(d, x, cy, s, size, color, bold=True):
    d.text((x, cy), s, font=font(size, bold), fill=color, anchor='lm')


def _dot_grid(d, box, gap, r, color):
    x0, y0, x1, y1 = box
    y = y0
    while y <= y1:
        x = x0
        while x <= x1:
            d.ellipse((x - r, y - r, x + r, y + r), fill=color)
            x += gap
        y += gap


# ── 레이아웃 ──

def _layout_classic(d, lines, badge, caption, ic, th):
    """가운데 흰 패널 + 좌우 아이콘 + 점선 화살표 (기존 스타일)."""
    cloud(d, 150, 165, color=th['deco'])
    cloud(d, 1215, 755, 0.85, color=th['deco'])
    plus(d, 880, 120, color=th['deco2'])
    plus(d, 1420, 640, color=th['deco2'])
    d.ellipse((1400, 200, 1434, 234), fill=th['deco'])
    d.ellipse((120, 700, 166, 746), fill=th['deco'])
    icon(d, ic, 262, 516, 270, th)
    icon(d, _ICON_PARTNER.get(ic, 'browser'), 1274, 500, 270, th)
    arrow(d, (410, 516), (512, 516), color=th['accent'], width=7, dashed=True)
    arrow(d, (1126, 516), (1024, 516), color=th['accent'], width=7, dashed=True)
    rrect(d, (528, 300, 1008, 732), 48, fill=th['panel'], outline=th['icon_line'], width=12)
    size = min(fit_size(d, l, 400, 108, True) for l in lines)
    ys = [410, 528] if len(lines) == 2 else [470]
    for l, y in zip(lines, ys):
        text_c(d, 768, y, l, size, color=th['panel_ink'], bold=True)
    _pill(d, 768, 651, badge, th, max_w=400)
    d.line([(220, 780), (1320, 780)], fill=th['deco2'], width=7)
    text_c(d, 768, 870, caption, fit_size(d, caption, 1100, 44, True, spacing=6), color=th['ink'], bold=True, spacing=6)


def _layout_split(d, lines, badge, caption, ic, th):
    """왼쪽 큰 타이포 + 오른쪽 원형 일러스트."""
    _dot_grid(d, (1310, 70, 1490, 190), 30, 5, th['deco2'])
    _dot_grid(d, (60, 860, 240, 960), 30, 5, th['deco2'])
    d.ellipse((1160 - 320, 512 - 320, 1160 + 320, 512 + 320), fill=th['deco'])
    d.ellipse((1160 - 245, 512 - 245, 1160 + 245, 512 + 245), fill=th['panel'], outline=th['icon_line'], width=10)
    icon(d, ic, 1160, 512, 280, th)
    plus(d, 1440, 820, color=th['deco2'])
    x = 110
    size = min(fit_size(d, l, 660, 150 if len(lines) == 2 else 170, True) for l in lines)
    ys, py = ([430, 430 + size * 1.02], 290) if len(lines) == 2 else ([470], 340)
    by = ys[-1] + size * 0.62 + 20
    cy = by + 90
    _pill(d, x, py, badge, th, size=28, align='left', max_w=520)
    for l, y in zip(lines, ys):
        _text_l(d, x, y, l, size, th['ink'])
    d.rounded_rectangle((x, by, x + 150, by + 14), 7, fill=th['accent'])
    _text_l(d, x, cy, caption, fit_size(d, caption, 660, 46, True), th['sub'])


def _layout_editor(d, lines, badge, caption, ic, th):
    """코드 에디터 창 안에 키워드를 적은 스타일."""
    _dot_grid(d, (40, 40, W - 40, H - 40), 48, 3, th['deco2'])
    x0, y0, x1, y1 = 140, 110, 1396, 900
    d.rounded_rectangle((x0 + 18, y0 + 22, x1 + 18, y1 + 22), 34, fill=th['deco2'])
    d.rounded_rectangle((x0, y0, x1, y1), 34, fill='#16263D')
    d.rounded_rectangle((x0, y0, x1, y0 + 76), 34, fill='#0F1C2E')
    d.rectangle((x0, y0 + 40, x1, y0 + 76), fill='#0F1C2E')
    for i, c in enumerate(_TRAFFIC):
        d.ellipse((x0 + 40 + i * 40 - 11, y0 + 38 - 11, x0 + 40 + i * 40 + 11, y0 + 38 + 11), fill=c)
    tab = '-'.join(lines).lower() + '.md'
    tf = font(24, False)
    tw = d.textlength(tab, font=tf)
    d.rounded_rectangle((x0 + 180, y0 + 16, x0 + 180 + tw + 48, y0 + 76), 12, fill='#16263D')
    d.rectangle((x0 + 180, y0 + 60, x0 + 180 + tw + 48, y0 + 76), fill='#16263D')
    d.text((x0 + 204, y0 + 46), tab, font=tf, fill='#C9D6E8', anchor='lm')
    gx, cx = x0 + 60, x0 + 130
    size = min(fit_size(d, l, 1000, 140, True) for l in lines)
    top = 250 if len(lines) == 2 else 330
    rows = [('c', top)]
    y = top + 50 + size * 0.55
    for _ in lines:
        rows.append(('k', y))
        y += size * 1.08
    rows.append(('p', y + 10))
    rows.append(('e', y + 90))
    ki = 0
    for n, (kind, ry) in enumerate(rows, 1):
        d.text((gx, ry), str(n), font=font(24, False), fill='#4F6380', anchor='rm')
        if kind == 'c':
            _text_l(d, cx, ry, '// ' + badge, fit_size(d, '// ' + badge, 1000, 34, False), '#6B7F99', bold=False)
        elif kind == 'k':
            _text_l(d, cx, ry, lines[ki], size, '#FFFFFF')
            ki += 1
        elif kind == 'p':
            cs = fit_size(d, caption, 880, 46, True)
            _text_l(d, cx, ry, '$', 44, '#FFD166')
            _text_l(d, cx + 56, ry, caption, cs, '#9ECE6A')
            cw = d.textlength(caption, font=font(cs, True))
            d.rectangle((cx + 56 + cw + 12, ry - cs * 0.5, cx + 56 + cw + 34, ry + cs * 0.5), fill='#C9D6E8')
    r = 150
    d.ellipse((1290 - r, 800 - r, 1290 + r, 800 + r), fill=th['panel'], outline=th['icon_line'], width=10)
    icon(d, ic, 1290, 800, 190, th)


def _layout_poster(d, lines, badge, caption, ic, th):
    """대각선 띠 + 거대한 타이포 + 하단 캡션 바."""
    d.polygon([(0, 720), (W, 360), (W, 600), (0, 960)], fill=th['deco'])
    d.ellipse((1210 - 300, 450 - 300, 1210 + 300, 450 + 300), fill=th['deco2'])
    d.ellipse((1210 - 230, 450 - 230, 1210 + 230, 450 + 230), fill=th['panel'], outline=th['icon_line'], width=10)
    icon(d, ic, 1210, 450, 270, th)
    for px, py in [(860, 110), (1470, 820), (110, 720)]:
        plus(d, px, py, color=th['deco2'])
    x = 100
    _pill(d, x, 140, badge, th, size=28, align='left', max_w=620)
    size = min(fit_size(d, l, 780, 190 if len(lines) == 2 else 210, True) for l in lines)
    y = 250 + size * 0.5
    for l in lines:
        _text_l(d, x, y, l, size, th['ink'])
        y += size * 1.0
    d.rectangle((0, 850, W, H), fill=th['pill'])
    d.rectangle((0, 850, W, 862), fill=th['accent'])
    _text_l(d, x, 940, caption, fit_size(d, caption, 1000, 52, True), th['pill_ink'])
    text_c(d, 1330, 940, 'TECHLOG', 26, color=th['pill_ink'], bold=True, spacing=10)


def _layout_emblem(d, lines, badge, caption, ic, th):
    """가운데 원형 엠블럼 아이콘 + 아래 키워드."""
    cx, cy = 768, 290
    for r in (335, 285):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=th['deco2'], width=4)
    d.ellipse((cx - 250, cy - 250, cx + 250, cy + 250), fill=th['deco'])
    d.ellipse((cx - 200, cy - 200, cx + 200, cy + 200), fill=th['panel'], outline=th['icon_line'], width=10)
    icon(d, ic, cx, cy, 240, th)
    for px, py, sz in [(200, 180, 28), (1340, 240, 22), (260, 560, 18), (1300, 600, 30)]:
        plus(d, px, py, s=sz, color=th['deco2'])
    for x, y, r in [(420, 120, 16), (1130, 110, 12), (1440, 460, 20), (90, 400, 14)]:
        d.ellipse((x - r, y - r, x + r, y + r), fill=th['deco2'])
    kw = ' '.join(lines)
    text_c(d, cx, 690, kw, fit_size(d, kw, 1300, 120, True), color=th['ink'], bold=True)
    _pill(d, cx, 805, badge, th, size=30, max_w=700)
    text_c(d, cx, 905, caption, fit_size(d, caption, 1200, 44, True, spacing=6), color=th['sub'], bold=True, spacing=6)


_LAYOUT_FN = {'classic': _layout_classic, 'split': _layout_split, 'editor': _layout_editor,
              'poster': _layout_poster, 'emblem': _layout_emblem}


def thumbnail(path, lines, badge, caption, icon_name='browser', layout='classic', theme='sky'):
    """1536×1024 썸네일. lines=영문 대문자 키워드 1~2줄, badge=영문 부제, caption=한글 카피."""
    th = THEMES.get(theme, THEMES['sky'])
    img, d = canvas(W, H, th['bg'])
    lines = [l for l in lines if l][:2] or ['TECH']
    _LAYOUT_FN.get(layout, _layout_classic)(d, lines, badge, caption, icon_name, th)
    img.save(path)


def flow_diagram(path, title, steps, caption):
    """가로 흐름도. steps = [{'label', 'sub'?, 'note'?}] 3~5개. 가운데 강조는 첫 단계 이후 한 칸."""
    img, d = canvas(1280, 640, 'white')
    text_c(d, 640, 62, title, fit_size(d, title, 1180, 38, True), bold=True)
    steps = steps[:5]
    n = len(steps)
    gap = 56
    bw = (1200 - gap * (n - 1)) / n
    for i, st in enumerate(steps):
        x = 40 + i * (bw + gap)
        hl = (i == 1)
        rrect(d, (x, 200, x + bw, 360), 18, fill='pale' if hl else 'paper', outline='navy', width=5)
        lab = st.get('label', '')
        sub = st.get('sub') or ''
        wrap_text(d, x + bw / 2, 250 if sub else 280, lab, bw - 28, 28, bold=True, min_size=18)
        if sub:
            wrap_text(d, x + bw / 2, 312, sub, bw - 28, 19, color='gray', min_size=15)
        note = st.get('note') or ''
        if note:
            rrect(d, (x + 10, 430, x + bw - 10, 490), 14, fill='white', outline='green', width=4)
            wrap_text(d, x + bw / 2, 460, note, bw - 40, 20, color='green', bold=True, min_size=14, max_lines=1)
            arrow(d, (x + bw / 2, 428), (x + bw / 2, 366), color='green', width=4, head=12)
        if i < n - 1:
            arrow(d, (x + bw + 8, 280), (x + bw + gap - 8, 280), width=6, head=14)
    text_c(d, 640, 580, caption, fit_size(d, caption, 1180, 24), color='navy')
    img.save(path)


def compare_diagram(path, title, left, right, caption):
    """좌우 비교도. left/right = {'title', 'rows': [3개 내외], 'result'}. 좌=빨강(기존), 우=초록(개선)."""
    img, d = canvas(1280, 640, 'white')
    text_c(d, 640, 58, title, fit_size(d, title, 1180, 38, True), bold=True)
    for x, side, color in [(60, left, 'red'), (680, right, 'green')]:
        rrect(d, (x, 110, x + 540, 540), 22, fill='paper', outline=color, width=5)
        t = side.get('title', '')
        wrap_text(d, x + 270, 150, t, 480, 32, color=color, bold=True, min_size=18, max_lines=1)
        rows = (side.get('rows') or [])[:3]
        for i, r in enumerate(rows):
            y = 196 + i * 88
            rrect(d, (x + 60, y, x + 480, y + 60), 14, fill='white', outline='navy', width=4)
            wrap_text(d, x + 270, y + 30, r, 390, 23, min_size=15, line_gap=1.15)
            if i < len(rows) - 1:
                arrow(d, (x + 270, y + 62), (x + 270, y + 86), width=4, head=12)
        res = side.get('result', '')
        rrect(d, (x + 110, 470, x + 430, 520), 25, fill=color)
        wrap_text(d, x + 270, 495, res, 290, 24, color='white', bold=True, min_size=15, max_lines=1)
    text_c(d, 640, 592, caption, fit_size(d, caption, 1180, 24), color='navy')
    img.save(path)
