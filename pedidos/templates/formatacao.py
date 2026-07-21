from django import template

register = template.Library()

@register.filter
def numero_br(valor, casas=4):
    if valor is None:
        return ""

    try:
        return (
            f"{float(valor):,.{int(casas)}f}"
            .replace(",", "§")
            .replace(".", ",")
            .replace("§", ".")
        )
    except Exception:
        return valor