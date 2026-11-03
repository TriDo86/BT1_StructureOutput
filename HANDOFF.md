# Handoff — chuẩn bị bài tập FastAPI

Ngày: 03/11/2026. Phạm vi lượt này: đọc nguồn và viết skill để bắt đầu bài tập, chưa triển khai bốn backend.

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

## Đã làm / chưa làm

Kiến thức B1–B6 cần dùng, coding style và ví dụ rút gọn đã được đưa vào references ngay trong folder này. Contract bốn bài và PDF gốc cũng ở đây. Không cần đọc lại học liệu ngoài folder hoặc lịch sử chat. Ví dụ minh họa được chỉnh cho rõ và dùng dữ liệu khác bài tập; chưa có backend làm sẵn. Các link web là nguồn bổ sung tùy nhu cầu, không phải điều kiện để đọc hiểu bộ hướng dẫn.

Chưa viết app, chưa cài dependency cho bốn bài, chưa chạy backend mới, chưa gọi model hoặc DB thật. Các folder bài mới chỉ là nơi Tri tự viết project sau này. Bộ tài liệu độc lập về ngữ cảnh; khi chạy code vẫn cần Python và dependency tương ứng, nhánh AI thật cần cấu hình provider/model hợp lệ.

Kiểm tra bàn giao đã đạt: định dạng skill hợp lệ; sao chép nguyên folder sang vị trí tạm rồi xác nhận 19 liên kết local trong 6 tài liệu đều tồn tại và nằm trong gốc mới; không còn đường dẫn ổ đĩa cố định. Đã thực thi offline 7 block Python minh họa trong môi trường có dependency, gồm assert mẫu và thử input sai cho schema/priority. Block model chỉ định nghĩa hàm, không gọi AI; block DB không mở kết nối. Bốn folder bài tập vẫn trống. Đây là kiểm tra tài liệu/ví dụ, không phải test backend bài tập hoặc kiểm chứng AI độc lập đã đọc hiểu.

## Bước tiếp theo

Đã đối chiếu repo giảng viên tại commit `de350b94cc305347b6735e602607ef3f2f38170f` ngày 03/11/2026: README, factory, config, DB, dependencies, models/schemas, các route auth/task/chat, service AI/task, middleware và tests/requirements. Chỉ bổ sung tài liệu/ví dụ, không sao chép backend hoàn chỉnh hoặc triển khai bài tập. Repo dùng routers và OpenAI SDK trả text; bài mới vẫn giữ nhịp tự code và structured output theo đề. Source/tests repo chưa được chạy lại; không gọi AI/DB thật.

Kiểm tra sau bổ sung: skill hợp lệ; bản sao sang vị trí tạm có 7 tài liệu Markdown và 23 liên kết nội bộ đều ở trong gốc, không có đường dẫn ổ đĩa cố định. Tổng 10 block Python minh họa (7 cũ, 3 mới) thực thi offline và assert mẫu đạt. Bốn folder bài tập vẫn trống. Kết quả này cập nhật số lượng ở lần kiểm tra trước, không chứng nhận test repo giảng viên đã pass.

Yêu cầu gợi ý để dùng skill cục bộ:

> Đọc AGENTS.md trong folder này và các tài liệu cục bộ được dẫn, rồi đồng hành để mình tự code bài 01 trong 01_ticket_priority. Mình tự tạo file, viết code/test và chạy lệnh. Trước hết giúp mình hiểu input/output bằng một ví dụ nhỏ, rồi giao bước đầu tiên để mình tự làm; chờ mình gửi kết quả để review. Không viết sẵn lời giải hoặc sửa file bài tập. Chưa nối model thật.

Có thể chuyển nguyên folder cho AI khác. AI chỉ cần đọc AGENTS.md rồi tài liệu được dẫn; không cần cài skill toàn cục. Nếu công cụ không tự đọc file, cung cấp nội dung các file liên quan cho AI.
