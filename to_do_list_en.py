import os
from colorama import init, Fore, Style
import json
import datetime

## If there are any mistakes in the translation, I apologize.

init(True)

clear = lambda: os.system("cls" if os.name == "nt" else "clear")
clear()
date_today = datetime.datetime.now()
date_today = date_today.strftime("%Y-%m-%d")

class HomePage:
    def __init__(self):
        print(Style.BRIGHT+Fore.WHITE+"="*3+" Welcome To To-Do List "+"="*3)
        print(Style.BRIGHT+Fore.GREEN+"Menu List : "
        "\n1. Create New To-Do List"
        "\n2. View To-Do List"
        "\n3. Delete To-Do List"
        "\n4. Exit")
        return self.input_menu()
    
    def input_menu(self):
        while True:
            choice = str(input("Enter Menu Number : "))
            if self.enter_menu(choice):
                break

    def enter_menu(self, choice):
        match choice:
            case "1":
                self.create_list()
                return True
            case "2":
                self.list_menu()
                return True
            case "3":
                self.delete_list()
                return True
            case "4":
                print(Fore.YELLOW+"=== Exiting ===")
                exit()
            case _:
                print(Fore.LIGHTRED_EX+"** Please Enter a Valid Option **")
                return False

    def read_json(self):
        with open("todo_en.json", "r") as i:
            self.data_json = json.load(i)

    def back_to_menu(self, user_input):
        if str(user_input).lower().strip() == "!m":
            print(Fore.LIGHTWHITE_EX+"** Back To Main Menu **")
            return HomePage()

    def show_lists(self):
        print(Style.BRIGHT+Fore.LIGHTCYAN_EX+"==== List of To-Do Lists ====")
        try:
            self.read_json()
            if not self.data_json:
                print(Fore.LIGHTRED_EX+"** No Lists Available **")
            for number, key in enumerate(self.data_json, start=1):
                if isinstance(self.data_json[key], dict):
                    print(f"{number}. {key}")
        except FileNotFoundError:
            print(Fore.LIGHTRED_EX+"** No Lists Available **")
        print("="*21)

    def create_list(self):
        clear()
        self.show_lists()
        print(Style.BRIGHT+Fore.CYAN+"="*3+" Create To-Do List "+"="*3)
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Hint : Enter the name of the list you want to create")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Hint : Type (!m) to return to the main menu")

        def new_list():
            while True:
                try:
                    self.read_json()
                    self.data_json[list_name] = {}
                    with open("todo_en.json", "w") as i:
                        json.dump(self.data_json, i, indent=4)
                        break
                except FileNotFoundError:
                    with open("todo_en.json", "w") as i:
                        json.dump({}, i, indent=4)
                        continue

        while True:
            list_name = str(input("Enter To-Do List Name : "))
            if not list_name.strip():
                print(Fore.LIGHTRED_EX+"*** Please enter a name ***")
                continue

            forbidden_chars = "!" # add more if needed
            if any(char in forbidden_chars for char in list_name):
                if self.back_to_menu(list_name):
                    break
                print(Fore.LIGHTRED_EX+"*** Input contains forbidden character ***")
                continue

            if self.back_to_menu(list_name):
                break
            duplicate = None
            try:
                self.read_json()
                for key in self.data_json.keys():
                    if list_name == key:
                        print(Fore.LIGHTRED_EX+"** List name must be unique! **")
                        print(Fore.LIGHTRED_EX+f"** Duplicate List Name : {Fore.LIGHTCYAN_EX+key+Fore.LIGHTRED_EX} **")
                        duplicate = True
                        break
                if duplicate:
                    duplicate = False
                    continue
            except FileNotFoundError:
                pass

            confirm = str(input("Are you sure? (Y/n):"))
            if confirm.lower() in ["y", "yes"]:
                new_list()
                print(Fore.LIGHTGREEN_EX+"** List Created Successfully! **")
                print(Fore.LIGHTWHITE_EX+"** Returning to Main Menu **")
                return HomePage()
            else:
                continue

    def delete_list(self):
        clear()
        def delete_list_input():
            while True:
                try:
                    input_list = str(input("Enter List Name : "))
                    if not input_list.strip():
                        print(Fore.LIGHTRED_EX+"*** Please enter a name ***")
                        continue
                    if self.back_to_menu(input_list):
                        break
                    if input_list in self.data_json and isinstance(self.data_json[input_list], dict):
                        confirm = str(input("Are you sure? (Y/n):"))
                        if confirm.lower() in ["y", "yes"]:
                            clear()
                            self.data_json.pop(input_list, None)
                            with open("todo_en.json", "w") as i:
                                json.dump(self.data_json, i, indent=4)
                            print(Fore.LIGHTGREEN_EX+"** List Deleted Successfully! **")
                            return self.delete_list()
                        else:
                            continue
                    else:
                        print(Fore.LIGHTRED_EX+"** List Not Found **")
                        print(Fore.LIGHTRED_EX+"** Or List Name is Incorrect **")
                        continue
                except FileNotFoundError:
                    print(Fore.LIGHTRED_EX+"** No Lists Available **")
                    print(Fore.LIGHTRED_EX+"** Please Create a List First **")
        self.show_lists()
        print(Fore.LIGHTCYAN_EX+"=== Delete List ===")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Hint : Enter the name of the list you want to delete")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Hint : Type (!m) to return to the main menu")
        delete_list_input()

    def list_menu(self):
        clear()
        def check_json_file():
            try:
                self.read_json()
            except FileNotFoundError:
                clear()
                print(Fore.LIGHTRED_EX+"** Please Create a List First **")
                input("Press any key to return to menu")
                HomePage()
                return None

        def input_enter_list():
            while True:
                input_list = str(input("Enter Command : "))
                if not input_list:
                    print(Fore.LIGHTRED_EX+"*** Please enter a list name ***")
                    continue
                if self.back_to_menu(input_list):
                    break
                result = enter_list(input_list)
                if result:
                    return result

        def enter_list(list_name):
            parts = str(list_name).strip().split(maxsplit=1)
            command = parts[0]
            argument = parts[1] if len(parts) > 1 else ""
            if not argument:
                print(Fore.LIGHTRED_EX+"*** Please enter the command correctly ***")
                return input_enter_list()
            if command.lower() == "!ls":
                if argument in self.data_json and isinstance(self.data_json[argument], dict):
                    page = ListPage(argument)
                    page.input_command()
                    return page
                else:
                    print(Fore.LIGHTRED_EX+"** List Not Found **")
                    print(Fore.LIGHTRED_EX+"** Or List Name is Incorrect **")
                    return input_enter_list()
        check_json_file()
        self.show_lists()
        print(Style.BRIGHT+Fore.LIGHTCYAN_EX+"==== Enter List ====")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Hint : Type (!ls) and enter the list name you want to access")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Hint : Type (!m) to return to the main menu")
        return input_enter_list()

class ListPage(HomePage):
    def __init__(self, list_name):
        clear()
        self.list_name = list_name

    def show_menu(self):
        clear()
        print(Style.BRIGHT+Fore.WHITE+"="*3+f" Welcome to {Fore.LIGHTCYAN_EX+self.list_name+Fore.WHITE} "+"="*3)
        print(Style.BRIGHT+Fore.GREEN+"Command List : "
        "\nType (!b) to Create a New Task"
        "\nType (!l) to View Tasks"
        "\nType (!k) to Go Back")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Hint : Enter one of the commands above")
        
    def input_command(self):
        self.show_menu()
        while True:
            choice = str(input("Enter Command : "))
            if not choice.strip():
                print(Fore.LIGHTRED_EX+"*** Please enter a command ***")
                continue

            if str(choice).lower().strip() == "!k":
                self.list_menu()
                return None

            if self.process_command(choice):
                break

    def process_command(self, command):
        match str(command).strip().lower():
            case "!b":
                self.create_task()
                return True

            case "!l":
                self.view_list()
                return True
            
            case _:
                print(Fore.LIGHTRED_EX+"*** Please enter a valid command ***")
                return False

    def go_back(self, input_command):
        if str(input_command).lower().strip() == "!k":
            self.input_command()
            return False
        else:
            return True
    
    def view_list(self):
        self.read_json()
        clear()    
        def show_tasks():
            if not self.data_json[self.list_name]:
                print(Fore.LIGHTRED_EX+"** No Tasks Available **")
                return False
            for number, (key, value) in enumerate(self.data_json[self.list_name].items(), start=1):
                checkbox = "[x]" if value["status"] else "[ ]"
                print(f"{number}. {checkbox} {key}")
        
        def edit_task():
            def clear_cache():
                clear()
                show_task_details()

            def back_to_previous(input_command, back_number):
                if back_number == 1:
                    if str(input_command).lower().strip() == "!k":
                        return True
                    else:
                        return False
                if back_number == 2:
                    if str(input_command).lower().strip() == "!k":
                        clear()
                        show_task_details()
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Hint : Enter which part you want to edit"
                        "\nExample : \"edit part : task name\""
                        "\nType (!k) to Go Back")
                        return True
                    else:
                        return False
                
            def confirm():
                sure = str(input("Are you sure? (Y/n):"))
                if sure.lower() in ["y", "yes"]:
                    print(Fore.LIGHTGREEN_EX+"** Successfully Edited **")
                    clear()
                    show_task_details()
                    print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Hint : Enter which part you want to edit"
                    "\nExample : \"edit part : task name\""
                    "\nType (!k) to Go Back")
                    return True
                else:
                    print(Fore.LIGHTRED_EX+"*** Failed to Edit ***")
                    return False
            def show_task_details():
                status = Fore.LIGHTGREEN_EX+"Completed" if value["status"] else Fore.LIGHTRED_EX+"Not Completed"
                print(Fore.LIGHTBLUE_EX + "="*40)
                print(Fore.LIGHTYELLOW_EX+f"Task Name : {key}")
                print(Fore.LIGHTCYAN_EX+f"Note : {value['note']}")
                print(f"Status : {status}")
                print(Fore.LIGHTMAGENTA_EX+f"Created Date : {value['created date']}")
                print(Fore.LIGHTBLUE_EX + "="*40)

            def input_edit():
                while True:
                    edit = input("Edit Part : ")
                    if not edit.strip():
                        print(Fore.LIGHTRED_EX+"*** Please enter input ***")
                    if back_to_previous(edit, 1):
                        return True
                    if process_edit_part(edit):
                        with open("todo_en.json", "w") as i:
                            json.dump(self.data_json, i, indent=4)
                        return True

            def process_edit_part(edit):
                header_edit = lambda edit_part = str:print(Fore.LIGHTBLUE_EX+"="*10+f" Edit {edit_part.capitalize()} "+"="*10)
                match edit.strip().lower():
                    case "task name":
                        clear_cache()
                        header_edit("task name")
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Hint : Enter the new task name")
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Type (!k) to Go Back")
                        while True:
                            new_name = str(input("Enter New Name : ")).strip()
                            if back_to_previous(new_name, 2):
                                return False
                            if not new_name:
                                print(Fore.LIGHTRED_EX+"*** Please enter input ***")
                                continue
                            if confirm():
                                self.data_json[self.list_name][new_name] = self.data_json[self.list_name].pop(key)
                                return True
                            else:
                                continue
                    case "note":
                        clear_cache()
                        header_edit("note")
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Hint : Enter the new note")
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Type (!k) to Go Back")
                        while True:
                            new_note = str(input("Enter New Note : ")).strip()
                            if back_to_previous(new_note, 2):
                                return False
                            if not new_note:
                                print(Fore.LIGHTRED_EX+"*** Please enter input ***")
                                continue

                            if confirm():
                                self.data_json[self.list_name][key]["note"] = new_note
                                return True
                            else:
                                continue
                    case "status":
                        clear_cache()
                        header_edit("status")
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Hint : Enter the new status" \
                        "\nHint: Only accepts [true / completed and false / not completed]")
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Type (!k) to Go Back")
                        while True:
                            new_status = str(input("Enter New Status : ")).strip().lower()
                            if back_to_previous(new_status, 2):
                                return False
                            if not new_status:
                                print(Fore.LIGHTRED_EX+"*** Please enter input ***")
                                continue

                            if new_status in ["true", "completed", "done"]:
                                self.data_json[self.list_name][key]["status"] = True
                            elif new_status in ["false", "not completed", "not done"]:
                                self.data_json[self.list_name][key]["status"] = False
                            else:
                                print(Fore.LIGHTRED_EX+"*** Please enter a valid status! ***")
                                continue
                            if confirm():
                                return True
                            else:
                                continue
                    case "created date":
                        clear_cache()
                        header_edit("created date")
                        print(Style.DIM+Fore.LIGHTYELLOW_EX+"Warning : Changing \"Created Date\" will affect history.")
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Hint : Enter the new created date (YYYY-MM-DD)")
                        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Type (!k) to Go Back")
                        while True:
                            new_date = str(input("Enter New Date : ")).strip().lower()

                            if back_to_previous(new_date, 2):
                                return False
                            if not new_date:
                                print(Fore.LIGHTRED_EX+"*** Please enter input ***")
                                continue
                                
                            new_date = new_date.split("-", maxsplit=3)
                            
                            if len(new_date) < 3:
                                print(Fore.LIGHTRED_EX+"** New date must follow the format **")
                                continue

                            if len(new_date[0]) > 4:
                                print(Fore.LIGHTRED_EX+"** Year is not valid **")
                                continue
                            elif len(new_date[1]) < 2 or len(new_date[1]) > 2:
                                print(Fore.LIGHTRED_EX+"** Month is not valid **")
                                continue
                            elif len(new_date[2]) < 2 or len(new_date[2]) > 2:
                                print(Fore.LIGHTRED_EX+"** Day is not valid **")
                                continue
                            
                            not_number = None
                            for date_part in new_date:
                                if not date_part.isnumeric():
                                    print(Fore.LIGHTRED_EX+"*** Date must be numeric ***")
                                    not_number = True
                                    break
                            if not_number:
                                not_number = False
                                continue

                            if int(new_date[1]) > 12:
                                print(Fore.LIGHTRED_EX+"** Month is not valid **")
                                continue
                            elif int(new_date[2]) > 31:
                                print(Fore.LIGHTRED_EX+"** Day is not valid **")
                                continue
                            
                            print(Style.DIM+Fore.LIGHTYELLOW_EX+"Warning : Changing \"Created Date\" will affect history.")
                            if confirm():
                                self.data_json[self.list_name][key]["created date"] = f"{new_date[0]}-{new_date[1]}-{new_date[2]} (Edited)"
                                return True
                            else:
                                continue
                    case _:
                        print(Fore.LIGHTRED_EX+"*** Part not found ***")
                        return False

            if self.argument > len(self.data_json[self.list_name]):
                print(Fore.LIGHTRED_EX+"*** Number not found ***")
                return False
            clear()
            for number, (key, value) in enumerate(self.data_json[self.list_name].items(), start=1):
                if self.argument == number:
                    show_task_details()
                    print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Hint : Enter which part you want to edit"
                    "\nExample : \"edit part : task name\""
                    "\nType (!k) to Go Back")
                    if input_edit():
                        self.view_list()
                        break
                        
        def task_info():
            if self.argument > len(self.data_json[self.list_name]):
                print(Fore.LIGHTRED_EX+"*** Number not found ***")
                return False
            clear()
            for number, (key, value) in enumerate(self.data_json[self.list_name].items(), start=1):
                if self.argument == number:
                    status = Fore.LIGHTGREEN_EX+"Completed" if value["status"] else Fore.LIGHTRED_EX+"Not Completed"
                    print(Fore.LIGHTBLUE_EX + "="*40)
                    print(Fore.LIGHTYELLOW_EX+f"Task Name : {key}")
                    print(Fore.LIGHTCYAN_EX+f"Note : {value['note']}")
                    print(f"Status : {status}")
                    print(Fore.LIGHTMAGENTA_EX+f"Created Date : {value['created date']}")
                    print(Fore.LIGHTBLUE_EX + "="*40)
                    input(Style.DIM+Fore.WHITE+"Press Enter to go back : ")
                    self.view_list()
                    return True

        def check_task():
            if self.argument > len(self.data_json[self.list_name]):
                print(Fore.LIGHTRED_EX+"*** Number not found ***")
                return False
            for number, key in enumerate(self.data_json[self.list_name].keys(), start=1):
                if int(self.argument) == number:
                    status = True if not self.data_json[self.list_name][key]["status"] else False
                    self.data_json[self.list_name][key]["status"] = status
                    with open("todo_en.json", "w") as i:
                        json.dump(self.data_json, i, indent=4)
                    self.view_list()
                    return True
                
        def delete_task():
            if self.argument > len(self.data_json[self.list_name]):
                print(Fore.LIGHTRED_EX+"*** Number not found ***")
                return False
            for number, key in enumerate(self.data_json[self.list_name].keys(), start=1):
                if self.argument == number:
                    sure = str(input("Are you sure? (Y/n):"))
                    if sure.lower() in ["y", "yes"]:
                        self.data_json[self.list_name].pop(key, None)
                        with open("todo_en.json", "w") as i:
                            json.dump(self.data_json, i, indent=4)
                        print(Fore.LIGHTGREEN_EX+"** Successfully Deleted Task **")
                        self.view_list()
                        return True
                    else:
                        print(Fore.LIGHTRED_EX+"** Failed to Delete Task **")
                        return False

        def command_selector(input_command):
            parts = str(input_command).strip().split(maxsplit=1)
            command = parts[0]
            argument = parts[1] if len(parts) > 1 else ""
            try:
                self.argument = int(argument)
            except ValueError:
                print(Fore.LIGHTRED_EX+"*** Please enter a number only! ***")
                return False

            match command.lower():
                case "!c":
                    if check_task():
                        return True
                    else:
                        return False
                case "!i":
                    if task_info():
                        return True
                    else:
                        return False
                case "!e":
                    if edit_task():
                        self.view_list()
                        return True
                    else:
                        return False
                case "!h":
                    if delete_task():
                        return True
                    else:
                        return False
                case _:
                    print(Fore.LIGHTRED_EX+"*** Command not found! ***")
                    return False

        print(Style.BRIGHT+Fore.LIGHTCYAN_EX+"=== Task List ===")
        print(Style.DIM+Fore.LIGHTBLUE_EX+
            "Type (!i) to View Task Info"
            "\nType (!c) to Check / Uncheck"
            "\nType (!e) to Edit Task"
            "\nType (!h) to Delete Task"
            "\nType (!k) to Go Back")
        print(Style.NORMAL+Fore.LIGHTGREEN_EX+"Hint : Type the command with the task number")
        print("="*10+" Task List "+"="*10)

        show_tasks()
        print("="*31)
        while True:
            command = str(input("Enter Command : "))
            if not command.strip():
                print(Fore.LIGHTRED_EX+"*** Please enter a command! ***")
                continue

            if not self.go_back(command):
                break
            
            if command_selector(command):
                break

    def create_task(self):

        def task_json():
            self.read_json()

            for todo in self.data_json[self.list_name]:
                if task == todo:
                    print(Fore.LIGHTRED_EX+"** Task name must be unique! **")
                    print(Fore.LIGHTRED_EX+f"** Duplicate Task Name : {Fore.LIGHTCYAN_EX+todo+Fore.LIGHTRED_EX} **")
                    return False

            note = str(input("Enter Additional Note (Optional) : "))

            sure = str(input("Are you sure? (Y/n):"))
            if sure.lower() in ["y", "yes"]:
                self.data_json[self.list_name][task] = {"note" : note, "status" : False, "created date" : date_today}
                # order in list = [additional note, status:bool, created date]

                with open("todo_en.json", "w") as i:
                    json.dump(self.data_json, i, indent=4)

                print(Fore.LIGHTGREEN_EX+"** Successfully Created Task **")
                return True
            else:
                print(Fore.LIGHTRED_EX+"** Failed to Create Task **")
                return False
        clear()
        print(Style.BRIGHT+Fore.LIGHTCYAN_EX+"=== Create Task ===")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Hint : Enter the name of the task you want to create")
        print(Style.DIM+Fore.LIGHTBLUE_EX+"Hint : Type (!k) to Go Back")

        while True:
            task = str(input("Enter Task Name : "))
            if not task.strip():
                print(Fore.LIGHTRED_EX+"*** Please enter a task name ***")
                continue
            if not self.go_back(task):
                break

            if not task_json():
                continue

if __name__ == "__main__":
    HomePage()
