# Phiếu Phản Ánh — K4 Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: dùng lời của mình và dựa trên code đã quan sát được.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Nguyễn Thị Kiều Trang
> Mã học viên: 2A202601961

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `api_token` không có giá trị mặc định nên app chết ngay khi
khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà việc
"chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Theo em, fail fast giúp phát hiện lỗi cấu hình ngay lúc khởi động. Ví dụ, Railway quên đặt `API_TOKEN` thì app dừng và log lỗi cấu hình ngay, không nhận request rồi mới phát hiện. Nếu để mặc định `"changeme"`, app vẫn chạy và người khác có thể đoán hoặc dùng token đó, gây mất an toàn và có thể phát sinh chi phí.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/chat` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Mình chạy app local với `REDIS_URL=fake://`, gọi `POST /chat` với `X-Client-Id: sv-test-cp2` và nhận HTTP 200. Dòng log thật thu được là: `{"event": "chat_completed", "severity": "INFO", "ts": "2026-08-10T13:26:12.636814+00:00", "client_id": "sv-test-cp2", "prompt_tokens": 3, "completion_tokens": 41, "usd_cost": 2.505e-05}`. Từ dòng này mình có thể lọc theo sự kiện hoặc client, biết request đã xong, đồng thời theo dõi token và chi phí. JSON cũng có `severity` viết hoa nên công cụ log có thể lọc mức độ; `print` chỉ nói chung chung là đã xong nên khó lọc và thống kê.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t chat:single .
docker build -t chat:multi .
docker images | grep chat
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) |287 MB disk usage, content khoảng 67.9 MB|
| Multi-stage | 270 MB disk usage, content khoảng 63.7 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> Kết quả mình đo được cho thấy multi-stage nhỏ hơn bản 1-stage: disk usage giảm từ 287 MB xuống 270 MB, còn content giảm từ khoảng 67.9 MB xuống 63.7 MB. Theo mình, phần chênh lệch đến từ việc bản multi-stage chỉ copy dependency cần chạy sang stage runtime, không mang theo các file build và thành phần dư thừa của stage cài đặt. Vì vậy image nhẹ hơn và thời gian build/deploy cũng tốt hơn.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Với Dockerfile hiện tại, Docker chép `requirements.txt` rồi mới chạy `pip install`, nên khi mình chỉ sửa một dòng trong `app/main.py`, các layer cài thư viện vẫn được dùng lại từ cache; chỉ phần chép source và các bước sau đó cần chạy lại. Nếu đặt `COPY . .` trước `pip install`, mọi thay đổi trong source có thể làm mất cache của layer đó, khiến Docker cài lại toàn bộ dependency và build chậm hơn.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Nếu app chạy bằng root và có lỗ hổng, kẻ tấn công có thể thoát khỏi phạm vi ứng dụng với quyền root trong container, rồi tìm cách khai thác tiếp để tác động đến host hoặc tài nguyên khác. Trong Dockerfile mình tạo user `appuser` có UID 10001 và đặt `USER appuser`, nên kể cả khi app bị khai thác thì quyền ban đầu cũng bị giới hạn, làm giảm mức độ thiệt hại.

---

### Câu 6 — Bearer token (CP3)

Vì sao 401 phải kèm header `WWW-Authenticate: Bearer`? Và vì sao ta trả **cùng
một** thông báo lỗi cho cả ba trường hợp (thiếu header, sai scheme, sai token)
thay vì nói rõ sai ở đâu cho người dùng dễ sửa?

> Header này cho client biết server yêu cầu kiểu xác thực Bearer khi trả về 401, đúng với quy ước HTTP. Mình dùng cùng thông báo `invalid or missing bearer token` cho thiếu header, sai scheme và sai token để không tiết lộ request sai ở bước nào. Nếu nói rõ “sai token” hay “thiếu header”, người đang dò endpoint có thể dùng thông tin đó để tìm cách tấn công dễ hơn.

---

### Câu 7 — Token bucket (CP3)

Với `capacity=10`, `refill_per_minute=10`: một client im lặng 10 phút rồi gửi
liên tiếp. Nó gửi được bao nhiêu request trước khi bị 429? Nếu bỏ đoạn
`min(capacity, ...)` trong `available()` thì con số đó thành bao nhiêu, và tại sao?

> Xô ban đầu có 10 token. Sau 10 phút, tốc độ nạp là 10 token/phút nhưng `min(capacity, ...)` giữ số token tối đa ở 10, nên client gửi được 10 request liên tiếp trước khi request thứ 11 bị 429. Nếu bỏ `min`, xô sẽ có 110 token (10 ban đầu cộng 100 token sau 10 phút), vì vậy client có thể gửi 110 request liên tiếp và làm mất ý nghĩa giới hạn burst của `capacity`.

---

### Câu 8 — Ngân sách theo ngày (CP3)

So sánh hạn mức $30/tháng với hạn mức $1/ngày cho cùng một client. Giả sử có sự
cố khiến một client gọi liên tục từ 2h sáng. Với mỗi cách, thiệt hại tối đa là
bao nhiêu và service tự hồi phục khi nào?

> Với hạn mức 30 USD/tháng, một sự cố kéo dài có thể làm mất gần hết 30 USD trước khi có người phát hiện; hạn mức chỉ tự mở lại theo chu kỳ tháng tiếp theo. Với hạn mức 1 USD/ngày, thiệt hại tối đa theo thiết kế là khoảng 1 USD cho client trong ngày đó. Sang ngày UTC mới, key chi phí đổi theo ngày nên service tự cho dùng lại phần ngân sách mới, đồng thời dữ liệu cũ còn TTL để theo dõi ngắn hạn.

---

### Câu 9 — /healthz khác /readyz (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Nếu `/healthz` cũng kiểm tra Redis, khi Redis mất kết nối thì cả ba container đều có thể trả lỗi health check. Load balancer tưởng cả ba instance đều hỏng, lần lượt loại chúng khỏi traffic hoặc khởi động lại, dù process ứng dụng vẫn còn sống. Với code hiện tại, `/healthz` chỉ kiểm tra process và trả 200; `/readyz` mới gọi `store.ping()`, trả 503 khi Redis không sẵn sàng. Cách tách này giúp hệ thống không biến lỗi dependency tạm thời thành restart cả cụm.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Mình từng phải kiểm tra lại cấu hình deploy vì cloud cấp `PORT` động, trong khi chạy local thường dùng cổng 8000. Mình đọc log Railway và kiểm tra health check để thấy app phải bind `0.0.0.0` và đọc `${PORT:-8000}` trong lệnh chạy. Sau đó cấu hình health check về `/healthz`, đặt `REDIS_URL` tới Redis service trên Railway và kiểm tra lại `/healthz`, `/readyz`, `/chat`; service đã chạy được trên public URL.
