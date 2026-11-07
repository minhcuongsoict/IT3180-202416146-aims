# Lab 01 – Thiết lập môi trường & Refactor flow

- Sinh viên: <Bui Minh Cuong> – MSSV 202416146
- Repo: https://github.com/minhcuongsoict/it3180-202416146-aims

## Câu 1. Cấu hình `--global` được lưu ở đâu? Khác gì so với `--local`?

Git có ba mức cấu hình, mức hẹp hơn ghi đè mức rộng hơn:

| Mức | Tệp lưu | Phạm vi áp dụng |
|---|---|---|
| `--system` | `<thư mục cài Git>/etc/gitconfig` | Mọi người dùng trên máy |
| `--global` | `~/.gitconfig` (trên Windows: `C:\Users\<tên>\.gitconfig`) | Mọi repo của một người dùng |
| `--local` | `.git/config` bên trong từng repo | Chỉ repo đó |

Khi cùng một khóa được đặt ở nhiều mức, giá trị ở `--local` được ưu tiên,
sau đó đến `--global`, cuối cùng là `--system`. Vì vậy có thể đặt
`user.email` cá nhân ở mức global, nhưng đặt email công ty ở mức local cho
riêng repo công việc mà không ảnh hưởng các repo khác.

Lệnh `git config --list --show-origin` cho biết mỗi giá trị đến từ tệp nào:

```
$ git config --list --show-origin | grep user
<dán kết quả>
```

## Câu 2. Vì sao dùng `git mv`?

Git không lưu thông tin "đổi tên" một cách tường minh; nó chỉ lưu nội dung
của từng phiên bản và **suy ra** rename khi thấy một tệp biến mất và một tệp
mới có nội dung gần giống xuất hiện trong cùng commit.

`git mv` gộp hai việc: đổi tên tệp trên đĩa và stage thay đổi đó, nên Git
ghi nhận ngay là `renamed` (thấy được trong `git status`). Quan trọng hơn,
trong bài em tách thành hai commit: commit thứ nhất **chỉ di chuyển tệp**,
commit thứ hai mới sửa import trong `main.py`. Vì commit di chuyển không làm
thay đổi nội dung tệp, Git nhận diện rename với độ giống 100%. Nhờ đó:

- Lịch sử của tệp không bị đứt: `git log --follow` vẫn truy được về các
  commit trước khi đổi tên.
- Trên GitHub, tab *Files changed* hiển thị "File renamed without changes"
  thay vì xóa toàn bộ rồi thêm mới, giúp reviewer biết ngay đây chỉ là
  di chuyển và chỉ cần xem kỹ phần thay đổi thực sự (2 dòng import).

Nếu vừa di chuyển vừa sửa nhiều nội dung trong cùng một commit, Git có thể
không nhận ra rename và lịch sử tệp sẽ bị cắt đứt.

```
$ git log --oneline --follow -- aims/cart.py
<dán kết quả>
```

Commit `feat: add initial DVD, Cart and demo program` được tạo khi tệp còn
tên `cart.py` ở thư mục gốc, nhưng vẫn xuất hiện trong lịch sử của
`aims/cart.py`.

## Câu 3. `release/lab01` có phải baseline không?

Theo lý thuyết SCM, baseline là một phiên bản của cấu hình đã được xem xét,
thống nhất, làm cơ sở cho các bước tiếp theo và chỉ được thay đổi thông qua
quy trình kiểm soát thay đổi.

`release/lab01` thỏa mãn điều này ở mức quy trình: nó được tạo từ master sau
khi các thay đổi đã đi qua PR, đại diện cho bản nộp của Lab 01, và theo quy
ước của học phần thì không commit trực tiếp lên đó, mọi sửa đổi về sau phải
đi qua nhánh `hotfix/*` và Pull Request.

Tuy nhiên, về mặt kỹ thuật, nhánh trong Git chỉ là một con trỏ có thể di
chuyển: khi có hotfix, `release/lab01` sẽ trỏ sang commit mới. Do đó nó giống
một **dòng bảo trì** của bản phát hành hơn là một định danh bất biến. Để đánh
dấu baseline một cách chính xác, không thể thay đổi, cần dùng **annotated
tag** (ví dụ `v0.1.0` gắn vào commit đầu `release/lab01` ở Lab 04). Kết hợp
lại: nhánh release để bảo trì, tag để định danh baseline.

## Câu 4. Vì sao không commit thẳng lên master dù làm một mình?

1. **Truy vết thay đổi:** mỗi PR ghi lại mục đích, nội dung thay đổi và cách
   kiểm thử. Sau này nhìn lịch sử có thể biết vì sao một thay đổi xuất hiện,
   điều mà một commit đẩy thẳng lên master thường không có.
2. **Master luôn ở trạng thái chạy được:** thay đổi được hoàn thiện và kiểm
   tra trên nhánh riêng. Ví dụ trong bài, sau commit `git mv` chương trình
   bị lỗi `ModuleNotFoundError`; nhờ làm trên nhánh, trạng thái hỏng đó
   không bao giờ nằm trên master.
3. **Có điểm dừng để xem lại:** PR là lúc xem lại diff trước khi tích hợp
   (vai trò của CCB thu nhỏ). Nếu thấy sai chỉ cần không merge hoặc đóng PR,
   không phải hoàn tác trên nhánh dùng chung.
4. **Hình thành thói quen