"""Build examples/ps42-test.pdf, a test page for /render=ps vs /render=ps42.

PDFium sends only embedded CID-keyed TrueType fonts (Type0 / CIDFontType2) as
Type 42; every other font goes as Type 3 outlines in both modes. fpdf2 embeds
TrueType fonts exactly that way, so every font on this page qualifies.

    pip install fpdf2
    python make-ps42-test.py path/to/dejavu-fonts-ttf/ttf

DejaVu fonts: https://dejavu-fonts.github.io (Bitstream Vera license).
"""
import os, sys
from fpdf import FPDF

TTF = sys.argv[1] if len(sys.argv) > 1 else "."
pdf = FPDF(unit="pt", format="letter")
pdf.set_auto_page_break(False)
pdf.add_font("Sans", "", os.path.join(TTF, "DejaVuSans.ttf"))
pdf.add_font("Serif", "", os.path.join(TTF, "DejaVuSerif.ttf"))
pdf.add_page()
M = 40
W = 612 - 2 * M

pdf.set_font("Sans", size=15)
pdf.set_xy(M, 36)
pdf.cell(W, 20, "ps vs ps42 test: embedded CID TrueType fonts")
pdf.set_font("Sans", size=8)
pdf.set_xy(M, 60)
pdf.multi_cell(W, 10.5,
    "Every font on this page is an embedded CID TrueType font (DejaVu Sans, DejaVu Serif), the only "
    "kind PDFium sends as Type 42 in /render=ps42. In /render=ps the same glyphs go as Type 3 "
    "outlines. The printer rasterizes Type 42 itself with TrueType hinting, so differences show mostly "
    "in the small sizes below (stem weight, spacing, 1 I l |). To confirm which one was sent, print to "
    "a file and search it:  /outfile=C:\\Temp\\t.prn  then  findstr /c:\"FontType 42\" C:\\Temp\\t.prn  "
    "(ps42: found; ps: not found).")

SAMPLE = "Illicit 1Il| 0Oo rn m 8B @&% The quick brown fox jumps over the lazy dog 0123456789"
y = 140
for fam, label in (("Sans", "DejaVu Sans"), ("Serif", "DejaVu Serif")):
    pdf.set_font("Sans", size=9)
    pdf.set_xy(M, y); pdf.cell(W, 12, label + " waterfall"); y += 16
    for size in (4, 5, 6, 7, 8, 9, 10, 11):
        pdf.set_font("Sans", size=6)
        pdf.set_xy(M, y); pdf.cell(24, size + 2, f"{size}pt")
        pdf.set_font(fam, size=size)
        pdf.set_xy(M + 26, y); pdf.cell(W - 26, size + 2, SAMPLE)
        y += size + 5
    y += 8

pdf.set_font("Sans", size=9)
pdf.set_xy(M, y); pdf.cell(W, 12, "Stems and dots at 7pt (compare weight and evenness)"); y += 14
for fam in ("Sans", "Serif"):
    pdf.set_font(fam, size=7)
    for _ in range(2):
        pdf.set_xy(M, y); pdf.cell(W, 9, "I l I l I l | 1.1.1.1 ll.ll.ll IIIII lllll ||||| iiiii ..... ,,,,, :::::"); y += 9
y += 8
pdf.set_font("Serif", size=100)
pdf.set_xy(M, y); pdf.cell(W, 110, "Rg&Qa")
pdf.output(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ps42-test.pdf"))
