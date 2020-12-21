import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import has_permissions
from discord.utils import get
from discord.ext.tasks import loop
from discord import Embed
import sqlite3
import datetime
import asyncio
import time
import sys
import yaml
import random
import string
from math import ceil

class Counter(commands.Cog):
	
    infos = 0

    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await update_counter(channel.guild)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await update_counter(channel.guild)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
            entry = entry 
        if entry.user != self.bot.user:
            await update_counter(after.guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await update_counter(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await update_counter(member.guild)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await update_counter(after.guild)
    connection = sqlite3.connect("bdd.db")
    cursor = connection.cursor()

    @commands.command()
    async def debug(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            await update_counter(ctx.guild)
            await ctx.send(":white_check_mark: Compteurs mis à jour")
        else:
            await ctx.send(":x:")

    @commands.command()
    async def counter(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            # Créer / Supprimer / Liste
            await ctx.send(":one: Veuillez envoyer l'action que vous voulez faire (**créer** un nouveau compteur, **supprimer** un compteur existant ou avoir la **liste** des compteurs existants) :")
            connection = sqlite3.connect("bdd.db")
            cursor = connection.cursor()
            while True:
                user = ctx.author.id
                channel = ctx.message.channel
                try:
                    msg = await self.bot.wait_for('message', check=lambda message: message.author.id == user and message.channel == channel, timeout=240)
                    content = msg.content
                    if "cancel" in content:
                        await ctx.send("Compteur annulée...")
                        return
                    if "cré" in content:
                        action = 0
                        await ctx.send(":one: Très bien, nous allons **créer** un nouveau compteur !")
                        break
                    elif "supp" in content:
                        action = 1
                        await ctx.send(":one: Très bien, nous allons **supprimer** un compteur !")
                        break
                    elif "ist" in content:
                        action = 2
                        await ctx.send(":one: Très bien, je vais envoyer une **liste** des compteurs !")
                        break
                    else:
                        await ctx.send(":x: Action inconnue, réessayez !")
                        continue
                except asyncio.TimeoutError():
                    await ctx.send("Vous avez mis trop de temps à répondre, création annulée...")
                    return
            check = cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{ctx.guild.id}_counters'")
            check = int(check.fetchone()[0])
            if check == 0:
                cursor.execute(f"CREATE TABLE '{ctx.guild.id}_counters' (type INTEGER, channel_name TEXT, channel_id INTEGER, role_id INTEGER)")
                connection.commit()
                if action == 1:
                    await ctx.send(":x: Il n'y a aucun compteur à supprimer")
                    return
            #-----CREER-----#
            if action == 0:
                # Type
                await ctx.send(":two: Veuillez envoyer le type de compteur (le numéro) \n**1**. Compteur de membres \n**2**. Compteur de bots \n**3**. Compteur de membres avec un certain rôle  \n**4**. Compteur de salons")
                while True:
                    user = ctx.author.id
                    channel = ctx.message.channel
                    try:
                        msg = await self.bot.wait_for('message', check=lambda message: message.author.id == user and message.channel == channel, timeout=240)
                        content = msg.content
                        if "cancel" in content:
                            await ctx.send("Compteur annulée...")
                            return
                        if "1" in content: #membres
                            counter_type = 1
                            await ctx.send(":two: Très bien, ce sera un **Compteur de membres**")
                            break
                        elif "2" in content: #bots
                            counter_type = 2
                            await ctx.send(":two: Très bien, ce sera un **Compteur de bots**")
                            break
                        elif "3" in content: #membres (role)
                            counter_type = 3
                            await ctx.send(":two: Très bien, ce sera un **Compteur de membres avec un certain rôle**")
                            break
                        elif "4" in content: #salons
                            counter_type = 4
                            await ctx.send(":two: Très bien, ce sera un **Compteur de salons**")
                            break
                        else:
                            await ctx.send(":x: Type inconnu, réessayez !")
                            continue
                    except asyncio.TimeoutError():
                        await ctx.send("Vous avez mis trop de temps à répondre, création annulée...")
                        return
                # Nom du salon
                await ctx.send(":three: Veuillez envoyer le nom que vous voulez pour le salon (*exemple :* **Bots :**)")
                while True:
                    user = ctx.author.id
                    channel = ctx.message.channel
                    try:
                        msg = await self.bot.wait_for('message', check=lambda message: message.author.id == user and message.channel == channel, timeout=240)
                        content = msg.content
                        if "cancel" in content:
                            await ctx.send("Compteur annulée...")
                            return
                        channel_name = content
                        await ctx.send(f":two: Très bien, ce salon sera nommé **{channel_name}**")
                        break
                    except asyncio.TimeoutError():
                        await ctx.send("Vous avez mis trop de temps à répondre, création annulée...")
                        return
                # Role (si compteur de membres avec un certain rôle)
                if counter_type == 3:
                    await ctx.send(":four: Veuillez mentionner le rôle pour le compteur")
                    while True:
                        user = ctx.author.id
                        channel = ctx.message.channel
                        try:
                            msg = await self.bot.wait_for('message', check=lambda message: message.author.id == user and message.channel == channel, timeout=240)
                            content = msg.content
                            if "cancel" in content:
                                await ctx.send("Compteur annulée...")
                                return
                            try:
                                role_id = content
                                role_id = role_id.replace("<", "")
                                role_id = role_id.replace("@", "")
                                role_id = role_id.replace("&", "")
                                role_id = role_id.replace(">", "")
                                role_id = int(role_id)
                                role = discord.utils.get(ctx.guild.roles, id=role_id)
                                if not role:
                                    await ctx.send(":x: Veuillez mentionner un rôle valide !")
                                    continue
                                else:
                                    await ctx.send(f":four: Très bien, le rôle du compteur sera **{role.name}**")
                                    break
                            except:
                                await ctx.send(":x: Veuillez mentionner un rôle valide !")
                                continue
                        except asyncio.TimeoutError():
                            await ctx.send("Vous avez mis trop de temps à répondre, création annulée...")
                            return
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(connect=False),
                }
                channel = await ctx.guild.create_voice_channel(channel_name, overwrites=overwrites)
                if counter_type == 3:
                    cursor.execute(f'''INSERT INTO '{ctx.guild.id}_counters' VALUES ({counter_type}, "{channel_name}", {channel.id}, {role.id}) ''')
                    connection.commit()
                else:
                    cursor.execute(f'''INSERT INTO '{ctx.guild.id}_counters' (type, channel_name, channel_id) VALUES ({counter_type}, "{channel_name}", {channel.id}) ''')
                    connection.commit()
                await update_counter(ctx.guild)
                await ctx.send(":white_check_mark: Compteur créé (vous pouvez le déplacer dans la catégorie de votre choix !")
                return
            #-----SUPPRIMER-----#
            elif action == 1:
                check = cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{ctx.guild.id}_counters'")
                check = int(check.fetchone()[0])
                if check == 0:
                    await ctx.send(":x: Il n'y a aucun compteur sur ce serveur")
                    return
                counters = cursor.execute(f"SELECT channel_id FROM '{ctx.guild.id}_counters'")
                counters = counters.fetchall()
                counters = [item for t in counters for item in t]
                # ID du compteur
                await ctx.send(":two: Veuillez envoyer l'**ID** du compteur (visible dans la liste)")
                while True:
                    user = ctx.author.id
                    channel = ctx.message.channel
                    try:
                        msg = await self.bot.wait_for('message', check=lambda message: message.author.id == user and message.channel == channel, timeout=240)
                        content = msg.content
                        if "cancel" in content:
                            await ctx.send("Compteur annulée...")
                            return
                        try:
                            counter_id = int(content)
                            channel_id = int(counters[counter_id-1])
                        except:
                            await ctx.send(":x: Veuillez entrer un ID correct")
                            continue
                        await ctx.send(f":two: Suppression du compteur n°**{counter_id}**")
                        break
                    except asyncio.TimeoutError():
                        await ctx.send("Vous avez mis trop de temps à répondre, création annulée...")
                        return
                channel_name = cursor.execute(f"SELECT channel_name FROM '{ctx.guild.id}_counters' WHERE channel_id={channel_id}")
                channel_name = channel_name.fetchone()[0]
                cursor.execute(f"DELETE FROM '{ctx.guild.id}_counters' WHERE channel_id={channel_id}")
                connection.commit()
                channel = discord.utils.get(ctx.guild.voice_channels, id=channel_id)
                await channel.delete()
                await ctx.send(f":white_check_mark: Le salon **{channel_name}** (compteur n°**{counter_id}**) a été supprimé !")
                await update_counter(ctx.guild)
                return
            #-----LISTE-----#
            elif action == 2:
                check = cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{ctx.guild.id}_counters'")
                check = int(check.fetchone()[0])
                if check == 0:
                    await ctx.send(":x: Il n'y a aucun compteur sur ce serveur")
                    return

                counters = cursor.execute(f"SELECT type, channel_name FROM '{ctx.guild.id}_counters'")
                counters = counters.fetchall()
                counters = [item for t in counters for item in t]
                i = 0
                final_send = []
                final_send.append("**Liste des compteurs du serveur :**\n")
                for e in range(ceil(len(counters)/2)):
                    counter_type = int(counters[i])
                    channel_name = counters[i+1]
                    if counter_type == 1:
                        counter_type = "Compteur de membres"
                    elif counter_type == 2:
                        counter_type = "Compteur de bots"
                    elif counter_type == 3:
                        counter_type = "Compteur de membres avec un certain rôle"
                    elif counter_type == 4:
                        counter_type = "Compteur de salons"
                    final_send.append(f'''- ID : **{e+1}** | Type : **{counter_type}** | Nom : **{channel_name}**\n''')
                    i += 2
                final_send = ''.join(final_send)
                await ctx.send(final_send)



    async def update_counter(self, guild: discord.guild.Guild):
        check = cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{guild.id}_counters'")
        check = int(check.fetchone()[0])
        if check != 0:
            counters = cursor.execute(f"SELECT type, channel_name, channel_id FROM '{guild.id}_counters'")
            counters = counters.fetchall()
            counters = [item for t in counters for item in t]
            i = 0
            for e in range(ceil(len(counters)/3)):
                counter_type = int(counters[i])
                if counter_type == 1:
                    members_list = []
                    for member in guild.members:
                        if not member.bot:
                            members_list.append(member)
                    channel = discord.utils.get(guild.voice_channels, id=int(counters[i+2]))
                    name = f"{counters[i+1]} {len(members_list)}"
                    if channel.name != name:
                        await channel.edit(name=name)
                elif counter_type == 2:
                    bot_list = []
                    for member in guild.members:
                        if member.bot:
                            bot_list.append(member)
                    channel = discord.utils.get(guild.voice_channels, id=int(counters[i+2]))
                    name = f"{counters[i+1]} {len(bot_list)}"
                    if channel.name != name:
                        await channel.edit(name=name)
                elif counter_type == 3:
                    role_id = cursor.execute(f"SELECT role_id FROM '{guild.id}_counters' WHERE channel_id={counters[i+2]}")
                    role_id = int(role_id.fetchone()[0])
                    role = discord.utils.get(guild.roles, id=role_id)
                    role_list = []
                    for member in guild.members:
                        if role in member.roles:
                            role_list.append(member)
                    role_list = len(role_list)
                    channel = discord.utils.get(guild.voice_channels, id=int(counters[i+2]))
                    name = f"{counters[i+1]} {role_list}"
                    if channel.name != name:
                        await channel.edit(name=name)
                elif counter_type == 4:
                    channel = discord.utils.get(guild.voice_channels, id=int(counters[i+2]))
                    list_channels = len(guild.channels)
                    name = f"{counters[i+1]} {list_channels}"
                    if channel.name != name:
                        await channel.edit(name=name)
                i += 3

def setup(bot):
	bot.add_cog(Counter(bot))
