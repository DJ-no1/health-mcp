# Health MCP Server 🏥

A comprehensive local MCP (Model Context Protocol) server for complete health tracking and personalized recommendations.

## ✨ Features

### 📊 Nutrition Tracking:

- **log_meal** - Log what you ate with automatic nutrient calculation
- **list_foods** - Browse 23+ foods (International + Indian foods)
- **get_daily_nutrition** - Complete daily nutrition summary
- **add_food_to_database** - Add custom foods
- **get_nutrition_stats** - Multi-day nutrition statistics

### 😴 Sleep Tracking:

- **log_sleep** - Track when you slept and woke up
- **get_sleep_summary** - Analyze sleep patterns and quality

### ⚖️ Weight Management:

- **log_weight** - Track weight over time
- **get_weight_trend** - Visualize weight changes

### 👤 User Profile & Goals:

- **set_user_profile** - Set height, target weight, calorie goals, region, diet preferences
- **get_user_profile** - View your profile

### 🤖 Smart Recommendations:

- **recommend_foods** - Get meal suggestions based on:
  - Your daily calorie goal
  - What you've already eaten today
  - Your region (region-specific foods!)
  - Remaining calories
- **recommend_exercise** - Get exercise recommendations based on:
  - Your sleep quality and duration
  - Target weight goals
  - Activity level
  - Energy levels

### 💪 Exercise Tracking:

- **log_exercise** - Track workouts with calorie burn estimates
- **get_daily_summary** - Complete daily health dashboard

### 🏃 Basic Health Tools:

- **calculate_bmi** - BMI calculator
- **daily_water_intake** - Water intake recommendations
- **steps_to_calories** - Convert steps to calories
- **heart_rate_zone** - Training heart rate zones

## 🎯 How It Works

This is exactly what you asked for! The LLM can now:

1. **Track Everything You Tell It:**

   - "I ate 2 rotis, dal, and paneer" → Logs meal with nutrients
   - "I slept at 11 PM and woke up at 7 AM" → Logs sleep duration
   - "I weigh 75 kg today" → Tracks weight

2. **Smart Food Recommendations:**

   - Calculates remaining calories for the day
   - Suggests region-appropriate meals (Indian/International)
   - Recommends portion sizes to meet your goals

3. **Personalized Exercise Advice:**

   - Analyzes your sleep quality
   - Considers your weight goals
   - Recommends appropriate intensity exercises

4. **Complete Health Dashboard:**
   - See everything in one place
   - Track progress over time
   - Maintain or reach your target weight

## 💾 Database

SQLite database (`health_data.db`) with:

- **food_database** - 23 foods (chicken, rice, dal, roti, paneer, etc.)
- **meals** - Every meal you log with timestamp
- **sleep_log** - Sleep and wake times
- **weight_log** - Weight tracking
- **exercise_log** - Workout tracking
- **user_profile** - Your goals and preferences

## 🚀 Quick Start

```bash
# Install dependencies
pip install fastmcp

# Run the server
python main.py
```

## 📖 Example Usage

### Day 1: Setup

```
LLM: "Let me set up your profile"
→ set_user_profile(height_m=1.75, target_weight_kg=70, daily_calorie_goal=2000,
                    activity_level="moderate", region="India", dietary_preferences="vegetarian")
```

### Morning

```
You: "I slept at 11 PM and woke up at 7 AM"
LLM: → log_sleep("23:00", "07:00")
Response: "✓ Sleep logged: 8 hours (good quality)"

You: "I had 2 idlis and sambar for breakfast"
LLM: → log_meal("idli:150, dal:100")
Response: "✓ Logged 203 calories, Protein: 11g..."
```

### Lunch Time

```
You: "What should I eat for lunch?"
LLM: → recommend_foods("lunch")
Response: "
🍽️ Food Recommendations:
📊 Consumed: 203 kcal, Remaining: 1797 kcal
🎯 Target for lunch: ~700 kcal

Suggested meals:
1. High protein balanced meal:
   Foods: brown rice:150, dal:100, paneer:80
   💡 Use: log_meal('brown rice:150, dal:100, paneer:80')
..."

You: "I'll have that"
LLM: → log_meal("brown rice:150, dal:100, paneer:80")
```

### Evening

```
You: "Should I exercise today?"
LLM: → recommend_exercise()
Response: "
💪 Exercise Recommendations:
😴 Sleep: 8 hours (Good energy - You can do intense workouts!)
🎯 Goal: Maintain weight

1. Brisk Walking/Jogging (30 mins) - Burns ~250 cal
2. Bodyweight Exercises (20 mins) - Burns ~180 cal
..."

You: "I did 30 minutes of jogging"
LLM: → log_exercise("jogging", 30, "moderate")
```

### Night

```
You: "Show me today's summary"
LLM: → get_daily_summary()
Response: "
📅 Health Summary for 2025-10-17
==================================================
🍽️ NUTRITION: 1450 kcal
😴 SLEEP: 23:00 → 07:00 (8 hours)
💪 EXERCISE: Jogging 30 min (~180 kcal)
⚖️ WEIGHT: 72 kg
📊 NET CALORIES: 1270 kcal
"
```

## 🌍 Region Support

The server includes region-specific foods:

**India:** roti, dal, paneer, chapati, idli, dosa, curd, samosa
**International:** chicken, rice, oatmeal, salmon, pasta, eggs, etc.

Set your region in profile for customized meal recommendations!

## 🎯 Weight Management

The system helps you:

- **Maintain weight**: Balanced recommendations
- **Lose weight**: Lower calorie meals, more cardio
- **Gain weight**: Higher calorie meals, strength training

## 📱 Integration

Add to your MCP client (Claude Desktop, etc.):

```json
{
  "mcpServers": {
    "health": {
      "command": "python",
      "args": ["path/to/health-mcp/main.py"]
    }
  }
}
```

## 🔧 Tools Summary

**Total: 20 tools** organized in 7 categories:

1. Basic Health (4 tools)
2. Nutrition Tracking (5 tools)
3. Sleep Tracking (2 tools)
4. Weight Tracking (2 tools)
5. User Profile (2 tools)
6. Smart Recommendations (2 tools)
7. Exercise & Summary (3 tools)

---

**This is exactly what you wanted:** Tell the LLM what you ate and when you slept, and it will track everything, recommend region-based foods to maintain your weight, and suggest exercises to keep you healthy and energetic! 🎉
