#!/usr/bin/env python3
"""
Test script to verify power-up functionality in the car racing game.
"""

import pygame
import sys
import os
sys.path.insert(0, 'game/python')

from config import WIDTH, HEIGHT, Difficulty, DIFFICULTY_SETTINGS
from game_utils import create_power_up

def test_power_up_creation():
    """Test that power-ups are created with correct properties."""
    print("Testing power-up creation...")
    
    # Test multiple power-up creations
    for i in range(20):
        power_up = create_power_up(WIDTH)
        
        # Verify power-up has required properties
        assert 'type' in power_up, "Power-up missing 'type' property"
        assert 'rect' in power_up, "Power-up missing 'rect' property"
        assert 'duration' in power_up, "Power-up missing 'duration' property"
        
        # Verify power-up type is valid
        valid_types = ['speed', 'shield', 'score_multiplier']
        assert power_up['type'] in valid_types, f"Invalid power-up type: {power_up['type']}"
        
        # Verify rect properties
        assert hasattr(power_up['rect'], 'x'), "Power-up rect missing x coordinate"
        assert hasattr(power_up['rect'], 'y'), "Power-up rect missing y coordinate"
        assert hasattr(power_up['rect'], 'width'), "Power-up rect missing width"
        assert hasattr(power_up['rect'], 'height'), "Power-up rect missing height"
        
        # Verify duration is positive
        assert power_up['duration'] > 0, f"Invalid duration: {power_up['duration']}"
        
        print(f"✓ Power-up {i+1}: {power_up['type']}, duration: {power_up['duration']}ms")

def test_power_up_distribution():
    """Test that power-ups are distributed with reasonable frequency."""
    print("\nTesting power-up type distribution...")
    
    type_counts = {'speed': 0, 'shield': 0, 'score_multiplier': 0}
    total_power_ups = 100
    
    for i in range(total_power_ups):
        power_up = create_power_up(WIDTH)
        type_counts[power_up['type']] += 1
    
    print(f"Power-up distribution (out of {total_power_ups}):")
    for power_type, count in type_counts.items():
        percentage = (count / total_power_ups) * 100
        print(f"  {power_type}: {count} ({percentage:.1f}%)")
    
    # Verify we have a reasonable distribution (not all one type)
    assert all(count > 0 for count in type_counts.values()), "Some power-up types never spawned"
    print("✓ Power-up distribution is reasonable")

def test_power_up_positioning():
    """Test that power-ups are positioned within screen bounds."""
    print("\nTesting power-up positioning...")
    
    for i in range(50):
        power_up = create_power_up(WIDTH)
        rect = power_up['rect']
        
        # Verify power-up is within screen width
        assert 0 <= rect.x <= WIDTH - rect.width, f"Power-up x position out of bounds: {rect.x}"
        assert rect.y <= 0, f"Power-up should start at or above y=0, got: {rect.y}"
        
        # Verify reasonable size
        assert 20 <= rect.width <= 50, f"Power-up width out of range: {rect.width}"
        assert 20 <= rect.height <= 50, f"Power-up height out of range: {rect.height}"
    
    print("✓ All power-ups positioned correctly")

def test_difficulty_settings():
    """Test that difficulty settings are properly configured."""
    print("\nTesting difficulty settings...")
    
    # Get all difficulty values from the enum
    difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
    
    for difficulty in difficulties:
        settings = DIFFICULTY_SETTINGS[difficulty]
        
        assert 'name' in settings, f"Difficulty {difficulty} missing name"
        assert 'obstacle_frequency' in settings, f"Difficulty {difficulty} missing obstacle_frequency"
        assert 'obstacle_speed' in settings, f"Difficulty {difficulty} missing obstacle_speed"
        
        assert isinstance(settings['obstacle_frequency'], int), "Obstacle frequency should be integer"
        assert isinstance(settings['obstacle_speed'], int), "Obstacle speed should be integer"
        assert settings['obstacle_frequency'] > 0, "Obstacle frequency should be positive"
        assert settings['obstacle_speed'] > 0, "Obstacle speed should be positive"
        
        print(f"✓ Difficulty {settings['name']}: frequency={settings['obstacle_frequency']}, speed={settings['obstacle_speed']}")

if __name__ == "__main__":
    print("Running power-up system tests...")
    print("=" * 50)
    
    try:
        test_power_up_creation()
        test_power_up_distribution()
        test_power_up_positioning()
        test_difficulty_settings()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED! Power-up system is working correctly.")
        print("\nSummary:")
        print("- Power-ups are created with correct properties")
        print("- Power-up types are distributed reasonably")
        print("- Power-ups are positioned within screen bounds")
        print("- Difficulty settings are properly configured")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
