import tanjun
import hikari

from src.modules import OWN_PERMISSIONS

component = tanjun.Component(name=__name__).load_from_scope()

@component.with_slash_command
@tanjun.with_own_permission_check(
    OWN_PERMISSIONS
)
@tanjun.as_slash_command("ping", "Return bot ping.")
async def ping_command(ctx: tanjun.abc.SlashContext) -> None:
    heartbeat_latency = ctx.shards.heartbeat_latency * 1000 if ctx.shards else float("NaN")

    await ctx.respond("Pinging the API.....")
    embed = hikari.Embed(
        description=(
                "I pinged the API and got these results.\n**Gateway:**"
                f" {heartbeat_latency:.0f}ms"
        ),
        color=0xF1C40F,
    )
    embed.set_author(name=ctx.member.display_name)

    await ctx.edit_last_response("", embed=embed)


loader = component.make_loader()
