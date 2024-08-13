from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

def generate_quotation():
    pdf = MarkdownPdf(toc_level=2)

    text = """
# 御見積書\n\n

|TableHeader1|TableHeader2|
|--|--|
|Text1|Text2|
|ListCell|<ul><li>FirstBullet</li><li>SecondBullet</li></ul>|
"""

    pdf.meta["title"] = "Quotation"
    pdf.meta["author"] = "Ai keiry"

    pdf.add_section(
        Section(text),
        user_css="h1 {text-align:center;}"
    )

    pdf.save("quotation.pdf")
