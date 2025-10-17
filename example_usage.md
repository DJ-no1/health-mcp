# Example Usage with an LLM

## Scenario: User tracking their meals throughout the day

### Morning (7:30 AM)

**User:** "I had 2 eggs and a banana for breakfast"

**LLM interprets:**

- 2 eggs ≈ 100g
- 1 banana ≈ 120g

**LLM calls:**

```
log_meal("eggs:100, banana:120")
```

**Server returns:**

```
Meal logged for 2025-10-17:

✓ Eggs (100g): 155cal, P:13.0g, C:1.1g, F:11.0g
✓ Banana (120g): 107cal, P:1.3g, C:27.6g, F:0.4g

📊 TOTAL: 262 calories, Protein: 14.3g, Carbs: 28.7g, Fats: 11.4g, Fiber: 3.1g
```

---

### Lunch (1:00 PM)

**User:** "For lunch I ate grilled chicken breast about 150g with brown rice and some broccoli"

**LLM interprets:**

- Chicken breast: 150g
- Brown rice: 200g (typical serving)
- Broccoli: 100g

**LLM calls:**

```
log_meal("chicken breast:150, brown rice:200, broccoli:100")
```

**Server returns:**

```
Meal logged for 2025-10-17:

✓ Chicken Breast (150g): 248cal, P:46.5g, C:0.0g, F:5.4g
✓ Brown Rice (200g): 224cal, P:5.2g, C:48.0g, F:1.8g
✓ Broccoli (100g): 34cal, P:2.8g, C:7.0g, F:0.4g

📊 TOTAL: 506 calories, Protein: 54.5g, Carbs: 55.0g, Fats: 7.6g, Fiber: 4.4g
```

---

### Snack (4:00 PM)

**User:** "I had a handful of almonds as a snack"

**LLM interprets:**

- Handful ≈ 30g

**LLM calls:**

```
log_meal("almonds:30")
```

**Server returns:**

```
Meal logged for 2025-10-17:

✓ Almonds (30g): 174cal, P:6.3g, C:6.6g, F:15.0g

📊 TOTAL: 174 calories, Protein: 6.3g, Carbs: 6.6g, Fats: 15.0g, Fiber: 3.8g
```

---

### End of Day

**User:** "What did I eat today?"

**LLM calls:**

```
get_daily_nutrition()
```

**Server returns:**

```
📅 Nutrition Summary for 2025-10-17

Meals logged:
  • 07:30 - Eggs (100g): 155cal, P:13.0g, C:1.1g, F:11.0g
  • 07:30 - Banana (120g): 107cal, P:1.3g, C:27.6g, F:0.4g
  • 13:00 - Chicken Breast (150g): 248cal, P:46.5g, C:0.0g, F:5.4g
  • 13:00 - Brown Rice (200g): 224cal, P:5.2g, C:48.0g, F:1.8g
  • 13:00 - Broccoli (100g): 34cal, P:2.8g, C:7.0g, F:0.4g
  • 16:00 - Almonds (30g): 174cal, P:6.3g, C:6.6g, F:15.0g

==================================================
📊 DAILY TOTALS:
  Calories: 942 kcal
  Protein:  75.1g (300 kcal, 32%)
  Carbs:    90.3g (361 kcal, 38%)
  Fats:     34.0g (306 kcal, 32%)
  Fiber:    11.3g
```

---

### Weekly Stats

**User:** "How has my nutrition been this week?"

**LLM calls:**

```
get_nutrition_stats(7)
```

**Server returns:**

```
📈 Nutrition Stats for Last 7 Days:

2025-10-17: 942 kcal | P:75g | C:90g | F:34g | Fiber:11g
2025-10-16: 1850 kcal | P:95g | C:180g | F:65g | Fiber:25g
2025-10-15: 1650 kcal | P:88g | C:165g | F:58g | Fiber:22g
... (more days)

==================================================
📊 Averages over 7 days:
  Calories: 1680 kcal/day
  Protein:  88g/day
  Carbs:    175g/day
  Fats:     60g/day
  Fiber:    23g/day
```

---

## Adding New Foods

**User:** "Can you add quinoa to the database? It has about 120 calories per 100g, 4.4g protein, 21g carbs, 1.9g fat, and 2.8g fiber"

**LLM calls:**

```
add_food_to_database("quinoa", 120, 4.4, 21, 1.9, 2.8)
```

**Server returns:**

```
✓ Added 'quinoa' to food database: 120cal, P:4.4g, C:21g, F:1.9g, Fiber:2.8g (per 100g)
```

Now the LLM can use "quinoa" in future meal logging!

---

## Key Benefits

1. **Automatic Nutrient Breakdown** - LLM doesn't need to know nutrition facts
2. **Persistent Storage** - All data saved in SQLite database
3. **Time Tracking** - Every meal logged with timestamp
4. **Flexible Parsing** - LLM can interpret natural language and convert to tool calls
5. **Extensible** - Easy to add new foods to the database
6. **Statistics** - Track progress over time

The database handles all the math, the LLM just needs to:

- Parse user input
- Make appropriate tool calls
- Present results in a friendly way
