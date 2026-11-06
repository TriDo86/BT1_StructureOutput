from typing import Literal

from pydantic import BaseModel, Field, AwareDatetime

class TicketExtractIn(BaseModel):
    """Email từ người dùng"""
    id: str = Field(min_length=1)
    received_at: AwareDatetime
    message: str = Field(min_length=1)


class TicketExtracted(BaseModel):
    """Bản nháp thông tin trích xuất từ nội dung ticket."""

    intent: Literal["billing", "technical", "account", "other"] = Field(
        description=(
            "Nhóm vấn đề: billing là thanh toán; technical là kỹ thuật; "
            "account là tài khoản; other là vấn đề khác hoặc không xác định rõ. "
            "Nếu nội dung mơ hồ, chọn other và đặt needs_human_review=true."
        )
    )
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description=(
            "Mức độ nghiêm trọng dựa trên tác động được mô tả trong tin nhắn. "
            "Không tự bịa mức độ ảnh hưởng; nếu chưa đủ thông tin để đánh giá, "
            "đặt needs_human_review=true."
        )
    )
    product: str | None = Field(
        description=(
            "Tên sản phẩm hoặc dịch vụ được nhắc đến trong tin nhắn. "
            "Không xác định được thì trả null, không tự suy đoán."
        )
    )
    summary: str = Field(
        max_length=200,
        description=(
            "Tóm tắt vấn đề khách hàng gặp phải, tối đa 200 ký tự. "
            "Giữ đúng nội dung gốc, không thêm thông tin chưa được cung cấp."
        )
    )
    needs_human_review: bool = Field(
        description=(
            "True nếu nội dung mơ hồ, thiếu thông tin hoặc có điểm chưa chắc chắn "
            "cần người dùng xem xét kỹ; ngược lại là false. "
            "Trường này không thay thế bước xác nhận của người dùng."
        )
    )

class TicketExtractOut(TicketExtracted):
    id: str
    received_at: AwareDatetime

class TicketConfirmIn(TicketExtracted):
    id: str