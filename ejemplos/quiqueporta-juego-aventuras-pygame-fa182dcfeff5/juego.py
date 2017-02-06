# -*- coding: utf-8 -*-

import pygame

from gamemanager.gamemanager import GameManager
from gamemanager.states.menustate import MenuState
from gamemanager.fpsclock import FpsClock
 
if __name__ == "__main__":
 
    game = GameManager("Estados Juego Python", (640, 480), False)
    game.changeState(MenuState(game))
    fps = FpsClock(35, 0)
 
    while game.running:
        game.handleEvents(pygame.event.get())
        game.update()
        game.draw()
        fps.tick()
        
    game.cleanUp()
