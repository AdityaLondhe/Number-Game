#!/usr/bin/env python3
"""
BrainPlay: Win or Lose - Main Entry Point
Enhanced with score reset option after game completion.

Author: Mr Hafeez
Version: 2.2.1
"""

import argparse
import asyncio
import logging
import sys
import uuid
from typing import Optional
from datetime import datetime

from questions import QuestionFactory
from score import ScoreManager
from session import SessionManager, PlayerProfile
from exceptions import GameExitException, InvalidInputException
from utils.decorators import timer, log_calls
from utils.context import game_session
from utils.file_io import save_game_history


# Configure comprehensive logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/game.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class BrainPlayGame:
    """
    Main game class with per-player score management and session tracking.
    Enhanced with score reset functionality.
    """
    
    def __init__(self, mode: str = "normal", player_name: str = None):
        self.mode = mode
        self.session_manager = SessionManager()
        self.question_factory = QuestionFactory()
        self.game_history = []
        self.session_id = str(uuid.uuid4())
        
        # Create or load player profile
        self.player = self._setup_player(player_name)
        
        # Create score manager for this specific player
        self.score_manager = ScoreManager(self.player.player_id)
        
        # Reset score for new game session
        self.score_manager.reset_score()
        
        logger.info(f"Game initialized - Session: {self.session_id}, Player: {self.player.name}, Mode: {mode}")
    
    def _setup_player(self, player_name: str = None) -> PlayerProfile:
        """Setup player profile with session tracking."""
        if not player_name:
            player_name = input("👤 Enter your name (or press Enter for 'Anonymous'): ").strip()
            if not player_name:
                player_name = "Anonymous"
        
        player = self.session_manager.get_or_create_player(player_name)
        logger.info(f"Player setup complete - Name: {player.name}, Total Games: {player.total_games}")
        return player
    
    @timer
    async def play_round(self) -> bool:
        """
        Play a single round with comprehensive logging.
        """
        try:
            with game_session(f"round-{len(self.game_history) + 1}") as session:
                # Generate question using factory pattern
                question = await self.question_factory.create_question(self.mode)
                
                logger.info(f"Question generated - Type: {question.question_type}, Difficulty: {question.difficulty}")
                
                print(f"\n🎯 {question.text}")
                
                # Get user input with validation
                user_answer = self._get_user_input()
                
                # Check answer and update score
                is_correct = question.check_answer(user_answer)
                points = 10 if is_correct else -5
                
                self.score_manager.add_points(points)
                
                # Log the round result with detailed information
                round_data = {
                    'session_id': self.session_id,
                    'player_name': self.player.name,
                    'player_id': self.player.player_id,
                    'round_number': len(self.game_history) + 1,
                    'question_type': question.question_type,
                    'question_text': question.text,
                    'correct_answer': question.answer,
                    'user_answer': user_answer,
                    'is_correct': is_correct,
                    'points_earned': points,
                    'total_score': self.score_manager.get_score(),
                    'timestamp': datetime.now().isoformat(),
                    'difficulty': question.difficulty
                }
                self.game_history.append(round_data)
                
                # Log round completion
                logger.info(f"Round completed - Player: {self.player.name}, "
                          f"Question: {question.question_type}, "
                          f"Correct: {is_correct}, "
                          f"Points: {points:+d}, "
                          f"Total Score: {self.score_manager.get_score()}")
                
                # Display result with emojis
                result_emoji = "✅" if is_correct else "❌"
                print(f"{result_emoji} {'Correct!' if is_correct else f'Wrong! Answer was {question.answer}'}")
                print(f"Points: {points:+d} | Total Score: {self.score_manager.get_score()}")
                
                # Check win condition
                if self.score_manager.get_score() >= 50:
                    print("\n🎉 WINNER! You've reached 50 points!")
                    logger.info(f"WINNER - Player: {self.player.name}, Final Score: {self.score_manager.get_score()}")
                    return False
                
                # Ask if player wants to continue
                return self._ask_continue()
                
        except InvalidInputException as e:
            logger.warning(f"Invalid input from player {self.player.name}: {e}")
            print(f"⚠️ {e}")
            return True
        except GameExitException:
            logger.info(f"Player {self.player.name} chose to exit game")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in round for player {self.player.name}: {e}")
            print(f"💥 An unexpected error occurred: {e}")
            return False
    
    def _get_user_input(self) -> str:
        """Get and validate user input with logging."""
        try:
            answer = input("Your answer: ").strip()
            if not answer:
                raise InvalidInputException("Answer cannot be empty")
            
            # Check for quit commands
            if answer.lower() in ['quit', 'exit', 'q']:
                logger.info(f"Player {self.player.name} entered quit command: {answer}")
                raise GameExitException("Player chose to quit via command")
            
            logger.debug(f"Player {self.player.name} entered answer: {answer}")
            return answer
        except KeyboardInterrupt:
            logger.info(f"Player {self.player.name} interrupted game with Ctrl+C")
            raise GameExitException("Game interrupted by user")
    
    def _ask_continue(self) -> bool:
        """Ask if player wants to continue with logging."""
        try:
            choice = input("\n🎮 Continue playing? (y/n): ").strip().lower()
            logger.debug(f"Player {self.player.name} continue choice: {choice}")
            
            if choice in ['n', 'no', 'quit', 'exit']:
                logger.info(f"Player {self.player.name} chose not to continue")
                raise GameExitException("Player chose to quit")
            return choice in ['y', 'yes', '']
        except KeyboardInterrupt:
            logger.info(f"Player {self.player.name} interrupted continue prompt")
            raise GameExitException("Game interrupted by user")
    
    def _ask_score_reset(self) -> bool:
        """Ask if player wants to reset their score after game ends."""
        try:
            print("\n" + "="*50)
            print("🔄 SCORE MANAGEMENT")
            print("="*50)
            print(f"Your current saved score: {self.score_manager.get_score()}")
            print("This score will be loaded when you start your next game.")
            print()
            print("Would you like to reset your score to 0 for future games?")
            print("This will clear your current progress but keep your player statistics.")
            print()
            
            while True:
                choice = input("🔄 Reset score to 0? (y/n): ").strip().lower()
                
                if choice in ['y', 'yes']:
                    logger.info(f"Player {self.player.name} chose to reset score")
                    return True
                elif choice in ['n', 'no']:
                    logger.info(f"Player {self.player.name} chose to keep score")
                    return False
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
                    
        except KeyboardInterrupt:
            logger.info(f"Player {self.player.name} interrupted score reset prompt")
            print("\nScore reset cancelled.")
            return False
    
    async def start_game(self):
        """Main game loop with session management."""
        # Start session
        self.session_manager.start_session(self.session_id, self.player.name)
        
        print("🧠 Welcome to BrainPlay: Win or Lose!")
        print("=" * 40)
        print(f"👤 Player: {self.player.name}")
        print(f"🎮 Session ID: {self.session_id[:8]}...")
        print(f"🎯 Mode: {self.mode.upper()}")
        print(f"📊 Your Stats: {self.player.total_games} games, {self.player.total_wins} wins")
        print(f"🎯 Starting Score: {self.score_manager.get_score()}")  # Show starting score
        print("=" * 40)
        print("Rules:")
        print("• +10 points for correct answers")
        print("• -5 points for wrong answers")
        print("• Reach 50 points to WIN!")
        print("• Type 'quit' anytime to exit")
        print("=" * 40)
        
        logger.info(f"Game started - Player: {self.player.name}, Session: {self.session_id}, Mode: {self.mode}")
        
        try:
            while True:
                continue_game = await self.play_round()
                if not continue_game:
                    break
                    
                # Small delay for better UX
                await asyncio.sleep(0.5)
            
            # Game ended - determine outcome
            await self._end_game(won=True)
            
        except GameExitException:
            print("\n👋 LOOSER! Thanks for playing!")
            await self._end_game(won=False)
        except Exception as e:
            logger.error(f"Game crashed for player {self.player.name}: {e}")
            print(f"💥 Game crashed: {e}")
            await self._end_game(won=False)
    
    async def _end_game(self, won: bool):
        """Handle game ending with comprehensive logging and session management."""
        final_score = self.score_manager.get_score()
        
        # Update player profile
        self.player.total_games += 1
        if won:
            self.player.total_wins += 1
        self.player.best_score = max(self.player.best_score, final_score)
        self.player.last_played = datetime.now()
        
        # End session
        self.session_manager.end_session(self.session_id, final_score, won)
        
        # Display final result
        if won:
            print(f"\n🏆 WINNER! Final Score: {final_score}")
            logger.info(f"GAME WON - Player: {self.player.name}, Score: {final_score}, Session: {self.session_id}")
        else:
            print(f"\n😔 LOOSER! Final Score: {final_score}")
            logger.info(f"GAME LOST - Player: {self.player.name}, Score: {final_score}, Session: {self.session_id}")
        
        # Save all data
        await self._save_game_data()
        self._show_statistics()
        
        # Save updated player profile
        self.session_manager.save_player_profile(self.player)
        
        # NEW: Ask if player wants to reset their score
        if self._ask_score_reset():
            try:
                # Reset the score to 0
                old_score = self.score_manager.get_score()
                self.score_manager.reset_score()
                
                print(f"\n✅ Score reset successfully!")
                print(f"Previous score: {old_score} -> New score: {self.score_manager.get_score()}")
                print("Your next game will start with a fresh score of 0.")
                
                # Use ASCII arrow instead of Unicode to avoid encoding issues
                logger.info(f"Score reset for player {self.player.name}: {old_score} -> 0")
                
            except Exception as e:
                logger.error(f"Failed to reset score for player {self.player.name}: {e}")
                print(f"❌ Failed to reset score: {e}")
        else:
            print(f"\n📊 Score kept at {final_score} for your next game.")
    
    async def _save_game_data(self):
        """Save comprehensive game data."""
        try:
            # Prepare comprehensive game data
            game_data = {
                'session_id': self.session_id,
                'player_name': self.player.name,
                'player_id': self.player.player_id,
                'mode': self.mode,
                'final_score': self.score_manager.get_score(),
                'rounds': self.game_history,
                'session_duration': self.session_manager.get_session_duration(self.session_id),
                'timestamp': datetime.now().isoformat()
            }
            
            await save_game_history([game_data], self.score_manager.get_score())
            print("📊 Game data saved successfully!")
            logger.info(f"Game data saved - Player: {self.player.name}, Session: {self.session_id}")
        except Exception as e:
            logger.error(f"Failed to save game data for player {self.player.name}: {e}")
            print("⚠️ Failed to save game data")
    
    def _show_statistics(self):
        """Display comprehensive game statistics."""
        if not self.game_history:
            return
        
        # Calculate statistics using functional programming
        correct_answers = list(filter(lambda r: r['is_correct'], self.game_history))
        wrong_answers = list(filter(lambda r: not r['is_correct'], self.game_history))
        
        # Use map and reduce for calculations
        from functools import reduce
        total_points = reduce(lambda acc, r: acc + r['points_earned'], self.game_history, 0)
        
        print("\n📈 Game Statistics:")
        print(f"Total Rounds: {len(self.game_history)}")
        print(f"Correct Answers: {len(correct_answers)}")
        print(f"Wrong Answers: {len(wrong_answers)}")
        print(f"Accuracy: {len(correct_answers)/len(self.game_history)*100:.1f}%")
        print(f"Total Points Earned: {total_points}")
        
        print(f"\n👤 Player Profile:")
        print(f"Name: {self.player.name}")
        print(f"Total Games: {self.player.total_games}")
        print(f"Total Wins: {self.player.total_wins}")
        print(f"Best Score: {self.player.best_score}")
        print(f"Win Rate: {(self.player.total_wins/max(self.player.total_games, 1)*100):.1f}%")


def setup_cli() -> argparse.ArgumentParser:
    """Setup command line interface with enhanced options."""
    parser = argparse.ArgumentParser(
        description="BrainPlay: Win or Lose - A CLI brain training game with per-player scoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Normal mode
  python main.py --mode easy               # Easy mode
  python main.py --mode hard               # Hard mode
  python main.py --player "John Doe"       # Specify player name
  python main.py --history                 # Show game history
  python main.py --stats                   # Show player statistics
        """
    )
    
    parser.add_argument(
        '--mode', '-m',
        choices=['easy', 'normal', 'hard'],
        default='normal',
        help='Game difficulty mode (default: normal)'
    )
    
    parser.add_argument(
        '--player', '-p',
        type=str,
        help='Player name for session tracking'
    )
    
    parser.add_argument(
        '--history',
        action='store_true',
        help='Show game history and exit'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show player statistics and exit'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='BrainPlay 2.2.1'
    )
    
    return parser


async def show_history():
    """Show comprehensive game history."""
    try:
        from utils.file_io import load_game_history
        history = await load_game_history()
        
        if not history:
            print("📝 No game history found.")
            return
        
        print("📚 Game History:")
        print("=" * 60)
        
        for i, game in enumerate(history[-10:], 1):  # Show last 10 games
            if isinstance(game, dict) and 'session_id' in game:
                # New format with session data
                print(f"Game {i}:")
                print(f"  Player: {game.get('player_name', 'Unknown')}")
                print(f"  Score: {game.get('final_score', 0)}")
                print(f"  Mode: {game.get('mode', 'normal')}")
                print(f"  Rounds: {len(game.get('rounds', []))}")
                print(f"  Date: {game.get('timestamp', 'Unknown')}")
                print(f"  Session: {game.get('session_id', 'Unknown')[:8]}...")
            else:
                # Legacy format
                print(f"Game {i}: Score {game.get('final_score', 0)} - {game.get('timestamp', 'Unknown')}")
            print()
            
    except Exception as e:
        logger.error(f"Failed to load history: {e}")
        print("⚠️ Failed to load game history")


async def show_stats():
    """Show player statistics."""
    try:
        session_manager = SessionManager()
        players = session_manager.get_all_players()
        
        if not players:
            print("📊 No player statistics found.")
            return
        
        print("📊 Player Statistics:")
        print("=" * 60)
        
        for player in players:
            print(f"👤 {player.name}")
            print(f"   Games Played: {player.total_games}")
            print(f"   Games Won: {player.total_wins}")
            print(f"   Best Score: {player.best_score}")
            print(f"   Win Rate: {(player.total_wins/max(player.total_games, 1)*100):.1f}%")
            print(f"   Last Played: {player.last_played}")
            print()
            
    except Exception as e:
        logger.error(f"Failed to load statistics: {e}")
        print("⚠️ Failed to load player statistics")


async def main():
    """Main entry point with enhanced session management."""
    parser = setup_cli()
    args = parser.parse_args()
    
    # Handle special commands
    if args.history:
        await show_history()
        return
    
    if args.stats:
        await show_stats()
        return
    
    # Start the game with per-player score management
    game = BrainPlayGame(mode=args.mode, player_name=args.player)
    await game.start_game()


if __name__ == "__main__":
    """Entry point with proper error handling and cleanup."""
    try:
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Game interrupted. Goodbye!")
        logger.info("Game interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        print(f"💥 Critical error: {e}")
        sys.exit(1)
