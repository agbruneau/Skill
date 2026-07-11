#!/usr/bin/env python3
"""
Sermon Research PDF Generator
Converts structured sermon research JSON into a formatted PDF document.

Usage: python generate-pdf.py <input.json> [output.pdf]

Required: pip install reportlab
"""

import json
import sys
import os

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "..", "shared"))

from pdf_utils import (
    NAVY, GOLD, SLATE, LIGHT_BG, RULE_GRAY, WHITE,
    LEFT_MARGIN, RIGHT_MARGIN, BOTTOM_MARGIN, PAGE_W,
    build_styles, section_header, add_section, add_title_banner,
    create_doc,
)
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle


# ponytail: shared pdf_utils.py was retooled for the MacArthur variant and no
# longer exports add_reachright_footer/add_shaded_box, and its
# make_page_footer hardcodes "perspective John MacArthur" regardless of
# scope. Kept local here instead of touching the shared file, so the
# MacArthur flow (which depends on the current shared API) stays untouched.
# Upgrade path: if the shared module regains generic (non-MacArthur) footer
# support, drop these locals and import from pdf_utils again.

def add_shaded_box(story, elements, styles):
    """Cream box with a gold left rule, holding a list of flowables."""
    content_width = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN
    t = Table([[e] for e in elements], colWidths=[content_width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t)


def add_reachright_footer(story, styles):
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=6))
    story.append(Paragraph(
        "Document de préparation : un point de départ pour l'étude, "
        "pas un substitut à la prière et à l'Esprit.",
        styles["body_label"],
    ))


def _page_footer(canvas, doc):
    canvas.saveState()
    y = BOTTOM_MARGIN - 22
    canvas.setStrokeColor(RULE_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(LEFT_MARGIN, y + 10, PAGE_W - RIGHT_MARGIN, y + 10)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(SLATE)
    canvas.drawString(LEFT_MARGIN, y, "Recherche de préparation de sermon")
    canvas.drawRightString(PAGE_W - RIGHT_MARGIN, y, f"Page {doc.page}")
    canvas.restoreState()


# --- Sermon-specific layout functions ---


def add_word_studies(story, word_studies, styles):
    """Add the word study table with refined styling."""
    section_header(story, "Étude des mots-clés", styles)

    if not word_studies:
        story.append(Paragraph("Aucune étude de mots fournie.", styles["body"]))
        return

    headers = [
        "Mot", "Translitération",
        "Sens littéral", "Champ sémantique", "Traductions comparées"
    ]

    header_row = [Paragraph(h, styles["table_header"]) for h in headers]
    table_data = [header_row]

    for ws in word_studies:
        translations = ws.get("translations", {})
        trans_parts = []
        for k, v in translations.items():
            trans_parts.append(f"<b>{k}</b>: {v}")
        trans_text = ", ".join(trans_parts) if trans_parts else ""

        row = [
            Paragraph(ws.get("english", ""), styles["table_cell_bold"]),
            Paragraph(ws.get("transliteration", ""), styles["table_cell"]),
            Paragraph(ws.get("literal_meaning", ""), styles["table_cell"]),
            Paragraph(ws.get("range_of_meaning", ""), styles["table_cell"]),
            Paragraph(trans_text, styles["table_cell"]),
        ]
        table_data.append(row)

    col_widths = [0.9 * inch, 0.95 * inch, 1.0 * inch, 1.8 * inch, 1.85 * inch]

    table = Table(table_data, colWidths=col_widths, repeatRows=1)

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


def add_cross_references(story, cross_refs, styles):
    """Add cross-references as a formatted bullet list."""
    section_header(story, "Renvois et passages parallèles", styles)

    if not cross_refs:
        story.append(Paragraph("Aucun renvoi fourni.", styles["body"]))
        return

    for ref in cross_refs:
        reference = ref.get("reference", "")
        connection = ref.get("connection", "")
        conn_type = ref.get("type", "")

        type_label = f'  <font color="#{SLATE.hexval()[2:]}">[{conn_type}]</font>' if conn_type else ""
        text = f"<b>{reference}</b>{type_label}:  {connection}"
        story.append(Paragraph(text, styles["bullet"], bulletText="\u2022"))


def add_theological_themes(story, themes, styles):
    """Add theological themes with structured sub-sections."""
    section_header(story, "Thèmes théologiques", styles)

    if not themes:
        story.append(Paragraph("Aucun thème fourni.", styles["body"]))
        return

    from reportlab.platypus import HRFlowable

    for theme in themes:
        name = theme.get("name", "")
        in_text = theme.get("in_text", "")
        implication = theme.get("implication", "")

        # Theme name with gold underline
        story.append(Paragraph(name, styles["body_bold"]))
        story.append(HRFlowable(
            width="30%", thickness=1.5, color=GOLD,
            spaceBefore=0, spaceAfter=8
        ))

        if in_text:
            story.append(Paragraph("DANS LE TEXTE", styles["body_label"]))
            story.append(Paragraph(in_text, styles["body_content"]))

        if implication:
            story.append(Paragraph("POUR VOTRE ASSEMBLÉE", styles["body_label"]))
            story.append(Paragraph(implication, styles["body_content"]))

        story.append(Spacer(1, 8))


def add_thinking_prompts(story, prompts, styles):
    """Add thinking prompts inside a shaded container with gold left border."""
    section_header(story, "Pistes de réflexion", styles)

    if not prompts:
        story.append(Paragraph("Aucune piste fournie.", styles["body"]))
        return

    # Build prompt paragraphs
    prompt_elements = []
    for i, prompt in enumerate(prompts, 1):
        prompt_elements.append(
            Paragraph(f"<b>{i}.</b>  {prompt}", styles["prompt"])
        )

    add_shaded_box(story, prompt_elements, styles)


# --- Main Generator ---

def generate_pdf(json_path, output_path=None):
    """Generate a formatted PDF from sermon research JSON data."""

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not output_path:
        passage = data.get("passage", "recherche")
        safe_name = passage.replace(":", "-").replace(" ", "-")
        output_path = f"Recherche-Sermon-{safe_name}.pdf"

    doc = create_doc(
        output_path,
        title=f"Recherche de sermon : {data.get('passage', '')}",
        author=data.get("pastor_name", ""),
    )

    styles = build_styles()
    # ponytail: shared build_styles() dropped "bullet" and "body_content"
    # when it was retooled for the MacArthur variant. Patched locally
    # for the same reason as the footer helpers above.
    styles.setdefault("body_content", styles["body_content_tight"])
    styles.setdefault("bullet", ParagraphStyle(
        "bullet", parent=styles["body"], leftIndent=14, bulletIndent=0,
    ))
    story = []

    # Title banner
    meta_parts = []
    if data.get("date"):
        meta_parts.append(data["date"])
    if data.get("pastor_name"):
        meta_parts.append(data["pastor_name"])
    if data.get("church_name"):
        meta_parts.append(data["church_name"])

    add_title_banner(story, "RECHERCHE DE SERMON", data.get("passage", ""), meta_parts, styles)

    # Sections
    if data.get("passage_context"):
        add_section(story, "Contexte du passage", data["passage_context"], styles)

    if data.get("historical_background"):
        add_section(
            story, "Arrière-plan historique et culturel",
            data["historical_background"], styles
        )

    if data.get("word_studies"):
        add_word_studies(story, data["word_studies"], styles)

    if data.get("commentary_insights"):
        add_section(
            story, "Apports des commentateurs",
            data["commentary_insights"], styles
        )

    if data.get("cross_references"):
        add_cross_references(story, data["cross_references"], styles)

    if data.get("theological_themes"):
        add_theological_themes(story, data["theological_themes"], styles)

    if data.get("thinking_prompts"):
        add_thinking_prompts(story, data["thinking_prompts"], styles)

    # REACHRIGHT branding
    add_reachright_footer(story, styles)

    doc.build(story, onFirstPage=_page_footer, onLaterPages=_page_footer)

    return os.path.abspath(output_path)


# --- CLI Entry ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate-pdf.py <input.json> [output.pdf]")
        sys.exit(1)

    json_input = sys.argv[1]
    pdf_output = sys.argv[2] if len(sys.argv) > 2 else None

    result_path = generate_pdf(json_input, pdf_output)
    print(f"PDF generated: {result_path}")
