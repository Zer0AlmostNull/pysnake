import sys
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE


# inspired by https://stackoverflow.com/questions/19479504/how-can-i-open-two-consoles-from-a-single-script
class console(Popen) :
    """
    Allows to create and control multiple subconsoles.
    """
    consoles_count = 0
    COMMAND_PREFIX = '***'
    def __init__(self, color: str = '0c' , title = None):
        console.consoles_count += 1

        title = title if title is not None else "console #" + str(console.consoles_count)
        cmd = "import sys, os, locale"
        cmd += "\nos.system(\'color " + color + "\')" if color is not None else ""
        cmd += "\nos.system(\"title " + title + "\")"

        # poor man's `cat`
        cmd += f""" \
# print(sys.stdout.encoding, locale.getpreferredencoding())
endcoding = locale.getpreferredencoding()
for line in sys.stdin:
    # detecting if it's command
    if(line[:3]=='{console.COMMAND_PREFIX}'):
        os.system(line[3:])
    else:
        sys.stdout.buffer.write(line.encode(endcoding))
    sys.stdout.flush()
"""

        cmd = sys.executable, "-c", cmd
        # print(cmd, end="", flush=True)
        super().__init__(cmd, stdin=PIPE, bufsize=1, universal_newlines=True, creationflags=CREATE_NEW_CONSOLE, encoding='utf-8')

    def write(self, msg, end = '\n'):
        f"""
        Writes text on the console.

        !!IMPORTANT!! message can't start with '{console.COMMAND_PREFIX}'
        """
        self.stdin.write(msg + end)
    
    def call_commad(self, command):
        """
        Calls a console command in subconsole
        """
        self.stdin.write(console.COMMAND_PREFIX + command + '\n')

    def clear(self):
        """
        Clears subconsole.
        """
        self.call_commad('cls')