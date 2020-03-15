# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:39:27 2020

@author: letic
"""


import kivy

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import choice
import pandas as pd
import numpy as np
from kivy.core.window import Window


class Ball(Widget):

    
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    angle = 0.5
    elast = .005
    vel = 0
    def move(self):
        # r = Vector(self.center) - Vector(self.parent.center)
        # raio = np.linalg.norm(r)
        # print("posicao bola {}, posicao parent {}, raio {}".format(self.center, self.parent.center, raio))
        # self.center_x = int(self.center_x - self.parent.center_x + raio*np.cos(self.angle)) + self.parent.center_x
        # self.center_y = int(self.center_y - self.parent.center_y - raio*np.sin(self.angle)) + self.parent.center_y
        dist = self.center_y - self.parent.center_y
        self.vel -= self.elast * dist
        self.center_y += self.vel

        

class Jogador(Widget):
    
    player = NumericProperty(0)

    def check_colisao(self,balls):
        for ball in balls:
            if self.collide_widget(ball):
                self.center_y = self.parent.center_y
                self.center_x = 0
                return True
        return False


class Caminho(Widget):

    pass
    
    

class Jogo(Widget):
    
    ball = ObjectProperty()
    player = ObjectProperty()
    bolas = []
    step_player = 6



    def __init__(self, **kwargs):
        super(Jogo, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        num_bolas = kwargs['num_bolas']
        MARGEM_TOP = 50
        MARGEM_LADO = 100
        
        step = (1000 - 2*MARGEM_LADO)/num_bolas
        print(self.size)

        for i in range(num_bolas):
            if i % 2 == 0:
                setattr(self, 'ball_{}'.format(i), Ball(center_x=MARGEM_LADO+step*i, center_y=Window.height-MARGEM_TOP))
            else:
                setattr(self, 'ball_{}'.format(i), Ball(center_x=MARGEM_LADO+step*i, center_y=MARGEM_TOP))
            bola = getattr(self,'ball_{}'.format(i),None)
            self.bolas.append(getattr(self,'ball_{}'.format(i),None))
            self.add_widget(bola)



    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.player.center_x -= self.step_player
        elif keycode[1] == 'right':
            self.player.center_x += self.step_player
        elif keycode[1] == 'up':
            self.player.center_y += self.step_player
        elif keycode[1] == 'down':
            self.player.center_y -= self.step_player
        return True

    def calcula_pos(self):
        decisoes = ['up', 'right', 'down', 'stop']
        return choice(decisoes)

    def move_player(self):
        direcao = self.calcula_pos()

        if direcao == 'up':
            self.player.center_y += self.step_player
        elif direcao == 'right':
            self.player.center_x += self.step_player
        elif direcao == 'down':
            self.player.center_y -= self.step_player
        elif direcao == 'stop':
            pass

        if self.player.check_colisao(self.bolas):
            reward = -1
        else:
            reward = 1

    def update(self, dt):

        self.move_player()

        for ball in self.bolas:
            ball.move()

        

        if self.player.right > self.width:
            self.player.center_y = self.center_y
            self.player.center_x = 0
        
                

class JogoApp(App):
    def build(self):
        jogo = Jogo(num_bolas=8)
        Clock.schedule_interval(jogo.update, 1.0/60.0) 
        return jogo


if __name__ == '__main__':
    JogoApp().run()