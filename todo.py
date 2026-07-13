import questionary
import json
import os
from questionary import Style, Choice
from rich import print as printr
from datetime import date

custom_style = Style([
    ("pointer", "fg:#ffff00 bold"),
    ("highlighted", "fg:#ffff00 bold"),
    ])

ADD = "Thêm task"
LIST = "Xem task"
UPDATE = "Cập nhật tiến độ"
EDIT = "Quản lý task"
EXIT = "Thoát"

DEFAULTS = {"target": 1,
            "current": 0,
            "unit": "",
            "level": "trung bình",
            "parent_habit": None,
            "day": ""
}

LEVEL_COLOR = {
    "cao": "#ff0000",
    "trung bình": "#FFA500",
    "thấp": "#96918e",
}

ORDER = {"cao": 1, "trung bình": 2, "thấp": 3}

FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(FOLDER,"todo.json")
TOOLS_PATH = r"C:\Python\hub_cli\tools.json"

def get_habit_py_path():
    with open(TOOLS_PATH, "r", encoding="utf-8") as f:
        tools = json.load(f)
    for t in tools:
        if t["name"] == "Habit tracker":
            return t["path"]
    return None

def get_habit_json_path():
    py_path = get_habit_py_path()
    folder = os.path.dirname(py_path)
    return os.path.join(folder, "habit.json")

def get_habit_data():
    path = get_habit_json_path()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_habit_data(data):
    path = get_habit_json_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_new_habit(habit):
    data = get_habit_data()
    new_id = data["next_id"]
    data["items"].append({"id": f"habit_{new_id}","habit": habit, "history": []})
    data["next_id"] += 1
    save_habit_data(data)
    return f"habit_{new_id}"
    

def choose_habit():
    data = get_habit_data()
    habits = data["items"]

    choices = [Choice(h["habit"], value=h["id"]) for h in habits]
    choices = choices + [Choice("Không link", value="nolink")]
    choices = choices + [Choice("Habit mới", value="new")]
    
    result = questionary.select(
        "Link với Habit:",
        choices = choices,
        style = custom_style
    ).ask()
    if result is None:
        return None
    elif result == "new":
        new = questionary.text("Tên Habit mới:").ask()
        if new is None:
            return None
        new = new.strip()
        if not new:
            return None
        return create_new_habit(new)
    return result

def add_task(name, data, target, unit, level, parent_habit):
    """Thêm task mới vào list"""
    new_id = data["next_id"]
    data["items"].append({"id": f"todo_{new_id}", "name": name, "target": target,
                          "current": 0, "unit": unit, "level": level, "parent_habit": parent_habit})
    data["next_id"] = data["next_id"] + 1

def progress_bar(current, target, color=False):
    LENGTH = 20
    filled = int(current / target * LENGTH)
    filled = min(filled, LENGTH)
    if color:
        return f"[#00aa00]{'█' * filled}[/]{'░' * (LENGTH - filled)}"
    else:
        return "█" * filled + "░" * (LENGTH - filled)


def list_tasks(tasks):
    """In ra tất cả task kèm số thứ tự và trạng thái"""
    for i, t in enumerate(tasks, 1):
        current = t["current"]
        target = t["target"]
        unit = t["unit"]
        color = LEVEL_COLOR[t['level']]
        bar = progress_bar(current, target, color=True)
        done = current >= target
        tick = "[#00aa00]✓[/]" if done else " "
        printr(f"{i}. {tick} [{color}]{t['name']}[/] - {current} / {target} {unit} {bar}")


def update_progress(task, amount):
    """Đánh dấu task[index] là hoàn thành"""
    task["current"] += amount
    return task

def reset_daily(data):
    today = date.today().isoformat()
    changed = False
    for t in data["items"]:
        if t["parent_habit"] is not None and t["day"] != today:
            t["current"] = 0
            t["day"] = today
            changed = True
    if changed:
        save_task(data)

def migrate(tasks):
    for i, t in enumerate(tasks):
        tasks[i] = {**DEFAULTS, **t}
    return tasks


def save_task(data):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_tasks():
    try:
        with open(PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"items": [], "next_id": 1}
    
    if isinstance(data, list):
        for i, task in enumerate(data, 1):
            task["id"] = f"todo_{i}"
        return {"items": data, "next_id": len(data) + 1}
    
    return data


def main():
    data = load_tasks()
    tasks = data["items"]
    migrate(tasks)
    reset_daily(data)
    while True:
        choice = questionary.select(
        "____TO-DO LIST____",
        choices=[
            ADD,
            LIST,
            EDIT,
            UPDATE,
            EXIT
            ],
        style = custom_style,
        ). ask()
        
        print(f"Bạn chọn {choice}")

        if choice == ADD:
            name = input("Tên task: ").strip()
            if not name:
                print("Tên task không được rỗng!")
                continue
            target = questionary.text(
                "Mục tiêu (VD: 50): ",
                validate=lambda s: True if s.isdigit() and int(s) > 0 else "Phải nhập số lớn hơn 0!"
            ).ask()
            target = int(target)
            unit = questionary.text("Đơn vị mục tiêu (VD: lần): ").ask()
            level = questionary.select(
                "Mức độ ưu tiên:",
                choices = ["cao", "trung bình", "thấp"],
                style=custom_style
            ).ask()
            parent = choose_habit()
            if parent == "nolink":
                parent = None
            add_task(name, data, target, unit, level, parent)
            save_task(data)

        elif choice == LIST:
            list_tasks(tasks)
            while True:
                action = questionary.select(
                    "Xem theo mức độ ưu tiên",
                    choices = [
                        Choice("cao -> thấp", value = 1),
                        Choice("Thấp -> cao", value = 2),
                        Choice("↩️ Quay lại", value = "back")
                    ],
                    style=custom_style
                ).ask()
                if action == "back" or action is None:
                    break
                elif action == 1:
                    sorted_tasks = sorted(tasks, key=lambda t: ORDER[t['level']])
                    list_tasks(sorted_tasks)
                elif action == 2:
                    sorted_tasks = sorted(tasks, key=lambda t: ORDER[t['level']], reverse=True)
                    list_tasks(sorted_tasks)
            
        elif choice == EDIT:
            while True:
                chosen = questionary.select(
                    "Chọn task để hiệu chỉnh:",
                    choices = [Choice(f"{t['name']} {t['current']} / {t['target']} {t['unit']}", value=t) for t in tasks] + 
                    [Choice("↩️ Quay lại", value="back")],
                    style = custom_style,
                ).ask()
                if chosen == 'back' or chosen is None:
                    break
                elif chosen:
                    while True:
                        action = questionary.select(
                            "Quản lý task",
                            choices = [
                                Choice("Chỉnh sửa tên", value="name"),
                                Choice("Chỉnh sửa mục tiêu", value="target"),
                                Choice("Chỉnh sửa đơn vị", value="unit"),
                                Choice("Chỉnh sửa ưu tiên", value="level"),
                                Choice("Xoá task", value="del"),
                                Choice("Điều chỉnh Habit", value="link"),
                                Choice("↩️ Quay lại", value="exit")],
                                style = custom_style,
                            ).ask()
                        if action == "name":
                            new_name = questionary.text(
                                "Nhập tên mới: "
                            ).ask()
                            if new_name is None:
                                continue
                            else:
                                new_name = new_name.strip()
                                chosen['name'] = new_name
                        elif action == "target":
                            new_target = questionary.text(
                                "Nhập mục tiêu mới: ",
                                validate = lambda s: True if s.isdigit() and int(s) > 0 else "Phải nhập số lớn hơn 0"
                            ).ask()
                            if new_target is None:
                                continue
                            else:
                                new_target = int(new_target)
                                chosen['target'] = new_target
                        elif action == "unit":
                            new_unit = questionary.text(
                                "Nhập đơn vị mới: "
                            ).ask()
                            if new_unit is None:
                                continue
                            else:
                                new_unit = new_unit.strip()
                                chosen['unit'] = new_unit
                        elif action == "level":
                            new_level = questionary.select(
                                "Thay đổi ưu tiên:",
                                choices = [
                                    "cao", "trung bình", "thấp"
                                ],
                                style = custom_style
                            ).ask()
                            if new_level is None:
                                continue
                            else:
                                chosen['level'] = new_level
                        elif action == "del":
                            confirm = questionary.confirm(f"Bạn chắc chắn muốn xoá?").ask()
                            if confirm:
                                tasks.remove(chosen)
                                print(f"Đã xoá {chosen['name']}")
                                save_task(data)
                                break
                            else:
                                print("Huỷ xoá")
                        elif action == "link":
                            new_link = questionary.select(
                                "Điều chỉnh Habit:",
                                choices = [
                                    Choice("Huỷ bỏ liên kết", value="nolink"),
                                    Choice("Thay đổi liên kết Habit / Tạo habit mới", value="change"),
                                ],
                                style=custom_style,
                            ).ask()
                            if new_link is None:
                                continue
                            elif new_link == "nolink":
                                chosen['parent_habit'] = None
                            elif new_link == "change":
                                new_link = choose_habit()
                                if new_link is None:
                                    continue
                                elif new_link == "nolink":
                                    chosen['parent_habit'] = None
                                else:
                                    chosen['parent_habit'] = new_link
                        else:
                            break
                        save_task(data)
                
                
        elif choice == UPDATE:
            while True:
                chosen = questionary.select(
                    "Chọn task để cập nhật:",
                    choices = [Choice(f"{t['name']} {t['current']} / {t['target']} {t['unit']}", value=t) for t in tasks] + 
                        [Choice("↩️ Quay lại", value="back")],
                        style = custom_style,
                ).ask()
                if chosen == 'back' or chosen is None:
                    break
                amount = questionary.text(
                "Đã làm thêm: ",
                validate=lambda s: True if s.isdigit() and int(s) > 0 else "Hãy nhập số lớn hơn 0" 
            ).ask()
                if amount is None:
                    continue
                else:
                    amount = int(amount)
                    just_done = chosen['current'] < chosen['target'] and chosen['current'] + amount >= chosen['target']
                    update_progress(chosen, amount)
                    save_task(data)
                    if just_done:
                        printr("🎉🎉🎉[green]Chúc mừng bạn đã hoàn thành task![/]🎉🎉🎉")
                    else:
                        print(f"{chosen['name']} đã cập nhật: {chosen['current']} / {chosen['target']}")
                    

                
        elif choice == EXIT:
            print("Tạm biệt, chương trình kết thúc!")
            break
if __name__ == "__main__":
    main()