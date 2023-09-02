############
# K-RE-DAS #
############
# Author = Gilles Aubin
# Website = gilles-aubin.net
# Version = 1.4.0 (langues, orientation horizontale, bug de sélection sur les bords)

import sys
import pygame
import random
import json

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
margin = 50  # Espace pour le titre et le score

delai_screen = 4000

# Polices de caractères
jetLight = "font/JetBrainsMono-Light.ttf"
jetBold = "font/JetBrainsMono-Bold.ttf"
jetExtraBold = "font/JetBrainsMono-ExtraBold.ttf"

window_size = (1280, 720)
demi_ecran = window_size[0] // 2

noir = (0, 0, 0)
blanc = (204, 204, 204)
vert = (0, 86, 52)

logoKredasX = 10
logoKredasY = 10
imageCartesX = 0
imageCartesY = 500


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

splash_image = load_image('img/splash_windows.jpg')  # Assurez-vous que l'image est dans le bon répertoire
game_image = load_image('img/tapis.jpg')
logo_studio = load_image('img/logo_studiocurieux.png')
logo_kredas = load_image('img/logo_kredas.png')
image_cartes = load_image('img/4as.png')
flag_en = load_image('img/flag_en.png')
flag_fr = load_image('img/flag_fr.png')
help_image = load_image('img/aide.jpg')
endgame_image = load_image('img/findejeu.jpg')
obstacle_image = load_image('img/obstacle.png')
fond_mobile = load_image('img/fond_mobile.jpg')
fond_pc = load_image('img/fond_pc.jpg')
contour_table = load_image('img/contour_table.png')

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

load_language()


########
# SONS #
########

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
    'BTN_HS': pygame.Rect(textHighScore_X - 10, textHighScore_Y, 200, 40),
    'BTN_NEW': pygame.Rect(BTNcentre, 350, BTNlarg, BTNhaut),
    'BTN_HELP': pygame.Rect(BTNcentre, 400, BTNlarg, BTNhaut),
    'BTN_QUIT': pygame.Rect(BTNcentre, 450, BTNlarg, BTNhaut),
    'BTN_CLOSE': pygame.Rect(demi_ecran - BTNlarg /2, 570, BTNlarg, BTNhaut),
    'BTN_RETRY': pygame.Rect(demi_ecran - BTNlarg * 1.5, 470, BTNlarg, BTNhaut),
    'BTN_NEXT': pygame.Rect(demi_ecran + BTNlarg/2, 470, BTNlarg, BTNhaut),
}

def draw_button(CARAC_BTN, text_size, text_button=None) :

    if text_button is not None:
        # bouton = pygame.draw.rect(window, blanc, buttons[CARAC_BTN], 1)
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
            print(f"CLICK GENERIC BTN > {CARAC_BTN}")
            return True
        return False


# >>>>>> BOUTON RESET HIGH SCORE

# Détecter le clic sur le high score
def click_on_button_HS(mouse_pos):
    if textHighScore_X - 10 < mouse_pos[0] < (textHighScore_X - 10 + 100) and textHighScore_Y < mouse_pos[1] < (textHighScore_Y + 40): 
        return True
    return False


###########
# NIVEAUX #
###########

# Lecture des informations du fichier config.json
def load_config_data() :
    try :
        with open('config/config.json', 'r') as file:
            data = json.load(file)
            if 'progression' not in data:
                data['progression'] = 1
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        sys.exit()

config_data = load_config_data()

# Trouver le niveau avec une progression de 1
def load_progress(config_data):
    if config_data:
        # Vérifiez si la clé "config" existe et contient des niveaux avec une progression égale à 1
        levels_with_progression = [level for level in config_data.get('config', []) if level.get('progression') == 1]
        
        # Si nous trouvons des niveaux avec une progression égale à 1, retournez le premier
        if levels_with_progression:
            return levels_with_progression[0]
        
        # Sinon, retournez le premier niveau par défaut
        return config_data.get('config', [{}])[0]
    
    # Si config_data est None ou vide, retournez un dictionnaire vide
    return {}

# Chargement des données de progression
current_level = load_progress(config_data)

# Charger les données du niveau en cours
levelToPlay = current_level['level']
current_objectif = current_level['objectif']
current_progress = current_level['progression']
current_meilleurScore = current_level['meilleurScore']
current_obstacles = current_level['obstacles']


def save_config_data(config_data):
    with open('config/config.json', 'w') as file:
        json.dump(config_data, file, indent=4)

def load_next_level():
    global levelToPlay, current_level, current_objectif, current_meilleurScore, high_score

    draw_recap_screen()

    waiting_for_input = True
    while waiting_for_input:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_on_button("BTN_RETRY"):
                    reset_game()
                    print("CLICK RETRY > after reset")
                    waiting_for_input = False
                elif click_on_button("BTN_NEXT"):
                    print(f"LevelToPlay {levelToPlay}")
                    if levelToPlay < len(config_data['config']):
                        levelToPlay += 1
                        # update_progression(levelToPlay)
                        save_progress(config_data)
                        print(f"CLICK NEXT {mouse_pos}")
                    else:
                        # Si c'est le dernier niveau, affichez l'écran de fin de jeu
                        save_progress(config_data)
                        show_endgame_screen()
                        # Ajoutez une boucle pour maintenir l'écran de fin de jeu à l'affichage
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if click_on_button("BTN_CLOSE"):
                                        levelToPlay = 1
                                        current_level = config_data['config'][levelToPlay-1]
                                        reset_game()
                                        return
                    current_level = config_data['config'][levelToPlay-1]
                    current_objectif = current_level['objectif']
                    current_meilleurScore = current_level['meilleurScore']
                    high_score = current_meilleurScore
                    reset_game()
                    waiting_for_input = False

# Fonction pour compter les symboles restants
def count_remaining_symbols(grid):
    count = 0
    for row in grid:
        for cell in row:
            if cell in symbols.keys():  # Vérifier si la cellule contient un symbole
                count += 1
    return count

#########
# SCORE #
#########

# Lecture du meilleur score du niveau
def get_high_score():
    global config_data
    # Récupérer le meilleur score du niveau actuel
    print(f"GET HIGHSCORE\n>>> meilleurScore : {current_meilleurScore}")

    return current_level['meilleurScore']


# Charger la variable score avec celui contenu dans le fichier
high_score = get_high_score()

# MISE A JOUR DU HIGH_SCORE > OK
def update_high_score():
    global high_score, score, config_data
    print(f"UPDATE HIGHSCORE\n>>> meilleurScore : {current_meilleurScore}")
    if score > current_level['meilleurScore']:
        current_level['meilleurScore'] = score
        save_config_data(config_data)

    return current_level['meilleurScore']


# REINITIALISER > OK
def reset_game():
    global config_data, grid, score
    grid = initialize_grid(*colignes)
    score = 0
    print(f"RESET GAME\n>>> {score}")
    return grid, score

# SAUVEGARDE PROGRESSION
def save_progress(config_data):
    # Réinitialiser la progression pour tous les niveaux
    for level in config_data['config']:
        level['progression'] = 0

    # Si le joueur a terminé tous les niveaux, définissez la progression du premier niveau sur 1
    if levelToPlay == 1:
        config_data['config'][0]['progression'] = 1
    else:
        config_data['config'][levelToPlay-1]['progression'] = 1

    save_config_data(config_data)
    print(f"SAVE PROGRESS\n>>> progression : {current_progress}")


#########################
# INITIALISER LA GRILLE #
#########################

def initialize_grid(*colignes):
    global config_data
    grid = []
    symbol_counts = {"pique": 0, "carreau": 0, "coeur": 0, "trefle": 0}
    symbols_list = list(symbols.keys())
    max_count = (colignes[0] * colignes[1]) // len(symbols_list)  # Calculer le nombre maximum de fois qu'un symbole peut apparaître

    for i in range(colignes[0]):
        row = []
        for j in range(colignes[1]):
            if any(obstacle['row'] == i and obstacle['col'] == j for obstacle in current_level['obstacles']):
                row.append('obstacle')  # Ajouter un obstacle
            else:
                # Choisir un symbole qui n'a pas encore atteint son maximum
                available_symbols = [symbol for symbol in symbols_list if symbol_counts[symbol] < max_count]
                chosen_symbol = random.choice(available_symbols)
                row.append(chosen_symbol)
                symbol_counts[chosen_symbol] += 1  # Incrémenter le compteur pour le symbole choisi
        grid.append(row)
    return grid

grid = initialize_grid(10,10)

# Créer une grille vide pour les positions des symboles
positions = []
for i in range(colignes[0]):
    row = []
    for j in range(colignes[1]):
        # La position initiale est basée sur l'indice de la cellule
        row.append((grid_x + j * cell_size, grid_y + i * cell_size))
    positions.append(row)


###############
# ALIGNEMENTS #
###############

def check_alignments(grid):
    to_delete = []
    global score
    for i in range(colignes[0]):
        for j in range(colignes[1]):
            # Vérifier l'alignement horizontal
            if j <= colignes[0] - 4:
                k = 0
                while j+k+1 < colignes[0] and grid[i][j] is not None and grid[i][j] == grid[i][j+k+1]:
                    k += 1
                if k >= 3:
                    for l in range(k+1):
                        to_delete.append((i, j + l))
                    score += 4  # Ajouter 4 points pour chaque alignement
            # Vérifier l'alignement vertical
            if i <= colignes[1] - 4:
                k = 0
                while i+k+1 < colignes[1] and grid[i][j] is not None and grid[i][j] == grid[i+k+1][j]:
                    k += 1
                if k >= 3:
                    for l in range(k+1):
                        to_delete.append((i + l, j))
                    score += 4  # Ajouter 4 points pour chaque alignement
    return to_delete

# Fonction d'animation des échanges de symboles
def lerp(start, end, factor):
    return (1 - factor) * start + factor * end


######################
# DESSINER LA GRILLE #
######################

# Créer une fenêtre
window = pygame.display.set_mode(window_size)

def draw_grid(grid, positions, symbols, cell_size, window, rows, cols, selected_pos1=None, selected_pos2=None, to_delete=None):
    # Pré-calculer les tailles des images
    obstacle_size = obstacle_image.get_size()
    
    # Convertir to_delete en set pour une recherche plus rapide
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
                
                # Si le symbole est sélectionné, utilisez la version "_on"
                if (i, j) in selected_positions:
                    window.blit(symbols_on[symbol], centered_pos)
                else:
                    window.blit(symbols[symbol], centered_pos)


##########
# ECRANS #
##########

# >>>>>> ECRAN LANGUES

def show_language_screen():
    global jetBold

    window.blit(fond_pc, (0,0))

    # Dessiner le titre
    # ecrire("ui_lang", 36, jetBold, blanc, 50, 100, align="center")

    flagEN_posX = buttons["BTN_EN"].x
    flagEN_posY = buttons["BTN_EN"].y
    flagFR_posX = buttons["BTN_FR"].x
    flagFR_posY = buttons["BTN_FR"].y

    place_image(flag_en, flagEN_posX, flagEN_posY)
    place_image(flag_fr, flagFR_posX, flagFR_posY)

    if click_on_button("BTN_EN"):
        load_language("en_US")

    elif click_on_button("BTN_FR"):
        load_language("fr_FR")
        
    # place_image(image_cartes, imageCartesX, imageCartesY)

    pygame.display.flip()
    # Attente de l'interaction de l'utilisateur
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


# >>>>>> SPLASH SCREEN

def show_splashscreen():

    # Dessinez tout pour le splash screen
    window.blit(fond_pc, (0, 0))
    place_image(logo_studio, 50, 50, position="center")
    ecrire("ui_present", 22, jetBold, blanc, 50, 120, align="center")
    place_image(logo_kredas, demi_ecran, 260, position="center")
    place_image(image_cartes, imageCartesX, imageCartesY)

    pygame.display.flip()
    pygame.time.wait(delai_screen)


# >>>>>> ECRAN AIDE

def show_help_screen():
    global jetBold

    # Dessiner le fond
    window.blit(fond_pc, (0,0))

    ecrire("help_how", 24, jetBold, blanc, 100, 80, align="center", ecran="help")
    place_image(logo_kredas, logoKredasX, 120, position="center")
    ecrire("help_rule1line1", 22, jetBold, blanc, 50, 270, align="center", ecran="help")
    ecrire("help_rule1line2", 22, jetBold, blanc, 50, 300, align="center", ecran="help")
    ecrire("help_rule2line1", 22, jetBold, blanc, 50, 370, align="center", ecran="help")
    ecrire("help_rule2line2", 22, jetBold, blanc, 50, 400, align="center", ecran="help")
    ecrire("help_rule3line1", 22, jetBold, blanc, 50, 470, align="center", ecran="help")
    ecrire("help_rule3line2", 22, jetBold, blanc, 50, 500, align="center", ecran="help")

    draw_button("BTN_CLOSE", 20, "ui_close")
    place_image(image_cartes, imageCartesX, imageCartesY)

    pygame.display.flip()


# >>>>>> ECRAN RECAP

def draw_recap_screen():
    mouse_pos = pygame.mouse.get_pos()

    window.blit(fond_pc, (0, 0))
    font = pygame.font.Font(jetBold, 40)
    place_image(logo_kredas, logoKredasX, 120, position="center")

    # Afficher le score et le highscore
    score_text = font.render(f"{score}", True, blanc)
    ecrire("ui_score", 20, jetBold, blanc, demi_ecran - 180, 280, align="left",ecran="ui")
    window.blit(score_text, (demi_ecran - 200 + 20, 330))

    highscore_text = font.render(f"{high_score}", True, blanc)
    ecrire("ui_best", 20, jetBold, blanc, demi_ecran + 60, 280, align="left",ecran="ui")
    window.blit(highscore_text, (demi_ecran + 120, 330))

    # Dessiner les boutons
    draw_button("BTN_RETRY", 20, "ui_retry")
    draw_button("BTN_NEXT", 20, "ui_next")

    place_image(image_cartes, imageCartesX, imageCartesY)

    pygame.display.flip()


# >>>>>> ECRAN FIN DE JEU

def show_endgame_screen():
    print("SHOW ENDGAME")

    global jetBold

    # Dessiner le fond
    window.fill((vert))
    window.blit(fond_pc, (0, 0))

    ecrire("end_well", 70, jetBold, blanc, 50, 150, align="center",ecran="end")
    ecrire("end_completed", 22, jetBold, blanc, 50, 230, align="center",ecran="end")
    ecrire("end_work", 22, jetBold, blanc, 50, 300, align="center",ecran="end")
    ecrire("end_share", 22, jetBold, blanc, 50, 330, align="center",ecran="end")
    ecrire(game_title, 45, jetBold, blanc, 50, 350, align="center",ecran="end")
    ecrire(game_url, 22, jetBold, blanc, 50, 430, align="center",ecran="end")

    draw_button("BTN_CLOSE", 20, "ui_close")

    place_image(image_cartes, imageCartesX, imageCartesY)

    pygame.display.flip()


# >>>>>> DECOR

def poseDecor():
    fond = pygame.transform.scale(game_image, window_size)
    window.blit(fond,(0,0))
    place_image(logo_kredas, 63, 65)
    place_image(image_cartes, imageCartesX, imageCartesY)
    place_image(contour_table, pos_contourX, pos_contourY)


####################
# LANCEMENT DU JEU #
####################

if debug is not True :
    show_splashscreen()
    show_language_screen()


#####################
# BOUCLE PRINCIPALE #
#####################

# Variable pour suivre le symbole actuellement sélectionné et sa position
selected_symbol1 = None
selected_pos1 = None
selected_symbol2 = None
selected_pos2 = None

running = True
showing_help = False
showing_endgame = False

while running:
    mouse_pos = pygame.mouse.get_pos()

    modeDebug()


# >>>>>> DECOR

    poseDecor()

# >>>>>> ECRAN AIDE

    if showing_help:
        show_help_screen()
        pygame.display.flip()

        # Boucle interne pour attendre un clic de souris
        while showing_help:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    showing_help = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if click_on_button("BTN_CLOSE"):
                        showing_help = False

        continue  # Continue à la prochaine itération de la boucle, en sautant le reste du code


# >>>>>> ECRAN FIN DE JEU

    if showing_endgame:
        show_endgame_screen()
        pygame.display.flip()

        # Boucle interne pour attendre un clic de souris
        while showing_endgame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    showing_endgame = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if click_on_button("BTN_CLOSE"):
                        showing_endgame = False

        continue  # Continue à la prochaine itération de la boucle, en sautant le reste du code


# >>>>>> INTERFACE

    # ecrire(game_title, 36, jetExtraBold, blanc, demi_ecran /2 - (logo_kredas.get_width() /2), 110) # Titre

    # Niveau
    fontLevel = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 24)
    textLevel = fontLevel.render(f"{ui_texts['ui_level']} : {levelToPlay:02}", True, blanc)
    window.blit(textLevel, (margeHRZ+(logoKRDLarg/2) - (textLevel.get_width()/2), 200))  # Vous pouvez ajuster la position selon vos besoins

    # Score le plus élevé
    fontHighScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 32)
    textHighScore = fontHighScore.render(f"{high_score:04}", True, blanc)
    window.blit(textHighScore, (margeHRZ+(logoKRDLarg/2) - (textLevel.get_width()/2), 250))
    draw_button("BTN_HS", 32, text_button=None)
    # high_score_BTN = pygame.draw.rect(window, blanc, (textHighScore_X - 10,textHighScore_Y,200,40), 2)

    # Score
    fontScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 32)
    textScore = fontScore.render(f"{score:04}", True, blanc)
    window.blit(textScore, (margeHRZ+(logoKRDLarg/2) - (textLevel.get_width()/2), 300))


    draw_button("BTN_NEW", 20, "ui_new")
    draw_button("BTN_HELP", 20, "ui_help")
    draw_button("BTN_QUIT", 20, "ui_quit")

    to_delete = []

    draw_grid(grid, positions, symbols, cell_size, window, colignes[0], colignes[1], selected_pos1, selected_pos2, to_delete)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Parcourir tous les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            # mouse_pos = pygame.mouse.get_pos()

            if showing_help:
                # Gestion des clics sur l'écran d'aide
                if click_on_button("BTN_CLOSE"):
                    showing_help = False
                continue  # Continue à la prochaine itération pour éviter de traiter d'autres clics

            if showing_endgame:
                # Gestion des clics sur l'écran d'aide
                if click_on_button("BTN_CLOSE"):
                    showing_endgame = False
                continue  # Continue à la prochaine itération pour éviter de traiter d'autres clics

            # Gestion des clics sur l'écran de jeu principal
            if click_on_button("BTN_NEW"):
                high_score = update_high_score()
                reset_game()

            elif click_on_button("BTN_QUIT"):
                high_score = update_high_score()
                running = False

            elif click_on_button("BTN_HELP"):
                showing_help = True
                show_help_screen()

            if buttons["BTN_HS"].collidepoint(mouse_pos):
                pygame.draw.rect(window, noir, buttons["BTN_HS"])

            if click_on_button("BTN_HS"):
                high_score = 0
                score = 0
                update_high_score()

            cell_x = (mouse_pos[0] - grid_x) // cell_size
            cell_y = (mouse_pos[1] - grid_y) // cell_size

            if 0 <= cell_x < colignes[0] and 0 <= cell_y < colignes[1] and grid[cell_y][cell_x] is not None:
                if grid[cell_y][cell_x] == 'obstacle':  # Si c'est un obstacle, ignorez la sélection
                    continue
                if selected_symbol1 is None:  # If no symbol is selected yet
                    selected_symbol1 = grid[cell_y][cell_x]
                    selected_pos1 = (cell_y, cell_x)
                    # print(f"Symbole1 : {selected_symbol1} à la position {selected_pos1}")

                else:  # If a symbol is already selected
                    if (cell_x, cell_y) != selected_pos1:
                        selected_symbol2 = grid[cell_y][cell_x]
                        selected_pos2 = (cell_y, cell_x)
                        # print(f"Symbole2 : {selected_symbol1} à la position {selected_pos1}")

                    # Animation de l'échange
                    vitessEchange = 10 # plus petit = plus rapide
                    swap_sound.set_volume(volume_FX)
                    swap_sound.play()

                    for _ in range(vitessEchange):
                        # 1. Effacer l'écran
                        window.blit(fond_pc, (0, 0))

                        # Redessiner tous les éléments de l'UI
                        # window.blit(textTitle, (70,10))
                        ecrire(game_title, 36, jetExtraBold, blanc, 70, 10)

                        # window.blit(textAuthor, (70,50))
                        ecrire(game_author, 12, jetLight, blanc, 70, 50)

                        window.blit(textHighScore, (textHighScore_X,textHighScore_Y))
                        pygame.draw.rect(window, blanc, (textHighScore_X - 10,textHighScore_Y,100,40), 2)
                        window.blit(textScore, (450,15))
                        window.blit(textLevel, (450, 5))

                        draw_button("BTN_NEW", 20, "ui_new")
                        draw_button("BTN_HELP", 20, "ui_help")
                        draw_button("BTN_QUIT", 20, "ui_quit")

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

                        # 3. Mettre à jour l'affichage
                        pygame.time.wait(50)
                        pygame.display.flip()

                        # Échangez les symboles dans la grille
                        grid[selected_pos1[0]][selected_pos1[1]] = selected_symbol2
                        grid[selected_pos2[0]][selected_pos2[1]] = selected_symbol1

                    # Reset the selected symbols and positions
                    selected_symbol1 = None
                    selected_pos1 = None
                    selected_symbol2 = None
                    selected_pos2 = None

                    # Vérifier les alignements après le mouvement
                    alignments = check_alignments(grid)
                    if alignments:  # Si la liste n'est pas vide

                        # Mettre en surbrillance les symboles à supprimer
                        for pos in alignments:
                            if len(pos) == 2:
                                i, j = pos
                                pygame.draw.rect(window, blanc, (positions[i][j][0], positions[i][j][1], cell_size, cell_size), 1)
                        aligner_sound.set_volume(volume_FX)
                        aligner_sound.play()

                        pygame.display.flip()  # Mettre à jour l'affichage pour montrer la surbrillance
                        pygame.time.wait(500)  # Attendre 500 millisecondes (0.5 seconde)

                        # Supprimer les symboles à supprimer de la grille
                        for pos in alignments:
                            if len(pos) == 2:
                                i, j = pos
                                grid[i][j] = None
                        # Vider la liste alignments
                        alignments = None, None

                        draw_grid(grid, positions, symbols, cell_size, window, colignes[0], colignes[1], selected_pos1, selected_pos2, to_delete)

                        pygame.display.flip()  # Mettre à jour l'affichage pour montrer la surbrillance

                        remaining_symbols = count_remaining_symbols(grid)
                        if remaining_symbols <= current_objectif:
                            # Gérer la fin de jeu ici (par exemple, passer au niveau suivant)
                            print("FIN DU NIVEAU !")
                            save_progress(config_data)
                            high_score = update_high_score()
                            load_next_level()

high_score = update_high_score()

# Quitter Pygame une fois la boucle terminée
pygame.mixer.quit()
pygame.quit()