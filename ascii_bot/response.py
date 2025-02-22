import discord
import os.path
import getpass
import datetime
from database import Database

# Attendance tracking state
attendance_tracking = {
    "is_counting": False,  # Whether attendance tracking is active
    "attendees": set()  # A set to store  usernames
}

# Create attendance report and store in the attendance folder
async def report_attendance(attendees, message: discord.Message, db: Database):
    # Use getpass to get the desktop path
    user = getpass.getuser()
    desktop_path = f'C:/Users/{user}/Desktop'

    # Make sure the folder exists. If not, create it
    attendance_folder = os.path.join(desktop_path, "Ascii_Attendance")
    os.makedirs(attendance_folder, exist_ok=True)

    # Create a new file based on the current date
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    file_path = os.path.join(attendance_folder, f"Attendance-{date}.txt")

    # Add attendees app ids to report
    with open(file_path, "a") as file:

        file.write(f"ASCII Attendance for {date}:\n")

        for app_id in attendees:
            file.write(f"{app_id}\n")

    await message.channel.send(f"Attendance report saved successfully.")

# Respond to user messages about attendance
async def get_response(user_input: str, message: discord.Message, db: Database, client: discord.Client) -> str:
    global attendance_tracking

    lowered: str = user_input.lower()

    # Count attendance
    if lowered == "start attendance":
        if attendance_tracking["is_counting"]:
            return "Attendance counting is already active."
        attendance_tracking["is_counting"] = True
        attendance_tracking["attendees"].clear()
        return "Attendance counting started! Type 'here' to mark yourself present."

    # "Here" command
    elif lowered == "here":
        if attendance_tracking["is_counting"]:
            discord_id = str(message.author.id)
            user = message.author
            app_id = db.get_app_id(discord_id)
            # Add the user if the id exists in the db
            if app_id:
                attendance_tracking["attendees"].add(app_id)
                return f"{user.name} has been marked present! Total: {len(attendance_tracking['attendees'])}"
            # Get user information if not in the db
            else:
                print("User not in database. Sending DM...")  # test print statement
                app_id = await get_app_id_from_dm(message, db, client)
                attendance_tracking["attendees"].add(app_id)
                return f"{user.name} has been marked present! Total: {len(attendance_tracking['attendees'])}"
        return None # Changed to say nothing if tracking isn't active

    # Stop counting and report attendance
    elif lowered == "save attendance":
        if not attendance_tracking["is_counting"]:
            return "Attendance counting is not active."
        attendance_tracking["is_counting"] = False
        #attendees_list = "\n".join(attendance_tracking["attendees"]) no longer needed
        await report_attendance(attendance_tracking["attendees"], message, db)

        return f"Total attendees: {len(attendance_tracking['attendees'])}"

    # Return nothing for unrelated responses
    else:
        return None

# Get the App ID from user DMs and store it in the db
async def get_app_id_from_dm(message: discord.Message, db: Database, client: discord.Client):
    try:
        if not message.author.dm_channel:
            await message.author.create_dm()

        # Prompt for app id
        await message.author.dm_channel.send("Please enter your App State id (the part of your email before the @)")

        # Check for the correct user and dm channel
        def check(m):
            return m.author == message.author and isinstance(m.channel, discord.DMChannel)
        
        # Store the next message in the dm channel from the user
        app_id_message = await client.wait_for('message', check=check, timeout=30.0) 
        app_id = app_id_message.content

        # Confirm response
        await message.author.dm_channel.send(f"Is this your app ID? {app_id} (Type 'Y' to confirm, anything else to cancel)")
        confirmation = await client.wait_for('message', check=check, timeout=30.0)

        # Insert into db if accepted
        if confirmation.content.upper() == 'Y':
            if db.insert_data(str(message.author.id), message.author.name, app_id):
                await message.author.dm_channel.send("Thank you! Your app ID has been recorded.")
                return app_id
            else:
                await message.author.dm_channel.send("There was an error saving your app ID. Please try again.")
                return None
        else:
            # Prompt again
            return await get_app_id_from_dm(message, db, client)

    except TimeoutError:
        await message.author.dm_channel.send("You took too long to respond.")
        return None