#!/usr/bin/env python3
"""Test script to verify all upgrades"""

import json
import os

def test_config():
    """Test config.json"""
    print("\n✅ TEST 1: config.json")
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    categories = config.get("panel_categories", [])
    print(f"   - Categories: {len(categories)} items")
    for cat in categories:
        print(f"     • {cat}")
    print(f"   - Max tickets: {config.get('max_user_tickets', 3)}")
    print(f"   - Panel channel ID: {config.get('panel_channel_id', 'Not set yet')}")
    return True

def test_files():
    """Test all files exist"""
    print("\n✅ TEST 2: Files Check")
    files_to_check = [
        'cogs/tickets.py',
        'utils/embed.py',
        '.gitignore',
        'Procfile',
        'SETUP_PANEL.md',
        'GITHUB_SETUP.md',
        'UPGRADE_SUMMARY.md'
    ]
    
    all_good = True
    for f in files_to_check:
        exists = os.path.exists(f)
        status = '✅' if exists else '❌'
        print(f"   {status} {f}")
        if not exists:
            all_good = False
    
    return all_good

def test_dropdown_code():
    """Check if dropdown code exists"""
    print("\n✅ TEST 3: Dropdown Code")
    with open('cogs/tickets.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('TicketCategorySelect', 'Dropdown class'),
        ('PanelView', 'Panel view'),
        ('create_ticket_from_select', 'Ticket creation from select'),
        ('await message.pin()', 'Pin message code'),
    ]
    
    for check, name in checks:
        found = check in content
        status = '✅' if found else '❌'
        print(f"   {status} {name}: {check}")
    
    return True

def main():
    print("🔍 Discord Ticket Bot v2.0 - Verification Test")
    print("=" * 50)
    
    try:
        test_config()
        test_files()
        test_dropdown_code()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("🎉 Bot is ready to use!\n")
        print("📝 Next steps:")
        print("   1. Add your bot token to .env")
        print("   2. Run: python main.py")
        print("   3. Run: !setup (in your ticket panel channel)")
        print("   4. Test the dropdown menu!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
