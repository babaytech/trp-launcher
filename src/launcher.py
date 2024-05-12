import minecraft_launcher_lib
import uuid
from subprocess import run
from loguru import logger


class Launcher:
    @logger.catch
    def __init__(self, directory, username):
        logger.add("./logs/launcher_logic.log", rotation="500 MB")
        self.options = {
            "username": username,
            "uuid": str(uuid.uuid4()),
            "token": "",
            "customResolution": True,
            "resolutionWidth": "920",
            "resolutionHeight": "540"
        }

        self.data_user = {
            "directory": directory,
            "username": username,
        }

    @logger.catch
    def get_vannila_versions(self):
        return minecraft_launcher_lib.utils.get_available_versions(self.data_user['directory'])

    @logger.catch
    def download(self, version):
        minecraft_launcher_lib.install.install_minecraft_version(version, self.data_user["directory"])

    @logger.catch
    def get_command(self, version: str):
        return minecraft_launcher_lib.command.get_minecraft_command(version, self.data_user['directory'], self.options)


if __name__ == "__main__":
    launch = Launcher(directory="./minecraft/minecraft",
                      username="Caretaker",
                      version="1.12.2")

    versions: list = []
    for index, version in enumerate(launch.get_vannila_versions()):
        print(f"{index}: {version["id"]}")
        versions.append(version["id"])

    version_id = int(input("введите айди версии:"))
    version = versions[version_id]

    try:
        command = launch.get_command(version=version)
    except:
        launch.download(version=version)
    command = launch.get_command(version=version)
    run(command)
