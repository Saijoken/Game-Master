import discord
import asyncio
from typing import Optional
from discord.ext import commands

class Start(commands.Cog):

	def __init__(self, bot):
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		pass

	def wrapper(self, ctx, emoji):
		def check(self, reaction, user):
			return user == ctx.author and str(reaction.emoji) == emoji
		return check

	@commands.command()
	async def start(self, ctx):
		"""
        Fonction pour lancer la création du personnage.
        :param ctx: le contexte de la commande.
        """
		await ctx.send("**Bonjour et bienvenue dans le monde périlleux de Hunter X Hunter !**\n**J'ai entendu dire que tu voulais devenir un grand aventurier, ou bien que tu voulais être un guerrier exceptionnel... Ou tout simplement explorer le monde avec tes amis ?**\n**Mince j'ai la mémoire trop courte...**\n**En tout cas, j'espère que tu accompliras ton objectif ! Es-tu prêt à commencer ta longue quête mais Attention !, elle sera longue, dangereuse, et sûrement mortel.**\n**Es-tu bien sûr de vouloir la commencer ? (O/N)**")
		while True:
			user = ctx.author.id
			channel = ctx.message.channel
			# Début de l'aventure et réponse du joueur
			try:
				msg = await self.bot.wait_for('message', check=lambda message: message.author.id == user and message.channel == channel, timeout=20)
				reponse = msg.content
				if "Oui" == reponse or "oui" == reponse or "o" == reponse or "O" == reponse:
					message = await ctx.send("**Super, coche la réaction ci-dessous pour que tu puisses créer ton personnage !**\n**Bonne Chance Jeune Héros !!! et n'hésite pas à demander des indications aux staff si tu as besoin d'aide :thumbsup:**")
					reac = True
					break
				elif "Non" == reponse or "non" == reponse or "N" == reponse or "n" == reponse:
					await ctx.send("**C'est dommage, n'hésite pas à revenir le jour où tu seras enfin prêt !**")
					break
				else:
					await ctx.send("**:x:Réponse incorrect réessaye**")
			except asyncio.TimeoutError:
				await ctx.send("**Tu mets pas mal de temps ..., reviens une fois que tu te seras décidé **")
				return
	# Réaction role si le joueur a répondu Oui pour qu'il le ramène a un channel spécifique
		if reac == True: 
			emoji = '📩'
			await message.add_reaction(emoji)
			try:
				reaction, user = await self.bot.wait_for('reaction_add', timeout=25.0, check=wrapper(self, ctx, emoji))
			except asyncio.TimeoutError:
				await ctx.send("**Tu mets pas mal de temps ..., reviens une fois que tu te seras décidé ^^ !**")
			else:
				guild = ctx.message.guild
				channel = await guild.create_text_channel('fiche '+ user.name)
				await channel.set_permissions(ctx.guild.default_role, read_messages=False)
				await channel.set_permissions(ctx.author, read_messages=True)
				fiche = discord.utils.get(ctx.guild.channels, name="Fiche")
				await channel.edit(category=fiche)
				await ctx.send(f"**Rends toi au channel: fiche {user.name} pour débuter ton aventure !!!**")
				message = await channel.send(f"**Ah tu es là {ctx.author.mention}, il ne te reste plus qu'à taper la commande fiche pour créer ton personnage\nClique sur la réac si tu souhaites fermer le ticket.**")
				emoji = '🔒'
				await message.add_reaction(emoji)
				try:
					reaction, user = await self.bot.wait_for('reaction_add', timeout=None, check=wrapper(self, ctx, emoji))
				except asyncio.TimeoutError:
					pass
				else:
					await channel.delete()

def setup(bot):
	bot.add_cog(Start(bot))
