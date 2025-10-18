# 🏗️ Health MCP Server - Architecture Documentation

## Table of Contents

- [System Overview](#system-overview)
- [Component Architecture](#component-architecture)
- [Database Architecture](#database-architecture)
- [Data Flow](#data-flow)
- [Tool Categories](#tool-categories)
- [Recommendation Engine](#recommendation-engine)
- [Integration Points](#integration-points)

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
│                                                                 │
│  "I ate 2 rotis and dal"    "What should I eat for lunch?"    │
│  "I slept at 11 PM"         "Show me my daily summary"        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Natural Language
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         LLM CLIENT                              │
│                   (Claude Desktop, VS Code)                     │
│                                                                 │
│  • Interprets natural language                                 │
│  • Translates to MCP tool calls                                │
│  • Formats responses for users                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ MCP Protocol (stdio)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HEALTH MCP SERVER                            │
│                       (main.py)                                 │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              FastMCP Framework                          │  │
│  │  • Tool Registration                                    │  │
│  │  • Request Routing                                      │  │
│  │  • Response Formatting                                  │  │
│  └─────────────────────────────────────────────────────────┘  │
│                             │                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              29 MCP Tools                               │  │
│  │  • Nutrition Tracking    • Sleep Tracking               │  │
│  │  • Weight Management     • Exercise Logging             │  │
│  │  • Smart Recommendations • Pantry Management            │  │
│  │  • Food Routines         • Time-based Availability      │  │
│  └─────────────────────────────────────────────────────────┘  │
│                             │                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │           Business Logic Layer                          │  │
│  │  • Nutrition Calculations • Recommendation Engine       │  │
│  │  • Sleep Analysis        • Calorie Burn Estimates       │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ sqlite3
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SQLITE DATABASE                              │
│                    (health_data.db)                             │
│                                                                 │
│  • food_database  • meals         • sleep_log                  │
│  • weight_log     • exercise_log  • user_profile               │
│  • user_pantry    • food_routines                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Single-File Architecture

```
main.py (1692 lines)
│
├─── Database Initialization (Lines 1-180)
│    ├── init_database()
│    ├── CREATE TABLE statements (8 tables)
│    └── Pre-loaded food data (35 items)
│
├─── Basic Health Tools (Lines 151-220)
│    ├── calculate_bmi()
│    ├── daily_water_intake()
│    ├── steps_to_calories()
│    └── heart_rate_zone()
│
├─── Nutrition Tools (Lines 221-450)
│    ├── list_foods()
│    ├── log_meal()
│    ├── get_daily_nutrition()
│    ├── add_food_to_database()
│    └── get_nutrition_stats()
│
├─── Sleep Tools (Lines 451-550)
│    ├── log_sleep()
│    └── get_sleep_summary()
│
├─── Weight Tools (Lines 551-650)
│    ├── log_weight()
│    └── get_weight_trend()
│
├─── User Profile Tools (Lines 651-720)
│    ├── set_user_profile()
│    └── get_user_profile()
│
├─── Smart Recommendation Tools (Lines 721-950)
│    ├── recommend_foods()
│    └── recommend_exercise()
│
├─── Exercise Tools (Lines 951-1030)
│    ├── log_exercise()
│    └── get_daily_summary()
│
├─── Pantry Management Tools (Lines 1031-1240)
│    ├── add_to_pantry()
│    ├── remove_from_pantry()
│    ├── list_my_pantry()
│    └── recommend_from_pantry()
│
└─── Food Routines Tools (Lines 1310-1680)
     ├── add_to_food_routine()
     ├── remove_from_food_routine()
     ├── view_food_routines()
     ├── recommend_from_routines()
     └── bulk_setup_routines()
```

---

## Database Architecture

### Entity Relationship Diagram

```
┌─────────────────────┐
│   food_database     │◄─────────────┐
│─────────────────────│              │
│ PK id               │              │ FK
│    name (UNIQUE)    │              │
│    calories         │              │
│    protein          │              │
│    carbs            │         ┌────┴────────────┐
│    fats             │         │   user_pantry   │
│    fiber            │         │─────────────────│
└──────┬──────────────┘         │ PK id           │
       │                        │ FK food_name    │
       │ FK                     │    available    │
       │                        │    quantity     │
       ▼                        │    notes        │
┌─────────────────────┐         │    last_updated │
│      meals          │         └─────────────────┘
│─────────────────────│              │
                                     │ FK
                                     ▼
                            ┌─────────────────────┐
                            │   food_routines     │
                            │─────────────────────│
                            │ PK id               │
                            │ FK food_name        │
                            │    morning (BOOL)   │
                            │    midday (BOOL)    │
                            │    afternoon (BOOL) │
                            │    evening (BOOL)   │
                            │    night (BOOL)     │
                            │    latenight (BOOL) │
                            │    prep_type        │
                            │    effort_level     │
                            │    portion_grams    │
                            │    preference       │
                            │    notes            │
                            │    last_updated     │
                            └─────────────────────┘
│ PK id               │
│ FK food_name        │
│    date             │
│    quantity_grams   │
│    calories         │         ┌─────────────────┐
│    protein          │         │   sleep_log     │
│    carbs            │         │─────────────────│
│    fats             │         │ PK id           │
│    fiber            │         │    date         │
│    timestamp        │         │    sleep_time   │
└─────────────────────┘         │    wake_time    │
                                │    hours        │
┌─────────────────────┐         │    quality      │
│   user_profile      │         │    notes        │
│─────────────────────│         └─────────────────┘
│ PK id               │
│    height_m         │         ┌─────────────────┐
│    target_weight    │         │   weight_log    │
│    calorie_goal     │         │─────────────────│
│    activity_level   │         │ PK id           │
│    region           │         │    date         │
│    diet_prefs       │         │    weight_kg    │
│    updated_at       │         │    notes        │
└─────────────────────┘         └─────────────────┘
         │
         │ (Used by all recommendation tools)
         │
         ▼
┌─────────────────────┐
│   exercise_log      │
│─────────────────────│
│ PK id               │
│    date             │
│    exercise_name    │
│    duration_min     │
│    intensity        │
│    calories_burned  │
└─────────────────────┘
```

### Table Details

| Table           | Rows (Typical) | Purpose                             | Key Relationships                     |
| --------------- | -------------- | ----------------------------------- | ------------------------------------- |
| `food_database` | 35             | Reference nutrition data (per 100g) | Referenced by meals, pantry, routines |
| `meals`         | 100-1000+      | Daily meal logs                     | FK to food_database                   |
| `sleep_log`     | 30-365         | Sleep tracking                      | Used by exercise recommendations      |
| `weight_log`    | 30-100         | Weight progress                     | Compared with target_weight           |
| `exercise_log`  | 50-500         | Workout history                     | Used in daily summaries               |
| `user_profile`  | 1              | User goals/preferences              | Single-row config                     |
| `user_pantry`   | 10-50          | Available food inventory            | FK to food_database                   |
| `food_routines` | 10-50          | Time-based food availability        | FK to food_database                   |

---

## Data Flow

### 1. Meal Logging Flow

```
User Input: "I ate 2 rotis and dal"
       │
       ▼
LLM Interpretation
       │
       ├─ "2 rotis" = roti:120g (60g each)
       └─ "dal" = dal:100g (standard serving)
       │
       ▼
Tool Call: log_meal("roti:120, dal:100")
       │
       ▼
┌──────────────────────────────────────┐
│  log_meal() Processing:              │
│  1. Parse "food:quantity" pairs      │
│  2. For each food:                   │
│     ├─ Query food_database           │
│     ├─ Get per-100g nutrition        │
│     ├─ Calculate: value * (qty/100)  │
│     └─ INSERT into meals table       │
│  3. Sum totals for response          │
└──────────────────────────────────────┘
       │
       ▼
Database Update
       │
meals table:
├─ roti, 120g, 356cal, 13.2g protein, ...
└─ dal, 100g, 116cal, 9g protein, ...
       │
       ▼
Return Formatted String
       │
       ▼
"✓ Roti (120g): 356cal, P:13.2g, ...
 ✓ Dal (100g): 116cal, P:9g, ...
 📊 TOTAL: 472 calories, Protein: 22.2g, ..."
       │
       ▼
LLM presents to user naturally
```

### 2. Food Recommendation Flow

```
User: "What should I eat for lunch?"
       │
       ▼
Tool Call: recommend_foods("lunch", pantry_only=False)
       │
       ▼
┌─────────────────────────────────────────────────┐
│  recommend_foods() Logic:                       │
│                                                 │
│  1. Query user_profile                          │
│     └─ Get: daily_calorie_goal, region          │
│                                                 │
│  2. Query meals (today)                         │
│     └─ Calculate: consumed calories             │
│                                                 │
│  3. Calculate remaining = goal - consumed       │
│                                                 │
│  4. Determine meal target                       │
│     └─ lunch = 35% of daily goal                │
│                                                 │
│  5. Select region-based meal templates          │
│     ├─ IF region="India":                       │
│     │  └─ Templates: roti+dal, rice+dal, ...    │
│     └─ ELSE:                                    │
│        └─ Templates: chicken+rice, pasta, ...   │
│                                                 │
│  6. Format 3-5 suggestions with instructions    │
└─────────────────────────────────────────────────┘
       │
       ▼
Return formatted recommendations with:
- Calorie status (consumed/remaining)
- Meal suggestions with portions
- log_meal() commands ready to use
```

### 3. Pantry-Based Recommendation Flow

```
User: "What can I cook with what I have?"
       │
       ▼
Tool Call: recommend_from_pantry("lunch")
       │
       ▼
┌─────────────────────────────────────────────────┐
│  recommend_from_pantry() Logic:                 │
│                                                 │
│  1. Query user_pantry WHERE available=1         │
│     └─ Get: list of foods user has             │
│                                                 │
│  2. Query user_profile + meals (today)          │
│     └─ Get: calorie goals & consumption        │
│                                                 │
│  3. Build foods_dict = {food: quantity}         │
│                                                 │
│  4. Smart combination matching:                 │
│     ├─ IF has("chicken") AND has("rice"):       │
│     │  └─ Suggest: "Protein Bowl"              │
│     ├─ IF has("eggs") AND has("spinach"):       │
│     │  └─ Suggest: "Healthy Omelette"          │
│     └─ IF has("roti") AND has("dal"):           │
│        └─ Suggest: "Traditional Indian"         │
│                                                 │
│  5. Check quantities & warn if insufficient     │
│                                                 │
│  6. Format with available ingredients list      │
└─────────────────────────────────────────────────┘
       │
       ▼
Return personalized suggestions based on
ONLY what user can afford/has available
```

### 4. Exercise Recommendation Flow

```
User: "Should I exercise today?"
       │
       ▼
Tool Call: recommend_exercise()
       │
       ▼
┌─────────────────────────────────────────────────┐
│  recommend_exercise() Logic:                    │
│                                                 │
│  1. Query sleep_log (last 7 days)              │
│     └─ Calculate: avg_sleep_hours              │
│                                                 │
│  2. Determine intensity based on sleep:         │
│     ├─ <6h  → intensity = "light"              │
│     ├─ 6-7h → intensity = "moderate"            │
│     └─ 7+h  → intensity = "high"                │
│                                                 │
│  3. Query user_profile + weight_log             │
│     ├─ Get: current_weight, target_weight       │
│     └─ Determine goal:                          │
│        ├─ current > target → "weight_loss"     │
│        ├─ current < target → "weight_gain"     │
│        └─ current ≈ target → "maintenance"     │
│                                                 │
│  4. Select exercises matching:                  │
│     └─ intensity + goal + user preferences      │
│                                                 │
│  5. Format with durations & calorie estimates   │
└─────────────────────────────────────────────────┘
       │
       ▼
Return contextual exercise plan based on
sleep quality, weight goals, and energy levels
```

### 5. Food Routines Recommendation Flow ✨ NEW

```
User: "What should I eat for breakfast?" (8:00 AM)
       │
       ▼
Tool Call: recommend_from_routines("current")
       │
       ▼
┌─────────────────────────────────────────────────┐
│  recommend_from_routines() Logic:               │
│                                                 │
│  1. Auto-detect time period:                    │
│     └─ 8:00 AM → time_period = "morning"       │
│                                                 │
│  2. Query user_profile + meals (today):         │
│     ├─ calorie_goal = 2000                     │
│     └─ consumed = 0 → remaining = 2000          │
│                                                 │
│  3. Query food_routines WHERE morning=1:        │
│     SELECT food_name, prep_type, effort,        │
│            portion, preference, notes           │
│     JOIN food_database for nutrition            │
│     ORDER BY preference DESC, effort ASC        │
│                                                 │
│  4. Group by effort level:                      │
│     ├─ EASY/QUICK: [bread, chana, juice]       │
│     └─ MEDIUM/COOK: [paratha, poha]            │
│                                                 │
│  5. Calculate portions & nutrition:             │
│     └─ For each: cal = (db_cal * portion/100)  │
│                                                 │
│  6. Optional: Query user_pantry for extras:     │
│     └─ Show available pantry items alongside    │
│                                                 │
│  7. Smart Pick = highest preference:            │
│     └─ "Paratha (9/10) = 384 cal"              │
└─────────────────────────────────────────────────┘
       │
       ▼
Return time-appropriate food options grouped by
effort, with smart pick based on preference scores
and current calorie goals
```

---

## Tool Categories

### Category Breakdown

```
┌─────────────────────────────────────────────────────────┐
│                    29 MCP TOOLS                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📊 CORE TRACKING (6 tools)                            │
│  ├─ log_meal()           Track food intake             │
│  ├─ log_sleep()          Track sleep patterns          │
│  ├─ log_weight()         Track weight changes          │
│  ├─ log_exercise()       Track workouts                │
│  ├─ set_user_profile()   Configure goals               │
│  └─ get_user_profile()   View current settings         │
│                                                         │
│  🍽️ NUTRITION TOOLS (5 tools)                          │
│  ├─ list_foods()         Browse food database          │
│  ├─ get_daily_nutrition() Day's nutrition breakdown    │
│  ├─ get_nutrition_stats() Multi-day statistics         │
│  └─ add_food_to_database() Add custom foods            │
│                                                         │
│  🧠 SMART RECOMMENDATIONS (2 tools)                     │
│  ├─ recommend_foods()     Meal suggestions             │
│  └─ recommend_exercise()  Workout plans                │
│                                                         │
│  📦 PANTRY MANAGEMENT (4 tools)                         │
│  ├─ add_to_pantry()      Add available foods           │
│  ├─ remove_from_pantry() Remove used foods             │
│  ├─ list_my_pantry()     View inventory                │
│  └─ recommend_from_pantry() Suggestions from inventory │
│                                                         │
│  ⏰ FOOD ROUTINES (5 tools) ✨ NEW                      │
│  ├─ add_to_food_routine()    Set time-based foods     │
│  ├─ remove_from_food_routine() Remove from routines   │
│  ├─ view_food_routines()     View by time period      │
│  ├─ recommend_from_routines() Smart time-based picks  │
│  └─ bulk_setup_routines()    Quick batch setup        │
│                                                         │
│  📈 ANALYTICS & REPORTS (3 tools)                       │
│  ├─ get_sleep_summary()  Sleep trend analysis          │
│  ├─ get_weight_trend()   Weight progress               │
│  └─ get_daily_summary()  Complete health dashboard     │
│                                                         │
│  🧮 BASIC CALCULATORS (4 tools)                         │
│  ├─ calculate_bmi()      BMI calculation               │
│  ├─ daily_water_intake() Water recommendations         │
│  ├─ steps_to_calories()  Step conversion               │
│  └─ heart_rate_zone()    Training zones                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Recommendation Engine

### Smart Recommendation Algorithm

```
┌───────────────────────────────────────────────────────────┐
│          FOOD RECOMMENDATION ENGINE (3 Modes)             │
└───────────────────────────────────────────────────────────┘

Mode 1: recommend_foods() - General Recommendations
Mode 2: recommend_from_pantry() - Inventory-Based
Mode 3: recommend_from_routines() - Time-Based ✨ NEW

Input Parameters:
├─ meal_type: "breakfast" | "lunch" | "dinner" | "snack"
├─ pantry_only: True | False
└─ time_period: "morning" | "afternoon" | "evening" | "current"

Process Flow:
│
├─ [Step 1] Load User Context
│  ├─ daily_calorie_goal (from user_profile)
│  ├─ region (from user_profile)
│  ├─ dietary_preferences (from user_profile)
│  └─ consumed_today (SUM from meals WHERE date=today)
│
├─ [Step 2] Calculate Targets
│  ├─ remaining_calories = goal - consumed
│  └─ meal_target_calories = goal * meal_percentage
│      ├─ breakfast: 25% of daily goal
│      ├─ lunch:     35% of daily goal
│      ├─ dinner:    30% of daily goal
│      └─ snack:     10% of daily goal
│
├─ [Step 3] Get Available Foods
│  ├─ IF pantry_only=True:
│  │  └─ Query user_pantry WHERE available=1
│  └─ ELSE:
│     └─ Use all foods from food_database
│
├─ [Step 4] Apply Region Filter
│  ├─ IF region contains "India":
│  │  └─ Priority: roti, dal, paneer, idli, dosa, curd
│  └─ ELSE:
│     └─ Priority: chicken, pasta, rice, salmon, eggs
│
├─ [Step 5] Generate Meal Combinations
│  ├─ Match complementary foods (protein + carb + fiber)
│  ├─ Ensure combinations meet meal_target_calories
│  ├─ Consider dietary_preferences (vegetarian, vegan, etc.)
│  └─ Provide 3-5 diverse options
│
└─ [Step 6] Format Output
   ├─ Show calorie status (consumed/remaining)
   ├─ List each suggestion with:
   │  ├─ Meal name
   │  ├─ Food items with quantities
   │  ├─ Description
   │  └─ Ready-to-use log_meal() command
   └─ Add warnings if remaining calories are low


┌───────────────────────────────────────────────────────────┐
│         EXERCISE RECOMMENDATION ENGINE                    │
└───────────────────────────────────────────────────────────┘

Input Parameters:
└─ (No direct params - analyzes user state)

Process Flow:
│
├─ [Step 1] Analyze Sleep Quality
│  ├─ Query sleep_log (last 7 days)
│  ├─ Calculate: avg_sleep_hours
│  └─ Determine intensity:
│     ├─ <6 hours  → "light" (walking, yoga)
│     ├─ 6-7 hours → "moderate" (jogging, bodyweight)
│     └─ 7+ hours  → "high" (running, HIIT, strength)
│
├─ [Step 2] Analyze Weight Goal
│  ├─ Get current_weight (latest from weight_log)
│  ├─ Get target_weight (from user_profile)
│  └─ Determine goal:
│     ├─ current > target+2kg → "weight_loss" (cardio focus)
│     ├─ current < target-2kg → "weight_gain" (strength focus)
│     └─ within ±2kg → "maintenance" (balanced)
│
├─ [Step 3] Select Exercise Categories
│  └─ Match (intensity, goal) to exercise database:
│      ├─ (light, weight_loss)     → Walking, swimming
│      ├─ (moderate, weight_loss)  → Jogging, cycling
│      ├─ (high, weight_loss)      → Running, HIIT
│      ├─ (light, maintenance)     → Yoga, stretching
│      ├─ (moderate, maintenance)  → Bodyweight circuits
│      ├─ (high, maintenance)      → Mixed cardio/strength
│      ├─ (light, weight_gain)     → Light resistance
│      ├─ (moderate, weight_gain)  → Strength training
│      └─ (high, weight_gain)      → Heavy lifting
│
├─ [Step 4] Estimate Calorie Burns
│  └─ Apply intensity multipliers:
│      ├─ light:    3 cal/min
│      ├─ moderate: 6 cal/min
│      └─ intense:  10 cal/min
│
└─ [Step 5] Format Recommendations
   ├─ Show sleep analysis
   ├─ Show weight goal context
   ├─ List 3-4 exercises with:
   │  ├─ Exercise name
   │  ├─ Duration recommendation
   │  ├─ Calorie burn estimate
   │  └─ Benefits description
   └─ Provide general tips (hydration, rest days)
```

### Food Routines Algorithm ✨ NEW

```
┌───────────────────────────────────────────────────────────┐
│          TIME-BASED ROUTINES ENGINE                       │
└───────────────────────────────────────────────────────────┘

Input Parameters:
├─ time_period: "morning" | "midday" | "afternoon" | "evening" | "night" | "current"
├─ filter_by_effort: "all" | "easy" | "medium" | "hard"
└─ include_pantry: True | False

Process Flow:
│
├─ [Step 1] Time Detection
│  └─ IF time_period = "current":
│     ├─ 6-10am   → "morning"
│     ├─ 10-12pm  → "midday"
│     ├─ 12-4pm   → "afternoon"
│     ├─ 4-8pm    → "evening"
│     ├─ 8-11pm   → "night"
│     └─ 11pm-6am → "latenight"
│
├─ [Step 2] Load Context
│  ├─ calorie_goal & consumed_today
│  └─ remaining_calories
│
├─ [Step 3] Query Routines
│  └─ SELECT * FROM food_routines
│     WHERE {time_period}=1
│     AND (effort_level=? OR 'all')
│     ORDER BY preference_score DESC, effort_level ASC
│
├─ [Step 4] JOIN with Food Database
│  └─ Get nutrition per 100g for each routine food
│
├─ [Step 5] Calculate Actual Nutrition
│  └─ For each food:
│     └─ actual = db_value * (typical_portion_grams / 100)
│
├─ [Step 6] Group by Effort Level
│  ├─ EASY/QUICK: [ready-to-eat, <5min prep]
│  └─ MEDIUM/COOK: [requires cooking, 10-20min]
│
├─ [Step 7] Optional: Add Pantry Items
│  └─ IF include_pantry=True:
│     └─ Query user_pantry for complementary items
│
└─ [Step 8] Smart Pick Selection
   └─ Top food = MAX(preference_score)
      └─ Consider: portion fits calorie budget

Key Features:
• Time-aware (only shows contextual foods)
• Effort-based filtering (lazy day? show easy options)
• Preference-driven (learns what you like)
• Portion-smart (typical serving sizes)
• Note-enhanced (personal context like "Mom cooks this")
```

---

## Integration Points

### MCP Protocol Communication

```
┌──────────────────────────────────────────────────────┐
│              MCP CLIENT (LLM)                        │
│  (Claude Desktop, VS Code with MCP Extension, etc.) │
└────────────────────┬─────────────────────────────────┘
                     │
                     │ stdio transport
                     │ (Standard Input/Output)
                     │
                     ├─ Request →
                     │  {
                     │    "jsonrpc": "2.0",
                     │    "method": "tools/call",
                     │    "params": {
                     │      "name": "log_meal",
                     │      "arguments": {
                     │        "food_items": "chicken:150, rice:200"
                     │      }
                     │    }
                     │  }
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│            FASTMCP FRAMEWORK                         │
│  • Deserializes JSON-RPC requests                   │
│  • Routes to appropriate @mcp.tool() function        │
│  • Handles errors and exceptions                    │
│  • Serializes responses back to JSON-RPC            │
└────────────────────┬─────────────────────────────────┘
                     │
                     │ Python function call
                     ▼
┌──────────────────────────────────────────────────────┐
│              TOOL FUNCTION                           │
│  def log_meal(food_items: str, date: str = None):   │
│      # Business logic here                          │
│      return "✓ Meal logged: ..."                    │
└────────────────────┬─────────────────────────────────┘
                     │
                     ├─ Response ←
                     │  {
                     │    "jsonrpc": "2.0",
                     │    "result": {
                     │      "content": [
                     │        {
                     │          "type": "text",
                     │          "text": "✓ Meal logged: 472 cal..."
                     │        }
                     │      ]
                     │    }
                     │  }
                     │
                     └────────────────────────────────────┘
```

### Configuration (MCP Client Side)

```json
// Example: Claude Desktop config
{
  "mcpServers": {
    "health-tracker": {
      "command": "python",
      "args": ["C:/path/to/health-mcp/main.py"],
      "env": {}
    }
  }
}
```

---

## Key Design Principles

### 1. **Single-File Simplicity**

- Everything in `main.py` (1259 lines)
- No module imports, no package complexity
- Easy to understand, debug, and modify

### 2. **Database-Centric**

- SQLite as single source of truth
- Simple open/close per request (no pooling)
- Foreign key constraints ensure data integrity

### 3. **User-Friendly Responses**

- Tools return formatted strings, not JSON
- Rich emoji usage for visual appeal
- LLM presents directly to users

### 4. **Per-100g Nutrition Standard**

- All food database values per 100g
- Tools multiply by (quantity/100) for actual intake
- Consistent calculation across all nutrition features

### 5. **Context-Aware Intelligence**

- Recommendations consider multiple factors:
  - Daily goals vs current consumption
  - Sleep quality (for exercise intensity)
  - Region (for culturally appropriate foods)
  - Available inventory (pantry-based suggestions)

### 6. **No External Dependencies**

- Only `fastmcp` package required
- `sqlite3` is built-in to Python
- No API calls, no network requests
- Fully offline capable

---

## Performance Characteristics

### Scalability Profile

```
┌─────────────────────────────────────────────────┐
│  Current Design Optimized For:                 │
│  • Single user (no user_id in tables)          │
│  • 1-10 requests per minute                    │
│  • Database size: <50MB (years of data)        │
│  • Response time: <100ms per tool call         │
└─────────────────────────────────────────────────┘

Bottlenecks (if scaling to multi-user):
├─ No connection pooling (open/close each request)
├─ No indexes on date columns (full table scans)
├─ No pagination (all results returned at once)
└─ No caching (recalculates recommendations each time)

Recommended for scaling:
├─ Add user_id to all tables
├─ Implement connection pooling
├─ Add indexes: CREATE INDEX idx_meals_date ON meals(date)
└─ Cache daily summaries (invalidate on new data)
```

---

## Extension Architecture

### Future Enhancement Points

```
Current System
     │
     ├─── [Easy Extensions]
     │    ├─ New foods → INSERT into food_database
     │    ├─ New regions → Add to recommend_foods() dict
     │    └─ New exercises → Extend exercise categories
     │
     ├─── [Medium Complexity]
     │    ├─ Micronutrients → Add columns to food_database
     │    ├─ Meal photos → Add photo_path to meals table
     │    ├─ Auto-deduct pantry → Trigger on log_meal()
     │    └─ Shopping lists → Generate from meal plans
     │
     └─── [Architectural Changes]
          ├─ Multi-user → Add user_id to all tables
          ├─ External APIs → Nutrition data from USDA
          ├─ REST wrapper → HTTP layer on MCP tools
          └─ Mobile app → GraphQL API + auth layer
```

---

## Summary

The Health MCP Server is a **monolithic, single-file architecture** designed for:

- **Simplicity**: One Python file, one database, zero config
- **LLM-Native**: Built for natural language interaction via MCP
- **Context-Aware**: Smart recommendations based on user state
- **Offline-First**: No external dependencies or API calls
- **Single-User**: Optimized for personal health tracking

**Key Innovations**:

1. **Pantry System** - Bridges the gap between what users want to eat and what they can actually afford/have
2. **Food Routines** - Time-based availability tracking that understands when foods are accessible (morning street vendor, office cafeteria, home cooking)

---

_Architecture Version: 3.0_  
_Last Updated: October 17, 2025_  
_Total Tools: 29 | Database Tables: 8 | Lines of Code: 1692_

**Latest Updates (v3.0):**

- ✅ Added `food_routines` table for time-based food availability
- ✅ Added 5 new MCP tools for routine management
- ✅ Added 11 new Indian foods (bread, poha, maggie, chowmein, etc.)
- ✅ Implemented smart time-aware recommendations
- ✅ Integrated routines with pantry and calorie goals
