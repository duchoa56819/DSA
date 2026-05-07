# 📖 Hướng Dẫn Sử Dụng Khóa Học DSA

Chào mừng bạn đến với khóa học **Cấu Trúc Dữ Liệu & Giải Thuật (DSA)** toàn diện. Tài liệu này sẽ giúp bạn hiểu cách khai thác tối đa bộ tài liệu và công cụ trực quan đi kèm.

---

## 🛠 Yêu cầu hệ thống

1.  **Python 3.8+**: Cài đặt tại [python.org](https://www.python.org/).
2.  **Trình duyệt web**: (Chrome, Edge, Firefox,...) để chạy bộ Visualizer.
3.  **Git**: Để quản lý phiên bản (tùy chọn).

---

## 📂 Cấu trúc thư mục

- `01-complexity/` đến `10-graph-algorithms/`: Chứa lý thuyết (`theory.md`) và code minh họa (`.py`).
- `visualizer/`: Website trực quan hóa thuật toán.
- `README.md`: Tổng quan lộ trình học.

---

## 🚀 Cách học hiệu quả

### 1. Đọc Lý Thuyết (`theory.md`)
Bắt đầu với file `theory.md` trong mỗi thư mục. Nội dung được viết bằng tiếng Việt, tập trung vào:
- Bản chất của cấu trúc dữ liệu/thuật toán.
- Độ phức tạp thời gian (Time Complexity) và không gian (Space Complexity).
- Các trường hợp ứng dụng thực tế.

### 2. Chạy Code Minh Họa (`.py`)
Mở terminal (CMD hoặc PowerShell) và chạy các file Python để xem kết quả thực tế.
> **Lưu ý**: Nếu gặp lỗi hiển thị tiếng Việt, hãy chạy lệnh sau trước khi chạy code:
> ```powershell
> $env:PYTHONIOENCODING='utf-8'
> ```

Ví dụ chạy thuật toán sắp xếp:
```powershell
python 07-sorting/sorting.py
```

### 3. Sử Dụng Visualizer (Trực Quan Hóa)
Đây là công cụ mạnh mẽ nhất để bạn "nhìn thấy" cách thuật toán hoạt động.
1. Mở file `visualizer/index.html` bằng trình duyệt.
2. Chọn Tab (Sorting, Searching, Pathfinding, Data Structures).
3. Tùy chỉnh thông số (Kích thước, Tốc độ) và nhấn **▶ Bắt đầu**.

### 4. Giải Bài Tập
Ở cuối mỗi file `theory.md` đều có danh sách các bài tập trên **LeetCode**. Bạn nên lên LeetCode tìm theo ID (ví dụ: #1, #20) để thực hành.

---

## 📤 Cập nhật mã nguồn lên GitHub

Để lưu trữ code của riêng bạn hoặc đóng góp:
1. Tạo repo trên GitHub.
2. Link local với remote:
   ```bash
   git remote add origin https://github.com/duchoa56819/DSA
   git push -u origin main
   ```

---
Chúc bạn có một hành trình chinh phục DSA thú vị! 🚀
