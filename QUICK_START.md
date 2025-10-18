# 🚀 Health MCP Quick Reference

One-page cheat sheet for common tasks.

---

## 🎯 First-Time Setup (5 minutes)

```
1. "Set up my profile: I'm 1.75m tall, weigh 75kg, want to reach 70kg,
    need 2000 calories daily, I live in India, I'm vegetarian"

2. "Add these to my pantry: chicken 500g, rice 1kg, dal 500g, eggs 10 pieces"

3. "I usually eat bread or poha in morning, roti and dal for lunch"
```

---

## 📅 Daily Routine

### Morning

```
1. "I slept at 11 PM and woke up at 7 AM"
2. "I weigh 74.5 kg today" (once a week)
3. "I had 2 idlis and sambar for breakfast"
4. "What should I eat for lunch?"
```

### Afternoon

```
5. "I ate roti with dal and paneer" (150g roti, 100g dal, 80g paneer)
6. "Should I exercise today?"
```

### Evening

```
7. "I did 30 minutes of jogging"
8. "Show me today's summary"
```

---

## 🔥 Most Used Commands

### Tracking

```
✅ "I ate [describe meal]"
✅ "I slept at [time] and woke at [time]"
✅ "I weigh [X] kg"
✅ "I exercised [activity] for [X] minutes"
```

### Getting Recommendations

```
✅ "What should I eat for [breakfast/lunch/dinner]?"
✅ "What can I cook with what I have?"
✅ "Should I exercise today?"
✅ "What do I usually eat in the morning?"
```

### Viewing Progress

```
✅ "Show me today's summary"
✅ "How well did I sleep this week?"
✅ "Show my weight trend for the last month"
✅ "What's my nutrition like this week?"
```

### Managing Data

```
✅ "What's in my pantry?"
✅ "Add [food] to pantry"
✅ "I'm out of [food]"
✅ "What foods can I track?"
✅ "Add [new food] to database"
```

---

## 🎨 Example Conversations

### Meal Logging

```
You: "I ate 2 rotis with dal and some paneer for lunch"

Claude: I'll log that meal for you.
→ Calls: log_meal("roti:120, dal:100, paneer:80")

Response: "✓ Logged 672 calories
  Roti: 356 cal, Protein: 13g
  Dal: 116 cal, Protein: 9g
  Paneer: 212 cal, Protein: 14g

📊 Total today: 1144/2000 calories"
```

---

### Getting Recommendations

```
You: "What should I eat for dinner? I want something easy to make"

Claude: Let me check your goals and what you've eaten today.
→ Calls: recommend_from_routines("evening", filter_by_effort="easy")

Response: "🌆 Evening Food Options:

📊 Consumed: 1144/2000 cal | Remaining: 856 cal

⚡ Easy Options:
  • Maggie (instant) - 400 cal
  • Bread with jam - 350 cal

Recommended: Maggie with vegetables for balanced meal
Use: log_meal('maggie:100, spinach:50')"
```

---

### Progress Tracking

```
You: "Show me my progress this week"

Claude: I'll get your weekly summary.
→ Calls: get_nutrition_stats(7), get_sleep_summary(7), get_weight_trend(7)

Response: "📊 Weekly Summary (Oct 11-18):

🍽️ NUTRITION:
  Average: 1850 cal/day (goal: 2000)
  Protein: 68g/day

😴 SLEEP:
  Average: 7.2 hours/night
  Quality: Mostly good

⚖️ WEIGHT:
  Start: 75 kg → Now: 73.5 kg
  Change: -1.5 kg (on track!)"
```

---

## 🛠️ Advanced Features

### Pantry Management

```
"I bought chicken 500g, rice 1kg, eggs 12 pieces"
→ Adds to pantry

"What can I make with what I have?"
→ Suggests meals from your pantry only

"Show my pantry"
→ Lists all available foods
```

---

### Food Routines (Time-Based)

```
"I usually eat bread, oats, or poha in the morning"
→ Sets morning routine

"What do I normally eat in the evening?"
→ Shows your evening food routine

"Set up routines: morning is bread,poha; evening is maggie,chowmein"
→ Bulk setup
```

---

### Health Calculations

```
"What's my BMI?"
→ Calculates from profile or you provide weight/height

"How much water should I drink?"
→ Based on your weight

"I walked 10,000 steps, how many calories is that?"
→ Estimates calorie burn

"What are my heart rate zones?" (if age set)
→ Shows training zones
```

---

## 🎯 Pro Tips

### For Best Results:

1. **Set profile first** - Goals enable smart recommendations
2. **Be specific with quantities** - "2 rotis" is better than "some roti"
3. **Log consistently** - Daily tracking = better insights
4. **Check recommendations** - Let AI help you plan meals
5. **Review weekly** - Use `get_nutrition_stats(7)` every Sunday

### Common Quantities:

- 1 roti = 60g
- 1 idli = 75g
- 1 dosa = 100g
- 1 cup rice = 150g
- 1 egg = 50g
- 1 banana = 120g
- 1 apple = 180g

---

## 🐛 Troubleshooting

### "Food not found in database"

```
"Add quinoa to database: 120 cal, 4g protein, 21g carbs, 2g fat per 100g"
```

### "Claude doesn't see the server"

1. Check config file path is correct
2. Restart Claude Desktop completely
3. Verify no JSON syntax errors

### "Wrong quantities logged"

```
Just log again with correct amounts - duplicates are OK for tracking
```

---

## 📱 Quick Access

After setup, just talk naturally:

- ✅ "I ate breakfast" → Claude will ask what you ate
- ✅ "Track my meal" → Claude will guide you
- ✅ "Health summary" → Shows today's overview
- ✅ "Weekly report" → 7-day stats

---

**Need detailed help?**

- Tool docs: [TOOL_REFERENCE.md](./TOOL_REFERENCE.md)
- Usage guide: [USAGE_GUIDE.md](./USAGE_GUIDE.md)
- Setup help: [MCP_SETUP.md](./MCP_SETUP.md)
