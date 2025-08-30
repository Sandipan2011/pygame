#!/usr/bin/env python3
"""
Test script to verify difficulty settings are working correctly.
"""

import sys
import os

# Add the game/python directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game/python'))

from config import Difficulty, DIFFICULTY_SETTINGS


def test_difficulty_settings():
    """Test that difficulty settings are properly configured."""
    print("Testing difficulty settings...")
    
    # Get all difficulty levels
    difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
    
    # Test each difficulty level
    for difficulty in difficulties:
        settings = DIFFICULTY_SETTINGS[difficulty]
        print(f"\nDifficulty {difficulty}:")
        print(f"  Name: {settings['name']}")
        print(f"  Obstacle Frequency: {settings['obstacle_frequency']}")
        print(f"  Obstacle Speed: {settings['obstacle_speed']}")
        
        # Verify settings are valid
        assert isinstance(settings['name'], str), "Name should be a string"
        assert isinstance(settings['obstacle_frequency'], int), (
            "Frequency should be integer"
        )
        assert isinstance(settings['obstacle_speed'], int), (
            "Speed should be integer"
        )
        assert settings['obstacle_frequency'] > 0, "Frequency should be positive"
        assert settings['obstacle_speed'] > 0, "Speed should be positive"
    
    print("\n✅ All difficulty settings are valid!")
    
    # Verify difficulty progression
    easy_freq = DIFFICULTY_SETTINGS[Difficulty.EASY]['obstacle_frequency']
    medium_freq = DIFFICULTY_SETTINGS[Difficulty.MEDIUM]['obstacle_frequency']
    hard_freq = DIFFICULTY_SETTINGS[Difficulty.HARD]['obstacle_frequency']
    
    easy_speed = DIFFICULTY_SETTINGS[Difficulty.EASY]['obstacle_speed']
    medium_speed = DIFFICULTY_SETTINGS[Difficulty.MEDIUM]['obstacle_speed']
    hard_speed = DIFFICULTY_SETTINGS[Difficulty.HARD]['obstacle_speed']
    
    # Higher difficulty should have more frequent obstacles
    assert easy_freq >= medium_freq >= hard_freq, (
        "Obstacle frequency should increase with difficulty"
    )
    
    # Higher difficulty should have faster obstacles
    assert easy_speed <= medium_speed <= hard_speed, (
        "Obstacle speed should increase with difficulty"
    )
    
    print("✅ Difficulty progression is correct!")
    print(f"Easy: {easy_freq} frequency, {easy_speed} speed")
    print(f"Medium: {medium_freq} frequency, {medium_speed} speed")
    print(f"Hard: {hard_freq} frequency, {hard_speed} speed")


if __name__ == "__main__":
    test_difficulty_settings()
