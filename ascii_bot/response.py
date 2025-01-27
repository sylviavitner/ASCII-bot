from random import choice
from discord import Message
import os.path
import getpass

# Attendance tracking state
attendance_tracking = {
    "is_counting": False,  # Whether attendance tracking is active
    "attendees": set()  # A set to store  usernames
}

# Function to report the attendance after a set of attendess has been collected
async def report_attendance(attendees, message: Message):
    # Use getpass to get the username of the device
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
        for attendee in attendees:
            file.write(attendee + "\n")

    await message.channel.send(f"Attendance report saved successfully.")

# Respond to user messages about attendance
async def get_response(user_input: str, message: Message) -> str:
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
            username = str(message.author)
            if username not in attendance_tracking["attendees"]:
                attendance_tracking["attendees"].add(username)
                return f"{username} has been marked present! Total: {len(attendance_tracking['attendees'])}"
            else:
                return "You've already been marked present!"
        return "Attendance counting is not active. Use 'count attendance' to start."

    # Stop counting and report attendance
    elif lowered == "save attendance":
        if not attendance_tracking["is_counting"]:
            return "Attendance counting is not active."
        attendance_tracking["is_counting"] = False
        attendees_list = "\n".join(attendance_tracking["attendees"])
        await report_attendance(attendance_tracking["attendees"], message) # make the report

        return f"Total attendees: {len(attendance_tracking['attendees'])}"

    # Return nothing for unrelated responses
    else:
        return None