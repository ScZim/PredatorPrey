import pygame
import random
import math
from perlin_noise import PerlinNoise

# Initialize Pygame
pygame.init()
pnoise2 = PerlinNoise()
# Set up the game window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Pygame')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (70, 130, 180)
# Define constants
PLAYER_SIZE = 20
ENEMY_SIZE = 10
ENEMY_COUNT = 45
PREDATOR_SIZE = 30

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.size = PLAYER_SIZE

    def draw(self):
        pygame.draw.rect(game_window, BLACK, (self.x, self.y, self.size, self.size))

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH - ENEMY_SIZE)
        self.y = random.randint(0, WINDOW_HEIGHT - ENEMY_SIZE)
        self.size = ENEMY_SIZE

    def draw(self):
        pygame.draw.rect(game_window, BLUE, (self.x, self.y, self.size, self.size))
        
class Predator:
    def __init__(self, player):
        self.player = player
        self.x = random.randint(0, WINDOW_WIDTH - PREDATOR_SIZE)
        self.y = random.randint(0, WINDOW_HEIGHT - PREDATOR_SIZE)
        self.size = PREDATOR_SIZE

    def draw(self):
        pygame.draw.rect(game_window, RED, (self.x, self.y, self.size, self.size))
        
# Initialize game objects
player = Player()
enemies = []
predators = []
predator = None
predator_countdown = 5 #number of enemies to eat before predator spawns
predator_spawned = False
game_over = False

for i in range(ENEMY_COUNT):
    enemies.append(Enemy())



score = 0
noise_offset = 0

#Boost Parameters
boost_duration = 2000  # in milliseconds
boost_start_time = 0
boost_end_time = None
boost_cooldown = 1000 #in milliseconds
boost_mult = 15  # increase the speed by a factor of 2 when boosting
boost_active = False
speed = 0.35
boost_available = False

#Game Loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # activate the boost
                boost_start_time = pygame.time.get_ticks()
                boost_active = True
    
                
    # update the boost status
    if boost_active:
        boost_time_elapsed = pygame.time.get_ticks() - boost_start_time
        if boost_time_elapsed >= boost_duration:
            # deactivate the boost
            boost_active = False
            boost_end_time = pygame.time.get_ticks() + boost_duration

    if pygame.time.get_ticks() > boost_start_time + boost_duration + boost_cooldown:
        boost_available = True
    if boost_active and boost_available:
        speed = 0.35 * boost_mult
    else:
        speed = 0.35        
    # Update game state
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    elif keys[pygame.K_RIGHT]:
        player.x += speed
    elif keys[pygame.K_UP]:
        player.y -= speed
    elif keys[pygame.K_DOWN]:
        player.y += speed

    # Move enemies
    for i, enemy in enumerate(enemies):
        # Determine enemy movement mode
        dx = player.x + player.size / 2 - (enemy.x + enemy.size / 2)
        dy = player.y + player.size / 2 - (enemy.y + enemy.size / 2)
        distance = math.sqrt(dx ** 2 + dy ** 2) - player.size / 2 + ENEMY_SIZE / 2
        if distance < 100:
            # Run away from player
            dx = enemy.x - player.x
            dy = enemy.y - player.y
            norm = math.sqrt(dx ** 2 + dy ** 2)
            if norm != 0:
                dx /= norm
                dy /= norm
            dx *= 0.17
            dy *= 0.17
        else:
            # Wander randomly using noise smoothing
            noise_scale = 0.01
            x_offset = pygame.time.get_ticks() * noise_scale
            y_offset = i * noise_scale
            angle = pnoise2(i * enemy.x + x_offset)
            dx = math.cos(angle * 2 * math.pi) * 0.05
            dy = math.sin(angle * 2 * math.pi) * 0.05
        # Avoid other enemies
            for other_enemy in enemies:
                if other_enemy != enemy:
                    other_distance = math.sqrt((enemy.x - other_enemy.x) ** 2 + (enemy.y - other_enemy.y) ** 2)
                    if other_distance < 50:
                        dx += (enemy.x - other_enemy.x) / other_distance * 0.1
                        dy += (enemy.y - other_enemy.y) / other_distance * 0.1
        
		# Update enemy position
        enemy.x += dx
        enemy.y += dy
        # Bound enemy within screen
        if enemy.x < 0:
            enemy.x = 0
        elif enemy.x + enemy.size > WINDOW_WIDTH:
            enemy.x = WINDOW_WIDTH - enemy.size
        if enemy.y < 0:
            enemy.y = 0
        elif enemy.y + enemy.size > WINDOW_HEIGHT:
            enemy.y = WINDOW_HEIGHT - enemy.size

    # Check for collisions
    for enemy in enemies:
        if player.x < enemy.x + enemy.size and \
           player.x + player.size > enemy.x and \
           player.y < enemy.y + enemy.size and \
           player.y + player.size > enemy.y:
            enemies.remove(enemy)
            player.size += 1
            score += 1
            # Spawn predator every 5 eaten enemies
            if score % 5 == 0:
                predators.append(Predator(Player))

    # Move predator if spawned
    for predator in predators:
        # Determine predator movement mode
        px = player.x + player.size / 2 - (predator.x + predator.size / 2)
        py = player.y + player.size / 2 - (predator.y + predator.size / 2)
        distance = math.sqrt(px ** 2 + py ** 2) - player.size / 2 + PREDATOR_SIZE / 2
        if distance < 200 + player.size:
            px = predator.x - player.x
            py = predator.y - player.y
            norm = math.sqrt(px ** 2 + py ** 2)
            if norm != 0:
                px /= norm
                py /= norm
            px *= -0.23
            py *= -0.23

        else:
            px = predator.x - player.x
            py = predator.y - player.y
            norm = math.sqrt(px ** 2 + py ** 2)
            if norm != 0:
                px /= norm
                py /= norm
            px *= -0.15
            py *= -0.15
		# Update predator position
        predator.x += px
        predator.y += py            
        # Check for collision with player
        if player.x < predator.x + predator.size and \
            player.x + player.size > predator.x and \
            player.y < predator.y + predator.size and \
            player.y + player.size > predator.y:
            game_over = True 

    # Spawn new enemies
    while len(enemies) < ENEMY_COUNT:
        enemies.append(Enemy())

    # Draw to the screen
    game_window.fill(WHITE)
    player.draw()
    for enemy in enemies:
        enemy.draw()
    for predator in predators:
	    predator.draw()
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, RED)
    game_window.blit(score_text, (10, 10))
    pygame.display.update()

    # Update noise offset for perlin noise
    noise_offset += 0.1

while game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    game_window.fill(WHITE)
    font = pygame.font.Font(None, 106)
    score_text = font.render("SCORE: " + str(score), True, RED)
    game_over_text = font.render("GAME OVER", True, RED)
    game_window.blit(score_text, (400, 450))
    game_window.blit(game_over_text, (400, 350))
    pygame.display.update()
