"""
Health MCP Server - Comprehensive Health Tracking with AI Recommendations

This MCP server provides 28 tools for complete health management:
- Nutrition tracking with 35+ foods (Indian & International)
- Sleep quality analysis
- Weight management with trends
- Exercise logging with calorie estimates
- Smart meal recommendations (region-aware, pantry-aware, time-aware)
- User profile & goals management

Perfect for LLM-driven health conversations: "I ate 2 rotis and dal" 
→ Automatically logs nutrition, suggests next meal, tracks progress.
"""

from fastmcp import FastMCP
import sqlite3
from datetime import datetime
from pathlib import Path

# Create health MCP server with detailed metadata
mcp = FastMCP(
    "Health Assistant",
    instructions="""You are a comprehensive health tracking assistant. You help users:
    
1. Track nutrition by logging meals and analyzing daily intake
2. Monitor sleep patterns and quality
3. Manage weight with trends and goals
4. Log exercises with calorie burn estimates
5. Provide personalized recommendations based on:
   - Daily calorie goals and consumption
   - Sleep quality and energy levels
   - Regional food preferences (India/International)
   - Available pantry items
   - Time-based food routines
   
When users describe what they ate, parse quantities and call log_meal().
When recommending foods, consider their region, goals, and what's available.
Always provide actionable insights and encourage healthy habits!
"""
)

# Database setup
DB_PATH = Path(__file__).parent / "health_data.db"

def init_database():
    """Initialize the SQLite database with necessary tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Food nutrition database (per 100g)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            calories REAL,
            protein REAL,
            carbs REAL,
            fats REAL,
            fiber REAL
        )
    """)
    
    # Meals log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            food_name TEXT NOT NULL,
            quantity_grams REAL NOT NULL,
            calories REAL,
            protein REAL,
            carbs REAL,
            fats REAL,
            fiber REAL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Sleep tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sleep_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            sleep_time TEXT NOT NULL,
            wake_time TEXT NOT NULL,
            hours REAL,
            quality TEXT,
            notes TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Weight tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weight_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            weight_kg REAL NOT NULL,
            notes TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User profile and goals
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            height_m REAL,
            target_weight_kg REAL,
            daily_calorie_goal REAL,
            activity_level TEXT,
            region TEXT,
            dietary_preferences TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Exercise log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercise_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            exercise_name TEXT NOT NULL,
            duration_minutes REAL,
            intensity TEXT,
            calories_burned REAL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User pantry/inventory
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_pantry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            available BOOLEAN DEFAULT 1,
            quantity_grams REAL,
            notes TEXT,
            last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (food_name) REFERENCES food_database(name)
        )
    """)
    
    # Food routines - time-based food availability/preferences
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_routines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            morning BOOLEAN DEFAULT 0,
            midday BOOLEAN DEFAULT 0,
            afternoon BOOLEAN DEFAULT 0,
            evening BOOLEAN DEFAULT 0,
            night BOOLEAN DEFAULT 0,
            latenight BOOLEAN DEFAULT 0,
            preparation_type TEXT,
            effort_level TEXT,
            typical_portion_grams REAL,
            preference_score INTEGER DEFAULT 5,
            notes TEXT,
            last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (food_name) REFERENCES food_database(name)
        )
    """)
    
    # Insert some common foods if table is empty
    cursor.execute("SELECT COUNT(*) FROM food_database")
    if cursor.fetchone()[0] == 0:
        common_foods = [
            # International foods
            ("chicken breast", 165, 31, 0, 3.6, 0),
            ("brown rice", 112, 2.6, 24, 0.9, 1.8),
            ("white rice", 130, 2.7, 28, 0.3, 0.4),
            ("broccoli", 34, 2.8, 7, 0.4, 2.6),
            ("banana", 89, 1.1, 23, 0.3, 2.6),
            ("apple", 52, 0.3, 14, 0.2, 2.4),
            ("salmon", 208, 20, 0, 13, 0),
            ("eggs", 155, 13, 1.1, 11, 0),
            ("oatmeal", 389, 17, 66, 7, 11),
            ("almonds", 579, 21, 22, 50, 12.5),
            ("sweet potato", 86, 1.6, 20, 0.1, 3),
            ("spinach", 23, 2.9, 3.6, 0.4, 2.2),
            ("greek yogurt", 59, 10, 3.6, 0.4, 0),
            ("avocado", 160, 2, 9, 15, 7),
            ("pasta", 131, 5, 25, 1.1, 1.8),
            ("beef", 250, 26, 0, 15, 0),
            # Indian foods
            ("roti", 297, 11, 45, 9, 4),
            ("dal", 116, 9, 20, 0.4, 8),
            ("paneer", 265, 18, 1.2, 20, 0),
            ("chapati", 120, 3.1, 18, 3.7, 2),
            ("idli", 58, 2, 12, 0.1, 0.3),
            ("dosa", 168, 4, 25, 6, 2),
            ("curd", 60, 3.5, 4.7, 3.3, 0),
            ("samosa", 252, 3.5, 23, 17, 2),
            # Additional Indian/common foods for routines
            ("bread", 265, 9, 49, 3.2, 2.7),
            ("jam", 278, 0.4, 69, 0.1, 1),
            ("poha", 110, 2, 23, 0.4, 2),
            ("paratha", 320, 6, 40, 15, 3),
            ("maggie", 400, 8, 60, 14, 2),
            ("chowmein", 138, 4.5, 20, 4.5, 2),
            ("fried rice", 130, 3, 20, 4, 1),
            ("chana", 164, 9, 27, 3, 8),
            ("ganne ka juice", 50, 0.2, 13, 0, 0),
            ("pakora", 180, 3.5, 18, 11, 2),
            ("cashews", 553, 18, 30, 44, 3.3),
        ]
        cursor.executemany(
            "INSERT INTO food_database (name, calories, protein, carbs, fats, fiber) VALUES (?, ?, ?, ?, ?, ?)",
            common_foods
        )
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """Calculate Body Mass Index (BMI) from weight and height.
    
    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters
    """
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return f"BMI: {bmi:.1f} - Category: {category}"

@mcp.tool()
def daily_water_intake(weight_kg: float) -> str:
    """Calculate recommended daily water intake based on body weight.
    
    Args:
        weight_kg: Weight in kilograms
    """
    # Simple formula: 30-35ml per kg of body weight
    min_water = weight_kg * 30
    max_water = weight_kg * 35
    
    return f"Recommended daily water intake: {min_water:.0f}-{max_water:.0f} ml ({min_water/1000:.1f}-{max_water/1000:.1f} liters)"

@mcp.tool()
def steps_to_calories(steps: int, weight_kg: float = 70) -> str:
    """Estimate calories burned from walking steps.
    
    Args:
        steps: Number of steps taken
        weight_kg: Body weight in kilograms (default: 70)
    """
    # Rough estimate: 0.04 calories per step per kg
    calories = steps * 0.04 * (weight_kg / 70)
    
    return f"{steps} steps burned approximately {calories:.0f} calories"

@mcp.tool()
def heart_rate_zone(age: int, resting_hr: int = 60) -> str:
    """Calculate heart rate training zones based on age.
    
    Args:
        age: Age in years
        resting_hr: Resting heart rate (default: 60 bpm)
    """
    max_hr = 220 - age
    hr_reserve = max_hr - resting_hr
    
    zones = {
        "Easy (50-60%)": (resting_hr + hr_reserve * 0.5, resting_hr + hr_reserve * 0.6),
        "Moderate (60-70%)": (resting_hr + hr_reserve * 0.6, resting_hr + hr_reserve * 0.7),
        "Hard (70-80%)": (resting_hr + hr_reserve * 0.7, resting_hr + hr_reserve * 0.8),
        "Very Hard (80-90%)": (resting_hr + hr_reserve * 0.8, resting_hr + hr_reserve * 0.9),
    }
    
    result = f"Max Heart Rate: {max_hr} bpm\n\nTraining Zones:\n"
    for zone_name, (low, high) in zones.items():
        result += f"  {zone_name}: {low:.0f}-{high:.0f} bpm\n"
    
    return result

# ==== NUTRITION TRACKING TOOLS ====

@mcp.tool()
def list_foods() -> str:
    """List all available foods in the nutrition database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, calories, protein, carbs, fats, fiber FROM food_database ORDER BY name")
    foods = cursor.fetchall()
    conn.close()
    
    if not foods:
        return "No foods found in database."
    
    result = "Available Foods (per 100g):\n\n"
    for name, cal, protein, carbs, fats, fiber in foods:
        result += f"• {name.title()}: {cal}cal, P:{protein}g, C:{carbs}g, F:{fats}g, Fiber:{fiber}g\n"
    
    return result

@mcp.tool()
def log_meal(food_items: str, date: str = None) -> str:
    """Log a meal by breaking it down into nutrients and storing in database.
    
    The LLM should parse the user's description and provide food items in format:
    "food_name1:quantity_grams, food_name2:quantity_grams"
    
    Args:
        food_items: Comma-separated list of "food:quantity" (e.g., "chicken breast:150, brown rice:200")
        date: Date in YYYY-MM-DD format (default: today)
    
    Example: log_meal("chicken breast:150, brown rice:100, broccoli:80")
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    result = f"Meal logged for {date}:\n\n"
    total_nutrients = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0, "fiber": 0}
    
    # Parse food items
    items = [item.strip() for item in food_items.split(",")]
    
    for item in items:
        try:
            food_name, quantity = item.split(":")
            food_name = food_name.strip().lower()
            quantity = float(quantity.strip())
            
            # Get nutrition info from database
            cursor.execute(
                "SELECT calories, protein, carbs, fats, fiber FROM food_database WHERE name = ?",
                (food_name,)
            )
            nutrition = cursor.fetchone()
            
            if not nutrition:
                result += f"⚠️  '{food_name}' not found in database. Skipped.\n"
                continue
            
            # Calculate nutrients for the given quantity (database is per 100g)
            multiplier = quantity / 100
            calories = nutrition[0] * multiplier
            protein = nutrition[1] * multiplier
            carbs = nutrition[2] * multiplier
            fats = nutrition[3] * multiplier
            fiber = nutrition[4] * multiplier
            
            # Insert into meals table
            cursor.execute("""
                INSERT INTO meals (date, food_name, quantity_grams, calories, protein, carbs, fats, fiber)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (date, food_name, quantity, calories, protein, carbs, fats, fiber))
            
            # Add to totals
            total_nutrients["calories"] += calories
            total_nutrients["protein"] += protein
            total_nutrients["carbs"] += carbs
            total_nutrients["fats"] += fats
            total_nutrients["fiber"] += fiber
            
            result += f"✓ {food_name.title()} ({quantity}g): {calories:.0f}cal, P:{protein:.1f}g, C:{carbs:.1f}g, F:{fats:.1f}g\n"
            
        except ValueError:
            result += f"⚠️  Invalid format for item: '{item}'. Use 'food:quantity'\n"
    
    conn.commit()
    conn.close()
    
    result += f"\n📊 TOTAL: {total_nutrients['calories']:.0f} calories, "
    result += f"Protein: {total_nutrients['protein']:.1f}g, "
    result += f"Carbs: {total_nutrients['carbs']:.1f}g, "
    result += f"Fats: {total_nutrients['fats']:.1f}g, "
    result += f"Fiber: {total_nutrients['fiber']:.1f}g"
    
    return result

@mcp.tool()
def get_daily_nutrition(date: str = None) -> str:
    """Get total nutrition intake for a specific day.
    
    Args:
        date: Date in YYYY-MM-DD format (default: today)
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all meals for the day
    cursor.execute("""
        SELECT food_name, quantity_grams, calories, protein, carbs, fats, fiber, timestamp
        FROM meals WHERE date = ?
        ORDER BY timestamp
    """, (date,))
    
    meals = cursor.fetchall()
    conn.close()
    
    if not meals:
        return f"No meals logged for {date}"
    
    result = f"📅 Nutrition Summary for {date}\n\n"
    result += "Meals logged:\n"
    
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0, "fiber": 0}
    
    for food, qty, cal, protein, carbs, fats, fiber, timestamp in meals:
        time = timestamp.split()[1][:5]  # Get HH:MM
        result += f"  • {time} - {food.title()} ({qty}g): {cal:.0f}cal, P:{protein:.1f}g, C:{carbs:.1f}g, F:{fats:.1f}g\n"
        
        totals["calories"] += cal
        totals["protein"] += protein
        totals["carbs"] += carbs
        totals["fats"] += fats
        totals["fiber"] += fiber
    
    result += f"\n{'='*50}\n"
    result += f"📊 DAILY TOTALS:\n"
    result += f"  Calories: {totals['calories']:.0f} kcal\n"
    result += f"  Protein:  {totals['protein']:.1f}g ({totals['protein']*4:.0f} kcal, {totals['protein']*4/totals['calories']*100:.0f}%)\n"
    result += f"  Carbs:    {totals['carbs']:.1f}g ({totals['carbs']*4:.0f} kcal, {totals['carbs']*4/totals['calories']*100:.0f}%)\n"
    result += f"  Fats:     {totals['fats']:.1f}g ({totals['fats']*9:.0f} kcal, {totals['fats']*9/totals['calories']*100:.0f}%)\n"
    result += f"  Fiber:    {totals['fiber']:.1f}g\n"
    
    return result

@mcp.tool()
def add_food_to_database(name: str, calories: float, protein: float, carbs: float, fats: float, fiber: float = 0) -> str:
    """Add a new food item to the nutrition database (values per 100g).
    
    Args:
        name: Name of the food
        calories: Calories per 100g
        protein: Protein in grams per 100g
        carbs: Carbohydrates in grams per 100g
        fats: Fats in grams per 100g
        fiber: Fiber in grams per 100g (optional)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO food_database (name, calories, protein, carbs, fats, fiber)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name.lower(), calories, protein, carbs, fats, fiber))
        conn.commit()
        result = f"✓ Added '{name}' to food database: {calories}cal, P:{protein}g, C:{carbs}g, F:{fats}g, Fiber:{fiber}g (per 100g)"
    except sqlite3.IntegrityError:
        result = f"⚠️  '{name}' already exists in the database."
    finally:
        conn.close()
    
    return result

@mcp.tool()
def get_nutrition_stats(days: int = 7) -> str:
    """Get nutrition statistics for the last N days.
    
    Args:
        days: Number of days to analyze (default: 7)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT date,
               SUM(calories) as total_cal,
               SUM(protein) as total_protein,
               SUM(carbs) as total_carbs,
               SUM(fats) as total_fats,
               SUM(fiber) as total_fiber
        FROM meals
        WHERE date >= date('now', '-' || ? || ' days')
        GROUP BY date
        ORDER BY date DESC
    """, (days,))
    
    stats = cursor.fetchall()
    conn.close()
    
    if not stats:
        return f"No nutrition data found for the last {days} days."
    
    result = f"📈 Nutrition Stats for Last {days} Days:\n\n"
    
    avg_cal, avg_protein, avg_carbs, avg_fats, avg_fiber = 0, 0, 0, 0, 0
    
    for date, cal, protein, carbs, fats, fiber in stats:
        result += f"{date}: {cal:.0f} kcal | P:{protein:.0f}g | C:{carbs:.0f}g | F:{fats:.0f}g | Fiber:{fiber:.0f}g\n"
        avg_cal += cal
        avg_protein += protein
        avg_carbs += carbs
        avg_fats += fats
        avg_fiber += fiber
    
    days_count = len(stats)
    result += f"\n{'='*50}\n"
    result += f"📊 Averages over {days_count} days:\n"
    result += f"  Calories: {avg_cal/days_count:.0f} kcal/day\n"
    result += f"  Protein:  {avg_protein/days_count:.0f}g/day\n"
    result += f"  Carbs:    {avg_carbs/days_count:.0f}g/day\n"
    result += f"  Fats:     {avg_fats/days_count:.0f}g/day\n"
    result += f"  Fiber:    {avg_fiber/days_count:.0f}g/day\n"
    
    return result

# ==== SLEEP TRACKING TOOLS ====

@mcp.tool()
def log_sleep(sleep_time: str, wake_time: str, date: str = None, quality: str = "good", notes: str = "") -> str:
    """Log sleep information - when you slept and when you woke up.
    
    Args:
        sleep_time: Time you went to sleep (HH:MM format, e.g., "23:30")
        wake_time: Time you woke up (HH:MM format, e.g., "07:00")
        date: Date in YYYY-MM-DD format (default: today)
        quality: Sleep quality: "excellent", "good", "fair", "poor" (default: "good")
        notes: Optional notes about sleep
    
    Example: log_sleep("23:00", "07:00") - slept 8 hours
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Calculate sleep hours
    from datetime import datetime as dt
    try:
        sleep_dt = dt.strptime(sleep_time, "%H:%M")
        wake_dt = dt.strptime(wake_time, "%H:%M")
        
        # Handle sleep across midnight
        if wake_dt < sleep_dt:
            hours = (24 - sleep_dt.hour + wake_dt.hour) + (wake_dt.minute - sleep_dt.minute) / 60
        else:
            hours = (wake_dt.hour - sleep_dt.hour) + (wake_dt.minute - sleep_dt.minute) / 60
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sleep_log (date, sleep_time, wake_time, hours, quality, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, sleep_time, wake_time, hours, quality, notes))
        
        conn.commit()
        conn.close()
        
        quality_emoji = {"excellent": "😴✨", "good": "😊", "fair": "😐", "poor": "😞"}.get(quality, "😊")
        
        return f"✓ Sleep logged for {date}:\n  Slept: {sleep_time}\n  Woke: {wake_time}\n  Duration: {hours:.1f} hours\n  Quality: {quality} {quality_emoji}\n  {notes if notes else ''}"
    
    except ValueError:
        return "⚠️ Invalid time format. Please use HH:MM format (e.g., '23:30')"

@mcp.tool()
def get_sleep_summary(days: int = 7) -> str:
    """Get sleep summary for the last N days.
    
    Args:
        days: Number of days to analyze (default: 7)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT date, sleep_time, wake_time, hours, quality
        FROM sleep_log
        WHERE date >= date('now', '-' || ? || ' days')
        ORDER BY date DESC
    """, (days,))
    
    logs = cursor.fetchall()
    conn.close()
    
    if not logs:
        return f"No sleep data found for the last {days} days."
    
    result = f"😴 Sleep Summary for Last {days} Days:\n\n"
    total_hours = 0
    
    for date, sleep, wake, hours, quality in logs:
        quality_emoji = {"excellent": "✨", "good": "😊", "fair": "😐", "poor": "😞"}.get(quality, "")
        result += f"{date}: {sleep} → {wake} ({hours:.1f}h) {quality_emoji}\n"
        total_hours += hours
    
    avg_hours = total_hours / len(logs)
    result += f"\n📊 Average: {avg_hours:.1f} hours/night\n"
    
    if avg_hours >= 7 and avg_hours <= 9:
        result += "✅ Great! You're getting optimal sleep!"
    elif avg_hours < 7:
        result += "⚠️ You might need more sleep for optimal health (7-9 hours recommended)"
    else:
        result += "💤 You're sleeping a lot! Make sure it's quality sleep."
    
    return result

# ==== WEIGHT TRACKING TOOLS ====

@mcp.tool()
def log_weight(weight_kg: float, date: str = None, notes: str = "") -> str:
    """Log your weight for tracking progress.
    
    Args:
        weight_kg: Your weight in kilograms
        date: Date in YYYY-MM-DD format (default: today)
        notes: Optional notes
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO weight_log (date, weight_kg, notes)
        VALUES (?, ?, ?)
    """, (date, weight_kg, notes))
    
    conn.commit()
    
    # Get weight trend
    cursor.execute("""
        SELECT weight_kg FROM weight_log
        WHERE date < ?
        ORDER BY date DESC LIMIT 1
    """, (date,))
    
    prev = cursor.fetchone()
    conn.close()
    
    result = f"✓ Weight logged: {weight_kg} kg on {date}"
    if prev:
        diff = weight_kg - prev[0]
        if diff > 0:
            result += f"\n  ⬆️ +{diff:.1f} kg from last entry"
        elif diff < 0:
            result += f"\n  ⬇️ {diff:.1f} kg from last entry"
        else:
            result += f"\n  ➡️ No change from last entry"
    
    return result

@mcp.tool()
def get_weight_trend(days: int = 30) -> str:
    """Get weight trend over time.
    
    Args:
        days: Number of days to analyze (default: 30)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT date, weight_kg FROM weight_log
        WHERE date >= date('now', '-' || ? || ' days')
        ORDER BY date DESC
    """, (days,))
    
    logs = cursor.fetchall()
    conn.close()
    
    if not logs:
        return f"No weight data found for the last {days} days."
    
    result = f"⚖️ Weight Trend (Last {days} Days):\n\n"
    
    for date, weight in logs:
        result += f"{date}: {weight:.1f} kg\n"
    
    if len(logs) >= 2:
        change = logs[0][1] - logs[-1][1]
        result += f"\n📊 Overall change: "
        if change > 0:
            result += f"+{change:.1f} kg (gained)"
        elif change < 0:
            result += f"{change:.1f} kg (lost)"
        else:
            result += "No change"
    
    return result

# ==== USER PROFILE & GOALS ====

@mcp.tool()
def set_user_profile(height_m: float = None, target_weight_kg: float = None, 
                     daily_calorie_goal: float = None, activity_level: str = None,
                     region: str = None, dietary_preferences: str = None) -> str:
    """Set or update user profile and goals.
    
    Args:
        height_m: Height in meters (e.g., 1.75)
        target_weight_kg: Target weight in kg
        daily_calorie_goal: Daily calorie goal
        activity_level: "sedentary", "light", "moderate", "active", "very_active"
        region: Your region (e.g., "India", "USA", "Europe")
        dietary_preferences: e.g., "vegetarian", "vegan", "no-restrictions"
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if profile exists
    cursor.execute("SELECT COUNT(*) FROM user_profile")
    exists = cursor.fetchone()[0] > 0
    
    if exists:
        # Update existing profile
        updates = []
        values = []
        if height_m: 
            updates.append("height_m = ?")
            values.append(height_m)
        if target_weight_kg:
            updates.append("target_weight_kg = ?")
            values.append(target_weight_kg)
        if daily_calorie_goal:
            updates.append("daily_calorie_goal = ?")
            values.append(daily_calorie_goal)
        if activity_level:
            updates.append("activity_level = ?")
            values.append(activity_level)
        if region:
            updates.append("region = ?")
            values.append(region)
        if dietary_preferences:
            updates.append("dietary_preferences = ?")
            values.append(dietary_preferences)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        
        if updates:
            query = f"UPDATE user_profile SET {', '.join(updates)} WHERE id = 1"
            cursor.execute(query, values)
    else:
        # Insert new profile
        cursor.execute("""
            INSERT INTO user_profile 
            (height_m, target_weight_kg, daily_calorie_goal, activity_level, region, dietary_preferences)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (height_m, target_weight_kg, daily_calorie_goal, activity_level, region, dietary_preferences))
    
    conn.commit()
    conn.close()
    
    return f"✓ Profile updated successfully!\n  Height: {height_m}m\n  Target: {target_weight_kg}kg\n  Calorie Goal: {daily_calorie_goal} kcal\n  Activity: {activity_level}\n  Region: {region}\n  Diet: {dietary_preferences}"

@mcp.tool()
def get_user_profile() -> str:
    """Get current user profile and goals."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1")
    profile = cursor.fetchone()
    conn.close()
    
    if not profile:
        return "❌ No profile found. Use set_user_profile() to create one."
    
    _, height, target, cal_goal, activity, region, diet, updated = profile
    
    result = "👤 Your Profile:\n\n"
    if height: result += f"  Height: {height}m\n"
    if target: result += f"  Target Weight: {target}kg\n"
    if cal_goal: result += f"  Daily Calorie Goal: {cal_goal} kcal\n"
    if activity: result += f"  Activity Level: {activity}\n"
    if region: result += f"  Region: {region}\n"
    if diet: result += f"  Dietary Preferences: {diet}\n"
    result += f"\n  Last Updated: {updated}"
    
    return result

# ==== SMART RECOMMENDATIONS ====

@mcp.tool()
def recommend_foods(meal_type: str = "lunch", pantry_only: bool = False) -> str:
    """Recommend foods based on daily calorie goal, what you've eaten today, and your region.
    
    Args:
        meal_type: "breakfast", "lunch", "dinner", or "snack"
        pantry_only: If True, only recommend from foods in your pantry
    """
    # If user wants pantry-only recommendations, use that tool
    if pantry_only:
        return recommend_from_pantry(meal_type)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get user profile
    cursor.execute("SELECT daily_calorie_goal, region, dietary_preferences FROM user_profile ORDER BY id DESC LIMIT 1")
    profile = cursor.fetchone()
    
    if not profile or not profile[0]:
        conn.close()
        return "❌ Please set your daily calorie goal first using set_user_profile()"
    
    cal_goal, region, diet_pref = profile
    
    # Get today's consumption
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT SUM(calories) FROM meals WHERE date = ?
    """, (today,))
    
    consumed = cursor.fetchone()[0] or 0
    remaining = cal_goal - consumed
    
    # Get available foods from region
    region_lower = region.lower() if region else ""
    
    result = f"🍽️ Food Recommendations for {meal_type.title()}:\n\n"
    result += f"📊 Today's Status:\n"
    result += f"  Goal: {cal_goal:.0f} kcal\n"
    result += f"  Consumed: {consumed:.0f} kcal\n"
    result += f"  Remaining: {remaining:.0f} kcal\n\n"
    
    # Meal calorie targets
    meal_targets = {
        "breakfast": 0.25,
        "lunch": 0.35,
        "dinner": 0.30,
        "snack": 0.10
    }
    
    target_calories = cal_goal * meal_targets.get(meal_type, 0.30)
    result += f"🎯 Target for {meal_type}: ~{target_calories:.0f} kcal\n\n"
    
    # Region-based recommendations
    if "india" in region_lower:
        recommendations = {
            "breakfast": [
                ("idli:150, sambar:100", "Light and healthy South Indian"),
                ("oatmeal:50, banana:100, almonds:10", "Nutritious balanced meal"),
                ("chapati:2, curd:100, dal:50", "Traditional North Indian"),
            ],
            "lunch": [
                ("brown rice:150, dal:100, chicken breast:100", "High protein balanced meal"),
                ("roti:3, paneer:80, spinach:100", "Vegetarian protein-rich"),
                ("white rice:150, dal:100, curd:100", "Light vegetarian meal"),
            ],
            "dinner": [
                ("chapati:2, dal:100, spinach:50", "Light dinner"),
                ("brown rice:100, chicken breast:120, broccoli:80", "Protein-focused"),
                ("idli:100, sambar:100", "Light South Indian"),
            ],
            "snack": [
                ("banana:100", "Quick energy"),
                ("almonds:20", "Healthy fats"),
                ("apple:150", "Low calorie fruit"),
            ]
        }
    else:
        recommendations = {
            "breakfast": [
                ("oatmeal:60, banana:100, almonds:10", "Balanced breakfast"),
                ("eggs:100, brown rice:80", "High protein"),
                ("greek yogurt:150, banana:100", "Quick and healthy"),
            ],
            "lunch": [
                ("chicken breast:150, brown rice:150, broccoli:100", "Balanced lunch"),
                ("salmon:120, sweet potato:150, spinach:80", "Omega-3 rich"),
                ("pasta:100, chicken breast:100, spinach:50", "Moderate carbs"),
            ],
            "dinner": [
                ("chicken breast:120, sweet potato:100, broccoli:80", "Light dinner"),
                ("salmon:100, brown rice:100, spinach:100", "Healthy fats"),
                ("eggs:100, avocado:50, spinach:80", "Low carb option"),
            ],
            "snack": [
                ("banana:100", "Quick snack"),
                ("almonds:20", "Healthy fats"),
                ("apple:150, almonds:10", "Fruit & nuts"),
            ]
        }
    
    meal_options = recommendations.get(meal_type, recommendations["lunch"])
    
    result += "Suggested meals:\n\n"
    for i, (meal, desc) in enumerate(meal_options, 1):
        result += f"{i}. {desc}:\n"
        result += f"   Foods: {meal}\n"
        result += f"   💡 Use: log_meal(\"{meal}\")\n\n"
    
    if remaining < 500 and meal_type != "snack":
        result += "⚠️ Low remaining calories! Consider lighter options or adjust your goal.\n"
    
    conn.close()
    return result

@mcp.tool()
def recommend_exercise() -> str:
    """Recommend exercises based on your activity level, sleep, and goals to stay healthy and energetic."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get user profile
    cursor.execute("SELECT activity_level, target_weight_kg FROM user_profile ORDER BY id DESC LIMIT 1")
    profile = cursor.fetchone()
    
    # Get latest weight
    cursor.execute("SELECT weight_kg FROM weight_log ORDER BY date DESC LIMIT 1")
    weight_data = cursor.fetchone()
    
    # Get sleep data
    cursor.execute("""
        SELECT AVG(hours), quality FROM sleep_log
        WHERE date >= date('now', '-7 days')
    """)
    sleep_data = cursor.fetchone()
    
    conn.close()
    
    result = "💪 Exercise Recommendations:\n\n"
    
    # Analyze sleep
    if sleep_data and sleep_data[0]:
        avg_sleep = sleep_data[0]
        result += f"😴 Sleep: {avg_sleep:.1f} hours/night average\n"
        if avg_sleep < 6:
            result += "   ⚠️ Low energy expected - Focus on light exercises\n"
            intensity = "light"
        elif avg_sleep < 7:
            result += "   💡 Moderate energy - Light to moderate exercise\n"
            intensity = "moderate"
        else:
            result += "   ✅ Good energy - You can do intense workouts!\n"
            intensity = "high"
    else:
        intensity = "moderate"
        result += "💤 No sleep data - Recommending moderate exercises\n"
    
    result += "\n"
    
    # Weight management goal
    if profile and weight_data and profile[1]:
        current = weight_data[0]
        target = profile[1]
        if current > target:
            goal = "weight_loss"
            result += f"🎯 Goal: Weight loss ({current:.1f}kg → {target:.1f}kg)\n\n"
        elif current < target:
            goal = "weight_gain"
            result += f"🎯 Goal: Weight gain ({current:.1f}kg → {target:.1f}kg)\n\n"
        else:
            goal = "maintenance"
            result += f"🎯 Goal: Maintain weight ({current:.1f}kg)\n\n"
    else:
        goal = "health"
        result += "🎯 Goal: General health and energy\n\n"
    
    # Recommend exercises
    result += "📋 Recommended Exercises:\n\n"
    
    if intensity == "light":
        result += "1. Walking (30 mins)\n   - Easy on joints\n   - Burns ~150 cal\n   - Boosts energy\n\n"
        result += "2. Yoga/Stretching (20 mins)\n   - Improves flexibility\n   - Reduces stress\n   - Enhances sleep quality\n\n"
        result += "3. Light Cycling (20 mins)\n   - Low impact\n   - Cardiovascular health\n   - Burns ~120 cal\n\n"
    
    elif intensity == "moderate":
        result += "1. Brisk Walking/Jogging (30 mins)\n   - Burns ~250 cal\n   - Cardio health\n   - Energizing\n\n"
        result += "2. Bodyweight Exercises (20 mins)\n   - Push-ups, squats, planks\n   - Builds strength\n   - Burns ~180 cal\n\n"
        result += "3. Swimming/Cycling (30 mins)\n   - Full body workout\n   - Low impact\n   - Burns ~300 cal\n\n"
    
    else:  # high intensity
        result += "1. Running (30-40 mins)\n   - Burns ~400 cal\n   - Great cardio\n   - Builds endurance\n\n"
        result += "2. HIIT Training (20 mins)\n   - High calorie burn (~300 cal)\n   - Boosts metabolism\n   - Time efficient\n\n"
        result += "3. Strength Training (40 mins)\n   - Builds muscle\n   - Burns ~250 cal\n   - Increases metabolism\n\n"
    
    result += "💡 Tips:\n"
    result += "  - Exercise in morning for better energy\n"
    result += "  - Stay hydrated (2-3L water/day)\n"
    result += "  - Rest 1-2 days per week\n"
    result += "  - Track with: log_exercise()\n"
    
    return result

@mcp.tool()
def log_exercise(exercise_name: str, duration_minutes: float, intensity: str = "moderate", date: str = None) -> str:
    """Log your exercise/workout.
    
    Args:
        exercise_name: Name of exercise (e.g., "running", "yoga", "gym")
        duration_minutes: Duration in minutes
        intensity: "light", "moderate", "intense"
        date: Date in YYYY-MM-DD format (default: today)
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Estimate calories burned (rough estimates)
    calorie_rates = {
        "light": 3,      # 3 cal/min
        "moderate": 6,   # 6 cal/min
        "intense": 10    # 10 cal/min
    }
    
    rate = calorie_rates.get(intensity, 6)
    calories_burned = duration_minutes * rate
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO exercise_log (date, exercise_name, duration_minutes, intensity, calories_burned)
        VALUES (?, ?, ?, ?, ?)
    """, (date, exercise_name, duration_minutes, intensity, calories_burned))
    
    conn.commit()
    conn.close()
    
    return f"✓ Exercise logged!\n  {exercise_name.title()}: {duration_minutes} min ({intensity})\n  🔥 Estimated calories burned: ~{calories_burned:.0f} kcal"

@mcp.tool()
def get_daily_summary(date: str = None) -> str:
    """Get complete health summary for a day - meals, sleep, exercise, weight.
    
    Args:
        date: Date in YYYY-MM-DD format (default: today)
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    result = f"📅 Health Summary for {date}\n"
    result += "=" * 50 + "\n\n"
    
    # Meals
    cursor.execute("""
        SELECT SUM(calories), SUM(protein), SUM(carbs), SUM(fats)
        FROM meals WHERE date = ?
    """, (date,))
    
    meal_data = cursor.fetchone()
    if meal_data and meal_data[0]:
        cal, protein, carbs, fats = meal_data
        result += f"🍽️ NUTRITION:\n"
        result += f"  Calories: {cal:.0f} kcal\n"
        result += f"  Protein: {protein:.1f}g | Carbs: {carbs:.1f}g | Fats: {fats:.1f}g\n\n"
    else:
        result += "🍽️ NUTRITION: No meals logged\n\n"
    
    # Sleep
    cursor.execute("""
        SELECT sleep_time, wake_time, hours, quality
        FROM sleep_log WHERE date = ?
    """, (date,))
    
    sleep_data = cursor.fetchone()
    if sleep_data:
        sleep, wake, hours, quality = sleep_data
        result += f"😴 SLEEP:\n"
        result += f"  {sleep} → {wake} ({hours:.1f} hours)\n"
        result += f"  Quality: {quality}\n\n"
    else:
        result += "😴 SLEEP: Not logged\n\n"
    
    # Exercise
    cursor.execute("""
        SELECT exercise_name, duration_minutes, calories_burned
        FROM exercise_log WHERE date = ?
    """, (date,))
    
    exercises = cursor.fetchall()
    if exercises:
        result += "💪 EXERCISE:\n"
        total_cal_burned = 0
        for name, duration, cal in exercises:
            result += f"  • {name.title()}: {duration:.0f} min (~{cal:.0f} kcal)\n"
            total_cal_burned += cal
        result += f"  Total burned: ~{total_cal_burned:.0f} kcal\n\n"
    else:
        result += "💪 EXERCISE: No exercise logged\n\n"
    
    # Weight
    cursor.execute("""
        SELECT weight_kg FROM weight_log WHERE date = ?
    """, (date,))
    
    weight_data = cursor.fetchone()
    if weight_data:
        result += f"⚖️ WEIGHT: {weight_data[0]:.1f} kg\n\n"
    else:
        result += "⚖️ WEIGHT: Not logged\n\n"
    
    # Net calories
    if meal_data and meal_data[0] and exercises:
        net_cal = meal_data[0] - sum(e[2] for e in exercises)
        result += f"📊 NET CALORIES: {net_cal:.0f} kcal\n"
    
    conn.close()
    return result

# ==== PANTRY MANAGEMENT TOOLS ====

@mcp.tool()
def add_to_pantry(food_name: str, quantity_grams: float = None, notes: str = "") -> str:
    """Add food to your available pantry inventory.
    
    Args:
        food_name: Name of food (must exist in food_database)
        quantity_grams: Optional quantity available (in grams)
        notes: Optional notes ("expires 10/25", "frozen", "need to buy more")
    
    Example: add_to_pantry("chicken breast", 500, "in freezer")
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verify food exists in database
    cursor.execute("SELECT name FROM food_database WHERE name = ?", (food_name.lower(),))
    if not cursor.fetchone():
        conn.close()
        return f"⚠️ '{food_name}' not in food database. Add it first with add_food_to_database()"
    
    # Check if already in pantry
    cursor.execute("SELECT id FROM user_pantry WHERE food_name = ?", (food_name.lower(),))
    existing = cursor.fetchone()
    
    if existing:
        # Update existing entry
        cursor.execute("""
            UPDATE user_pantry 
            SET available = 1, quantity_grams = ?, notes = ?, last_updated = CURRENT_TIMESTAMP
            WHERE food_name = ?
        """, (quantity_grams, notes, food_name.lower()))
        result = f"✓ Updated '{food_name}' in pantry"
    else:
        # Insert new entry
        cursor.execute("""
            INSERT INTO user_pantry (food_name, quantity_grams, notes)
            VALUES (?, ?, ?)
        """, (food_name.lower(), quantity_grams, notes))
        result = f"✓ Added '{food_name}' to pantry"
    
    if quantity_grams:
        result += f"\n  Quantity: {quantity_grams}g"
    if notes:
        result += f"\n  Notes: {notes}"
    
    conn.commit()
    conn.close()
    return result


@mcp.tool()
def remove_from_pantry(food_name: str) -> str:
    """Remove food from your pantry (mark as unavailable)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM user_pantry WHERE food_name = ?", (food_name.lower(),))
    
    if cursor.rowcount > 0:
        result = f"✓ Removed '{food_name}' from pantry"
    else:
        result = f"⚠️ '{food_name}' was not in your pantry"
    
    conn.commit()
    conn.close()
    return result


@mcp.tool()
def list_my_pantry() -> str:
    """List all foods currently in your pantry with quantities and notes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.food_name, p.quantity_grams, p.notes, p.last_updated,
               f.calories, f.protein, f.carbs, f.fats
        FROM user_pantry p
        JOIN food_database f ON p.food_name = f.name
        WHERE p.available = 1
        ORDER BY p.last_updated DESC
    """)
    
    items = cursor.fetchall()
    conn.close()
    
    if not items:
        return "🍽️ Your pantry is empty!\n💡 Add foods with: add_to_pantry()"
    
    result = "🍽️ Your Pantry Inventory:\n\n"
    
    for food, qty, notes, updated, cal, protein, carbs, fats in items:
        result += f"• {food.title()}"
        if qty:
            result += f" ({qty}g available)"
        result += f"\n  Nutrition (per 100g): {cal}cal, P:{protein}g, C:{carbs}g, F:{fats}g"
        if notes:
            result += f"\n  📝 {notes}"
        result += f"\n  Last updated: {updated[:10]}\n\n"
    
    return result


@mcp.tool()
def recommend_from_pantry(meal_type: str = "lunch") -> str:
    """Recommend meals using ONLY foods available in your pantry.
    
    Args:
        meal_type: "breakfast", "lunch", "dinner", or "snack"
    
    This considers:
    - Only foods in your pantry
    - Your calorie goals and what you've eaten today
    - Your region preferences
    - Available quantities (warns if insufficient)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get user profile
    cursor.execute("SELECT daily_calorie_goal, region FROM user_profile ORDER BY id DESC LIMIT 1")
    profile = cursor.fetchone()
    
    if not profile or not profile[0]:
        conn.close()
        return "❌ Please set your daily calorie goal first using set_user_profile()"
    
    cal_goal, region = profile
    
    # Get today's consumption
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT SUM(calories) FROM meals WHERE date = ?", (today,))
    consumed = cursor.fetchone()[0] or 0
    remaining = cal_goal - consumed
    
    # Get available pantry foods
    cursor.execute("""
        SELECT p.food_name, p.quantity_grams
        FROM user_pantry p
        WHERE p.available = 1
    """)
    
    pantry_items = cursor.fetchall()
    conn.close()
    
    if not pantry_items:
        return "🍽️ Your pantry is empty! Add foods with add_to_pantry() first."
    
    result = f"🍽️ Meal Recommendations from YOUR PANTRY ({meal_type.title()}):\n\n"
    result += f"📊 Today: {consumed:.0f}/{cal_goal:.0f} kcal consumed, {remaining:.0f} remaining\n\n"
    
    # Meal calorie targets
    meal_targets = {
        "breakfast": 0.25,
        "lunch": 0.35,
        "dinner": 0.30,
        "snack": 0.10
    }
    target_cal = cal_goal * meal_targets.get(meal_type, 0.30)
    result += f"🎯 Target for {meal_type}: ~{target_cal:.0f} kcal\n\n"
    
    result += "Available ingredients:\n"
    for food, qty in pantry_items:
        result += f"  • {food.title()}"
        if qty:
            result += f" ({qty}g)"
        result += "\n"
    
    result += "\n💡 Suggested combinations:\n\n"
    
    # Generate meal combinations based on available foods
    foods_dict = {food: qty for food, qty in pantry_items}
    suggestions = []
    
    # Smart combination logic
    if "chicken breast" in foods_dict and "brown rice" in foods_dict:
        suggestions.append(("Protein Bowl", "chicken breast:150, brown rice:150", 
                           "High protein balanced meal"))
    
    if "eggs" in foods_dict and "spinach" in foods_dict:
        suggestions.append(("Healthy Omelette", "eggs:100, spinach:50",
                           "Quick protein-rich option"))
    
    if "roti" in foods_dict and "dal" in foods_dict:
        suggestions.append(("Traditional Indian", "roti:120, dal:100",
                           "Balanced vegetarian meal"))
    
    if "oatmeal" in foods_dict:
        banana_part = ", banana:100" if "banana" in foods_dict else ""
        suggestions.append(("Oats Bowl", f"oatmeal:50{banana_part}",
                           "Healthy breakfast"))
    
    if "pasta" in foods_dict and "chicken breast" in foods_dict:
        suggestions.append(("Chicken Pasta", "pasta:100, chicken breast:100",
                           "Balanced protein meal"))
    
    if "brown rice" in foods_dict and "dal" in foods_dict:
        suggestions.append(("Rice & Dal", "brown rice:150, dal:100",
                           "Complete protein vegetarian"))
    
    if not suggestions:
        result += "⚠️ Not enough variety for meal suggestions.\n"
        result += "Try combining what you have or add more foods to pantry!"
    else:
        for i, (name, foods, desc) in enumerate(suggestions, 1):
            result += f"{i}. {name}: {desc}\n"
            result += f"   Foods: {foods}\n"
            result += f"   💡 Use: log_meal(\"{foods}\")\n\n"
    
    return result


# ==================== FOOD ROUTINES MANAGEMENT ====================

@mcp.tool()
def add_to_food_routine(
    food_name: str,
    morning: bool = False,
    midday: bool = False,
    afternoon: bool = False,
    evening: bool = False,
    night: bool = False,
    latenight: bool = False,
    preparation_type: str = "",
    effort_level: str = "easy",
    typical_portion_grams: float = 100,
    preference_score: int = 5,
    notes: str = ""
) -> str:
    """Add food to your time-based routine (what you typically eat/cook at different times).
    
    Args:
        food_name: Name of food (must exist in food_database)
        morning: Available 6-10am (breakfast items like bread, poha, paratha)
        midday: Available 10am-12pm (brunch/snacks)
        afternoon: Available 12-3pm (lunch items like dal-rice, roti-sabzi)
        evening: Available 4-7pm (evening snacks like maggie, chowmein, pakora)
        night: Available 8-11pm (dinner items)
        latenight: Available 11pm-6am (light snacks)
        preparation_type: 'quick', 'cook', 'ready', 'snack'
        effort_level: 'easy', 'medium', 'hard'
        typical_portion_grams: Your usual portion size
        preference_score: 1-10 how much you like this option
        notes: Additional context
    
    Example: add_to_food_routine("maggie", evening=True, preparation="quick", effort="easy", portion=50)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verify food exists in database
    cursor.execute("SELECT name FROM food_database WHERE name = ?", (food_name.lower(),))
    if not cursor.fetchone():
        conn.close()
        return f"⚠️ '{food_name}' not in food database. Add it first with add_food_to_database()"
    
    # Check if already in routines
    cursor.execute("SELECT id FROM food_routines WHERE food_name = ?", (food_name.lower(),))
    existing = cursor.fetchone()
    
    if existing:
        # Update existing entry
        cursor.execute("""
            UPDATE food_routines 
            SET morning = ?, midday = ?, afternoon = ?, evening = ?, night = ?, latenight = ?,
                preparation_type = ?, effort_level = ?, typical_portion_grams = ?,
                preference_score = ?, notes = ?, last_updated = CURRENT_TIMESTAMP
            WHERE food_name = ?
        """, (morning, midday, afternoon, evening, night, latenight,
              preparation_type, effort_level, typical_portion_grams,
              preference_score, notes, food_name.lower()))
        result = f"✓ Updated '{food_name}' in routines"
    else:
        # Insert new entry
        cursor.execute("""
            INSERT INTO food_routines 
            (food_name, morning, midday, afternoon, evening, night, latenight,
             preparation_type, effort_level, typical_portion_grams, preference_score, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (food_name.lower(), morning, midday, afternoon, evening, night, latenight,
              preparation_type, effort_level, typical_portion_grams, preference_score, notes))
        result = f"✓ Added '{food_name}' to routines"
    
    # Show what times it's available
    times = []
    if morning: times.append("morning")
    if midday: times.append("midday")
    if afternoon: times.append("afternoon")
    if evening: times.append("evening")
    if night: times.append("night")
    if latenight: times.append("latenight")
    
    if times:
        result += f"\n  Available: {', '.join(times)}"
    if preparation_type:
        result += f"\n  Type: {preparation_type}"
    if effort_level:
        result += f"\n  Effort: {effort_level}"
    result += f"\n  Portion: {typical_portion_grams}g"
    result += f"\n  Preference: {preference_score}/10"
    
    conn.commit()
    conn.close()
    return result


@mcp.tool()
def remove_from_food_routine(food_name: str) -> str:
    """Remove food from your routines."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM food_routines WHERE food_name = ?", (food_name.lower(),))
    
    if cursor.rowcount > 0:
        result = f"✓ Removed '{food_name}' from routines"
    else:
        result = f"⚠️ '{food_name}' was not in your routines"
    
    conn.commit()
    conn.close()
    return result


@mcp.tool()
def view_food_routines(time_period: str = "all") -> str:
    """View your food routines by time period.
    
    Args:
        time_period: 'all', 'morning', 'midday', 'afternoon', 'evening', 'night', 'latenight'
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if time_period == "all":
        cursor.execute("""
            SELECT r.food_name, r.morning, r.midday, r.afternoon, r.evening, r.night, r.latenight,
                   r.preparation_type, r.effort_level, r.typical_portion_grams, r.preference_score,
                   f.calories, f.protein, f.carbs, f.fats
            FROM food_routines r
            JOIN food_database f ON r.food_name = f.name
            ORDER BY r.preference_score DESC, r.food_name
        """)
    else:
        # Filter by specific time period
        time_col = time_period.lower()
        cursor.execute(f"""
            SELECT r.food_name, r.preparation_type, r.effort_level, r.typical_portion_grams,
                   r.preference_score, r.notes,
                   f.calories, f.protein, f.carbs, f.fats
            FROM food_routines r
            JOIN food_database f ON r.food_name = f.name
            WHERE r.{time_col} = 1
            ORDER BY r.preference_score DESC, r.effort_level
        """)
    
    items = cursor.fetchall()
    conn.close()
    
    if not items:
        return f"🍽️ No routines set for {time_period}!\n💡 Add with: add_to_food_routine()"
    
    result = f"🍽️ Your Food Routines ({time_period.title()}):\n\n"
    
    if time_period == "all":
        for food, morn, mid, aft, eve, nig, late, prep, effort, portion, pref, cal, prot, carbs, fats in items:
            result += f"• {food.title()} (preference: {pref}/10)\n"
            times = []
            if morn: times.append("morning")
            if mid: times.append("midday")
            if aft: times.append("afternoon")
            if eve: times.append("evening")
            if nig: times.append("night")
            if late: times.append("latenight")
            result += f"  Times: {', '.join(times)}\n"
            result += f"  {prep} | {effort} effort | {portion}g portion\n"
            result += f"  Nutrition: {cal}cal, P:{prot}g, C:{carbs}g, F:{fats}g (per 100g)\n\n"
    else:
        for food, prep, effort, portion, pref, notes, cal, prot, carbs, fats in items:
            result += f"• {food.title()} (⭐{pref}/10)\n"
            result += f"  {prep} | {effort} effort | {portion}g typical\n"
            actual_cal = cal * portion / 100
            result += f"  {actual_cal:.0f} cal per portion\n"
            if notes:
                result += f"  📝 {notes}\n"
            result += "\n"
    
    return result


@mcp.tool()
def recommend_from_routines(
    time_period: str = "current",
    filter_by_effort: str = "all",
    include_pantry: bool = True
) -> str:
    """Get food recommendations based on time-based routines and current goals.
    
    Args:
        time_period: 'current' (auto-detect), 'morning', 'midday', 'afternoon', 'evening', 'night', 'latenight'
        filter_by_effort: 'all', 'easy', 'medium', 'hard'
        include_pantry: If True, also show foods from your pantry
    
    This considers:
    - What you typically eat/cook at this time
    - Your calorie goals and consumption today
    - Preparation effort level
    - Your preference scores
    - What's in your pantry (if include_pantry=True)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Auto-detect time period if "current"
    if time_period == "current":
        hour = datetime.now().hour
        if 6 <= hour < 10:
            time_period = "morning"
        elif 10 <= hour < 12:
            time_period = "midday"
        elif 12 <= hour < 16:
            time_period = "afternoon"
        elif 16 <= hour < 20:
            time_period = "evening"
        elif 20 <= hour < 23:
            time_period = "night"
        else:
            time_period = "latenight"
    
    # Get user profile
    cursor.execute("SELECT daily_calorie_goal, region FROM user_profile ORDER BY id DESC LIMIT 1")
    profile = cursor.fetchone()
    
    if not profile or not profile[0]:
        conn.close()
        return "❌ Please set your daily calorie goal first using set_user_profile()"
    
    cal_goal, region = profile
    
    # Get today's consumption
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT SUM(calories) FROM meals WHERE date = ?", (today,))
    consumed = cursor.fetchone()[0] or 0
    remaining = cal_goal - consumed
    
    # Get routines for this time period
    time_col = time_period.lower()
    if filter_by_effort == "all":
        cursor.execute(f"""
            SELECT r.food_name, r.preparation_type, r.effort_level, r.typical_portion_grams,
                   r.preference_score, r.notes,
                   f.calories, f.protein, f.carbs, f.fats
            FROM food_routines r
            JOIN food_database f ON r.food_name = f.name
            WHERE r.{time_col} = 1
            ORDER BY r.preference_score DESC, r.effort_level
        """)
    else:
        cursor.execute(f"""
            SELECT r.food_name, r.preparation_type, r.effort_level, r.typical_portion_grams,
                   r.preference_score, r.notes,
                   f.calories, f.protein, f.carbs, f.fats
            FROM food_routines r
            JOIN food_database f ON r.food_name = f.name
            WHERE r.{time_col} = 1 AND r.effort_level = ?
            ORDER BY r.preference_score DESC
        """, (filter_by_effort,))
    
    routine_items = cursor.fetchall()
    
    # Get pantry items if requested
    pantry_items = []
    if include_pantry:
        cursor.execute("""
            SELECT p.food_name, p.quantity_grams, f.calories, f.protein
            FROM user_pantry p
            JOIN food_database f ON p.food_name = f.name
            WHERE p.available = 1
        """)
        pantry_items = cursor.fetchall()
    
    conn.close()
    
    # Build response
    time_emoji = {
        "morning": "🌅",
        "midday": "☀️",
        "afternoon": "🌤️",
        "evening": "🌆",
        "night": "🌙",
        "latenight": "🌃"
    }
    
    result = f"{time_emoji.get(time_period, '🍽️')} {time_period.title()} Food Options:\n\n"
    result += f"📊 Today: {consumed:.0f}/{cal_goal:.0f} kcal | Remaining: {remaining:.0f} kcal\n\n"
    
    if not routine_items and not pantry_items:
        result += f"⚠️ No routines set for {time_period}!\n"
        result += "💡 Add foods with: add_to_food_routine()\n"
        result += "💡 Or add to pantry with: add_to_pantry()"
        return result
    
    # Group by effort level
    if routine_items:
        result += "**Your Usual Options:**\n\n"
        
        effort_groups = {"easy": [], "medium": [], "hard": []}
        for food, prep, effort, portion, pref, notes, cal, prot, carbs, fats in routine_items:
            if effort not in effort_groups:
                effort = "easy"
            effort_groups[effort].append((food, prep, portion, pref, notes, cal, prot))
        
        for effort_name, emoji in [("easy", "⚡"), ("medium", "🔥"), ("hard", "💪")]:
            items = effort_groups.get(effort_name, [])
            if items:
                result += f"{emoji} **{effort_name.title()} Options:**\n"
                for food, prep, portion, pref, notes, cal, prot in items:
                    actual_cal = cal * portion / 100
                    actual_prot = prot * portion / 100
                    result += f"  • {food.title()} ({prep}) - {actual_cal:.0f} cal, {actual_prot:.1f}g protein\n"
                    result += f"    {portion}g portion | ⭐{pref}/10"
                    if notes:
                        result += f" | {notes}"
                    result += "\n"
                result += "\n"
    
    # Add pantry suggestions
    if pantry_items:
        result += "**From Your Pantry:**\n"
        for food, qty, cal, prot in pantry_items:
            result += f"  • {food.title()}"
            if qty:
                result += f" ({qty}g available)"
            result += f" - {cal}cal/100g\n"
        result += "\n"
    
    # Add smart suggestion
    result += "💡 **Smart Pick:** "
    if routine_items:
        best = routine_items[0]
        food, prep, effort, portion, pref, notes, cal, prot, carbs, fats = best
        actual_cal = cal * portion / 100
        result += f"{food.title()} ({prep}, {effort}) = {actual_cal:.0f} cal"
    
    return result


@mcp.tool()
def bulk_setup_routines(morning_foods: str = "", evening_foods: str = "", afternoon_foods: str = "") -> str:
    """Quick setup multiple foods for different times at once.
    
    Args:
        morning_foods: Comma-separated food names for morning (e.g., "bread,poha,paratha")
        evening_foods: Comma-separated food names for evening (e.g., "maggie,oats,chowmein")
        afternoon_foods: Comma-separated food names for afternoon (e.g., "roti,dal,rice")
    
    Example: bulk_setup_routines(morning="bread,poha,paratha", evening="maggie,oats")
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added = []
    failed = []
    
    def add_foods(foods_str, time_col):
        if not foods_str:
            return
        foods = [f.strip().lower() for f in foods_str.split(",")]
        for food in foods:
            if not food:
                continue
            # Check if food exists
            cursor.execute("SELECT name FROM food_database WHERE name = ?", (food,))
            if not cursor.fetchone():
                failed.append(f"{food} (not in database)")
                continue
            
            # Insert or update
            cursor.execute("SELECT id FROM food_routines WHERE food_name = ?", (food,))
            if cursor.fetchone():
                cursor.execute(f"UPDATE food_routines SET {time_col} = 1 WHERE food_name = ?", (food,))
            else:
                cursor.execute(f"""
                    INSERT INTO food_routines (food_name, {time_col})
                    VALUES (?, 1)
                """, (food,))
            added.append(f"{food} ({time_col})")
    
    add_foods(morning_foods, "morning")
    add_foods(afternoon_foods, "afternoon")
    add_foods(evening_foods, "evening")
    
    conn.commit()
    conn.close()
    
    result = "✓ Bulk routine setup complete!\n\n"
    if added:
        result += f"Added {len(added)} items:\n"
        for item in added:
            result += f"  • {item}\n"
    if failed:
        result += f"\n⚠️ Failed {len(failed)} items:\n"
        for item in failed:
            result += f"  • {item}\n"
        result += "\nAdd missing foods with: add_food_to_database()"
    
    return result


if __name__ == "__main__":
    mcp.run()


