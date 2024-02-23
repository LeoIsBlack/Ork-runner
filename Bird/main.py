import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1500, 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")


background_img = pygame.image.load('background.jpg')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
dino_img = pygame.image.load('dino.png')
cactus_img = pygame.image.load('cactus.png')

dino_width, dino_height = 70, 60
dino_x, dino_y = 50, HEIGHT - dino_height - 10
is_jumping = False
jump_count = 10
score = 0

cactus_width, cactus_height = 5, 80
cactus_x, cactus_y = WIDTH, HEIGHT - cactus_height - 10
cactus_speed = 5


jump_sound = pygame.mixer.Sound('jump_sound.wav')
point_sound = pygame.mixer.Sound('pointsound.wav')

pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()


def get_record():
    try:
        with open('record.txt', 'r') as file:
            return int(file.read())
    except:
        return 0

def update_record(score):
    with open('record.txt', 'w') as file:
        file.write(str(score))

record = get_record()

def show_menu(score, record):
    pygame.mixer.music.stop()
    menu_font = pygame.font.Font(None, 72)
    menu_text = menu_font.render(f"Game Over!!! Score: {score} Record: {record}", True, BLACK)
    screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 - menu_text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(2500)
    pygame.quit()
    sys.exit()

game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        jump_sound.play()

    if is_jumping:

        if jump_count >= -10:
            neg = 1 if jump_count >= 0 else -1
            dino_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    cactus_x -= cactus_speed
    if cactus_x < 0:
        cactus_x = WIDTH
        score += 1
        cactus_speed += 1.1

        if score % 10 == 0:
            point_sound.play()

    if (
        dino_x < cactus_x + cactus_width
        and dino_x + dino_width > cactus_x
        and dino_y < cactus_y + cactus_height
        and dino_y + dino_height > cactus_y
    ):
        if score > record:
            update_record(score)
            record = score
        show_menu(score, record)

    screen.blit(background_img, (0, 0))
    screen.blit(dino_img, (dino_x, dino_y))
    screen.blit(cactus_img, (cactus_x, cactus_y))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score} Record: {record}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

show_menu(score, record)



