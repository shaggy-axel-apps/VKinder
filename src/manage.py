import sys
from vkinder import management_commands


if __name__ == '__main__':
    command = "start"
    if len(sys.argv) > 1:
        command = sys.argv[1]
    management_commands.run(command)
