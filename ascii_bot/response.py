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

# TODO: Change reporting attendance so it creates a folder named "ascii_attendance" if there isn't one
# Each time attendance is saved, a new file is created and stored in this folder named Attendance [Day's Date]
# Attendees should still be written to the file from the set of that day's attendance. Their appstate id should be on the file.
async def report_attendance(attendees, message: discord.Message, db: Database):
    # Use getpass to get the device user
    user = getpass.getuser()
    file_path = f'C:/Users/{user}/Desktop/attendance.txt'

    # Make sure the path exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        print("Directory not found.")
        return

    # Check if the file exists, if not create one
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("")

    # Check if the file is empty or not
    add_newline = False
    with open(file_path, "r") as file:
        if file.read().strip() != "":
            add_newline = True

    # Add newline if necessary and add attendees to report
    with open(file_path, "a") as file:
        if add_newline:
            file.write("\n")

        # Get the current date and time and format it
        now = datetime.datetime.now()
        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
        file.write(f"Attendance recorded at {date_time}\n")

        for app_id in attendees:
            file.write(f"{app_id}\n")

    await message.channel.send(f"Attendance report saved successfully.")

# Respond to user messages about attendance
async def get_response(user_input: str, message: discord.Message, db: Database) -> str:
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
    # TODO: Need to implement checking the database for the discord id (primary key)
    # If it is not found, the bot needs to DM the user and say: "Hi, please enter your appstate id (the first part of your email before the @)"
    # In case of a typo, the bot should say the id back, and have the user type Y to confirm
    # Then, the appstate id should be inserted into the database so the bot never has to ask again
    # Add their appstate id to the set of ids to report
    # If it is found, the appstate id of the discord user is added to a set of ids in the report
    elif lowered == "here":
        if attendance_tracking["is_counting"]:
            discord_id = str(message.author.id)
            user = message.author
            app_id = db.get_app_id(discord_id)
            # Add the user if the id exists in the db
            if app_id:
                attendance_tracking["attendees"].add(app_id)
                return f"{user.name} has been marked present! Total: {len(attendance_tracking['attendees'])}"
            # Get user information and store it
            else:
                print("User not in database. Sending DM...")  # test print statement.
                return await get_app_id_from_dm(message, db)
        return "Attendance counting is not active. Use 'start attendance' to start."

    elif lowered == "save attendance":
        # ... (save attendance command - pass db to report_attendance)
        await report_attendance(attendance_tracking["attendees"], message, db)
        return f"Total attendees: {len(attendance_tracking['attendees'])}"

    # Stop counting and report attendance
    elif lowered == "save attendance":
        if not attendance_tracking["is_counting"]:
            return "Attendance counting is not active."
        attendance_tracking["is_counting"] = False
        attendees_list = "\n".join(attendance_tracking["attendees"])
        await report_attendance(attendance_tracking["attendees"], message, db)

        return f"Total attendees: {len(attendance_tracking['attendees'])}"

    # Return nothing for unrelated responses
    else:
        return None

# Get the app id from user DMs and store it in the db
async def get_app_id_from_dm(message: discord.Message, db: Database):
    print("get_app_id_from_dm called.")

    try:
        if not message.author.dm_channel:
            await message.author.create_dm()

        print(f"message.author.dm_channel: {message.author.dm_channel}")

        await message.author.dm_channel.send("Please enter your appstate id.")

        def check(m):
            return m.author == message.author and m.channel == message.author.dm_channel
        
        app_id_message = await message.guild.get_member(message.author.id).guild.client.wait_for('message', check=check, timeout=30.0) # Corrected line here.
        app_id = app_id_message.content

        await message.author.dm_channel.send(f"Is this your app ID? {app_id} (Type 'Y' to confirm, anything else to cancel)")
        confirmation = await message.guild.get_member(message.author.id).guild.client.wait_for('message', check=check, timeout=30.0) # Corrected line here.

        if confirmation.content.upper() == 'Y':
            if db.insert_data(str(message.author.id), message.author.name, app_id):
                await message.author.dm_channel.send("Thank you! Your app ID has been recorded.")
                return app_id
            else:
                await message.author.dm_channel.send("There was an error saving your app ID. Please try again.")
                return None
        else:
            await message.author.dm_channel.send("App ID entry cancelled.")
            return None

    except TimeoutError:
        await message.author.dm_channel.send("You took too long to respond.")
        return None