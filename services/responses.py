"""Formatação factual de consultas ao estoque e detecção simples de recusas."""
import unicodedata


def normalize(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.casefold()) if unicodedata.category(c) != "Mn")


def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_stock(products, question):
    q = normalize(question)
    if any(token in q for token in ("sem estoque", "indisponiv", "esgotad", "zerado")):
        selected = [p for p in products if p["estoque"] <= 0]
        heading = "Produtos sem estoque"
    elif any(token in q for token in ("disponiv", "em estoque", "comprar", "venda")):
        selected = [p for p in products if p["estoque"] > 0]
        heading = "Produtos disponíveis em estoque"
    else:
        selected = products
        heading = "Produtos cadastrados"
    if not selected:
        return f"{heading}: nenhum produto encontrado."
    lines = [f"**{heading} (fonte: SQLite local):**", ""]
    lines += [f'- **{p["nome"]}** — {format_currency(p["preco"])}; estoque: {p["estoque"]} unidade(s).' for p in selected]
    return "\n".join(lines)


def is_false_refusal(answer):
    q = normalize(answer)
    return any(token in q for token in (
        "nao posso fornecer", "nao posso ajudar", "violacao de privacidade",
        "violacao de seguranca", "nao tenho permissao", "nao e permitido",
        "nao posso divulgar", "nao posso compartilhar", "nao posso revelar",
    ))


def format_weather(data):
    return (
        f'**Clima em {data["cidade"]} ({data["estado"]})**\n\n'
        f'- Temperatura: **{data["temperatura_c"]} °C**\n'
        f'- Umidade relativa: **{data["umidade_percentual"]}%**\n'
        f'- Vento: **{data["vento_kmh"]} km/h**\n'
        f'- Medição: {data["horario_medicao"]}\n\n'
        'Fonte: Open-Meteo.'
    )
