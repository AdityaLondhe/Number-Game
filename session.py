"""
Session Management Module
Demonstrates session tracking, player profiles, and data persistence.
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class PlayerProfile:
    """
    Player profile data class.
    Demonstrates dataclasses and player tracking.
    """
    name: str
    player_id: str
    total_games: int = 0
    total_wins: int = 0
    best_score: int = 0
    created_date: str = None
    last_played: datetime = None
    
    def __post_init__(self):
        """Initialize default values after creation."""
        if self.created_date is None:
            self.created_date = datetime.now().isoformat()
        if self.last_played is None:
            self.last_played = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert datetime to string for JSON serialization
        if isinstance(data['last_played'], datetime):
            data['last_played'] = data['last_played'].isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerProfile':
        """Create PlayerProfile from dictionary."""
        # Convert string back to datetime
        if 'last_played' in data and isinstance(data['last_played'], str):
            data['last_played'] = datetime.fromisoformat(data['last_played'])
        return cls(**data)


@dataclass
class GameSession:
    """
    Game session data class.
    Demonstrates session tracking and timing.
    """
    session_id: str
    player_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    final_score: Optional[int] = None
    won: Optional[bool] = None
    mode: str = "normal"
    
    def get_duration(self) -> Optional[timedelta]:
        """Get session duration."""
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert datetime objects to strings
        data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GameSession':
        """Create GameSession from dictionary."""
        # Convert strings back to datetime
        data['start_time'] = datetime.fromisoformat(data['start_time'])
        if data.get('end_time'):
            data['end_time'] = datetime.fromisoformat(data['end_time'])
        return cls(**data)


class SessionManager:
    """
    Manages game sessions and player profiles.
    Demonstrates singleton-like behavior and data persistence.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.players_file = self.data_dir / "players.json"
        self.sessions_file = self.data_dir / "sessions.json"
        
        self.active_sessions: Dict[str, GameSession] = {}
        self.players: Dict[str, PlayerProfile] = {}
        
        # Load existing data
        self._load_players()
        self._load_sessions()
        
        logger.info(f"SessionManager initialized - {len(self.players)} players loaded")
    
    def get_or_create_player(self, name: str) -> PlayerProfile:
        """Get existing player or create new one."""
        # Look for existing player by name
        for player in self.players.values():
            if player.name.lower() == name.lower():
                logger.info(f"Found existing player: {player.name}")
                return player
        
        # Create new player
        player_id = str(uuid.uuid4())
        player = PlayerProfile(
            name=name,
            player_id=player_id
        )
        
        self.players[player_id] = player
        self.save_player_profile(player)
        
        logger.info(f"Created new player: {player.name} (ID: {player_id})")
        return player
    
    def start_session(self, session_id: str, player_name: str, mode: str = "normal") -> GameSession:
        """Start a new game session."""
        session = GameSession(
            session_id=session_id,
            player_name=player_name,
            start_time=datetime.now(),
            mode=mode
        )
        
        self.active_sessions[session_id] = session
        logger.info(f"Started session {session_id} for player {player_name}")
        
        return session
    
    def end_session(self, session_id: str, final_score: int, won: bool) -> Optional[GameSession]:
        """End a game session."""
        if session_id not in self.active_sessions:
            logger.warning(f"Attempted to end non-existent session: {session_id}")
            return None
        
        session = self.active_sessions[session_id]
        session.end_time = datetime.now()
        session.final_score = final_score
        session.won = won
        
        # Save session data
        self._save_session(session)
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        duration = session.get_duration()
        logger.info(f"Ended session {session_id} - Score: {final_score}, Won: {won}, Duration: {duration}")
        
        return session
    
    def get_session_duration(self, session_id: str) -> Optional[str]:
        """Get formatted session duration."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            duration = datetime.now() - session.start_time
            minutes, seconds = divmod(int(duration.total_seconds()), 60)
            return f"{minutes:02d}:{seconds:02d}"
        return None
    
    def save_player_profile(self, player: PlayerProfile):
        """Save player profile to file."""
        try:
            self.players[player.player_id] = player
            self._save_players()
            logger.debug(f"Saved player profile: {player.name}")
        except Exception as e:
            logger.error(f"Failed to save player profile {player.name}: {e}")
    
    def get_all_players(self) -> List[PlayerProfile]:
        """Get all player profiles."""
        return list(self.players.values())
    
    def get_player_stats(self, player_name: str) -> Optional[PlayerProfile]:
        """Get statistics for a specific player."""
        for player in self.players.values():
            if player.name.lower() == player_name.lower():
                return player
        return None
    
    def _load_players(self):
        """Load player profiles from file."""
        try:
            if self.players_file.exists():
                with open(self.players_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for player_id, player_data in data.items():
                    self.players[player_id] = PlayerProfile.from_dict(player_data)
                
                logger.debug(f"Loaded {len(self.players)} player profiles")
        except Exception as e:
            logger.error(f"Failed to load player profiles: {e}")
    
    def _save_players(self):
        """Save player profiles to file."""
        try:
            data = {
                player_id: player.to_dict() 
                for player_id, player in self.players.items()
            }
            
            with open(self.players_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Saved {len(self.players)} player profiles")
        except Exception as e:
            logger.error(f"Failed to save player profiles: {e}")
    
    def _load_sessions(self):
        """Load session history from file."""
        try:
            if self.sessions_file.exists():
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load recent sessions (last 100)
                sessions = [GameSession.from_dict(session_data) for session_data in data[-100:]]
                logger.debug(f"Loaded {len(sessions)} session records")
        except Exception as e:
            logger.error(f"Failed to load session history: {e}")
    
    def _save_session(self, session: GameSession):
        """Save individual session to history."""
        try:
            # Load existing sessions
            sessions = []
            if self.sessions_file.exists():
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    sessions = json.load(f)
            
            # Add new session
            sessions.append(session.to_dict())
            
            # Keep only last 1000 sessions
            if len(sessions) > 1000:
                sessions = sessions[-1000:]
            
            # Save back to file
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(sessions, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Saved session {session.session_id}")
        except Exception as e:
            logger.error(f"Failed to save session {session.session_id}: {e}")
    
    def get_session_statistics(self) -> dict:
        """Get overall session statistics."""
        try:
            if not self.sessions_file.exists():
                return {}
            
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                sessions_data = json.load(f)
            
            total_sessions = len(sessions_data)
            won_sessions = sum(1 for s in sessions_data if s.get('won', False))
            
            # Calculate average scores
            scores = [s.get('final_score', 0) for s in sessions_data if s.get('final_score') is not None]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            return {
                'total_sessions': total_sessions,
                'won_sessions': won_sessions,
                'win_rate': (won_sessions / total_sessions * 100) if total_sessions > 0 else 0,
                'average_score': avg_score,
                'total_players': len(self.players)
            }
        except Exception as e:
            logger.error(f"Failed to calculate session statistics: {e}")
            return {}


# Example usage and testing
if __name__ == "__main__":
    """
    Module testing and demonstration.
    Shows session management functionality.
    """
    
    print("Testing Session Management...")
    
    # Create session manager
    session_manager = SessionManager()
    
    # Create test player
    player = session_manager.get_or_create_player("Test Player")
    print(f"Player created: {player.name} (ID: {player.player_id})")
    
    # Start test session
    session_id = str(uuid.uuid4())
    session = session_manager.start_session(session_id, player.name)
    print(f"Session started: {session_id}")
    
    # Simulate some time passing
    import time
    time.sleep(1)
    
    # End session
    final_session = session_manager.end_session(session_id, 42, True)
    print(f"Session ended: Duration = {final_session.get_duration()}")
    
    # Update player stats
    player.total_games += 1
    player.total_wins += 1
    player.best_score = 42
    session_manager.save_player_profile(player)
    
    # Show statistics
    stats = session_manager.get_session_statistics()
    print(f"Session statistics: {stats}")
    
    print("Session management test completed!")