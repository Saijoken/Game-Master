import discord
from discord.ext import commands

import asyncio

bot = commands.Bot(command_prefix = "!", description = "organise des combats") 
token = str(os.environ.get('BOT_TOKEN'))
bot.remove_command('help')
@bot.event
async def on_ready():
    print("Bot connecté")

@bot.command()
async def prefix(ctx, arg):
    if ctx.message.author.guild_permissions.administrator:
        #bot = commands.Bot(command_prefix = arg)
        await ctx.send("Tu viens de changé le préfixe pour "+ arg)
    else:
        await ctx.send("**:x: Cette commande est réservé aux administrateurs**")

@bot.command()
async def start(ctx):
    await ctx.send("**Bonjour et bienvenue dans le monde périlleux de Hunter X Hunter !**\n**J'ai entendu dire que tu voulais devenir un grand aventurier, ou bien que tu voulais être un guerrier exceptionnel... Ou tout simplement explorer le monde avec tes amis ?**\n**Mince j'ai la mémoire trop courte...**\n**En tout cas, j'espère que tu accompliras ton objectif ! Es-tu prêt à commencer ta longue quête mais Attention !, elle sera longue, dangereuse, et sûrement mortel.**\n**Es-tu bien sûr de vouloir la commencer ? (O/N)**")
    while True:
        user = ctx.author.id
        channel = ctx.message.channel
        # Début de l'aventure et réponse du joueur
        try:
            msg = await bot.wait_for('message', check=lambda message: message.author.id == user and message.channel == channel, timeout=20)
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
        #messag = await ctx.send("**Super, coche la réaction ci-dessous pour que tu puisses créer ton personnage !**\n**Bonne Chance Jeune Héros !!! et n'hésite pas à demander des indications aux staff si tu as besoin d'aide :thumbsup:**")
        emoji = '📩'
        await message.add_reaction(emoji)
        #async def on_reaction_add(reaction, user):
          #  if reaction.emoji.name == 'envelope_with_arrow' and user == ctx.author_id and message.content == "**Super, coche la réaction ci-dessous pour que tu puisses créer ton personnage !**\n**Bonne Chance Jeune Héros !!! et n'hésite pas à demander des indications aux staff si tu as besoin d'aide :thumbsup:**" :
          #      roles = ["746717186285895791"]
           #     role = discord.utils.get(message.server.roles, name=team)
           #     await bot.add_roles(user, role)
    else:
        pass
            
            

                #roles = ["746717186285895791"]
    #role = discord.utils.get(message.server.roles, name=team)
    #try:
        #await client.add_roles(Member.name, role)

@bot.command()                                                                                                          #SAY
async def say(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(arg)

@bot.command()                                                                                                          #KICK
async def kick(ctx, user : discord.User, *reason):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.guild.kick(user, reason = reason)
        await ctx.send(f"{user} vient d'etre kick !")

@bot.command()                                                                                                          #BAN
async def ban(ctx, user:discord.User):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send(f"{user} vient d'être banni ! Il a surement fait quelque chose de mal c'est triste :pensive:")
    else :
        await ctx.send("Tu n'as pas les droits d'administrateurs !")

@bot.command()
async def unban(ctx, user):
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()                                                                                                          #CLEAR
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await message.delete()

@bot.command()                                                                                                          #FIGHT
@commands.cooldown(1, 10, commands.BucketType.user)
async def fight (ctx, adversaire: discord.User):
    await ctx.send(adversaire.mention)

@bot.command()
async def help (ctx):
    await ctx.send("Voici les différentes commandes du bot :\nStart \n Commande pour débuter ton aventure si ce n'est pas déjà fait. N'hésite pas à passer voir les salons infos auparavant.\nHelp \n Commande que tu viens de taper pour obtenir des informations sur tout types de commandes différentes pour ce bot !\nCommandes de modérations de base \n (Reservé au Staff) Les commandes Clear, Kick, Ban et Unban pour modérer le serveur.\nShop \n Commande pour afficher la Boutique et les différents éléments et objets utilisables et achetables inRP.\nProfil (ou p) \n Commande pour afficher différentes données dans une image (ex: Photo de Profil, Pseudo, Nom inRP, Vos Items, Level, Stats ...)")

bot.run(token)