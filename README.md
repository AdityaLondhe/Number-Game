# 🧠 BrainPlay: Win or Lose v2.0

A comprehensive Command-Line Interactive Python Game with **Session Management** and **Player Tracking** that demonstrates **advanced Python concepts** and **best practices** for real-world software development.

## 🎯 Game Overview

**BrainPlay** challenges players with two types of mathematical questions:
1. **Square Calculation**: Calculate the square of a number (e.g., "What is 7²?" Answer: 49)
2. **Square Root**: Find the square root of perfect squares (e.g., "What is √144?" Answer: 12)

### 🎮 Game Rules
- ✅ **+10 points** for correct answers
- ❌ **-5 points** for wrong answers  
- 🏆 **WIN** when you reach 50+ points
- 👋 **LOSE** if you quit before winning

### 🆕 New Features in v2.0
- 👤 **Player Profiles** with persistent statistics
- 🎮 **Session Management** with unique session IDs
- 📊 **Comprehensive Logging** of all game events
- 📈 **Enhanced Statistics** and achievement tracking
- 💾 **Session Data Persistence** across game restarts

---

## 🚀 Quick Start for Windows

### Prerequisites
- **Python 3.8+** (recommended: Python 3.9+)
- **pip** package manager

### Installation Steps

1. **Create project directory**:
   ```cmd
   mkdir brainplay-game
   cd brainplay-game
   ```

2. **Copy all the game files** to this directory

3. **Create virtual environment**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the game**:
   ```cmd
   python main.py
   ```

### CLI Options
```cmd
# Basic gameplay
python main.py                           # Normal mode
python main.py --mode easy               # Easy difficulty
python main.py --mode hard               # Hard difficulty

# Player management
python main.py --player "Your Name"      # Specify player name

# Data viewing
python main.py --history                 # Show game history
python main.py --stats                   # Show player statistics

# Help and version
python main.py --help                    # Show all options
python main.py --version                 # Show version
```

---

## 🏗️ Enhanced Project Structure

```
brainplay-game/
├── main.py                 # 🎯 Entry point & game loop with session management
├── questions.py            # 🏭 Question factory & generators (FIXED)
├── score.py               # 📊 Score management (Singleton)
├── session.py             # 👤 Session & player management (NEW)
├── exceptions.py          # ⚠️ Custom exception hierarchy
├── utils/                 # 🛠️ Utility modules
│   ├── __init__.py
│   ├── decorators.py      # 🎨 Decorators & closures
│   ├── context.py         # 📋 Context managers
│   └── file_io.py         # 💾 File I/O operations
├── data/                  # 📁 Game data storage
│   ├── .gitkeep
│   ├── game.log           # 📝 Comprehensive game logs
│   ├── players.json       # 👤 Player profiles
│   ├── sessions.json      # 🎮 Session history
│   └── game_history.json  # 📊 Game data
├── requirements.txt       # 📦 Dependencies
└── README.md             # 📖 This file
```

---

## 🎮 Game Features

### ✅ **Correct Question Types**
1. **Square Calculation**: "What is X²?" (e.g., "What is 7²?")
   - Player calculates the square of a given number
   - Answer: X × X (e.g., 7² = 49)
   - Difficulty affects the range of base numbers

2. **Square Root**: "What is √X?" (e.g., "What is √144?")
   - Player calculates the square root of perfect squares
   - Answer: The number that when squared gives X (e.g., √144 = 12)
   - Difficulty affects the range of perfect squares

### 🆕 **Session Management**
- **Unique Session IDs** for each game
- **Player Profiles** with persistent statistics
- **Session Duration** tracking
- **Comprehensive Logging** of all events

### 📊 **Enhanced Statistics**
- **Player Stats**: Total games, wins, best score, win rate
- **Session Data**: Duration, rounds played, accuracy
- **Achievement System**: Unlockable badges and milestones
- **Historical Data**: Complete game history with session details

---

## 🧠 Advanced Python Concepts Demonstrated

### 1. **Session Management & Data Persistence**
- ✅ Player profile management with dataclasses
- ✅ Session tracking with unique IDs
- ✅ Persistent data storage across game sessions
- ✅ JSON serialization/deserialization

### 2. **Enhanced Logging & Monitoring**
- ✅ Comprehensive logging with multiple levels
- ✅ Session-aware log messages
- ✅ Performance monitoring and timing
- ✅ Error tracking and debugging

### 3. **Object-Oriented Programming**
- ✅ Classes, inheritance, polymorphism
- ✅ Abstract base classes (`ABC`)
- ✅ Data classes (`@dataclass`)
- ✅ Properties and descriptors

### 4. **Design Patterns**
- ✅ **Singleton Pattern** (ScoreManager)
- ✅ **Factory Pattern** (QuestionFactory)
- ✅ **Template Method** (QuestionGenerator)

### 5. **Functional Programming**
- ✅ Lambda functions
- ✅ `map()`, `filter()`, `reduce()`
- ✅ List/dict/set comprehensions
- ✅ Generator functions and expressions

### 6. **Async Programming**
- ✅ `async`/`await` syntax
- ✅ `asyncio` event loop
- ✅ Async file I/O with `aiofiles`
- ✅ Async HTTP requests with `aiohttp`

### 7. **Error Handling**
- ✅ Custom exception hierarchy
- ✅ `try`/`except`/`else`/`finally`
- ✅ Exception chaining
- ✅ Context managers for cleanup

### 8. **Decorators & Closures**
- ✅ Function decorators
- ✅ Class decorators  
- ✅ Parameterized decorators
- ✅ `functools.wraps`

### 9. **Context Managers**
- ✅ `with` statement
- ✅ `@contextmanager` decorator
- ✅ Custom context managers
- ✅ Resource management

### 10. **Type Hints**
- ✅ Static type annotations
- ✅ `typing` module usage
- ✅ Generic types

---

## 📝 Sample Game Session

```cmd
(venv) D:\brainplay-game> python main.py --player "Alice"

👤 Enter your name (or press Enter for 'Anonymous'): Alice
🧠 Welcome to BrainPlay: Win or Lose!
========================================
👤 Player: Alice
🎮 Session ID: a1b2c3d4...
🎯 Mode: NORMAL
📊 Your Stats: 5 games, 3 wins
========================================
Rules:
• +10 points for correct answers
• -5 points for wrong answers
• Reach 50 points to WIN!
• Type 'quit' anytime to exit
========================================

🎯 🔢 What is 7²? (What is 7 squared?)
💡 Hint: 7 is considered a lucky number in many cultures.
Your answer: 49
🏆 Achievement Unlocked: First Points!
✅ Correct!
Points: +10 | Total Score: 10

🎮 Continue playing? (y/n): y

🎯 🔢 What is √144? (What is the square root of 144?)
Your answer: 12
✅ Correct!
Points: +10 | Total Score: 20

🎮 Continue playing? (y/n): y

🎯 🔢 What is 9²? (What is 9 squared?)
💡 Hint: 9 is the number of squares in a tic-tac-toe grid.
Your answer: 81
🏆 Achievement Unlocked: Hot Streak!
🏆 Achievement Unlocked: Half Century!
✅ Correct!
Points: +10 | Total Score: 50

🎉 WINNER! You've reached 50 points!

🏆 WINNER! Final Score: 50
📊 Game data saved successfully!

📈 Game Statistics:
Total Rounds: 5
Correct Answers: 5
Wrong Answers: 0
Accuracy: 100.0%
Total Points Earned: 50

👤 Player Profile:
Name: Alice
Total Games: 6
Total Wins: 4
Best Score: 50
Win Rate: 66.7%
```

---

## 🔧 Troubleshooting

### Common Windows Issues

**1. Python not found**
```cmd
# Try python instead of python3
python main.py
```

**2. Virtual environment activation**
```cmd
# Make sure you're using Windows syntax
venv\Scripts\activate
```

**3. Module not found errors**
```cmd
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**4. Permission denied**
```cmd
# Run Command Prompt as Administrator
# Or use:
python -m pip install --user -r requirements.txt
```

---

## 📊 Data Files Explained

### `data/players.json`
Stores player profiles with statistics:
```json
{
  "player_id": {
    "name": "Alice",
    "total_games": 10,
    "total_wins": 7,
    "best_score": 85,
    "created_date": "2025-01-01T12:00:00",
    "last_played": "2025-01-02T15:30:00"
  }
}
```

### `data/sessions.json`
Stores session history:
```json
[
  {
    "session_id": "abc123...",
    "player_name": "Alice",
    "start_time": "2025-01-02T15:00:00",
    "end_time": "2025-01-02T15:10:00",
    "final_score": 50,
    "won": true,
    "mode": "normal"
  }
]
```

### `data/game_history.json`
Stores detailed game data with rounds:
```json
[
  {
    "session_id": "abc123...",
    "player_name": "Alice",
    "mode": "normal",
    "final_score": 50,
    "rounds": [
      {
        "round_number": 1,
        "question_type": "square",
        "question_text": "What is 7²? (What is 7 squared?)",
        "correct_answer": 49,
        "user_answer": "49",
        "is_correct": true,
        "points_earned": 10,
        "total_score": 10,
        "timestamp": "2025-01-02T15:01:00"
      }
    ]
  }
]
```

---

## 🎓 Learning Path & Extensions

### 🔰 Beginner Extensions
1. **Add new question types** (e.g., cube calculations, basic arithmetic)
2. **Implement difficulty scaling** (adaptive difficulty based on performance)
3. **Add more achievements** (streaks, speed bonuses, etc.)
4. **Create player leaderboards**

### 🔥 Intermediate Extensions  
1. **Database integration** with SQLite or PostgreSQL
2. **Web interface** using Flask or FastAPI
3. **Multiplayer support** with WebSockets
4. **Machine learning** for question difficulty optimization

### 🚀 Advanced Extensions
1. **Microservices architecture** with Docker
2. **Cloud deployment** (AWS, GCP, Azure)
3. **Real-time analytics** with Redis/Elasticsearch
4. **Mobile app** with Kivy or React Native bridge

---

## 📚 Educational Value

This project demonstrates:

- **Production-ready code structure**
- **Industry best practices**
- **Advanced Python features**
- **Real-world design patterns**
- **Professional error handling**
- **Session management**
- **Data persistence**
- **Comprehensive logging**

Perfect for:
- 🎓 **Computer Science students**
- 👨‍💻 **Junior developers** learning Python
- 🏢 **Bootcamp participants**
- 📖 **Self-taught programmers**
- 🧑‍🏫 **Instructors** teaching advanced Python

---

## 🎉 Getting Started

1. **Copy all files** to your project directory
2. **Follow the installation steps** above
3. **Run** `python main.py` to start playing
4. **Create your player profile** and start earning achievements
5. **Explore the code** to learn advanced Python concepts
6. **Check the logs** in `data/game.log` to see detailed session tracking

---

**Happy Coding! 🎉**

*Remember: The goal isn't just to build a game, but to master Python through practical, real-world application of advanced concepts with proper session management and data persistence.*