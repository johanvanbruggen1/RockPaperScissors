import pygame
import os

class FlyingObject:
    def __init__(self, game, id, x_position, y_position, horizontal_step, vertical_step, mortal, lifetime, subtype):
        # game
        self.game = game

        # id
        self.id = id
        
        # position, size, velocity 
        self.x_position = x_position
        self.y_position = y_position
        self.width = 40
        self.height = 40
        self.horizontal_step = horizontal_step
        self.vertical_step = vertical_step
        
        # subtype, image, rectangle
        self.subtype = subtype
        self.image = self.set_image_according_to_subtype()
        self.rectangle = self.image.get_rect(topleft = [self.x_position, self.y_position])

        # 
        self.collision_already_handled_ids = []
        
        # mortality
        self.mortal = mortal

        # lifetime
        self.lifetime = lifetime

    # set image according to subtype   
    def set_image_according_to_subtype(self):
        if self.subtype == "rock":
            return pygame.transform.scale(pygame.image.load(os.path.join("Images", "rock.png")), (self.width, self.height))
        if self.subtype == "paper":
            return pygame.transform.scale(pygame.image.load(os.path.join("Images", "paper.png")), (self.width, self.height))
        if self.subtype == "scissors":
            return pygame.transform.scale(pygame.image.load(os.path.join("Images", "scissors.png")), (self.width, self.height))

    def check_borders(self):
        # if new position is outside the borders, the object will be given a virtual position outside the borders.
        # From this virtual position, one step will in the new direction will bring the object to the right position (between the borders).
        # For example: x_position is 1 and horizontal_step = -5. Then 1 - 5 < 0, so virtual x_position will be -1 and horizontal_step = 5.
        # When the horizontal_step is added, this will give a new x_position of 4. The object has then travelled 5 positions, from 1 to 0 to 4.

        # left-side                                                                 # left
        if self.x_position + self.horizontal_step < 0:
            self.x_position = -1 * self.x_position                                  # set position virtual position
            self.horizontal_step = -1 * self.horizontal_step                        # change step direction

        # right-side                                                                # right
        if self.x_position + self.width + self.horizontal_step > self.game.width:
            self.x_position = 2 *(self.game.width - self.width) - self.x_position   # set position virtual position
            self.horizontal_step = -1 * self.horizontal_step                        # change step direction

        # top-side                                                                  # top
        if self.y_position + self.vertical_step < 0:
            self.y_position = -1 * self.y_position                                  # set position virtual position
            self.vertical_step = -1 * self.vertical_step                            # change step direction

        # bottom-side                                                               # bottom
        if self.y_position + self.height + self.vertical_step > self.game.height :
            self.y_position = 2 *(self.game.height - self.height) - self.y_position # set position virtual position
            self.vertical_step = -1 * self.vertical_step                            # change step direction

    # move
    def move(self):
        self.x_position += self.horizontal_step
        self.y_position += self.vertical_step
        self.rectangle.topleft = (self.x_position, self.y_position)

    # decrease lifetime
    def decrease_lifetime(self):
        self.lifetime -= 1

    # update
    def update(self):
        self.check_borders()
        self.move()
        if self.mortal:
            self.decrease_lifetime()

    # draw
    def render(self):
        self.game.screen.blit(self.image, self.rectangle)
