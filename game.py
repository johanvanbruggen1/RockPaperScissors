from operator import index
import pygame
import os
import random
import sys
import math

from game_objects import FlyingObject

# general bounch
def bounch(flying_object_step, other_flying_object_step):
    if flying_object_step*other_flying_object_step > 0:
        return bounch_after_chasing(flying_object_step, other_flying_object_step)
    else:
        return bounch_frontal(flying_object_step, other_flying_object_step)

# specific bounch: after chasing
def bounch_after_chasing(flying_object_step, other_flying_object_step):
    temporary_step = flying_object_step
    flying_object_step = other_flying_object_step
    other_flying_object_step = temporary_step
    return flying_object_step, other_flying_object_step

# specific bounch: frontal
def bounch_frontal(flying_object_step, other_flying_object_step):
    flying_object_step *= -1
    other_flying_object_step *= -1
    return flying_object_step, other_flying_object_step

list_of_subtypes = ["rock", "paper", "scissors"]

def index_of_subtype(flying_object):
    return list_of_subtypes.index(flying_object.subtype)

def index_difference(flying_object, other_flying_object):
    return index_of_subtype(flying_object) - index_of_subtype(other_flying_object)

def first_attacks_second(flying_object, other_flying_object):
    if index_difference(flying_object, other_flying_object) == 1 or index_difference(flying_object, other_flying_object) == -len(list_of_subtypes) + 1:
        # if self.list_of_subtypes.index(flying_object.subtype) - self.list_of_subtypes.index(other_flying_object.subtype) == 1 or self.list_of_subtypes.index(flying_object.subtype) - self.list_of_subtypes.index(other_flying_object.subtype) == -len(self.list_of_subtypes) + 1:
        other_flying_object.subtype = flying_object.subtype                                   # weaker flying object gets type of stronger flying object
        other_flying_object.image = other_flying_object.set_image_according_to_subtype()      # set image according to type


class Game:

    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        pygame.init()                   # game initialization
        # window
        self.width = 1366              # width
        self.height = 768               # height
        self.screen = pygame.display.set_mode((self.width, self.height))        # screen
        self.background = pygame.transform.scale(pygame.image.load(os.path.join("Images", "background.png")), (self.width, self.height))
        
        # clock
        self.clock = pygame.time.Clock() # to track time
        
        # icon and caption
        self.caption = "Rock, Paper, Scissors"
        pygame.display.set_caption(self.caption)
        title_bar_icon = pygame.transform.scale(pygame.image.load(os.path.join("Images", "scissors.png")), (32, 32))
        pygame.display.set_icon(title_bar_icon)
        
        # list of subtypes
        # self.list_of_subtypes = ["rock", "paper", "scissors"]
        self.list_of_subtypes = list_of_subtypes                    # dit nog terugveranderen
        
        # new game
        self.new_game()

    def new_game(self):

        # initialization of list of flying objects
        self.flying_objects=[]
        id = 0
        
        # create x number of flying objects
        for i in range(35):

            id += 1
            collision_at_the_start = True

            # while no free space is found to put new flying object 
            while collision_at_the_start:
                
                # create new scissors
                new_flying_object = FlyingObject(
                    self,
                    id,
                    random.randint(0, self.width-50),                       # x_postiion
                    random.randint(0, self.height-50),                      # y_position
                    random.randint(0,3000)/1000*(2*random.randint(1,2)-3),  # horizontal step (velocity)
                    random.randint(0,3000)/1000*(2*random.randint(1,2)-3),  # vertical step (velocity)
                    False,                                                  # mortal
                    random.randint(300,1000),                               # lifetime
                    self.list_of_subtypes[random.randint(0,2)]              # subtype
                )

                # check if new flying object would collide with an existing flying object from at the start
                collision_with_other_flying_object = False
                for existing_flying_object in self.flying_objects:
                    if pygame.Rect.colliderect(new_flying_object.rectangle, existing_flying_object.rectangle):
                        collision_with_other_flying_object = True

                # if at least one collision (with existing flying object) would happen, start while loop again
                if collision_with_other_flying_object:
                    continue
                
                # if it made it to here, the new scissors didn't collide with any other
                # so there is space and new scissors can safely be added
                collision_at_the_start = False
                self.flying_objects.append(new_flying_object)
            
    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):   # if 'x' is clicked or 'escape' is pressed
                pygame.quit()               # quit
                sys.exit()                  # exit

            # by pressing the key 'D', the flying objects become mortal en die at a certain moment
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                for flying_object in self.flying_objects:
                    flying_object.mortal = True

            # by pressing the key 'R', the objects are freshly assigned to random types
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                for flying_object in self.flying_objects:
                    flying_object.subtype = self.list_of_subtypes[random.randint(0,2)]
                    flying_object.image = flying_object.set_image_according_to_subtype()

            
                
    
    def update(self):
        
        for flying_object in self.flying_objects:
            flying_object.update()                              # update flying objects
            
            # remove not alive objects
            if flying_object.lifetime <= 0:                     # if not alive
                self.flying_objects.remove(flying_object)       # remove

            # check for collision
            for other_flying_object in self.flying_objects:
                if flying_object != other_flying_object:
                    if pygame.Rect.colliderect(flying_object.rectangle, other_flying_object.rectangle):
                        
                        # check if collision is not already handled. Half of the time, this is the case:
                        # the objects are the same, but flying_object is former other_flying_object and
                        # other_flying_object is former flying_object
                        if not(flying_object.id in other_flying_object.collision_already_handled_ids):
                            flying_object.collision_already_handled_ids.append(other_flying_object.id)

                            # prohibit dividing by zero. This happens when objects are straight above each other
                            # deviate slightly from zero to get desired result
                            if flying_object.rectangle.centerx - other_flying_object.rectangle.centerx == 0:
                                flying_object.rectangle.centerx += 1

                            # if flying objects are more horizontally positioned from each oter
                            if -math.pi/4 < math.atan((flying_object.rectangle.centery - other_flying_object.rectangle.centery)/(flying_object.rectangle.centerx - other_flying_object.rectangle.centerx)) < math.pi/4:
                                flying_object.horizontal_step, other_flying_object.horizontal_step = bounch(flying_object.horizontal_step,other_flying_object.horizontal_step)
                            # if flying objects are more vertically positioned from each oter
                            else:
                                flying_object.vertical_step, other_flying_object.vertical_step = bounch(flying_object.vertical_step,other_flying_object.vertical_step)

                            # moving after bounching is not necessary, but helps to get objects not stick to each oter
                            flying_object.move()
                            flying_object.move()
                            other_flying_object.move()
                            other_flying_object.move()

                        # subtype battle
                        # if subtype is one index further in the list of subtypes, it means it is stronger
                        # special case: first item in the list is stronger than last item in the list
                        first_attacks_second(flying_object, other_flying_object)
                        first_attacks_second(other_flying_object, flying_object)

        # clean 'collisions_already_handled' for next iteration
        for flying_object in self.flying_objects:
            flying_object.collision_already_handled_ids = []                

        pygame.display.flip() # update the full display surface to the screen
        self.clock.tick(60)   # update the clock 60 times a second

    def draw(self):
        self.screen.fill((250,235,214))                   # draw work surface pink
        self.screen.blit(self.background, (0,0))    # draw background
        for flying_object in self.flying_objects:     # draw scissors
            flying_object.render()
    
    def run(self):
        while True:
            self.check_event()              # check for events
            self.update()                   # update
            self.draw()                     # draw

            