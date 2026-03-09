from clypi import Command
from typing_extensions import override
# https://danimelchor.github.io/clypi/learn/getting_started/#prompting-for-values
class Cli(Command):
    @override
    async def run(self):
        print(f"Hello, world!")

if __name__ == '__main__':
    cmd = Cli.parse()
    cmd.start()