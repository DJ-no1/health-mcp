# 🚀 MCP Client Setup Guide

This guide shows how to configure different MCP clients to use the Health MCP Server.

---

## 📱 Claude Desktop

### Step 1: Locate Config File

**Windows:**

```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**

```
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Add Health MCP Server

Open the config file and add:

```json
{
  "mcpServers": {
    "health-tracker": {
      "command": "uv",
      "args": ["--directory", "/ABSOLUTE/PATH/TO/health-mcp", "run", "main.py"]
    }
  }
}
```

**Or using Python directly:**

```json
{
  "mcpServers": {
    "health-tracker": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/health-mcp/main.py"]
    }
  }
}
```

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop. You should see the Health Assistant server connected!

### Step 4: Test It!

Try: **"I ate 2 rotis and dal for breakfast"**

Claude will automatically use the `log_meal` tool to track your nutrition!

---

## 🔧 VS Code with MCP Extension

### Step 1: Install MCP Extension

Search for "Model Context Protocol" in VS Code extensions.

### Step 2: Add to workspace settings

Create `.vscode/settings.json`:

```json
{
  "mcp.servers": {
    "health-tracker": {
      "command": "python",
      "args": ["${workspaceFolder}/main.py"]
    }
  }
}
```

### Step 3: Reload VS Code

Press `Ctrl+Shift+P` → "Reload Window"

---

## 🐳 Alternative: Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .

RUN pip install fastmcp

CMD ["python", "main.py"]
```

Then in config:

```json
{
  "mcpServers": {
    "health-tracker": {
      "command": "docker",
      "args": ["run", "-i", "health-mcp"]
    }
  }
}
```

---

## 🧪 Testing the Connection

### Method 1: Claude Desktop UI

Look for the 🔌 plugin icon in Claude Desktop. Click it to see:

- Connected servers
- Available tools (should show 28 tools)
- Server status

### Method 2: Direct Test

Ask Claude:

```
"What health tracking tools do you have available?"
```

Claude should list all 28 tools with descriptions!

### Method 3: Quick Functionality Test

```
User: "Set up my profile: I'm 1.75m tall, weigh 75kg,
       want to reach 70kg, need 2000 calories daily,
       I live in India and I'm vegetarian"

Claude will call: set_user_profile()

User: "What should I eat for breakfast?"

Claude will call: recommend_foods("breakfast")
```

---

## 📊 What Claude Can See

When your MCP server connects, Claude receives:

### 1. **Server Metadata**

```
Name: Health Assistant
Description: Track meals, sleep, exercise, weight with AI recommendations
Version: 0.1.0
```

### 2. **All 28 Tools with:**

- Tool name (e.g., `log_meal`)
- Full docstring explaining usage
- Parameter types and defaults
- Return type (always `str`)

### 3. **Tool Categories** (Claude auto-groups)

- Basic Health Tools (4)
- Nutrition Tracking (8)
- Sleep Management (2)
- Weight Tracking (2)
- User Profile (2)
- Smart Recommendations (4)
- Pantry & Routines (6)

### 4. **Example Usage Patterns**

Claude learns from your docstrings! Example:

```python
@mcp.tool()
def log_meal(food_items: str, date: str = None) -> str:
    """Log a meal by breaking it down into nutrients.

    Args:
        food_items: "food1:grams, food2:grams" format
        date: YYYY-MM-DD (default: today)

    Example: log_meal("chicken breast:150, brown rice:100")
    """
```

Claude sees this and knows:
✅ How to format the `food_items` parameter
✅ Date is optional
✅ Example usage pattern

---

## 🎯 Best Practices for LLM Usage

### ✅ DO:

```
"I had 2 idlis and sambar for breakfast"
→ Claude parses: idli:150g, dal:100g → log_meal()

"What can I cook with what I have?"
→ Claude calls: recommend_from_pantry()

"Show me my progress this week"
→ Claude calls: get_nutrition_stats(days=7)
```

### ❌ DON'T:

```
"Call the nutrition logging function with chicken"
→ Too vague, lacks quantity

"Execute log_meal with invalid JSON"
→ Claude handles this, but descriptive input is better
```

---

## 🐛 Troubleshooting

### Server Not Connecting

**Check:**

1. Config file path is correct
2. Python/uv is in system PATH
3. No syntax errors in config JSON
4. Absolute paths (not relative)

**Test manually:**

```bash
cd /path/to/health-mcp
python main.py
```

Should start without errors.

### Tools Not Showing

**Check:**

1. Restart Claude Desktop completely
2. Check Claude logs: `%APPDATA%\Claude\logs`
3. Verify all `@mcp.tool()` decorators exist

### Database Issues

**Fix:**

```bash
# Delete and reinitialize
rm health_data.db
python main.py  # Auto-creates fresh DB
```

---

## 📖 Next Steps

Once connected:

1. **Read**: [USAGE_GUIDE.md](./USAGE_GUIDE.md) - Detailed usage examples
2. **Read**: [README.md](./README.md) - Feature overview
3. **Try**: Start with profile setup, then log a meal!

---

## 💡 Advanced: Multiple MCP Servers

You can run multiple MCP servers simultaneously:

```json
{
  "mcpServers": {
    "health-tracker": {
      "command": "python",
      "args": ["/path/to/health-mcp/main.py"]
    },
    "file-manager": {
      "command": "python",
      "args": ["/path/to/file-mcp/main.py"]
    },
    "calendar": {
      "command": "python",
      "args": ["/path/to/calendar-mcp/main.py"]
    }
  }
}
```

Claude will have access to ALL tools from ALL servers! 🎉

---

**Need help?** Open an issue on GitHub or check FastMCP documentation: https://github.com/jlowin/fastmcp
