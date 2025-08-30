# 3D Perspective Configuration for Asphalt-style Racing


# Road perspective settings
ROAD_WIDTH = 2000  # Virtual road width in 3D space
ROAD_LENGTH = 5000  # Virtual road length in 3D space
SEGMENT_LENGTH = 200  # Length of each road segment


# Camera settings
CAMERA_HEIGHT = 1500  # Camera height above road
CAMERA_DEPTH = 0.84  # Camera depth (field of view)
CAMERA_FOV = 100  # Field of view in degrees


# Player car settings
PLAYER_Z = 0  # Player's Z position (always at camera)
PLAYER_X = 0  # Player's X position (center of road)


# Rendering settings
DRAW_DISTANCE = 300  # How many segments to draw
CLIP_NEAR = 100  # Near clipping plane
CLIP_FAR = 3000  # Far clipping plane


# Road appearance
ROAD_COLOR = (100, 100, 100)  # Dark gray
GRASS_COLOR = (60, 180, 75)  # Green
RUMBLE_COLOR = (255, 255, 255)  # White
LANE_COLOR = (255, 255, 255)  # White


# Sky and environment
SKY_COLOR = (113, 197, 207)  # Light blue
HORIZON_COLOR = (150, 200, 255)  # Horizon blue


# Road segment types
class SegmentType:
    FLAT = 0
    UP = 1
    DOWN = 2


# Curve intensities
class CurveIntensity:
    NONE = 0
    EASY = 2
    MEDIUM = 4
    HARD = 6


# Hill intensities
class HillIntensity:
    NONE = 0
    LOW = 20
    MEDIUM = 40
    HIGH = 60


# Track definition
TRACK_LENGTH = 200  # Number of segments in track
