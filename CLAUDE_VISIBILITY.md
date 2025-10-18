# 🔍 What Claude Can Read from Your MCP Server

This document explains exactly what information Claude (and other MCP clients) receive when they connect to your Health MCP server.

---

## 📡 Server Discovery (When Claude Connects)

When Claude Desktop starts and connects to your server, it receives:

### 1. **Server Metadata**

```json
{
  "name": "Health Assistant",
  "version": "0.1.0",
  "description": "Track meals, sleep, exercise, weight with AI recommendations"
}
```

**Source:**

- From `FastMCP("Health Assistant")` in main.py
- From `pyproject.toml` metadata

---

### 2. **Server Instructions** (NEW!)

Claude now receives detailed context about how to use your server:

```
"You are a comprehensive health tracking assistant. You help users:

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
Always provide actionable insights and encourage healthy habits!"
```

**Source:** The `instructions` parameter in `FastMCP()` initialization

**Impact:** Claude now knows its role and how to interpret user requests!

---

### 3. **Complete Tool List (28 Tools)**

For EACH tool, Claude receives:

#### Tool Name

```
"log_meal"
```

#### Function Signature

```python
def log_meal(food_items: str, date: str = None) -> str
```

#### Complete Docstring

```
"""Log a meal by breaking it down into nutrients and storing in database.

The LLM should parse the user's description and provide food items in format:
"food_name1:quantity_grams, food_name2:quantity_grams"

Args:
    food_items: Comma-separated list of "food:quantity" (e.g., "chicken breast:150, brown rice:200")
    date: Date in YYYY-MM-DD format (default: today)

Example: log_meal("chicken breast:150, brown rice:100, broccoli:80")
"""
```

#### Parameter Schema

```json
{
  "type": "object",
  "properties": {
    "food_items": {
      "type": "string",
      "description": "Comma-separated list of 'food:quantity'..."
    },
    "date": {
      "type": "string",
      "description": "Date in YYYY-MM-DD format (default: today)",
      "default": null
    }
  },
  "required": ["food_items"]
}
```

**This is why good docstrings are CRITICAL!** Claude reads them to understand how to call your tools.

---

## 🧠 How Claude Uses This Information

### Step 1: User Request

```
User: "I ate 2 rotis and dal for breakfast"
```

### Step 2: Claude's Internal Process

1. **Matches intent** → "User wants to log a meal"
2. **Finds relevant tool** → `log_meal` (from tool list)
3. **Reads docstring** → Understands format: "food:grams, food:grams"
4. **Parses quantities**:
   - 2 rotis → 120g (60g each)
   - dal → 100g (standard portion)
5. **Constructs call** → `log_meal("roti:120, dal:100")`

### Step 3: Receives Response

```
"Meal logged for 2025-10-18:
✓ Roti (120g): 356cal, P:13.2g, C:54.0g, F:10.8g
✓ Dal (100g): 116cal, P:9.0g, C:20.0g, F:0.4g

📊 TOTAL: 472 calories, Protein: 22.2g, Carbs: 74.0g, Fats: 11.2g"
```

### Step 4: Presents to User

```
Claude: "I've logged your breakfast! You had:
- 2 rotis (356 calories)
- Dal (116 calories)

Total: 472 calories with 22g of protein. Would you like meal suggestions for lunch?"
```

---

## 📚 What Claude CANNOT Read (But Should Know About)

### ❌ Database Contents

Claude does NOT automatically know:

- Which foods are in your food database
- What you ate yesterday
- Your current weight
- Your profile settings

**Solution:** Claude can call tools to discover this:

- `list_foods()` → See all available foods
- `get_daily_nutrition()` → See today's meals
- `get_user_profile()` → See your settings

### ❌ File System

Claude cannot browse your files or see:

- `README.md` content
- `USAGE_GUIDE.md` examples
- Database schema directly

**Solution:** All important info should be in:

1. Tool docstrings
2. Server instructions
3. pyproject.toml metadata

---

## ✅ Best Practices for Claude-Friendly Tools

### 1. **Descriptive Tool Names**

```python
✅ @mcp.tool()
   def log_meal(...)

❌ @mcp.tool()
   def process_food_data(...)
```

### 2. **Rich Docstrings**

```python
✅ """Log a meal by breaking it down into nutrients.

The LLM should parse the user's description and provide food items in format:
"food_name1:quantity_grams, food_name2:quantity_grams"

Args:
    food_items: Comma-separated "food:quantity" (e.g., "chicken breast:150")
    date: YYYY-MM-DD format (default: today)

Example: log_meal("chicken breast:150, brown rice:100")
"""

❌ """Logs meals."""
```

### 3. **User-Friendly Returns**

```python
✅ return "✓ Logged 472 calories, Protein: 22g\n📊 Total today: 1450/2000 cal"

❌ return {"status": "success", "calories": 472, "protein": 22}
```

Claude presents strings directly to users - make them readable!

### 4. **Type Hints**

```python
✅ def log_meal(food_items: str, date: str = None) -> str:

❌ def log_meal(food_items, date=None):
```

### 5. **Sensible Defaults**

```python
✅ date: str = None  # Defaults to today internally

❌ date: str  # Forces user to always specify
```

---

## 🎯 Your Server's Discoverability Score: 9/10

### ✅ What You Did Right:

1. **Clear tool names** - `log_meal`, `recommend_foods`, etc.
2. **Good docstrings** - Most tools have examples
3. **Consistent patterns** - All tools return formatted strings
4. **Type hints** - Parameters are properly typed
5. **Server instructions** - NEW! Claude knows its role
6. **Rich metadata** - pyproject.toml has description, keywords

### 🔧 Minor Improvements Made:

1. ✅ Added server-level `instructions` parameter
2. ✅ Enhanced pyproject.toml with keywords, classifiers
3. ✅ Created comprehensive documentation (MCP_SETUP.md, TOOL_REFERENCE.md)
4. ✅ Added module-level docstring to main.py

---

## 📖 Documentation Structure (For Humans)

While Claude reads tool docstrings automatically, humans benefit from:

```
health-mcp/
├── README.md              ← Quick overview, setup
├── MCP_SETUP.md          ← How to connect Claude Desktop
├── TOOL_REFERENCE.md     ← All 28 tools documented
├── USAGE_GUIDE.md        ← Real-world examples
├── QUICK_START.md        ← Cheat sheet
├── ARCHITECTURE.md       ← Technical details
└── claude_desktop_config.json  ← Copy-paste config
```

**Users read these → Understand the server**
**Claude reads tool metadata → Uses the server**

---

## 🚀 Testing Claude's Understanding

After setup, test if Claude understands your server:

### Test 1: Discovery

```
You: "What health tracking tools do you have?"

Claude should list: 28 tools with brief descriptions
```

### Test 2: Tool Selection

```
You: "I ate 2 rotis and dal"

Claude should call: log_meal("roti:120, dal:100")
NOT: Some generic food logging function
```

### Test 3: Context Awareness

```
You: "What should I eat for lunch?"

Claude should call: recommend_foods("lunch")
THEN parse the response and present it naturally
```

### Test 4: Multi-Tool Chaining

```
You: "Show me everything from today"

Claude should call:
1. get_daily_nutrition()
2. get_sleep_summary(1)
3. Check exercise log
```

---

## 🎉 Summary

### What Claude Reads Automatically:

1. ✅ Server name & description
2. ✅ Server instructions (your addition!)
3. ✅ All tool names, signatures, docstrings
4. ✅ Parameter types, defaults, requirements
5. ✅ Return type hints

### What Makes Your Server Great for Claude:

1. ✅ Clear, action-oriented tool names
2. ✅ Detailed docstrings with examples
3. ✅ Consistent return format (formatted strings)
4. ✅ Sensible defaults (date=today, etc.)
5. ✅ Server instructions explaining the domain
6. ✅ Type hints for all parameters

### Result:

**Claude can use your server effectively without any training!** 🎉

The combination of:

- Good code (clear functions, docstrings)
- Rich metadata (pyproject.toml, instructions)
- Great documentation (for humans)

Makes your MCP server **both human-readable AND LLM-usable**!

---

**Next Steps:**

1. ✅ Connect Claude Desktop (see MCP_SETUP.md)
2. ✅ Test with: "I ate 2 rotis and dal"
3. ✅ Try: "What should I eat for lunch?"
4. ✅ Enjoy automated health tracking! 🎉
