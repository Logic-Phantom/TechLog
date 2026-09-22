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


def thumbnail_base():
    """README 6절: 연하늘 배경 + 구름/플러스 장식."""
    img, d = canvas(1536, 1024, 'bg')
    cloud(d, 150, 165)
    cloud(d, 1215, 755, 0.85)
    plus(d, 880, 120)
    plus(d, 1420, 640)
    d.ellipse((1400, 200, 1434, 234), fill=C['pale'])
    d.ellipse((120, 700, 166, 746), fill=C['pale'])
    return img, d


def fit_size(d, s, max_w, size, bold=False, min_size=14, spacing=0):
    """max_w 안에 들어가도록 폰트 크기를 줄인다."""
    while size > min_size:
        f = font(size, bold)
        w = d.textlength(s, font=f) + spacing * max(len(s) - 1, 0)
        if w <= max_w:
            break
        size -= 2
    return size


def thumbnail_panel(d, lines, badge, caption):
    """가운데 흰 패널 + 영문 대문자 키워드 + 네이비 알약 배지 + 하단 한글 카피."""
    rrect(d, (528, 300, 1008, 732), 48, fill='white', outline='navy', width=12)
    lines = lines[:2]
    size = min(fit_size(d, l, 400, 108, True) for l in lines)
    ys = [410, 528] if len(lines) == 2 else [470]
    for l, y in zip(lines, ys):
        text_c(d, 768, y, l, size, bold=True)
    rrect(d, (580, 620, 956, 682), 31, fill='navy')
    sp = 14 if len(badge) <= 12 else 6
    text_c(d, 768, 651, badge, fit_size(d, badge, 330, 32, True, spacing=sp), color='white', bold=True, spacing=sp)
    d.line([(220, 760), (1320, 760)], fill=C['lblue'], width=7)
    text_c(d, 768, 858, caption, fit_size(d, caption, 1100, 44, True, spacing=6), bold=True, spacing=6)


def thumbnail_devices(d, left_label='OK'):
    """좌: 스마트폰, 우: 모니터 + 가운데 패널을 향하는 점선 화살표."""
    rrect(d, (140, 350, 340, 720), 36, fill='lblue', outline='navy', width=10)
    rrect(d, (165, 395, 315, 672), 14, fill='white')
    d.rounded_rectangle((210, 367, 270, 377), 5, fill=C['navy'])
    d.ellipse((228, 688, 252, 712), fill=C['navy'])
    for i, w in enumerate([100, 70, 100]):
        d.rectangle((188, 430 + i * 30, 188 + w, 444 + i * 30), fill=C['lblue'])
    d.ellipse((188, 620, 212, 644), fill=C['green'])
    d.text((222, 632), left_label, font=font(22, True), fill=C['navy'], anchor='lm')
    arrow(d, (348, 490), (516, 490), color='blue', width=7, dashed=True)
    rrect(d, (1196, 370, 1456, 570), 22, fill='lblue', outline='navy', width=10)
    rrect(d, (1218, 392, 1434, 548), 10, fill='white')
    for i, w in enumerate([140, 100, 124]):
        d.rectangle((1240, 420 + i * 30, 1240 + w, 434 + i * 30), fill=C['lblue'])
    d.ellipse((1240, 508, 1262, 530), fill=C['green'])
    d.rectangle((1314, 570, 1338, 612), fill=C['navy'])
    d.rounded_rectangle((1276, 610, 1376, 630), 10, fill=C['navy'])
    arrow(d, (1188, 490), (1020, 490), color='blue', width=7, dashed=True)


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
        text_c(d, x + bw / 2, 262, lab, fit_size(d, lab, bw - 30, 28, True), bold=True)
        sub = st.get('sub') or ''
        if sub:
            text_c(d, x + bw / 2, 306, sub, fit_size(d, sub, bw - 30, 19), color='gray')
        note = st.get('note') or ''
        if note:
            rrect(d, (x + 10, 430, x + bw - 10, 490), 14, fill='white', outline='green', width=4)
            text_c(d, x + bw / 2, 460, note, fit_size(d, note, bw - 40, 20, True), color='green', bold=True)
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
        text_c(d, x + 270, 150, t, fit_size(d, t, 480, 32, True), color=color, bold=True)
        rows = (side.get('rows') or [])[:3]
        for i, r in enumerate(rows):
            y = 196 + i * 88
            rrect(d, (x + 60, y, x + 480, y + 60), 14, fill='white', outline='navy', width=4)
            text_c(d, x + 270, y + 30, r, fit_size(d, r, 390, 23), color='navy')
            if i < len(rows) - 1:
                arrow(d, (x + 270, y + 62), (x + 270, y + 86), width=4, head=12)
        res = side.get('result', '')
        rrect(d, (x + 110, 470, x + 430, 520), 25, fill=color)
        text_c(d, x + 270, 495, res, fit_size(d, res, 290, 24, True), color='white', bold=True)
    text_c(d, 640, 592, caption, fit_size(d, caption, 1180, 24), color='navy')
    img.save(path)
