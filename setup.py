#!/usr/bin/env python3
"""
Setup script cho Discord Ticket Bot
Chạy: python setup.py
"""

import os
import json

def create_env_file():
    """Tạo file .env"""
    if os.path.exists('.env'):
        print("✅ File .env đã tồn tại")
        return
    
    print("\n🔧 Tạo file .env...")
    token = input("Nhập Discord Bot Token: ").strip()
    prefix = input("Nhập prefix (mặc định: !): ").strip() or "!"
    
    with open('.env', 'w') as f:
        f.write(f"DISCORD_TOKEN={token}\n")
        f.write(f"PREFIX={prefix}\n")
    
    print("✅ File .env đã được tạo!")

def create_config():
    """Tạo/cập nhật config.json"""
    default_config = {
        "prefix": "!",
        "staff_role": "Staff",
        "admin_role": "Admin",
        "ticket_category": "Tickets",
        "ticket_prefix": "ticket",
        "welcome_message": "Cảm ơn bạn đã mở ticket! 👋\n\nStaff sẽ sớm hỗ trợ bạn. Vui lòng mô tả vấn đề chi tiết.",
        "ticket_color": 5814783
    }
    
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            existing = json.load(f)
        existing.update(default_config)
        config = existing
    else:
        config = default_config
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ File config.json đã được tạo/cập nhật!")

def create_data_dir():
    """Tạo thư mục data"""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("✅ Thư mục data được tạo!")
    
    if not os.path.exists('data/tickets.json'):
        data = {
            "panels": [],
            "tickets": {},
            "closed_tickets": []
        }
        with open('data/tickets.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("✅ File data/tickets.json được tạo!")

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║          🎫 Discord Ticket Bot - Setup Script            ║
║                                                           ║
║  Trình này sẽ giúp bạn thiết lập bot ticket            ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("📝 Bước 1: Kiểm tra/tạo file .env")
    create_env_file()
    
    print("\n⚙️ Bước 2: Tạo/cập nhật config.json")
    create_config()
    
    print("\n📁 Bước 3: Tạo thư mục data")
    create_data_dir()
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║                   ✅ Setup Hoàn Tất!                     ║
║                                                           ║
║  Bước tiếp theo:                                          ║
║  1. Cài dependencies: pip install -r requirements.txt    ║
║  2. Chạy bot: python main.py                            ║
║  3. Tạo roles Staff & Admin trong server                 ║
║  4. Dùng lệnh: !setup [category] để tạo panel           ║
║                                                           ║
║  📖 Xem hướng dẫn chi tiết: GUIDE.md                      ║
╚═══════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()
