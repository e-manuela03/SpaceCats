import pygame
import sys
import random
import time
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shoot the Enemy")

# Set up background image
background_image = pygame.image.load("C:\\Users\\elena_0\\Desktop\\Joc Python\\photo.jpg")  # Replace with the path to your image
background_image = pygame.transform.scale(background_image, (width, height))

# Set up colors
white = (255, 255, 255)
black = (255, 255, 255)
red = (255, 0, 0)

# Set up the player icon (PNG image)
player_size = 50
player_icon = pygame.image.load("C:\\Users\\elena_0\\Desktop\\Joc Python\\rocket.png")  # Replace with the path to your PNG image
player_icon = pygame.transform.scale(player_icon, (player_size, player_size))

# Set up the bullet icons (PNG images)
bullet_size = (20, 20)  # Set the desired size for the bullet images
bullet_icons = [
    pygame.image.load("C:\\Users\\elena_0\\Desktop\\Joc Python\\cat1.png"),  # Replace with the path to your PNG image
    pygame.image.load("C:\\Users\\elena_0\\Desktop\\Joc Python\\cat2.png"),  # Replace with the path to your PNG image
    pygame.image.load("C:\\Users\\elena_0\\Desktop\\Joc Python\\cat3.png"),  # Replace with the path to your PNG image
    pygame.image.load("C:\\Users\\elena_0\\Desktop\\Joc Python\\cat4.png"),  # Replace with the path to your PNG image
    pygame.image.load("C:\\Users\\elena_0\\Desktop\\Joc Python\\cat5.png"),  # Replace with the path to your PNG image
    pygame.image.load("C:\\Users\\elena_0\\Desktop\\Joc Python\\cat6.png"),  # Replace with the path to your PNG image
    # Add more paths as needed
]

# Scale down the bullet images
bullet_icons = [pygame.transform.scale(bullet, bullet_size) for bullet in bullet_icons]

# Set up the player
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
player_speed = 10

# Set up the bullets
bullets = []

# Set up the enemy icon (PNG image)
enemy_size = 45
enemy_icon = pygame.image.load("C:\\Users\\elena_0\\Desktop\\Joc Python\\asteroid.png")  # Replace with the path to your PNG image
enemy_icon = pygame.transform.scale(enemy_icon, (enemy_size, enemy_size))

# Set up enemy position
enemy_x = random.randint(0, width - enemy_size)
enemy_y = 0

# Lives
lives = 3

# Score
score = 0
font = pygame.font.Font(None, 36)

# High score
high_score_file = "highscore.txt"
high_score = 0
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        try:
            high_score = int(file.read())
        except ValueError:
            high_score = 0

# Enemy respawn delay
enemy_respawn_delay = 1  # in seconds
last_enemy_destroyed_time = time.time()

# Enemy speed
enemy_speed = 5

# Bullet speed
bullet_speed = 15

# Initialize Pygame mixer
pygame.mixer.init()

# Load and play the MP3 file
mp3_file_path = "C:\\Users\\elena_0\\Desktop\\Joc Python\\music.wav"  # Replace with the path to your MP3 file
pygame.mixer.music.load(mp3_file_path)
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Main game loop
clock = pygame.time.Clock()

while lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed

    # Shoot bullets
    if keys[pygame.K_SPACE]:
        bullet_x = player_x + player_size // 2 - bullet_size[0] // 2
        bullet_y = player_y
        bullet_icon = random.choice(bullet_icons)
        bullets.append((bullet_x, bullet_y, bullet_icon))

    # Update bullets
    bullets = [(bx, by - bullet_speed, bi) for bx, by, bi in bullets if by > 0]

    # Update enemy position
    if time.time() - last_enemy_destroyed_time > enemy_respawn_delay:
        enemy_y += enemy_speed

    # Check collision with bullets
    for bullet_x, bullet_y, bullet_icon in bullets:
        if (
            enemy_x < bullet_x < enemy_x + enemy_size
            and enemy_y < bullet_y < enemy_y + enemy_size
        ):
            enemy_x = random.randint(0, width - enemy_size)
            enemy_y = 0
            score += 1
            last_enemy_destroyed_time = time.time()

    # Check if the enemy is out of the screen
    if enemy_y > height:
        enemy_x = random.randint(0, width - enemy_size)
        enemy_y = 0
        lives -= 1

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Draw everything
    screen.blit(player_icon, (player_x, player_y))
    screen.blit(enemy_icon, (enemy_x, enemy_y))

    for bullet_x, bullet_y, bullet_icon in bullets:
        screen.blit(bullet_icon, (bullet_x, bullet_y))

    # Display score and lives
    score_text = font.render(f"Score: {score} | Lives: {lives}", True, black)
    screen.blit(score_text, (10, 10))

    # Display high score in the upper right corner
    high_score_text = font.render(f"High Score: {high_score}", True, black)
    screen.blit(high_score_text, (width - high_score_text.get_width() - 10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(30)

# Stop the music when the game ends
pygame.mixer.music.stop()

# Update and display high score
if score > high_score:
    high_score = score
    with open(high_score_file, "w") as file:
        file.write(str(high_score))

# Display "You lost" message
font_large = pygame.font.Font(None, 72)
game_over_text = font_large.render("You lost!", True, black)
score_text = font.render(f"Your Score: {score} | High Score: {high_score}", True, black)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw "You lost" message and final score
    screen.blit(game_over_text, (width // 2 - 150, height // 2 - 50))
    screen.blit(score_text, (width // 2 - 200, height // 2 + 50))

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(30)
