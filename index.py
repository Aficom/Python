import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Collision Game")

# Colors (RGB format)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)    # Player color
RED = (255, 0, 0)     # Enemy color
BLACK = (0, 0, 0)     # Text color

# Frame rate controller
clock = pygame.time.Clock()
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a blue square for the player
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        # Start player in the middle of the screen
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5

    def update(self):
        # Move the player based on arrow key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a red square for the enemy
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Spawn the enemy at a random location on the screen
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

# Create Sprite Groups for rendering and collision detection
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# 1. Initialize Player and add to sprite group
player = Player()
all_sprites.add(player)

# 2. Initialize 7 Enemies randomly
for i in range(7):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# 3. Score Variable
score = 0

# Font for displaying the score
font = pygame.font.SysFont(None, 36)

# Main Game Loop
running = True
while running:
    # Handle Events (like closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites (handles player movement)
    all_sprites.update()

    # 4. Collision Detection
    # spritecollide checks if 'player' hits anything in the 'enemies' group.
    # True means the enemy will be removed from all groups upon collision.
    hits = pygame.sprite.spritecollide(player, enemies, True)
    
    for hit in hits:
        score += 1  # Increase score by 1
        
        # Respawn a new enemy to keep exactly 7 on screen
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)

    # Draw everything
    screen.fill(WHITE) # Clear screen with white background
    all_sprites.draw(screen) # Draw all sprites

    # Render and display the score text
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the display and tick the clock
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame cleanly
pygame.quit()