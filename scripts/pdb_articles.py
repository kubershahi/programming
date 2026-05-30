"""
PDB Article Merger with Outline Sidebar
----------------------------------------
Merges 00_index.pdf + 01_article.pdf ... 30_article.pdf into a single PDF.
Inserts a title separator page before each article and adds a clickable
document outline (bookmark sidebar) for navigation.

Usage:
    python merge_with_outline.py

Edit the two paths at the top before running.

Requirements:
    pip install pypdf reportlab
"""

import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas as rl_canvas

# ── CONFIGURE THESE TWO PATHS ─────────────────────────────────────────────────

ARTICLES_FOLDER = Path("./articles/")  # folder with 00_index.pdf + 01_article.pdf etc.
OUTPUT_FILE     = Path("./pdb_articles.pdf")  # where the merged PDF will be saved

# ── Article titles ────────────────────────────────────────────────────────────

ARTICLE_TITLES = [
    "AP: This hard-line Iranian general is a major player in talks with U.S. over war",
    "Al Jazeera: Pakistan's mediation faces limits as Iran-US tensions deepen",
    "CNN: Iran rebuilding military industrial base faster than expected",
    "NBC News: Iran says no deal 'imminent' despite progress in talks with U.S.",
    "Reuters: No full Hormuz flows until first half of 2027, UAE's oil giant says",
    "The Times of Israel: US said to fire more interceptors to protect Israel in latest Iran war",
    "BBC: Netanyahu says Israel will intensify strikes against Hezbollah",
    "AP: Russia unleashes another aerial barrage on Ukraine",
    "Reuters: Russians covertly trained by China return to fight in Ukraine",
    'AP: Germany urges the EU to offer Ukraine "associate membership"',
    "The Defense Post: Many NATO countries not spending enough to support Ukraine, says Rutte",
    "Chosun Biz: Europe weighs envoy to engage Putin as Draghi, Merkel top candidate list",
    "AP: China conducts combat patrols in South China Sea",
    "AP: U.S. to deploy more missile launchers to Philippines",
    "CNBC: Taiwan and China coast guards in standoff at top of South China Sea",
    "Reuters: North Korea fired projectiles, including short-range ballistic missile",
    "The Guardian: Cartel corruption claims push US-Mexico relations to breaking point",
    "AP: U.S. sanctions hit alleged Sinaloa cartel fentanyl network",
    "Al Jazeera: Cuba says it has 'legitimate' right to defend itself amid US threats",
    "U.N. OHCHR: Gangs expand reach in Haiti amid persistent deadly violence",
    "Al Jazeera: Haiti's PM casts doubt on presidential vote by August as gang clashes grow",
    "Al Jazeera: Can Venezuelan oil save India amid the Hormuz energy crisis?",
    "AP: Drones are making Sudan's war even deadlier for civilians",
    "CNN: Rebels jeered Putin's troops out of a key African town",
    "Al Jazeera: Nigeria says joint US strikes kill 175 ISIL fighters",
    "The Guardian: Infectious diseases such as hantavirus and Ebola becoming more frequent",
    "US News: Polls and Protests Show Americans Are Turning on Data Centers",
    "BBC: Pope Leo says AI must be 'disarmed' in first major teaching",
    "Reuters: China's Huawei reveals chip design breakthrough amid US sanctions",
    "Al Jazeera: Are India and Pakistan quietly preparing to restart dialogue?",
]

# ── Title page generator ──────────────────────────────────────────────────────

def make_title_page(number: int, title: str) -> PdfReader:
    """Returns a PdfReader of a single-page title separator for an article."""
    buf = io.BytesIO()
    w, h = letter
    c = rl_canvas.Canvas(buf, pagesize=letter)

    # Light grey background bar across the middle
    bar_h = 180
    c.setFillColor(colors.HexColor("#f0f0f0"))
    c.rect(0, h / 2 - bar_h / 2, w, bar_h, fill=1, stroke=0)

    # Article number
    c.setFillColor(colors.HexColor("#888888"))
    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, h / 2 + 55, f"ARTICLE {number:02d}")

    # Divider line
    c.setStrokeColor(colors.HexColor("#cccccc"))
    c.setLineWidth(1)
    c.line(72, h / 2 + 40, w - 72, h / 2 + 40)

    # Title -- wrap long titles across multiple lines
    words = title.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, "Helvetica-Bold", 16) < w - 144:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    c.setFillColor(colors.HexColor("#1a1a2e"))
    c.setFont("Helvetica-Bold", 16)
    total_text_h = len(lines) * 22
    y_start = h / 2 + 18 - (total_text_h - 22) / 2
    for ln in lines:
        c.drawCentredString(w / 2, y_start, ln)
        y_start -= 22

    c.save()
    buf.seek(0)
    return PdfReader(buf)


# ── Merge ─────────────────────────────────────────────────────────────────────

def main():
    writer = PdfWriter()

    # 1. Add index pages
    index_path = ARTICLES_FOLDER / "00_index.pdf"
    assert index_path.exists(), f"Index not found: {index_path}"

    index_reader = PdfReader(str(index_path))
    index_start = len(writer.pages)
    for page in index_reader.pages:
        writer.add_page(page)

    writer.add_outline_item("Article List", index_start)

    # 2. Add each article preceded by its title page
    for i, title in enumerate(ARTICLE_TITLES, start=1):
        article_path = ARTICLES_FOLDER / f"{i:02d}_article.pdf"
        if not article_path.exists():
            print(f"  WARNING: {article_path.name} not found, skipping.")
            continue

        # Insert title separator page
        title_reader = make_title_page(i, title)
        title_page_index = len(writer.pages)
        writer.add_page(title_reader.pages[0])

        # Bookmark points to the title page
        writer.add_outline_item(f"Article {i:02d}: {title}", title_page_index)

        # Add article pages
        article_reader = PdfReader(str(article_path))
        for page in article_reader.pages:
            writer.add_page(page)

        print(f"  Added Article {i:02d} ({len(article_reader.pages)} page(s))")

    # 3. Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "wb") as fh:
        writer.write(fh)

    print(f"\nDone! {len(writer.pages)} total pages.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()