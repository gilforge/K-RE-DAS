############
# K-RE-DAS #
############
# Author = Gilles Aubin
# Website = gilles-aubin.net
# Version = 1.3.1

import sys
import pygame
import random
import json

# Initialiser Pygame
pygame.init()
pygame.mixer.init()


#############
# VARIABLES #
#############

# Définir les variables du jeu
game_title = "K-RE-DAS"
pygame.display.set_caption(game_title)

game_author = "by Gilles Aubin"
score = 0
margin = 50  # Espace pour le titre et le score
window_size = (600, 650)  # Taille de la fenêtre
cell_size = (window_size[0] - 2 * margin) // 10  # Taille de chaque cellule de la grille

color_Black = (0, 0, 0)
color_White = (204, 204, 204)

# Définir les coordonnées de la grille, du cadre et des cellules
grid_x = 50
grid_y = 75


##########
# IMAGES #
##########

def load_image(filename):
    try:
        return pygame.image.load(filename)
    except pygame.error:
        print(f"Erreur lors du chargement de l'image : {filename}")
        sys.exit()

splash_image = load_image('img/splash_windows.png')  # Assurez-vous que l'image est dans le bon répertoire
game_image = load_image('img/tapis.jpg')
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
help_image = load_image('img/aide.jpg')
endgame_image = load_image('img/findejeu.jpg')
obstacle_image = load_image('img/obstacle.png')


########
# SONS #
########

volume_FX = 0.5
volume_ambiance = 0.5

def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except pygame.error:
        print(f"Erreur lors du chargement du son : {filename}")
        sys.exit()

ambiance_music = pygame.mixer.music.load("sons/ambiance.wav")
swap_sound = load_sound("sons/swap.ogg")
aligner_sound = load_sound("sons/aligner.ogg")

pygame.mixer.music.play(-1)  # Le -1 signifie que la musique sera jouée en boucle indéfiniment
pygame.mixer.music.set_volume(volume_ambiance)


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
        print("Erreur lors du chargement du fichier de configuration.")
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
    print(f"SAVECONFIGDATA\n>>> config : {config_data}")
    with open('config/config.json', 'w') as file:
        json.dump(config_data, file, indent=4)

def load_next_level():
    global levelToPlay, current_level, current_objectif, current_meilleurScore, high_score

    print("LOADNEXTLEVEL")

    draw_recap_screen()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_on_button_retry(pygame.mouse.get_pos()):
                    reset_game()
                    waiting_for_input = False
                elif click_on_button_next_level(pygame.mouse.get_pos()):
                    if levelToPlay < len(config_data['config']):
                        levelToPlay += 1
                        # update_progression(levelToPlay)
                        save_progress(config_data)
                    else:
                        # Si c'est le dernier niveau, affichez l'écran de fin de jeu
                        save_progress(config_data)
                        show_endgame_screen()
                        # Ajoutez une boucle pour maintenir l'écran de fin de jeu à l'affichage
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if click_on_button_close(pygame.mouse.get_pos()):
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
    grid = initialize_grid()
    score = 0
    print(f"RESSET GAME\n>>> {score}")
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

def initialize_grid():
    global config_data
    grid = []
    symbol_counts = {"pique": 0, "carreau": 0, "coeur": 0, "trefle": 0}
    symbols_list = list(symbols.keys())

    for i in range(10):
        row = []
        for j in range(10):
            if any(obstacle['row'] == i and obstacle['col'] == j for obstacle in current_level['obstacles']):
                row.append('obstacle')  # Ajouter un obstacle
            else:
                # Choisir un symbole qui n'a pas encore été ajouté 25 fois
                available_symbols = [symbol for symbol in symbols_list if symbol_counts[symbol] < 25]
                chosen_symbol = random.choice(available_symbols)
                row.append(chosen_symbol)
                symbol_counts[chosen_symbol] += 1  # Incrémenter le compteur pour le symbole choisi
        grid.append(row)
    return grid

grid = initialize_grid()

# Créer une grille vide pour les positions des symboles
positions = []
for i in range(10):
    row = []
    for j in range(10):
        # La position initiale est basée sur l'indice de la cellule
        row.append((grid_x + j * cell_size, grid_y + i * cell_size))
    positions.append(row)


###############
# ALIGNEMENTS #
###############

def check_alignments(grid):
    to_delete = []
    global score
    for i in range(10):
        for j in range(10):
            # Vérifier l'alignement horizontal
            if j <= 6:
                k = 0
                while j+k+1 < 10 and grid[i][j] is not None and grid[i][j] == grid[i][j+k+1]:
                    k += 1
                if k >= 3:
                    for l in range(k+1):
                        to_delete.append((i, j + l))
                    score += 4  # Ajouter 4 points pour chaque alignement
            # Vérifier l'alignement vertical
            if i <= 6:
                k = 0
                while i+k+1 < 10 and grid[i][j] is not None and grid[i][j] == grid[i+k+1][j]:
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

# Fonction qui dessine la grille et place les obstacles en fonction du niveau
def draw_grid(grid, positions, symbols, cell_size, window, selected_pos1=None, selected_pos2=None, to_delete=None):
    # Pré-calculer les tailles des images
    obstacle_size = obstacle_image.get_size()
    
    # Convertir to_delete en set pour une recherche plus rapide
    to_delete_set = set(to_delete) if to_delete else set()
    
    selected_positions = {selected_pos1, selected_pos2}

    for i in range(10):
        for j in range(10):
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


###########
# BOUTONS #
###########

# >>>>>> BOUTON RESET HIGH SCORE

# Détecter le clic sur le high score
def click_on_button_HS(mouse_pos):
    if textHighScore_X - 10 < mouse_pos[0] < (textHighScore_X - 10 + 100) and textHighScore_Y < mouse_pos[1] < (textHighScore_Y + 40): 
        return True
    return False


# >>>>>> BOUTON NOUVEAU

# Variables du bouton NOUVEAU
width_new = 152
height_new = 40
posX_new = 58
posY_new = 590
posX_text_new = posX_new + 10
posY_text_new = posY_new + 5

def draw_button_new():
    pygame.draw.rect(window, color_White, (posX_new, posY_new, width_new, height_new),1)
    font_new = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text_new = font_new.render("Nouveau", True, color_White) 
    window.blit(text_new, (posX_text_new, posY_text_new)) 

# Détecter le clic sur le bouton Nouveau
def click_on_button_new(mouse_pos):
    if posX_new < mouse_pos[0] < (posX_new + width_new) and posY_new < mouse_pos[1] < (posY_new + height_new): 
        print("BOUTON NOUVEAU")
        return True
    return False


# >>>>>> BOUTON AIDE

# Variables du bouton AIDE
width_help = 152
height_help = 40
posX_help = posX_new + width_new + 10
posY_help = 590
posX_text_help = posX_help + 10
posY_text_help = posY_help + 5

def draw_button_help():
    pygame.draw.rect(window, color_White, (posX_help, posY_help, width_help, height_help), 1)
    font_help = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text_help = font_help.render("Aide", True, color_White)
    window.blit(text_help, (posX_text_help, posY_text_help))

# Détecter le clic sur le bouton Aide
def click_on_button_help(mouse_pos):
    if posX_help < mouse_pos[0] < (posX_help + width_help) and posY_help < mouse_pos[1] < (posY_help + height_help):
        print(f"{showing_help} | BOUTON AIDE")
        return True
    return False


# >>>>>> BOUTON QUITTER

# Variables du bouton QUITTER
width_quit = 152
height_quit = 40
posX_quit = posX_help + width_help + 10
posY_quit = 590
posX_text_quit = posX_quit + 10
posY_text_quit = posY_quit + 5

def draw_button_quit():
    pygame.draw.rect(window, color_White, (posX_quit, posY_quit, width_quit, height_quit),1)
    font_quit = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text_quit = font_quit.render("Quitter", True, color_White) 
    window.blit(text_quit, (posX_text_quit, posY_text_quit)) 

# Détecter le clic sur le bouton QUITTER
def click_on_button_quit(mouse_pos):
    if posX_quit < mouse_pos[0] < (posX_quit + width_quit) and posY_quit < mouse_pos[1] < (posY_quit + height_quit): 
        print("BOUTON QUITTER")
        return True
    return False


# >>>>>> BOUTON FERMER

# Variables du bouton FERMER
width_close = 152
height_close = 40
posX_close = posX_new + width_new + 10
posY_close = 590
posX_text_close = posX_close + 10
posY_text_close = posY_close + 5

# Dessiner le bouton Fermer
def draw_button_close():
    pygame.draw.rect(window, color_White, (posX_close, posY_close, width_close, height_close), 1)
    font_close = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text_close = font_close.render("Fermer", True, color_White)
    window.blit(text_close, (posX_text_close, posY_text_close))

# Détecter le clic sur le bouton Fermer
def click_on_button_close(mouse_pos):
    if posX_close < mouse_pos[0] < (posX_close + width_close) and posY_close < mouse_pos[1] < (posY_close + height_close):
        print("BOUTON FERMER")
        return True
    return False


# >>>>>> BOUTONS RECAP

# Variables des boutons RECAP

def click_on_button_retry(pos):
    return window_size[0] // 4 <= pos[0] <= window_size[0] // 4 + 100 and window_size[1] // 2 <= pos[1] <= window_size[1] // 2 + 50

def click_on_button_next_level(pos):
    return 3 * window_size[0] // 4 - 100 <= pos[0] <= 3 * window_size[0] // 4 and window_size[1] // 2 <= pos[1] <= window_size[1] // 2 + 50



##########
# ECRANS #
##########

# >>>>>> ECRAN AIDE

def show_help_screen():
    print("SHOW HELPSCREEN")
    window.blit(help_image, (0, 0))
    draw_button_close()
    pygame.display.flip()


# >>>>>> ECRAN RECAP

def draw_recap_screen():
    window.blit(fond, (0, 0))
    font = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)

    # Afficher le score et le highscore
    score_text = font.render(f"Score : {score}", True, color_White)
    highscore_text = font.render(f"Meilleur score : {high_score}", True, color_White)

    window.blit(score_text, (window_size[0] // 2 - score_text.get_width() // 2, window_size[1] // 4))
    window.blit(highscore_text, (window_size[0] // 2 - highscore_text.get_width() // 2, window_size[1] // 4 + 30))

    # Dessiner les boutons
    pygame.draw.rect(window, color_White, (window_size[0] // 4, window_size[1] // 2, 100, 50),1)
    font = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text = font.render("Refaire", True, color_White)  # Assurez-vous d'avoir défini color_Black
    window.blit(text, (window_size[0] // 4 + 50 - text.get_width() // 2, window_size[1] // 2 + 25 - text.get_height() // 2))

    pygame.draw.rect(window, color_White, (3 * window_size[0] // 4 - 100, window_size[1] // 2, 100, 50),1)
    font = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text = font.render("Suivant", True, color_White)
    window.blit(text, (3 * window_size[0] // 4 - 50 - text.get_width() // 2, window_size[1] // 2 + 25 - text.get_height() // 2))

    pygame.display.flip()

# >>>>>> ECRAN FIN DE JEU

def show_endgame_screen():
    print("SHOW ENDGAME")
    window.blit(endgame_image, (0, 0))
    draw_button_close()
    pygame.display.flip()


# >>>>>> ECRAN ACCUEIL

# Transition entre 2 images
def fade_between_images(image1, image2):
    for i in range(256):
        alpha = i  # Alpha pour l'image1
        beta = 255 - i  # Alpha pour l'image2

        # Créez une copie temporaire des images avec les valeurs alpha appropriées
        splash_temp = image2.copy()
        game_temp = image1.copy()
        splash_temp.set_alpha(alpha)
        game_temp.set_alpha(beta)

        # Dessinez les images avec les valeurs alpha
        window.blit(splash_temp, (0, 0))
        window.blit(game_temp, (0, 0))

        # Mettez à jour l'affichage
        pygame.display.flip()

        # Attendez un peu pour voir l'effet de fondu
        pygame.time.wait(3)  # Attendre 10 millisecondes

fade_between_images(splash_image, game_image)


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
                    mouse_pos = pygame.mouse.get_pos()
                    if click_on_button_close(mouse_pos):
                        showing_help = False

        continue  # Continue à la prochaine itération de la boucle, en sautant le reste du code

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
                    mouse_pos = pygame.mouse.get_pos()
                    if click_on_button_close(mouse_pos):
                        showing_endgame = False

        continue  # Continue à la prochaine itération de la boucle, en sautant le reste du code

    # Remplir l'écran avec l'image de fond
    image_fond = load_image("img/tapis.jpg")
    fond = pygame.transform.scale(image_fond, window_size)
    window.blit(fond,(0,0))

    # Titre
    fontTitle = pygame.font.Font("font/JetBrainsMono-ExtraBold.ttf", 36)
    textTitle = fontTitle.render(game_title, True, color_White)
    window.blit(textTitle, (70,10))

    # Nom de l'auteur
    fontAuthor = pygame.font.Font("font/JetBrainsMono-Light.ttf", 12)
    textAuthor = fontAuthor.render(game_author, True, color_White)
    window.blit(textAuthor, (70,50))  # -30 pour le rapprocher du titre

    # Score le plus élevé
    textHighScore_X = 300
    textHighScore_Y = 15
    fontHighScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 32)
    textHighScore = fontHighScore.render(f"{high_score:04}", True, color_White)
    window.blit(textHighScore, (textHighScore_X,textHighScore_Y))
    high_score_BTN = pygame.draw.rect(window, color_White, (textHighScore_X - 10,textHighScore_Y,100,40), 2)

    # Score
    fontScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 32)
    textScore = fontScore.render(f"{score:04}", True, color_White)
    window.blit(textScore, (450,15))

    # Niveau
    fontLevel = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 12)
    textLevel = fontLevel.render(f"Level: {levelToPlay}", True, color_White)
    window.blit(textLevel, (450, 5))  # Vous pouvez ajuster la position selon vos besoins

    draw_button_new()
    draw_button_help()
    draw_button_quit()

    to_delete = []

    draw_grid(grid, positions, symbols, cell_size, window, selected_pos1, selected_pos2, to_delete)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Parcourir tous les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            if showing_help:
                # Gestion des clics sur l'écran d'aide
                if click_on_button_close(mouse_pos):
                    showing_help = False
                continue  # Continue à la prochaine itération pour éviter de traiter d'autres clics

            if showing_endgame:
                # Gestion des clics sur l'écran d'aide
                if click_on_button_close(mouse_pos):
                    showing_endgame = False
                continue  # Continue à la prochaine itération pour éviter de traiter d'autres clics

            # Gestion des clics sur l'écran de jeu principal
            if click_on_button_new(mouse_pos):
                high_score = update_high_score()
                reset_game()

            elif click_on_button_quit(mouse_pos):
                high_score = update_high_score()
                running = False

            elif click_on_button_help(mouse_pos):
                showing_help = True
                show_help_screen()

            if high_score_BTN.collidepoint(mouse_pos):
                pygame.draw.rect(window, color_Black, high_score_BTN)

            if click_on_button_HS(mouse_pos):
                high_score = 0
                score = 0
                update_high_score()

            cell_x = (mouse_pos[0] - grid_x) // cell_size
            cell_y = (mouse_pos[1] - grid_y) // cell_size

            if 0 <= cell_x < 10 and 0 <= cell_y < 10 and grid[cell_y][cell_x] is not None:
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
                        window.blit(fond, (0, 0))

                        # Redessiner tous les éléments de l'UI
                        window.blit(textTitle, (70,10))
                        window.blit(textAuthor, (70,50))
                        window.blit(textHighScore, (textHighScore_X,textHighScore_Y))
                        pygame.draw.rect(window, color_White, (textHighScore_X - 10,textHighScore_Y,100,40), 2)
                        window.blit(textScore, (450,15))
                        window.blit(textLevel, (450, 5))
                        draw_button_new()
                        draw_button_help()
                        draw_button_quit()
                        
                        # 2. Dessiner les éléments
                        factor = _ / vitessEchange

                        # Pour pos1_x
                        pos1_1 = positions[selected_pos1[1]][selected_pos1[0]]
                        if selected_pos2 is not None:                            
                            pos2_1 = positions[selected_pos2[1]][selected_pos2[0]]
                            pos1_x = lerp(pos1_1[0], pos2_1[0], factor)
                        else:
                            continue
                        # Pour pos1_y
                        # Nous avons déjà défini pos1_1 et pos2_1 ci-dessus, donc nous pouvons les réutiliser
                        pos1_y = lerp(pos1_1[1], pos2_1[1], factor)

                        # Pour pos2_x
                        pos1_2 = positions[selected_pos1[1]][selected_pos1[0]]  # C'est la même que pos1_1, mais pour la clarté, je la redéfinis
                        pos2_2 = positions[selected_pos2[1]][selected_pos2[0]]
                        pos2_x = lerp(pos2_2[0], pos1_2[0], factor)

                        # Pour pos2_y
                        # Nous avons déjà défini pos1_2 et pos2_2 ci-dessus, donc nous pouvons les réutiliser
                        pos2_y = lerp(pos2_2[1], pos1_2[1], factor)


                        # Dessiner la grille sans les symboles en mouvement
                        draw_grid(grid, positions, symbols, cell_size, window, selected_pos1, selected_pos2, to_delete)

                        # Dessiner les symboles en mouvement à leurs positions interpolées
                        window.blit(symbols[selected_symbol1], (pos1_y, pos1_x))
                        window.blit(symbols[selected_symbol2], (pos2_y, pos2_x))

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
                                pygame.draw.rect(window, color_White, (positions[i][j][0], positions[i][j][1], cell_size, cell_size), 1)
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

                        draw_grid(grid, positions, symbols, cell_size, window, selected_pos1, selected_pos2, to_delete)
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