# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:39:27 2020

@author: letic
"""
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1500')
Config.set('graphics', 'height', '800')

import kivy

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint, uniform
import pandas as pd
import numpy as np
from kivy.core.window import Window

from modelos import posiciona_player, salva_dados

class Ball(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    vel_y = 0
    vel_x = 0
    def move(self, gravidade, vento):
        self.vel_y -= gravidade
        self.center_y += self.vel_y

        self.vel_x += vento
        self.center_x += self.vel_x


class Obstaculo(Widget):

    tocou = False
    
    def bounce_ball(self, bola):
        if self.collide_widget(bola) and not(self.tocou):
            dif_x = bola.x - self.x
            dif_y = bola.y - self.y
            norm = np.linalg.norm((dif_x,dif_y))
            bola.vel_x *= (dif_x/norm).item()
            bola.vel_y *= -(dif_y/norm).item()
            self.tocou = True

        
class Jogador(Widget):
    
    player = NumericProperty(0)
    flag_win = False

    def check_colisao(self,bola):
        if self.collide_widget(bola):
            self.flag_win = True
            return True
        return False

class Barra(Widget):
    pass

class Vento(Widget):
    def __init__(self, **kwargs):
        super(Vento, self).__init__(**kwargs)
        self.vel_x = 30*uniform(1,1.5)
    def move(self):        
        self.center_x += self.vel_x
        if self.center_x > self.parent.width:
            self.center_x = 0
            self.y = self.parent.height*uniform(0,1)
            self.vel_x = 30*uniform(1,1.5)

class Jogo(FloatLayout):
    
    ball = ObjectProperty()
    player = ObjectProperty()
    wins = ObjectProperty()
    jogos = ObjectProperty()
    percent = ObjectProperty()
    obst1 = ObjectProperty()
    obst2 = ObjectProperty()
    obst3 = ObjectProperty()
    obst4 = ObjectProperty()
    bolas = []
    step_player = 10
    gravidade = 0.08
    
    num_ventinhos = 15

    num_jogos = 0
    num_wins = 0
    vento = 0

    infos = []
    
    def __init__(self, **kwargs):
        super(Jogo, self).__init__()
        self._keyboard = Window.request_keyboard(None, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        for i in range(self.num_ventinhos):
                    setattr(self,'ventinho_{}'.format(i), Vento(x=0,y=self.height*uniform(0,1)))
                    self.add_widget(getattr(self,'ventinho_{}'.format(i)))
        Clock.schedule_interval(self.update, 1.0/60.0)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.player.center_x -= self.step_player
        elif keycode[1] == 'right':
            self.player.center_x += self.step_player
        elif keycode[1] == 'spacebar':
            Clock.schedule_interval(self.fisica, 1.0/60.0)
        elif keycode[1] == 'p':
            Clock.unschedule(self.fisica)
        elif keycode[1] == 'enter':
            if not(getattr(self,'bola',None)):
                self.inicializa_jogo()
                
    def att_labels(self):
        self.label_vento.text = 'Vento: {:.2f}'.format(self.vento*100)
        self.wins.text = 'Wins: {}'.format(self.num_wins)
        self.jogos.text = 'Jogos: {}'.format(self.num_jogos)
        self.percent.text = 'Acertos: {:.1f}%'.format(((self.num_wins/self.num_jogos) if self.num_jogos != 0 else 0)*100)

    def inicializa_jogo(self, **kwargs):
        self.vento = uniform(0,0.07)
        self.bola = Ball(center_x=randint(50,800), center_y=self.height)
        self.add_widget(self.bola)
        self.infos = [i for i in [self.bola.x, self.vento, self.gravidade, self.height]]
        self.player.center_x = posiciona_player(self.bola.x, self.vento, self.gravidade, self.height)
        self.att_labels()

    def fisica(self, dt):
        self.bola.move(self.gravidade, self.vento)
        self.obst1.bounce_ball(self.bola)
        self.obst2.bounce_ball(self.bola)
        self.obst3.bounce_ball(self.bola)
        self.obst4.bounce_ball(self.bola)
        self.player.check_colisao(self.bola)
        if self.bola.y < 0:
            self.infos.append(self.bola.x)
            salva_dados(self.infos)
            self.num_jogos += 1
            if self.player.flag_win:
                self.num_wins += 1
                self.player.flag_win = False
#            Clock.unschedule(self.fisica)
            self.remove_widget(self.bola)
            self.inicializa_jogo()
            self.obst1.tocou = False
            self.obst2.tocou = False
            self.obst3.tocou = False
            self.obst4.tocou = False
    
    def update(self, dt):
        for i in range(self.num_ventinhos):
            ventinho = getattr(self, 'ventinho_{}'.format(i))
            ventinho.move()
                

class JogoApp(App):
    def build(self):
        jogo = Jogo()
        return jogo


if __name__ == '__main__':
    JogoApp().run()
