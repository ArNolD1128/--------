import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ашот: Проклятый Лаваш")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Класс игрока (Ашота)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Загрузка изображений для анимации
        self.idle_img = pygame.Surface((50, 80))
        self.idle_img.fill(GREEN)  # Заглушка вместо спрайта
        self.run_imgs = [pygame.Surface((50, 80)) for _ in range(4)]  # Список "кадров" бега
        for img in self.run_imgs:
            img.fill(RED)
        
        self.current_img = self.idle_img
        self.image = self.current_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Физика
        self.velocity_y = 0
        self.jumping = False
        self.on_ground = False
        self.speed = 5
        self.jump_power = -15
        
        # Анимация
        self.frame_index = 0
        self.animation_speed = 0.15
        self.facing_right = True
        
    def update(self, platforms):
        # Гравитация
        self.velocity_y += 0.8
        if self.velocity_y > 10:
            self.velocity_y = 10
        
        # Движение по горизонтали
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.facing_right = True
        
        # Прыжок
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
        
        # Обновление позиции по Y
        self.rect.y += self.velocity_y
        
        # Коллизия с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Если падаем вниз и касаемся платформы
                if self.velocity_y > 0 and self.rect.bottom > platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                # Если прыгаем вверх и ударяемся головой
                elif self.velocity_y < 0 and self.rect.top < platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        
        # Анимация
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.run_imgs):
                self.frame_index = 0
            self.current_img = self.run_imgs[int(self.frame_index)]
        else:
            self.current_img = self.idle_img
        
        # Отражение спрайта, если повернулись
        if not self.facing_right:
            self.image = pygame.transform.flip(self.current_img, True, False)
        else:
            self.image = self.current_img

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Создание спрайтов
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Игрок
player = Player(100, 300)
all_sprites.add(player)

# Платформы
ground = Platform(0, 550, 800, 50)
platform1 = Platform(200, 450, 200, 20)
platform2 = Platform(500, 350, 200, 20)

platforms.add(ground, platform1, platform2)
all_sprites.add(ground, platform1, platform2)

# Игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Обновление
    player.update(platforms)
    
    # Отрисовка
    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()