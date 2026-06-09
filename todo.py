import questionary
import json
import os
from questionary import Style, Choice

custom_style = Style([
    ("pointer", "fg:#ffff00 bold"),
    ("highlighted", "fg:#ffff00 bold"),
])


DEFAULTS = {"target": 1,
            "current": 0,
            "unit": ""}

FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(FOLDER,"todo.json")


def add_task(name, tasks, target, unit):
    """Thêm task mới vào list"""
    tasks.append({"name": name, "target": target, "current": 0, "unit": unit})


def progress_bar(current, target):
    LENGTH = 20
    filled = int(current / target * LENGTH)
    filled = min(filled, LENGTH)
    return "█" * filled + "░" * (LENGTH - filled)


def list_tasks(tasks):
    """In ra tất cả task kèm số thứ tự và trạng thái"""
    for i, t in enumerate(tasks, 1):
        current = t["current"]
        target = t["target"]
        unit = t["unit"]
        bar = progress_bar(current, target)
        done = current >= target
        tick = "✓" if done else " "
        print(f"{i}. {tick} {t['name']} - {current} / {target} {unit} ({bar})")


def update_progress(task, amount):
    """Đánh dấu task[index] là hoàn thành"""
    task["current"] += amount
    return task


def migrate(tasks):
    for i, t in enumerate(tasks):
        tasks[i] = {**DEFAULTS, **t}
    return tasks


def save_task(tasks):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def load_tasks():
    try:
        with open(PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
ADD = "Thêm task"
LIST = "Xem task"
UPDATE = "Cập nhật tiến độ"
EDIT = "Quản lý task"
EXIT = "Thoát"


def main():
    tasks = load_tasks()
    migrate(tasks)
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
            add_task(name, tasks, target, unit)
            save_task(tasks)

        elif choice == LIST:
            list_tasks(tasks)


        elif choice == EDIT:
            while True:
                chosen = questionary.select(
                    "Chọn task để hiệu chỉnh:",
                    choices = [Choice(f"{t['name']} {t['current']} / {t['target']} {t['unit']} {progress_bar(t['current'], t['target'])}", value=t) for t in tasks] + 
                    [Choice("↩️ Quay lại", value="back")]
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
                                Choice("Xoá task", value="del"),
                                Choice("↩️ Quay lại", value="exit")]
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
                        elif action == "del":
                            confirm = questionary.confirm(f"Bạn chắc chắn muốn xoá?").ask()
                            if confirm:
                                tasks.remove(chosen)
                                print(f"Đã xoá {chosen['name']}")
                                break
                            else:
                                print("Huỷ xoá")
                        else:
                            break
                save_task(tasks)
                

        elif choice == UPDATE:
            while True:
                chosen = questionary.select(
                    "Chọn task để cập nhật:",
                    choices = [Choice(f"{t['name']} {t['current']} / {t['target']} {t['unit']} {progress_bar(t['current'], t['target'])}", value=t) for t in tasks] + 
                        [Choice("↩️ Quay lại", value="back")]
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
                    update_progress(chosen, amount)
                    print(f"{chosen['name']} đã cập nhật: {chosen['current']} / {chosen['target']}")
                    save_task(tasks)
                
        elif choice == EXIT:
            print("Tạm biệt, chương trình kết thúc!")
            break
if __name__ == "__main__":
    main()
