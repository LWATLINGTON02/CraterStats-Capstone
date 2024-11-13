from datetime import datetime
import os
import shutil
import re

PATH = os.path.dirname(os.path.abspath(__file__))


def count_files_in_folder(folder_path):
    try:

        all_files = os.listdir(folder_path)

        files = [
            file
            for file in all_files
            if os.path.isfile(os.path.join(folder_path, file))
        ]

        return len(files)

    except FileNotFoundError:
        return 0


def delete_temp_plots(folder_path, extensions):

    if folder_path.endswith("demo/"):

        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
        except Exception as e:
            print(f"Error occured: {e}")

    else:

        # Loop through all files in the folder
        for file in os.listdir(folder_path):

            # Check if the file has the correct extension
            for extension in extensions:

                if file.endswith(extension) and file != "blank_plot.png":

                    # Delete the file
                    os.remove(os.path.join(folder_path, file))


def generate_output_file_name():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"plotimage_{timestamp}"
    count = 1
    base_filename = file_name
    while os.path.exists(file_name):
        file_name = f"{base_filename.split('.')[0]}_{count}"
        count += 1

    return file_name


def parse_command_string(command_string):

    print(command_string)

    curr_word = ""

    option_list = []

    for index, char in enumerate(command_string):
        curr_word += char
        if char == " " or index == len(command_string) - 1:
            if "source" in curr_word:
                if ".scc" in curr_word or ".diam" in curr_word:
                    option_list.append(curr_word)
                    curr_word = ""
            else:
                option_list.append(curr_word)
                curr_word = ""

    print(option_list)
    option_list.pop(0)

    option_dict = {}
    for index, option in enumerate(option_list):
        if index % 2 == 0:
            if "-p" in option:
                if option in option_dict:
                    option_dict[option].add(option_list[index + 1])
                else:
                    option_dict[option] = {option_list[index + 1]}
            else:
                option_dict[option] = option_list[index + 1]

    return option_dict

def parse_demo_commands(demo_file_path):

    commands_dict = {}
    index = 0

    if not os.path.exists(demo_file_path):
        print("Demos need to be created first")
        return

    with open(PATH + "/assets/config files/demo_commands.txt", "r") as file:
        for line in file:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("-l"):
                continue

            if "pdf" in line:
                commands_dict[f"{index:02}-demo.pdf"] = line
            elif "txt" in line:
                continue
            else:
                commands_dict[f"{index:02}-demo.png"] = line

            index += 1

    return commands_dict


def print_tree(dictionary, indent=0):
    for key, value in dictionary.items():
        print("  " * indent + str(key))
        if isinstance(value, dict):
            print_tree(value, indent + 1)
        else:
            print("  " * (indent + 1) + str(value))
