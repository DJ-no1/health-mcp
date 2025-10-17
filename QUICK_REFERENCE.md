# 🎴 QUICK REFERENCE CARD

## Essential Commands (Just say these to your LLM!)

### 🌅 Morning

```
"I slept at [TIME] and woke up at [TIME]"
"I weigh [NUMBER] kg today"
"I had [FOOD] for breakfast"
```

### 🥗 Meals

```
"I ate [FOOD DESCRIPTION]"
"What should I eat for lunch/dinner?"
"Show me available foods"
```

### 💪 Exercise

```
"Should I exercise today?"
"I did [EXERCISE] for [MINUTES] minutes"
```

### 📊 Tracking

```
"Show me today's summary"
"What's my progress this week?"
"How's my sleep been?"
```

### ⚙️ Setup (First Time)

```
"I'm [HEIGHT]m tall, [WEIGHT]kg, want to reach [TARGET]kg"
"I need [CALORIES] calories per day"
"I live in [REGION], I'm [DIET TYPE]"
```

---

## Food Database (24 items)

### Indian Foods 🇮🇳

- Roti, Chapati, Dal, Paneer
- Idli, Dosa, Samosa, Curd

### International 🌍

- Chicken, Salmon, Beef, Eggs
- Rice (white/brown), Pasta, Oatmeal
- Vegetables: Broccoli, Spinach, Sweet Potato
- Fruits: Banana, Apple
- Nuts: Almonds
- Dairy: Greek Yogurt
- Healthy Fats: Avocado

**Add more:** "Add [FOOD] to database with [NUTRITION INFO]"

---

## Features at a Glance

| Feature             | Tool               | What It Does                       |
| ------------------- | ------------------ | ---------------------------------- |
| 🍽️ Log Food         | log_meal           | Tracks what you ate with nutrients |
| 😴 Log Sleep        | log_sleep          | Tracks sleep duration & quality    |
| ⚖️ Log Weight       | log_weight         | Tracks weight over time            |
| 💪 Log Exercise     | log_exercise       | Tracks workouts & calories burned  |
| 🎯 Food Suggestions | recommend_foods    | Region-based meal recommendations  |
| 🏃 Exercise Plans   | recommend_exercise | Based on sleep & goals             |
| 📊 Daily Summary    | get_daily_summary  | Complete health dashboard          |

---

## Smart Features

### 🧠 Context-Aware Recommendations

- **Low Calories Left** → Suggests lighter meals
- **Slept Well** → Recommends intense workouts
- **Poor Sleep** → Suggests light exercises
- **Weight Loss Goal** → More cardio, fewer calories
- **Weight Gain Goal** → Strength training, more calories

### 🌍 Region-Based

Set your region, get appropriate foods:

- **India** → Roti, dal, paneer, idli
- **Other** → Pasta, oatmeal, salmon

### 🎯 Goal-Oriented

Every recommendation helps you:

- Reach target weight
- Stay energetic
- Sleep better
- Eat balanced

---

## Database Tables

```
📦 food_database     → Nutrition info (per 100g)
📝 meals            → What you ate, when, nutrients
😴 sleep_log        → Sleep & wake times
⚖️ weight_log       → Weight tracking
💪 exercise_log     → Workout tracking
👤 user_profile     → Your goals & preferences
```

---

## File Structure

```
health-mcp/
├── main.py                    → Main server (run this!)
├── health_data.db             → Your data (auto-created)
├── README.md                  → Full documentation
├── USAGE_GUIDE.md             → Step-by-step guide
├── IMPLEMENTATION_SUMMARY.md  → What was built
└── test_server.py            → Test script
```

---

## Run the Server

```bash
# Option 1: Direct
python main.py

# Option 2: With uv
uvx --from . health-mcp

# Test
python test_server.py
```

---

## Integration (Claude Desktop)

```json
{
  "mcpServers": {
    "health": {
      "command": "python",
      "args": ["C:/path/to/health-mcp/main.py"]
    }
  }
}
```

---

## Example Conversation

```
You: "I'm 1.75m, 75kg, want to be 70kg, live in India"
AI: ✓ Profile set!

You: "I slept at 11 PM, woke at 7 AM"
AI: ✓ 8 hours logged!

You: "I had 2 idlis and sambar"
AI: ✓ 203 calories logged

You: "What should I eat for lunch?"
AI: 🍽️ Try: roti, paneer, spinach (~500 cal)
    You have 1797 cal remaining

You: "I'll have that"
AI: ✓ Logged! 502 calories

You: "Should I exercise?"
AI: 💪 You slept well (8h)! Try:
    - Running 30 min (~400 cal)
    - HIIT 20 min (~300 cal)

You: "I went running for 30 minutes"
AI: ✓ Great! ~180 cal burned

You: "Show today's summary"
AI: 📊 Food: 705 cal | Sleep: 8h | Exercise: 30 min
    Net: 525 cal | Goal: 2000 cal
```

---

## 🎯 Remember

1. **Talk naturally** - LLM understands context
2. **Be consistent** - Log daily for best recommendations
3. **Trust the system** - It learns your patterns
4. **Stay honest** - Track everything for accurate insights

---

## 🚀 Status: READY TO USE!

**Tools:** 20 ✅
**Foods:** 24 (expandable) ✅
**Regions:** Supported ✅
**Smart Recommendations:** Active ✅
**Database:** Working ✅

**Start tracking your health today!** 🎉
