# Contract bốn project

Nguồn chuẩn: [đề gốc cục bộ](../../23-10-2026-01-01-30-bai-tap-structured-output-va-thuat-toan.pdf), 8 trang. Các trang dưới đây là số trang thực trong PDF. Không đổi luật để khớp thuật toán ví dụ lớp.

## Chung — trang 2–3

- GenAI trích xuất JSON theo schema; Python kiểm dữ liệu và tính kết quả; người dùng có thể xem, sửa, xác nhận trước xử lý chính thức.
- Lưu nguồn gốc, JSON AI, bản sửa, kết quả cuối, thời gian xử lý. API key ở backend. Chỉ dùng dữ liệu giả; không cần gọi dịch vụ thật để chạy test thuật toán.
- Có mẫu JSON, README, ít nhất ba test thuật toán (thường/biên/sai), giải thích AI làm gì/Python làm gì và minh họa luồng chính.
- **Override trực tiếp của Tri:** chỉ backend/test, bốn folder riêng. PDF có yêu cầu web và rubric UI; backend-only không chứng minh đáp ứng phần UI của rubric gốc. Không tự bổ sung frontend để theo PDF.
- Mock offline là bước phát triển, không thay thế việc cài nhánh structured output thật trong bản hoàn chỉnh. Ghi rõ nhánh nào đã chạy.

## Bài 01 — 01_ticket_priority — trang 3–4

**Input hệ thống:** ticket_id, received_at có timezone và tin nhắn gốc. **AI output:** ticket_id, intent, severity, product, summary, needs_human_review.

- intent: billing/technical/account/other; severity: low/medium/high/critical; product có thể null; summary tối đa 200 ký tự.
- Mơ hồ: intent=other, needs_human_review=true; AI không được đổi ticket_id hệ thống.
- SLA Python tính: critical=30 phút, high=2 giờ, medium=8 giờ, low=24 giờ. Không gọi AI để tính deadline.
- Khóa min-heap: `(deadline_at, -severity_rank, received_at, ticket_id)`, critical=4/high=3/medium=2/low=1.
- Chỉ confirm hợp lệ mới thêm heap. Đề cho chọn quy tắc ID trùng; mặc định đề xuất từ chối 409. top K không xóa; next mới lấy ra.
- Invariant: phần tử nhỏ nhất trong heap là ticket chưa xử lý có khóa ưu tiên nhỏ nhất; ID không lặp; DB và heap phản ánh cùng tập ticket đang chờ.
- Add/pop O(log n) khi heap đã có; top K có thể `heapq.nsmallest` không mutate heap, chi phí riêng O(n log k) khi k nhỏ. Không rebuild/sort cả queue mỗi lần thêm rồi tuyên bố O(log n). Khởi động có thể `heapify` từ DB.

**API tối thiểu:** POST `/tickets/extract`, POST `/tickets/confirm`, GET `/tickets/queue?limit=...`, POST `/tickets/next`.

**Kỳ vọng và test:**

1. T01 high nhận 21/10/2026 09:00 +07 → 11:00; T02 critical 09:20 → 09:50; T03 medium 08:30 → 16:30. Thứ tự T02,T01,T03; xem top 2 rồi next vẫn T02.
2. T04 high nhận 07:00 → 09:00, lên đầu. Test tie key và ID quyết định thứ tự; lưu ý một số cấp tie chỉ xuất hiện nếu các thành phần trước đã bằng.
3. ID trùng, sai ID output AI, severity ngoài enum, datetime không timezone, limit<1 bị từ chối. Queue rỗng có response đã định nghĩa; không để lỗi IndexError thành 500.
4. Restart giữ ticket chờ và thứ tự; next đã lấy không xuất hiện lại.

## Bài 02 — 02_dock_booking — trang 5–6

**AI output:** request_id, carrier, earliest_start, duration_minutes, dock_type, missing_fields.

- earliest_start có timezone; duration_minutes>0. Nếu email không nói thời lượng: null và missing_fields chứa duration_minutes, chưa được tính/confirm booking.
- dock_type: standard/refrigerated; backend kiểm request_id, cửa đúng loại, dữ liệu lịch và giờ mở cửa.
- Giờ làm việc 08:00–18:00 theo ngày local UTC+07:00. Không có slot trong ngày thì `no_slot`, không tự chuyển ngày.
- Với mỗi cửa phù hợp: sort, gộp lịch chồng hoặc chạm nhau, tìm gap đầu tiên từ max(earliest_start, giờ mở cửa) đủ thời lượng; chọn `(start, dock_id)` nhỏ nhất.
- Dùng khoảng [start,end): hai booking chạm biên không xung đột. Predicate xung đột: `existing.start < new.end and new.start < existing.end`.
- Invariant: lịch đã merge tăng dần, không còn overlap/chạm; cursor không lùi; một cửa không có hai booking xác nhận chồng thời gian.
- Mục tiêu O(n log n) cho sort/merge, n là số booking đang xét. Không thêm optimizer phân công xe hoặc khoảng dọn cửa vào bản đầu.

**API tối thiểu:** POST `/requests/extract`, POST `/slots/suggest`, POST `/bookings/confirm`.

**Confirm là kiểm lại + ghi nguyên tử:** re-read dữ liệu mới nhất và kiểm slot trong cùng transaction trước khi insert. Với SQLite local, có thể dùng transaction `BEGIN IMMEDIATE` trước SELECT và giữ đến commit/rollback; triển khai/kiểm tra cách điều khiển transaction với SQLAlchemy thực tế, không chạy BEGIN sau khi Session đã bắt đầu transaction khác. Lock chỉ trong Python không bảo vệ process khác; khi chuyển DB cần cơ chế DB phù hợp (ví dụ khóa dòng cửa kho). Xung đột trả 409, không tự dời booking sang giờ khác mà chưa xác nhận.

**Kỳ vọng và test:**

1. Ngày 21/10/2026: cửa A bận 09–10,10–11; B bận 09:30–10:15; request từ 09:00 cần 60 phút → B,10:15–11:15.
2. Booking kết thúc 10:00 cho phép booking mới bắt đầu 10:00; hai cửa cùng start chọn alphabet; kết thúc đúng 18:00 hợp lệ.
3. Thiếu thời lượng, duration≤0, giờ thiếu timezone, end≤start, không đúng loại cửa và no_slot có kết quả rõ.
4. Hai client cùng confirm slot: chỉ một thành công, một conflict, DB có đúng một booking. Test cả hai cùng nhận đề xuất cũ rồi confirm, và kiểm transaction bảo vệ cạnh tranh thực tế; không chỉ hai request nối tiếp để tuyên bố concurrency đã kiểm chứng.

## Bài 03 — 03_expense_duplicates — trang 6–7

**AI output:** submission_id, vendor, invoice_number, transaction_date, amount_minor, currency, receipt_id, missing_fields. Không đọc được: null và ghi missing_fields; confirmed input phải qua kiểm tra nghiệp vụ.

- amount_minor integer không âm: VND=đồng, USD=cent. Chọn VND/USD cho bản đầu và ghi đây là allowlist đề xuất; loại khác báo không hỗ trợ, không tự quy đổi.
- Chuẩn hóa Unicode và khoảng trắng thừa, không phân biệt hoa/thường ở vendor/invoice. Đề xuất Unicode NFC + casefold + split/join; giữ dấu gạch nối. Quy tắc receipt_id chưa nói case-insensitive: mặc định trim/NFC và giữ nguyên case, ghi rõ quyết định này.
- Chỉ mục dict: khóa receipt `(currency, receipt_id)` nếu có; thêm khóa invoice `(currency, normalized_vendor, normalized_invoice)` nếu đủ. Dùng namespace/key riêng để hai dạng không va chạm.
- Mỗi key nên ánh xạ đến tập/danh sách submission_id; hợp nhất toàn bộ ứng viên khi hai key trỏ các bản khác nhau, không lấy tùy tiện một bản đầu.
- Tìm thấy key cũ: `duplicate_candidate`, trả ID cũ và khác biệt trường, kể cả amount/date khác. Không đưa amount vào key nên không làm mất nghi vấn khi tiền thay đổi.
- Không đủ tạo key hoặc dữ liệu thiết yếu chưa đáng tin: `needs_review`; không trả unique để che thiếu dữ liệu. Dữ liệu sai như tiền âm/currency không hỗ trợ bị từ chối.
- Chưa có key cũ và dữ liệu đủ: `unique_under_current_rules`; không diễn giải thành hợp lệ/chắc chắn không trùng. Không kết luận gian lận hoặc tự từ chối hoàn tiền.
- Invariant: chỉ mục phản ánh các khóa hiện tại của bản đã lưu; không so một submission với chính nó. Sửa mã phải bỏ ánh xạ cũ của đúng bản đó, tạo khóa mới và kiểm lại; không xóa khóa dùng bởi bản khác.
- Tra cứu dict trung bình O(1) mỗi key, O(n) cho một lượt xây/kiểm n chứng từ, chưa tính chi phí đọc chuỗi và xuất mọi cặp trùng. Nhóm toàn bản trùng có thể tạo output lớn hơn O(n).

**API tối thiểu:** POST `/expenses/extract`, POST `/expenses/check`, POST `/expenses/review`.

MVP nhận văn bản đã OCR, là một lựa chọn đầu vào có trong đề. Không cần xây OCR/upload ảnh ngay; `pypdf.extract_text` không thay được OCR ảnh scan. Review lưu quyết định xác nhận/bỏ nghi vấn cùng bản trước/sau sửa; bản sửa phải được check lại, không tái dùng kết quả cũ.

**Kỳ vọng và test:**

1. E01 vendor ABC Travel/invoice INV-0042/receipt R-42/1.250.000 VND → unique; E02 cùng dữ liệu nhưng vendor/invoice khác case/space → candidate E01; E03 thiếu invoice/receipt → needs_review.
2. E02 khác tiền vẫn candidate và có chênh lệch; INV-0042 và INV0042 là hai mã khác nếu receipt không trùng. Bản sau thiếu receipt vẫn tìm được bằng key invoice.
3. Tiền âm, tiền float không phải integer, thiếu mã, currency sai; các key khác currency không trùng; normalized Unicode tương đương cho cùng key.
4. Sửa receipt/invoice → check lại, không còn key cũ sai; review giữ bản gốc; restart rebuild index không làm mất ứng viên.

## Bài 04 — 04_task_dependencies — trang 7–8

**AI output:** tasks `[{id,title,owner}]`, dependencies `[{before,after,evidence}]`. owner có thể null; evidence phải dựa trên câu trong biên bản, không bịa quan hệ. Task có ID riêng, không dùng title làm ID.

- Backend từ chối ID task trùng, cạnh tới ID lạ, self-loop. Cạnh lặp `(before,after)` dedupe trước tính indegree.
- Chỉ dùng danh sách task/cạnh đã được người dùng xác nhận. Validate/order phải gắn đúng bản sửa hiện tại, không áp confirmation của bản cũ.
- Kahn: adjacency list + indegree; heap các ID indegree=0 để chọn alphabet ở mỗi bước, không chỉ sort input một lần.
- Invariant: heap chứa task chưa xuất có indegree=0 trong đồ thị còn lại; mọi cạnh đi từ task trước sang task sau trong kết quả hoàn chỉnh.
- Nếu xuất ít hơn V task: `cycle_detected`, không trả một phần như kế hoạch hoàn chỉnh. Trả ít nhất vòng thật hoặc các cạnh liên quan ở phần đồ thị còn lại để người dùng sửa. Không gọi toàn bộ node chưa xuất là node thuộc vòng: có node chỉ bị vòng chặn phía trước.
- O((V+E) log V) với heap; không gọi là O(V+E) cho bản có tie-break heap. Không thêm duration, lịch ngày hoặc giới hạn nhân lực.

**API tối thiểu:** POST `/plans/extract`, POST `/plans/validate`, POST `/plans/order`.

**Kỳ vọng và test:**

1. Cạnh A→C,B→C,C→D: kết quả A,B,C,D, kể cả đảo thứ tự JSON input.
2. Thêm D→A: cycle_detected, chỉ vòng/cạnh liên quan, không kế hoạch một phần; xóa D→A lại hợp lệ.
3. ID lạ, ID trùng, self-loop bị từ chối; cạnh lặp không tăng indegree hai lần; không có cạnh thì alphabet. Định nghĩa kết quả danh sách rỗng một cách rõ ràng.

## Không mở scope khi bắt đầu

Phần tùy chọn trong PDF (skill nhân viên, khoảng dọn cửa, fuzzy OCR, nhóm việc song song) chưa đưa vào bản đầu. Khi contract còn điểm mở, ghi quyết định vào README; chỉ hỏi Tri nếu quyết định làm thay đổi đáng kể dữ liệu hoặc hành vi yêu cầu.
