from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def generate_shopping_cart_pdf(ingredients):
    pdfmetrics.registerFont(
        TTFont(
            "caviar-dreams",
            "data/TimesNewRoman.ttf",
            "UTF-8"
        )
    )

    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = "attachment; filename='shopping_list.pdf'"
    page = canvas.Canvas(response)
    page.setFont("caviar-dreams", size=16)
    page.drawString(200, 800, "Список ингридиентов")
    page.setFont("caviar-dreams", size=14)
    height = 700
    for i, (name, data) in enumerate(ingredients.items(), 1):
        page.drawString(
            75,
            height,
            f'{i}. {name} - {data["amount"]} {data["measurement_unit"]}',
        )
        height -= 25
    page.showPage()
    page.save()
    return response
