import datetime
from app.types.quotation import Quotation
from xhtml2pdf import pisa
import fitz

def currency_format(x):
    return "{:,d}".format(int(x))

def currency_format_html(x):
    return '<div style="text-align: right; margin-right: 5px">%s</div>' % "{:,d}".format(int(x))

def other_quotation_condition_html(conditions=[]):
    condition_list_html = ''
    html = '<p>(その他のお見積り条件)</p>'
    for condition in conditions:
        condition_list_html = condition_list_html + '<li>%s</li>' % condition

    if condition_list_html == '':
        html = ''
    else:
        html = html + '<ul>%s</ul>' % condition_list_html

    return html

def generate_quotation(
    quotation: Quotation = None,
    file_path='/tmp/quotation.pdf'
):
    if quotation is None:
        return

    subtotal_amount = quotation.details["金額"].sum()
    subtotal_tax10 = int(quotation.details.query("税率 == 0.1")["消費税"].sum())
    subtotal_tax08 = int(quotation.details.query("税率 == 0.08")["消費税"].sum())
    subtotal_tax00 = int(quotation.details.query("税率 == 0.0")["消費税"].sum())
    total_tax = subtotal_tax10 + subtotal_tax08 + subtotal_tax00
    total_amount = subtotal_amount + total_tax

    html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: HeiseiMin-W3; line-height: 10px; font-size: 16px;}
        .dataframe { padding-top: 3px; padding-bottom: 1px; font-size: 16px; text-indent: 5px; }
        .quotation-details > td:nth-child(1) { text-align: right; }
        .subtotal { padding-top: 3px; padding-bottom: 1px; font-size: 16px; text-indent: 5px; }
    </style>
</head>
<body>
    <div style="text-align: right; font-size: 14px;">%s</div>
    <h1 style="text-align: center; font-size: 24px; font-weight:bold;">御　見　積　書</h1>
    <h2 style="text-align: left; font-size: 20px;">%s</h2>
    <table>
        <td style="width: 470px;">
            <h3 style="text-align: left; font-size: 16px;"><span style="font-size: 14px;">[件名]</span> %s</h3>
            <div style="text-align: left; font-size: 14px;">次の通り、御見積り申し上げます。</div>
            <div style="text-decoration: underline; padding-top: 10px;">
                <span style="font-size: 20px;">合計金額(税込):</span><span style="font-size: 24px;"> %s 円</span>
            </div>
            <ul style="font-size: 14px; padding-top: 5px;">
                <li>納期: %s </li>
                <li>お支払い条件: %s </li>
                <li>見積有効期限: %s </li>
            </ul>
        </td>
        <td>
            <div style="padding-top: 20px;">%s</div>
            <div>〒%s</div>
            <div>%s</div>
            <div>登録番号: %s</div>
            <div>TEL : %s</div>
            <div>Mail: %s</div>
        </td>
    </table>
    <div style="margin-top: 20px; font-size: 14px;">[内訳]</div>
    %s
    <table>
        <td style="width: 369px; font-size: 14px;">
            %s
        </td>
        <td>
        <table class="subtotal" border="0.5">
        <tr>
            <td style="width: 180px">(合計)</td><td style="width: 100px">%s</td><td style="width: 100px"></td>
        </tr>
        <tr>
            <td style="width: 180px">(消費税 10％)</td><td style="width: 100px">%s</td><td style="width: 100px"></td>
        </tr>
        <tr>
            <td style="width: 180px">(消費税  8％)</td><td style="width: 100px">%s</td><td style="width: 100px"></td>
        </tr>
        <tr>
            <td style="width: 180px">合計金額(税込)</td><td style="width: 100px">%s</td><td style="width: 100px"></td>
        </tr>
        </table>
        </td>
    </table>
    <p>備考</p>
    <div style="font-size: 14px;">
    %s
    </div>
    <div style="font-size: 14px; padding-top: 50px; text-align: right;">
    (以下余白)
    </div>
</body>
</html>
    """ % (
        quotation.issued_at.strftime('%Y年%m月%d日'),
        quotation.customer,
        quotation.title,
        currency_format(total_amount),
        quotation.delivery,
        quotation.payment,
        quotation.expiry,
        quotation.company_name,
        quotation.company_postal_no,
        quotation.company_address,
        quotation.company_tax_no,
        quotation.company_tel,
        quotation.company_mail,
        quotation.details.to_html(
            columns=['項目', '単価', '数量', '単位', '金額', '備考'],
            col_space=[400, 100, 40, 40, 100, 100],
            justify=None,
            formatters={
                '単価': currency_format_html,
                '数量': currency_format_html,
                '金額': currency_format_html,
            },
            classes=['quotation-details'],
            index=False,
            border=0.1,
            escape=False,
        ).replace('min-', ''),
        other_quotation_condition_html(quotation.other_conditions),
        '<div style="text-align: right; margin-right: 5px;">%s</div>' % currency_format(subtotal_amount),
        '<div style="text-align: right; margin-right: 5px;">%s</div>' % currency_format(subtotal_tax10),
        '<div style="text-align: right; margin-right: 5px;">%s</div>' % currency_format(subtotal_tax08),
        '<div style="text-align: right; margin-right: 5px;">%s</div>' % currency_format(total_amount),
        quotation.remark
    )

    temporary_work_file_path = "/tmp/work.pdf"
    with open(temporary_work_file_path, "wb") as pdf_file:
        pisa.CreatePDF(html_content, dest=pdf_file)

    pdf_document = fitz.open(temporary_work_file_path)

    # Specify the image you want to overlay
    image_path = "assets/stamp.png"

    # Select the page number (0-based index)
    page_number = 0  # First page
    page = pdf_document.load_page(page_number)

    # Set image properties: position and size (x0, y0, x1, y1)
    rect = fitz.Rect(525, 185, 575, 235)

    # Insert the image into the selected page at the specified position
    page.insert_image(rect, filename=image_path)

    # Save the updated PDF to a new file
    pdf_document.save(file_path)

    # Close the document
    pdf_document.close()
