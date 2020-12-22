import os
import discord
from typing import Optional
from discord.ext import commands
import asyncio
import json
import random

os.chdir('.')
token = 'token'

def wrapper(ctx, emoji):
		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) == emoji1
		return check

def get_prefix(client,message):
    with open("prefixe.json", "r") as f:
        prefixe = json.load(f)
    
    return prefixe[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name='des gens combattre 😎'))
    print("Bot connecté")

@bot.command
async def load(ctx,extension):
    bot.load_extension(f'cogs.{extension}')
    
@bot.command
async def unload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')
    
@bot.event
async def on_guild_join(guild):
    with open("prefixe.json", "r") as f:
        prefixe = json.load(f)
    
    prefixe[str(guild.id)] = "!"
    
    with open("prefixe.json", "w") as f:
        json.dump(prefixe,f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixe.json', 'r') as f:
        prefixe = json.load(f)
   	
    prefixe[str(guild.id)] = '!'
    
    with open('prefixe.json', 'w') as f:
        json.dump(prefixe, f, indent=4)
        
@bot.command()
async def prefix(ctx, prefix):
    
    with open("prefixe.json", "r") as f:
        prefixe = json.load(f)
    
    prefixe[str(ctx.guild.id)] = prefix
    await ctx.send("Le préfixe a été changé pour " + prefix)

    with open("prefixe.json", "w") as f:
        json.dump(prefixe,f, indent=4)

@bot.command()                                                                                                          #SAY
async def say(ctx, *, arg):
    """
    Fonction pour faire parler le bot en reproduisant ce qui est tapé précédemment
    :param ctx: le contexte de la commande.
    :param *, arg: Le texte a renvoyé avec espaces.
    """
    await ctx.message.delete()
    await ctx.send(arg)

#COMMANDES DE MODERATIONS #COMMANDES DE MODERATIONS #COMMANDES DE MODERATIONS #COMMANDES DE MODERATIONS #COMMANDES DE MODERATIONS #COMMANDES DE MODERATIONS #COMMANDES DE MODERATIONS

@bot.command()                                                                                                          #KICK
async def kick(ctx, user : discord.User):
    """
    Fonction pour Kick du serveur des utilisateurs 
    :param ctx: Le contexte de la commande.
    :param user: L'utilisateur qui va etre kick.
    """
    if ctx.message.author.guild_permissions.administrator:
        await ctx.guild.kick(user)
        await ctx.send(f"{user} vient d'etre kick !")
    else:
        await ctx.send("Tu n'as pas les droits d'administrateurs !")

@bot.command()                                                                                                          #BAN
async def ban(ctx, user:discord.User):
    """
    Fonction pour bannir du serveur des utilisateurs 
    :param ctx: Le contexte de la commande.
    :param user: L'utilisateur qui va etre ban.
    """
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send(f"{user} vient d'être banni ! Il a surement fait quelque chose de mal c'est triste :pensive:")
    else :
        await ctx.send("Tu n'as pas les droits d'administrateurs !")

@bot.command()
async def unban(ctx, user):
    """
    Fonction pour débannir du serveur des utilisateurs 
    :param ctx: Le contexte de la commande.
    :param user: L'utilisateur qui va etre débanni.
    
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que l'utilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")
    """
@bot.command()
async def mplessansfichesaproposdunsujet(ctx):
	if ctx.author==ctx.guild.owner:
		await ctx.send("Ok c bav tu es le maitre supreme bg :person_bowing: ")

@bot.command()                                                                                                          #CLEAR
async def clear(ctx, nombre : int):
    """
    Fonction pour supprimer les derniers messages d'un channel 
    :param ctx: Le contexte de la commande.
    :param nombre: Le nombre de messages qui vont etre supprimés.
    """
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await message.delete()

#COMMANDES SHOP ET ITEM #COMMANDES SHOP ET ITEM #COMMANDES SHOP ET ITEM #COMMANDES SHOP ET ITEM #COMMANDES SHOP ET ITEM #COMMANDES SHOP ET ITEM #COMMANDES SHOP ET ITEM #COMMANDES SHOP ET ITEM

@bot.command()
async def open_account(ctx):
    """
    Fonction pour créer un compte et l'enregistré dans un json (sauf si déjà fait)
    :param ctx: Le contexte de la commande.
    """
    users = await get_bank_data()
    user = ctx.author
    if str(user.id) in users:
        await ctx.send("Votre compte a déjà été créé !")
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["monnaie"] = 0
        users[str(user.id)]["banque"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    await ctx.send("Bravo votre compte vient d'être enregistré avec succès !")
    return True

@bot.command()
async def opened_account(ctx):
    """
    Fonction presque identique a celle au dessus mais réutilisé pour la verification uniquement
    :param ctx: Le contexte de la commande.
    """
    users = await get_bank_data()
    user = ctx.author
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["monnaie"] = 0
        users[str(user.id)]["banque"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True

@bot.command()
async def money(ctx, Utilisateur: Optional[discord.User]):
    """
    Fonction permettant d'afficher l'argent d'un utilisateur dans son portemonnaie et son compte en banque
    :param ctx: Le contexte de la commande.
    :param Utilisateur: Afficher la money de l'utilisateur qui a été ping.
    """
    users = await get_bank_data()
    
    if Utilisateur is None:
        user = ctx.author
    else:
        user = Utilisateur

    if str(user.id) in users:
    
        porte_monnaie = users[str(user.id)]["monnaie"]
        banque_argent = users[str(user.id)]["banque"]

        em = discord.Embed(title = f"Argent de {user.name}", color = discord.Color.green())
        em.set_thumbnail(url = user.avatar_url)
        em.add_field(name = "Porte Monnaie", value = porte_monnaie)
        em.add_field(name = "Compte en Banque", value = banque_argent)

        await ctx.send(embed = em)
        with open("mainbank.json", "w") as f:
            json.dump(users,f)
        return True
    else:
         pass
    return False

@bot.command()
async def get_bank_data():
    """
    Fonction pour chercher dans les données d'un utilisateur (utilisé pour la verification seulement)
    """
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

@bot.command()
async def add_money(ctx, money : int, utilisateur: discord.User):
    """
    Fonction pour ajouter de l'argent sur ton compte et l'enregistré dans un json
    :param ctx: Le contexte de la commande.
    """
    users = await get_bank_data()
    user = utilisateur
    if str(user.id) in users and ctx.message.author.guild_permissions.administrator:
        if money<0:
            await ctx.send("**Euh... Pourquoi tu utilises la commande ``add`` pour enlever de l'argent ? ... utilise plutot la commande ``!remove_money`` pour ca**")
        elif money==0:
            await ctx.send("**Hmmmmm qu'est ce que je suis censé répondre à ça ... Beh ... ducoup rien ne se passe. Bon j'y vais moi ...**")
        elif user==ctx.author:
            await ctx.send("**Tu serais pas en train d'essayer de toucher à ton compte. Ca m'a tout l'air d'etre de la triche ...**")
        else:
            users[str(user.id)]["monnaie"] = users[str(user.id)]["monnaie"] + money
            with open("mainbank.json", "w") as f:
                json.dump(users,f)
            await ctx.send(f"**Here comes the MONEY !!! Money money money money money\nTu viens de rajouter {money} dans le compte de {user.mention} Félicitation à toi !**")
            return True
    elif ctx.message.author.guild_permissions.administrator==False:
        await ctx.send("Tu n'as pas les droits d'administrateurs pour gérer ça ... dommage.")
    else:
        await ctx.send("Cet utilisateur n'a pas de compte on dirait ... dites à cette personne de taper la commande open_account pour ouvrir un compte.")
        pass
        return False

@bot.command()
async def remove_money(ctx, money : int, utilisateur: discord.User):
    """
    Fonction pour ajouter de l'argent sur ton compte et l'enregistré dans un json
    :param ctx: Le contexte de la commande.
    """
    users = await get_bank_data()
    user = utilisateur
    if str(user.id) in users and ctx.message.author.guild_permissions.administrator:
        if money<0:
            await ctx.send("**Euh... Pourquoi tu utilises la commande remove pour donner de l'argent ? ... utilise plutot la commande ``!add_money`` pour ca**")
        elif user==ctx.author:
            await ctx.send("**Tu serais pas en train d'essayer de toucher à ton compte. Ca m'a tout l'air d'être de la triche ... et quoi me regarde pas comme ça !**")
        elif money==0:
            await ctx.send("**Hmmmmm qu'est ce que je suis censé répondre à ça ... Beh ... ducoup rien ne se passe. Bon j'y vais moi ...**")
        elif money>users[str(user.id)]["monnaie"]:
            await ctx.send("**Tu ne peux pas enlever plus d'argent que ce que cette personne a déjà sinon ça va aller dans les négatifs **")
        else:
            users[str(user.id)]["monnaie"] = users[str(user.id)]["monnaie"] - money
            with open("mainbank.json", "w") as f:
                json.dump(users,f)
            await ctx.send(f"**Tu viens d'enlever {money} du compte de {user.mention}. **")
            return True
    elif ctx.message.author.guild_permissions.administrator==False:
        await ctx.send("Tu n'as pas les droits d'administrateurs pour gérer ça ... dommage.")
    else:
        await ctx.send("Cet utilisateur n'a pas de compte on dirait ... dites à cette personne de taper la commande open_account pour ouvrir un compte.")
        pass
        return False

@bot.command()
async def get_stats():
    """
    Fonction pour chercher dans les données d'un utilisateur (utilisé pour la verification seulement)
    """
    with open("stats.json", "r") as f:
        users = json.load(f)
    return users


#COMMANDES DE FIGHT #COMMANDES DE FIGHT #COMMANDES DE FIGHT #COMMANDES DE FIGHT #COMMANDES DE FIGHT #COMMANDES DE FIGHT #COMMANDES DE FIGHT #COMMANDES DE FIGHT 
@bot.command()                                                                #FIGHT
@commands.cooldown(1, 10, commands.BucketType.user)
async def fight (ctx, adversaire: discord.User):
	"""
	Fonction pour lancer un combat entre deux utilisateurs (commande très complexe)
	:param ctx: Le contexte de la commande.
	:param adversaire: L'utilisateur que vous allez affronter.
	"""
	await ctx.send("**C'est l'heure du combat !!! Choisissez le mode de combat (1, 2 ou 3):**\n\n**:one: Match Amicale :**\nAucun des personnages ne mourront le combat se termine lorsqu'il reste 5% des PV à l'un d'entre eux.\n\n**:two: DEATH MATCH :**\nCombattez pour votre vie JUSQU'A LA MORT !!!!! (Reset du personnage qui mourra lors du combat)\n\n**:three: Role Play :**\nUne option qui n'utilisera aucune fonctionnalité du bot a vous de jouez et de définir le gagnant à la fin du combat (vous êtes seuls juges du combat a vous deux de définir le perdant (soyez Fair Play ;) )")
	user = ctx.author.id
	channel = ctx.message.channel
	# Début de l'aventure et réponse du joueur
	try:
		msg = await bot.wait_for('message', check=lambda message: message.author.id == user and message.channel == channel, timeout=20)
		reponse = msg.content
		if "1" == reponse :
			message = await ctx.send(f"**Le combat opposant {ctx.author.mention} et {adversaire.mention}**")
		elif "2" == reponse :
			await ctx.send(f"**Un grand combat commence aujourd'hui, une ambiance mortelle se crée aux alentours et une brise glaciale se fait sentir, un match à mort est prêt à debuter le lieu s'emplit peu à peu d'une aura meurtrière qui ne cesse de grandir mais qui gagnera ce combat .....**\n\n**Le combat opposera donc {ctx.author.mention} à {adversaire.mention} une page de l'histoire est en train de s'écrire aujourd'hui !**")
		elif "3" == reponse :
			await ctx.send("**Vous avez choisi le mode Role Play alors à vous de jouer maintenant !!!**")
		else:
			await ctx.send("**:x: Réponse incorrect réessaye**")
	except asyncio.TimeoutError:
		await ctx.send("**Tu mets pas mal de temps ..., reviens une fois que tu te seras décidé ^^ !**")
		return False

@bot.command()
async def get_fiche():
    """
    Fonction pour chercher dans les données d'un utilisateur (utilisé pour la verification seulement)
    """
    with open("fiche.json", "r") as f:
        users = json.load(f)
    return users

@bot.command()
async def ping(ctx):
	await ctx.send(f':ping_pong: **Pong : {round(bot.latency * 1000)} ms**')

@bot.command()
async def fiche(ctx):
	user = ctx.author
	channel = ctx.channel
	await ctx.send(f"**Bienvenue dans le créateur de fiche {ctx.author.mention} n'est-ce pas excitant !!!\nC'est ici que tu vas pouvoir donner vie à ton personnage mais réflechis bien car les changements seront définitifs sauf si vous effectuez le reset de votre personnage en reprenant l'aventure de ZERO.\nSi tu es prêt ALLONS-Y !!!**")
	users = await get_fiche()
	await ctx.send("**Pour commencer quel sera le prénom de ton personnage ?**")
	emoji1 = '✅'
	emoji2 = '❌'
	try:
		msg = await bot.wait_for('message', check=lambda message: message.author.id == user and message.channel == channel, timeout=30)
		await ctx.send(msg.content)
		await msg.add_reaction(emoji1)
		await msg.add_reaction(emoji2)
		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=None, check=wrapper(ctx, emoji))
			users[str(user.id)] = {}
			users[str(user.id)]["prenom"] = msg.content
			await ctx.send("Bien maintenant le nom de ton personnage")
		except asyncio.TimeoutError:
			pass
	except asyncio.TimeoutError:
		pass
bot.run(token)
