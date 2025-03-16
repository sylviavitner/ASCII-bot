# ASCII-bot
ASCII bot tracks attendance for club meetings by collecting student IDs. It allows users to mark themselves as present and maintains the data in a MySQL database to avoid repeatedly asking for user information and create a more efficient attendance process. 

---
## 💡 Features
- Type 'start attendance' to begin tracking
- Users type 'here' to mark themselves as present
- If a user is not in the database, the bot will DM them and ask for their App State ID.
- Attendance is saved in a folder called 'Ascii_Attendance' on the desktop, with reports by date
- Attendance reports store App State IDs, the date, and total number of attendees.
  
---
## 📌 Requirements
Before running the bot you will need:
- Python 3.8+
- discord.py installed ('pip install discord.py')
- A Discord bot made through the [Discord Developer Portal](https://discord.com/developers/applications)
- dotenv installed (pip install python-dotenv)
- mysql.connector installed (pip install mysql-connector-python)
- MySQL installed with a database containing the following table:

| Column Name      | Data Type     | Description                                |
|------------------|---------------|--------------------------------------------|
| discord_id       | BIGINT        | Stores Discord IDs (Primary Key)           |
| discord_username | VARCHAR(50)   | Stores Discord usernames                   |
| app_id           | VARCHAR(50)   | Stores App State IDs (Unique)              |


---
## 🛠️ Installation 
- Make sure you have met the requirements
- Clone this repository: ```git clone https://github.com/sylviavitner/ASCII-bot.git```
- cd ASCII-bot
- Copy the bot token from your Discord bot and add it to the environment variables (DISCORD_TOKEN="your-token")
- Add your MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE to the environment variables.
- Run the program (python main.py)

---
## 🎮 Using ASCII Bot
|Command           | What it does                                                      |
|------------------|-------------------------------------------------------------------|
|start attendance  |Starts tracking attendance.                                        |
|here              |Marks a user as present.                                           |
|save attendance   |Stops counting and saves a report to the Ascii_Attendance folder.  |

---
## 📢 Acknowledgments
- The Appalachian Society of Computing, Informatics, and Innovation
- Indently's [Discord Bot Tutorial](https://www.youtube.com/watch?v=UYJDKSah-Ww) to help me get started.

  
