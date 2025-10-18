# Health MCP Server - AI Coding Agent Instructions

## Project Overview
This is a **FastMCP-based Model Context Protocol (MCP) server** for comprehensive health tracking. The server exposes 20+ tools for LLM-driven health management through natural language interactions. Users tell an LLM what they ate/did, and the LLM calls appropriate tools to track and recommend.

**Core Architecture**: Single `main.py` file (1029 lines) containing all MCP tools + SQLite database layer. No separate modules - everything is self-contained.

## Critical Context for AI Agents

### The User Interaction Model
This is NOT a typical REST API or CLI tool. The interaction flow is:
1. **User** speaks to an **LLM** in natural language: "I ate 2 rotis and dal"
2. **LLM** interprets and calls MCP tools: `log_meal("roti:120, dal:100")`
3. **MCP Server** processes, updates SQLite DB, returns formatted results
4. **LLM** presents results to user naturally

**Key Implication**: Tools must return user-friendly, formatted strings (not JSON objects) since LLMs present them directly to users.

### Database Schema (health_data.db)
SQLite database with 6 tables initialized on server startup via `init_database()`:
- `food_database` - 23 pre-loaded foods (per 100g basis) - Indian + International
- `meals` - Logged meals with auto-calculated nutrients
- `sleep_log` - Sleep/wake times with quality ratings
- `weight_log` - Weight tracking over time
- `exercise_log` - Workouts with calorie burn estimates
- `user_profile` - Single-row profile (goals, region, preferences)

**Important**: All nutrition values in `food_database` are per 100g. The `log_meal` tool multiplies by quantity/100 to calculate actual intake.

### Pantry/Inventory System (Planned Feature)
**Purpose**: Track foods you currently have available (afford/own) so LLM can recommend meals from your actual inventory.

**New Table Schema**:
```sql
CREATE TABLE user_pantry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    available BOOLEAN DEFAULT 1,
    quantity_grams REAL,
    notes TEXT,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_name) REFERENCES food_database(name)
)
```

**Use Cases**:
- "What can I cook with what I have?" → `recommend_from_pantry()`
- "I bought chicken and rice" → `add_to_pantry("chicken breast", 500)`
- "I'm out of eggs" → `remove_from_pantry("eggs")`
- Track expiring foods with notes field

### Region-Based Recommendations
The `recommend_foods()` tool adapts meal suggestions based on `user_profile.region`:
- **India region**: Suggests roti, dal, paneer, idli, dosa, curd
- **Other regions**: Suggests chicken, pasta, oatmeal, salmon

This is hardcoded in `recommend_foods()` with region-specific meal dictionaries (lines 713-785).

### Smart Recommendation Logic

**Food Recommendations** (`recommend_foods()`):
- Queries today's consumed calories from `meals` table
- Calculates remaining calories vs `daily_calorie_goal`
- Suggests meals based on meal type (breakfast=25%, lunch=35%, dinner=30%, snack=10% of goal)

**Exercise Recommendations** (`recommend_exercise()`):
- Analyzes last 7 days sleep average from `sleep_log`
- <6h sleep → light exercises; 6-7h → moderate; 7+h → high intensity
- Considers weight gap (current vs target) to recommend weight loss/gain/maintenance exercises

## Development Workflow

### Running the Server
```bash
python main.py  # Starts FastMCP server, initializes DB if not exists
```
Server runs in stdio mode (default FastMCP transport) - designed for MCP client consumption, not direct HTTP calls.

### Testing
```bash
python test_server.py  # Validates DB initialization, table counts, food availability
python demo.py         # Shows nutrition tracking flow with sample queries
```

### Adding New Foods
Use the `add_food_to_database()` tool or manually insert into `food_database` table. **Must provide per-100g values**.

## Code Patterns & Conventions

### Tool Function Signatures
All MCP tools follow this pattern:
```python
@mcp.tool()
def tool_name(required_arg: type, optional_arg: type = default) -> str:
    """Docstring explaining args - LLM sees this!"""
    # Implementation
    return "User-friendly formatted string result"
```

**Critical**: Docstrings must explain how LLMs should call the tool and what format to use (see `log_meal` docstring with example).

### Database Connection Pattern
Every tool that touches DB follows:
```python
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
# ... queries ...
conn.commit()  # If writing
conn.close()   # Always close
```
No connection pooling - simple open/close per request. DB is co-located (`health_data.db` in project root).

### Date Handling
Default date is always `datetime.now().strftime("%Y-%m-%d")` if not provided. All dates stored as strings in YYYY-MM-DD format.

### Calorie Burn Estimates
Rough estimation in `log_exercise()`: light=3 cal/min, moderate=6, intense=10. These are approximations for user convenience, not medical accuracy.

## Common Pitfalls

1. **Don't return JSON**: Tools return formatted strings, not dicts/JSON. LLMs present these directly to users.
2. **Quantity format matters**: `log_meal()` expects "food:quantity_grams" - users may describe "2 rotis" which LLMs must translate to "roti:120" (60g per roti).
3. **Database must exist first**: `init_database()` is called in `if __name__ == "__main__"` block. Testing code should import and call it if needed.
4. **Per-100g basis**: When adding foods or debugging nutrition calculations, remember database values are per 100g.
5. **Single user profile**: The `user_profile` table has no user_id - this is a single-user system. Updates modify the single row.

## File Organization

```
main.py              # All MCP tools + DB initialization (1029 lines)
test_server.py       # DB validation test script
demo.py              # Sample usage demonstration
pyproject.toml       # Dependencies: fastmcp>=2.12.4
health_data.db       # Auto-created SQLite database
README.md            # User-facing feature documentation
USAGE_GUIDE.md       # Detailed usage scenarios
QUICK_REFERENCE.md   # Command cheat sheet
IMPLEMENTATION_SUMMARY.md  # Requirements checklist
```

## When Modifying Tools

- **Update docstrings** if changing parameter formats - LLMs read these to understand how to call tools
- **Test with `test_server.py`** to validate DB schema changes
- **Consider region-based logic** if adding food recommendations
- **Maintain formatted string output** - use emojis and sections for readability
- **Follow date format**: YYYY-MM-DD consistently across all tools

## Key Dependencies

- `fastmcp>=2.12.4` - MCP server framework (handles tool registration, client communication)
- `sqlite3` - Built-in Python module (no external dependency)
- Python 3.13+ required (per pyproject.toml)

## Integration Points

This server is designed to be called by **MCP-compatible LLM clients** (Claude Desktop, VS Code with MCP extension, etc.). It does not expose REST endpoints or have a web interface.

Configuration in MCP client should point to: `python main.py` as the command to start the server.

---

## Pantry/Inventory Feature Implementation Guide

### New Tools to Implement

```python
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
        SELECT p.food_name, p.quantity_grams, f.calories, f.protein, f.carbs, f.fats
        FROM user_pantry p
        JOIN food_database f ON p.food_name = f.name
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
    for food, qty, cal, protein, carbs, fats in pantry_items:
        result += f"  • {food.title()}"
        if qty:
            result += f" ({qty}g)"
        result += "\n"
    
    result += "\n💡 Suggested combinations:\n\n"
    
    # Generate meal combinations based on available foods
    # This is simplified - you can make it smarter
    foods_dict = {food: qty for food, qty, *_ in pantry_items}
    
    # Example combinations (customize based on what's available)
    suggestions = []
    
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
        suggestions.append(("Oats Bowl", "oatmeal:50, banana:100" if "banana" in foods_dict else "oatmeal:60",
                           "Healthy breakfast"))
    
    if not suggestions:
        result += "⚠️ Not enough variety for meal suggestions.\n"
        result += "Try combining what you have or add more foods to pantry!"
    else:
        for i, (name, foods, desc) in enumerate(suggestions, 1):
            result += f"{i}. {name}: {desc}\n"
            result += f"   Foods: {foods}\n"
            result += f"   💡 Use: log_meal(\"{foods}\")\n\n"
    
    return result
```

### Modify Existing `recommend_foods()` Tool

Add `pantry_only` parameter:

```python
@mcp.tool()
def recommend_foods(meal_type: str = "lunch", pantry_only: bool = False) -> str:
    """Recommend foods based on goals and region.
    
    Args:
        meal_type: "breakfast", "lunch", "dinner", or "snack"
        pantry_only: If True, only recommend from your pantry inventory
    """
    if pantry_only:
        return recommend_from_pantry(meal_type)
    
    # ... existing recommendation logic ...
```

### Usage Examples

**User:** "I bought chicken, rice, and eggs today"
**LLM calls:**
```python
add_to_pantry("chicken breast", 500, "fresh")
add_to_pantry("brown rice", 1000)
add_to_pantry("eggs", 600)  # ~6 eggs
```

**User:** "What can I cook for lunch with what I have?"
**LLM calls:**
```python
recommend_from_pantry("lunch")
```

**User:** "I'm out of chicken"
**LLM calls:**
```python
remove_from_pantry("chicken breast")
```

**User:** "Show me my pantry"
**LLM calls:**
```python
list_my_pantry()
```

### Implementation Steps

1. **Add table to `init_database()`** - Insert the CREATE TABLE statement
2. **Add the 4 new tools** to `main.py` after existing tools
3. **Modify `recommend_foods()`** to check `pantry_only` parameter
4. **Test with `test_server.py`** - Verify table creation
5. **Update documentation** - Add to README.md feature list

### Database Migration

If database already exists, run this SQL manually or add migration:

```python
def migrate_add_pantry():
    """Add pantry table to existing database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_pantry'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE user_pantry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_name TEXT NOT NULL,
                available BOOLEAN DEFAULT 1,
                quantity_grams REAL,
                notes TEXT,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (food_name) REFERENCES food_database(name)
            )
        """)
        conn.commit()
        print("✓ Pantry table created")
    else:
        print("ℹ Pantry table already exists")
    
    conn.close()
```
