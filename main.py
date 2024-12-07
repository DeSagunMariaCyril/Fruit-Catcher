import pygame
import random
import time

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
fruit_speed = 5  # Initial fruit fall speed

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
feedback_message = None  # Initial feedback message is None
feedback_start_time = 0  # Start time for feedback messages

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

# Function to show feedback message in center for 2 seconds
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
        if next_object_time <= 0 and len(objects) < 30:  # Increase the max number of objects on the screen
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
            next_object_time = random.randint(40, 80)  # Decrease spawn time as level increases

        # Increase falling speed as the game progresses
        fruit_speed = 5 + level * 2  # Increase speed by 2 units per level (adjust as needed)

        # Move objects
        new_objects = []
        for obj in objects:
            obj["y"] += fruit_speed  # Move the object downwards
            if obj["y"] > screen_height:
                continue  # Ignore objects that go out of screen
            if obj["y"] + basket_radius * 2 >= basket_y and abs(obj["x"] - basket_x) < basket_radius * 2:
                if obj["img"] == bomb_img:
                    if not shield_active:  # Only deduct life if shield is not active
                        lives -= 1
                        show_feedback_message("Bomb Caught!", (255, 0, 0))
                    else:
                        show_feedback_message("Bomb Blocked by Shield!", (0, 255, 0))  # If shield is active, block the bomb
                elif obj["img"] == shield_img:
                    shield_active = True
                    shield_count = shield_lifetime
                    show_feedback_message("Shield Activated!", (0, 255, 0))
                elif obj["img"] == double_points_img:
                    double_points_active = True
                    double_points_timer = 5 * 60  # 5 seconds of double points (60 FPS)
                    show_feedback_message("Double Points Active!", (0, 255, 255))
                else:
                    # Score logic: Double points active
                    if double_points_active:
                        score += 20  # Double points (10 * 2)
                    else:
                        score += 10  # Catch healthy fruit
            else:
                new_objects.append(obj)

        # Update the list of objects
        objects = new_objects

        # Level up logic
        if score // 100 >= level:
            level += 1
            show_feedback_message(level_feedback[level - 1], (0, 0, 255))

        # Draw the basket and objects
        screen.blit(fruit_basket, (basket_x - basket_radius, basket_y - basket_radius))

        for obj in objects:
            screen.blit(obj["img"], (obj["x"], obj["y"]))

        # Draw score, level, and lives
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))

        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (screen_width - level_text.get_width() - 20, 20))
        screen.blit(lives_text, (screen_width // 2 - lives_text.get_width() // 2, 20))

        # Feedback message (if any)
        if feedback_message and pygame.time.get_ticks() - feedback_start_time < 2000:
            feedback_text = feedback_font.render(feedback_message[0], True, feedback_message[1])
            screen.blit(feedback_text, (screen_width // 2 - feedback_text.get_width() // 2, screen_height // 2 - feedback_text.get_height() // 2))
        elif pygame.time.get_ticks() - feedback_start_time >= 2000:
            feedback_message = None  # Remove feedback message after 2 seconds

        # Handle power-up timers
        if shield_active:
            shield_timer += 1
            if shield_timer >= shield_lifetime * 60:  # 5 seconds, as we are running at 60 FPS
                shield_active = False
                shield_timer = 0
                show_feedback_message("Shield Deactivated!", (255, 0, 0))

        if double_points_active:
            double_points_timer -= 1
            if double_points_timer <= 0:
                double_points_active = False
                show_feedback_message("Double Points Deactivated!", (255, 0, 0))

        # Update the screen
        pygame.display.update()

        # Delay to create frame rate
        clock.tick(60)

        # Check for game over
        if lives <= 0:
            game_over()

    pygame.quit()
    quit()

# Game over screen
def game_over():
    screen.fill((0, 0, 0))
    game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    retry_text = font.render("Click to Retry", True, (0, 255, 0))

    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 50))

    pygame.display.update()

    waiting_for_retry = True
    while waiting_for_retry:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()  # Restart the game

# Start the game
main_menu()
