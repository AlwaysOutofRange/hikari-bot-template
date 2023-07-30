from pathlib import Path
from typing import Any, Self

import hikari
import tanjun


class Client(tanjun.Client):
    __slots__ = tanjun.Client.__slots__ + ("scheduler",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def load_modules(self) -> Self:
        path = Path("./src/modules/")

        for ext in path.glob("**/" + "[!_]*.py"):
            super().load_modules(".".join([*ext.parts[:-1], ext.stem]))

        return self

    @classmethod
    def from_gateway_bot(
        cls,
        bot: hikari.GatewayBotAware,
        /,
        *,
        event_managed: bool = True,
        mention_prefix: bool = False,
        declare_global_commands: int | bool = False,
    ) -> "Client":
        constructor = (
            cls(
                rest=bot.rest,
                cache=bot.cache,
                events=bot.event_manager,
                shards=bot,
                event_managed=event_managed,
                mention_prefix=mention_prefix,
                declare_global_commands=declare_global_commands,
            )
            .set_human_only()
            .set_hikari_trait_injectors(bot)
        )

        return constructor
