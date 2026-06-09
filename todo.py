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


def list_tasks(tasks):
    """In ra tất cả task kèm số thứ tự và trạng thái"""
    LENGTH = 20
    for i, t in enumerate(tasks, 1):
        current = t["current"]
        target = t["target"]
        unit = t["unit"]
        filled = int(current / target * LENGTH)
        filled = min(filled, LENGTH)
        bar = "█" * filled + "░" * (LENGTH - filled)
        done = current >= target
        tick = "✓" if done else " "
        print(f"{i}. {tick} {t['name']} - {current} / {target} {unit} ({bar})")


def update_progress(task, amount):
    """Đánh dấu task[index] là hoàn thành"""
    task["current"] += amount
    return task
        

def delete_task(index, tasks):
    """Trả về task đã xoá, hoặc None nếu Index sai"""
    if 0 < index <= len(tasks):
        return tasks.pop(index - 1)
    return None


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
DEL = "Xoá task"
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
            UPDATE,
            DEL,
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

        elif choice == DEL:
            list_tasks(tasks)
            try:
                idx = int(input("Nhập số thứ tự muốn xoá: "))
            except ValueError:
                print("Số không hợp lệ!")
                continue
            confirm = questionary.confirm(f"Bạn chắc chắn muốn xoá?").ask()
            if confirm:
                deleted = delete_task(idx, tasks)
                save_task(tasks)
                if deleted:
                    print(f"Đã xoá {deleted['name']}")
                else:
                    print(f"Số thứ tự không hợp lệ. Chỉ có {len(tasks)} task!")
            else:
                print("Huỷ xoá")
                
        elif choice == UPDATE:
            chosen = questionary.select(
                "Chọn task để cập nhật:",
                choices = [Choice(f"{t['name']} {t['current']} / {t['target']}", value=t) for t in tasks]
            ).ask()
            if chosen:
                amount = questionary.text(
                "Đã làm thêm: ",
                validate=lambda s: True if s.isdigit() and int(s) > 0 else "Hãy nhập số lớn hơn 0" 
            ).ask()
                amount = int(amount)
                update_progress(chosen, amount)
                print(f"{chosen['name']} đã cập nhật: {chosen['current']} / {chosen['target']}")
                save_task(tasks)

        elif choice == EXIT:
            print("Tạm biệt, chương trình kết thúc!")
            break
if __name__ == "__main__":
    main()



   