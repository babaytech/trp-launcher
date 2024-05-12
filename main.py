import psutil
import os
import minecraft_launcher_lib
from src.launcher import Launcher as launcher
import dearpygui.dearpygui as dpg
import configparser
from screeninfo import get_monitors
from loguru import logger

# константы
WIDTH = int(get_monitors()[0].width / 1.5)
HEIGHT = int(get_monitors()[0].height / 1.5)
ram_info = psutil.virtual_memory()
config = configparser.ConfigParser()


@logger.catch()
def run_minecraft():
    installed_versions = os.listdir(
        config.get("default",
                   "directory"
                   )
    )
    print(installed_versions)


def install(sender):
    try:
        dpg.remove_alias("progress")
        dpg.remove_alias("test status")
        dpg.remove_alias("progress window")

    except:
        pass

    version = dpg.get_item_label(sender)
    current_max = 0

    def set_status(status: str):
        dpg.set_value("text status", status)

    def set_progress(progress: int):
        if current_max != 0:
            dpg.set_value("progress", value=float(progress / current_max))
        print(f"{progress}/{current_max}", end="\r")

    def set_max(new_max: int):
        global current_max
        current_max = new_max

    with dpg.window(width=400, tag="progress window"):
        dpg.add_progress_bar(label="install", width=400, tag="progress", default_value=0.0)
        dpg.add_text("", tag="text status")

    callback = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max
    }

    logger.success(f"download version: {version}")
    minecraft_launcher_lib.install.install_minecraft_version(version,
                                                             config.get("default",
                                                                        "directory"),
                                                             callback=callback)


@logger.catch()
def get_vanilla_versions():
    try:
        dpg.remove_alias("vanilla window")
        dpg.remove_alias("index")
        dpg.remove_alias("type")
        dpg.remove_alias("version")
    except:
        pass

    config.read("config.ini")
    get = launcher(directory=config.get("default",
                                        "directory"
                                        ),
                   username=config.get("default",
                                       "username"
                                       )
                   )

    with dpg.window(label="vanilla", tag="vanilla window", width=int(WIDTH / 2), height=int(HEIGHT / 2)):
        with dpg.table():
            dpg.add_table_column(label="id")
            dpg.add_table_column(label="type")
            dpg.add_table_column(label="version")

            for index, version in enumerate(get.get_vannila_versions()):
                with dpg.table_row():
                    dpg.add_text(f"{index}")

                    with dpg.table_cell():
                        dpg.add_text(f"{version["type"]}")

                    with dpg.table_cell():
                        dpg.add_selectable(label=f"{version["id"]}", callback=install, tag=str(index))


@logger.catch()
def save_settings():
    if dpg.get_value("username") != config.get("default", "username"):
        config.set("default", "username", dpg.get_value("username"))

    if dpg.get_value("directory") != config.get("default", "directory"):
        config.set("default", "directory", dpg.get_value("directory"))

    if str(dpg.get_value("ram slider")) != config.get("default", "ram"):
        config.set("default", "ram", str(dpg.get_value("ram slider")))

    with open("config.ini", "w") as conf:
        config.write(conf)


@logger.catch()
def settings():
    try:
        dpg.remove_alias("settings window")
        dpg.remove_alias("username")
        dpg.remove_alias("directory")
        dpg.remove_alias("ram slider")
        dpg.remove_alias("save settings")

    except:
        pass

    config.read('config.ini')

    username = config.get("default", "username", )
    directory = config.get("default", "directory")

    with dpg.window(label="settings", tag="settings window", width=int(WIDTH / 2), height=int(HEIGHT / 5)):
        dpg.add_input_text(label="username",
                           default_value=username,
                           tag="username"
                           )
        dpg.add_input_text(label="directory",
                           default_value=directory,
                           tag="directory"
                           )
        dpg.add_slider_int(label="ram usage (MB)",
                           min_value=256,
                           max_value=int(ram_info.total / 1024 / 1024),
                           tag="ram slider",
                           default_value=config.getint("default",
                                                       "ram")
                           )
        dpg.add_button(label="Save",
                       callback=save_settings,
                       tag="save settings"
                       )


if __name__ == "__main__":
    #####################################################
    logger.add("./logs/gui_logic.log", rotation="500 MB")
    #####################################################

    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=WIDTH, height=HEIGHT)

    with dpg.window(tag="primary"):
        with dpg.menu_bar():
            dpg.add_menu_item(label="vanilla", callback=get_vanilla_versions)
            dpg.add_menu_item(label="forge")
            dpg.add_menu_item(label="fabric")
            dpg.add_menu_item(label="settings", callback=settings)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary", True)
    dpg.start_dearpygui()
    while dpg.is_dearpygui_running():
        pass

    dpg.destroy_context()
