import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Hunter")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

WHITE = (255, 255, 255)
RED = (255, 50, 50)

clock = pygame.time.Clock()
FPS = 60

# ================= ASSET =================
player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (40, 40))

coin_sound = pygame.mixer.Sound("coin.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

# ================= CLASS =================
class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, (0,0,0), self.rect)

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
        self.speed = 5
        self.score = 0
        self.lives = 3
        self.image = player_img

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class Enemy(GameObject):
    def __init__(self, level):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-100, -40)
        super().__init__(x, y, 40, 40)
        self.speed = random.randint(2, 3) + level

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 40)
            self.rect.y = random.randint(-100, -40)

class Coin(GameObject):
    def __init__(self):
        x = random.randint(0, WIDTH - 20)
        y = random.randint(0, HEIGHT - 20)
        super().__init__(x, y, 20, 20)

    def draw(self):
        pygame.draw.circle(screen, (255, 215, 0), self.rect.center, 10)

# ================= RESET =================
def reset_game():
    player = Player(400, 300)
    enemies = []
    coin = Coin()
    level = 1
    return player, enemies, coin, level

stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(50)]

def draw_background():
    for y in range(HEIGHT):
        color = (135, 206, 235 - int(y * 0.2))
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    for star in stars:
        star[1] += 1
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0

        pygame.draw.circle(screen, (255, 255, 255), star, 2)

# ================= MAIN =================
def main():
    state = "menu"
    player, enemies, coin, level = reset_game()

    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 60)

    running = True
    game_over_time = 0

    while running:
        clock.tick(FPS)
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # ===== MENU =====
        if state == "menu":
            title = big_font.render("COIN HUNTER", True, (0,0,0))
            start = font.render("Press SPACE to Start", True, (0,0,0))

            screen.blit(title, (WIDTH//2 - 150, 200))
            screen.blit(start, (WIDTH//2 - 150, 300))

            if keys[pygame.K_SPACE]:
                state = "game"

        # ===== GAME =====
        elif state == "game":
            player.move(keys)

            # spawn musuh sesuai level
            if len(enemies) < level + 2:
                enemies.append(Enemy(level))

            for enemy in enemies:
                enemy.move()

                if player.rect.colliderect(enemy.rect):
                    hit_sound.play()
                    player.lives -= 1
                    enemy.rect.y = -50

            # ambil coin
            if player.rect.colliderect(coin.rect):
                coin_sound.play()
                player.score += 1
                coin = Coin()

                if player.score % 5 == 0:
                    level += 1

            # game over
            if player.lives <= 0:
                state = "gameover"
                game_over_time = pygame.time.get_ticks()

            # draw
            player.draw()
            for enemy in enemies:
                enemy.draw()
            coin.draw()

            screen.blit(font.render(f"Score: {player.score}", True, (0,0,0)), (10,10))
            screen.blit(font.render(f"Lives: {player.lives}", True, (0,0,0)), (10,40))
            screen.blit(font.render(f"Level: {level}", True, (0,0,0)), (10,70))

        # ===== GAME OVER =====
        elif state == "gameover":
            text = big_font.render("GAME OVER", True, RED)
            screen.blit(text, (WIDTH//2 - 150, 200))

            if pygame.time.get_ticks() - game_over_time > 2000:
                restart = font.render("Press R to Restart", True, (0,0,0))
                screen.blit(restart, (WIDTH//2 - 150, 300))

                if keys[pygame.K_r]:
                    player, enemies, coin, level = reset_game()
                    state = "menu"
            else:
                wait = font.render("Wait 2 seconds...", True, (0,0,0))
                screen.blit(wait, (WIDTH//2 - 150, 300))

        # ===== EXIT =====
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
