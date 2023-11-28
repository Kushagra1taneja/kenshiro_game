import pygame
from os import walk

def import_folder(path):
    surface_list = []
    for U, X, information in walk(path):
        for img in information:
            full_path = path + '\\' + img
            img = pygame.image.load(full_path)
            surface_list.append(img)
    return surface_list
