"""
Demo script to test the nutrition tracking features
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "health_data.db"

def demo_nutrition_tracking():
    print("=" * 60)
    print("HEALTH MCP SERVER - NUTRITION TRACKING DEMO")
    print("=" * 60)
    print()
    
    # Check database was created
    if DB_PATH.exists():
        print("✓ Database created successfully!")
        print(f"  Location: {DB_PATH}")
        print()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check food database
        cursor.execute("SELECT COUNT(*) FROM food_database")
        food_count = cursor.fetchone()[0]
        print(f"✓ Food database initialized with {food_count} items")
        
        # Show some foods
        cursor.execute("SELECT name, calories, protein FROM food_database LIMIT 5")
        foods = cursor.fetchall()
        print("\n  Sample foods:")
        for name, cal, protein in foods:
            print(f"    • {name.title()}: {cal} cal, {protein}g protein")
        
        print()
        print("=" * 60)
        print("HOW IT WORKS:")
        print("=" * 60)
        print()
        print("1. LLM receives: 'I ate chicken breast and rice for lunch'")
        print()
        print("2. LLM calls: log_meal('chicken breast:150, brown rice:200')")
        print()
        print("3. Server automatically:")
        print("   - Looks up each food in database")
        print("   - Calculates nutrients based on quantity")
        print("   - Stores in meals table with timestamp")
        print("   - Returns nutrient breakdown")
        print()
        print("4. Result: '✓ Logged 495 calories, Protein: 54g, Carbs: 55g'")
        print()
        print("5. Later, call get_daily_nutrition() to see full day summary")
        print()
        
        conn.close()
    else:
        print("⚠️  Database not found. Run main.py first!")

if __name__ == "__main__":
    demo_nutrition_tracking()
