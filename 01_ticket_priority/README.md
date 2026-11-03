Tóm tắt yêu cầu phải làm:

# POST /tickets/extract
Input:  JSON
{
  "ticket_id": "T01",
  "received_at": "2026-11-03T16:00:00+07:00",
  "message": "Chào bạn, tôi gặp vấn đề khi thanh toán."
}
Output: Ticket(BaseModel) (ticket_id, received_at, intent, severity, product, summary, needs_human_review)
Flow:
- Đọc từng Email, gọi API sử dụng structure output đẻ fill "message" vào Ticket. Kiểm tra các trường hợp mơ hồ, output LLM sai:
    + Sai schema hay trường thông tin intent/severiy: Báo lỗi
    + Mơ hồ: needs_human_review=true
- Lưu nội dung gốc, metadata và bản AI trích xuất, giữ riêng với bản người dùng xác nhận để đối chiếu. (Yêu cầu chung số 4, trang 3)
- Trả bản Ticket do AI điền cho người dùng để duyệt bằng lệnh "POST /tickets/confirm"

# POST /tickets/confirm
Input: Ticket(BaseModel) từ bước trước
Output: None
Flow:
- Người dùng đọc và chỉnh info của tickets
- Lưu vào Database
- Lưu vào Queue

# GET /tickets/queue?limit=...
Input: limit hoặc None (để lấy hết)
Output: Queue
Flow:
- Show cho người dùng Queue

# POST /tickets/next
Input: None
Output: Ticket ở đầu Queue
Flow:
- Lấy Ticket đầu ở Queue
- Xóa ticket đó đi trong queue (có update lại Queue)
