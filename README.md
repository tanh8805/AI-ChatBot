# AI ChatBot

Ứng dụng ChatBot AI tương tác qua giao diện dòng lệnh (CLI), sử dụng mô hình Google Gemini.

## 🌟 Tính năng

- **Phản hồi thời gian thực (Streaming):** Hiển thị câu trả lời dạng luồng trực tiếp ngay khi mô hình đang sinh dữ liệu.
- **Quản lý lịch sử hội thoại:** Tự động duy trì và cắt tỉa ngữ cảnh cuộc trò chuyện theo số lượng tin nhắn cấu hình.
- **Tách biệt cấu hình & bí mật:**
  - `config.yaml`: Chứa toàn bộ tham số mô hình (`temperature`, `system_prompt`, `max_history`,...).
  - `.env`: Lưu trữ riêng API key bảo mật.
- **Kiến trúc Factory & Abstraction:** Dễ dàng thay thế hoặc mở rộng sang các nhà cung cấp LLM khác.
- **Xử lý ngoại lệ chuẩn hóa:** Bắt và thông báo rõ ràng các lỗi API (sai API key, hết quota, mất kết nối mạng,...).

## 🚀 Cách cài đặt & Sử dụng

### 1. Chuẩn bị môi trường
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Cài đặt ứng dụng
```bash
pip install -e .
```

### 3. Cấu hình API Key
Sao chép file mẫu và điền API Key của Google Gemini:
```bash
cp .env.example .env
```
Mở file `.env` và cập nhật:
```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Khởi chạy ChatBot
Chạy lệnh sau để bắt đầu trò chuyện:
```bash
chatbot
```
*(Hoặc chạy qua module: `python -m src.cli`)*
