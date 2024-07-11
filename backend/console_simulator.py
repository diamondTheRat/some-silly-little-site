import os
import subprocess
from data_types import *
import glob


ERROR = 0
OK = 1
USER = 2

class Console:
    def __init__(self):
        self.current_directory = os.path.expanduser("~")
        self.things = []

    async def run(self, command):
        self.things.append([USER, self.current_directory, command])
        if command in ["cls", "clear"]:
            self.things = []
            return
        if command.startswith("cd ") or command.startswith("ls"):
            # directory = os.path.join(self.current_directory, command[:3])
            # if os.path.isdir(directory):
            #     self.current_directory = directory
            #     self.things.append([OK, f"Changed directory to {self.current_directory}"])
            # else:
            #     self.things.append([ERROR, f'Directory not found: "{command[3:]}"'])
            cwd = os.getcwd()
            try:
                path = command[3:].replace("~", os.path.expanduser("~"))
                
                os.chdir(glob.glob(os.path.join(self.current_directory, path))[0])
                self.current_directory = os.getcwd()
            except Exception:
                self.things.append([ERROR, f'Directory not found: {command[3:]}'])
            os.chdir(cwd)
        else:
            self.process = subprocess.Popen(command, shell=True, cwd=self.current_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = self.process.communicate(timeout=5)
            self.things.append([OK, out])
            if err:
                self.things.append([ERROR, err])

    async def get_output(self):
        return consoleOutput(output=self.things, cwd=self.current_directory)

console = Console()