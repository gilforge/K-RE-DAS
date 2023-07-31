import pygame

# Initialiser Pygame
pygame.init()

# Définir la taille de la fenêtre
window_size = (800, 600)

# Créer la fenêtre
window = pygame.display.set_mode(window_size)

# Définir une couleur pour le fond (RGB)
background_color = (0, 0, 0)  # Noir

# Boucle principale du jeu
running = True
while running:
    # Parcourir tous les événements
    for event in pygame.event.get():
        # Si l'événement est le fait de fermer la fenêtre, arrêter la boucle
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'écran avec la couleur de fond
    window.fill(background_color)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame une fois la boucle terminée
pygame.quit()
