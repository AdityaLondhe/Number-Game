"""
Score Management Module
Fixed to support per-player scoring instead of global singleton.
"""

import json
import threading
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ScoreManager:
    """
    Score manager class with per-player score tracking.
    No longer uses singleton pattern to allow separate scores per player.
    """
    
    def __init__(self, player_id: str = None):
        """
        Initialize score manager for a specific player.
        
        Args:
            player_id: Unique identifier for the player
        """
        self.player_id = player_id or "default"
        self._score: int = 0
        self._round_count: int = 0
        self._correct_answers: int = 0
        self._wrong_answers: int = 0
        self._game_start_time: datetime = datetime.now()
        self._score_history: List[Dict] = []
        self._achievements: List[str] = []
        
        # File path for persistent storage (per player)
        self._score_file = Path(f"data/score_{self.player_id}.json")
        self._ensure_data_directory()
        
        # Load previous score for this player if exists
        self._load_score()
        
        logger.info(f"ScoreManager initialized for player: {self.player_id}")
    
    def _ensure_data_directory(self):
        """Ensure data directory exists."""
        self._score_file.parent.mkdir(exist_ok=True)
    
    @property
    def score(self) -> int:
        """Property decorator for score access."""
        return self._score
    
    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        total = self._correct_answers + self._wrong_answers
        if total == 0:
            return 0.0
        return (self._correct_answers / total) * 100
    
    @property
    def game_duration(self) -> str:
        """Get formatted game duration."""
        duration = datetime.now() - self._game_start_time
        minutes, seconds = divmod(int(duration.total_seconds()), 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def add_points(self, points: int) -> None:
        """
        Add points to the score with validation and logging.
        """
        if not isinstance(points, int):
            raise TypeError("Points must be an integer")
        
        old_score = self._score
        self._score += points
        self._round_count += 1
        
        # Track correct/wrong answers
        if points > 0:
            self._correct_answers += 1
        else:
            self._wrong_answers += 1
        
        # Record score change in history
        score_change = {
            'round': self._round_count,
            'points_added': points,
            'old_score': old_score,
            'new_score': self._score,
            'timestamp': datetime.now().isoformat()
        }
        self._score_history.append(score_change)
        
        # Check for achievements
        self._check_achievements()
        
        # Auto-save score
        self._save_score()
        
        logger.info(f"Score updated for {self.player_id}: {old_score} -> {self._score} ({points:+d})")
    
    def get_score(self) -> int:
        """Get current score."""
        return self._score
    
    def reset_score(self) -> None:
        """
        Reset score and statistics for new game.
        """
        logger.info(f"Resetting score for {self.player_id} from {self._score}")
        
        self._score = 0
        self._round_count = 0
        self._correct_answers = 0
        self._wrong_answers = 0
        self._game_start_time = datetime.now()
        self._score_history.clear()
        self._achievements.clear()
        
        self._save_score()
    
    def get_statistics(self) -> Dict:
        """Get comprehensive game statistics."""
        return {
            'player_id': self.player_id,
            'current_score': self._score,
            'rounds_played': self._round_count,
            'correct_answers': self._correct_answers,
            'wrong_answers': self._wrong_answers,
            'accuracy': round(self.accuracy, 2),
            'game_duration': self.game_duration,
            'achievements': self._achievements.copy(),
            'score_progression': [
                {
                    'round': entry['round'],
                    'score': entry['new_score']
                }
                for entry in self._score_history
            ],
            'average_points_per_round': (
                sum(entry['points_added'] for entry in self._score_history) / len(self._score_history)
                if self._score_history else 0
            )
        }
    
    def _check_achievements(self) -> None:
        """Check and award achievements based on current statistics."""
        new_achievements = []
        
        # Score-based achievements
        if self._score >= 10 and "First Points" not in self._achievements:
            new_achievements.append("First Points")
        
        if self._score >= 50 and "Half Century" not in self._achievements:
            new_achievements.append("Half Century")
        
        if self._score >= 100 and "Century" not in self._achievements:
            new_achievements.append("Century")
        
        # Accuracy-based achievements
        if self._round_count >= 5 and self.accuracy == 100 and "Perfect Start" not in self._achievements:
            new_achievements.append("Perfect Start")
        
        if self._round_count >= 10 and self.accuracy >= 90 and "Sharp Shooter" not in self._achievements:
            new_achievements.append("Sharp Shooter")
        
        # Streak-based achievements (check last 5 answers)
        if len(self._score_history) >= 5:
            last_five = self._score_history[-5:]
            if all(entry['points_added'] > 0 for entry in last_five) and "Hot Streak" not in self._achievements:
                new_achievements.append("Hot Streak")
        
        # Add new achievements
        for achievement in new_achievements:
            self._achievements.append(achievement)
            logger.info(f"Achievement unlocked for {self.player_id}: {achievement}")
            print(f"🏆 Achievement Unlocked: {achievement}!")
    
    def _save_score(self) -> None:
        """Save current score and statistics to file."""
        try:
            score_data = {
                'player_id': self.player_id,
                'score': self._score,
                'round_count': self._round_count,
                'correct_answers': self._correct_answers,
                'wrong_answers': self._wrong_answers,
                'game_start_time': self._game_start_time.isoformat(),
                'score_history': self._score_history,
                'achievements': self._achievements,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self._score_file, 'w') as f:
                json.dump(score_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save score for {self.player_id}: {e}")
    
    def _load_score(self) -> None:
        """Load score and statistics from file."""
        try:
            if self._score_file.exists():
                with open(self._score_file, 'r') as f:
                    score_data = json.load(f)
                
                # Only load if it's for the same player
                if score_data.get('player_id') == self.player_id:
                    self._score = score_data.get('score', 0)
                    self._round_count = score_data.get('round_count', 0)
                    self._correct_answers = score_data.get('correct_answers', 0)
                    self._wrong_answers = score_data.get('wrong_answers', 0)
                    self._score_history = score_data.get('score_history', [])
                    self._achievements = score_data.get('achievements', [])
                    
                    # Parse game start time
                    start_time_str = score_data.get('game_start_time')
                    if start_time_str:
                        self._game_start_time = datetime.fromisoformat(start_time_str)
                    
                    logger.info(f"Loaded previous score for {self.player_id}: {self._score}")
                else:
                    logger.info(f"No previous score found for {self.player_id}")
                
        except Exception as e:
            logger.warning(f"Failed to load previous score for {self.player_id}: {e}")
            # Continue with default values


# Example usage and testing
if __name__ == "__main__":
    """
    Module testing and demonstration.
    Shows per-player score management.
    """
    
    print("Testing Per-Player Score Management...")
    
    # Test different players
    alice_score = ScoreManager("alice")
    bob_score = ScoreManager("bob")
    
    print(f"Alice initial score: {alice_score.get_score()}")
    print(f"Bob initial score: {bob_score.get_score()}")
    
    # Add points to Alice
    alice_score.add_points(10)
    print(f"Alice after +10: {alice_score.get_score()}")
    print(f"Bob after Alice +10: {bob_score.get_score()}")  # Should remain unchanged
    
    # Add points to Bob
    bob_score.add_points(20)
    print(f"Alice after Bob +20: {alice_score.get_score()}")  # Should remain unchanged
    print(f"Bob after +20: {bob_score.get_score()}")
    
    print("Per-player score management test completed!")