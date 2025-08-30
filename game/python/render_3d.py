import pygame
import math
from config_3d import (
    ROAD_WIDTH, CAMERA_HEIGHT, CAMERA_DEPTH, ROAD_COLOR,
    GRASS_COLOR, RUMBLE_COLOR, LANE_COLOR, SKY_COLOR,
    HORIZON_COLOR, DRAW_DISTANCE, CLIP_NEAR
)


class RoadSegment:
    def __init__(self, index, world_z, curve=0, y=0, type=0):
        self.index = index
        self.world_z = world_z
        self.curve = curve
        self.y = y
        self.type = type
        self.screen_x = 0
        self.screen_y = 0
        self.scale = 0
        self.clip = 0


class Renderer3D:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_x = 0
        self.camera_y = CAMERA_HEIGHT
        self.camera_z = 0
        self.player_x = 0
        self.player_z = 0
        self.road_segments = []
        
    def project(self, point_x, point_y, point_z, camera_x, camera_y, camera_z):
        translated_x = point_x - camera_x
        translated_y = point_y - camera_y
        translated_z = point_z - camera_z
        
        scale = CAMERA_DEPTH / translated_z if translated_z > 0 else 0
        
        # Break up long lines for Flake8 compliance
        screen_x = (self.screen_width / 2)
        screen_x += scale * translated_x * self.screen_width / 2
        
        screen_y = (self.screen_height / 2)
        screen_y -= scale * translated_y * self.screen_height / 2
        
        return screen_x, screen_y, scale
        
    def create_road_segments(self, track_length):
        self.road_segments = []
        for i in range(track_length):
            z = i * 200
            
            curve_val = math.sin(i * 0.1) * 0.5 if i > 50 and i < 150 else 0
            y_val = math.sin(i * 0.05) * 100 if i > 30 and i < 170 else 0
            
            segment_type = 0
            if y_val > 50:
                segment_type = 1
            elif y_val < -50:
                segment_type = 2
                
            self.road_segments.append(
                RoadSegment(i, z, int(curve_val), int(y_val), segment_type)
            )
            
    def update_camera(self, player_x, player_z, speed):
        self.camera_z = player_z
        self.player_x = player_x
        self.player_z = player_z
        
        target_x = player_x
        self.camera_x += (target_x - self.camera_x) * 0.1
        
    def render_sky_and_ground(self, screen):
        screen.fill(SKY_COLOR)
        
        horizon_y = self.screen_height * 0.4
        pygame.draw.line(
            screen, HORIZON_COLOR, (0, horizon_y),
            (self.screen_width, horizon_y), 2
        )
        
        pygame.draw.rect(
            screen, GRASS_COLOR,
            (0, horizon_y, self.screen_width, self.screen_height - horizon_y)
        )
        
    def render_road(self, screen):
        if not self.road_segments:
            return
            
        visible_segments = []
        for segment in self.road_segments:
            if segment.world_z - self.camera_z < DRAW_DISTANCE:
                visible_segments.append(segment)
                
        visible_segments.sort(key=lambda s: s.world_z, reverse=True)
        
        for segment in visible_segments:
            if segment.world_z - self.camera_z <= CLIP_NEAR:
                continue
                
            screen_x, screen_y, scale = self.project(
                segment.world_z * segment.curve,
                segment.y,
                segment.world_z - self.camera_z,
                self.camera_x, self.camera_y, self.camera_z
            )
            
            segment.screen_x = screen_x
            segment.screen_y = screen_y
            segment.scale = scale
            segment.clip = scale
            
            if scale > 0.01:
                self.render_segment(screen, segment)
                
    def render_segment(self, screen, segment):
        road_width = ROAD_WIDTH * segment.scale
        lane_width = road_width / 3
        
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        
        road_rect = pygame.Rect(
            center_x - road_width / 2,
            center_y - road_width / 2,
            road_width,
            road_width
        )
        pygame.draw.rect(screen, ROAD_COLOR, road_rect)
        
        for i in range(1, 3):
            lane_x = center_x - road_width / 2 + lane_width * i
            pygame.draw.line(
                screen, LANE_COLOR,
                (lane_x, center_y - road_width / 2),
                (lane_x, center_y + road_width / 2), 2
            )
        
        pygame.draw.line(
            screen, RUMBLE_COLOR,
            (center_x - road_width / 2, center_y - road_width / 2),
            (center_x - road_width / 2, center_y + road_width / 2), 4
        )
        pygame.draw.line(
            screen, RUMBLE_COLOR,
            (center_x + road_width / 2, center_y - road_width / 2),
            (center_x + road_width / 2, center_y + road_width / 2), 4
        )
        
    def render_car(self, screen, car_x, car_z, car_image=None):
        screen_x, screen_y, scale = self.project(
            car_x, 0, car_z - self.camera_z,
            self.camera_x, self.camera_y, self.camera_z
        )
        
        if scale > 0.01:
            if car_image:
                scaled_width = int(car_image.get_width() * scale)
                scaled_height = int(car_image.get_height() * scale)
                scaled_car = pygame.transform.scale(
                    car_image, (scaled_width, scaled_height)
                )
                screen.blit(
                    scaled_car, 
                    (screen_x - scaled_width / 2, screen_y - scaled_height / 2)
                )
            else:
                car_width = 50 * scale
                car_height = 100 * scale
                pygame.draw.rect(
                    screen, (255, 0, 0),
                    (screen_x - car_width / 2, screen_y - car_height / 2,
                     car_width, car_height)
                )
