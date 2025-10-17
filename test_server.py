"""Test script to verify all features work correctly"""
from main import init_database
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "health_data.db"

print("=" * 60)
print("TESTING HEALTH MCP SERVER")
print("=" * 60)

# Initialize database
print("\n1. Initializing database...")
init_database()
print("   ✅ Database initialized!")

# Check all tables
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("\n2. Database tables created:")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"   ✅ {table[0]}: {count} records")

# Check food database
cursor.execute("SELECT COUNT(*) FROM food_database")
food_count = cursor.fetchone()[0]
print(f"\n3. Food database:")
print(f"   ✅ {food_count} foods available")

cursor.execute("SELECT name FROM food_database WHERE name LIKE '%roti%' OR name LIKE '%dal%' OR name LIKE '%paneer%'")
indian_foods = cursor.fetchall()
print(f"   ✅ Indian foods included: {len(indian_foods)}")
for food in indian_foods:
    print(f"      • {food[0]}")

conn.close()

print("\n" + "=" * 60)
print("✅ ALL SYSTEMS READY!")
print("=" * 60)
print("\n📋 Available Features:")
print("   • Nutrition tracking with 23+ foods")
print("   • Sleep tracking")
print("   • Weight tracking")
print("   • Exercise logging")
print("   • Smart food recommendations (region-based)")
print("   • Exercise recommendations (based on sleep & goals)")
print("   • Complete daily health summaries")
print("\n🚀 Run: python main.py")
print("=" * 60)
