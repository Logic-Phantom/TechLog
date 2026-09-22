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


def thumbnail_panel(d, lines, badge, caption):
    """가운데 흰 패널 + 영문 대문자 키워드 + 네이비 알약 배지 + 하단 한글 카피."""
    rrect(d, (528, 300, 1008, 732), 48, fill='white', outline='navy', width=12)
    size = 108 if max(len(l) for l in lines) <= 7 else 84
    ys = [410, 528] if len(lines) == 2 else [470]
    for l, y in zip(lines, ys):
        text_c(d, 768, y, l, size, bold=True)
    rrect(d, (580, 620, 956, 682), 31, fill='navy')
    text_c(d, 768, 651, badge, 32, color='white', bold=True, spacing=14)
    d.line([(220, 760), (1320, 760)], fill=C['lblue'], width=7)
    text_c(d, 768, 858, caption, 44, bold=True, spacing=6)
