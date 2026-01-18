import json
import os
from datetime import datetime
from typing import Dict, List, Optional

DATA_FILE = "data/tickets.json"

def ensure_data_file():
    """Đảm bảo file data tồn tại"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"panels": [], "tickets": {}, "closed_tickets": []}, f, indent=2)

def load_data() -> Dict:
    """Load dữ liệu từ JSON"""
    ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data: Dict):
    """Lưu dữ liệu vào JSON"""
    ensure_data_file()
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Panel Functions
def add_panel(message_id: int, channel_id: int, guild_id: int, category: str):
    """Thêm panel mới"""
    data = load_data()
    data["panels"].append({
        "message_id": message_id,
        "channel_id": channel_id,
        "guild_id": guild_id,
        "category": category,
        "created_at": datetime.now().isoformat()
    })
    save_data(data)

def get_panels(guild_id: int) -> List[Dict]:
    """Lấy danh sách panels của server"""
    data = load_data()
    return [p for p in data["panels"] if p["guild_id"] == guild_id]

# Ticket Functions
def create_ticket(
    ticket_id: str,
    user_id: int,
    channel_id: int,
    guild_id: int,
    category: str
) -> Dict:
    """Tạo ticket mới"""
    data = load_data()
    ticket = {
        "ticket_id": ticket_id,
        "user_id": user_id,
        "channel_id": channel_id,
        "guild_id": guild_id,
        "category": category,
        "claimed_by": None,
        "claimed_at": None,
        "created_at": datetime.now().isoformat(),
        "closed": False,
        "closed_at": None,
        "closed_by": None,
        "members": [user_id],
        "status": "open"
    }
    data["tickets"][ticket_id] = ticket
    save_data(data)
    return ticket

def get_ticket(ticket_id: str) -> Optional[Dict]:
    """Lấy thông tin ticket"""
    data = load_data()
    return data["tickets"].get(ticket_id)

def update_ticket(ticket_id: str, **kwargs):
    """Cập nhật thông tin ticket"""
    data = load_data()
    if ticket_id in data["tickets"]:
        data["tickets"][ticket_id].update(kwargs)
        save_data(data)

def claim_ticket(ticket_id: str, user_id: int):
    """Claim ticket"""
    data = load_data()
    if ticket_id in data["tickets"]:
        data["tickets"][ticket_id].update({
            "claimed_by": user_id,
            "claimed_at": datetime.now().isoformat()
        })
        save_data(data)

def close_ticket(ticket_id: str, user_id: int):
    """Đóng ticket"""
    data = load_data()
    if ticket_id in data["tickets"]:
        ticket = data["tickets"][ticket_id]
        ticket.update({
            "closed": True,
            "closed_at": datetime.now().isoformat(),
            "closed_by": user_id
        })
        data["closed_tickets"].append(ticket)
        del data["tickets"][ticket_id]
        save_data(data)

def get_user_tickets(user_id: int, guild_id: int) -> List[Dict]:
    """Lấy danh sách tickets của user"""
    data = load_data()
    return [t for t in data["tickets"].values() 
            if t["user_id"] == user_id and t["guild_id"] == guild_id and not t["closed"]]

def get_channel_ticket(channel_id: int) -> Optional[str]:
    """Lấy ticket ID từ channel ID"""
    data = load_data()
    for ticket_id, ticket in data["tickets"].items():
        if ticket["channel_id"] == channel_id:
            return ticket_id
    return None

def add_ticket_member(ticket_id: str, user_id: int):
    """Thêm member vào ticket"""
    data = load_data()
    if ticket_id in data["tickets"]:
        if user_id not in data["tickets"][ticket_id]["members"]:
            data["tickets"][ticket_id]["members"].append(user_id)
            save_data(data)

def remove_ticket_member(ticket_id: str, user_id: int):
    """Xóa member khỏi ticket"""
    data = load_data()
    if ticket_id in data["tickets"]:
        if user_id in data["tickets"][ticket_id]["members"]:
            data["tickets"][ticket_id]["members"].remove(user_id)
            save_data(data)
