# Thông Tin Deploy — Checkpoint 5

> Điền file này sau khi deploy xong. `pytest tests/test_cp5.py` đọc file này
> để tìm địa chỉ service của bạn và gọi thử.
>
> **Chỉ ghi TÊN biến môi trường, tuyệt đối không dán giá trị token vào đây.**
> Repo này công khai — dán token vào là mất token.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Nguyễn Thị Kiều Trang |
| Mã học viên | 2A202601961 |
| Repo | https://github.com/Nguyentrangntkt/K4-Day12-2A202601961-NguyenThiKieuTrang |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | https://day12-chat-production-0175.up.railway.app |
| Platform | Railway |
| Ngày deploy | 10/08/2026 |

## Biến Môi Trường Đã Set Trên Cloud

Ghi tên biến và **nguồn giá trị**, không ghi giá trị:

| Biến | Đã set | Ghi chú |
|------|--------|---------|
| `PORT` | ✅ | platform tự gán |
| `API_TOKEN` | ✅ | đặt trong dashboard, không nằm trong repo |
| `REDIS_URL` | ✅ | Redis service riêng trên Railway |
| `BUCKET_CAPACITY` | ✅ | Đã set trên Railway |
| `REFILL_PER_MINUTE` | ✅ | Đã set trên Railway |
| `DAILY_BUDGET_USD` | ✅ | Đã set trên Railway |
| `LOG_LEVEL` | ✅ | Đã set trên Railway |

## Lệnh Kiểm Tra

Các lệnh dưới đây dùng trực tiếp Public URL ở trên:

```bash
# 1. Liveness — mong đợi 200 {"status":"ok"}
curl -i https://day12-chat-production-0175.up.railway.app/healthz

# 2. Readiness — mong đợi 200 {"status":"ready"} (đã nối được Redis)
curl -i https://day12-chat-production-0175.up.railway.app/readyz

# 3. Không có token — mong đợi 401 kèm header WWW-Authenticate
curl -i -X POST https://day12-chat-production-0175.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}'

# 4. Có token — mong đợi 200 kèm câu trả lời
curl -i -X POST https://day12-chat-production-0175.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "X-Client-Id: sv-test" \
  -d '{"message":"Deploy là gì?"}'

# 5. Rate limit — gọi 15 lần, những lần cuối phải trả 429
for i in $(seq 1 15); do
  curl -s -o /dev/null -w "%{http_code} " -X POST https://day12-chat-production-0175.up.railway.app/chat \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_TOKEN" \
    -H "X-Client-Id: sv-test" \
    -d '{"message":"test"}'
done; echo
```

## Kết Quả Chạy Thật

Dựa trên các lần kiểm tra live:

```
/healthz -> 200
/readyz -> 200
/chat không có token hợp lệ -> 401
/chat có Bearer token đúng -> 200
```

## Ảnh Chụp Màn Hình

Các ảnh evidence thực tế đang có trong repo:

- `screenshots/Ảnh chụp màn hình 2026-08-10 185758.png`
- `screenshots/Ảnh chụp màn hình 2026-08-10 185846.png`
- `screenshots/Ảnh chụp màn hình 2026-08-10 195524.png`
- `screenshots/Ảnh chụp màn hình 2026-08-10 195638.png`
