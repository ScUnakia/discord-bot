import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# CHANGE THESE
REVIEW_CHANNEL_ID = 1494333936191541289

ROLES = {
    "Pilot": 1495767688075673662,
    "Co-Pilot": 1495768432740663336,
    "Cabin Crew": 1495768900439113799,
    "Ground Crew": 1495768682813591612
}

class ApplyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Pilot ✈️", style=discord.ButtonStyle.primary)
    async def pilot(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ApplicationModal("Pilot"))

    @discord.ui.button(label="Co-Pilot 👨‍✈️", style=discord.ButtonStyle.primary)
    async def copilot(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ApplicationModal("Co-Pilot"))

    @discord.ui.button(label="Cabin Crew 👨‍💼", style=discord.ButtonStyle.success)
    async def cabin(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ApplicationModal("Cabin Crew"))

    @discord.ui.button(label="Ground Crew 🛠️", style=discord.ButtonStyle.secondary)
    async def ground(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ApplicationModal("Ground Crew"))

class ApplicationModal(discord.ui.Modal, title="Application"):
    def __init__(self, role_name):
        super().__init__()
        self.role_name = role_name

        self.name = discord.ui.TextInput(label="Your Name")
        self.experience = discord.ui.TextInput(label="Experience", style=discord.TextStyle.paragraph)
        self.why = discord.ui.TextInput(label="Why should we choose you?", style=discord.TextStyle.paragraph)

        self.add_item(self.name)
        self.add_item(self.experience)
        self.add_item(self.why)

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(REVIEW_CHANNEL_ID)

        embed = discord.Embed(title=f"{self.role_name} Application ✈️", color=discord.Color.blue())
        embed.add_field(name="User", value=interaction.user.mention, inline=False)
        embed.add_field(name="Name", value=self.name.value, inline=False)
        embed.add_field(name="Experience", value=self.experience.value, inline=False)
        embed.add_field(name="Why", value=self.why.value, inline=False)

        await channel.send(embed=embed, view=ReviewView(interaction.user, self.role_name))
        await interaction.response.send_message("Application submitted!", ephemeral=True)

class ReviewView(discord.ui.View):
    def __init__(self, user, role_name):
        super().__init__(timeout=None)
        self.user = user
        self.role_name = role_name

    @discord.ui.button(label="Accept ✅", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_id = ROLES[self.role_name]
        role = interaction.guild.get_role(role_id)

        await self.user.add_roles(role)
        await interaction.response.send_message(f"Accepted {self.user.mention}", ephemeral=True)

    @discord.ui.button(label="Deny ❌", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Denied {self.user.mention}", ephemeral=True)

@bot.command()
async def apply(ctx):
    embed = discord.Embed(
        title="Applications ✈️",
        description="Choose your role below to apply",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=ApplyView())

@bot.event
async def on_ready():
    bot.add_view(ApplyView())
    print(f"Logged in as {bot.user}")

bot.run("YOUR_BOT_TOKEN")
