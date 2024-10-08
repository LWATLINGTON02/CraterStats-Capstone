from datetime import datetime
import os


def print_tree(dictionary, indent=0):
    for key, value in dictionary.items():
        print('  ' * indent + str(key))
        if isinstance(value, dict):
            print_tree(value, indent + 1)
        else:
            print('  ' * (indent + 1) + str(value))


def generate_output_file_name():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"plotimage_{timestamp}"
    count = 1
    base_filename = file_name
    while os.path.exists(file_name):
        file_name = f"{base_filename.split('.')[0]}_{count}"
        count += 1

    return file_name

def delete_temp_plots(folder_path, extensions):

    # Loop through all files in the folder
    for file in os.listdir(folder_path):

        # Check if the file has the correct extension
        for extension in extensions:

            if file.endswith(extension) and file != "blank_plot.png":

                # Delete the file
                os.remove(os.path.join(folder_path, file))