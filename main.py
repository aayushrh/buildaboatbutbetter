import random, pygame, time, sys, math

# Global Variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIN_W = 1270
WIN_H = 720
CAMSPED = 5
CHANCE = 5000

BLUE = (52, 222, 235)
BROWN = (196, 16, 116)
GREY = (87, 87, 87)

BLOCK_WIDTH = BLOCK_HEIGHT = 20

bg_group = pygame.sprite.Group()
anim_group = pygame.sprite.Group()

num_blocks = 5

class Anim(pygame.sprite.Sprite):
    def __init__(self, start_posx):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(start_posx, random.randint(0, WIN_H), random.randint(20, 100), 5)
        self.image = pygame.Surface((random.randint(20, 100), 5)).convert()
        self.image.fill(WHITE)
        self.speed = random.randint(round(CAMSPED) + 1, round(CAMSPED + 5))

    def update(self):
        self.rect.x += self.speed


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y ,image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x + WIN_W/2, y + WIN_W/2 - 275, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.otherrect = pygame.Rect(x, y, BLOCK_WIDTH * 2, BLOCK_HEIGHT * 2)
        self.image = image
        self.otherimage = pygame.transform.scale(image, (BLOCK_WIDTH * 2, BLOCK_HEIGHT * 2))

    def collide(self, therect, platform_group):
        ogrect = self.rect
        self.rect = therect
        for p in platform_group:
            if pygame.sprite.collide_rect(self, p):
                p.kill()
                self.kill()
        self.rect = ogrect

    def turn(self, dir):
        pass
        #angle = math.atan2(self.otherrect.centerx, self.otherrect.centery)
        #angle = angle + (dir/10)
        #hypot = math.sqrt(self.otherrect.centerx ** 2 + self.otherrect.centery ** 2)
        #if hypot >= 1:
            #self.otherrect.centerx = math.cos(angle) * hypot
            #self.otherrect.centerx = math.sin(angle) * hypot
        #else:
            #self.otherrect.centerx = math.cos(angle)
            #self.otherrect.centerx = math.sin(angle)


class Build():
    def __init__(self):
        self.blockgroup = pygame.sprite.Group()
        self.notusedblockgroup = pygame.sprite.Group()
        self.blocksused = 0

    def update(self, click):
        mouse_pos = pygame.mouse.get_pos()
        if click and self.blocksused < num_blocks:
            self.blocksused += 1
            new_block = Block(mouse_pos[0] - WIN_W/2, mouse_pos[1] - WIN_H/2, pygame.transform.scale(pygame.image.load("images/wood.png"), (BLOCK_WIDTH, BLOCK_HEIGHT)))
            self.blockgroup.add(new_block)
            new_blocku = Block(mouse_pos[0] - WIN_W/2, mouse_pos[1] - WIN_H/2, pygame.transform.scale(pygame.image.load("images/wood.png"), (BLOCK_WIDTH, BLOCK_HEIGHT)))
            self.notusedblockgroup.add(new_blocku)

    def reset(self):
        self.blocksused = 0

    def combine(self):
        self.blockgroup = self.notusedblockgroup
        for e in self.notusedblockgroup:
            e.kill()
        for b in self.blockgroup:
            new_blocku = Block(b.otherrect.x, b.otherrect.y, b.image)
            self.notusedblockgroup.add(new_blocku)

class Bg(pygame.sprite.Sprite):
    def __init__(self, x, color, width):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, 0, width, WIN_H)
        self.image = pygame.Surface((width, WIN_H)).convert()
        self.image.fill(color)

class Camera(object):
    def __init__(self, total_width, total_height):
        self.state = pygame.Rect(0, 0, total_width, total_height)
        self.cooldown = 150
        self.alivefor = 0
        self.currentcolor = BLUE
        self.lvlswitch = 1000
        self.lvlswitchcounter = 0

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def apply_rect(self, target_rect):
        return target_rect.move(self.state.topleft)

    def left(self):
        return (self.state.left) + (self.alivefor * CAMSPED)

    def reset(self):
        global CAMSPED
        global CHANCE
        self.state.x = 0
        self.state.y = 0
        self.cooldown = 150
        self.alivefor = 0
        CAMSPED = 5
        CHANCE = 5000

    def update(self, target_rect, platform_group):
        global num_blocks
        self.alivefor += 1
        self.state.x -= CAMSPED
        self.cooldown -= 1
        #new_bg = Bg(((self.state.right) + (self.alivefor * CAMSPED) * 2) - self.lvlswitch * CAMSPED, self.currentcolor, self.lvlswitch * CAMSPED)
        #bg_group.add(new_bg)
        new_bg = Bg((self.state.right) + (self.alivefor * CAMSPED) * 2, self.currentcolor, 2 * CAMSPED)
        bg_group.add(new_bg)
        if self.cooldown <= 0:
            self.lvlswitchcounter -= 1
            if self.lvlswitchcounter <= 0:
                num_blocks += 1
                r = random.randint(1, 4)
                if r == 1:
                    self.currentcolor = BLUE
                elif r == 2:
                    self.currentcolor = BLUE
                else:
                    self.currentcolor = BLUE
                self.lvlswitchcounter = self.lvlswitch
            for i in range(self.state.height):
                if random.randint(1, CHANCE) == 1:
                    new_platform = Platform((self.state.right) + (self.alivefor * CAMSPED) * 2, i, 0)
                    platform_group.add(new_platform)



class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 1
        self.image = pygame.transform.scale(pygame.image.load("images\player.png"), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.centery += WIN_H/2
        self.rect.x = 2 * 10
        self.health = 1

    def reset(self):
        self.rect.centery = WIN_H/2
        self.rect.x = 2 * 10
        self.health = 1

    def collide(self, platform_group):
        for p in platform_group:
            if pygame.sprite.collide_rect(self, p):
                platform_group.remove(p)
                self.health -= 1

    def update(self, platform_group, hero):
        # Movement
        self.rect.x += CAMSPED
        key = pygame.key.get_pressed()
        self.collide(platform_group)

        # Movement and barriers
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.rect.y -= self.speed
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            self.rect.y += self.speed
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.rect.x += self.speed


# Function#
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, col):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("images\spike.png"), (32, 32))
        self.image.convert()
        self.col = col
        self.rect = pygame.Rect(x, y, 32, 32)


def main():
    global CAMSPED
    global CHANCE
    global bg_group

    # variables
    screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)

    hero = Hero()

    platform_group = pygame.sprite.Group()
    total_width = 30*20*5
    total_height = WIN_H
    camera = Camera(total_width, total_height)

    play = False
    build = True
    clock = pygame.time.Clock()
    fps = 60
    left = False
    right = False
    ship = Build()
    while True:
        screen.fill(WHITE)
        if build:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        play = True
                        build = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True

            screen.blit(pygame.transform.scale(pygame.image.load("images\player.png"), (30, 30)), (WIN_W/2 - 30, WIN_H/2 - 30))

            ship.update(click)
            ship.notusedblockgroup.draw(screen)

        elif play:
            # Checks if window exit button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_o:
                        left = True
                    elif event.key == pygame.K_p:
                        right = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_o:
                        left = False
                    elif event.key == pygame.K_p:
                        right = False
            if left:
                for c in ship.blockgroup:
                    c.turn(-1)
            elif right:
                for c in ship.blockgroup:
                    c.turn(1)

            if random.randint(1, 25) == 1:
                new_anim = Anim(camera.left())
                anim_group.add(new_anim)

            # Update
            hero.update(platform_group, hero)
            camera.update(hero.rect, platform_group)
            anim_group.update()

            CAMSPED += 0.001
            CHANCE -= 1

            # Blits
            #screen.fill(WHITE)
            for b in bg_group:
                screen.blit(b.image, camera.apply(b))
            for a in anim_group:
                screen.blit(a.image, camera.apply(a))
            screen.blit(hero.image, camera.apply(hero))
            for p in platform_group:
                screen.blit(p.image, camera.apply(p))
            for c in ship.blockgroup:
                c_rect = pygame.Rect(hero.rect.centerx + c.otherrect.centerx, hero.rect.centery + c.otherrect.centery, c.otherrect.width, c.otherrect.height)
                screen.blit(c.image, camera.apply_rect(c_rect))
                c.collide(c_rect, platform_group)

            if hero.health <= 0:
                hero.reset()
                camera.reset()
                ship.reset()
                for p in platform_group:
                    p.kill()
                for a in anim_group:
                    a.kill()
                for b in bg_group:
                    b.kill()
                build = True
                play = False
                ship.combine()

        # Limits FPS
        clock.tick(fps)
        # Writes to surface
        pygame.display.flip()


main()
