# okno główne
import pygame, os
SIZESCREEN = WIDTH, HEIGHT = 1320, 900


# kolory
DARKGREEN = pygame.color.THECOLORS['darkgreen']
LIGHTBLUE = pygame.color.THECOLORS['lightblue']


screen = pygame.display.set_mode(SIZESCREEN)

# grafika  - wczytywanie grafik
path = os.path.join(os.pardir, 'images')

file_names = sorted(os.listdir(path))
file_names.remove('background.png')
BACKGROUND = pygame.image.load(os.path.join(path, 'background.png')).convert()
for file_name in file_names:
    image_name = file_name[:-4].upper()
    globals()[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)

PLAYER_WALK_LIST_R = [PLAYER_STAND_R, PLAYER_WALK_R1, PLAYER_WALK_R2]
PLAYER_WALK_LIST_L = [PLAYER_STAND_L, PLAYER_WALK_L1, PLAYER_WALK_L2]
PLAYER_WALK_LIST_U = [PLAYER_STAND_U, PLAYER_WALK_U1, PLAYER_WALK_U2]
PLAYER_WALK_LIST_D = [PLAYER_STAND, PLAYER_WALK_D1, PLAYER_WALK_D2]

# PLAYER_WALK_LIST_R = [XAYOP, XAYOP, XAYOP]
# PLAYER_WALK_LIST_L = [XAYO, XAYO, XAYO]
# PLAYER_WALK_LIST_U = [XAYO, XAYO, XAYO]
# PLAYER_WALK_LIST_D = [XAYOP, XAYOP, XAYOP]


TERRAIN_LIST = [BUTLA, PARCEL, KAMIEN, SENZU]
DEAD_BODIES = [GOKU_DEAD]
BUTTONS = [RESET_BUTTON]
DRAGON_G = [SMOK_G1, SMOK_G2, SMOK_G3]
DRAGON_D = [SMOK_D1, SMOK_D2, SMOK_D3]
DRAGON_L = [SMOK_L1, SMOK_L2, SMOK_L3]
DRAGON_R = [SMOK_R1, SMOK_R2, SMOK_R3]

# DRAGON_G = [LEWUS, LEWUS, LEWUS]
# DRAGON_D = [LEWUS, LEWUS, LEWUS]
# DRAGON_L = [LEWUS, LEWUS, LEWUS]
# DRAGON_R = [LEWUS, LEWUS, LEWUS]

BULLET = [BULLET, BULLET1]
