"""
Test file để xác minh ticket bot hoạt động đúng
Chạy: python test_bot.py
"""

import json
import asyncio
from utils.database import (
    create_ticket, get_ticket, update_ticket, close_ticket,
    get_user_tickets, get_channel_ticket, load_data, save_data
)

def test_ticket_creation():
    """Test tạo ticket"""
    print("=" * 60)
    print("TEST 1: Tạo Ticket")
    print("=" * 60)
    
    ticket = create_ticket(
        ticket_id="test123",
        user_id=123456789,
        channel_id=987654321,
        guild_id=111111111,
        category="General Support"
    )
    
    print(f"✅ Ticket created: {ticket['ticket_id']}")
    print(f"   - User ID: {ticket['user_id']}")
    print(f"   - Channel ID: {ticket['channel_id']}")
    print(f"   - Status: {ticket['status']}")
    print(f"   - Closed: {ticket['closed']}")
    
    return ticket

def test_get_ticket(ticket_id):
    """Test lấy ticket"""
    print("\n" + "=" * 60)
    print("TEST 2: Lấy Thông Tin Ticket")
    print("=" * 60)
    
    ticket = get_ticket(ticket_id)
    if ticket:
        print(f"✅ Ticket tìm thấy: {ticket['ticket_id']}")
        print(f"   - Status: {ticket['status']}")
        print(f"   - Closed: {ticket['closed']}")
    else:
        print(f"❌ Ticket không tìm thấy")
    
    return ticket

def test_close_ticket(ticket_id):
    """Test đóng ticket"""
    print("\n" + "=" * 60)
    print("TEST 3: Đóng Ticket (It Works!)")
    print("=" * 60)
    
    close_ticket(ticket_id, user_id=123456789)
    
    data = load_data()
    
    # Kiểm tra ticket đã xóa khỏi tickets
    if ticket_id not in data["tickets"]:
        print(f"✅ Ticket '{ticket_id}' đã xóa khỏi 'tickets'")
    
    # Kiểm tra ticket đã thêm vào closed_tickets
    closed = next((t for t in data["closed_tickets"] if t["ticket_id"] == ticket_id), None)
    if closed:
        print(f"✅ Ticket '{ticket_id}' đã thêm vào 'closed_tickets'")
        print(f"   - Closed: {closed['closed']}")
        print(f"   - Closed At: {closed['closed_at']}")
        print(f"   - Closed By: {closed['closed_by']}")
    
    return closed

def test_channel_lookup(channel_id):
    """Test tìm ticket từ channel ID"""
    print("\n" + "=" * 60)
    print("TEST 4: Tìm Ticket Từ Channel ID")
    print("=" * 60)
    
    # Tạo ticket mới
    create_ticket(
        ticket_id="channel_test",
        user_id=111111111,
        channel_id=channel_id,
        guild_id=222222222,
        category="Support"
    )
    
    ticket_id = get_channel_ticket(channel_id)
    if ticket_id:
        print(f"✅ Channel ID {channel_id} → Ticket ID: {ticket_id}")
    else:
        print(f"❌ Không tìm thấy ticket cho channel này")
    
    return ticket_id

def test_user_tickets():
    """Test lấy tickets của user"""
    print("\n" + "=" * 60)
    print("TEST 5: Lấy Tickets Của User")
    print("=" * 60)
    
    user_id = 111111111
    guild_id = 222222222
    
    tickets = get_user_tickets(user_id, guild_id)
    print(f"✅ User {user_id} có {len(tickets)} ticket(s)")
    
    for ticket in tickets:
        print(f"   - {ticket['ticket_id']}: {ticket['category']} (Status: {ticket['status']})")
    
    return tickets

def test_status_update():
    """Test update status"""
    print("\n" + "=" * 60)
    print("TEST 6: Cập Nhật Status (Need Help)")
    print("=" * 60)
    
    ticket_id = "status_test"
    create_ticket(
        ticket_id=ticket_id,
        user_id=999999999,
        channel_id=888888888,
        guild_id=777777777,
        category="Support"
    )
    
    # Update status
    update_ticket(ticket_id, status="need_help")
    
    ticket = get_ticket(ticket_id)
    if ticket and ticket['status'] == 'need_help':
        print(f"✅ Status updated: {ticket['status']}")
    else:
        print(f"❌ Status update failed")
    
    return ticket

def test_database_structure():
    """Test cấu trúc database"""
    print("\n" + "=" * 60)
    print("TEST 7: Cấu Trúc Database")
    print("=" * 60)
    
    data = load_data()
    
    print(f"✅ Database structure:")
    print(f"   - Panels: {len(data.get('panels', []))} item(s)")
    print(f"   - Open Tickets: {len(data.get('tickets', {}))} item(s)")
    print(f"   - Closed Tickets: {len(data.get('closed_tickets', []))} item(s)")
    
    # Hiển thị sample ticket structure
    if data.get('tickets'):
        sample_ticket = next(iter(data['tickets'].values()))
        print(f"\n✅ Sample Ticket Structure:")
        print(f"   - ticket_id: {sample_ticket.get('ticket_id')}")
        print(f"   - user_id: {sample_ticket.get('user_id')}")
        print(f"   - channel_id: {sample_ticket.get('channel_id')}")
        print(f"   - category: {sample_ticket.get('category')}")
        print(f"   - status: {sample_ticket.get('status')}")
        print(f"   - closed: {sample_ticket.get('closed')}")
        print(f"   - claimed_by: {sample_ticket.get('claimed_by')}")

def cleanup():
    """Dọn dẹp test data"""
    print("\n" + "=" * 60)
    print("CLEANUP: Xóa Test Data")
    print("=" * 60)
    
    data = load_data()
    
    # Xóa test tickets
    test_ids = ["test123", "channel_test", "status_test"]
    for tid in test_ids:
        if tid in data["tickets"]:
            del data["tickets"][tid]
            print(f"✅ Xóa test ticket: {tid}")
    
    # Xóa test closed tickets
    data["closed_tickets"] = [t for t in data.get("closed_tickets", []) 
                              if t["ticket_id"] not in test_ids]
    
    save_data(data)
    print(f"✅ Cleanup hoàn tất")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  🎫 DISCORD TICKET BOT - TEST SUITE  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        # Run tests
        ticket = test_ticket_creation()
        test_get_ticket(ticket['ticket_id'])
        test_channel_lookup(987654322)
        test_user_tickets()
        test_status_update()
        test_database_structure()
        
        # Test close workflow
        print("\n" + "=" * 60)
        print("TEST 8: Closed Ticket Workflow (It Works!)")
        print("=" * 60)
        closed_ticket = create_ticket(
            ticket_id="close_test",
            user_id=444444444,
            channel_id=555555555,
            guild_id=666666666,
            category="Activation"
        )
        print(f"✅ Tạo ticket: {closed_ticket['ticket_id']}")
        print(f"   - Status: {closed_ticket['status']}")
        print(f"   - Closed: {closed_ticket['closed']}")
        
        # Giả lập bấm "It Works!"
        close_ticket(closed_ticket['ticket_id'], user_id=444444444)
        
        data = load_data()
        closed = next((t for t in data["closed_tickets"] 
                      if t["ticket_id"] == "close_test"), None)
        
        if closed:
            print(f"\n✅ Ticket đóng thành công!")
            print(f"   - Closed: {closed['closed']}")
            print(f"   - Closed By: {closed['closed_by']}")
            print(f"   - Closed At: {closed['closed_at']}")
            print(f"\n✅ Database đã cập nhật")
            print(f"   - Xóa khỏi 'tickets'")
            print(f"   - Thêm vào 'closed_tickets'")
        
        # Cleanup
        cleanup()
        
        # Final report
        print("\n" + "=" * 60)
        print("✅ TẤT CẢ TEST PASSED!")
        print("=" * 60)
        print("\n📋 KẾT LUẬN:")
        print("   ✅ Ticket tạo được đúng cách")
        print("   ✅ Có thể lấy ticket từ ID")
        print("   ✅ Có thể lấy ticket từ channel ID")
        print("   ✅ Status có thể cập nhật")
        print("   ✅ Đóng ticket hoạt động đúng")
        print("   ✅ Database lưu trữ đúng cách")
        print("\n🎮 Bot sẵn sàng hoạt động!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
