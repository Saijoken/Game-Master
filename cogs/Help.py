import discord
from typing import Optional
from discord.ext import commands

class Help(commands.Cog):

	def __init__(self, bot):
		self.bot=bot

	@commands.Cog.listener()
	async def on_ready(self):
		pass

	#COMMANDES HELP #COMMANDES HELP #COMMANDES HELP #COMMANDES HELP #COMMANDES HELP #COMMANDES HELP #COMMANDES HELP #COMMANDES HELP #COMMANDES HELP #COMMANDES HELP 
	@commands.command()
	async def help(self, ctx, arg: Optional[str]):
		"""
		Fonction pour aider l'utilisateur a reconnaitre les commandes qu'il pourra utiliser pour bien vivre son RP
		:param ctx: Le contexte de la commande.
		"""
		if arg is None:
			em = discord.Embed(title = "\❓ | Besoin d'aide ?", description = "Pour consulter un type de commande taper !help <Catégorie>.\nVoici les différentes catégories :\n Aventure, Moderation, Economie.", color = discord.Color.from_rgb(232, 18, 36), inline = False)
			em.set_thumbnail(url = "https://cdn.discordapp.com/avatars/740502952405499905/4302949675662d03170dd52ace7ac17c.png")
			em.add_field(name = "**Commande Start**", value = "Commande pour débuter ton aventure si ce n'est pas déjà fait. N'hésite pas à passer voir les salons infos auparavant.", inline = False)
			em.add_field(name = "**Commandes d'Aventure**", value = "Si tu viens de mettre les pieds dans ce monde et tu souhaites te repérer un peu.", inline = False)
			em.add_field(name = "**Commandes de Modérations (Réservé au Staff)**", value = "Commandes utiles aux modérateurs pour modérer les messages et les utilisateurs", inline = False)
			em.add_field(name = "**Commandes d'Economie**", value = "Les commandes servant a utiliser (ou gérer pour le Staff) l'argent et le Shop des utilisateurs.", inline = False)
			em.set_footer(text="En maintenance ne pas utiliser les commandes !!!")

		elif arg == "Moderation" or arg == "Modération" or arg == "moderation" or arg == "modération":
			em = discord.Embed(title = "Commandes de Modérations", description = "Voici les différentes commandes de modérations disponibles sur le bot :", color = discord.Color.from_rgb(232, 18, 36), inline = False)
			em.add_field(name = "**Ban :**", value = "Commande pour bannir définitivement (sauf Unban) un utilisateur du serveur (il ne pourra pas être réinvité au serveur)", inline = False)
			em.add_field(name = "**Kick :**", value = "Commande pour Expulser un utilisateur du serveur (il peut toutefois etre réinvité au serveur contrairement au ban)", inline = False)
			em.add_field(name = "**Clear :**", value = "Commande pour supprimer un certain nombre de derniers messages dans un channel spécifique par exemple: (!clear 10 supprimera les 10 derniers messages du channel)", inline = False)
			em.add_field(name = "**Unban :**", value = "Commande pour supprimer un utilisateur de la liste de ban du serveur pour qu'il puisse être réinvité.", inline = False)
			em.set_footer(text="En maintenance ne pas utiliser les commandes !!!")

		elif arg == "Economy" or arg == "Economie" or arg == "économie" or arg == "economie":
			em = discord.Embed(title = "Commandes d'Economie", description = "Voici les commandes d'Economie elles vous serviront a gérer votre porte monnaie et accéder à la boutique par exemple", color = discord.Color.from_rgb(232, 18, 36), inline = False)
			em.add_field(name = "**Money :**", value = "Commande pour savoir quel somme d'argent vous avez dans votre porte-monnaie et vous permettre de gérer votre budget", inline = False)
			em.add_field(name = "**Shop :**", value = "Commande pour obtenir les informations de la boutique et connaitre les objets que vous pouvez payer en fonction de votre budget", inline = False)
			em.add_field(name = "**Buy (Objet) :**", value = "Commande pour acheter un objet dans le Shop et si vous en avez les moyens.", inline = False)
			em.add_field(name = "**Sell (Objet) (Utilisateur (facultatif)) :**", value = "Commande pour vendre un objet à une boutique ou à un utilisateur en particulier s'il accepte ou non", inline = False)
			em.add_field(name = "**Items :**", value = "Commande pour voir tout les objets que vous avez dans votre inventaire leurs quantités et leurs valeurs", inline = False)
			em.add_field(name = "**Add_Money :**", value = "Commande réservé aux administrateurs permettant de donner une certaine somme d'argent à un joueur", inline = False)
			em.add_field(name = "**Remove_Money :**", value = "Commande réservé aux administrateurs permettant de prendre une certaine somme d'argent à un joueur.", inline = False)
			em.set_footer(text="En maintenance ne pas utiliser les commandes !!!")

		elif arg == "Aventure" or arg == "aventure" or arg == "Adventure" or arg == "adventure":
			em = discord.Embed(title = "Commandes d'Aventure", description = "Tu viens de commencer ton aventure et tu souhaites decouvrir des commandes qui t'aideront a mieux vivre ton RP alors tu es au bon endroit", color = discord.Color.from_rgb(232, 18, 36), inline = False)
			em.add_field(name = "**Start :**", value = "Commande pour débuter ton aventure si ce n'est pas déjà fait. N'hésite pas à passer voir les salons infos auparavant.", inline = False)
			em.add_field(name = "**Fiche :**", value = "Commande pour aider le membre à créer sa fiche avec des instructions a noter etc etc une fois la fiche faite en tapant la commande on pourra voir la fiche du personnage en question", inline = False)
			em.add_field(name = "**Profil (ou p) :**", value = "Commande pour afficher des données de l'utilisateur aussi bien inRP que HRP avec une image (comme Koya ^^)", inline = False)
			em.add_field(name = "**Train :**", value = "Commande pour entrainer son personnage et amélioré ces statistiques de combat", inline = False)
			em.add_field(name = "**Fight @Adversaire :**", value = "Commande pour combattre un adversaire avec système de sélection des attaques et actions avec utlisations d'item (style jeu vidéo)", inline = False)
			em.add_field(name = "**Statistiques (ou stats) :**", value = "Commande pour afficher les statistiques du personnage montrant le nombre d'entrainements restants par jour etc etc...", inline = False)
			em.set_footer(text="En maintenance ne pas utiliser les commandes !!!")
		else:
			await ctx.send("**:x: Cela ne correspond pas a une catégorie disponible.**")
		await ctx.send(embed = em)

def setup(bot):
	bot.remove_command("help")
	bot.add_cog(Help(bot))  