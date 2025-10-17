# 🎯 Complete Usage Guide - Health MCP Server

This guide shows exactly how to use the health MCP server for your daily health tracking!

---

## 📅 Day 1: Getting Started

### Step 1: Set Your Profile

Tell the LLM about yourself:

**You say:** "I'm 1.75m tall, currently 75kg, want to reach 70kg. I need about 2000 calories per day. I'm moderately active, live in India, and I'm vegetarian."

**LLM calls:**

```
set_user_profile(
    height_m=1.75,
    target_weight_kg=70,
    daily_calorie_goal=2000,
    activity_level="moderate",
    region="India",
    dietary_preferences="vegetarian"
)
```

**Result:** ✅ Profile created with your goals!

---

## 🌅 Morning Routine

### Log Your Sleep

**You say:** "I slept at 11 PM last night and woke up at 7 AM"

**LLM calls:**

```
log_sleep("23:00", "07:00")
```

**Result:**

```
✓ Sleep logged for 2025-10-17:
  Slept: 23:00
  Woke: 07:00
  Duration: 8.0 hours
  Quality: good 😊
```

### Log Your Weight (Weekly)

**You say:** "I weighed myself today, I'm 75 kg"

**LLM calls:**

```
log_weight(75)
```

**Result:** ✓ Weight logged: 75.0 kg

### Breakfast

**You say:** "I had 2 idlis with sambar for breakfast"

**LLM interprets:** 2 idlis ≈ 150g, sambar ≈ 100g

**LLM calls:**

```
log_meal("idli:150, dal:100")
```

**Result:**

```
Meal logged for 2025-10-17:
✓ Idli (150g): 87cal, P:3.0g, C:18.0g, F:0.2g
✓ Dal (100g): 116cal, P:9.0g, C:20.0g, F:0.4g

📊 TOTAL: 203 calories, Protein: 12.0g, Carbs: 38.0g, Fats: 0.6g
```

---

## 🥗 Lunch Time

### Ask for Recommendations

**You say:** "What should I eat for lunch?"

**LLM calls:**

```
recommend_foods("lunch")
```

**Result:**

```
🍽️ Food Recommendations for Lunch:

📊 Today's Status:
  Goal: 2000 kcal
  Consumed: 203 kcal
  Remaining: 1797 kcal

🎯 Target for lunch: ~700 kcal

Suggested meals:

1. High protein balanced meal:
   Foods: brown rice:150, dal:100, paneer:80
   💡 Use: log_meal("brown rice:150, dal:100, paneer:80")

2. Vegetarian protein-rich:
   Foods: roti:3, paneer:80, spinach:100
   💡 Use: log_meal("roti:90, paneer:80, spinach:100")

3. Light vegetarian meal:
   Foods: white rice:150, dal:100, curd:100
   💡 Use: log_meal("white rice:150, dal:100, curd:100")
```

### Log Your Lunch

**You say:** "I'll have the roti, paneer and spinach"

**LLM calls:**

```
log_meal("roti:90, paneer:80, spinach:100")
```

**Result:**

```
✓ Roti (90g): 267cal, P:9.9g, C:40.5g, F:8.1g
✓ Paneer (80g): 212cal, P:14.4g, C:1.0g, F:16.0g
✓ Spinach (100g): 23cal, P:2.9g, C:3.6g, F:0.4g

📊 TOTAL: 502 calories, Protein: 27.2g, Carbs: 45.1g, Fats: 24.5g
```

---

## 🏃 Exercise Time

### Get Exercise Recommendations

**You say:** "Should I exercise today?"

**LLM calls:**

```
recommend_exercise()
```

**Result:**

```
💪 Exercise Recommendations:

😴 Sleep: 8.0 hours/night average
   ✅ Good energy - You can do intense workouts!

🎯 Goal: Weight loss (75.0kg → 70.0kg)

📋 Recommended Exercises:

1. Running (30-40 mins)
   - Burns ~400 cal
   - Great cardio
   - Builds endurance

2. HIIT Training (20 mins)
   - High calorie burn (~300 cal)
   - Boosts metabolism
   - Time efficient

3. Strength Training (40 mins)
   - Builds muscle
   - Burns ~250 cal
   - Increases metabolism

💡 Tips:
  - Exercise in morning for better energy
  - Stay hydrated (2-3L water/day)
  - Rest 1-2 days per week
```

### Log Your Exercise

**You say:** "I went for a 30-minute run"

**LLM calls:**

```
log_exercise("running", 30, "moderate")
```

**Result:**

```
✓ Exercise logged!
  Running: 30 min (moderate)
  🔥 Estimated calories burned: ~180 kcal
```

---

## 🌙 Evening & Dinner

### Afternoon Snack

**You say:** "I had a banana as a snack at 4 PM"

**LLM calls:**

```
log_meal("banana:120")
```

**Result:** ✓ Banana (120g): 107cal, P:1.3g, C:27.6g, F:0.4g

### Dinner Recommendation

**You say:** "What should I have for dinner?"

**LLM calls:**

```
recommend_foods("dinner")
```

**Result:** Light dinner suggestions based on remaining calories

### Log Dinner

**You say:** "I had 2 chapatis with dal and some spinach"

**LLM calls:**

```
log_meal("chapati:240, dal:100, spinach:50")
```

---

## 📊 End of Day Summary

### Complete Health Summary

**You say:** "Show me today's complete summary"

**LLM calls:**

```
get_daily_summary()
```

**Result:**

```
📅 Health Summary for 2025-10-17
==================================================

🍽️ NUTRITION:
  Calories: 1547 kcal
  Protein: 64.3g | Carbs: 198.2g | Fats: 37.8g

😴 SLEEP:
  23:00 → 07:00 (8.0 hours)
  Quality: good

💪 EXERCISE:
  • Running: 30 min (~180 kcal)
  Total burned: ~180 kcal

⚖️ WEIGHT: 75.0 kg

📊 NET CALORIES: 1367 kcal
```

---

## 📈 Weekly Review

### Check Sleep Patterns

**You say:** "How has my sleep been this week?"

**LLM calls:**

```
get_sleep_summary(7)
```

### Check Nutrition Trends

**You say:** "Show me my nutrition stats for the week"

**LLM calls:**

```
get_nutrition_stats(7)
```

### Check Weight Progress

**You say:** "What's my weight trend this month?"

**LLM calls:**

```
get_weight_trend(30)
```

---

## 💡 Pro Tips

### 1. **Be Natural with LLM**

Just talk normally:

- ❌ Don't say: "log_meal('chicken:150')"
- ✅ Say: "I ate grilled chicken breast for lunch, about 150 grams"

### 2. **LLM Will Parse for You**

The LLM understands:

- "2 rotis" → 60-90g
- "a bowl of rice" → 150-200g
- "handful of almonds" → 20-30g

### 3. **Add Custom Foods**

**You say:** "Add quinoa to the database - 120 cal, 4.4g protein, 21g carbs, 1.9g fat per 100g"

**LLM calls:**

```
add_food_to_database("quinoa", 120, 4.4, 21, 1.9, 2.8)
```

### 4. **Regional Preferences**

Set your region in profile, and recommendations will be tailored:

- **India**: Roti, dal, paneer, idli, dosa
- **Other**: Pasta, oatmeal, salmon, chicken

### 5. **Maintain Weight**

The system automatically:

- Tracks your intake vs goal
- Suggests appropriate meals
- Recommends exercise based on sleep quality
- Helps you stay on target!

---

## 🎯 Common Scenarios

### Scenario 1: Busy Day, Quick Meals

**You:** "I'm busy today, suggest quick meals"
**LLM:** Checks remaining calories, suggests quick 10-min options

### Scenario 2: Slept Poorly

**You:** "I slept only 5 hours last night"
**LLM:** Logs sleep, later recommends light exercises only

### Scenario 3: Cheat Day

**You:** "I had pizza and ice cream"
**LLM:** Logs it, suggests lighter meals for rest of day

### Scenario 4: Traveling

**You:** "I'm traveling, no access to specific foods"
**LLM:** Suggests common foods available anywhere

---

## 🚀 Start Today!

1. Set your profile
2. Log what you eat
3. Log when you sleep
4. Ask for recommendations
5. Track your progress!

The system learns your patterns and helps you maintain your target weight with region-appropriate foods and smart exercise recommendations! 🎉
