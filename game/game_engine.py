import pygame
import random
from .target import Target

# Game Engine

WHITE = (255, 255, 255)
RED = (220, 60, 60)
DIFFICULTIES = {
    "Easy": {"base_radius": 45, "min_radius": 15, "lifespan_frames": 120},
    "Medium": {"base_radius": 40, "min_radius": 12, "lifespan_frames": 90},
    "Hard": {"base_radius": 35, "min_radius": 10, "lifespan_frames": 60},
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60
        self.difficulty = "Medium"
        self.target = self._spawn_target()

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.hits = 0
        self.misses = 0
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 26)
        self.game_over = False

    def _spawn_target(self):
        x = random.randint(self.margin, self.width - self.margin)
        y = random.randint(self.margin + self.hud_height, self.height - self.margin)

        settings = DIFFICULTIES[self.difficulty]

        return Target(
            x,
            y,
            base_radius=settings["base_radius"],
            min_radius=settings["min_radius"],
            lifespan_frames=settings["lifespan_frames"],
        )

    def restart(self, difficulty):
        self.difficulty = difficulty
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.time_left_frames = self.round_seconds * 60
        self.game_over = False
        self.target = self._spawn_target()
        
    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.restart("Easy")
                elif event.key == pygame.K_2:
                    self.restart("Medium")
                elif event.key == pygame.K_3:
                    self.restart("Hard")
                elif event.key == pygame.K_ESCAPE:
                    return False
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

        return True

    def _handle_click(self, pos):
        x, y = pos
        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            self.target = self._spawn_target()
        else:
            self.misses += 1

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.game_over = True
            return

        self.target.update()
        if self.target.expired():
            self.misses += 1  # letting a target time out counts as a miss too
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100 * self.hits / total, 1)

    def render(self, screen):
        screen.fill((0,0,0))
        if not self.game_over:
            # Draw target
            radius = int(self.target.visual_radius())
            pygame.draw.circle(
                screen,
                RED,
                (self.target.x, self.target.y),
                radius
            )

            # Draw target outline
            pygame.draw.circle(
                screen,
                WHITE,
                (self.target.x, self.target.y),
                radius,
                2
            )

            # Draw score
            score_text = self.font.render(
                f"Score: {self.score}",
                True,
                WHITE
            )
            screen.blit(score_text, (10, 10))

            # Draw timer
            seconds_left = max(0, self.time_left_frames // 60)
            timer_text = self.font.render(
                f"Time: {seconds_left}s",
                True,
                WHITE
            )
            screen.blit(
                timer_text,
                (self.width - 140, 10)
            )

            # Draw accuracy
            accuracy_text = self.font.render(
                f"Accuracy: {self.accuracy()}%",
                True,
                WHITE
            )
            screen.blit(
                accuracy_text,
                (self.width // 2 - 90, 10)
            )

        else:
            # Game Over screen
            game_over_text = self.font.render(
                "GAME OVER",
                True,
                WHITE
            )

            score_text = self.font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            accuracy_text = self.font.render(
                f"Final Accuracy: {self.accuracy()}%",
                True,
                WHITE
            )

            difficulty_text = self.font.render(
                "1 - Easy    2 - Medium    3 - Hard",
                True,
                WHITE
            )

            exit_text = self.font.render(
                "ESC - Exit",
                True,
                WHITE
            )

            screen.blit(
                game_over_text,
                game_over_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 100
                    )
                )
            )

            screen.blit(
                score_text,
                score_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 50
                    )
                )
            )

            screen.blit(
                accuracy_text,
                accuracy_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 10
                    )
                )
            )

            screen.blit(
                difficulty_text,
                difficulty_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 40
                    )
                )
            )

            screen.blit(
                exit_text,
                exit_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 80
                    )
                )
            )