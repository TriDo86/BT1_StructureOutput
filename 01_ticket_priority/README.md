# Bài 01 — Hàng đợi ưu tiên ticket

Backend FastAPI nhận tin nhắn hỗ trợ, dùng GenAI để tạo bản nháp, rồi cho người dùng duyệt. Python tính hạn xử lý (SLA) từ giờ nhận gốc và mức độ đã xác nhận. Hàng đợi đưa ticket có hạn gần nhất lên đầu.

## Chạy backend

Mở PowerShell tại thư mục `01_ticket_priority`. Dùng môi trường Python của bài hoặc tạo mới với Python 3.11 trở lên:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Tạo file `.env` ở thư mục này với ba biến. Điền giá trị thật trên máy của bạn:

```dotenv
OPENAI_API_KEY=<api-key>
OPENAI_MODEL=<ten-model>
DATABASE_URL=postgresql+psycopg://<user>:<password>@<host>:<port>/<database>
```

`DATABASE_URL` là chuỗi kết nối PostgreSQL của Supabase. Dùng tiền tố `postgresql+psycopg://` cho driver `psycopg` trong requirements. Giữ file `.env` ngoài Git.

Nếu đã có bảng `ticket_confirmed` từ bản trước, chạy câu lệnh sau trong SQL Editor của Supabase trước khi khởi động:

```sql
ALTER TABLE public.ticket_confirmed
ADD COLUMN IF NOT EXISTS dequeued_at timestamptz;
```

Với DB mới, app tạo các bảng còn thiếu khi khởi động. Với bảng `email` đã có, kiểm tra `received_at` thực tế là `timestamp with time zone`. `create_all()` giữ nguyên kiểu của cột có sẵn. Nếu cần chuyển dữ liệu cũ, xác định múi giờ của giá trị đã lưu trước khi đổi kiểu.

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Sau khi thấy `Application startup complete`, mở [Swagger UI](http://127.0.0.1:8000/docs). `GET /api/health` trả `{"status":"ok"}`.

## Luồng API

| Endpoint | Input | Kết quả |
|---|---|---|
| `POST /tickets/extract` | `id`, `received_at` có timezone, `message` | Lưu email gốc và bản nháp AI trong một transaction. Trả bản nháp cùng ID và giờ nhận. |
| `POST /tickets/confirm` | `id` và các field đã duyệt | Lưu bản duyệt riêng, tính khóa ưu tiên và thêm vào heap sau khi commit. Trả HTTP 200 với body `null`. |
| `GET /tickets/queue?limit=2` | `limit` là số nguyên từ 1 trở lên, mặc định 10 | Trả tối đa K phần tử theo thứ tự ưu tiên, mỗi phần tử là `[deadline_at, negative_severity_rank, received_at, ticket_id]`. Heap rỗng trả `[]`. |
| `POST /tickets/next` | Body trống | Lưu dấu đã lấy rồi bỏ ticket đầu khỏi heap. Trả `ticket_id` và `deadline_at`. Hàng đợi rỗng trả 404. |

Ví dụ body cho `extract`:

```json
{
  "id": "DEMO-T01",
  "received_at": "2026-11-04T09:00:00+07:00",
  "message": "Tôi dùng FujiDesk và bị tính phí hai lần cho cùng một gói."
}
```

Ví dụ body cho `confirm`. Dùng ID mới nếu ID mẫu đã có trong DB:

```json
{
  "id": "DEMO-T01",
  "intent": "billing",
  "severity": "high",
  "product": "FujiDesk",
  "summary": "Khách bị tính phí hai lần cho cùng một gói.",
  "needs_human_review": false
}
```

Backend giữ ID và thời điểm nhận. GenAI chỉ nhận nội dung tin nhắn. `confirm` lấy lại `received_at` từ DB và dùng severity người dùng chốt. `product` có thể là `null`. Nếu chưa có bản AI cho ID được confirm, API trả 404.

## SLA và dữ liệu lưu

| Severity | SLA | Rank |
|---|---:|---:|
| `critical` | 30 phút | 4 |
| `high` | 2 giờ | 3 |
| `medium` | 8 giờ | 2 |
| `low` | 24 giờ | 1 |

Khóa min-heap là `(deadline_at, -severity_rank, received_at, ticket_id)`. Ticket có hạn gần nhất đứng đầu. Nếu cùng hạn, xét severity cao hơn, rồi giờ nhận sớm hơn và cuối cùng là ID.

- `email` giữ tin nhắn và giờ nhận gốc.
- `ticket` giữ bản AI, liên kết tới `email` bằng cùng ID.
- `ticket_confirmed` giữ bản người dùng chốt, liên kết tới `ticket`. `dequeued_at IS NULL` nghĩa là còn chờ.

Khi khởi động, app dựng lại heap từ các bản đã xác nhận còn chờ trong DB. `next` chỉ bỏ phần tử khỏi heap sau khi ghi `dequeued_at` thành công.

## Thử nhanh

Chạy trên DB thử có hàng đợi trống để kết quả khớp với ví dụ.

1. Extract và confirm `DEMO-T01` với `high`, giờ nhận 09:00, hạn 11:00. Tạo thêm `DEMO-T02` với `critical`, giờ nhận 09:20, hạn 09:50. Dùng cùng ngày và offset `+07:00`.
2. Gọi `GET /tickets/queue?limit=1` hai lần. Cả hai lần phải thấy `DEMO-T02`.
3. Gọi `POST /tickets/next`. Kết quả phải là `DEMO-T02`. Kiểm tra dòng đó có `dequeued_at`, rồi restart và xác nhận hàng đợi chỉ còn `DEMO-T01`.

Bản này chạy một process và thử các thao tác hàng đợi tuần tự. Hai request `next` đồng thời có thể cùng đọc một ticket. Xem [HANDOFF](HANDOFF.md) để biết phạm vi kiểm chứng và phần còn thiếu.
