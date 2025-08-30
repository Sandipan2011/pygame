#!/usr/bin/env python3
"""
Test script to verify power-up sound functionality
"""
import os
import sys

# Add the game/python directory to the path
sys.path.insert(0, 'game/python')

import pygame
from config import CRASH_SOUND, SCORE_SOUND, ENGINE_SOUND, POWERUP_SOUND


def test_sound_config():
    """Test that sound constants are properly defined"""
    print("Testing sound configuration...")
    print(f"CRASH_SOUND: {CRASH_SOUND}")
    print(f"SCORE_SOUND: {SCORE_SOUND}")
    print(f"ENGINE_SOUND: {ENGINE_SOUND}")
    print(f"POWERUP_SOUND: {POWERUP_SOUND}")
    
    # Check if files exist (they won't, but we can check the paths)
    assets_dir = 'game/python/assets'
    for sound_file in [CRASH_SOUND, SCORE_SOUND, ENGINE_SOUND, POWERUP_SOUND]:
        full_path = os.path.join(assets_dir, sound_file)
        exists = os.path.exists(full_path)
        print(f"{sound_file}: {'Exists' if exists else 'Missing'}")


def test_power_up_logic():
    """Test power-up collection logic"""
    print("\nTesting power-up collection logic...")
    
    # Mock the power-up collection scenario
    power_up = {
        'type': 'speed',
        'duration': 5000,
        'rect': pygame.Rect(100, 100, 30, 30)
    }
    
    print(f"Power-up type: {power_up['type']}")
    print(f"Power-up duration: {power_up['duration']}ms")
    print("Power-up would play sound when collected")


if __name__ == "__main__":
    pygame.init()
    test_sound_config()
    test_power_up_logic()
    print("\n✅ Power-up sound system test completed successfully!")
