from random import choice, randint
from discord import Message

# Attendance tracking state
attendance_tracking = {
    "is_counting": False,  # Whether attendance tracking is active
    "attendees": set()  # A set to store  usernames
}

async def get_response(user_input: str, message: Message) -> str:
    global attendance_tracking

    lowered: str = user_input.lower()

    # General commands
    if lowered == "":
        return "I'm listening..."
    elif "help" in lowered:
        return ("Here is a list of bot functions: \n"
                "Simple greetings (hello, bye, how are you, etc.) \n"
                "roll dice: Roll a six-sided die \n"
                "count attendance: Start counting attendance \n"
                "here: Count yourself present for attendance \n"
                "stop attendance: Stop counting and show the attendance report")
    elif any(greeting in lowered for greeting in ["hello", "hi", "hey"]):
        return "Hello!"
    elif "how are you" in lowered:
        return "I'm good, how about you?"
    elif any(bye in lowered for bye in ["goodbye", "bye"]):
        return "See you later!"
    elif "roll dice" in lowered:
        return f"You rolled: {randint(1, 6)}"

    # Count attendance
    elif lowered == "count attendance":
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

    # Stop counting and print total
    elif lowered == "stop attendance":
        if not attendance_tracking["is_counting"]:
            return "Attendance counting is not active."
        attendance_tracking["is_counting"] = False
        attendees_list = "\n".join(attendance_tracking["attendees"])
        return f"Attendance counting stopped. Total attendees: {len(attendance_tracking['attendees'])}\nAttendees:\n{attendees_list}"

    # Default response for unknown commands
    else:
        return choice(["Could you rephrase that?",
                       "What do you mean?",
                       "Sorry, I do not understand."])
