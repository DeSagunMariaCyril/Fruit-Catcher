import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions for landscape
screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit Catcher")

# Load images (ensure these files exist in your directory)
background = pygame.image.load("background_image.jpeg")
fruit_basket = pygame.image.load("fruit_basket.png")
apple_img = pygame.image.load("apple.png")
cherry_img = pygame.image.load("cherry.png")
bomb_img = pygame.image.load("bomb.png")
apple_half_img = pygame.image.load("appleHalf.png")
lemon_half_img = pygame.image.load("lemonHalf.png")
play_button = pygame.image.load("play_button.png")
quit_button = pygame.image.load("quit_button.png")
shield_img = pygame.image.load("shield.png")  # Power-up image for shield
double_points_img = pygame.image.load("double_points.png")  # Power-up image for double points
retry_button = pygame.image.load("retry_button.png")  # Retry button image

# Resize images
apple_img = pygame.transform.scale(apple_img, (80, 80))
cherry_img = pygame.transform.scale(cherry_img, (80, 80))
apple_half_img = pygame.transform.scale(apple_half_img, (80, 80))
lemon_half_img = pygame.transform.scale(lemon_half_img, (80, 80))
bomb_img = pygame.transform.scale(bomb_img, (80, 80))
play_button = pygame.transform.scale(play_button, (400, 150))
quit_button = pygame.transform.scale(quit_button, (400, 150))
shield_img = pygame.transform.scale(shield_img, (80, 80))
double_points_img = pygame.transform.scale(double_points_img, (80, 80))
retry_button = pygame.transform.scale(retry_button, (400, 150))

# Set up fonts
font = pygame.font.SysFont(None, 40)
feedback_font = pygame.font.SysFont(None, 50)
title_font = pygame.font.SysFont(None, 80)
game_over_font = pygame.font.SysFont(None, 80)

# Define object sizes and speeds
basket_width = 120
basket_height = 200
basket_speed = 15
fruit_speed = 5

# Game variables
score = 0
level = 1
basket_x = (screen_width - basket_width) // 2
basket_y = screen_height - basket_height - 10
achievement_message = ""
objects = []
bomb_chance = 0.1
next_object_time = 100
shield_active = False
double_points_active = False
lives = 5
missed_fruits = 0

# Level feedback messages
level_feedback = [
    "Welcome to the game! Start catching fruits!",
    "Things are getting faster!",
    "Watch out for bombs!",
    "You're doing great!",
    "Keep going!"
]

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load fruit categories
healthy_fruit_images = [apple_img, cherry_img]
rotten_fruit_images = [apple_half_img, lemon_half_img]
power_up_images = [shield_img, double_points_img]

# Function to display the main menu
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill((255, 255, 255))

        # Display title
        title_text = title_font.render("Fruit Catcher", True, (255, 0, 0))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

        # Display play and quit buttons
        play_button_rect = screen.blit(play_button, (screen_width // 2 - play_button.get_width() // 2, screen_height // 2))
        quit_button_rect = screen.blit(quit_button, (screen_width // 2 - quit_button.get_width() // 2, screen_height // 2 + 160))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_loop()
                    menu_running = False
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

# Main game loop
def game_loop():
    global score, basket_x, next_object_time, bomb_chance, level, achievement_message, shield_active, double_points_active, lives, missed_fruits, fruit_speed, objects

    objects = []
    running = True

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Basket movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < screen_width - basket_width:
            basket_x += basket_speed

        # Spawn objects
        next_object_time -= 1
        if next_object_time <= 0 and len(objects) < 10:
            object_x = random.randint(0, screen_width - basket_width)
            if random.random() < bomb_chance:
                object_img = bomb_img
            elif random.random() < 0.1:
                object_img = random.choice(power_up_images)
            else:
                object_img = random.choice(healthy_fruit_images + rotten_fruit_images)
            objects.append({"img": object_img, "x": object_x, "y": -100})
            next_object_time = random.randint(60, 120)

        # Move objects and handle collisions
        new_objects = []
        basket_rect = pygame.Rect(basket_x, basket_y, basket_width, basket_height)
        for obj in objects:
            obj["y"] += fruit_speed
            obj_rect = pygame.Rect(obj["x"], obj["y"], 80, 80)

            if obj_rect.colliderect(basket_rect):
                if obj["img"] == bomb_img:
                    if not shield_active:
                        lives -= 1
                        achievement_message = f"Boom! Lives left: {lives}"
                        if lives <= 0:
                            running = False
                    else:
                        achievement_message = "Shield protected you!"
                elif obj["img"] in healthy_fruit_images:
                    score += 20 if double_points_active else 10
                    achievement_message = "Healthy fruit caught!"
                elif obj["img"] in rotten_fruit_images:
                    score -= 5
                    missed_fruits += 1
                    achievement_message = f"Oops! Rotten fruit missed! Total missed: {missed_fruits}"
                elif obj["img"] == shield_img:
                    shield_active = True
                    achievement_message = "Shield activated!"
                elif obj["img"] == double_points_img:
                    double_points_active = True
                    achievement_message = "Double points activated!"
            elif obj["y"] < screen_height:
                new_objects.append(obj)

        objects = new_objects

        # Level progression
        if score >= 100 and level == 1:
            level = 2
            fruit_speed += 1
            achievement_message = "Level 2 unlocked!"
        elif score >= 200 and level == 2:
            level = 3
            fruit_speed += 2
            achievement_message = "Level 3 unlocked!"
        elif score >= 300 and level == 3:
            level = 4
            fruit_speed += 3
            achievement_message = "Level 4 unlocked!"
        elif score >= 400 and level == 4:
            level = 5
            fruit_speed += 4
            achievement_message = "Level 5 unlocked!"

        # Render score and lives
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        achievement_text = feedback_font.render(achievement_message, True, (0, 255, 0))

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (screen_width - 200, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(achievement_text, (screen_width // 2 - achievement_text.get_width() // 2, 50))

        # Draw basket and objects
        screen.blit(fruit_basket, (basket_x, basket_y))
        for obj in objects:
            screen.blit(obj["img"], (obj["x"], obj["y"]))

        pygame.display.update()
        clock.tick(60)

    # Game over
    game_over()

# Function to display game over screen
def game_over():
    global score
    screen.fill((0, 0, 0))
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    score_text = font.render(f"Your score: {score}", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 50))

    retry_button_rect = screen.blit(retry_button, (screen_width // 2 - retry_button.get_width() // 2, screen_height // 2 + 120))
    pygame.display.update()

    waiting_for_retry = True
    while waiting_for_retry:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    score = 0
                    level = 1
                    lives = 3
                    game_loop()
                    waiting_for_retry = False

# Run the game
main_menu()

