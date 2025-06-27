"""
Question Factory Module
Demonstrates Factory Design Pattern, Abstract Base Classes, and Random Generation.
Fixed to only include square calculation and square root questions as per game rules.
"""

import random
import math
import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import Union, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class QuestionResult:
    """
    Data class to represent a question and its answer.
    Demonstrates dataclasses and type hints.
    """
    text: str
    answer: Union[int, float, str]
    question_type: str
    difficulty: str
    
    def check_answer(self, user_answer: str) -> bool:
        """
        Check if user answer is correct.
        Handles different answer types and formats.
        """
        try:
            # Handle numeric answers
            if isinstance(self.answer, (int, float)):
                user_numeric = float(user_answer)
                # Allow small floating point errors
                return abs(user_numeric - float(self.answer)) < 0.01
            
            # Handle string answers (case insensitive)
            return str(self.answer).lower() == user_answer.lower().strip()
            
        except ValueError:
            return False


class QuestionGenerator(ABC):
    """
    Abstract base class for question generators.
    Demonstrates Abstract Base Classes and Template Method pattern.
    """
    
    def __init__(self, difficulty: str = "normal"):
        self.difficulty = difficulty
        self.difficulty_multiplier = {
            "easy": 0.5,
            "normal": 1.0,
            "hard": 1.5
        }.get(difficulty, 1.0)
    
    @abstractmethod
    async def generate(self) -> QuestionResult:
        """Generate a question. Must be implemented by subclasses."""
        pass
    
    def _adjust_for_difficulty(self, base_range: tuple) -> tuple:
        """Adjust number ranges based on difficulty."""
        min_val, max_val = base_range
        if self.difficulty == "easy":
            return (min_val, min(max_val, int(max_val * 0.6)))
        elif self.difficulty == "hard":
            return (min_val, int(max_val * 1.5))
        return base_range


class SquareGenerator(QuestionGenerator):
    """
    Generates square calculation questions.
    Asks "What is X²?" where player calculates the square of a number.
    """
    
    async def generate(self) -> QuestionResult:
        """Generate a square calculation question."""
        # Adjust range based on difficulty
        min_val, max_val = self._adjust_for_difficulty((1, 20))
        
        # Generate a random number to square
        base_number = random.randint(min_val, max_val)
        square_result = base_number ** 2
        
        # Try to get a fun fact about the base number
        fun_fact = await self._get_number_fact(base_number)
        
        question_text = f"🔢 What is {base_number}²? (What is {base_number} squared?)"
        if fun_fact:
            question_text += f"\n💡 Hint: {fun_fact}"
        
        logger.debug(f"Generated square question: {base_number}² = {square_result}")
        
        return QuestionResult(
            text=question_text,
            answer=square_result,
            question_type="square",
            difficulty=self.difficulty
        )
    
    async def _get_number_fact(self, number: int) -> Optional[str]:
        """
        Get a fun fact about a number from numbersapi.com
        Demonstrates async HTTP requests and error handling.
        """
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2)) as session:
                async with session.get(f"http://numbersapi.com/{number}/trivia") as response:
                    if response.status == 200:
                        fact = await response.text()
                        # Limit fact length for better UX
                        return fact[:100] + "..." if len(fact) > 100 else fact
        except Exception as e:
            logger.debug(f"Failed to get number fact for {number}: {e}")
        
        return None


class SquareRootGenerator(QuestionGenerator):
    """
    Generates square root questions.
    Asks "What is √X?" where player finds the square root of a perfect square.
    """
    
    def __init__(self, difficulty: str = "normal"):
        super().__init__(difficulty)
        # Generate perfect squares for different difficulties
        self.perfect_squares = self._generate_perfect_squares()
    
    def _generate_perfect_squares(self) -> list:
        """
        Generate perfect squares based on difficulty.
        Demonstrates list comprehensions and mathematical operations.
        """
        if self.difficulty == "easy":
            # Perfect squares from 1 to 100 (1² to 10²)
            return [i**2 for i in range(1, 11)]
        elif self.difficulty == "hard":
            # Perfect squares from 1 to 10000 (1² to 100²)
            return [i**2 for i in range(1, 101)]
        else:
            # Normal: Perfect squares from 1 to 2500 (1² to 50²)
            return [i**2 for i in range(1, 51)]
    
    async def generate(self) -> QuestionResult:
        """Generate a square root question."""
        # Select a random perfect square
        perfect_square = random.choice(self.perfect_squares)
        square_root = int(math.sqrt(perfect_square))
        
        question_text = f"🔢 What is √{perfect_square}? (What is the square root of {perfect_square}?)"
        
        logger.debug(f"Generated square root question: √{perfect_square} = {square_root}")
        
        return QuestionResult(
            text=question_text,
            answer=square_root,
            question_type="square_root",
            difficulty=self.difficulty
        )


class QuestionFactory:
    """
    Factory class to create different types of questions.
    FIXED: Only includes square calculation and square root questions as per game rules.
    """
    
    def __init__(self):
        # FIXED: Only the two required question types
        self.generators = {
            'square': SquareGenerator,           # Square calculation (X²)
            'square_root': SquareRootGenerator,  # Square root calculation (√X)
        }
        
        # FIXED: Equal weight for both question types (50/50 split)
        self.question_weights = {
            'square': 0.5,           # 50% - Square calculation (X²)
            'square_root': 0.5,      # 50% - Square root calculation (√X)
        }
    
    async def create_question(self, difficulty: str = "normal") -> QuestionResult:
        """
        Create a random question using weighted selection.
        Now only creates square and square root questions.
        """
        # Use weighted random selection
        question_types = list(self.question_weights.keys())
        weights = list(self.question_weights.values())
        
        # Python 3.6+ random.choices for weighted selection
        selected_type = random.choices(question_types, weights=weights)[0]
        
        # Create generator instance
        generator = self.generators[selected_type](difficulty)
        
        # Generate and return question
        question = await generator.generate()
        
        logger.info(f"Generated {selected_type} question in {difficulty} mode")
        return question
    
    def get_available_types(self) -> list:
        """Get list of available question types."""
        return list(self.generators.keys())
    
    async def create_specific_question(self, question_type: str, difficulty: str = "normal") -> QuestionResult:
        """
        Create a specific type of question.
        Useful for testing or specific game modes.
        """
        if question_type not in self.generators:
            raise ValueError(f"Unknown question type: {question_type}. Available types: {list(self.generators.keys())}")
        
        generator = self.generators[question_type](difficulty)
        return await generator.generate()


# Example usage and testing
if __name__ == "__main__":
    """
    Module testing and demonstration.
    Shows how to test the question factory with ONLY the correct question types.
    """
    async def test_factory():
        factory = QuestionFactory()
        
        print("Testing Question Factory - ONLY Square and Square Root Questions")
        print("=" * 70)
        
        print(f"Available question types: {factory.get_available_types()}")
        print(f"Question weights: {factory.question_weights}")
        print()
        
        # Test different difficulties
        for difficulty in ['easy', 'normal', 'hard']:
            print(f"--- {difficulty.upper()} MODE ---")
            
            for i in range(3):
                question = await factory.create_question(difficulty)
                print(f"Q{i+1}: {question.text}")
                print(f"Answer: {question.answer}")
                print(f"Type: {question.question_type}")
                print()
        
        # Test specific question types
        print("--- SPECIFIC QUESTION TYPES ---")
        for qtype in factory.get_available_types():
            question = await factory.create_specific_question(qtype, "normal")
            print(f"{qtype.upper()}: {question.text}")
            print(f"Answer: {question.answer}")
            print()
        
        # Demonstrate the correct question types
        print("--- CORRECT QUESTION TYPE EXAMPLES ---")
        
        # Square calculation
        square_gen = SquareGenerator("normal")
        square_q = await square_gen.generate()
        print(f"SQUARE CALCULATION: {square_q.text}")
        print(f"Answer: {square_q.answer}")
        print()
        
        # Square root calculation
        sqrt_gen = SquareRootGenerator("normal")
        sqrt_q = await sqrt_gen.generate()
        print(f"SQUARE ROOT: {sqrt_q.text}")
        print(f"Answer: {sqrt_q.answer}")
        print()
        
        # Test question distribution
        print("--- QUESTION DISTRIBUTION TEST ---")
        question_counts = {'square': 0, 'square_root': 0}
        
        for _ in range(20):
            question = await factory.create_question("normal")
            question_counts[question.question_type] += 1
        
        print(f"Generated 20 questions:")
        print(f"Square questions: {question_counts['square']}")
        print(f"Square root questions: {question_counts['square_root']}")
        print(f"Distribution: {question_counts['square']/20*100:.1f}% square, {question_counts['square_root']/20*100:.1f}% square root")
    
    # Run tests if module is executed directly
    asyncio.run(test_factory())