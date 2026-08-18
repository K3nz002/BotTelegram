import asyncio
import html
import logging
from services.currency import get_usd_rate
from services.world_news import get_latest_world_news
from services.football import get_latest_football_news
from services.hltv import get_latest_hltv_news
from services.seen_news import load_seen, save_seen, filter_new

logger = logging.getLogger(__name__)


async def send_daily_digest(context):
    chat_id = context.job.chat_id
    logger.info("Iniciando envio do digest...")

    # Carrega o histórico de notícias já enviadas (com TTL de 3 dias)
    seen = load_seen()

    # Busca e filtra apenas notícias novas por categoria
    usd_info = await get_usd_rate()
    hltv_news = filter_new(
        await asyncio.to_thread(get_latest_hltv_news, "https://www.hltv.org/rss/news", 5),
        seen, "hltv"
    )
    world_news = filter_new(
        await asyncio.to_thread(get_latest_world_news, "https://admin.cnnbrasil.com.br/feed/", 5),
        seen, "world"
    )
    football_news = filter_new(
        await asyncio.to_thread(get_latest_football_news, "https://www.espn.com.br/rss", 5),
        seen, "football"
    )

    # Se não há nenhuma novidade, não envia nada
    if not any([hltv_news, world_news, football_news]):
        logger.info("Nenhuma novidade encontrada. Digest não enviado.")
        return

    # Monta a mensagem — omite seções sem novidades
    msg = f"📊 <b>Resumo do Dia</b>\n\n{usd_info}\n"

    if hltv_news:
        msg += "\n🎮 <b>HLTV (CS2)</b>:\n"
        for item in hltv_news:
            title = html.escape(item["title"])
            link = item["link"]
            msg += f"• <a href=\"{link}\">{title}</a>\n"

    if world_news:
        msg += "\n🌍 <b>Mundo</b>:\n"
        for item in world_news:
            title = html.escape(item["title"])
            link = item["link"]
            msg += f"• <a href=\"{link}\">{title}</a>\n"

    if football_news:
        msg += "\n⚽ <b>Futebol</b>:\n"
        for item in football_news:
            title = html.escape(item["title"])
            link = item["link"]
            msg += f"• <a href=\"{link}\">{title}</a>\n"

    await context.bot.send_message(
        chat_id=chat_id,
        text=msg,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    # Persiste o estado apenas após o envio bem-sucedido
    save_seen(seen)
    logger.info(
        "Digest enviado. Novas notícias: hltv=%d, world=%d, football=%d",
        len(hltv_news), len(world_news), len(football_news),
    )
