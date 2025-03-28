import os
import shutil
import tomllib

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

SCRIPT_DIRECTORY = "../scripts"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with open("commands.toml", "rb") as f:
    topics_and_commands = tomllib.load(f)


try:
    shutil.rmtree(SCRIPT_DIRECTORY)
    os.makedirs(SCRIPT_DIRECTORY)
except Exception as ex:
    print(ex)
    os.exit(-42)
    
for topic, commands in topics_and_commands.items():
    print(topic)
    for name, command in commands.items():
        print("    "+name)
        # print(command[""])
