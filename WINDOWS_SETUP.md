# 🪟 Windows Setup Guide for BrainPlay v2.0

This guide will help you set up and run the enhanced BrainPlay game with session management on Windows.

## 📋 Prerequisites

### Check if Python is Installed
Open **Command Prompt** (cmd) and type:
```cmd
python --version
```

If you see a version number (like `Python 3.9.7`), you're good to go!

If not, download Python from: https://www.python.org/downloads/

**Important**: During installation, check "Add Python to PATH"

---

## 🚀 Step-by-Step Installation

### Step 1: Create Project Folder
```cmd
mkdir brainplay-game
cd brainplay-game
```

### Step 2: Copy Game Files
Copy all the Python files to your `brainplay-game` folder:
- `main.py`
- `questions.py`
- `score.py`
- `session.py` (NEW)
- `exceptions.py`
- `requirements.txt`
- `README.md`
- `WINDOWS_SETUP.md`
- `utils/` folder with all its files
- `data/` folder

### Step 3: Create Virtual Environment
```cmd
python -m venv venv
```

### Step 4: Activate Virtual Environment
```cmd
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 5: Install Dependencies
```cmd
pip install -r requirements.txt
```

### Step 6: Run the Game!
```cmd
python main.py
```

---

## 🎮 Playing the Enhanced Game

### Basic Commands
```cmd
# Start normal game
python main.py

# Specify player name
python main.py --player "Your Name"

# Different difficulty modes
python main.py --mode easy
python main.py --mode normal
python main.py --mode hard

# View data
python main.py --history
python main.py --stats

# Help and version
python main.py --help
python main.py --version
```

### Game Features
- **Player Profiles**: Your stats are saved between games
- **Session Tracking**: Each game has a unique session ID
- **Comprehensive Logging**: All events are logged to `data/game.log`
- **Achievement System**: Unlock badges as you play
- **Persistent Data**: Your progress is saved automatically

### Game Controls
- Type your answer and press **Enter**
- Type `quit`, `exit`, `n`, or `no` to quit
- Press **Ctrl+C** to force quit

---

## 📊 Understanding the Data Files

After playing, you'll see these files in the `data/` folder:

### `game.log`
Contains detailed logs of all game events:
```
2025-01-02 15:00:00,123 - session - INFO - Created new player: Alice (ID: abc123...)
2025-01-02 15:00:01,456 - __main__ - INFO - Game started - Player: Alice, Session: def456...
2025-01-02 15:00:15,789 - questions - INFO - Generated number_guess question in normal mode
```

### `players.json`
Your player profile and statistics:
```json
{
  "abc123...": {
    "name": "Alice",
    "total_games": 5,
    "total_wins": 3,
    "best_score": 85,
    "created_date": "2025-01-02T15:00:00",
    "last_played": "2025-01-02T16:30:00"
  }
}
```

### `game_history.json`
Complete game history with session details:
```json
[
  {
    "session_id": "def456...",
    "player_name": "Alice",
    "mode": "normal",
    "final_score": 50,
    "rounds": [...]
  }
]
```

---

## 🔧 Troubleshooting

### Problem: "python is not recognized"
**Solution**: 
1. Reinstall Python from python.org
2. Check "Add Python to PATH" during installation
3. Restart Command Prompt

### Problem: "pip is not recognized"
**Solution**:
```cmd
python -m pip install -r requirements.txt
```

### Problem: Virtual environment won't activate
**Solution**:
```cmd
# Try this instead:
venv\Scripts\activate.bat
```

### Problem: Permission denied
**Solution**:
1. Run Command Prompt as Administrator
2. Or use: `python -m pip install --user -r requirements.txt`

### Problem: Module not found
**Solution**:
```cmd
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Session data not saving
**Solution**:
1. Check if `data/` folder exists
2. Ensure you have write permissions
3. Check `data/game.log` for error messages

---

## 📁 File Structure Check

Your folder should look like this:
```
brainplay-game/
├── main.py
├── questions.py
├── score.py
├── session.py          # NEW - Session management
├── exceptions.py
├── requirements.txt
├── README.md
├── WINDOWS_SETUP.md
├── utils/
│   ├── __init__.py
│   ├── decorators.py
│   ├── context.py
│   └── file_io.py
├── data/
│   ├── .gitkeep
│   ├── game.log         # Created after first run
│   ├── players.json     # Created after first run
│   ├── sessions.json    # Created after first run
│   └── game_history.json # Created after first run
└── venv/
    └── (virtual environment files)
```

---

## ✅ Quick Test

After setup, test if everything works:

1. **Activate virtual environment**: `venv\Scripts\activate`
2. **Run game**: `python main.py`
3. **Enter your name**: When prompted, enter a player name
4. **Play a round**: Answer a question
5. **Check logs**: Look at `data/game.log` to see session tracking
6. **View stats**: Run `python main.py --stats` to see your profile

If you see the game interface, session tracking, and can view your stats, you're all set! 🎉

---

## 🆕 New Features to Try

### Player Management
```cmd
# Play with different players
python main.py --player "Alice"
python main.py --player "Bob"

# View all player statistics
python main.py --stats
```

### Session Tracking
- Each game gets a unique session ID
- Session duration is tracked
- All events are logged with session context

### Enhanced Statistics
- Player win rates
- Best scores
- Game history with session details
- Achievement tracking

---

## 🆘 Need Help?

If you're still having issues:

1. **Check Python version**: Must be 3.8 or higher
2. **Verify all files are copied**: See file structure above
3. **Ensure virtual environment is activated**: Look for `(venv)` in prompt
4. **Check the logs**: Look at `data/game.log` for error messages
5. **Try running without virtual environment**: Skip steps 3-4 and run directly

---

## 🎯 Next Steps

Once the game is running:

1. **Play multiple games** to see session tracking in action
2. **Check the data files** to understand how information is stored
3. **Read the logs** to see comprehensive event tracking
4. **Explore the code** to learn about session management
5. **Try different players** to see profile management
6. **View statistics** to see your progress over time

**Have fun learning Python with enhanced session management! 🐍🎮**