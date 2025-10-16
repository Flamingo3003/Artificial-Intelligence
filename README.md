# Artificial-Intelligence
Giới thiệu

♟️ BÁO CÁO CÁ NHÂN
👤 Thông tin sinh viên

Họ và tên: Tạ Hoàng Đạt

MSSV: 23110090

Lớp: Tri tue nhan tao_ Nhom 04CLC

Môn học: Trí tuệ nhân tạo

Đề tài: Giải bài toán 8 quân hậu bằng nhiều thuật toán tìm kiếm

Giảng viên hướng dẫn: TS.Phan Thị Huyền Trang

🎯 Mục tiêu

Hiểu rõ cơ chế hoạt động của các thuật toán tìm kiếm trong AI.

So sánh hiệu quả của từng thuật toán khi áp dụng cho bài toán 8 quân hậu.

Xây dựng chương trình minh họa trực quan bằng Pygame.

⚙️ Công cụ và môi trường phát triển
Thành phần	Mô tả
Ngôn ngữ	Python 3.12
Thư viện	pygame, heapq, collections, tkinter, random, time, sys
IDE	Visual Studio 2022 / VS Code
Hệ điều hành	Windows 10
💡 Giới thiệu bài toán

Bài toán 8 Queens (8 quân hậu) yêu cầu đặt 8 quân hậu lên bàn cờ 8×8 sao cho không quân nào tấn công được nhau (tức là không có 2 quân cùng hàng, cùng cột hoặc cùng đường chéo).

Chương trình cài đặt nhiều thuật toán khác nhau để tìm kiếm lời giải và hiển thị trực quan quá trình tìm kiếm trên giao diện đồ họa.

🔍 Các thuật toán được cài đặt
Nhóm thuật toán	Cụ thể
Tìm kiếm có hệ thống	DFS, BFS, UCS, DLS, IDS
Tìm kiếm heuristic	Greedy Best-First, A*, Hill Climbing
Tối ưu hóa	Beam Search, Genetic Algorithm
Ràng buộc	Backtracking, Forward Checking
Biến thể	Partial Observation

Mỗi thuật toán đều có hàm riêng trong file 8Queens_23110090.py, ví dụ:

def dfs_8_queens_steps():
def bfs_8_queens_steps():
def astar_8_queens_steps():
...

🧩 Mô tả giao diện

Giao diện sử dụng thư viện Pygame, hiển thị:

Bảng cờ bên trái: diễn tiến từng bước thuật toán.

Bảng cờ bên phải: lời giải cuối cùng (nếu tìm được).

Các nút bấm chọn thuật toán (DFS, BFS, A*, Hill, Genetic, v.v...).

Hai nút điều khiển đặc biệt:

Steps: in ra các bước trên terminal.

Skip: tua nhanh đến kết quả cuối.

▶️ Hướng dẫn chạy chương trình

Cài đặt các thư viện cần thiết:

pip install pygame


Chạy chương trình:

python 8Queens_23110090.py


Chọn thuật toán bạn muốn chạy (bấm nút trên giao diện).

Quan sát quá trình đặt quân hậu.

📸 Ảnh minh họa giao diện

<img width="1052" height="711" alt="image" src="https://github.com/user-attachments/assets/98434449-1445-4e22-a350-f69f87ef3d9a" />

