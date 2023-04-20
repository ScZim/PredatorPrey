import pygame
import random
import math
from perlin_noise import PerlinNoise
from pygame.locals import *
# Initialize Pygame
pygame.init()
pnoise2 = PerlinNoise()
# Set up the game window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Preydator')

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

#Main Menu
def main_menu():
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 1000
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    main_menu = True
    while main_menu:
        click = False
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
    
        game_window.fill(WHITE)
        font = pygame.font.Font(None, 106)
        rules_font = pygame.font.Font(None, 36)
        #MENU AND RULES TEXT
        play_text = font.render("PLAY: ", True, RED)
        menu_text = font.render("Main Menu", True, RED)
        rules_text1 = rules_font.render("RULES: Use the arrow keys to eat as many blue prey as possible but WATCH OUT for red", True, RED)
        rules_text2 = rules_font.render("predators. Use SPACE when you see 'Boost Available' for an extra jolt of speed.", True, RED)
        game_window.blit(menu_text, (400, 50))
        game_window.blit(play_text, (175, 200))
        game_window.blit(rules_text1, (100, 350))
        game_window.blit(rules_text2, (196, 385))
        
        #BUTTON - EASY
        button_1 = pygame.Rect(400, 200, 178, 80)
        pygame.draw.rect(game_window, (55, 55, 55), button_1)
        
        #BUTTON - MEDIUM
        button_2 = pygame.Rect(600, 200, 288, 80)
        pygame.draw.rect(game_window, (55, 55, 55), button_2)
        
        #BUTTON - HARD
        button_3 = pygame.Rect(910, 200, 185, 80)
        pygame.draw.rect(game_window, (55, 55, 55), button_3)
        
        #BUTTON DIFFICULTY TEXT
        easy_text = font.render('Easy', True, BLUE)
        med_text = font.render('Medium', True, BLUE)
        hard_text = font.render('Hard', True, BLUE)
        game_window.blit(easy_text, (405, 200))
        game_window.blit(med_text, (605, 200))
        game_window.blit(hard_text, (915, 200))
        mx, my = pygame.mouse.get_pos()
        
        if button_1.collidepoint((mx, my)):
            if click:
                game_easy()
        if button_2.collidepoint((mx, my)):
            if click:
                game_med()
        if button_3.collidepoint((mx, my)):
            if click:
                game_hard()
        pygame.display.update()

#EASY GAME MODE        
def game_easy():        
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
    boost_duration = 500  # in milliseconds
    boost_start_time = 0
    boost_end_time = None
    boost_cooldown = 10000 #in milliseconds
    boost_mult = 2  # increase the speed by a factor of 2 when boosting
    boost_active = False
    speed = 0.33
    boost_available = True
    # Create boost text surface
    font = pygame.font.Font(None, 36)
    boost_text = font.render("Boost Available", True, RED)

#Game Loop
    game_over = False
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_SPACE and boost_available:
                    # activate the boost
                    boost_start_time = pygame.time.get_ticks()
                    boost_end_time = boost_start_time + boost_duration
                    boost_active = True
                    boost_available = False
    
                
        # update the boost status
        if boost_active:
            if pygame.time.get_ticks() >= boost_end_time:
                # deactivate the boost
                boost_active = False
                boost_start_time = pygame.time.get_ticks()

        if boost_active:
            speed = 0.33 * boost_mult
        else:
            speed = 0.33
    
        if not boost_active and pygame.time.get_ticks() >= boost_start_time + boost_cooldown:
            boost_available = True

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
                        other_distance = math.sqrt(((enemy.x - other_enemy.x) ** 2 + (enemy.y - other_enemy.y) ** 2)+1)
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
    #Boost available text    
        if boost_available:
            game_window.blit(boost_text, (1000, 10))
        #Score Font
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, RED)
        game_window.blit(score_text, (10, 10))
        pygame.display.update()

    # Update noise offset for perlin noise
        noise_offset += 0.1

    while game_over:
        click = False
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
    
        game_window.fill(WHITE)
        font = pygame.font.Font(None, 106)
        score_text = font.render("SCORE: " + str(score), True, RED)
        game_over_text = font.render("GAME OVER", True, RED)
        game_window.blit(score_text, (400, 450))
        game_window.blit(game_over_text, (400, 350))
        #Restart button
        button_1 = pygame.Rect(400, 550, 250, 100)
        pygame.draw.rect(game_window, (155, 155, 155), button_1)
        retry_text = font.render('Retry?', True, RED)
        game_window.blit(retry_text, (405, 555))
        mx, my = pygame.mouse.get_pos()
        
        if button_1.collidepoint((mx, my)):
            if click:
                game_easy()

        pygame.display.update()
        
#MEDIUM GAME MODE        
def game_med():        
# Initialize game objects
    player = Player()
    ENEMY_COUNT = 35
    enemies = []
    predators = []
    predator = None
    predator_countdown = 4 #number of enemies to eat before predator spawns
    predator_spawned = False
    game_over = False

    for i in range(ENEMY_COUNT):
        enemies.append(Enemy())



    score = 0
    noise_offset = 0

    #Boost Parameters
    boost_duration = 500  # in milliseconds
    boost_start_time = 0
    boost_end_time = None
    boost_cooldown = 10000 #in milliseconds
    boost_mult = 2  # increase the speed by a factor of 2 when boosting
    boost_active = False
    speed = 0.33
    boost_available = True
    # Create boost text surface
    font = pygame.font.Font(None, 36)
    boost_text = font.render("Boost Available", True, RED)

#Game Loop
    game_over = False
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # if event.type == pygame.KEYDOWN:
                # if event.key == K_ESCAPE:
                    # pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_SPACE and boost_available:
                    # activate the boost
                    boost_start_time = pygame.time.get_ticks()
                    boost_end_time = boost_start_time + boost_duration
                    boost_active = True
                    boost_available = False
    
                
        # update the boost status
        if boost_active:
            if pygame.time.get_ticks() >= boost_end_time:
                # deactivate the boost
                boost_active = False
                boost_start_time = pygame.time.get_ticks()

        if boost_active:
            speed = 0.33 * boost_mult
        else:
            speed = 0.33
    
        if not boost_active and pygame.time.get_ticks() >= boost_start_time + boost_cooldown:
            boost_available = True

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
                dx *= 0.2
                dy *= 0.2
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
                        other_distance = math.sqrt(((enemy.x - other_enemy.x) ** 2 + (enemy.y - other_enemy.y) ** 2)+1)
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
               if score % 4 == 0:
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
                px *= -0.25
                py *= -0.25

            else:
                px = predator.x - player.x
                py = predator.y - player.y
                norm = math.sqrt(px ** 2 + py ** 2)
                if norm != 0:
                    px /= norm
                    py /= norm
                px *= -0.18
                py *= -0.18
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
    #Boost available text    
        if boost_available:
            game_window.blit(boost_text, (1000, 10))
        #Score Font
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, RED)
        game_window.blit(score_text, (10, 10))
        pygame.display.update()

    # Update noise offset for perlin noise
        noise_offset += 0.1

    while game_over:
        click = False
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
    
        game_window.fill(WHITE)
        font = pygame.font.Font(None, 106)
        score_text = font.render("SCORE: " + str(score), True, RED)
        game_over_text = font.render("GAME OVER", True, RED)
        game_window.blit(score_text, (400, 450))
        game_window.blit(game_over_text, (400, 350))
        #Restart button
        button_1 = pygame.Rect(400, 550, 250, 100)
        pygame.draw.rect(game_window, (155, 155, 155), button_1)
        retry_text = font.render('Retry?', True, RED)
        game_window.blit(retry_text, (405, 555))
        mx, my = pygame.mouse.get_pos()
        
        if button_1.collidepoint((mx, my)):
            if click:
                game_med()

        pygame.display.update()

#HARD GAME MODE        
def game_hard():
# Initialize game objects
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    ENEMY_COUNT = 25
    game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    player = Player()
    enemies = []
    predators = []
    predator = None
    predator_countdown = 3 #number of enemies to eat before predator spawns
    predator_spawned = False
    game_over = False

    for i in range(ENEMY_COUNT):
        enemies.append(Enemy())



    score = 0
    noise_offset = 0

    #Boost Parameters
    boost_duration = 500  # in milliseconds
    boost_start_time = 0
    boost_end_time = None
    boost_cooldown = 10000 #in milliseconds
    boost_mult = 2  # increase the speed by a factor of 2 when boosting
    boost_active = False
    speed = 0.33
    boost_available = True
    # Create boost text surface
    font = pygame.font.Font(None, 36)
    boost_text = font.render("Boost Available", True, RED)

#Game Loop
    game_over = False
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # if event.type == pygame.KEYDOWN:
                # if event.key == K_ESCAPE:
                    # pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_SPACE and boost_available:
                    # activate the boost
                    boost_start_time = pygame.time.get_ticks()
                    boost_end_time = boost_start_time + boost_duration
                    boost_active = True
                    boost_available = False
    
                
        # update the boost status
        if boost_active:
            if pygame.time.get_ticks() >= boost_end_time:
                # deactivate the boost
                boost_active = False
                boost_start_time = pygame.time.get_ticks()

        if boost_active:
            speed = 0.33 * boost_mult
        else:
            speed = 0.33
    
        if not boost_active and pygame.time.get_ticks() >= boost_start_time + boost_cooldown:
            boost_available = True

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
                dx *= 0.25
                dy *= 0.25
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
                        other_distance = math.sqrt(((enemy.x - other_enemy.x) ** 2 + (enemy.y - other_enemy.y) ** 2)+1)
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
            # Spawn predator every 3 eaten enemies
               if score % 3 == 0:
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
                px *= -0.28
                py *= -0.28

            else:
                px = predator.x - player.x
                py = predator.y - player.y
                norm = math.sqrt(px ** 2 + py ** 2)
                if norm != 0:
                    px /= norm
                    py /= norm
                px *= -0.2
                py *= -0.2
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
    #Boost available text    
        if boost_available:
            game_window.blit(boost_text, (WINDOW_WIDTH-200, 10))
        #Score Font
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, RED)
        game_window.blit(score_text, (10, 10))
        pygame.display.update()

    # Update noise offset for perlin noise
        noise_offset += 0.1

    while game_over:
        click = False
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
    
        game_window.fill(WHITE)
        font = pygame.font.Font(None, 106)
        score_text = font.render("SCORE: " + str(score), True, RED)
        game_over_text = font.render("GAME OVER", True, RED)
        game_window.blit(score_text, (300, 350))
        game_window.blit(game_over_text, (300, 250))
        #Restart button
        button_1 = pygame.Rect(300, 450, 250, 100)
        pygame.draw.rect(game_window, (155, 155, 155), button_1)
        retry_text = font.render('Retry?', True, RED)
        game_window.blit(retry_text, (305, 455))
        mx, my = pygame.mouse.get_pos()
        
        if button_1.collidepoint((mx, my)):
            if click:
                game_hard()

        pygame.display.update()
        
main_menu()
