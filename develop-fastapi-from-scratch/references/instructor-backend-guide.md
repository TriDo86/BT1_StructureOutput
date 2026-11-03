# Bổ sung từ hướng dẫn backend của giảng viên

Đối chiếu ngày 03/11/2026 với repo Real-world-Codespace/backend-fastapi-intro, commit `de350b94cc305347b6735e602607ef3f2f38170f` (commit ngày 25/10/2026). Đây là nguồn được Tri cung cấp bổ sung; không đồng nhất nó với snapshot code B5–B6 đã đọc trước đó.

Nội dung cần dùng đã được tóm tắt ngay trong file này. Các URL ở cuối chỉ để truy nguyên, không bắt buộc truy cập để bắt đầu học. Không clone project giảng viên vào folder bài tập, không dùng nó làm bài nộp của Tri.

## 1. Bản đồ project tham khảo

Repo có một ứng dụng quản lý công việc và chatbot; Python 3.11+ theo README. Ngoài backend còn có giao diện thử API, nhưng bốn bài của Tri vẫn chỉ backend/test.

| Thành phần repo | Trách nhiệm | Cách dùng khi đồng hành với Tri |
|---|---|---|
| main.py | create_app(settings=None), lifespan, app.state, include_router | Cho Tri hiểu điểm lắp ráp ứng dụng; factory cho phép test truyền settings riêng. |
| routers/auth, tasks, chat, system | Nhóm route theo chức năng, APIRouter có prefix/tags | Giới thiệu sau khi Tri đã hiểu route nhỏ; không phải điều kiện để viết health đầu tiên. |
| schemas.py | Request và response Pydantic | Phân biệt input/output, validation và serialization từ ORM. |
| models.py | ORM SQLAlchemy, enum trạng thái/ưu tiên, quan hệ user/task | Không nhầm schemas với bảng DB; không cần bê mô hình user vào bốn bài. |
| database.py | Base, engine, session factory; chọn driver và SQLite connect_args | Giữ rõ engine/factory/Session; giải thích cấu hình DB theo backend thực tế. |
| dependencies.py | get_db và current_user | Depends cung cấp tài nguyên hoặc kiểm điều kiện trước khi route xử lý. |
| task_service.py | Truy vấn chỉ các task user được xem; kiểm task có thể truy cập | Hàm dùng chung có lý do khi nhiều route cần cùng quy tắc. Không tự tạo repository layer. |
| ai_service.py | Provider thật/demo, chuẩn bị context, gọi AI | Tách model khỏi route để fake khi test; demo phải nói rõ không gọi LLM. |
| tests/test_app.py | Settings/DB tạm, TestClient, fake provider, monkeypatch | Test hành vi quan sát được, không lệ thuộc API key thật. |

Luồng đọc hiểu: request → route đã đăng ký → Pydantic và Depends kiểm input/tài nguyên → hàm nghiệp vụ/query → response model → JSON. Không hiểu đây là cam kết thứ tự cứng giữa mọi bước nội bộ validation/dependency.

### Chọn cấu trúc cho bài tự code

Giữ schema.py/model_db.py và route trong create_app khi bài còn nhỏ, đúng lựa chọn hiện tại. Nếu Tri muốn theo repo hoặc main.py có nhiều nhóm route, chuyển sang APIRouter theo từng phần sau khi đã hiểu, giữ nguyên URL và test. Repo gọi file là schemas.py/models.py; đây là khác biệt naming, không cần đổi tên file bài đã viết. Không bắt buộc thêm toàn bộ router/service/middleware từ đầu.

## 2. Những pattern nên đưa vào lúc cần

**Cấu hình:** Settings có default SQLite, cookie_secure là bool; get_settings dùng default cho getenv và chuyển chuỗi bool bằng so sánh với "true". Bản local B6 trước đó có chuỗi COOKIE_SECURE và int có thể nhận None; không mô tả lỗi đó như thể repo mới cũng giống hệt. Pattern env cần kiểm giá trị hợp lệ theo config thực dùng; default không thay mọi validation.

**SQLite/driver:** repo dùng check_same_thread=False cho URL SQLite và chọn psycopg 3 từ URL postgres/postgresql. Cho phép sử dụng SQLite khác thread không có nghĩa một ORM Session an toàn để chia sẻ đồng thời. Bài học vẫn Session riêng theo request. Đổi URL không tự chuyển dữ liệu SQLite sang PostgreSQL; create_all chỉ tạo bảng thiếu, không thay migration.

**Response model:** route list trả list[TaskOut], create trả TaskOut với 201, delete 204. TaskOut dùng ConfigDict(from_attributes=True) để đọc field từ ORM object. Output schema giới hạn field công khai, không trả trực tiếp password_hash/token. Khi sửa/xác nhận JSON trong bài mới, input và output có thể có trường khác nhau.

**Cập nhật một phần:** repo lấy `payload.model_dump(exclude_unset=True)` để phân biệt field chưa gửi với field được gửi null. Có kiểm từng field có được null không. Chỉ copy exclude_unset mà không có luật null sẽ tạo hành vi sai. Bốn bài không cần thêm PATCH chỉ để luyện pattern này; dùng khi phần người dùng sửa dữ liệu cần phân biệt tương tự.

**Dependency:** get_db mở/đóng Session bằng with/yield. current_user đọc cookie, kiểm token hash, hạn phiên và user tồn tại. Repo mới có xác thực này; snapshot local trước đó chưa có. Kiến thức cần nhớ là kiểm ở backend trước dùng dữ liệu; auth không nằm trong scope bốn bài trừ khi Tri yêu cầu.

**Tách provider và test:** app.state.chat_provider được gán provider thật/demo rồi test có thể thay bằng fake. Fake nhận input, ghi nhận tham số và trả kết quả cố định; test kiểm dữ liệu thật sự đưa vào provider. Khi áp dụng bài mới, gọi nó là extractor, dùng cùng output schema của phần trích xuất; không chỉ fake câu trả lời chat rồi coi đã test structured output.

**Lifespan:** factory nhận Settings của test; fixture dùng SQLite file dưới tmp_path. Trong repo có test tạo bảng thủ công và test riêng dùng with TestClient(app) để chứng minh startup tạo bảng. Bài mới nên dùng context manager cho API test để kiểm đúng lifespan và teardown, không chỉ gọi create_all thủ công thay startup.

## 3. AI trong repo khác AI trong bài tập

Repo dùng OpenAI SDK trực tiếp qua Responses API để tạo câu trả lời text, có timeout=20 giây và max_retries=1 trong source được đọc. Không có LangChain with_structured_output trong nhánh này. Những con số đó là cấu hình của mẫu, không phải yêu cầu bài tập hoặc hướng dẫn chọn model hiện hành.

Provider demo nói rõ không gọi LLM. Nhánh thật thiếu key trả 503; lỗi dịch vụ hoặc reply rỗng được xử lý thành lỗi, không fallback im lặng sang demo. Backend lọc task được phép xem trước khi gửi context. Prompt phân biệt dữ liệu task/history với chỉ thị; nhưng prompt không thay validation/quyền truy cập bằng code.

Bốn bài cần **trích xuất dữ liệu theo schema rồi Python tính kết quả**. Vẫn ưu tiên with_structured_output đã học ở B3; không đổi sang chatbot text hoặc thêm lịch sử chat vì thấy repo có. Chỉ giữ pattern provider riêng, mock rõ ràng, giới hạn dữ liệu và lỗi có thể quan sát được. Model/key thật phải kiểm tại lúc Tri tích hợp; tài liệu này không chứng nhận model mặc định trong repo còn dùng được.

## 4. Ví dụ nhỏ bổ sung cho AI dùng khi giải thích

Các block độc lập, được viết lại với dữ liệu sách, không chép toàn project giảng viên và không phải lời giải bài tập. Chỉ đưa ví dụ cho Tri khi cần.

### Đọc object bằng schema output, loại field không công khai

```python
from types import SimpleNamespace
from pydantic import BaseModel, ConfigDict


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str


record = SimpleNamespace(id=1, title="Sách mẫu", internal_note="Chỉ dùng nội bộ")
public = BookOut.model_validate(record).model_dump()
assert public == {"id": 1, "title": "Sách mẫu"}
```

Schema đọc attribute của object, chỉ xuất field công bố. from_attributes không làm input tự đáng tin và không tự kiểm quyền truy cập.

### Phân biệt chưa gửi và gửi null

```python
from pydantic import BaseModel


class BookEdit(BaseModel):
    note: str | None = None


assert BookEdit().model_dump(exclude_unset=True) == {}
assert BookEdit(note=None).model_dump(exclude_unset=True) == {"note": None}
assert BookEdit(note="Mới").model_dump(exclude_unset=True) == {"note": "Mới"}
```

Ví dụ cho phép xóa note bằng null; trường khác có thể không được null. Tri cần tự chốt luật trước khi dùng pattern.

### APIRouter tối thiểu, không cần database hoặc model thật

```python
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/health")
def health():
    return {"status": "ok"}


app = FastAPI()
app.include_router(router)
with TestClient(app) as client:
    assert client.get("/books/health").json() == {"status": "ok"}
```

Khi tách file, router ở module riêng, main import rồi include_router. Prefix và path nối thành URL; không vô tình thêm /api vào endpoint đề bài. Đây là ví dụ giảng giải một khái niệm, không yêu cầu Tri tạo tất cả routers ngay.

## 5. Giới hạn cần hiểu đúng

- Source register vẫn bắt mọi IntegrityError thành email trùng; không copy cách thông báo này thành quy tắc chung cho DB.
- now_utc trong repo lưu UTC bỏ tzinfo cho SQLite. Bốn bài yêu cầu datetime có múi giờ nên cần strategy rõ ràng và test round-trip; không copy rồi làm mất ý nghĩa thời điểm.
- Requirements repo có khoảng phiên bản cho FastAPI/Pydantic/SQLAlchemy/pytest và nhiều gói phục vụ auth/chat. Chỉ lấy dependency thực cần; bộ đã đọc chưa được cài/chạy lại để chứng nhận tương thích.
- Test repo thể hiện cách tổ chức và các kỳ vọng, không phải bằng chứng test đã pass trong lượt đọc này. Có app mặc định được tạo lúc import; khi tự thiết kế bài mới cần tránh để test vô tình phụ thuộc cấu hình thật.
- Repo có auth, quyền user, static UI, origin middleware, rate limit chat. Chưa cần mang các chức năng đó vào bốn bài. SQLite/thread config không chứng minh booking không bị đặt trùng; transaction vẫn phải giải riêng theo contract bài 02.

## Nguồn truy nguyên, không phải dependency đọc tài liệu

- [README của snapshot](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/README.md): mục tiêu, Python 3.11+, cấu trúc, cách chạy và giới hạn.
- [main.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/main.py), [config.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/config.py), [database.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/database.py): factory, cấu hình, driver.
- [schemas.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/schemas.py), [routers/tasks.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/routers/tasks.py): response và cập nhật một phần.
- [dependencies.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/dependencies.py), [models.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/models.py), [task_service.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/task_service.py): Session, quyền truy cập, ORM.
- [ai_service.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/ai_service.py), [routers/chat.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/routers/chat.py): provider, demo và lỗi dịch vụ.
- [tests/test_app.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/tests/test_app.py), [requirements.txt](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/requirements.txt): cách test và phạm vi dependency.
- [routers/auth.py](https://github.com/Real-world-Codespace/backend-fastapi-intro/blob/de350b94cc305347b6735e602607ef3f2f38170f/app/routers/auth.py): giới hạn bắt IntegrityError nêu trên.
