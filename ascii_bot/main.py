from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from response import get_response
from database import Database

# Load token from env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Initialize db connection
try:
    db = Database()
except Exception as e:
    print(f"Database connection failed: {e}")
    exit() 

# Bot setup
intents: Intents = Intents.default()
intents.message_content = True
intents.members = True # enable member intents for discord id
client: Client = Client(intents=intents)

# Send message functionality
async def send_message(message: Message, user_message: str, db: Database) -> None:
    if not user_message:
        print('Message was empty because intents were not enabled properly')
        return

    # For sending private messages (currently unused)
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = await get_response(user_message, message, db, client)
        if response:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Handling startup for the bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# Handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    # return if message is from bot
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message, db)

# Close db connection when done
@client.event
async def on_close():
    print("Closing database connection.")
    del db # calls __del__ method and closes connection

# Main entry point
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()