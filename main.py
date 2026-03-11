import os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bot is running!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive() 

import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
ID_CATEGORIA = 1477092269973573846
ID_RUOLO_STAFF = 1477089966218543135

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Generale", description="Supporto Generale e domande varie", emoji="<:totem:1477711735501619273>"),
            discord.SelectOption(label="Acquisti", description="Per problemi con lo store o acquisti", emoji="<:gift_pack:1478179128292282419>"),
            discord.SelectOption(label="UnBan / UnMute", description="Per una richiesta Unban o Unmute", emoji="<:orologio:1477710716139212810>"),
            discord.SelectOption(label="Segnala Bug / Player",description="Per segnalare un Bug o un Player", emoji="<:stella:1453848580648337731>"),
            discord.SelectOption(label="Account", description="Reset Password e problemi vari", emoji="<:DiscordLogo:1477712788863320085>"),    

        ]
        super().__init__(placeholder="Seleziona un motivo per aprire il ticket!", options=options, custom_id="t_select")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        cat = guild.get_channel(ID_CATEGORIA)
        nome = f"{self.values[0].lower().replace(' ', '-')}-{interaction.user.name}"
        
        ch = await guild.create_text_channel(name=nome, category=cat)
        
        await ch.set_permissions(guild.default_role, read_messages=False)
        await ch.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await ch.set_permissions(guild.get_role(ID_RUOLO_STAFF), read_messages=True, send_messages=True)
        
        emb = discord.Embed(
            title=f"TICKET: {self.values[0].upper()}", 
            description=f"Benvenuto {interaction.user.mention}, lo staff ti aiuterà a breve.\n\nClicca il tasto rosso per chiudere.", 
            color=0x9B59B6
        )
        
        view_close = discord.ui.View(timeout=None)
        btn_close = discord.ui.Button(label="Chiudi Ticket", style=discord.ButtonStyle.danger, emoji="🔒")
        
        async def close_call(i): await i.channel.delete()
        btn_close.callback = close_call
        view_close.add_item(btn_close)
        
        await ch.send(embed=emb, view=view_close)
        await interaction.response.send_message(f"Ticket aperto: {ch.mention}", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    print(f'>>> TICKET BOT ONLINE: {bot.user}')

@bot.command()
async def setup(ctx):
    embed = discord.Embed(
        title="Supporto", 
        description="Ti serve aiuto? Nessun problema! Usa la reazione qua sotto per creare un nuovo ticket dove il nostro staff ti assisterà.", 
        color=0x9B59B6
    )
    await ctx.send(embed=embed, view=TicketView())
    try: await ctx.message.delete()
    except: pass

bot.run(os.getenv("DISCORD_TOKEN"))

