from .. import loader, utils
import time

@loader.tds
class PingMod(loader.Module):
    """Пинг"""

    strings = {
        "name": "Ping",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    def __init__(self):
        self.config = loader.ModuleConfig(
            "ping_text",
            "<emoji document_id=5942913498349571809>🙂</emoji><b>user:</b> {me}\n"
            "<emoji document_id=5936130851635990622>⚡️</emoji><b>ping:</b> {ping}\n"
            "<emoji document_id=5988023995125993550>🛠</emoji><b>uptime:</b> {uptime}",
        )

    @loader.command()
    async def ping(self, message):
        """пинг"""
        start = time.perf_counter_ns()
        msg = await message.client.send_message(message.peer_id, '⏳')
        ping = round((time.perf_counter_ns() - start) / 10**6, 3)
        await msg.delete()

        info = self.config["ping_text"].format(
            me=self._client.hikka_me.first_name + ' ' + (self._client.hikka_me.last_name or ''),
            ping=ping,
            uptime=utils.formatted_uptime(),
        )

        await utils.answer(message, info)

    @loader.command()
    async def setping(self, message):
        """Установить кастомный текст пинга: .setping <текст>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "текст для пинга")
            return

        self.config["custom_ping_text"] = args
        await utils.answer(message, "текст поставлен</b>")
