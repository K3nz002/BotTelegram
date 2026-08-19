import httpx
from datetime import datetime
async def get_usd_rate() -> str:
    url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{}'&$format=json"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}
    try:
        today = datetime.now().strftime("%m-%d-%Y")
        async with httpx.AsyncClient(headers=headers, timeout=10.0,follow_redirects=True) as client:
            response = await client.get(url.format(today))
            if response.status_code == 200:
                values = response.json().get("value", {})
                if values:
                    cotacao = values[-1]["cotacaoCompra"]
                    return f"💵 <b>Dólar (USD/BRL)</b>: R$ {cotacao:.2f}"
                else:
                    raise ValueError("Dados da cotação inválidos")
            else:
                raise ValueError(f"Erro ao buscar cotação: {response.status_code}")
    except Exception as e:
        return f"💵 <b>Dólar (USD/BRL)</b>: Não disponível {e}"
