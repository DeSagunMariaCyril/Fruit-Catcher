import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
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

# Load game-style fonts
title_font = pygame.font.SysFont("pressstart2p", 80)
feedback_font = pygame.font.SysFont("pressstart2p", 50)
font = pygame.font.SysFont("comicsansms", 40)
game_over_font = pygame.font.SysFont("pressstart2p", 80)
shield_font = pygame.font.SysFont("comicsansms", 30)

# Define object sizes and speeds
basket_radius = 60  # Basket now behaves as a circle for collision detection
basket_speed = 15
fruit_speed = 5

# Game variables
score = 0
level = 1
basket_x = screen_width // 2
basket_y = screen_height - basket_radius - 10
achievement_message = ""
objects = []
bomb_chance = 0.1
next_object_time = 100
shield_active = False
double_points_active = False
lives = 5
missed_fruits = 0
shield_count = 0
shield_timer = 0
shield_lifetime = 5
last_shield_spawn = 0
double_points_timer = 0  # Track double points duration

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
                    show_instructions()  # Show instructions before starting the game
                    menu_running = False
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

# Function to display the instructions screen
def show_instructions():
    screen.fill((255, 255, 255))
    instructions_text1 = font.render("INSTRUCTIONS:", True, (0, 0, 0))
    instructions_text2 = font.render("Use the LEFT and RIGHT arrow keys", True, (0, 0, 0))
    instructions_text3 = font.render("to move the basket and catch fruits.", True, (0, 0, 0))
    instructions_text4 = font.render("Avoid rotten fruits and bombs!", True, (0, 0, 0))
    instructions_text5 = font.render("Press any key to start the game.", True, (255, 0, 0))

    screen.blit(instructions_text1, (screen_width // 2 - instructions_text1.get_width() // 2, screen_height // 4))
    screen.blit(instructions_text2, (screen_width // 2 - instructions_text2.get_width() // 2, screen_height // 4 + 50))
    screen.blit(instructions_text3, (screen_width // 2 - instructions_text3.get_width() // 2, screen_height // 4 + 100))
    screen.blit(instructions_text4, (screen_width // 2 - instructions_text4.get_width() // 2, screen_height // 4 + 150))
    screen.blit(instructions_text5, (screen_width // 2 - instructions_text5.get_width() // 2, screen_height // 4 + 200))

    pygame.display.update()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()  # Start the game after the instructions
                waiting_for_start = False

# Function to show feedback message (without blocking game loop)
def show_feedback_message(message, color, display_time=2000):
    global feedback_message, feedback_start_time
    feedback_message = (message, color)
    feedback_start_time = pygame.time.get_ticks()
    
# Main game loop
def game_loop():
    global score, basket_x, next_object_time, bomb_chance, level, achievement_message, shield_active, double_points_active, lives, missed_fruits, fruit_speed, objects, shield_count, shield_timer, last_shield_spawn, double_points_timer, feedback_message, feedback_start_time

    objects = []  # Reset objects list at the start of each game
    feedback_message = None  # No feedback message initially
    feedback_start_time = 0  # Start time for feedback messages
    running = True

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Basket movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > basket_radius:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < screen_width - basket_radius:
            basket_x += basket_speed

        # Spawn objects (including shield and double points)
        next_object_time -= 1
        if next_object_time <= 0 and len(objects) < 10:
            object_x = random.randint(0, screen_width - basket_radius * 2)
            if random.random() < bomb_chance:
                object_img = bomb_img
            elif random.random() < 0.1:  # 10% chance to spawn a shield
                object_img = shield_img
            elif random.random() < 0.1:  # 10% chance to spawn double points
                object_img = double_points_img
            else:
                object_img = random.choice(healthy_fruit_images + rotten_fruit_images)
            objects.append({"img": object_img, "x": object_x, "y": -100})
            next_object_time = random.randint(100, 300)

        # Move objects
        new_objects = []
        for obj in objects:
            obj["y"] += fruit_speed  # Move the object downwards
            if obj["y"] > screen_height:
                continue  # Ignore objects that go out of screen
            if obj["y"] + basket_radius * 2 >= basket_y and abs(obj["x"] - basket_x) < basket_radius * 2:
                if obj["img"] == bomb_img:
                    lives -= 1
                    show_feedback_message("Bomb Caught!", (255, 0, 0))
                elif obj["img"] in healthy_fruit_images:
                    score += 5
                    show_feedback_message("Healthy Fruit Caught!", (0, 255, 0))
                elif obj["img"] in rotten_fruit_images:
                    score -= 5
                    if score < 0:
                        score = 0
                    missed_fruits += 1
                    show_feedback_message("Rotten Fruit Caught!", (255, 165, 0))
                elif obj["img"] == shield_img:
                    shield_count += 1
                    show_feedback_message("Shield Activated!", (0, 0, 255))
                elif obj["img"] == double_points_img:
                    double_points_active = True
                    double_points_timer = time.time()
                    show_feedback_message("Double Points Activated!", (255, 215, 0))

                continue  # Skip to next object

            new_objects.append(obj)

        objects = new_objects

        # Draw objects
        for obj in objects:
            screen.blit(obj["img"], (obj["x"], obj["y"]))

        # Draw basket
        basket_rect = fruit_basket.get_rect(center=(basket_x, basket_y))
        screen.blit(fruit_basket, basket_rect)

        # Display score, level, lives, shield count, and double points
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        shield_text = shield_font.render(f"Shields: {shield_count}", True, (0, 0, 255))
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (screen_width - lives_text.get_width() - 20, 20))
        screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, 20))
        screen.blit(shield_text, (20, 70))

        # Show feedback message
        if feedback_message:
            message, color = feedback_message
            feedback_text = feedback_font.render(message, True, color)
            screen.blit(feedback_text, (screen_width // 2 - feedback_text.get_width() // 2, screen_height // 2))

        # Check if the feedback message time has passed
        if feedback_message and pygame.time.get_ticks() - feedback_start_time > 2000:
            feedback_message = None  # Remove feedback after 2 seconds

        # Level up check
        if score >= level * 100:
            level += 1
            show_feedback_message(level_feedback[level - 1], (0, 255, 0))

        # Double points active
        if double_points_active:
            elapsed_time = time.time() - double_points_timer
            double_points_time_remaining = max(0, 10 - int(elapsed_time))  # Prevent going below 0
            if double_points_time_remaining == 0:
                double_points_active = False
                show_feedback_message("Double Points Ended!", (255, 0, 0))
            double_points_text = font.render(f"Double Points: {double_points_time_remaining}s", True, (255, 215, 0))
            screen.blit(double_points_text, (screen_width // 2 - double_points_text.get_width() // 2, 70))

        # Update screen
        pygame.display.update()

        # Check for game over
        if lives <= 0:
            game_over()

        clock.tick(60)

# Game over function
def game_over():
    screen.fill((255, 255, 255))
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))

    score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))

    retry_button_rect = screen.blit(retry_button, (screen_width // 2 - retry_button.get_width() // 2, screen_height // 2 + 100))

    pygame.display.update()

    waiting_for_retry = True
    while waiting_for_retry:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    game_loop()  # Restart the game
                    waiting_for_retry = False

# Run the game
main_menu()
