# Nhật ký tư duy — Bài 01: hàng đợi ticket

Ngày: 03/11/2026.

Mục đích: để Tri và AI sau này xem lại các câu hỏi, giả định, thay đổi trong cách hiểu và bước thực hành đang dở. Đây là bản biên tập theo cuộc trao đổi, không phải transcript nguyên văn toàn bộ. Câu hỏi được giữ sát lời Tri, lược lỗi gõ/định dạng; phản hồi AI được tóm tắt. Không coi một gợi ý hoặc một câu chưa được Tri trả lời là quyết định đã chốt.

## 1. Nạp ngữ cảnh và xin bản đồ tổng thể

**Tri hỏi:** “Tôi cần bạn đọc những thông tin cần thiết trong folder này để bắt đầu.” Sau đó: “Tôi chưa biết bắt đầu từ đâu, hãy chỉ tôi step by step để làm bài tập 1 nhé. Bây giờ cho tôi plan high level trước.”

**AI tóm tắt:** đọc hướng dẫn cục bộ, đề xuất năm chặng: hiểu luật → schema/thuật toán offline → API và lưu dữ liệu → Structured Output → kiểm tra/bàn giao. Tri tự viết và chạy, AI giải thích và review từng phần nhỏ. Backend/test là phạm vi đang áp dụng; dùng Swagger để thử thay cho frontend riêng.

**Trạng thái khi bắt đầu:** bốn folder bài tập trống. Đây là quan sát ở đầu phiên, không phải mô tả vĩnh viễn của project.

## 2. Flow ban đầu và câu hỏi về confirm

**Tri suy nghĩ:** nhóm chăm sóc nhận N tin nhắn → LLM điền schema qua `/tickets/extract` → backend bổ sung thời điểm nhận, deadline, status `pending/done/overdue` và lưu DB → nhân viên xem `/tickets/queue` hoặc lấy việc tiếp theo qua `/tickets/next`.

**Tri hỏi:** “Tôi thắc mắc là /tickets/confirm là gì? Tôi có đang hiểu sai gì không?”

**AI sửa/giải thích:**

- Bản AI là bản nháp; cần có bước nhân viên xem/sửa/xác nhận trước khi vào queue theo flow đang áp dụng.
- `received_at` là thời điểm hệ thống nhận tin, không phải lúc LLM xử lý xong.
- Deadline tính từ thời điểm nhận và severity đã xác nhận.
- `needs_human_review=false` không tự động đồng nghĩa đã confirm.
- `next` lấy ticket khỏi hàng đợi, không đồng nghĩa đã xử lý xong. `overdue` mô tả quá hạn, không nên gộp tùy tiện với trạng thái tiến trình.

**Ví dụ AI giao nhưng Tri chưa trả lời trực tiếp:** nhận 09:00, sửa thành critical, confirm 09:20 → deadline phải tính từ 09:00, tức 09:30.

## 3. Dữ liệu mẫu và cách bắt đầu như một dev

**Tri hỏi:** “Tôi nên làm test data như thế nào? Cho tôi vài mẫu?”

**AI tóm tắt:** dùng dữ liệu giả và kết quả mong đợi. Ví dụ ngày 03/11/2026, cùng múi giờ +07:00: T01 high nhận 09:00 → hạn 11:00; T02 critical nhận 09:20 → hạn 09:50; T03 medium nhận 08:30 → hạn 16:30. Thứ tự T02 → T01 → T03. Thêm ca mơ hồ, sửa severity, thiếu timezone, ID trùng.

**Giới hạn:** severity trong các mẫu là giả định đã được nhân viên duyệt để test Python; không phải bằng chứng LLM nhất định phân loại như vậy.

**Tri hỏi:** “Nếu là một dev thì tôi nên bắt đầu suy nghĩ như thế nào? Và bắt tay làm công đoạn nào trước tiên?”

**AI tóm tắt:** bắt đầu từ invariant và nguồn quyết định dữ liệu. Đề xuất viết hàm tính deadline nhỏ, chưa ghép API/DB/AI.

**Điều AI cần điều chỉnh:** gợi ý code này đến quá sớm so với nhu cầu của Tri; Tri vẫn cần hình dung toàn bộ app và dữ liệu trước.

## 4. Tri kéo cuộc trao đổi trở lại flow và vận hành

**Tri trích mục tiêu đề và hỏi:** “Tôi nghĩ tôi cần biết flow trước để biết mình phải làm gì? Dữ liệu như thế nào? App vận hành ra sao?”

**AI đính chính:** thừa nhận đã chuyển sang code hơi sớm. Giải thích lại hành trình một ticket: nhận tin → extract bản nháp → nhân viên duyệt → confirm/kiểm dữ liệu/tính deadline → vào queue → lấy next.

**AI làm rõ:**

- Ba nhóm dữ liệu: nguồn đầu vào; bản trích xuất và bản xác nhận; kết quả và lịch sử xử lý.
- Giải thích vì sao đứng đầu bằng deadline và khóa ưu tiên do Python tính; không cần gọi LLM thêm để giải thích.
- Chưa cần thiết kế bảng DB chi tiết ngay.

**Quan sát về nhu cầu học trong phiên:** Tri chủ động yêu cầu nhìn thấy flow, dữ liệu và hành vi app trước khi làm hàm riêng lẻ. Đây là quan sát của AI từ cuộc trao đổi, không phải một tuyên bố mới của Tri.

## 5. Vẽ sơ đồ và review thiết kế đầu tiên

**Tri hỏi:** “Để vẽ hệ thống, tôi nên lên web nào để visualize?”

**AI tóm tắt:** đề xuất draw.io; Excalidraw là lựa chọn phác thảo khác. Bắt đầu bằng các bước nghiệp vụ, ghi input/output dưới mỗi bước.

**Tri gửi sơ đồ và hỏi:** “Tôi đang hiểu sai hay chưa tối ưu chỗ nào không?”

**Thiết kế Tri vẽ:**

- Extract: Email → LLM fill Ticket Schema → Ticket → Save to DB.
- Confirm: load các ticket `needs_human_review` → load DB → người dùng sửa → confirmed ticket → save DB.
- Queue: load toàn bộ ticket DB → rank và chọn top N → trả queue.
- Next: load toàn bộ ticket DB → rank và chọn top 1 → trả ticket.

**AI sửa/giải thích:**

- Gọi output extract là Draft Ticket để tránh hiểu đã vào hàng đợi.
- Theo flow đang áp dụng, confirm không chỉ dành cho ticket bị gắn cờ mơ hồ. Xem/sửa diễn ra trước khi gửi request confirm; sửa là tùy chọn.
- Confirm cần kiểm lại dữ liệu, tính deadline, lưu bản xác nhận và thêm heap.
- Đề yêu cầu min-heap: không tải và sort toàn bộ DB mỗi request rồi gọi đó là hàng đợi heap.
- Queue chỉ xem; next phải lấy ticket ra và cập nhật trạng thái chờ trong DB. Không xóa bản ghi DB.
- Cần trả thông tin giải thích thứ tự ưu tiên.

## 6. Heap trong RAM

**Tri hỏi:** “Heap lưu trong RAM và update mỗi khi có ticket mới?”

**AI sửa/giải thích:** đúng, nhưng thêm khi ticket mới **đã confirm**, không phải ngay khi extract. Heap giữ khóa `(deadline_at, -severity_rank, received_at, ticket_id)`; DB giữ chi tiết và trạng thái bền vững. Confirm dùng push, next dùng pop, xem top K không xóa. Restart đọc ticket còn chờ để dựng lại heap.

**Invariant:** tập ticket trong heap khớp tập ticket đang chờ trong DB.

**Giới hạn thiết kế được AI nêu:** demo một process/worker; chưa có giải pháp nhiều worker và chưa kiểm concurrency.

## 7. Tri yêu cầu dẫn nguồn cho “mọi ticket phải confirm”

**Tri hỏi:** “Từ yêu cầu nào mà bạn nói là tất cả ticket phải được confirm. Trích nguyên văn.”

**AI kiểm PDF gốc trang 2–4 và trích:**

Yêu cầu chung số 1, trang 2:

> Trang web cho người dùng nhập nội dung, xem GenAI đã đọc ra những gì, sửa thông tin sai, rồi bấm xác nhận để xem kết quả và lý do.

Bài 01, trang 4:

> Ví dụ: coi GenAI đã đọc đúng và nhân viên đã xác nhận ba ticket sau.

Danh sách API trang 4 có `POST /tickets/confirm`.

**AI đính chính chính mình:** PDF không có nguyên câu “tất cả ticket phải được confirm”. Đó là cách diễn giải từ yêu cầu chung và ví dụ, đồng thời là quy tắc đã có trong contract cục bộ. AI trước đó đã trình bày suy luận như quy định trực tiếp. PDF cũng không nói `needs_human_review=false` được bỏ qua confirm.

**Diễn biến sau đó:** ở phần kiểm tra hiểu biết, Tri tự trả lời rằng false vẫn cần nhân viên check và confirm trước khi vào queue; đó là flow Tri đang hiểu và áp dụng trong phiên này.

## 8. Thấy kết quả khi làm backend; Swagger là gì?

**Tri hỏi:** “Vậy làm sao để vừa dev backend vừa thấy frontend trong giai đoạn này?”

**AI tóm tắt:** dùng Swagger UI `/docs` để gửi JSON, xem response và thử chuỗi extract → confirm → queue → next. Đây là màn hình thử API, chưa phải giao diện người dùng cuối hay bằng chứng đáp ứng rubric UI.

**Tri hỏi:** “Swagger là gì?”

**AI tóm tắt:** trang xem và gọi thử API; có Try it out/Execute, hiển thị status code và response JSON. Địa chỉ phụ thuộc host/port app đang chạy.

**Tri hỏi:** “Tại sao tên là Swagger?”

**AI tóm tắt:** Swagger là tên riêng; OpenAPI là chuẩn mô tả API, Swagger UI đọc mô tả để dựng trang thử. AI chỉ giải thích nghĩa từ tiếng Anh, không xác minh lịch sử đặt tên.

## 9. Tạo main.py và bài thực hành đầu tiên

**Tri nói/hỏi:** “Tôi đã hiểu flow rồi. Tôi đã tạo 01_ticket_priority/app/main.py. Tôi phải làm gì tiếp theo? Practice là gì?”

**AI đã đọc file:** lúc kiểm tra, `main.py` trống.

**AI tóm tắt:** practice là thực hành: tự viết một phần, chạy và kiểm kết quả. Giao bài nhỏ: import FastAPI → tạo `create_app()` trả app → khai báo `GET /health` trả `{"status":"ok"}` → gán app ở cuối file. Kỳ vọng thử được `/health` qua `/docs`, nhận 200.

**Trạng thái:** chưa có bằng chứng Tri đã hoàn thành hoặc chạy bài health. Không coi đề xuất hàm tính deadline trước đó là phần đã làm.

## 10. HTTP method và từ vựng API

**Tri hỏi:** “POST, GET và những từ liên quan là gì? Tính năng mỗi cái?”

**AI tóm tắt:** GET đọc, POST tạo hoặc yêu cầu hành động, PUT thay thế, PATCH sửa một phần, DELETE xóa. Giải thích endpoint, request/response, body, path/query parameter và status code.

**Điểm gắn với bài:** next dùng POST vì lấy khỏi queue làm đổi trạng thái; queue dùng GET vì chỉ xem. Tên method không tự bảo đảm backend được triển khai đúng.

## 11. README đầu tiên và bộ câu hỏi kiểm tra extract

**Tri nói/hỏi:** đã tạo README ghi ý chính từng tính năng, muốn AI kiểm và đặt câu hỏi để chắc chắn hiểu extract.

**README khi AI đọc:**

- Extract: input email text, output Ticket BaseModel, gọi model structured output rồi trả người dùng duyệt.
- Confirm: nhận Ticket, người dùng sửa, lưu DB và queue; output ghi None.
- Queue: nhận limit hoặc None để lấy hết, trả queue.
- Next: trả ticket đầu và xóa khỏi queue.

**AI nhận xét tập trung extract:** khung đúng nhưng thiếu metadata hệ thống, kiểm output ngoài schema, lưu nguồn và bản AI. Chưa review đầy đủ các endpoint còn lại; `Output: None` và mặc định limit trong README chưa phải contract đã được xác nhận đúng.

**AI hỏi 5 câu:**

1. Ai cung cấp ID/thời điểm nhận, LLM trích field nào?
2. Tin mơ hồ thì intent/cờ review/product ra sao?
3. Model trả sai ID hoặc severity ngoài enum thì xử lý thế nào?
4. `needs_human_review=false` có vào queue ngay không?
5. Khi nhân viên sửa severity, cần lưu những bản nào?

## 12. Câu trả lời của Tri và phần được chỉnh

### Câu 1 — Nguồn ID và thời điểm nhận

**Tri trả lời:** chưa hiểu lấy từ đâu, có phải tự code không và nên giả định ra sao. Cho rằng email có datetime nhận, ví dụ đặt ngày giờ trước lời nhắn để lấy `received_at`. Đề xuất một class giữ biến đếm tăng dần mỗi khi có ticket vào DB để cấp `ticket_id`.

**AI sửa/đề xuất:**

- Thời điểm nhận nên là metadata riêng, không trộn vào nội dung khách viết để LLM đoán.
- Bài học có thể mô phỏng hệ thống tiếp nhận bằng request có `ticket_id`, `received_at` ISO 8601 kèm timezone và `message` riêng.
- Tạm nhập T01/T02 qua Swagger. Đây là gợi ý triển khai, chưa có phản hồi chốt tiếp theo của Tri.
- ID tăng dần dùng được nhưng nên để DB cấp; class đếm trong RAM bị mất khi restart và có nguy cơ trùng.
- Chưa cần tích hợp email thật.

### Câu 2 — Mơ hồ

**Tri trả lời:** `intent="other"`, `needs_human_review=true`; product tùy nội dung có nêu tên sản phẩm hay không, nếu không thì null; lý do là tài liệu yêu cầu như vậy.

**AI đánh giá:** đúng; không tự đoán thêm product.

### Câu 3 — Output sai

**Tri trả lời:** “Tôi chưa nghĩ đến tình huống này.”

**AI bổ sung:** schema chặn severity ngoài enum; backend còn phải so output ID với ID hệ thống vì chuỗi đúng kiểu vẫn có thể sai ID. Báo lỗi, không đưa vào queue. Chưa chốt cụ thể error response/status cho lỗi model.

### Câu 4 — false có cần confirm?

**Tri trả lời:** “Nếu là false thì vẫn cần xác nhận để vào queue, nhân viên vẫn check để confirm.”

**AI đánh giá:** đúng với flow đang áp dụng.

### Câu 5 — Lưu lịch sử

**Tri trả lời:** “Chỉ lưu của nhân viên làm final vì con người là người quyết định và chịu trách nhiệm.”

**AI sửa:** bản nhân viên xác nhận là dữ liệu chính thức để tính, nhưng vẫn phải giữ nguồn và bản AI để truy nguyên. Yêu cầu chung số 4, trang 3 PDF:

> Lưu nội dung gốc, JSON GenAI trả về, bản người dùng sửa, kết quả cuối và thời gian xử lý để có thể xem lại.

Ví dụ chỉ giữ `low` sau khi sửa từ `high` thì không thể biết AI ban đầu đã phân loại thế nào.

## 13. Các vòng sửa README về extract

**Tri gửi bản sửa và hỏi:** “Tôi vừa sửa lại. Check cho tôi nhé”, sau đó tiếp tục hỏi “Ok chưa?” qua các bản cập nhật.

**Diễn biến suy nghĩ của Tri:**

- Thêm request JSON mẫu gồm `ticket_id`, `received_at`, `message`.
- Ghi rõ extract không đưa ticket vào queue; bổ sung kiểm tra mơ hồ và output sai.
- Ban đầu ghi lưu vào database riêng cho AI response, sau đó đổi thành table riêng có cùng schema với Ticket confirm.
- Sau review, đổi thành lưu nội dung gốc, metadata và bản AI, giữ riêng với bản người dùng xác nhận để đối chiếu.
- Bổ sung `ticket_id`, rồi `received_at` vào danh sách field output API.

**AI sửa/giải thích:**

- Input là JSON gồm metadata và text, không chỉ một chuỗi email.
- LLM trích xuất thông tin từ message, không phải chép nguyên message vào Ticket.
- Mơ hồ nhưng hợp lệ vẫn trả bản nháp; sai schema hoặc sai ID phải báo lỗi, không trả như Ticket hợp lệ. Extract chưa thêm queue trong cả hai trường hợp.
- Không có yêu cầu database riêng hoặc hai bảng phải cùng schema; schema Pydantic và bảng DB có vai trò khác nhau. Trước hết mô tả dữ liệu phải lưu, chưa cần chốt cách chia bảng.
- AI nhắc output cần giữ `ticket_id`; “category” không phải field của bài này, nên dùng intent/severity.

**Tri hỏi cụ thể:** “Tôi đưa received_at vào schema nhé? Hay nên xử lý như thế nào?”

**AI tóm tắt:** `received_at` được có trong response API, nhưng không cần yêu cầu LLM trả lại. Phân biệt ba vai trò: request nhận ID/thời điểm/message; schema trích xuất LLM có ID/intent/severity/product/summary/cờ review; response backend ghép bản trích xuất đã kiểm với thời điểm nhận từ input. Kiểm timezone trước khi gọi model, đối chiếu ID sau khi model trả.

**Tri nói đã sửa xong và nhờ cập nhật nhật ký/handoff. AI đọc lại README thực tế:** request mẫu và danh sách output đã có; phần lưu nguồn/metadata/bản AI tách bản xác nhận đã cập nhật. Vẫn còn vài ý chưa viết rõ: ai bổ sung received_at, kiểm sai ID, mơ hồ cần intent=other, extract chưa thêm queue. Không coi những dòng còn thiếu là Tri đã phản đối hoặc đã thực hiện sai; cần làm rõ khi chuyển sang schema.

## 14. Điểm tiếp tục cho Tri/AI sau này

**Tiến độ hiện tại:** Tri đã hoàn thành nhiều vòng sửa mô tả extract trong README. Bước tiếp theo được đề xuất là phân biệt ba vai trò request / output LLM / response API rồi để Tri tự định nghĩa schema đầu vào trước, từng phần nhỏ. Nếu Tri muốn hoàn thiện README trước, chỉ chỉnh những ý còn thiếu đã nêu; không lặp lại toàn bộ bài giảng flow.

**Bằng chứng hiện có:** đã đọc lại README bản mới nhất khi cập nhật nhật ký; main.py vẫn trống. Chưa chạy backend/test/model; chưa cài dependency cho bài trong phiên này. Khi tiếp tục phải đọc file hiện tại, không dựa riêng vào trạng thái ghi ở đây. Xem [HANDOFF bài 01](HANDOFF.md) để tiếp tục nhanh.

**Chưa chốt/triển khai:** schema request/response chi tiết, thiết kế DB, cơ chế cấp ID thực tế, error contract, provider/model, đồng bộ DB–heap. SQLite + SQLAlchemy sync và input giả qua Swagger là các đề xuất, không tự nâng thành quyết định đã được Tri xác nhận.

**Cách đồng hành cần giữ:** giải thích flow/dữ liệu trước công cụ; mỗi lượt một mục tiêu nhỏ; Tri tự viết và chạy; không tự sửa bài nếu chưa được nhờ rõ. Không coi những câu hỏi kiểm tra chưa trả lời là Tri đã hiểu.

## Nguồn để kiểm tra lại

- [README của Tri](README.md): ghi chú yêu cầu đang được Tri hoàn thiện, không phải bản đặc tả cuối.
- [Điểm bắt đầu](../AGENTS.md) và [skill đồng hành](../develop-fastapi-from-scratch/SKILL.md).
- [Contract cục bộ](../develop-fastapi-from-scratch/references/exercise-contracts.md): quy tắc hướng dẫn triển khai; phân biệt với nguyên văn đề.
- [PDF gốc](../23-10-2026-01-01-30-bai-tap-structured-output-va-thuat-toan.pdf): yêu cầu chung trang 2–3, bài 01 trang 3–4. Các đoạn dẫn nguyên văn ở trên đã được kiểm trong PDF ở lượt trao đổi về confirm.

File này chỉ ghi lại cuộc trao đổi và suy nghĩ đã thể hiện; không thay thế đề, contract hoặc kiểm chứng code chạy thật.

## 15. Bổ sung ngày 04/11/2026 — bắt đầu tự dựng FastAPI

Tri bắt đầu từ app buổi 6, hỏi app cần gì, chạy thế nào và lifespan có bắt buộc không. AI giải thích create_app → đăng ký route → return app. Lifespan quản lý tài nguyên khởi động/dừng, không phải cache hoặc refresh Session từng request. Tri đã viết health/extract; lifespan hiện còn pass và chưa dùng. Dòng truyền get_settings đã được đổi thành gọi get_settings().

Tri hỏi về gitignore, tên gói requirements và cách đặt model/schema. Đã phân biệt Pydantic kiểm dữ liệu với ORM ánh xạ bảng. Source hiện dùng model.py cho Pydantic và model_db.py cho ORM; không cần đổi naming theo gợi ý cũ. Requirements có gói web/AI/ORM nhưng chưa kiểm chứng cài đủ hoặc tương thích.

## 16. Structured Output và ba vai trò dữ liệu

Tri tự viết TicketExtracted và hỏi Literal, bool, nullable, description. Đã có enum intent/severity, product null khi không biết, summary tối đa 200 ký tự, cờ review bool. Description hướng dẫn LLM; Literal/Field kiểm cấu trúc, không bảo đảm đúng nghĩa. Source vẫn dùng chuỗi nối trong ngoặc dù đã trao đổi cách viết ngắn hơn.

Tri phản biện: email là JSON, chỉ gửi message cho LLM thì cần ID không? AI đồng ý metadata do backend giữ, không nhờ model chép ID. Đây là điều chỉnh so với contract cục bộ, không khẳng định đã tuân thủ nguyên trạng contract. TicketExtractIn hiện dùng id, received_at AwareDatetime, message; min_length=1 chưa chặn toàn khoảng trắng. README vẫn dùng ticket_id.

Tri hỏi vì nhớ client.chat.completions.create. Đã phân biệt SDK OpenAI trực tiếp với LangChain invoke; messages có thể dùng dictionary hoặc tuple. Source dùng ChatOpenAI + with_structured_output, tuple system/human và route def đồng bộ.

Tri nhắc response phải có ID/thời điểm nhận. Đã thêm TicketExtractOut kế thừa TicketExtracted, backend ghép metadata. Đã trao đổi **result.model_dump(), gán từng field và schema lồng; source hiện dùng gán từng field, response phẳng. Không coi ví dụ schema lồng là lựa chọn đã triển khai.

## 17. Thử mẫu và kiểm tra thông tin AI thêm vào

Tri ghi bốn case trong samples/post_ticket_extract.txt: billing/high nhưng summary thêm yêu cầu hoàn tiền/điều chỉnh; technical/critical; mơ hồ other/product=null/review=true; thiếu timezone có lỗi timezone_aware. AI chỉ đọc ghi chép, không tự chạy lại. Chưa có HTTP status hoặc metadata trong response mẫu để xác nhận lần chạy API mới nhất.

Sau review, main.py có system prompt “Trích xuất thông tin ticket. Không thêm thông tin ngoài tin nhắn.” Chưa có mẫu chạy lại chứng minh khắc phục lỗi case 1. Severity chưa có rubric chi tiết để đặt đáp án cố định. JSON đúng schema không bảo đảm nội dung đúng.

## 18. Lưu đối chiếu và tích hợp Supabase

Tri nhắc phải lưu DB để đối chiếu. AI xác nhận route demo trước đó chưa đủ: extract lưu nguồn/metadata và bản AI, confirm giữ bản người dùng riêng, không ghi đè bản AI. Lưu extract không đưa ticket vào heap.

Tri cho biết tạo DB Supabase, đã có URL và viết database.py. Các câu hỏi tập trung Base, engine, sessionmaker, type hint return và lý do trả cặp. AI giải thích Base.metadata tập hợp mô tả bảng; engine quản lý kết nối; factory tạo Session, Session thực hiện CRUD; trả engine để app còn tạo bảng demo và dispose pool. Context manager đóng Session, không tự commit.

Tri hỏi String/Text và bắt đầu model_db.py. Khi đọc ngày 04/11, đã có Email/Ticket nhưng chưa nối vào app. Cần review now_utc đang bỏ timezone, received_at chưa bật timezone và phải giữ thời điểm nguồn; product ORM chưa nullable; chưa có FK nguồn–AI hoặc bản confirmed/timestamp/thời lượng xử lý. Đây là khung đang học, chưa chứng minh tạo bảng/lưu Supabase thành công.

## 19. Điểm dừng sau lần bổ sung

Đã đọc lại main.py, model.py, database.py, model_db.py, config.py, requirements.txt, README và samples. Theo yêu cầu Tri, chỉ thêm vào HANDOFF gốc, HANDOFF bài 01 và NHAT_KY.md, giữ nguyên nội dung trước. Không đọc .env, sửa code, chạy server/test hoặc gọi dịch vụ.

Bước tiếp theo: cùng Tri review model_db.py, sửa ràng buộc timezone/product và chốt liên kết nguồn–AI trước khi nối lifecycle/get_db. Tiếp tục từng phần nhỏ, Tri tự code/chạy; không tự triển khai cả hệ thống. Xem [HANDOFF](HANDOFF.md), phần bổ sung ngày 04/11, để biết đầy đủ khoảng trống và tiêu chí kiểm tra bước lưu extract.

NHAT_KY_TU_DUY_2026-11-03.md được dẫn trong phần cũ không xuất hiện trong danh sách file hiện tại; giữ nguyên các link cũ theo yêu cầu không xóa, nhật ký đang nối tiếp tại file này.
