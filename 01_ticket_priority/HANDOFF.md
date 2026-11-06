# Handoff — Bài 01: ticket priority

Cập nhật ngày 06/11/2026 theo backend có đủ bốn route nghiệp vụ. Các mục ngày 03–04/11 bên dưới ghi lại lịch sử.

## Trạng thái hiện tại

- `extract` gọi ChatOpenAI với structured output rồi lưu email gốc và bản AI trong một transaction. Backend giữ `id` và `received_at`, chỉ gửi `message` cho model. Việc backend giữ ID là lựa chọn của bài làm hiện tại, khác với mẫu JSON trong đề có ID ở output AI.
- `confirm` đọc giờ nhận gốc từ DB, tính khóa bằng `cal_priority()`, lưu bản người dùng duyệt vào `ticket_confirmed` và thêm khóa vào heap sau commit. Bản AI vẫn nằm ở `ticket`.
- `queue` dùng `heapq.nsmallest()` để xem top K. `next` ghi `dequeued_at` trước khi pop. Khi khởi động, `lifespan` chỉ nạp bản xác nhận còn chờ và gọi `heapify()`. [Route và lifecycle](app/main.py) · [ORM](app/model_db.py) · [SLA và khóa ưu tiên](app/algorithm.py)
- Backend dùng một Session SQLAlchemy mỗi request. Heap trong RAM của một process. Theo lựa chọn của Tri, các thao tác hàng đợi hiện dùng tuần tự, chưa có cơ chế bảo vệ khi nhiều request thao tác heap cùng lúc.

## Đã kiểm chứng và cần làm tiếp

- Tri cho biết đã gọi `extract` lần đầu. Chưa có kết quả trong lượt này xác nhận toàn bộ luồng trên Supabase.
- Đã chạy kiểm tra cục bộ bằng FastAPI TestClient, SQLite tạm và model giả. Các ca đạt gồm hàng đợi rỗng trả 404, lấy đúng ticket đầu, lỗi commit giữ nguyên heap và DB, rồi restart vẫn loại ticket đã lấy. Kiểm tra này không gọi OpenAI hoặc Supabase và chưa nằm trong một bộ test lưu trong repo.
- Bước tiếp theo là kiểm tra kiểu `email.received_at` và cột `ticket_confirmed.dequeued_at` thực tế trên Supabase, rồi thử tuần tự `extract → confirm → queue → next → restart` bằng dữ liệu giả. [Lệnh chạy và cập nhật schema](README.md)
- Phần còn thiếu theo contract gồm test thuật toán tự động, xử lý ID trùng thành phản hồi rõ ràng và xử lý lỗi model. Bản hiện tại tính lại deadline từ dữ liệu đã lưu và ghi thời điểm lấy ticket, chưa lưu riêng kết quả SLA hoặc thời lượng xử lý. [Contract Bài 1](../develop-fastapi-from-scratch/references/exercise-contracts.md)

## Lịch sử 03–04/11/2026

### Tài liệu tại thời điểm bắt đầu

- [AGENTS.md](../AGENTS.md), [skill đồng hành](../develop-fastapi-from-scratch/SKILL.md): Tri tự code/chạy, AI giải thích và review từng phần nhỏ.
- [Contract](../develop-fastapi-from-scratch/references/exercise-contracts.md), phần chung và bài 01; [PDF gốc](../23-10-2026-01-01-30-bai-tap-structured-output-va-thuat-toan.pdf), trang 2–4.
- [README hiện tại](README.md): ghi chú của Tri đang hoàn thiện, chưa phải API contract hoàn chỉnh.
- [Nhật ký tư duy](NHAT_KY.md) ghi câu hỏi, giả định, phản hồi và các đính chính, đặc biệt mục 12–14.

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

## Bổ sung ngày 04/11/2026 — trạng thái đọc từ source hiện tại

Phần này cập nhật trạng thái mới; giữ nguyên nội dung ngày 03/11 ở trên để truy lại lịch sử. Không tiếp tục từ giả định main.py trống.

### Đã viết và đã đọc lại

- [app/main.py](app/main.py): create_app(settings), GET /api/health và POST /tickets/extract; cuối file gọi create_app(get_settings()). ChatOpenAI được tạo trong factory; extractor dùng with_structured_output(TicketExtracted). System prompt hiện là “Trích xuất thông tin ticket. Không thêm thông tin ngoài tin nhắn.”; human message chỉ chứa email.message.
- [app/model.py](app/model.py): TicketExtractIn có id/message min_length=1 và received_at AwareDatetime. TicketExtracted có intent/severity Literal, product cho null, summary max_length=200, needs_human_review bool. TicketExtractOut kế thừa TicketExtracted, thêm id/received_at. Route gán từng field để trả JSON phẳng; phương án response lồng đã trao đổi nhưng không dùng trong source hiện tại.
- [app/config.py](app/config.py): Settings đọc OPENAI_API_KEY, OPENAI_MODEL, DATABASE_URL qua dotenv/os.getenv. Chưa kiểm biến thiếu/rỗng; không đọc .env hay xác nhận giá trị thật.
- [app/database.py](app/database.py): Base kế thừa DeclarativeBase; make_session_factory trả engine và sessionmaker bind=engine, autoflush=False, expire_on_commit=False; engine có pool_pre_ping=True, connect_args rỗng. Chưa có type hint return.
- [app/model_db.py](app/model_db.py): Email (bảng email) có id, received_at, message. Ticket (bảng ticket) có id, received_at, intent, severity, product, summary, needs_human_review. Đây mới là khung ORM, chưa chứng minh đã tạo bảng.
- [requirements.txt](requirements.txt) hiện có dataclasses, dotenv, fastapi, uvicorn, pydantic, langchain-openai, sqlalchemy. Chưa rà môi trường cài thực tế; cần rà tên gói python-dotenv, dataclasses thuộc stdlib Python hiện đại, driver PostgreSQL phải khớp URL. Không ghi connection string thật vào tài liệu.

### Quyết định, khác biệt và bằng chứng

- Tri chọn LLM chỉ nhận message; backend giữ id/received_at. Không có ID trong output LLM để so khớp. Đây là điều chỉnh so với contract cục bộ liệt kê ticket_id trong output AI; contract chưa sửa. README vẫn dùng ticket_id, source dùng id: cần thống nhất, không tự đổi hộ.
- Tri cho biết đã tạo DB Supabase và có URL; đang hướng PostgreSQL/Supabase + SQLAlchemy sync. Chưa kiểm driver, URL, kết nối hay dữ liệu thực. SQLite trong phần cũ là đề xuất trước đây.
- Extract phải giữ nguồn và bản AI; confirm giữ bản người dùng riêng, không ghi đè bản AI. Extract chưa thêm queue; needs_human_review=false vẫn cần confirm theo flow đã thống nhất.
- [samples/post_ticket_extract.txt](samples/post_ticket_extract.txt) ghi bốn case do Tri cung cấp: billing/high, technical/critical, mơ hồ other + product=null + review=true, và lỗi timezone_aware khi thiếu timezone. Không có HTTP status/log để xác nhận toàn bộ quá trình. Response mẫu chưa có id/received_at nên chưa chứng minh response mới nhất đã chạy.
- Case 1 tự thêm “hoàn tiền/điều chỉnh” ngoài lời khách. Prompt hiện đã thêm chỉ dẫn không thêm thông tin, chưa có bằng chứng chạy lại. Severity chưa có tiêu chí chi tiết; không coi các mức trong mẫu là đáp án cố định. Chưa có test tự động.

### Khoảng trống cần review trước khi nối DB

- now_utc() đang bỏ tzinfo; hai received_at dùng DateTime chưa bật timezone và có default thời gian hiện tại. Cần lưu đúng thời điểm nhận từ request; với PostgreSQL chọn cột có timezone và kiểm round-trip, không thay received_at bằng lúc xử lý.
- Ticket.product là Mapped[str], theo mapping mặc định không cho null, trái với Pydantic và case mơ hồ. Cần cho phép null.
- Email/Ticket có id nhưng chưa có ForeignKey/relationship; chưa chốt cách ràng buộc nguồn–bản AI, xử lý ID trùng hoặc extract lại. Không coi mô hình hai bảng là thiết kế hoàn tất.
- Chưa có bản confirmed riêng, timestamp/thời lượng xử lý hoặc kết quả deadline. Khi thêm confirm phải bảo toàn bản AI.
- main.py chưa tạo/gắn engine/session_factory, chưa import ORM, chưa có get_db hoặc thao tác add/commit/rollback. lifespan đang pass và chưa gắn vào FastAPI; phải có yield trước khi dùng. Import ORM trước create_all.
- Chưa có timeout/lỗi upstream có kiểm soát, chưa chặn ID/message toàn khoảng trắng, chưa có confirm/queue/next/SLA/heap.

### Điểm tiếp tục

Trước tiên cùng Tri review model_db.py và để Tri tự sửa timezone, product nullable, rồi chốt liên kết nguồn–AI. Sau đó mới nối make_session_factory vào create_app, app.state, lifespan tạo bảng demo/dispose engine, get_db cấp Session mỗi request và transaction lưu nguồn + bản AI trước khi trả response.

Xong bước lưu extract khi: request tạo đủ nguồn/bản AI liên kết đúng trong Supabase; product=null lưu được; đọc lại giữ đúng thời điểm; lỗi ghi rollback toàn bộ; chưa vào queue. Đây là kiểm tra cần làm, chưa phải kết quả đã đạt.

Lượt này chỉ đọc và thêm tài liệu, không sửa code/README/requirements, không đọc .env hoặc gọi server/test/model/DB. Nhật ký đang dùng: [NHAT_KY.md](NHAT_KY.md); file tên ngày 03/11 được dẫn trong phần cũ không xuất hiện trong danh sách hiện tại.
