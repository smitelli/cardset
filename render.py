import re
import copy
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, TableStyle

br_finder = re.compile('<\s*br\s*>', re.IGNORECASE)


def render_plot(data):
    _render(data, 'plot.pdf', 4)


def _render(data, filename, width):
    styles = getSampleStyleSheet()
    s = styles['Normal']
    s.alignment = TA_CENTER
    s.fontName = 'TheSansBP'
    s.fontSize = 12.96
    s.leading = 14.64
    s.textColor = colors.black

    icon = Image('resources/icon_plottwist2.png')
    icon.drawWidth = 0.556 * inch
    icon.drawHeight = 0.233 * inch

    pdfmetrics.registerFont(TTFont('TheSansBP', 'resources/TheSans-BoldPlain.ttf'))

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=0.293 * inch,
        rightMargin=0.293 * inch,
        topMargin=0.188 * inch,
        bottomMargin=0)

    def layout(data):
        text = br_finder.sub('<br/>', data['text'])

        if data['size']:
            ls = copy.deepcopy(s)
            ls.fontSize = float(data['size'])
            ls.leading = float(data['size']) * (float(s.leading) / float(s.fontSize))
        else:
            ls = s

        it = Table(
            [
                [Paragraph(text, ls)],
                [icon]
            ],
            colWidths=(1.97 * inch),
            rowHeights=(1.844 * inch, 0.233 * inch))

        it.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0.15 * inch),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0.15 * inch),
            ('TOPPADDING', (0, 0), (-1, -1), 0.117 * inch),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            # Logo stuff
            ('VALIGN', (0, 1), (0, 1), 'BOTTOM'),
            ('BOTTOMPADDING', (0, 1), (0, 1), 0.063 * inch),
        ]))

        return it

    data = [layout(x) for x in data]
    rows = [data[x:x + width] for x in xrange(0, len(data), width)]

    t = Table(rows)

    t.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('GRID', (0, 0), (-1, -1), 0.02 * inch, (0.341, 0.341, 0.341))
    ]))

    doc.build([t])
