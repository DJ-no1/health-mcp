# 🛠️ Complete Tool Reference - Health MCP Server

This document lists ALL 28 tools with examples for LLM consumption.

---

## 📂 Tool Categories

- [Basic Health Tools](#basic-health-tools) (4 tools)
- [Nutrition Tracking](#nutrition-tracking) (8 tools)
- [Sleep Management](#sleep-management) (2 tools)
- [Weight Tracking](#weight-tracking) (2 tools)
- [User Profile](#user-profile) (2 tools)
- [Smart Recommendations](#smart-recommendations) (4 tools)
- [Pantry Management](#pantry-management) (3 tools)
- [Food Routines](#food-routines) (3 tools)

---

## Basic Health Tools

### 1. `calculate_bmi`

**Purpose:** Calculate Body Mass Index

**Parameters:**

- `weight_kg` (float): Weight in kilograms
- `height_m` (float): Height in meters

**Example:**

```
User: "I'm 75 kg and 1.75 meters tall, what's my BMI?"
→ calculate_bmi(75, 1.75)
→ "BMI: 24.5 - Category: Normal weight"
```

---

### 2. `daily_water_intake`

**Purpose:** Calculate recommended water intake

**Parameters:**

- `weight_kg` (float): Body weight in kilograms

**Example:**

```
User: "How much water should I drink if I weigh 70kg?"
→ daily_water_intake(70)
→ "Recommended: 2100-2450 ml (2.1-2.5 liters)"
```

---

### 3. `steps_to_calories`

**Purpose:** Estimate calories burned from walking

**Parameters:**

- `steps` (int): Number of steps
- `weight_kg` (float, optional): Body weight (default: 70)

**Example:**

```
User: "I walked 10,000 steps today, how many calories did I burn?"
→ steps_to_calories(10000, 75)
→ "10000 steps burned approximately 428 calories"
```

---

### 4. `heart_rate_zone`

**Purpose:** Calculate training heart rate zones

**Parameters:**

- `age` (int): Age in years
- `resting_hr` (int, optional): Resting heart rate (default: 60)

**Example:**

```
User: "I'm 30 years old, what are my heart rate zones?"
→ heart_rate_zone(30)
→ "Max Heart Rate: 190 bpm\nTraining Zones:\n  Easy: 95-108 bpm\n..."
```

---

## Nutrition Tracking

### 5. `list_foods`

**Purpose:** Browse all available foods in database

**Parameters:** None

**Example:**

```
User: "What foods can I track?"
→ list_foods()
→ "Available Foods (per 100g):\n• Chicken Breast: 165cal..."
```

---

### 6. `log_meal`

⭐ **MOST IMPORTANT TOOL** ⭐

**Purpose:** Log a meal with automatic nutrient calculation

**Parameters:**

- `food_items` (str): "food1:grams, food2:grams" format
- `date` (str, optional): YYYY-MM-DD (default: today)

**Examples:**

```
User: "I ate 2 rotis and dal"
→ LLM interprets: 2 rotis = 120g, dal = 100g
→ log_meal("roti:120, dal:100")

User: "I had chicken breast 150g and brown rice 200g for lunch"
→ log_meal("chicken breast:150, brown rice:200")

User: "I ate a banana"
→ LLM assumes: 1 banana ≈ 120g
→ log_meal("banana:120")
```

**Output:**

```
Meal logged for 2025-10-18:
✓ Roti (120g): 356cal, P:13.2g, C:54.0g, F:10.8g
✓ Dal (100g): 116cal, P:9.0g, C:20.0g, F:0.4g

📊 TOTAL: 472 calories, Protein: 22.2g, Carbs: 74.0g, Fats: 11.2g
```

---

### 7. `get_daily_nutrition`

**Purpose:** Get total nutrition for a day

**Parameters:**

- `date` (str, optional): YYYY-MM-DD (default: today)

**Example:**

```
User: "What did I eat today?"
→ get_daily_nutrition()

User: "Show my nutrition from October 15"
→ get_daily_nutrition("2025-10-15")
```

---

### 8. `add_food_to_database`

**Purpose:** Add custom foods not in database

**Parameters:**

- `name` (str): Food name
- `calories` (float): Calories per 100g
- `protein` (float): Protein grams per 100g
- `carbs` (float): Carbs grams per 100g
- `fats` (float): Fats grams per 100g
- `fiber` (float, optional): Fiber grams per 100g

**Example:**

```
User: "Can you add quinoa to the database? It has 120 cal, 4g protein, 21g carbs, 2g fat per 100g"
→ add_food_to_database("quinoa", 120, 4, 21, 2, 2.8)
```

---

### 9. `get_nutrition_stats`

**Purpose:** Multi-day nutrition statistics

**Parameters:**

- `days` (int, optional): Number of days (default: 7)

**Example:**

```
User: "Show me my nutrition trends for the last month"
→ get_nutrition_stats(30)
```

---

### 10-12. Other Nutrition Tools

- `get_daily_summary` - Complete daily health dashboard
- `log_exercise` - Track workouts
- Various analysis tools

---

## Sleep Management

### 13. `log_sleep`

**Purpose:** Track sleep duration and quality

**Parameters:**

- `sleep_time` (str): "HH:MM" format (24h)
- `wake_time` (str): "HH:MM" format
- `quality` (str, optional): "poor", "fair", "good", "excellent"
- `notes` (str, optional): Additional notes

**Examples:**

```
User: "I slept at 11 PM and woke up at 7 AM"
→ log_sleep("23:00", "07:00")

User: "I went to bed at 10:30 PM, woke at 6:00 AM, slept poorly"
→ log_sleep("22:30", "06:00", "poor", "had nightmares")
```

---

### 14. `get_sleep_summary`

**Purpose:** Analyze sleep patterns

**Parameters:**

- `days` (int, optional): Days to analyze (default: 7)

**Example:**

```
User: "How well have I been sleeping this week?"
→ get_sleep_summary(7)
```

---

## Weight Tracking

### 15. `log_weight`

**Purpose:** Track weight over time

**Parameters:**

- `weight_kg` (float): Weight in kilograms
- `date` (str, optional): YYYY-MM-DD
- `notes` (str, optional): Notes

**Example:**

```
User: "I weigh 72.5 kg today"
→ log_weight(72.5)
```

---

### 16. `get_weight_trend`

**Purpose:** Visualize weight changes

**Parameters:**

- `days` (int, optional): Days to show (default: 30)

**Example:**

```
User: "Show my weight progress this month"
→ get_weight_trend(30)
```

---

## User Profile

### 17. `set_user_profile`

⭐ **FIRST TOOL TO CALL** ⭐

**Purpose:** Set up user goals and preferences

**Parameters:**

- `height_m` (float, optional): Height in meters
- `target_weight_kg` (float, optional): Goal weight
- `daily_calorie_goal` (float, optional): Daily calorie target
- `activity_level` (str, optional): "sedentary", "light", "moderate", "active", "very_active"
- `region` (str, optional): "India", "USA", "International", etc.
- `dietary_preferences` (str, optional): "vegetarian", "vegan", "non-veg", etc.

**Example:**

```
User: "Set up my profile: I'm 1.75m tall, weigh 75kg, want to reach 70kg, need 2000 calories daily, I live in India and I'm vegetarian"

→ set_user_profile(
    height_m=1.75,
    target_weight_kg=70,
    daily_calorie_goal=2000,
    activity_level="moderate",
    region="India",
    dietary_preferences="vegetarian"
)
```

---

### 18. `get_user_profile`

**Purpose:** View current profile settings

**Example:**

```
User: "What are my goals?"
→ get_user_profile()
```

---

## Smart Recommendations

### 19. `recommend_foods`

⭐ **POWERFUL RECOMMENDATION ENGINE** ⭐

**Purpose:** Get meal suggestions based on goals, region, and consumption

**Parameters:**

- `meal_type` (str, optional): "breakfast", "lunch", "dinner", "snack"
- `pantry_only` (bool, optional): Only suggest from pantry

**How it works:**

1. Checks your daily calorie goal
2. Checks what you've eaten today
3. Calculates remaining calories
4. Suggests region-appropriate meals
5. Provides portion sizes

**Examples:**

```
User: "What should I eat for lunch?"
→ recommend_foods("lunch")

User: "Suggest a healthy breakfast"
→ recommend_foods("breakfast")

User: "What can I cook with what I have?"
→ recommend_foods("lunch", pantry_only=True)
```

**Output Example:**

```
🍽️ Food Recommendations (Lunch):
📊 Today: 472/2000 kcal consumed, 1528 remaining
🎯 Target for lunch: ~700 kcal

Suggested meals (India region):
1. High protein balanced meal:
   Foods: brown rice:150, dal:100, paneer:80
   Total: ~680 cal, P:31g, C:74g, F:24g
   💡 Use: log_meal('brown rice:150, dal:100, paneer:80')
...
```

---

### 20. `recommend_exercise`

**Purpose:** Exercise suggestions based on sleep and goals

**Parameters:** None (auto-analyzes sleep data)

**Example:**

```
User: "Should I exercise today?"
→ recommend_exercise()
```

---

### 21. `recommend_from_pantry`

**Purpose:** Meal suggestions from available pantry items

**Parameters:**

- `meal_type` (str, optional): Meal type

**Example:**

```
User: "What can I make for dinner with what I have?"
→ recommend_from_pantry("dinner")
```

---

### 22. `recommend_from_routines`

**Purpose:** Time-based food suggestions from your routines

**Parameters:**

- `time_period` (str, optional): "current" (auto), "morning", "evening", etc.
- `filter_by_effort` (str, optional): "all", "easy", "medium", "hard"
- `include_pantry` (bool, optional): Include pantry items

**Example:**

```
User: "What do I usually eat in the morning?"
→ recommend_from_routines("morning", "easy")
```

---

## Pantry Management

### 23. `add_to_pantry`

**Purpose:** Track foods you currently have

**Parameters:**

- `food_name` (str): Food name (must exist in database)
- `quantity_grams` (float, optional): Amount available
- `notes` (str, optional): Notes ("in freezer", "expires soon")

**Example:**

```
User: "I bought chicken breast 500g and rice 1kg"
→ add_to_pantry("chicken breast", 500)
→ add_to_pantry("brown rice", 1000)
```

---

### 24. `remove_from_pantry`

**Purpose:** Remove food from pantry

**Example:**

```
User: "I'm out of eggs"
→ remove_from_pantry("eggs")
```

---

### 25. `list_my_pantry`

**Purpose:** Show all pantry items

**Example:**

```
User: "What's in my pantry?"
→ list_my_pantry()
```

---

## Food Routines

### 26. `add_to_food_routine`

**Purpose:** Set time-based food preferences

**Parameters:**

- `food_name` (str): Food name
- `morning` (bool, optional): Available in morning?
- `evening` (bool, optional): Available in evening?
- (+ other time periods)
- `preparation_type` (str, optional): "cooked", "raw", "instant"
- `effort_level` (str, optional): "easy", "medium", "hard"
- `typical_portion_grams` (float, optional): Usual serving size
- `preference_score` (int, optional): 1-10 rating

**Example:**

```
User: "I usually have bread and jam in the morning, it's easy to prepare"
→ add_to_food_routine("bread", morning=True, preparation_type="instant", effort_level="easy", typical_portion_grams=60, preference_score=8)
```

---

### 27. `list_food_routines`

**Purpose:** View all routines

---

### 28. `bulk_setup_routines`

**Purpose:** Quick setup multiple foods at once

**Parameters:**

- `morning_foods` (str): "food1,food2,food3"
- `evening_foods` (str): "food1,food2"
- `afternoon_foods` (str): "food1,food2"

**Example:**

```
User: "I usually eat bread, poha, or paratha in the morning, and maggie or chowmein in the evening"
→ bulk_setup_routines(
    morning_foods="bread,poha,paratha",
    evening_foods="maggie,chowmein"
)
```

---

## 🎯 Common User Flows

### Flow 1: First-Time Setup

```
1. set_user_profile(...)
2. add_to_pantry("chicken breast", 500)
3. bulk_setup_routines(morning="bread,oats", evening="roti,rice")
```

### Flow 2: Daily Tracking

```
1. log_sleep("23:00", "07:00")
2. log_meal("idli:150, dal:100")  # Breakfast
3. recommend_foods("lunch")
4. log_meal(...)  # Lunch based on recommendation
5. log_exercise("jogging", 30, "moderate")
6. get_daily_summary()
```

### Flow 3: Progress Checking

```
1. get_weight_trend(30)
2. get_nutrition_stats(7)
3. get_sleep_summary(14)
```

---

## 💡 Tips for LLM Usage

### Parsing User Input

**User says:** "I ate 2 rotis, dal, and some paneer"

**LLM should:**

1. Identify foods: roti, dal, paneer
2. Parse quantities: 2 rotis = 120g, dal ≈ 100g, paneer ≈ 80g
3. Call: `log_meal("roti:120, dal:100, paneer:80")`

### Handling Ambiguity

**User says:** "I had rice"

**LLM should ask:** "How much rice did you have? (e.g., 1 cup ≈ 150g)"

### Chaining Tools

**User says:** "Show me everything from today"

**LLM should call:**

1. `get_daily_nutrition()`
2. `get_sleep_summary(1)`
3. Check if exercise logged

---

This reference covers all 28 tools! LLMs reading this will understand exactly how to use your MCP server. 🎉
