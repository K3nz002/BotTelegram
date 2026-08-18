import httpx

async def get_usd_rate() -> str:
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json().get("USDBRL", {})
                if data and "bid" in data:
                    bid = float(data["bid"])
                    pct_change = data.get("pctChange", "0")
                    return f"💵 <b>Dólar (USD/BRL)</b>: R$ {bid:.2f} ({pct_change}%)"
                else:
                    raise ValueError("Dados da cotação inválidos")
            else:
                raise ValueError(f"Erro ao buscar cotação: {response.status_code}")
    except Exception as e:
        return f"💵 <b>Dólar (USD/BRL)</b>: Não disponível"