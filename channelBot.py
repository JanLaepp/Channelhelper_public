import os
import discord
from discord.ext import commands
from discord import app_commands
from BookPicker import BookPicker
from BookBean import BookBean
from Config.python_definitions import ROOT_DIR, GERMAN, ENGLISH

intents = discord.Intents.default()

application_id = "995625838349402202"
bot = commands.Bot(command_prefix="!", intents=intents, application_id=application_id)

yes_synonyms = ["yes", "yas", "ja", "y", "oui", "yaaas", "yaas", "yep", "yarp", "yeppers", "han", "ji", "ys", "yrp", "yis"]

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    try:
        # Syncing slash commands
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
        print(f"Registered Commands: {synced}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


def get_category_id(guild):
    return guild.categories[0]

def tests_passed(message):
    """tests user message if it's within accepted parameters"""
    return True
    
async def say_pin_message(server_id,channel,book_title):
    msg = None
    if server_id in GERMAN:
        msg = await channel.send("**Dies ist der Beginn der Diskussion für " + book_title+".**")
    else:
        msg = await channel.send("**This is the start of discussion for " + book_title+".**")
    await msg.pin()

def parse_out_of_order(oor_string):
    if oor_string.lower() in yes_synonyms:
        return True
    else:
        return False

@bot.tree.command(name="who_is_next", description="Tells you who is next to have their pile picked from and who will do the picking.")
async def whos_next(interaction: discord.Interaction):
    bookpicker = BookPicker()
    next_order = bookpicker.get_next_order(str(interaction.guild.id)).split(";")
    await interaction.response.send_message("The next book will be from the list of " + next_order[0] + ".\n" + next_order[1] + " will pick three \nand " + next_order[2] + " will choose one.")

@bot.tree.command(name="start_book", description="Starts a book that was already set up.")
async def do_start(interaction: discord.Interaction):
    """Starts book from set up"""
    server_id = str(interaction.guild.id)
    next_book = BookBean.get_next_book(server_id)
    BookBean.write_history(server_id)
    
    channel_list = interaction.guild.text_channels
    for channel in channel_list:
        if channel.name == "og-general":
            await channel.send("Starting with " + next_book.title + ". Have fun!")
        elif channel.name == "book-discussion":
            await say_pin_message(server_id,channel,next_book.title)


@bot.tree.command(name="set_up_book", description="Set up a new book to start later.")
@app_commands.describe(book_title="The title of the book", order="the order of book choosing (optional).", out_of_order="If the book has been chosen in an unusual way and shouldn't affect the choosing order of the next book. Defaults to no.")
async def book_setup(interaction: discord.Interaction, book_title: str, order: str = None, out_of_order: str = "False"):
    """Sets up new book with optional order argument."""
    server_id = str(interaction.guild.id)
    out_of_order_bool = parse_out_of_order(out_of_order)
    try:
        next_book = BookBean.book_setup(server_id, book_title, order, out_of_order_bool)
        if not out_of_order_bool:
            await interaction.response.send_message(
                    f"Looks like you'll be reading '{next_book.title}' next.\n"
                    f"It is from the pile of {next_book.listowner}, {next_book.selection} boiled it down to three and {next_book.pick} made the pick."
                )
        else: 
            await interaction.response.send_message(
                    f"Looks like you'll be reading '{next_book.title}' next.\n"
                    f"It seems like you love anarchy, as this book was chosen out of order. Have fun!"
                )
    except ValueError:
        await interaction.response.send_message(
            "One or more of the names you entered are not correct. The only accepted names are Jan, Nina, and Sukriti."
        )

#bot.run("")
