#!/usr/bin/env python

import pygame

class Button(pygame.sprite.Sprite):
    """Class used to create a button, use setCords to set 
        position of topleft corner. Method pressed() returns
        a boolean and should be called inside the input loop."""
    def __init__(self, image_name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/' + image_name + '.png')
        self.rect = self.image.get_rect()
        
    def setCords(self,x,y):
        self.rect.topleft = x-(self.rect.width/2),y
        
    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
