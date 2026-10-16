import sys
from src.bot import ChatBot
from src.exceptions import ChatBotError


def main() -> None:
    try:
        bot = ChatBot()
    except Exception as e:
        print(f"❌ Khởi động thất bại: {e}")
        sys.exit(1)

    print("=" * 60)
    print("🤖 AI CHATBOT CLI")
    print("Lệnh: 'exit' hoặc 'quit' để thoát | 'clear' để xóa lịch sử")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nBạn: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("Tạm biệt!")
                break

            if user_input.lower() == "clear":
                bot.clear()
                print("🧹 Đã làm mới phiên hội thoại.")
                continue

            print("Bot: ", end="", flush=True)
            for chunk in bot.ask_stream(user_input):
                print(chunk, end="", flush=True)
            print()

        except (KeyboardInterrupt, EOFError):
            print("\n\nĐã thoát chương trình. Tạm biệt!")
            break
        except ChatBotError as e:
            print(f"\n❌ Lỗi: {e.message}")
            if e.details:
                print(f"Chi tiết: {e.details}")


if __name__ == "__main__":
    main()
