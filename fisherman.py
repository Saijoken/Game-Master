import discord
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown
from discord.ext import commands
from math import ceil

import asyncio
import random
import time
import datetime

bot = commands.Bot(command_prefix = "!") 
bot.remove_command('help')
token = "NzQ5NzE1NDU3MzI1NTMxMjE4.X0wA7g.b9RbcEw2ETwGJdk3UftJ07GDP9A"

@bot.event
async def on_ready():
    print("Bot connecté")

@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def fish(ctx):
    poisson = random.randint(1, 81)
    user = ctx.author.mention
    if poisson <= 12 :
        await ctx.send(user + "\nC'est vraiment pas ton jour de chance gamin ! Ce poisson est **MINUSCULE**, même si c'est tout à fait normal , vu que le lac en est rempli mais avec un peu de chance on peut trouver des pépites !")
    elif poisson >= 13 and poisson <= 23:
        await ctx.send(user + "\nHé mais attend ce poisson est **TOUT PETIT** tu devrais revoir tes critères à la hausse gamin sinon tu risque pas de faire du bénéfice avec ce que t'as.")
    elif poisson >= 24 and poisson <= 33:
        await ctx.send(user + "\nFais moi voir ce que tu as là ! Hmmmm un **PETIT POISSON** Tu peux etre sur que c'est pas le genre de poissons qui va remplir ton ventre.")
    elif poisson >= 34 and poisson <= 42:
        await ctx.send(user + "\nTu viens d'attraper un **POISSON MOYEN** c'est le poisson le plus répandu ! Et le plus vendu bien qu'il soit plus petit qu'un poisson commun.")
    elif poisson >= 43 and poisson <= 50:
        await ctx.send(user + "\nTu viens de tomber sur un **POISSON COMMUN** rien à dire de spécial là dessus ... Tu feras surement mieux la prochaine fois je te le promets !")
    elif poisson >= 51 and poisson <= 57:
        await ctx.send(user + "\nRien de tel qu'un **BON POISSON** comme celui là après une bonne journée de dur labeur ! Ça c'est sur ! Ça rempli bien l'estomac surtout quand on est affamé !")
    elif poisson >= 58 and poisson <= 63:
        await ctx.send(user + "\nOuah un **POISSON DE QUALITÉ** t'en as de la chance ! On dit que la chair est si tendre qu'elle fond dans la bouche ! Un vrai délice.")
    elif poisson >= 64 and poisson <= 68:
        await ctx.send(user + "\nEt beh c'est une sacré bête ce poisson ! Ce genre de **GROS POISSON** t'en trouves pas à tout les spots ça c'est sur ! C'est un vrai délice s'il est bien préparer !")
    elif poisson >= 69 and poisson <= 72:
        await ctx.send(user + "\nC'est un **TRES GROS POISSON** que tu nous ramènes là ! Tu pourrai nourrir tout un bataillon avec ce poisson ! Ça se revend à bon prix au marché !")
    elif poisson >= 73 and poisson <= 75:
        await ctx.send(user + "\nCE POISSON EST **GIGANTESQUE** Nom de dieu !!! Tu pourras le revendre à très très bon prix au marché ça c'est sur ! On dit aussi qu'il a des propriétés revitalisantes exceptionnels !")
    elif poisson == 76:
        await ctx.send(user + "\n**OUAHHHHHHHH, C'EST IMPOSSIBLE TU VIENS D'ATTRAPER LE POISSON LÉGENDAIRE !!!! MÊME LES MEILLEURS PÊCHEURS DE LA RÉGION N'ONT PAS RÉUSSI !**")
    elif poisson >= 77:
        await ctx.send(user + "\nTu n'as attrapé **AUCUN POISSON** c'est pas si grave attends encore un peu et tu en trouveras d'autres.")
    else:
        await ctx.send("wlh ya un problème dans le code")

@bot.command()
async def list(ctx):
    await ctx.send("**Voici une liste des poissons pêchables classer par niveau de rareté par les Hunters Gourmets:\nPoisson Minuscule :** Valeur 500 Jenys; Stats (+5 sur 1 stat)\n**Tout petit Poisson :** Valeur 1 500 Jenys; Stats (+5 sur 2 stats différentes)\n**Petit Poisson :** Valeur 3 000 Jenys; Stats (+5 sur 3 stats différentes)\n**Poisson Moyen :** Valeur 5 000 Jenys; Stats (+10 sur 1 stat)\n**Poisson Commun :** Valeur 6 500 Jenys; Stats (+10 sur 2 stats différentes)\n**Bon Poisson :** Valeur 8 000 Jenys; Stats (+10 sur 3 stats différentes)\n**Poisson de Qualité :** Valeur 10 000 Jenys; Stats (+20 sur 1 stat)\n**Gros Poisson :** Valeur 12 000 Jenys; Stats (+20 sur 2 stats différentes)\n**Très Gros Poisson :** Valeur 20 000 Jenys; Stats (+20 sur 3 stats différentes)\n**Poisson Gigantesque :** Valeur 50 000 Jenys; Stats (+30 sur toutes les stats)\n**Poisson Légendaire :** Valeur 100 000 Jenys; Stats (+50 sur toutes les stats)")

@bot.command()
async def help(ctx):
    await ctx.send("**Tapes la commande ``!fish`` dans un des ports pour pecher, ou ``!list`` pour voir tout les poissons pêchables**\n**Il y a aussi une commande ``!say`` pour me faire dire quelque chose**")

@bot.command()
async def say(ctx, *, arg):
    user = ctx.author.mention
    await ctx.message.delete()
    await ctx.send(arg +"\n"+ user )

@bot.command()
async def talk(ctx, *, arg):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.message.delete()
        await ctx.send(arg)
    else:
        await ctx.send (":x:")

@fish.error
async def fish_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Te presses pas trop gamin attend encore {0:.0f} minutes et {1:.0f} secondes avant qu\'un autre poisson ne fasse son apparition'.format(((error.retry_after + 30)/60)-1, (error.retry_after % 60) -1)
        await ctx.send(msg)
    else:
        raise error


bot.run(token)