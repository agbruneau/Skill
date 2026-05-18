#!/usr/bin/env python3
"""Sermon Series PDF Generator (also writes a Markdown sibling file)."""

import json
import sys
import os

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "..", "shared"))

from pdf_utils import (
    build_styles, section_header, add_section, add_title_banner,
    make_page_footer, create_doc, add_table,
)
from reportlab.platypus import Paragraph


def add_practical_notes(story, notes, styles):
    section_header(story, "Notes pratiques", styles)
    if notes.get("duration_check"):
        story.append(Paragraph("VÉRIFICATION DE LA DURÉE", styles["body_label"]))
        story.append(Paragraph(notes["duration_check"], styles["body_content"]))
    if notes.get("special_attention"):
        story.append(Paragraph("SEMAINES À TRAITER AVEC SOIN", styles["body_label"]))
        story.append(Paragraph(notes["special_attention"], styles["body_content"]))
    if notes.get("launch_recommendation"):
        story.append(Paragraph("RECOMMANDATION POUR LE LANCEMENT", styles["body_label"]))
        story.append(Paragraph(notes["launch_recommendation"], styles["body_content"]))


def _md_escape_cell(text):
    """Escape pipe and newline characters so the cell stays inside one Markdown table row."""
    if text is None:
        return ""
    return str(text).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def _md_paragraphs(text):
    if not text:
        return ""
    return text.strip()


def generate_markdown(data, output_path):
    """Write a Markdown file mirroring the PDF structure."""
    lines = []

    title = data.get("series_title", "")
    subtitle = title
    if data.get("series_tagline"):
        subtitle = f"{title} : {data['series_tagline']}"
    lines.append(f"# Série de prédications : {subtitle}".rstrip())
    lines.append("")

    meta_parts = [p for p in [data.get("date"), data.get("pastor_name"), data.get("church_name")] if p]
    if meta_parts:
        lines.append(" · ".join(f"**{p}**" for p in meta_parts))
        lines.append("")

    lines.append("---")
    lines.append("")

    if data.get("scope_assessment"):
        lines.append("## Évaluation de la portée")
        lines.append("")
        lines.append(_md_paragraphs(data["scope_assessment"]))
        lines.append("")

    if data.get("title_options"):
        lines.append("## Propositions de titre")
        lines.append("")
        lines.append("| Titre | Slogan |")
        lines.append("|---|---|")
        for opt in data["title_options"]:
            lines.append(
                "| **{title}** | {tagline} |".format(
                    title=_md_escape_cell(opt.get("title", "")),
                    tagline=_md_escape_cell(opt.get("tagline", "")),
                )
            )
        lines.append("")

    if data.get("weekly_breakdown"):
        lines.append("## Plan semaine par semaine")
        lines.append("")
        lines.append("| Semaine | Titre de la prédication | Passage | Idée maîtresse | Fil conducteur |")
        lines.append("|---|---|---|---|---|")
        for week in data["weekly_breakdown"]:
            lines.append(
                "| {w} | {title} | {passage} | {idea} | {thread} |".format(
                    w=_md_escape_cell(week.get("week", "")),
                    title=_md_escape_cell(week.get("sermon_title", "")),
                    passage=_md_escape_cell(week.get("passage", "")),
                    idea=_md_escape_cell(week.get("big_idea", "")),
                    thread=_md_escape_cell(week.get("connective_thread", "")),
                )
            )
        lines.append("")

    if data.get("series_arc"):
        lines.append("## Arc narratif de la série")
        lines.append("")
        lines.append(_md_paragraphs(data["series_arc"]))
        lines.append("")

    notes = data.get("practical_notes") or {}
    if notes:
        lines.append("## Notes pratiques")
        lines.append("")
        if notes.get("duration_check"):
            lines.append("**Vérification de la durée**")
            lines.append("")
            lines.append(notes["duration_check"])
            lines.append("")
        if notes.get("special_attention"):
            lines.append("**Semaines à traiter avec soin**")
            lines.append("")
            lines.append(notes["special_attention"])
            lines.append("")
        if notes.get("launch_recommendation"):
            lines.append("**Recommandation pour le lancement**")
            lines.append("")
            lines.append(notes["launch_recommendation"])
            lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    return os.path.abspath(output_path)


def generate_pdf(json_path, output_path=None):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not output_path:
        title = data.get("series_title", "serie")
        safe_name = title.replace(" ", "-").replace(":", "-")
        output_path = f"Serie-de-Predications-{safe_name}.pdf"

    doc = create_doc(
        output_path,
        title=f"Série de prédications : {data.get('series_title', '')}",
        author=data.get("pastor_name", ""),
    )
    styles = build_styles()
    story = []

    meta_parts = [p for p in [data.get("date"), data.get("pastor_name"), data.get("church_name")] if p]
    subtitle = data.get("series_title", "")
    if data.get("series_tagline"):
        subtitle += f" : {data['series_tagline']}"
    add_title_banner(story, "SÉRIE DE PRÉDICATIONS", subtitle, meta_parts, styles)

    if data.get("scope_assessment"):
        add_section(story, "Évaluation de la portée", data["scope_assessment"], styles)

    if data.get("title_options"):
        section_header(story, "Propositions de titre", styles)
        headers = ["Titre", "Slogan"]
        rows = [[opt.get("title", ""), opt.get("tagline", "")] for opt in data["title_options"]]
        add_table(story, headers, rows, [2.0, 4.5], styles)

    if data.get("weekly_breakdown"):
        section_header(story, "Plan semaine par semaine", styles)
        headers = ["Semaine", "Titre de la prédication", "Passage", "Idée maîtresse", "Fil conducteur"]
        rows = []
        for week in data["weekly_breakdown"]:
            rows.append([
                str(week.get("week", "")),
                week.get("sermon_title", ""),
                week.get("passage", ""),
                week.get("big_idea", ""),
                week.get("connective_thread", ""),
            ])
        add_table(story, headers, rows, [0.6, 1.4, 1.1, 1.7, 2.2], styles)

    if data.get("series_arc"):
        add_section(story, "Arc narratif de la série", data["series_arc"], styles)

    if data.get("practical_notes"):
        add_practical_notes(story, data["practical_notes"], styles)

    page_footer = make_page_footer("church", language="fr")
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)

    md_path = os.path.splitext(output_path)[0] + ".md"
    md_result = generate_markdown(data, md_path)

    return os.path.abspath(output_path), md_result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate-pdf.py <input.json> [output.pdf]")
        sys.exit(1)
    json_input = sys.argv[1]
    pdf_output = sys.argv[2] if len(sys.argv) > 2 else None
    pdf_path, md_path = generate_pdf(json_input, pdf_output)
    print(f"PDF généré : {pdf_path}")
    print(f"Markdown généré : {md_path}")
