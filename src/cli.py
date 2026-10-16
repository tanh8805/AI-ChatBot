import sys
from src.bot import ChatBot
from src.exceptions import ChatBotError


def main() -> None:
    try:
        bot = ChatBot()
    except Exception as e:
        print(f"❌ Khởi động thất bại: {e}")
        sys.exit(1)

    current_session = "default"

    print("=" * 60)
    print("🤖 AI CHATBOT CLI (Đa Session & Tùy chỉnh Persona)")
    print("Lệnh:")
    print(" - 'exit' | 'quit'    : Thoát chương trình")
    print(" - 'clear'            : Xóa lịch sử session hiện tại")
    print(" - 'session'          : Xem session đang kích hoạt")
    print(" - 'session <id>'     : Chuyển hoặc tạo session mới")
    print(" - 'sessions'         : Xem danh sách session đang có")
    print(" - 'persona <prompt>' : Đổi persona/system prompt cho session này")
    print(" - 'persona'          : Xem persona hiện tại của session")
    print("=" * 60)

    while True:
        try:
            prompt_label = f"[{current_session}] Bạn: " if current_session != "default" else "Bạn: "
            user_input = input(f"\n{prompt_label}").strip()
            if not user_input:
                continue

            cmd = user_input.lower()
            if cmd in ("exit", "quit"):
                print("Tạm biệt!")
                break

            if cmd == "clear":
                bot.clear(current_session)
                print(f"🧹 Đã làm mới lịch sử session '{current_session}'.")
                continue

            if cmd == "sessions":
                active = bot.list_sessions()
                print(f"📋 Các session hiện có: {active or ['chưa có tin nhắn']}")
                continue

            if cmd == "session":
                print(f"ℹ️ Session hiện tại là: '{current_session}'. Dùng 'session <tên>' để chuyển session.")
                continue

            if user_input.startswith("session "):
                new_session = user_input.split(maxsplit=1)[1].strip()
                if new_session:
                    current_session = new_session
                    print(f"👉 Đã chuyển sang session: '{current_session}'")
                continue

            if cmd == "persona":
                current_p = bot.get_persona(current_session)
                print(f"🎭 Persona hiện tại của [{current_session}]:\n{current_p}")
                continue

            if user_input.startswith("persona "):
                new_persona = user_input.split(maxsplit=1)[1].strip()
                if new_persona:
                    bot.set_persona(current_session, new_persona)
                    print(f"🎭 Đã cập nhật persona cho session '{current_session}'!")
                continue

            print("Bot: ", end="", flush=True)
            for chunk in bot.ask_stream(user_input, session_id=current_session):
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
