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


def build_color_class_legend(current_name_map, class_to_color_map):
  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)

  legend_elements = []
  for idx in range(len(current_name_map.keys())):
    class_name = current_name_map[idx]
    class_color = class_to_color_map[idx]
    class_color = [i/255 for i in class_color]
    patch = Patch(facecolor= class_color, label=class_name, edgecolor='black')
    legend_elements.append(patch)
  ax.legend(handles=legend_elements, loc='center')
  return fig, ax
