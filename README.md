## Todo CLI
CLI tool quản lý task định lượng - khởi đầu là bài G14.1, đã mở rộng nhiều đợt

## Tính năng
- Task định lượng: mục tiêu + tiến độ (VD "Đọc sách 10/20 trang") thay vì chỉ done/chưa
- Progress bar màu + đánh dấu ✓ khi đạt
- Độ ưu tiên (cao/trung bình/thấp) - tô màu theo mức, sort theo ưu tiên
- Cập nhật tiến độ cộng dồn, chúc mừng khi vừa đạt mục tiêu
- Quản lý task: sửa tên/mục tiêu/đơn vị/ưu tiên, xoá
- **Link task với Habit** (habit_cli): task là "việc con" của 1 habit dài hạn;
  tạo habit mới ngay từ todo, gỡ/đổi liên kết trong menu Quản lý task
- Mỗi task có ID ổn định (todo_N), file JSON tự nâng cấp cấu trúc cũ

## Cách chạy
python todo.py
Yêu cầu: Python 3.x, questionary, rich

## Phụ thuộc (cho tính năng link)
Tính năng link cần 2 thứ cùng tồn tại trên máy:
- hub_cli - todo tra `tools.json` của hub để tìm đường tới habit_cli
- habit_cli - đã đăng ký trong hub với tên "Habit tracker"
Không có 2 cái này thì phần link sẽ lỗi khi thêm task.

## Learning transparency

## Khái niệm mới - AI hỗ trợ nhiều (lần đầu):
- validate=lambda + isdigit() trong questionary - Claude chỉ (nhận từ trước), AI này giải thích thêm short-circuit and
- min() để cap progress bar - AI giải thích cách dùng
- Quirk questionary: Choice(value=None) trả về title - AI chẩn đoán khi bug xuất hiện; ESC vs Ctrl+C trong text prompt - AI giải thích
- is None vs == None, early-break pattern - AI giải thích và đặt tên pattern
- ID + auto-increment counter (next_id riêng, chỉ tiến không lùi) - AI giải thích cơ chế; ⚠️ nhưng nguyên tắc "không tái dùng số sau khi xoá" là mình tự suy ra trước (liên hệ DB của FB) rồi AI mới xác nhận + đặt tên
- isinstance() phân biệt list/dict - AI giải thích
- Schema migration (convert list cũ → dict {items, next_id}) - hàm load_tasks bản convert do AI viết hộ khi mình bí (mức co-written) - sau đó mình tự mirror toàn bộ sang habit_cli không cần hỗ trợ
- Cross-file read/write qua registry (todo đọc/ghi habit.json) - AI đưa khung hàm đầu tiên (get_habit_py_path), 3 hàm còn lại tự viết theo
- Nguyên tắc helper phân loại - caller diễn giải (choose_habit trả 3 tín hiệu, mỗi chỗ gọi tự xử) - AI giải thích khi mình thắc mắc "sao lọc 2 lần"

## Mới nhưng tự làm được:
- Data model định lượng (current/target/unit thay done bool) - tự thiết kế từ nhu cầu thật
- Điều kiện just_done (chúc mừng đúng lúc vừa đạt target) - tự viết logic check-trước-khi-cộng, AI chỉ sửa biên > → >=
- Màu theo ưu tiên (LEVEL_COLOR dict lookup) - ý tưởng + triển khai tự làm theo skeleton
- Sort menu giữ màu rich (lai questionary chọn kiểu sort + rich in) - tự nghĩ ra cách né xung khắc màu/tương tác
- Phát hiện trùng lặp thiết kế (menu link bọc ngoài choose_habit) và trade-off của nó - tự nhận ra
