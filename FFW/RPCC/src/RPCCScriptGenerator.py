import os
import sys
import shutil
import tomllib
import jinja2

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

SCRIPT_DIRECTORY = "../scripts"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

host = config["server"]["host"]
port = config["server"]["port"]

with open("commands.toml", "rb") as f:
    topics_and_commands = tomllib.load(f)

with open(r".\templates\linux_script.sh", "rt") as f:
    template_linux = jinja2.Template(f.read())

with open(r".\templates\windows_script.bat", "rt") as f:
    template_windows = jinja2.Template(f.read())


try:
    shutil.rmtree(SCRIPT_DIRECTORY)
    os.makedirs(SCRIPT_DIRECTORY)
except Exception as ex:
    print(ex)
    sys.exit(-42)


for topic, commands in topics_and_commands.items():
    for command in commands:

        # script_name_linux = f"{topic}_{command}.sh"
        # script_name_windows = f"{topic}_{command}.bat"

        with open(f"{SCRIPT_DIRECTORY}/{topic}_{command}.sh","wt") as f:
            f.write(template_linux.render(host=host, port=port, topic=topic, command=command))

        with open(f"{SCRIPT_DIRECTORY}/{topic}_{command}.bat","wt") as f:
            f.write(template_windows.render(host=host, port=port, topic=topic, command=command))

        # template_linux.render(host=host, port=port, topic=topic, command=command)
        # template_windows.render(host=host, port=port, topic=topic, command=command)
        # print(script_name_linux)
        # print(script_name_windows)
