from src.utils.general_utils import open_yaml_file, save_yaml_file


def check_ultralytics_settings(address):
    """
    Use it to check if original settings.yaml file has datasets_dir pointing to the current
    dir or not.

    :Usage:
    ultralytics_settings_address = "/root/.config/Ultralytics/settings.yaml"
    result = check_ultralytics_settings(ultralytics_settings_address)

    :param address:
    :return:
    """
    if address == "":
        print("No address for Ultralytics Settings given...")
        return False
    # checking if config is problematic or not
    settings = open_yaml_file(address)
    if settings['datasets_dir'] != ".":
        settings['datasets_dir'] = "."
        save_yaml_file(settings, address)
        print('Changed Datasets Directory in Ultralytics Settings. Rerun please...')
        return False
    else:
        return True
