from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

def generate_ghg_report():
    pdf = MarkdownPdf(toc_level=2)
    text = """
# お見積書

|TableHeader1|TableHeader2|
|--|--|
|Text1|Text2|
|ListCell|<ul><li>FirstBullet</li><li>SecondBullet</li></ul>|
"""

    pdf.meta["title"] = "Quotation"
    pdf.meta["author"] = "Ai keiry"

    pdf.add_section(Section(text))
    pdf.save("quotation.pdf")
