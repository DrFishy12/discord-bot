import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'הבוט מחובר בהצלחה כ-{bot.user}!')
    activity = discord.Game(name="DrFishy Official BOT")
    await bot.change_presence(activity=activity)

@bot.command()
async def hello(ctx):
    await ctx.send(f'שלום {ctx.author.name}! הבוט מוכן לפעולה. 🤖')

# מחלקת הטופס הקופץ המשודרג
class EmbedModal(discord.ui.Modal, title="יצירת הודעת Embed מתקדמת"):
    embed_title = discord.ui.TextInput(
        label="כותרת ההודעה", 
        placeholder="כותרת ראשית...", 
        required=True
    )
    
    embed_description = discord.ui.TextInput(
        label="תוכן ההודעה (תיאור)", 
        placeholder="טקסט ההודעה...", 
        style=discord.TextStyle.paragraph, 
        required=True
    )

    embed_color = discord.ui.TextInput(
        label="צבע (blue, red, green, gold)", 
        placeholder="blue", 
        required=False,
        max_length=10
    )

    embed_url = discord.ui.TextInput(
        label="קישור לכותרת (אופציונלי)", 
        placeholder="https://example.com", 
        required=False
    )

    embed_image = discord.ui.TextInput(
        label="קישור לתמונה (Image URL)", 
        placeholder="https://... (קישור ישיר לתמונה)", 
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        # בחירת צבע מותאמת אישית או ברירת מחדל
        color = discord.Color.blue()
        c_text = self.embed_color.value.strip().lower()
        if c_text == "red":
            color = discord.Color.red()
        elif c_text == "green":
            color = discord.Color.green()
        elif c_text == "gold" or c_text == "yellow":
            color = discord.Color.gold()
        elif c_text == "purple":
            color = discord.Color.purple()

        # יצירת ה-Embed עם כל ההגדרות
        embed_msg = discord.Embed(
            title=self.embed_title.value,
            description=self.embed_description.value,
            color=color
        )

        # הוספת קישור לכותרת אם המשתמש הזין
        if self.embed_url.value.strip():
            embed_msg.url = self.embed_url.value.strip()

        # הוספת תמונה אם המשתמש הזין קישור
        if self.embed_image.value.strip():
            embed_msg.set_image(url=self.embed_image.value.strip())

        embed_msg.set_footer(text=f"All Rights To DrFishy")

        # שליחת ההודעה לערוץ
        await interaction.channel.send(embed=embed_msg)
        await interaction.response.send_message("הודעת ה-Embed נוצרה ונשלחה בהצלחה! 🚀", ephemeral=True)

# מחלקת הכפתור שפותח את הטופס
class EmbedButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="צור הודעת Embed מתקדמת 📝", style=discord.ButtonStyle.green)
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = EmbedModal()
        await interaction.response.send_modal(modal)

# פקודה ששולחת את ההודעה עם הכפתור
@bot.command()
async def embed(ctx):
    view = EmbedButtonView()
    await ctx.send("לחץ להמשך", view=view)
    try:
        await ctx.message.delete()
    except:
        pass

# החלף כאן את הטוקן שלך
bot.run('YOUR_BOT_TOKEN_HERE')