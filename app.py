import pygame
import random
import sys

pygame.init()

# Cấu hình màn hình
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Runner - Python Edition")

# Màu sắc
BG_COLOR = (30, 30, 30)
LINE_COLOR = (80, 80, 80)
OBS_COLOR = (255, 51, 102)
WHITE = (255, 255, 255)

# Làn đường (3 làn)
LANES = [80, 200, 320]
current_lane = 1

# Tải ảnh nhân vật
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 70
try:
    player_img = pygame.image.load("player.jpg")
    player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
except Exception as e:
    player_img = None
    print("Không tìm thấy player.jpg, chuyển sang hình khối tạm thời.")

player_y = 480
player_speed = 6

obstacles = []
score = 0
spawn_timer = 0
game_over = False

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)
big_font = pygame.font.SysFont("Arial", 36, bold=True)

def reset_game():
    global current_lane, obstacles, score, game_over, player_speed
    current_lane = 1
    obstacles = []
    score = 0
    player_speed = 6
    game_over = False

# Vòng lặp game
while True:
    screen.fill(BG_COLOR)

    # Sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_over:
                reset_game()
            else:
                if event.key == pygame.K_LEFT and current_lane > 0:
                    current_lane -= 1
                elif event.key == pygame.K_RIGHT and current_lane < len(LANES) - 1:
                    current_lane += 1

    if not game_over:
        # Cập nhật tốc độ & sinh chướng ngại vật
        player_speed = 6 + (score // 400)
        spawn_timer += 1
        if spawn_timer > max(20, 50 - (score // 300)):
            obs_lane = random.randint(0, len(LANES) - 1)
            obstacles.append([obs_lane, -50, 45, 45])
            spawn_timer = 0

        # Cập nhật chướng ngại vật
        for obs in obstacles[:]:
            obs[1] += player_speed

            # Kiểm tra va chạm
            if obs[0] == current_lane:
                obs_rect = pygame.Rect(LANES[obs[0]] - obs[2]//2, obs[1], obs[2], obs[3])
                player_rect = pygame.Rect(LANES[current_lane] - PLAYER_WIDTH//2, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
                if obs_rect.colliderect(player_rect):
                    game_over = True

            # Ra khỏi màn hình
            if obs[1] > HEIGHT:
                obstacles.remove(obs)
                score += 100

    # Vẽ đường phân làn
    for x in [140, 260]:
        for y in range(0, HEIGHT, 30):
            pygame.draw.line(screen, LINE_COLOR, (x, y), (x, y + 15), 2)

    # Vẽ nhân vật
    player_x = LANES[current_lane] - PLAYER_WIDTH // 2
    if player_img:
        screen.blit(player_img, (player_x, player_y))
    else:
        pygame.draw.rect(screen, (0, 255, 204), (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    # Vẽ chướng ngại vật
    for obs in obstacles:
        obs_x = LANES[obs[0]] - obs[2] // 2
        pygame.draw.rect(screen, OBS_COLOR, (obs_x, obs[1], obs[2], obs[3]))

    # Hiển thị điểm số
    score_text = font.render(f"Điểm: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    # Màn hình thua
    if game_over:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))

        over_text = big_font.render("THUA RỒI!", True, OBS_COLOR)
        restart_text = font.render("Bấm phím bất kỳ để chơi lại", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()
    clock.tick(60)
