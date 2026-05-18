#!/usr/bin/env python3
"""
Shared PDF Utility Library for Pastor AI Skills
Reusable components for generating branded PDF documents.

Aesthetic: "Quiet Doctrine" — editorial restraint inspired by 16th-century
Reformed printing tradition (Estienne, Geneva 1560) interpreted through
modern editorial typography. See docs/design-philosophy-quiet-doctrine.md.

Required: pip install reportlab
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily


# --- Font registration (Quiet Doctrine) ---

_HERE = os.path.dirname(os.path.abspath(__file__))
_FONT_DIR = os.path.join(_HERE, "fonts")


def _try_register_font(font_name, filename):
    """Register a TTF if present; return True on success."""
    path = os.path.join(_FONT_DIR, filename)
    if not os.path.exists(path):
        return False
    try:
        pdfmetrics.registerFont(TTFont(font_name, path))
        return True
    except Exception:
        return False


_HAS_CRIMSON = (
    _try_register_font("CrimsonPro", "CrimsonPro-Regular.ttf")
    and _try_register_font("CrimsonPro-Bold", "CrimsonPro-Bold.ttf")
    and _try_register_font("CrimsonPro-Italic", "CrimsonPro-Italic.ttf")
)
if _HAS_CRIMSON:
    registerFontFamily(
        "CrimsonPro",
        normal="CrimsonPro",
        bold="CrimsonPro-Bold",
        italic="CrimsonPro-Italic",
    )

_HAS_ARSENAL = _try_register_font("ArsenalSC", "ArsenalSC-Regular.ttf")

# Font role aliases — graceful fallback to Type 1 builtins if TTFs missing
SERIF_BODY = "CrimsonPro" if _HAS_CRIMSON else "Times-Roman"
SERIF_BOLD = "CrimsonPro-Bold" if _HAS_CRIMSON else "Times-Bold"
SERIF_ITALIC = "CrimsonPro-Italic" if _HAS_CRIMSON else "Times-Italic"
SMALL_CAPS = "ArsenalSC" if _HAS_ARSENAL else "Helvetica-Bold"


# --- Color Palette (Quiet Doctrine) ---
# Deep ink, patinated bronze accent, warm parchment — restrained and patient.

NAVY = HexColor("#1A2438")           # Deep ink, slightly bluish
GOLD = HexColor("#8C6B3A")           # Patinated bronze (was bright gold)
GOLD_LIGHT = HexColor("#B89968")     # Pale bronze (rare use)
BODY_COLOR = HexColor("#1F1F1F")     # Solid ink for body
SLATE = HexColor("#5A5A5A")          # Warm neutral gray
MED_GRAY = HexColor("#9A9A9A")       # Mid gray for footers
LIGHT_BG = HexColor("#FAF7F1")       # Warm cream parchment
RULE_GRAY = HexColor("#C9C2B5")      # Warm rule gray
WHITE = HexColor("#FFFFFF")
PASSAGE_PALE = HexColor("#C8D3E5")   # Banner subtitle ink
META_PALE = HexColor("#7A8AA0")      # Banner meta ink

# Page geometry — narrow margins for editorial density
# Letter (8.5") minus 0.75" margins each side = 7.0" content width
PAGE_MARGIN = 0.75 * inch
CONTENT_WIDTH = 7.0 * inch


# --- Styles ---

def build_styles():
    """Create custom paragraph styles for the document (Quiet Doctrine)."""
    s = {}

    # --- Title banner styles (white on deep ink) ---
    # Inverted hierarchy: small caps label above, large passage subject below.
    s["title"] = ParagraphStyle(
        "Title", fontName=SMALL_CAPS, fontSize=11, leading=14,
        textColor=PASSAGE_PALE, spaceAfter=10, wordSpace=2,
    )
    s["passage"] = ParagraphStyle(
        "Passage", fontName=SERIF_BOLD, fontSize=30, leading=36,
        textColor=WHITE, spaceAfter=14,
    )
    s["meta"] = ParagraphStyle(
        "Meta", fontName=SMALL_CAPS, fontSize=8.5, leading=12,
        textColor=META_PALE, wordSpace=1.5,
    )

    # --- Section headers (small caps via ArsenalSC, no rule below) ---
    # Sized for strong visual hierarchy — easy section-spotting when scanning.
    # keepWithNext is INTENTIONALLY NOT set: it causes huge white space when
    # the immediately following flowable is a multi-page splittable table
    # (reportlab pushes both to the next page). For sections where header
    # orphaning is a real risk (e.g. shaded box at end), use an explicit
    # KeepTogether wrapper at the call site instead.
    s["section_header"] = ParagraphStyle(
        "SectionHeader", fontName=SMALL_CAPS, fontSize=16, leading=20,
        textColor=NAVY, spaceBefore=22, spaceAfter=12, wordSpace=2,
    )

    # --- Body (CrimsonPro, generous leading for sustained reading) ---
    s["body"] = ParagraphStyle(
        "Body", fontName=SERIF_BODY, fontSize=11, leading=17,
        textColor=BODY_COLOR, spaceAfter=10, alignment=TA_JUSTIFY,
    )
    s["body_bold"] = ParagraphStyle(
        "BodyBold", fontName=SERIF_BOLD, fontSize=11.5, leading=15,
        textColor=NAVY, spaceAfter=2, keepWithNext=1,
    )
    s["body_label"] = ParagraphStyle(
        # Quiet small caps in slate — never gold (Quiet Doctrine: bronze is rare)
        "BodyLabel", fontName=SMALL_CAPS, fontSize=8, leading=11,
        textColor=SLATE, spaceAfter=2, wordSpace=1.5,
    )
    s["body_content"] = ParagraphStyle(
        "BodyContent", fontName=SERIF_BODY, fontSize=11, leading=17,
        textColor=BODY_COLOR, spaceAfter=10, leftIndent=0,
        alignment=TA_JUSTIFY,
    )
    # Tighter variant for theme blocks (compress vertical rhythm slightly)
    s["body_content_tight"] = ParagraphStyle(
        "BodyContentTight", fontName=SERIF_BODY, fontSize=11, leading=15,
        textColor=BODY_COLOR, spaceAfter=6, leftIndent=0,
        alignment=TA_JUSTIFY,
    )

    # --- Cross-reference entries (definition-list style) ---
    s["xref_head"] = ParagraphStyle(
        "XrefHead", fontName=SERIF_BOLD, fontSize=11, leading=14,
        textColor=NAVY, spaceBefore=4, spaceAfter=1, keepWithNext=1,
    )
    s["xref_body"] = ParagraphStyle(
        "XrefBody", fontName=SERIF_BODY, fontSize=10.5, leading=15,
        textColor=BODY_COLOR, leftIndent=14, spaceAfter=10,
        alignment=TA_JUSTIFY,
    )

    # --- Bullets (kept for compatibility; bronze marker, restrained) ---
    s["bullet"] = ParagraphStyle(
        "Bullet", fontName=SERIF_BODY, fontSize=11, leading=17,
        textColor=BODY_COLOR, leftIndent=18, spaceAfter=8,
        bulletIndent=4, bulletFontName=SERIF_BOLD,
        bulletFontSize=9, bulletColor=GOLD,
    )

    # --- Thinking prompts (italic serif inside shaded box) ---
    # Slightly compressed (vs body) so the section can stay close to its predecessor.
    s["prompt"] = ParagraphStyle(
        "Prompt", fontName=SERIF_ITALIC, fontSize=10.5, leading=14,
        textColor=BODY_COLOR, spaceAfter=5, leftIndent=0,
        alignment=TA_LEFT,
    )

    # --- Table styles (open editorial table, no heavy fills) ---
    s["table_header"] = ParagraphStyle(
        "TableHeader", fontName=SMALL_CAPS, fontSize=9,
        leading=12, textColor=NAVY, wordSpace=1,
    )
    s["table_cell"] = ParagraphStyle(
        "TableCell", fontName=SERIF_BODY, fontSize=9,
        leading=12.5, textColor=BODY_COLOR,
    )
    s["table_cell_bold"] = ParagraphStyle(
        "TableCellBold", fontName=SERIF_BOLD, fontSize=9,
        leading=12.5, textColor=NAVY,
    )

    # --- Brand banner styles (legacy, kept for unaffected skills) ---
    s["brand_body"] = ParagraphStyle(
        "BrandBody", fontName=SERIF_BODY, fontSize=9, leading=13,
        textColor=PASSAGE_PALE,
    )
    s["brand_url"] = ParagraphStyle(
        "BrandURL", fontName=SMALL_CAPS, fontSize=10, leading=14,
        textColor=GOLD_LIGHT, spaceBefore=4,
    )

    return s


# --- Helper: Section header (Quiet Doctrine: small caps, no rule) ---

def section_header(story, title, styles):
    """Add a section header in small caps. No rule below — typography alone marks the boundary."""
    story.append(Paragraph(title, styles["section_header"]))


# --- Text Section ---

def add_section(story, title, content, styles):
    """Add a text section with header and body paragraphs."""
    section_header(story, title, styles)

    if isinstance(content, str):
        for p in content.split("\n\n"):
            p = p.strip()
            if p:
                story.append(Paragraph(p, styles["body"]))
    elif isinstance(content, list):
        for item in content:
            story.append(Paragraph(item, styles["body"]))


# --- Bullet List ---

def add_bullet_list(story, items, styles):
    """Add a list of strings as gold-bulleted paragraphs."""
    for item in items:
        story.append(Paragraph(item, styles["bullet"], bulletText="\u2022"))


# --- Generic Table ---

def add_table(story, headers, rows, col_widths, styles):
    """Add a styled table with navy header, gold accent, and alternating rows.

    Args:
        story: The PDF story list to append to.
        headers: List of header strings.
        rows: List of lists of strings.
        col_widths: List of floats in inches (converted to points inside).
        styles: Dict of ParagraphStyles from build_styles().
    """
    col_widths_pts = [w * inch for w in col_widths]

    # Header style: white text on navy fill (cell-level TEXTCOLOR is overridden
    # by Paragraph's own textColor, so we mint a local style instead of using
    # the public `table_header` which is navy-on-white for open editorial tables).
    header_style = ParagraphStyle(
        "TableHeaderInverse", parent=styles["table_header"], textColor=WHITE,
    )
    header_row = [Paragraph(h, header_style) for h in headers]
    table_data = [header_row]

    for row in rows:
        table_data.append([Paragraph(cell, styles["table_cell"]) for cell in row])

    table = Table(table_data, colWidths=col_widths_pts, repeatRows=1)

    style_commands = [
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        # Gold line below header
        ("LINEBELOW", (0, 0), (-1, 0), 2, GOLD),
        # All cells
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        # Subtle grid
        ("GRID", (0, 0), (-1, 0), 0, WHITE),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, RULE_GRAY),
        ("LINEBEFORE", (1, 1), (-1, -1), 0.5, RULE_GRAY),
    ]

    # Alternating row backgrounds
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            style_commands.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BG))

    table.setStyle(TableStyle(style_commands))
    story.append(table)
    story.append(Spacer(1, 16))


# --- Shaded Box (gold left border + cream background) ---

def add_shaded_box(story, elements, styles):
    """Add content inside a gold-left-border + cream background container.

    Args:
        story: The PDF story list to append to.
        elements: List of Paragraph/Spacer flowables to place inside the box.
        styles: Dict of ParagraphStyles from build_styles().
    """
    gold_bar_width = 4
    content_col_width = CONTENT_WIDTH - gold_bar_width - 2

    box = Table(
        [[None, elements]],
        colWidths=[gold_bar_width, content_col_width],
    )
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), GOLD),
        ("BACKGROUND", (1, 0), (1, -1), LIGHT_BG),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 0),
        ("TOPPADDING", (0, 0), (0, -1), 0),
        ("BOTTOMPADDING", (0, 0), (0, -1), 0),
        ("LEFTPADDING", (1, 0), (1, -1), 14),
        ("RIGHTPADDING", (1, 0), (1, -1), 14),
        ("TOPPADDING", (1, 0), (1, -1), 10),
        ("BOTTOMPADDING", (1, 0), (1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(box)


# --- Title Banner (generalized) ---

def add_title_banner(story, title_text, subtitle_text, meta_parts, styles):
    """Add a full-width deep-ink banner with editorial inverted hierarchy.

    The document type label (title_text) is rendered as a small-caps tag above
    a large serif passage reference (subtitle_text). A single thin bronze rule
    seals the banner. This is the only moment of visual weight in the document.

    Args:
        story: The PDF story list to append to.
        title_text: Document type label, e.g. "RECHERCHE EXÉGÉTIQUE".
        subtitle_text: Subject line, e.g. "Luc 17.1-10".
        meta_parts: List of strings joined with " · ", e.g. ["2026-05-02", "Pastor Name"].
        styles: Dict of ParagraphStyles from build_styles().
    """
    banner_content = []
    banner_content.append(Paragraph(title_text, styles["title"]))
    if subtitle_text:
        banner_content.append(Paragraph(subtitle_text, styles["passage"]))
    if meta_parts:
        banner_content.append(
            Paragraph(" · ".join(meta_parts), styles["meta"])
        )

    banner = Table(
        [[banner_content]],
        colWidths=[CONTENT_WIDTH],
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 30),
        ("RIGHTPADDING", (0, 0), (-1, -1), 30),
        ("TOPPADDING", (0, 0), (-1, -1), 32),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 28),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(banner)

    # Single thin bronze rule — the rare punctuation
    story.append(HRFlowable(
        width="100%", thickness=1, color=GOLD,
        spaceBefore=0, spaceAfter=30
    ))


# --- REACHRIGHT Branding Banner ---

REACHRIGHT_BLURBS = {
    "en": (
        "Built by REACHRIGHT. We help churches get found online: custom websites, "
        "Google Ad Grants, local SEO, and social media done for you. "
        "If this tool saved you time this week, we can save you a lot more."
    ),
    "fr": (
        "Développé par REACHRIGHT. Nous aidons les Églises à se faire connaître en ligne : "
        "sites web sur mesure, subventions Google Ad Grants, référencement local et "
        "médias sociaux clés en main. Si cet outil vous a fait gagner du temps cette semaine, "
        "nous pouvons vous en faire gagner beaucoup plus."
    ),
}


def add_reachright_footer(story, styles, language="en"):
    """Add REACHRIGHT branding as a navy banner at the end.

    Args:
        story: The PDF story list to append to.
        styles: Dict of ParagraphStyles from build_styles().
        language: "en" (default) or "fr" for the marketing copy.
    """
    story.append(Spacer(1, 30))

    blurb = REACHRIGHT_BLURBS.get(language, REACHRIGHT_BLURBS["en"])

    brand_content = []
    brand_content.append(Paragraph(blurb, styles["brand_body"]))
    brand_content.append(Paragraph("reachrightstudios.com", styles["brand_url"]))

    banner = Table(
        [[brand_content]],
        colWidths=[CONTENT_WIDTH],
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        # Gold top accent
        ("LINEABOVE", (0, 0), (-1, 0), 3, GOLD),
    ]))
    story.append(banner)


# --- Page Footer (canvas callback factory) ---

FOOTER_LABELS = {
    "en": {"powered_by": "Powered by REACHRIGHT", "page": "Page"},
    "fr": {"powered_by": "Propulsé par REACHRIGHT", "page": "Page"},
}


def make_page_footer(brand="reachright", language="en"):
    """Return a canvas callback for page footers.

    Args:
        brand: "reachright" for gold rule + "Powered by REACHRIGHT" + page number.
               "church" for thin gray rule + page number only.
        language: "en" (default) or "fr" for footer labels.
    """
    labels = FOOTER_LABELS.get(language, FOOTER_LABELS["en"])

    def _footer(canvas_obj, doc):
        canvas_obj.saveState()
        page_width = letter[0]
        margin = PAGE_MARGIN
        rule_y = 0.45 * inch
        text_y = 0.28 * inch

        if brand == "reachright":
            # Thin bronze rule
            canvas_obj.setStrokeColor(GOLD)
            canvas_obj.setLineWidth(0.4)
            canvas_obj.line(margin, rule_y, page_width - margin, rule_y)

            # "Powered by REACHRIGHT" left, small caps
            canvas_obj.setFont(SMALL_CAPS, 7.5)
            canvas_obj.setFillColor(SLATE)
            canvas_obj.drawString(margin, text_y, labels["powered_by"])

            # Page number right, small caps
            page_num = canvas_obj.getPageNumber()
            canvas_obj.drawRightString(
                page_width - margin, text_y,
                f"{labels['page']}  {page_num}"
            )

        elif brand == "church":
            # Hairline warm-gray rule, set high so the footer floats
            canvas_obj.setStrokeColor(RULE_GRAY)
            canvas_obj.setLineWidth(0.4)
            canvas_obj.line(margin, rule_y, page_width - margin, rule_y)

            # Small caps page number, right-aligned
            canvas_obj.setFont(SMALL_CAPS, 8)
            canvas_obj.setFillColor(SLATE)
            page_num = canvas_obj.getPageNumber()
            canvas_obj.drawRightString(
                page_width - margin, text_y,
                f"{labels['page']}  {page_num}"
            )

        canvas_obj.restoreState()

    return _footer


# --- Document Creation ---

def create_doc(output_path, title="", author=""):
    """Create and return a SimpleDocTemplate with standard layout.

    Letter size, 1" side margins, 0.85" top/bottom margins.

    Args:
        output_path: File path for the PDF.
        title: PDF metadata title.
        author: PDF metadata author.

    Returns:
        A SimpleDocTemplate instance.
    """
    return SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=PAGE_MARGIN,
        rightMargin=PAGE_MARGIN,
        topMargin=PAGE_MARGIN,
        bottomMargin=PAGE_MARGIN,
        title=title,
        author=author,
    )
