# Đối chiếu kiến thức và convention

Bản rút gọn từ học liệu đã đọc ngày 03/11/2026. Kiến thức cần thiết đã nằm trong file này và [ví dụ mẫu cục bộ](course-examples.md); không cần source khóa học ở folder khác hoặc lịch sử chat. Đây là tổng hợp từ học liệu, không chứng nhận Tri đã thành thạo hoặc mọi project cũ chạy được.

Tri đã cung cấp thêm repo hướng dẫn backend của giảng viên. Xem [bản bổ sung cục bộ](instructor-backend-guide.md) cho APIRouter, response model, cấu hình và test đầy đủ hơn. Các mô tả lỗi/thiếu bên dưới nói về snapshot local B5–B6 đã đọc trước đó, không mặc định áp cho repo bổ sung; repo mới đã có current_user, response schema, test và bool config.

## Kiến thức kế thừa

| Buổi | Nội dung đã xuất hiện | Dùng cho bài mới |
|---|---|---|
| B1 | Client API, dotenv/os.getenv, messages system/user, response; giao diện Streamlit riêng | Env → client → messages → response; API key giữ backend. Không cần Streamlit. |
| B2 | ChatOpenAI/ChatGroq, invoke, ChatPromptTemplate, prompt nối model; MessagesPlaceholder và lịch sử theo session_id | Gọi model theo message/prompt; không cần memory/session chat cho trích xuất một lần. Lịch sử cần gửi lại hoặc nạp từ kho lưu; dict RAM mất khi dừng app. |
| B3 | Movie với title/year/director/rating; Actor lồng trong list cast; with_structured_output và include_raw | BaseModel/Field, schema lồng. JSON đúng khuôn chưa bảo đảm đúng sự thật. Parser PDF text không phải OCR ảnh scan. Xem ví dụ 1/5. |
| B4 | Schema tham số → hàm Python → wrapper @tool; bind_tools đề xuất lời gọi, chương trình thực thi rồi trả ToolMessage theo tool_call_id | Hàm thuần, kiểm dữ liệu, dict/Counter/sort/heapq. Không cần wrapper hoặc agent loop cho bài mới. Xem ví dụ 6. |
| B5–6 | Một project nối tiếp: đăng ký, đăng nhập, tạo/đọc task; 7 file app gồm main/config/schema/database/dependencies/model_db/security | Cấu trúc phẳng; dataclass Settings; create_app; lifespan; app.state; engine/sessionmaker; Depends(get_db); Pydantic khác ORM. Xem ví dụ 2–4. |

Luồng backend: JSON → Pydantic → endpoint → ORM Session → query hoặc add/commit/refresh → JSON. Engine quản lý kết nối/pool, sessionmaker tạo Session; get_db cấp Session theo request. LoginSession là bản ghi đăng nhập, không phải ORM Session. Pydantic kiểm request, ORM ánh xạ bảng/cột; Mapped không tự hash dữ liệu. create_app phải trả app; startup tạo bảng demo, shutdown dispose engine; model cần được import trước create_all.

B4 còn có Counter đếm category rồi sort `(-count, category)` lấy K nhóm: đây là tần suất, không phải tổng tiền. Hàm duplicate_claims dùng Decimal kiểm tiền hữu hạn/không âm và dict nhóm ID. Hàm free_slots đổi HH:MM thành phút, sort/merge khoảng chồng/chạm, cursor không lùi để tìm gap. Các khác biệt với bài tập mới nằm ở phần cuối tài liệu này.

Project mẫu B1–3 có chia routers/services/schemas thành thư mục. B5–6 gần mức tự viết từ đầu hiện tại hơn: chỉ 7 file Python trong `app`. Vì vậy chọn cấu trúc phẳng và thêm `algorithm.py`/`extractor.py` có lý do cụ thể; không mặc định bê toàn kiến trúc project mẫu lớn.

## Dùng kiến thức cũ để đồng hành

Đây là bản đồ những gì xuất hiện trong học liệu, không phải xác nhận Tri đã thành thạo. Khi giải thích một bước mới, chỉ rõ nó nối với phần nào đã học; nếu chưa rõ cách hiểu của Tri, dùng một ví dụ/câu hỏi nhỏ ngay tại bước đó.

- **Gọi AI:** liên hệ B1 messages và B2 invoke; chỉ cần một lần trích xuất, không mang chat memory vào bài. Trước tích hợp, Tri cần giải thích input gửi model và output nhận về.
- **Structured Output:** liên hệ Movie/Actor ở B3 để Tri tự định nghĩa schema nghiệp vụ. Phân biệt Field description với điều kiện validation và phân biệt JSON đúng khuôn với dữ liệu đúng nghĩa.
- **Thuật toán:** liên hệ hàm Python thuần ở B4, cùng Tri trace vài phần tử bằng tay rồi mới tự viết hàm. Chỉ ra luật bài mới khác notebook; không đưa nguyên hàm notebook thành đáp án.
- **FastAPI:** bám B5–B6 để trace JSON → Pydantic → endpoint → kết quả; Tri tự tạo app nhỏ và thử health trước khi ghép nhiều module.
- **Database:** giải thích riêng engine, session factory, Session từng request và ORM model bằng code B5–B6; sau đó mới hướng dẫn Tri tự nối Depends/get_db và transaction. Không coi Session DB là phiên đăng nhập.
- **Phần bổ sung:** pytest/fixture, response model riêng, audit history, timezone round-trip, transaction chống booking trùng và topological sort cần được giới thiệu khi dùng; không giao như kiến thức Tri mặc nhiên đã biết.

Coding style ưu tiên gần source B5–B6: file nhỏ, hàm dễ đọc, type hint và tên rõ nghĩa. Nếu đề xuất một cách khác bài học (ví dụ def thay async def khi dùng thư viện sync), giải thích lý do trong đúng bước đang làm. Chưa cần dạy toàn bộ convention trong một lượt.

## Có trong nguồn và đề xuất thêm

| Đã thấy trong B5–6 | Đề xuất cho bài mới |
|---|---|
| `main.py`, `schema.py`, `model_db.py`, `config.py`, `database.py`, `dependencies.py` | Giữ tên/vai trò để dễ đọc nối tiếp. |
| create_app(settings), lifespan, `app.state.engine/session_factory/settings` | Giữ pattern; cho test truyền cấu hình tạm và giả lập extractor. |
| Session theo request, add/commit/refresh, select/db.get | Giữ với DB local, rollback lỗi và kiểm transaction nghiệp vụ. |
| field_validator normalize name/email có return | Giữ nguyên tắc validator trả dữ liệu; thay bằng schema đúng bài. |
| Có route đặt trong create_app, prefix `/api` | Route vẫn có thể ở create_app; bài mới theo path PDF để dễ đối chiếu. |
| Chưa có response model riêng, test gốc hoặc README trong B6 | Thêm response model, pytest, TestClient, samples, README vì đầu ra bài tập cần kiểm được. |
| Source có register/login, Argon2/session cookie | Không cần mang auth sang bốn bài nếu không có requirement. |

Naming/import/type hints được chuẩn hóa trong skill là khuyến nghị, không phải coding standard chính thức do giáo viên công bố. Code lớp có import thừa, comment tạm và cách đặt tên chưa đều; không nên coi mọi dòng đang có là convention cần giữ.

## Những chỗ cần tránh học theo máy móc

- B5/B6 `main.py`: bắt toàn bộ IntegrityError thành email trùng; lỗi NOT NULL hoặc constraint khác sẽ bị che. Skill mới yêu cầu phân loại đúng lỗi.
- B6 `main.py`: async route đăng ký/đăng nhập gọi SQLAlchemy sync. Với bài nhỏ dùng def nhất quán sẽ dễ hiểu hơn, không cần thêm AsyncSession.
- B6 `config.py`: dataclass khai báo type không tự validate env; `int(os.getenv(...))` có thể lỗi nếu thiếu. Chỉ giữ env thật sự dùng, kiểm điều kiện ngay khi cần.
- B6 `config.py/main.py`: COOKIE_SECURE là chuỗi nhưng truyền vào boolean cookie option; không sao chép cả module config không liên quan.
- B6 `model_db.py`: `created_by_id` là datetime thực tế, không phải FK user. Tên trường mới phải đúng nghĩa.
- B6 `model_db.py`: now_utc bỏ tzinfo. Ticket và lịch kho của đề yêu cầu timezone, nên cần strategy lưu/đọc rõ ràng và test round-trip.
- B6 task routes chưa kiểm cookie/current user; không dùng làm bằng chứng auth hoàn chỉnh. Bài mới không cần triển khai auth để bù thiếu sót của bài cũ.
- Comment lifespan là cache/refresh session không mô tả đúng cơ chế: startup tạo bảng, shutdown dispose engine; mỗi request mới có ORM Session.
- Requirements B5–6 chưa pin và có dependency AI dù source chưa gọi model. Chỉ thêm phần cần và ghi phiên bản đã test trong môi trường mới.

## Notebook B4 không phải đáp án bốn bài

1. `duplicate_claims` gom `(vendor, invoice, amount)`; đề mới ưu tiên currency + receipt, thêm currency + vendor + invoice, vẫn gắn cờ khi tiền khác. Thay khóa, không dùng nguyên hàm.
2. `free_slots` dùng HH:MM, khung 09:00–17:00 và trả mọi khoảng trống; đề kho dùng datetime có timezone, 08:00–18:00, lọc loại cửa, chọn sớm nhất và xác nhận tránh tranh chấp.
3. `select_priority_tasks` dùng `(due_days, -urgency, effort_minutes, task_id)` và top K trên một danh sách; bài ticket dùng deadline SLA thật và hàng đợi có thao tác thêm/lấy.
4. Không tìm thấy topological sort của bài 04 trong các notebook B4 đã đọc. Đây là thuật toán cần giải thích mới, không ghi rằng Tri đã học đầy đủ.

## Nguồn web bổ sung, không bắt buộc để bắt đầu

- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/): TestClient, pytest và request JSON dùng cho test API.
- [Pydantic validators](https://pydantic.dev/docs/validation/latest/concepts/validators/): validator cần trả giá trị đã kiểm tra.
- [LangChain model structured output](https://docs.langchain.com/oss/python/langchain/models#structured-output): dùng schema trực tiếp trên model, phù hợp B3; không cần chuyển sang create_agent.

Các link được đối chiếu ngày 03/11/2026 và chỉ phục vụ kiểm tra API thư viện lúc cần; bộ hướng dẫn cục bộ đủ để bắt đầu offline. Chưa xác nhận provider/model hoặc bộ dependency nào chạy trong bài mới. Khi tích hợp nhánh thật, kiểm phiên bản/model thực tế.
