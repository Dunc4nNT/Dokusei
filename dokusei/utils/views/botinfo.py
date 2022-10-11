from __future__ import annotations

import os
import platform
import shutil
import sys
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import asyncpg
import discord
import psutil
from discord import app_commands

from dokusei.utils import format_timedelta
from dokusei.utils.views.base import BaseView

if TYPE_CHECKING:
    from dokusei import DokuseiBot


class BotInfoView(BaseView):
    def __init__(
        self,
        author: discord.User | discord.Member,
        client: DokuseiBot,
        *,
        timeout: int = 300,
    ):
        super().__init__(author=author, timeout=timeout)

        self.add_item(BotInfoSelect(client))
        self.add_item(
            discord.ui.Button(
                label="Invite",
                url=f"https://discord.com/oauth2/authorize?client_id={client.user.id}&scope=bot&permissions=8",
                style=discord.ButtonStyle.link,
            )
        )
        self.add_item(
            discord.ui.Button(
                label="Website",
                url=client.config["LINKS"]["WEBSITE"],
                style=discord.ButtonStyle.link,
            )
        )


class BotInfoSelect(discord.ui.Select):
    def __init__(self, client: DokuseiBot):
        self.client: DokuseiBot = client
        options = [
            discord.SelectOption(
                label="Client Information",
                emoji="🤖",
                description="Information about the bot.",
                value="0",
            ),
            discord.SelectOption(
                label="System Information",
                emoji="🖥️",
                description="Information about the system the bot is running on.",
                value="1",
            ),
        ]
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
            placeholder="Select other information",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        match self.values[0]:
            case "0":
                embed = await client_info_embed(self.client)
                await interaction.response.edit_message(embed=embed)
            case "1":
                embed = await system_info_embed(self.client)
                await interaction.response.edit_message(embed=embed)
            case _:
                pass


async def client_info_embed(client: DokuseiBot) -> discord.Embed:
    embed = discord.Embed(
        title="Client Information",
        description=f"[Documentation]({client.config['LINKS']['DOCS']}) • "
        f"[Dashboard]({client.config['LINKS']['DASHBOARD']}) • "
        f"[Support]({client.config['LINKS']['SUPPORT']}) • "
        f"[Source Code]({client.config['LINKS']['REPO']})",
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )

    uptime = discord.utils.utcnow() - client.start_time
    td = format_timedelta(uptime)
    process = psutil.Process(os.getpid())
    memory = round(process.memory_full_info().rss / 2**20, 1)

    embed.add_field(
        name="Information",
        value=f"```yml\n"
        f"Uptime: {td}\n"
        f"Latency: {round(client.latency * 1000)}ms\n"
        f"RAM in use: {memory} MiB```",
        inline=False,
    )

    embed.add_field(
        name="Bot Stats",
        value=f"```yml\n"
        f"Guilds: {len(client.guilds)}\n"
        f"Members: {len(list(client.get_all_members()))}\n"
        f"Channels: {len(list(client.get_all_channels()))}```",
        inline=False,
    )

    command_counter = {
        "cogs": len(client.cogs),
        "prefix_commands": len(client.commands),
        "slash_groups": 0,
        "slash_commands": 0,
    }

    slash_commands = client.tree.get_commands()
    for cmd in slash_commands:
        if isinstance(cmd, app_commands.Group):
            command_counter["slash_groups"] += 1
            command_counter["slash_commands"] += len(cmd.commands)
        else:
            command_counter["slash_commands"] += 1

    total_command_count = (
        command_counter["prefix_commands"] + command_counter["slash_commands"]
    )

    embed.add_field(
        name="Commands",
        value=f"```yml\n"
        f"Command Cogs: {command_counter['cogs']}\n"
        f"Prefix Commands: {command_counter['prefix_commands']}\n"
        f"Slash Groups: {command_counter['slash_groups']}\n"
        f"Slash Commands: {command_counter['slash_commands']}\n"
        f"Total Commands: {total_command_count}```",
    )

    embed.add_field(
        name="Code Stats",
        value=f"```yml\n"
        f"Files: {client.counters['code_stats']['files']}\n"
        f"Spaghetti Code: {client.counters['code_stats']['spaghetti']}\n"
        f"Comments: {client.counters['code_stats']['comments']}\n"
        f"Blank: {client.counters['code_stats']['blank']}\n"
        f"Total: {client.counters['code_stats']['spaghetti'] + client.counters['code_stats']['comments'] + client.counters['code_stats']['blank']}```",
    )

    py_version = sys.version_info
    discord_ver_info = discord.version_info

    embed.add_field(
        name="Version Info",
        value=f"```yml\n"
        f"Dokusei: {client.config['DEV']['VERSION']}\n"
        f"Python: {py_version.major}.{py_version.minor}.{py_version.micro}\n"
        f"Discord.py: {discord_ver_info.major}.{discord_ver_info.minor}.{discord_ver_info.micro}\n"
        f"Asyncpg: {asyncpg.__version__}```",
        inline=False,
    )

    embed.set_footer(
        text=f"Created by {client.app_info.owner.name}#{client.app_info.owner.discriminator}",
        icon_url=client.app_info.owner.display_avatar.url,
    )

    return embed


async def system_info_embed(client: DokuseiBot) -> discord.Embed:
    embed = discord.Embed(
        title="System Information",
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )

    uname = platform.uname()
    boot_time = datetime.fromtimestamp(psutil.boot_time(), timezone.utc)
    system_uptime = discord.utils.utcnow() - boot_time
    system_uptime = format_timedelta(system_uptime)

    embed.add_field(
        name="System",
        value=f"```yml\n"
        f"OS: {uname.system}\n"
        f"Machine: {uname.machine}\n"
        f"Uptime: {system_uptime}```",
        inline=False,
    )

    embed.add_field(
        name="CPU",
        value=f"```yml\n"
        f"Name: {platform.processor()}\n"
        f"Physical Cores: {psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}\n"
        f"Usage: {psutil.cpu_percent()}%```",
        inline=False,
    )

    vmem = psutil.virtual_memory()

    embed.add_field(
        name="Memory",
        value=f"```yml\n"
        f"Total Memory: {round(vmem.total / 2 ** 30, 1)} GiB\n"
        f"Used Memory: {round(vmem.used / 2 ** 30, 1)} GiB ({vmem.percent}%)\n"
        f"Free Memory: {round(vmem.free / 2 ** 30, 1)} GiB```",
    )

    disk_io = psutil.disk_io_counters()
    total, used, free = shutil.disk_usage("/")
    total_gib = total / 2**30
    used_gib = used / 2**30

    embed.add_field(
        name="Disk",
        value=f"```yml\n"
        f"Size: {round(total_gib, 1)} GiB\n"
        f"Used: {round(used_gib, 1)} GiB ({round(used_gib / total_gib * 100, 1)}%)\n\n"
        f"Read: {round(disk_io.read_bytes / 2 ** 30, 1)} GiB\n"
        f"Write: {round(disk_io.write_bytes / 2 ** 30, 1)} GiB```",
    )

    net_io = psutil.net_io_counters()

    embed.add_field(
        name="Network",
        value=f"```yml\n"
        f"Bytes Sent: {round(net_io.bytes_sent / 2 ** 30, 1)} GiB\n"
        f"Bytes Received: {round(net_io.bytes_recv / 2 ** 30, 1)} GiB\n"
        f"Packets Sent: {net_io.packets_sent:,}\n"
        f"Packets Received: {net_io.packets_recv:,}```",
        inline=False,
    )

    embed.set_footer(
        text=f"Created by {client.app_info.owner.name}#{client.app_info.owner.discriminator}",
        icon_url=client.app_info.owner.display_avatar.url,
    )

    return embed
