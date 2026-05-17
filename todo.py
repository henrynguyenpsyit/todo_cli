import questionary


def add_task(name, tasks):
    """Thêm task mới vào list"""
    tasks.append({"name": name, "done": False})


def list_tasks(tasks):
    """In ra tất cả task kèm số thứ tự và trạng thái"""
    for i, t in enumerate(tasks, 1):
        tick = "[x]" if t["done"] else "[ ]"
        print(f"{i}. {tick} - {t['name']}")


def mark_done(index, tasks):
    """Đánh dấu task[index] là hoàn thành"""
    if 0 < index <= len(tasks):
        tasks[index - 1]["done"] = True
        return tasks[index-1]
    return None
        

def delete_task(index, tasks):
    """Trả về task đã xoá, hoặc None nếu Index sai"""
    if 0 < index <= len(tasks):
        return tasks.pop(index - 1)
    return None


def main ():
    tasks = []
    while True:
        choice = questionary.select(
        "____TO-DO LIST____",
        choices=[
            "Thêm task",
            "Xem task",
            "Đánh dấu hoàn thành",
            "Xoá task",
            "Thoát"
            ]
        ). ask()
        
        print(f"Bạn chọn {choice}")

        if choice == "Thêm task":
            name = input("Tên task: ")
            add_task(name, tasks)

        elif choice == "Xem task":
            list_tasks(tasks)

        elif choice == "Xoá task":
            list_tasks(tasks)
            try:
                idx = int(input("Nhập số thứ tự muốn xoá: "))
            except ValueError:
                print("Số không hợp lệ!")
                continue
            confirm = questionary.confirm(f"Bạn chắc chắn muốn xoá?").ask()
            if confirm:
                deleted = delete_task(idx, tasks)
                if deleted:
                    print(f"Đã xoá {deleted['name']}")
                else:
                    print(f"Số thứ tự không hợp lệ. Chỉ có {len(tasks)} task!")
            else:
                print("Huỷ xoá")
                
        elif choice == "Đánh dấu hoàn thành":
            list_tasks(tasks)
            try:
                mark = int(input("Chọn task hoàn thành: "))
            except ValueError:
                print("Vui lòng nhập số!")
                continue
            done_mark = mark_done(mark, tasks)
            if done_mark:
                print(f"{done_mark['name']} đã hoàn thành")
            else:
                print(f"Số thứ tự không hợp lệ. Chỉ có {len(tasks)} task")
        elif choice == "Thoát":
            print("Tạm biệt, chương trình kết thúc!")
            break
if __name__ == "__main__":
    main()