import hikari
import tanjun
import yuyo

from core.client import Client
from core.config import Config


class Bot(hikari.GatewayBot):
    def __init__(self) -> None:
        self.config = Config(TOKEN="no token", DEV_GUILD=None)

        super().__init__(token=self.config.TOKEN, intents=hikari.Intents.ALL)
        
        self.component_client = yuyo.ComponentClient.from_gateway_bot(
            self, event_managed=False
        )

    def create_client(self) -> None:
        dev_guild = self.config.DEV_GUILD if self.config.DEV_GUILD is not None else True
        self.client = Client.from_gateway_bot(self, declare_global_commands=dev_guild)
        (
            self.client.add_client_callback(
                tanjun.ClientCallbackNames.STARTING, self.component_client.open
            ).add_client_callback(
                tanjun.ClientCallbackNames.CLOSING, self.component_client.close
            )
        )
        self.client.set_type_dependency(yuyo.ComponentClient, self.component_client)

        self.client.load_modules()

    def run(self) -> None:
        self.create_client()

        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppedEvent, self.on_stopped)

        super().run()

    async def on_started(self, _: hikari.StartedEvent) -> None:
        ...

    async def on_stopped(self, _: hikari.StoppedEvent) -> None:
        ...
