from random import choice, randint

def get_response(user_input: str) -> str:

    lowered: str = user_input.lower()

    # Response logic

    # General chatting
    if lowered == "":
        return "I'm listening..."
    elif "help" in lowered:
        return ("Here is a list of bot functions: \n"
                "Simple greetings (hello, bye, how are you, etc.) \n"
                "roll dice: Roll a six sided die \n"
                "here: Count yourself present for attendance")
    elif any(greeting in lowered for greeting in ["hello", "hi", "hey"]):
        return "Hello!"
    elif "how are you" in lowered:
        return "I'm good, how about you?"
    elif any(bye in lowered for bye in ["goodbye", "bye"]):
        return "See you later!"
    elif "roll dice" in lowered:
        return f"You rolled: {randint(1, 6)}"

    # Attendance
    elif lowered == "count attendance":
        get_attendance()
        return "Counting attendance..."
        # todo: implement the rest...
    
    # Other
    else:
        return choice(["Could you rephrase that?",
                       "What do you mean?",
                       "Sorry, I do not understand."])

def get_attendance() -> None:
    counting: bool = True
    count: int = 0