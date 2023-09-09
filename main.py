############
# K-RE-DAS #
############
# Author = Gilles Aubin
# Website = gilles-aubin.net
# Version = 1.4.0
#
# multi langues
# orientation horizontale
# bug de sélection sur les bords
# affichage des symboles restants
# combos
# coupure son

# Délai avant recap


import sys
import pygame
import random
import json
import math
import webbrowser

from enum import Enum

pygame.init()
pygame.mixer.init()


#############
# VARIABLES #
#############

debug = True #>>>> CHANGE AVANT DE PUBLIER <<<<#

game_title = "K-RE-DAS"
pygame.display.set_caption(game_title)

game_author = "Gilles Aubin"
game_url = "https://studiocurieux.itch.io/K-RE-DAS"
score = 0
window_size = (1280, 720)
window = pygame.display.set_mode(window_size)
demi_ecran = window_size[0] // 2

# Délai d'affichage du Splash Screen
delai_screen = 4000

# Polices de caractères
jetLight = "font/JetBrainsMono-Light.ttf"
jetBold = "font/JetBrainsMono-Bold.ttf"
jetExtraBold = "font/JetBrainsMono-ExtraBold.ttf"

# Couleurs
noir = (0, 0, 0)
blanc = (204, 204, 204)
vert = (0, 86, 52)

# Position des éléments
logoKredasX = 10
logoKredasY = 10
imageCartesX = 0
imageCartesY = 500

posTxtBestScoreX = 50
posTxtBestScoreY = 225
posBestScoreX = 100
posBestScoreY = 250

posNivX = 275
posNivY = 225
posScoreX = 290
posScoreY = 250

posTxtResteX = 445
posTxtResteY = 225
posResteX = 460
posResteY = 250

posOverlayX = 900
posOverlayY = 360


##############################
# CONFIGURATION DE LA GRILLE #
##############################

colignes = [10,10] # Taille de la grille

grid_width = 500  # Largeur de la grille
grid_height = 500  # Hauteur de la grille

cell_size = grid_width // colignes[1] # Largeur des cellules

# Coordonnées de la grille
grid_x = 655
grid_y = 115

pos_contourX = grid_x - 50
pos_contourY = grid_y - 50


##########
# IMAGES #
##########

def load_image(filename):
    try:
        return pygame.image.load(filename)
    except pygame.error:
        sys.exit()

game_image = load_image('img/tapis.jpg')
logo_studio = load_image('img/logo_studiocurieux.png')
logo_kredas = load_image('img/logo_kredas.png')
image_cartes = load_image('img/4as.png')
flag_en = load_image('img/flag_en.png')
flag_fr = load_image('img/flag_fr.png')
obstacle_image = load_image('img/obstacle.png')
fond_pc = load_image('img/fond_pc.jpg')
contour_table = load_image('img/contour_table.png')
soundControlON = load_image('img/sound-max.png')
soundControlOFF = load_image('img/sound-mute.png')

overlay_S = load_image('img/S-Combo.png')
overlay_M = load_image('img/M-Master.png')
overlay_XL = load_image('img/XL-Awesome.png')

symbols = {
    "pique": load_image('img/pique.png'),
    "carreau": load_image('img/carreau.png'),
    "coeur": load_image('img/coeur.png'),
    "trefle": load_image('img/trefle.png')
}
symbols_on = {
    "pique": load_image('img/pique_on.png'),
    "carreau": load_image('img/carreau_on.png'),
    "coeur": load_image('img/coeur_on.png'),
    "trefle": load_image('img/trefle_on.png')
}

logoKRDLarg = logo_kredas.get_width()
contourLarg = contour_table.get_width()
margeHRZ = (window_size[0] - (logoKRDLarg+contourLarg)) / 3


###########
# LANGUES #
###########

def load_language(language="fr_FR"):
    global help_texts, ui_texts, end_texts  # Dictionnaires utilisé dans les fichiers de langues
    if language == "en_US":
        from languages import en_US as lang_module
    elif language == "fr_FR":
        from languages import fr_FR as lang_module
    else:
        from languages import en_US as lang_module  # Langue par défaut

    help_texts = lang_module.help_texts
    ui_texts = lang_module.ui_texts
    end_texts = lang_module.end_texts

    return language

load_language()


########
# SONS #
########

soundState = True
volume_FX = 0.5
volume_ambiance = 0.5

if debug :
    volume_FX = 0
    volume_ambiance = 0

def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except pygame.error:
        sys.exit()

ambiance_music = pygame.mixer.music.load("sons/ambiance.wav")
swap_sound = load_sound("sons/swap.ogg")
aligner_sound = load_sound("sons/aligner.ogg")

pygame.mixer.music.play(-1)  # Le -1 signifie que la musique sera jouée en boucle indéfiniment
pygame.mixer.music.set_volume(volume_ambiance)


#############
# FONCTIONS #
#############

# >>>>>> MODE DEBUG
def modeDebug():
    if debug:
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        # Afficher les coordonnées de la souris
        coords_text = f"X: {mouse_x}, Y: {mouse_y}"
        font = pygame.font.Font(jetBold, 20)  # Remplacez 'jetBold' par le chemin vers votre police si nécessaire
        text_surface = font.render(coords_text, True, (255, 255, 255))
        window.blit(text_surface, (5, 5))

        # Dessiner un réticule en forme de croix
        reticule_size = 2000  # Taille du réticule (longueur des lignes)

        # Dessiner les lignes horizontales et verticales
        pygame.draw.line(window, blanc, (mouse_x - reticule_size, mouse_y), (mouse_x + reticule_size, mouse_y), 2)
        pygame.draw.line(window, blanc, (mouse_x, mouse_y - reticule_size), (mouse_x, mouse_y + reticule_size), 2)

        pygame.display.flip()

def ecrire(champ_texte, taille_texte, police, couleur, posX, posY, align="left", ecran="ui"):
    font = pygame.font.Font(police, taille_texte)

    if champ_texte == game_title or champ_texte == game_url or champ_texte == game_author or champ_texte == high_score or champ_texte == score:
        text_surface = font.render(champ_texte, True, couleur)
    elif ecran == "help":
        text_surface = font.render(help_texts[champ_texte], True, couleur)
    elif ecran == "end":
        text_surface = font.render(end_texts[champ_texte].upper(), True, couleur)
    elif ecran == "ui":
        text_surface = font.render(ui_texts[champ_texte], True, couleur)
    text_width, text_height = text_surface.get_size()
  
    if align == "center":
        posX = (window_size[0] - text_width) // 2
    elif align == "right":
        posX = window_size[0] - text_width - posX

    window.blit(text_surface, (posX, posY))

def place_image(nom_image, posX, posY, position="left"):
    if position == "center":
        posX = (window_size[0] - nom_image.get_width()) // 2
    elif position == "right":
        posX = window_size[0] - nom_image.get_width() - posX

    window.blit(nom_image, (posX, posY))

# >>>>>> GENERATEUR DE BOUTON
BTNlarg = 150
BTNhaut = 40
BTNcentre = (margeHRZ + logoKRDLarg/2) - BTNlarg/2

textHighScore_X = demi_ecran - (BTNlarg /2)
textHighScore_Y = 300

buttons = {
    'BTN_EN': pygame.Rect(425, 360, 48, 34),
    'BTN_FR': pygame.Rect(850, 360, 48, 34),
    'BTN_SOUND': pygame.Rect(150, 350, 34, 34),
    'BTN_NEW': pygame.Rect(BTNcentre, 350, BTNlarg, BTNhaut),
    'BTN_HELP': pygame.Rect(BTNcentre, 400, BTNlarg, BTNhaut),
    'BTN_QUIT': pygame.Rect(BTNcentre, 450, BTNlarg, BTNhaut),
    'BTN_CLOSE': pygame.Rect(demi_ecran - BTNlarg /2, 570, BTNlarg, BTNhaut),
    'BTN_RETRY': pygame.Rect(demi_ecran - BTNlarg * 1.5, 470, BTNlarg, BTNhaut),
    'BTN_NEXT': pygame.Rect(demi_ecran + BTNlarg/2, 470, BTNlarg, BTNhaut),
}

def draw_button(CARAC_BTN, text_size, text_button=None) :
    if text_button is not None:
        bouton = buttons[CARAC_BTN]
        font = pygame.font.Font(jetBold, text_size)
        text = font.render(ui_texts[text_button], True, blanc)
        window.blit(text, (buttons[CARAC_BTN].left + 10, buttons[CARAC_BTN].top + 5))

        if bouton.collidepoint(mouse_pos):
            bouton = pygame.draw.rect(window, noir, buttons[CARAC_BTN])
            text = font.render(ui_texts[text_button], True, blanc)
            window.blit(text, (buttons[CARAC_BTN].left + 10, buttons[CARAC_BTN].top + 5))
        else:
            bouton = pygame.draw.rect(window, blanc, buttons[CARAC_BTN], 1)
            text = font.render(ui_texts[text_button], True, blanc)
            window.blit(text, (buttons[CARAC_BTN].left + 10, buttons[CARAC_BTN].top + 5))

        pygame.draw.rect(window, blanc, buttons[CARAC_BTN], 1)

def click_on_button(CARAC_BTN):
    mouse_pos = pygame.mouse.get_pos()
    if CARAC_BTN in buttons:
        if buttons[CARAC_BTN].left < mouse_pos[0] < (buttons[CARAC_BTN].left + buttons[CARAC_BTN].width) and buttons[CARAC_BTN].top < mouse_pos[1] < (buttons[CARAC_BTN].top + buttons[CARAC_BTN].height):
            return True
        return False

# Animation des combos
def animate_overlay(overlay_image):
    frames = 5  # nombre de frames entre deux images clés
    delay = 5  # durée de chaque frame en ms (500 ms = 15 frames * 33 ms)

    # image clé 1 > image clé 2
    for i in range(frames + 1):
        factor = i / frames
        scale_factor = 0.2 + 0.8 * factor
        alpha = int(255 * factor)

        animate_frame(overlay_image, scale_factor, alpha)
        pygame.time.wait(delay)

    # Pause image clé 2 de 500 ms
    animate_frame(overlay_image, 1, 255)
    pygame.time.wait(500)

    # image clé 2 > image clé 3
    for i in range(frames, -1, -1):
        factor = i / frames
        scale_factor = 0.2 + 0.8 * factor
        alpha = int(255 * factor)

        animate_frame(overlay_image, scale_factor, alpha)
        pygame.time.wait(delay)

def animate_frame(overlay_image, scale_factor, alpha):
    width, height = overlay_image.get_size()
    scaled_image = pygame.transform.scale(overlay_image, (int(width * scale_factor), int(height * scale_factor)))
    scaled_image.set_alpha(alpha)

    x = posOverlayX - scaled_image.get_width() // 2
    y = posOverlayY - scaled_image.get_height() // 2

    window.blit(fond_pc, (0, 0))
    poseDecor()
    poseUI()
    show_remaining()
    draw_grid(grid, positions, symbols, cell_size, window, colignes[0], colignes[1], selected_pos1, selected_pos2, to_delete)
    window.blit(scaled_image, (x, y))
    pygame.display.flip()


###########
# NIVEAUX #
###########

if modeDebug:
    ConfigJSON = "config_debug.json"
else:
    ConfigJSON = "config.json"

def load_config_data():     
    try:
        with open('config/' + ConfigJSON, 'r') as file:
            data = json.load(file)

            if not any(level.get('progression', 0) == 1 for level in data['config']):
                data['config'][0]['progression'] = 1

            return data

    except (FileNotFoundError, json.JSONDecodeError):
        sys.exit()

config_data = load_config_data()

def load_progress(config_data):
    if config_data:
        levels_with_progression = [
            level for level in config_data.get('config', []) 
            if level.get('progression') == 1
        ]
        if levels_with_progression:
            return levels_with_progression[0]
        else:
            return config_data.get('config', [{}])[0]
    else:
        return {}

# Chargement des données de progression
current_level = load_progress(config_data)

levelToPlay = current_level['level']
current_objectif = current_level['objectif'] - len(current_level['obstacles'])
current_progress = current_level['progression']
current_meilleurScore = current_level['meilleurScore']
current_obstacles = current_level['obstacles']

def save_config_data(config_data):
    with open('config/' + ConfigJSON, 'w') as file:
        json.dump(config_data, file, indent=4)


# Calculer le nombre initial de symboles
initial_symbols = (colignes[0] * colignes[1])

def load_next_level():
    global levelToPlay, current_level, current_objectif, current_meilleurScore, high_score

    draw_recap_screen()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_on_button("BTN_RETRY"):
                    reset_game()
                    high_score = update_high_score()
                    waiting_for_input = False

                elif click_on_button("BTN_NEXT"):
                    if levelToPlay < len(config_data['config']):
                        levelToPlay += 1
                        save_progress(config_data)
                    else:
                        save_progress(config_data)
                        show_endgame_screen()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if click_on_button("BTN_CLOSE"):
                                        levelToPlay = 1
                                        reset_game()
                                        return

                    current_level = config_data['config'][levelToPlay-1]
                    current_objectif = current_level['objectif'] - len(current_level['obstacles'])
                    current_meilleurScore = current_level['meilleurScore']
                    high_score = current_meilleurScore
                    reset_game()
                    waiting_for_input = False


#########
# SCORE #
#########

def get_high_score():
    global config_data
    return current_level['meilleurScore']

high_score = get_high_score()

def update_high_score():
    global high_score, score, config_data

    if score > current_level['meilleurScore']:
        current_level['meilleurScore'] = score
        save_config_data(config_data)

    return current_level['meilleurScore']

def reset_game():
    global config_data, grid, score, symboles_suppr
    grid = initialize_grid(colignes[0], colignes[1])
    score = 0
    symboles_suppr = 0
    return grid, score

def save_progress(config_data):
    for level in config_data['config']:
        level['progression'] = 0

    if levelToPlay == 1:
        config_data['config'][0]['progression'] = 1
    else:
        config_data['config'][levelToPlay-1]['progression'] = 1

    save_config_data(config_data)

def count_remaining_symbols(grid, level_obstacles):
    count = 0
    for row in grid:
        for cell in row:
            if cell in symbols.keys():  # Vérifier si la cellule contient un symbole
                count += 1
    count += level_obstacles
    return count

def show_remaining():
    remaining_symbols = count_remaining_symbols(grid, len(current_level['obstacles']))
    toGoal = initial_symbols - remaining_symbols
    remaining_to_goal = current_level['objectif'] - toGoal

    ecrire("ui_left", 20, jetBold, blanc, posTxtResteX, posTxtResteY, align="left",ecran="ui")

    font = pygame.font.Font(jetBold, 32)
    toGoal_text = font.render(f"{remaining_to_goal}", True, blanc)
    window.blit(toGoal_text, (posResteX, posResteY))


#########################
# INITIALISER LA GRILLE #
#########################

def initialize_grid(rows, columns):
    grid = []
    symbol_counts = {"pique": 0, "carreau": 0, "coeur": 0, "trefle": 0}
    remaining_symbols = {"pique": 0, "carreau": 0, "coeur": 0, "trefle": 0}
    symbols_list = list(symbol_counts.keys())
    max_count = (rows * columns) // len(symbols_list)

    for i in range(rows):
        row = []
        for j in range(columns):
            # Check if current position is an obstacle
            if any(obstacle['row'] == i and obstacle['col'] == j for obstacle in current_level['obstacles']):
                row.append('obstacle')
            else:
                # Choose a symbol that hasn't reached its maximum count
                available_symbols = [symbol for symbol in symbols_list if symbol_counts[symbol] < max_count]
                chosen_symbol = random.choice(available_symbols)
                row.append(chosen_symbol)
                symbol_counts[chosen_symbol] += 1  # Increment the count for the chosen symbol
        grid.append(row)
    return grid

grid = initialize_grid(*colignes)

positions = []
for i in range(colignes[0]):
    row = []
    for j in range(colignes[1]):
        # La position initiale est basée sur l'indice de la cellule
        row.append((grid_x + j * cell_size, grid_y + i * cell_size))
    positions.append(row)

def update_game_state():
    save_progress(config_data)
    update_high_score()

def handle_level_completion():
    save_progress(config_data)
    update_high_score()
    # pygame.time.delay(1000)
    load_next_level()


###############
# ALIGNEMENTS #
###############

def check_alignments(grid):
    global score

    cells_to_delete_for_objective = set()
    cells_to_delete_for_score = []

    rows, cols = len(grid), len(grid[0])

    for i in range(rows):
        for j in range(cols):

            if j <= rows - 4:
                k = 0
                while j + k + 1 < rows and grid[i][j] is not None and grid[i][j] == grid[i][j + k + 1]:
                    k += 1
                if k >= 3:
                    for l in range(k + 1):
                        cells_to_delete_for_objective.add((i, j + l))
                        cells_to_delete_for_score.append((i, j + l))
                    score += 4

            if i <= cols - 4:
                k = 0
                while i + k + 1 < cols and grid[i][j] is not None and grid[i][j] == grid[i + k + 1][j]:
                    k += 1
                if k >= 3:
                    for l in range(k + 1):
                        cells_to_delete_for_objective.add((i + l, j))
                        cells_to_delete_for_score.append((i + l, j))
                    score += 4

    return list(cells_to_delete_for_objective), cells_to_delete_for_score

# Fonction d'animation des échanges de symboles
def lerp(start, end, factor):
    return (1 - factor) * start + factor * end


######################
# DESSINER LA GRILLE #
######################

window = pygame.display.set_mode(window_size)

def draw_grid(grid, positions, symbols, cell_size, window, rows, cols, selected_pos1=None, selected_pos2=None, to_delete=None):
    obstacle_size = obstacle_image.get_size()
    to_delete_set = set(to_delete) if to_delete else set()
    selected_positions = {selected_pos1, selected_pos2}

    for i in range(rows):
        for j in range(cols):
            symbol = grid[i][j]
            pos = positions[i][j]

            if symbol == 'obstacle':
                centered_obstacle_pos = (pos[0] + cell_size // 2 - obstacle_size[0] // 2, pos[1] + cell_size // 2 - obstacle_size[1] // 2)
                window.blit(obstacle_image, centered_obstacle_pos)
                continue

            if symbol is not None:
                symbol_size = symbols[symbol].get_size()
                centered_pos = (pos[0] + cell_size // 2 - symbol_size[0] // 2, pos[1] + cell_size // 2 - symbol_size[1] // 2)

                if (i, j) in selected_positions:
                    window.blit(symbols_on[symbol], centered_pos)
                else:
                    window.blit(symbols[symbol], centered_pos)


##########
# ECRANS #
##########

def show_language_screen():
    window.blit(fond_pc, (0, 0))
    place_image(flag_en, buttons["BTN_EN"].x, buttons["BTN_EN"].y)
    place_image(flag_fr, buttons["BTN_FR"].x, buttons["BTN_FR"].y)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if click_on_button("BTN_EN"):
                    load_language("en_US")
                    waiting_for_input = False
                elif click_on_button("BTN_FR"):
                    load_language("fr_FR")
                    waiting_for_input = False

def show_splashscreen():
    window.blit(fond_pc, (0, 0))
    place_image(logo_studio, 50, 50, position="center")
    ecrire("ui_present", 22, jetBold, blanc, 50, 120, align="center")
    place_image(logo_kredas, demi_ecran, 260, position="center")
    place_image(image_cartes, imageCartesX, imageCartesY)

    pygame.display.flip()
    pygame.time.wait(delai_screen)

def show_help_screen():
    window.blit(fond_pc, (0, 0))

    ecrire("help_how", 24, jetBold, blanc, 100, 80, align="center", ecran="help")
    place_image(logo_kredas, logoKredasX, 120, position="center")
    ecrire("help_rule1line1", 22, jetBold, blanc, 50, 270, align="center", ecran="help")
    ecrire("help_rule1line2", 22, jetBold, blanc, 50, 300, align="center", ecran="help")
    ecrire("help_rule2line1", 22, jetBold, blanc, 50, 330, align="center", ecran="help")
    ecrire("help_rule2line2", 22, jetBold, blanc, 50, 400, align="center", ecran="help")
    ecrire("help_rule3line1", 22, jetBold, blanc, 50, 470, align="center", ecran="help")
    ecrire("help_rule3line2", 22, jetBold, blanc, 50, 500, align="center", ecran="help")

    draw_button("BTN_CLOSE", 20, "ui_close")
    place_image(image_cartes, imageCartesX, imageCartesY)

    if help_texts["help_lang"] == "US":
        place_image(obstacle_image, 750, 465)
    elif  help_texts["help_lang"] == "FR":
        place_image(obstacle_image, 820, 475)

    pygame.display.flip()

def draw_recap_screen():

    window.blit(fond_pc, (0, 0))
    font = pygame.font.Font(jetBold, 40)
    place_image(logo_kredas, logoKredasX, 120, position="center")

    score_text = font.render(f"{score}", True, blanc)
    ecrire("ui_score", 20, jetBold, blanc, demi_ecran - 180, 280, align="left",ecran="ui")
    window.blit(score_text, (demi_ecran - 200 + 20, 330))

    highscore_text = font.render(f"{high_score}", True, blanc)
    ecrire("ui_best", 20, jetBold, blanc, demi_ecran + 60, 280, align="left",ecran="ui")
    window.blit(highscore_text, (demi_ecran + 120, 330))

    place_image(image_cartes, imageCartesX, imageCartesY)

    draw_button("BTN_RETRY", 20, "ui_retry")
    draw_button("BTN_NEXT", 20, "ui_next")

    pygame.display.flip()

def show_endgame_screen():
    global jetBold

    window.blit(fond_pc, (0, 0))

    ecrire("end_well", 70, jetBold, blanc, 50, 105, align="center",ecran="end")
    ecrire("end_completed", 22, jetBold, blanc, 50, 185, align="center",ecran="end")
    ecrire("end_work", 22, jetBold, blanc, 50, 255, align="center",ecran="end")
    ecrire("end_share", 22, jetBold, blanc, 50, 285, align="center",ecran="end")
    place_image(logo_kredas, 415, 355)
    ecrire(game_url, 22, jetBold, blanc, 50, 525, align="center",ecran="end")
    draw_button("BTN_CLOSE", 20, "ui_close")
    place_image(image_cartes, imageCartesX, imageCartesY)

    pygame.display.flip()

def poseDecor():
    fond = pygame.transform.scale(game_image, window_size)
    window.blit(fond,(0,0))
    place_image(logo_kredas, 63, 65)
    place_image(image_cartes, imageCartesX, imageCartesY)
    place_image(contour_table, pos_contourX, pos_contourY)

def poseUI():
    fontLevel = pygame.font.Font(jetBold, 20)
    textLevel = fontLevel.render(f"{ui_texts['ui_level']} {levelToPlay:02}", True, blanc)
    window.blit(textLevel, (posNivX, posNivY))

    ecrire("ui_best", 20, jetBold, blanc, posTxtBestScoreX, posTxtBestScoreY, align="left",ecran="ui")
    fontHighScore = pygame.font.Font(jetBold, 32)
    textHighScore = fontHighScore.render(f"{high_score:04}", True, blanc)
    window.blit(textHighScore, (posBestScoreX, posBestScoreY))

    fontScore = pygame.font.Font(jetBold, 32)
    textScore = fontScore.render(f"{score:04}", True, blanc)
    window.blit(textScore, (posScoreX, posScoreY))

    if soundState : 
        place_image(soundControlON, buttons["BTN_SOUND"].x, buttons["BTN_SOUND"].y)
    else:
        place_image(soundControlOFF, buttons["BTN_SOUND"].x, buttons["BTN_SOUND"].y)
 
    draw_button("BTN_NEW", 20, "ui_new")
    draw_button("BTN_HELP", 20, "ui_help")
    draw_button("BTN_QUIT", 20, "ui_quit")


####################
# LANCEMENT DU JEU #
####################

if debug is not True :
    show_splashscreen()
    show_language_screen()

class GameState(Enum):
    PLAYING = 1
    RECAP = 2
    HELP = 3
    ENDGAME = 4

current_state = GameState.PLAYING

selected_symbol1 = None
selected_pos1 = None
selected_symbol2 = None
selected_pos2 = None

running = True
showing_help = False
showing_endgame = False

symboles_suppr = 0

#####################
# BOUCLE PRINCIPALE #
#####################

while running:
    if current_state == GameState.PLAYING:
        mouse_pos = pygame.mouse.get_pos()

        modeDebug()
        poseDecor()
        poseUI()
        show_remaining()

        to_delete = []

        draw_grid(grid, positions, symbols, cell_size, window, colignes[0], colignes[1], selected_pos1, selected_pos2, to_delete)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if click_on_button("BTN_SOUND"):
                    if soundState : 
                        volume_FX = 0
                        volume_ambiance = 0
                        soundState = False
                    else:
                        volume_FX = 0.5
                        volume_ambiance = 0.5
                        soundState = True

                pygame.mixer.music.set_volume(volume_ambiance)
                swap_sound.set_volume(volume_FX)
                aligner_sound.set_volume(volume_FX)

                if click_on_button("BTN_NEW"):
                    update_game_state()
                    reset_game()

                if click_on_button("BTN_HELP"):
                    current_state = GameState.HELP

                if click_on_button("BTN_QUIT"):
                    update_game_state()
                    running = False

                cell_x = (mouse_pos[0] - grid_x) // cell_size
                cell_y = (mouse_pos[1] - grid_y) // cell_size

                # Inversion de symboles
                if 0 <= cell_x < colignes[0] and 0 <= cell_y < colignes[1] and grid[cell_y][cell_x] is not None:
                    if grid[cell_y][cell_x] == 'obstacle':  # Si obstacle, ignore sélection
                        continue

                    if selected_symbol1 is None:
                        selected_symbol1 = grid[cell_y][cell_x]
                        selected_pos1 = (cell_y, cell_x)

                    else:
                        selected_pos1_converted = (selected_pos1[1], selected_pos1[0])  # Convertit en (X, Y)

                        if (cell_x, cell_y) != selected_pos1_converted:
                            selected_symbol2 = grid[cell_y][cell_x]
                            selected_pos2 = (cell_y, cell_x)

                        # Animation de l'échange
                        vitessEchange = 10 # plus petit = plus rapide
                        swap_sound.set_volume(volume_FX)
                        swap_sound.play()

                        for _ in range(vitessEchange):
                            window.blit(fond_pc, (0, 0))

                            poseDecor()
                            poseUI()
                            show_remaining()

                            # 2. Dessiner les éléments
                            factor = _ / vitessEchange

                            # Pour pos1_x
                            pos1_1 = positions[selected_pos1[0]][selected_pos1[1]]
                            if selected_pos2 is not None:                            
                                pos2_1 = positions[selected_pos2[0]][selected_pos2[1]]
                                pos1_x = lerp(pos1_1[0], pos2_1[0], factor)
                            else:
                                continue
                            pos1_y = lerp(pos1_1[1], pos2_1[1], factor)

                            # Pour pos2_x
                            pos1_2 = positions[selected_pos1[0]][selected_pos1[1]]
                            pos2_2 = positions[selected_pos2[0]][selected_pos2[1]]
                            pos2_x = lerp(pos2_2[0], pos1_2[0], factor)
                            pos2_y = lerp(pos2_2[1], pos1_2[1], factor)

                            # Dessiner la grille sans les symboles en mouvement
                            draw_grid(grid, positions, symbols, cell_size, window, colignes[0], colignes[1], selected_pos1, selected_pos2, to_delete)

                            # Calcul des décalages pour centrer le symbole
                            symbol_width1, symbol_height1 = symbols[selected_symbol1].get_size()
                            offset_x1 = (cell_size - symbol_width1) // 2
                            offset_y1 = (cell_size - symbol_height1) // 2

                            symbol_width2, symbol_height2 = symbols[selected_symbol2].get_size()
                            offset_x2 = (cell_size - symbol_width2) // 2
                            offset_y2 = (cell_size - symbol_height2) // 2

                            # Dessiner les symboles en mouvement à leurs positions interpolées avec les décalages
                            window.blit(symbols[selected_symbol1], (pos1_x + offset_x1, pos1_y + offset_y1))
                            window.blit(symbols[selected_symbol2], (pos2_x + offset_x2, pos2_y + offset_y2))

                            pygame.time.wait(50)
                            pygame.display.flip()

                            # Échangez les symboles dans la grille
                            grid[selected_pos1[0]][selected_pos1[1]] = selected_symbol2
                            grid[selected_pos2[0]][selected_pos2[1]] = selected_symbol1

                        selected_symbol1 = None
                        selected_pos1 = None
                        selected_symbol2 = None
                        selected_pos2 = None

                        alignments_for_objectif, alignments_for_score = check_alignments(grid)

                        if alignments_for_objectif:
                            totalSymboles = len(alignments_for_objectif)

                            # for pos in alignments_for_objectif:
                            #     if len(pos) == 2:
                            #         i, j = pos
                            #         pygame.draw.rect(window, blanc, (positions[i][j][0], positions[i][j][1], cell_size, cell_size), 1)

                            aligner_sound.set_volume(volume_FX)
                            aligner_sound.play()

                            if 4 <= totalSymboles <= 6:
                                    overlay_image = overlay_S
                            elif 7 <= totalSymboles <= 12:
                                overlay_image = overlay_M
                            elif totalSymboles >= 13:
                                overlay_image = overlay_XL
                            else:
                                overlay_image = None

                            animate_overlay(overlay_image)

                            pygame.display.flip()
                            pygame.time.wait(50)

                            for pos in alignments_for_objectif:
                                i, j = pos
                                grid[i][j] = None

                            symboles_suppr_temp = 0
                            symboles_suppr += len(alignments_for_objectif)
                            score += len(alignments_for_score)
                            alignments_for_objectif = None
                            alignments_for_score = None

                            draw_grid(grid, positions, symbols, cell_size, window, colignes[0], colignes[1], selected_pos1, selected_pos2, to_delete)

                            pygame.display.flip() # Mettre à jour l'affichage pour montrer la surbrillance

                            if symboles_suppr >= current_objectif:
                                handle_level_completion()

    elif current_state == GameState.HELP:
        show_help_screen()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if click_on_button("BTN_CLOSE"):
                    current_state = GameState.PLAYING

    elif current_state == GameState.ENDGAME:
        show_endgame_screen()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if click_on_button("BTN_CLOSE"):
                    current_state = GameState.PLAYING

high_score = update_high_score()
pygame.mixer.quit()
pygame.quit()