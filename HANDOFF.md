# Handoff — chuẩn bị bài tập FastAPI

Ngày: 03/11/2026. Đã chuyển từ chuẩn bị tài liệu sang đồng hành phân tích bài 01; chưa triển khai bốn backend.

## Trạng thái mới nhất — bài 01

- Tri đã tự tạo README ghi flow và app/main.py. Đọc lại ở lần cập nhật này: main.py vẫn trống; README đã qua nhiều vòng review phần extract.
- Đọc [HANDOFF bài 01](01_ticket_priority/HANDOFF.md) để tiếp tục công việc; [nhật ký tư duy](01_ticket_priority/NHAT_KY_TU_DUY_2026-11-03.md) ghi câu hỏi, giả định, những điểm sửa và đính chính.
- Trọng tâm đã trao đổi: metadata đầu vào khác dữ liệu LLM trích xuất; bản nháp khác bản xác nhận; lưu nguồn và cả hai bản để đối chiếu; extract chưa thêm queue. Backend bổ sung received_at từ input vào response, không yêu cầu LLM tạo thời điểm này.
- Tri đã sửa mô tả extract. Bước tiếp theo đề xuất: phân biệt request / output LLM / response API, rồi Tri tự viết schema request từng phần nhỏ. Một số ý đã trao đổi chưa được ghi đầy đủ trong README; xem handoff bài 01, không tự sửa hộ.
- Chưa chạy backend/test/model, chưa xác minh dependency cho bài. DB/provider/cách cấp ID thực tế chưa chốt. Vẫn giữ nhịp Tri tự code và chạy.

Các kết quả kiểm tra tài liệu ở phần dưới là lịch sử giai đoạn chuẩn bị, không phải kiểm tra chạy lại trong lần cập nhật này. Những câu “bốn folder trống” chỉ đúng tại thời điểm chuẩn bị; bài 01 hiện đã có file của Tri.

## Mở từ đây

- [Điểm bắt đầu cho AI bất kỳ](AGENTS.md): vai trò, scope và thứ tự đọc; không yêu cầu cơ chế skill riêng.
- [Skill develop FastAPI từ đầu](develop-fastapi-from-scratch/SKILL.md)
- [Đối chiếu kiến thức/convention B1–B6](develop-fastapi-from-scratch/references/course-conventions.md)
- [Ví dụ mẫu cục bộ](develop-fastapi-from-scratch/references/course-examples.md): schema, settings, ORM/Session, app lifecycle, structured output, heap.
- [Bổ sung từ repo giảng viên](develop-fastapi-from-scratch/references/instructor-backend-guide.md): snapshot đã đọc, các pattern backend/test và ba ví dụ nhỏ; đủ ngữ cảnh ngay trong folder.
- [Contract, route, invariant, test bốn bài](develop-fastapi-from-scratch/references/exercise-contracts.md)
- [Đề gốc 8 trang](23-10-2026-01-01-30-bai-tap-structured-output-va-thuat-toan.pdf)

## Quyết định

- Tri tự tay tạo file, viết code/test và chạy lệnh from scratch. LLM đọc nguồn, giải thích, gợi ý theo từng bước nhỏ và review; không tự triển khai hoặc sửa code bài tập nếu chưa được nhờ rõ hành động đó.
- Backend và test; không frontend. Swagger/JSON thể hiện các bước xem, sửa, xác nhận.
- Bốn folder độc lập: `01_ticket_priority`, `02_dock_booking`, `03_expense_duplicates`, `04_task_dependencies`.
- Theo cấu trúc phẳng B5–B6; thêm algorithm.py/extractor.py để tách thuật toán khỏi AI/API.
- Đề xuất SQLite local + SQLAlchemy sync; test DB tạm. Đây là mặc định của skill, chưa phải lựa chọn DB được Tri chốt.
- Không bê auth, memory, agent loop hoặc requirements dư từ project mẫu.
- Bắt đầu bài 01 theo thứ tự đề; hoàn thành từng phần quan sát được trước khi sang bài tiếp.

## Lịch sử chuẩn bị — đã làm / chưa làm

Kiến thức B1–B6 cần dùng, coding style và ví dụ rút gọn đã được đưa vào references ngay trong folder này. Contract bốn bài và PDF gốc cũng ở đây. Không cần đọc lại học liệu ngoài folder hoặc lịch sử chat. Ví dụ minh họa được chỉnh cho rõ và dùng dữ liệu khác bài tập; chưa có backend làm sẵn. Các link web là nguồn bổ sung tùy nhu cầu, không phải điều kiện để đọc hiểu bộ hướng dẫn.

Chưa viết app, chưa cài dependency cho bốn bài, chưa chạy backend mới, chưa gọi model hoặc DB thật. Các folder bài mới chỉ là nơi Tri tự viết project sau này. Bộ tài liệu độc lập về ngữ cảnh; khi chạy code vẫn cần Python và dependency tương ứng, nhánh AI thật cần cấu hình provider/model hợp lệ.

Kiểm tra bàn giao đã đạt: định dạng skill hợp lệ; sao chép nguyên folder sang vị trí tạm rồi xác nhận 19 liên kết local trong 6 tài liệu đều tồn tại và nằm trong gốc mới; không còn đường dẫn ổ đĩa cố định. Đã thực thi offline 7 block Python minh họa trong môi trường có dependency, gồm assert mẫu và thử input sai cho schema/priority. Block model chỉ định nghĩa hàm, không gọi AI; block DB không mở kết nối. Bốn folder bài tập vẫn trống. Đây là kiểm tra tài liệu/ví dụ, không phải test backend bài tập hoặc kiểm chứng AI độc lập đã đọc hiểu.

## Lịch sử bổ sung tài liệu và gợi ý khởi đầu

Đã đối chiếu repo giảng viên tại commit `de350b94cc305347b6735e602607ef3f2f38170f` ngày 03/11/2026: README, factory, config, DB, dependencies, models/schemas, các route auth/task/chat, service AI/task, middleware và tests/requirements. Chỉ bổ sung tài liệu/ví dụ, không sao chép backend hoàn chỉnh hoặc triển khai bài tập. Repo dùng routers và OpenAI SDK trả text; bài mới vẫn giữ nhịp tự code và structured output theo đề. Source/tests repo chưa được chạy lại; không gọi AI/DB thật.

Kiểm tra sau bổ sung: skill hợp lệ; bản sao sang vị trí tạm có 7 tài liệu Markdown và 23 liên kết nội bộ đều ở trong gốc, không có đường dẫn ổ đĩa cố định. Tổng 10 block Python minh họa (7 cũ, 3 mới) thực thi offline và assert mẫu đạt. Bốn folder bài tập vẫn trống. Kết quả này cập nhật số lượng ở lần kiểm tra trước, không chứng nhận test repo giảng viên đã pass.

Yêu cầu gợi ý để dùng skill cục bộ:

> Đọc AGENTS.md trong folder này và các tài liệu cục bộ được dẫn, rồi đồng hành để mình tự code bài 01 trong 01_ticket_priority. Mình tự tạo file, viết code/test và chạy lệnh. Trước hết giúp mình hiểu input/output bằng một ví dụ nhỏ, rồi giao bước đầu tiên để mình tự làm; chờ mình gửi kết quả để review. Không viết sẵn lời giải hoặc sửa file bài tập. Chưa nối model thật.

Có thể chuyển nguyên folder cho AI khác. AI chỉ cần đọc AGENTS.md rồi tài liệu được dẫn; không cần cài skill toàn cục. Nếu công cụ không tự đọc file, cung cấp nội dung các file liên quan cho AI.

## Bổ sung ngày 04/11/2026 — extract đã viết, đang tích hợp DB

Phần bổ sung này cập nhật trạng thái; những mô tả main.py trống/chưa có schema ở trên là lịch sử ngày 03/11.

- Tri đã viết GET /api/health và POST /tickets/extract. Dùng ChatOpenAI + with_structured_output(TicketExtracted), chỉ gửi message cho LLM; backend ghép id và received_at vào response phẳng TicketExtractOut.
- Pydantic đặt trong model.py, ORM đặt trong model_db.py. Không tự đổi naming của Tri.
- Tri cho biết đã tạo DB Supabase và có DATABASE_URL. Source có engine/session factory và khung bảng Email/Ticket; chưa nối DB vào app hoặc kiểm chứng kết nối/lưu dữ liệu. SQLite ở phần trước chỉ là đề xuất cũ.
- samples/post_ticket_extract.txt có bốn request/kết quả do Tri ghi; chưa phải test tự động hay kết quả AI tự chạy lại. Case 1 thêm yêu cầu hoàn tiền/điều chỉnh ngoài nguồn. Prompt hiện có chỉ dẫn không thêm thông tin, chưa có mẫu chạy lại chứng minh đã sửa được lỗi.
- Bước tiếp theo: review model_db.py, đặc biệt timezone, product nullable và liên kết nguồn–bản AI; sau đó nối lifecycle/get_db và transaction lưu extract. Chưa có confirm/queue/next/SLA/heap.

Chi tiết: [HANDOFF bài 01](01_ticket_priority/HANDOFF.md), phần bổ sung ngày 04/11. Nhật ký hiện có là [NHAT_KY.md](01_ticket_priority/NHAT_KY.md); file tên NHAT_KY_TU_DUY_2026-11-03.md được dẫn trong phần cũ không xuất hiện trong danh sách file hiện tại.

Lượt này đọc lại code, config.py, requirements, README và samples; chỉ nối thêm tài liệu. Không đọc .env, sửa code, chạy server/test hoặc gọi OpenAI/Supabase.
