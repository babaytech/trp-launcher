import psutil
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
def install(version):
    print(version)


@logger.catch()
def get_vannila_versions():
    try:
        dpg.remove_alias("vanilla window")
    except:
        pass

    config.read("config.ini")
    version = None
    get = launcher(directory=config.get("default",
                                        "directory"
                                        ),
                   username=config.get("default",
                                       "username"
                                       ),
                   version=version
                   )

    with dpg.window(label="vanilla", tag="vanilla window") as window:
        with dpg.table():
            dpg.add_table_column(label="id")
            dpg.add_table_column(label="version")

            for index, version in enumerate(get.get_vannila_versions()):
                with dpg.table_row():
                    dpg.add_text(index)
                    with dpg.table_cell():
                        dpg.add_button(label=f"{version["id"]}", user_data=f"{version["id"]}", callback=install)


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

    with dpg.window(label="settings", tag="settings window", width=int(WIDTH / 2), height=int(HEIGHT / 5)) as window:
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
                           tag="ram slider"
                           )
        dpg.add_button(label="Save",
                       callback=save_settings,
                       tag="save settings"
                       )


if __name__ == "__main__":
    logger.add("./logs/gui_logic.log", rotation="500 MB")

    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=WIDTH, height=HEIGHT)

    with dpg.window(tag="primary"):
        with dpg.menu_bar():
            dpg.add_menu_item(label="vannila", callback=get_vannila_versions)
            dpg.add_menu_item(label="forge")
            dpg.add_menu_item(label="fabrick")
            dpg.add_menu_item(label="settings", callback=settings)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary", True)
    dpg.start_dearpygui()
    while dpg.is_dearpygui_running():
        pass

    dpg.destroy_context()
