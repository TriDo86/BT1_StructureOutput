# Handoff — Bài 01: ticket priority

Cập nhật: 03/11/2026, sau các vòng review README phần extract.

## Đọc để tiếp tục

- [AGENTS.md](../AGENTS.md), [skill đồng hành](../develop-fastapi-from-scratch/SKILL.md): Tri tự code/chạy, AI giải thích và review từng phần nhỏ.
- [Contract](../develop-fastapi-from-scratch/references/exercise-contracts.md), phần chung và bài 01; [PDF gốc](../23-10-2026-01-01-30-bai-tap-structured-output-va-thuat-toan.pdf), trang 2–4.
- [README hiện tại](README.md): ghi chú của Tri đang hoàn thiện, chưa phải API contract hoàn chỉnh.
- [Nhật ký tư duy](NHAT_KY_TU_DUY_2026-11-03.md): câu hỏi, giả định, phản hồi và các đính chính, đặc biệt mục 12–14.

## Tiến độ đã kiểm tra

- Tri đã hiểu flow tổng thể và sửa README qua nhiều vòng, tập trung POST /tickets/extract.
- README có request mẫu `ticket_id`, `received_at` có timezone, `message`; response dự kiến gồm ID, thời điểm nhận và các field trích xuất.
- README đã đổi từ chỉ lưu final / DB hoặc table AI riêng sang lưu nguồn, metadata và bản AI, giữ riêng với bản nhân viên xác nhận để đối chiếu.
- `app/main.py` hiện trống khi đọc lại. Chưa có schema/thuật toán/API triển khai được kiểm chứng; chưa chạy server, test hoặc gọi model. Chưa kiểm tra dependency cho bài.
- Chỉ cập nhật tài liệu bàn giao và nhật ký trong lượt này; không sửa README/code của Tri.

## Cách hiểu đã trao đổi

- AI trích xuất, người dùng xác nhận, Python tính SLA/deadline và ưu tiên.
- Flow đang áp dụng: cả bản nháp có needs_human_review=false cũng cần confirm trước khi vào queue. Tri đã tự trả lời như vậy. PDF yêu cầu chung có bước xác nhận, nhưng không viết nguyên câu “tất cả ticket phải confirm”; AI đã đính chính việc trình bày suy luận như trích dẫn trực tiếp.
- Extract không thêm queue. Queue chỉ xem; next lấy khỏi queue nhưng không xóa bản ghi DB hoặc đồng nghĩa hoàn tất công việc.
- Heap ở RAM cho demo một process, DB lưu bền vững; restart dựng lại heap từ các ticket còn chờ. Đồng bộ DB–heap chưa được triển khai.
- Received_at là metadata đầu vào, không phải lúc gọi model hay confirm. Backend kiểm timezone và giữ thời điểm gốc; LLM không cần trả lại received_at. Response API có thể chứa trường này do backend bổ sung.

## Điểm cần làm rõ ở README/schema tiếp theo

README hiện vẫn chưa ghi rõ một số chi tiết đã trao đổi:

- Tách request / schema output LLM / response API; không hiểu toàn bộ response là do LLM điền.
- Kiểm ticket_id của LLM khớp input; sai schema hoặc ID thì báo lỗi, không trả bản nháp hợp lệ.
- Mơ hồ: intent=other và needs_human_review=true; product dựa trên nội dung, không biết thì null.
- Extract không thêm queue; dữ liệu hợp lệ mới trả bản nháp để duyệt.

Các phần confirm, queue, next mới là ghi chú ban đầu, chưa được review đầy đủ. Ví dụ `Output: None` của confirm và `limit hoặc None để lấy hết` chưa phải contract đã chốt. Không tự coi chúng là lỗi cần sửa hộ khi Tri chưa yêu cầu.

## Bước tiếp theo đề xuất

Giúp Tri xác định các field/type/ràng buộc của **schema request extract** trước; Tri tự tạo schema.py và viết từng phần, AI review rồi mới tiếp tục. Chưa đưa toàn bộ file lời giải, chưa nối model hoặc DB. Nếu Tri hỏi về chạy app trước, quay lại bài health đã giao: create_app trả app, GET /health, xem /docs; bài đó chưa hoàn thành.

Chưa chốt DB, cơ chế cấp ID thực tế, provider/model, error response, thiết kế bảng. Input giả qua Swagger và SQLite + SQLAlchemy sync là đề xuất. Giữ scope backend/test, chưa thêm frontend hoặc tích hợp email thật.
