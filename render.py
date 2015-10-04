import re
import copy
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, TableStyle

pdfmetrics.registerFont(TTFont('TheSansReg', 'resources/TheSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('TheSansRC', 'resources/TheSans-RegularCaps.ttf'))
pdfmetrics.registerFont(TTFont('TheSansBP', 'resources/TheSans-BoldPlain.ttf'))
pdfmetrics.registerFont(TTFont('TheSansBC', 'resources/TheSans-BoldCaps.ttf'))

base_style = getSampleStyleSheet().get('Normal')
base_style.textColor = colors.black


def _get_style(font, size, align):
    style = copy.deepcopy(base_style)
    style.fontName = font
    style.fontSize = float(size)
    style.leading = float(size) * (14.64 / 12.96)
    style.alignment = align
    style.spaceAfter = 0.15 * inch
    return style


def _get_icon(width, height):
    icon = Image('resources/icon_plottwist2.png')
    icon.drawWidth = width
    icon.drawHeight = height
    return icon


def _rewrap(text, num_font=None):
    text = re.sub(r'<\s*br\s*>', r'<br/>', text, flags=re.IGNORECASE)

    if num_font is not None:
        text = re.sub(r'(\d+)', r'<font name="{}">\1</font>'.format(num_font), text)

    return text


def render_plot(data):
    doc = SimpleDocTemplate(
        'plot.pdf',
        pagesize=letter,
        leftMargin=0.293 * inch,
        rightMargin=0.293 * inch,
        topMargin=0.188 * inch,
        bottomMargin=0)

    icon = _get_icon(0.556 * inch, 0.233 * inch)

    def layout(data):
        if data['size']:
            style = _get_style('TheSansBP', data['size'], TA_CENTER)
        else:
            style = _get_style('TheSansBP', 12.96, TA_CENTER)

        inside_table = Table(
            [
                [Paragraph(_rewrap(data['text'], num_font='TheSansBC'), style)], [icon]
            ],
            colWidths=(1.97 * inch),
            rowHeights=(1.844 * inch, 0.233 * inch))

        inside_table.setStyle(TableStyle([
            # Global
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0.15 * inch),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0.15 * inch),
            ('TOPPADDING', (0, 0), (-1, -1), 0.117 * inch),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            # Logo
            ('VALIGN', (0, 1), (0, 1), 'BOTTOM'),
            ('BOTTOMPADDING', (0, 1), (0, 1), 0.063 * inch),
        ]))

        return inside_table

    cells = [layout(x) for x in data]
    rows = [cells[x:x + 4] for x in xrange(0, len(cells), 4)]

    outside_table = Table(rows)

    outside_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('GRID', (0, 0), (-1, -1), 0.02 * inch, (0.341, 0.341, 0.341))
    ]))

    doc.build([outside_table])


def render_trope(data):
    doc = SimpleDocTemplate(
        'trope.pdf',
        pagesize=letter,
        leftMargin=0.418 * inch,
        rightMargin=0.418 * inch,
        topMargin=0.155 * inch,
        bottomMargin=0)

    icon = _get_icon(0.712 * inch, 0.299 * inch)

    def layout(data):
        line_top = Paragraph(
            _rewrap(data['top'], num_font='TheSansBC'),
            _get_style('TheSansBP', 13.92, TA_CENTER))
        line_mid = Paragraph(
            _rewrap(data['mid'], num_font='TheSansRC'),
            _get_style('TheSansReg', 9.77, TA_JUSTIFY))
        line_bot = Paragraph(
            _rewrap(data['bot'], num_font='TheSansBC'),
            _get_style('TheSansBP', 9.77, TA_JUSTIFY))

        inside_table = Table(
            [
                [[line_top, line_mid, line_bot]], [icon]
            ],
            colWidths=(2.5 * inch),
            rowHeights=(2.333 * inch, 0.299 * inch))

        inside_table.setStyle(TableStyle([
            # Global
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0.10 * inch),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0.10 * inch),
            ('TOPPADDING', (0, 0), (-1, -1), 0.117 * inch),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            # Logo
            ('VALIGN', (0, 1), (0, 1), 'BOTTOM'),
            ('BOTTOMPADDING', (0, 1), (0, 1), 0.101 * inch),
        ]))

        return inside_table

    cells = [layout(x) for x in data]
    rows = [cells[x:x + 3] for x in xrange(0, len(cells), 3)]

    outside_table = Table(rows)

    outside_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('GRID', (0, 0), (-1, -1), 0.02 * inch, (0.341, 0.341, 0.341))
    ]))

    doc.build([outside_table])
