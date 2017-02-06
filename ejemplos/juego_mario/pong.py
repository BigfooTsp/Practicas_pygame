# coding=utf-8

import os

import pygame

from videogame import VideoGame

# colores
colors = {
    'bounding-box': (0, 255, 48),
    'texto': (0, 85, 212)
}

# rutas de imágenes
image_paths = {
    'mesa': os.path.join('imagenes', 'mesa.png'),
    'bola': os.path.join('imagenes', 'bola.png'),
    'paleta': os.path.join('imagenes', 'paleta.png'),
    'controles-izquierda': os.path.join('imagenes', 'controles_izquierda.png'),
    'controles-derecha': os.path.join('imagenes', 'controles_derecha.png'),
    'controles-juego': os.path.join('imagenes', 'controles_juego.png'),
}


class StaticObject(object):
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

    def draw(self, screen, dt):
        screen.blit(self.image, self.rect)


class DynamicObject(StaticObject):
    def __init__(self, image_path, speed):
        super(DynamicObject, self).__init__(image_path)
        self.speed = speed


class Pong(VideoGame):
    def __init__(self):
        super(Pong, self).__init__(title='Pong',  # título del juego
                                   width=680, height=380,  # dimensiones de la pantalla
                                   is_resizable=False,  # establece que la ventana es redimensionable
                                   max_fps=60)  # establece el máximo número de cuadros por segundo

    def initialize(self):
        self.font = pygame.font.Font(None, 22)

        # medio ancho
        hw = self.width / 2

        # media altura
        hh = self.height / 2

        # mesa
        self.table = StaticObject(image_paths['mesa'])

        # bola
        self.ball = DynamicObject(image_paths['bola'], [400, 160])
        self.ball.rect.center = (hw, hh)

        # paleta izquierda
        self.left_paddle = DynamicObject(image_paths['paleta'], [400, 400])
        self.left_paddle.rect.centery = hh
        self.left_paddle.rect.left = 40

        # paleta derecha
        self.rigth_paddle = DynamicObject(image_paths['paleta'], [400, 400])
        self.rigth_paddle.rect.centery = hh
        self.rigth_paddle.rect.right = self.width - 40

        # controles del jugador izquierdo
        self.left_controls = StaticObject(image_paths['controles-izquierda'])
        self.left_controls.rect.centerx = self.width / 4 - 20
        self.left_controls.rect.centery = hh

        # controles del jugador derecho
        self.right_controls = StaticObject(image_paths['controles-derecha'])
        self.right_controls.rect.centerx = self.width * 3 / 4 + 20
        self.right_controls.rect.centery = hh

        # controles del juego
        self.game_controls = StaticObject(image_paths['controles-juego'])
        self.game_controls.rect.centerx = hw
        self.game_controls.rect.centery = hh + 10

        # puntuación de jugador izquierdo
        self.left_score = 0

        # puntuación de jugador derecho
        self.right_score = 0

        # imagen pausa
        self.pause_image = self.font.render('Paused', True, colors['texto'])
        self.pause_rect = self.pause_image.get_rect()

        # pared superior
        self.top_wall = pygame.Rect((0, 0), (600, 10))
        self.top_wall.centerx = hw
        self.top_wall.bottom = 40

        # pared inferior
        self.bottom_wall = pygame.Rect((0, 0), (600, 10))
        self.bottom_wall.centerx = hw
        self.bottom_wall.top = 340

        # pared izquierda
        self.left_wall = pygame.Rect((0, 0), (10, 300))
        self.left_wall.centery = hh
        self.left_wall.right = 40

        # pared derecha
        self.right_wall = pygame.Rect((0, 0), (10, 300))
        self.right_wall.centery = hh
        self.right_wall.left = self.width - 40

        # pared izquierda de en medio
        self.middle_left_wall = pygame.Rect((0, 0), (10, 300))
        self.middle_left_wall.centery = hh
        self.middle_left_wall.right = 200

        # pared derecha de en medio
        self.middle_right_wall = pygame.Rect((0, 0), (10, 300))
        self.middle_right_wall.centery = hh
        self.middle_right_wall.left = 480

        # ¿mostrar bounding-boxes?
        self.show_bounding_boxes = False

        # pausa el juego
        self.pause()

    def key_pressed(self, key, modifier, scancode):
        # presiona la tecla SPACE para pausar/reanudar el juego
        if key == pygame.K_SPACE:
            self.is_paused = not self.is_paused

        # presiona la tecla ENTER para mostrar/ocultar los bounding-boxes
        if key == pygame.K_RETURN:
            self.show_bounding_boxes = not self.show_bounding_boxes

    def update_collisions(self, dt):
        # *** paleta izquierda ***

        # test de colisión de paleta izquierda con pared superior
        if self.keyboard.get(pygame.K_w):
            speed_y = self.left_paddle.speed[1]
            dy = int(speed_y * dt)
            next_move = self.left_paddle.rect.move(0, -dy)

            if not next_move.colliderect(self.top_wall):
                self.left_paddle.rect.move_ip(0, -dy)

        # test de colisión de paleta izquierda con pared inferior
        if self.keyboard.get(pygame.K_s):
            speed_y = self.left_paddle.speed[1]
            dy = int(speed_y * dt)
            next_move = self.left_paddle.rect.move(0, dy)

            if not next_move.colliderect(self.bottom_wall):
                self.left_paddle.rect.move_ip(0, dy)

        # test de colisión de paleta izquierda con pared izquierda
        if self.keyboard.get(pygame.K_a):
            speed_x = self.left_paddle.speed[0]
            dx = int(speed_x * dt)
            next_move = self.left_paddle.rect.move(-dx, 0)

            if not next_move.colliderect(self.left_wall):
                self.left_paddle.rect.move_ip(-dx, 0)

        # test de colisión de paleta izquierda con pared izquierda de en medio
        if self.keyboard.get(pygame.K_d):
            speed_x = self.left_paddle.speed[0]
            dx = int(speed_x * dt)
            next_move = self.left_paddle.rect.move(dx, 0)

            if not next_move.colliderect(self.middle_left_wall):
                self.left_paddle.rect.move_ip(dx, 0)

        # *** paleta derecha ***

        # test de colisión de paleta derecha con pared superior
        if self.keyboard.get(pygame.K_UP):
            speed_y = self.rigth_paddle.speed[1]
            dy = int(speed_y * dt)
            next_move = self.rigth_paddle.rect.move(0, -dy)

            if not next_move.colliderect(self.top_wall):
                self.rigth_paddle.rect.move_ip(0, -dy)

        # test de colisión de paleta derecha con pared inferior
        if self.keyboard.get(pygame.K_DOWN):
            speed_y = self.rigth_paddle.speed[1]
            dy = int(speed_y * dt)
            next_move = self.rigth_paddle.rect.move(0, dy)

            if not next_move.colliderect(self.bottom_wall):
                self.rigth_paddle.rect.move_ip(0, dy)

        # test de colisión de paleta derecha con pared derecha de en medio
        if self.keyboard.get(pygame.K_LEFT):
            speed_x = self.rigth_paddle.speed[0]
            dx = int(speed_x * dt)
            next_move = self.rigth_paddle.rect.move(-dx, 0)

            if not next_move.colliderect(self.middle_right_wall):
                self.rigth_paddle.rect.move_ip(-dx, 0)

        # test de colisión de paleta derecha con pared derecha
        if self.keyboard.get(pygame.K_RIGHT):
            speed_x = self.rigth_paddle.speed[0]
            dx = int(speed_x * dt)
            next_move = self.rigth_paddle.rect.move(dx, 0)

            if not next_move.colliderect(self.right_wall):
                self.rigth_paddle.rect.move_ip(dx, 0)

        # *** bola ***
        ball_dx = int(self.ball.speed[0] * dt)
        ball_dy = int(self.ball.speed[1] * dt)
        self.ball.rect.move_ip(ball_dx, ball_dy)

        # test de colisión de bola con paletas
        if self.ball.rect.colliderect(self.left_paddle.rect) or self.ball.rect.colliderect(self.rigth_paddle.rect):
            self.ball.speed[0] = -self.ball.speed[0]
            ball_dx = int(self.ball.speed[0] * dt)
            self.ball.rect.move_ip(ball_dx * 3, ball_dy)

        # test de colisión de bola con paredes
        if self.ball.rect.colliderect(self.top_wall) or self.ball.rect.colliderect(self.bottom_wall):
            self.ball.speed[1] = -self.ball.speed[1]
            ball_dy = int(self.ball.speed[1] * dt)
            self.ball.rect.move_ip(ball_dx, ball_dy * 3)

        # colisión de bola en pared izquierda
        left_collision = self.ball.rect.colliderect(self.left_wall)

        # colisión de bola en pared derecha
        right_collision = self.ball.rect.colliderect(self.right_wall)

        if left_collision:
            # si la bola colisiona en la pared izquierda, aumentar puntuación de jugador derecho
            self.right_score += 1
        if right_collision:
            # si la bola colisiona en la pared derecha, aumentar puntuación de jugador izquierdo
            self.left_score += 1

        # si la bola colisiona en la pared izquierda o derecha, restaurar el juego
        if left_collision or right_collision:
            # restaura la posición de la bola
            self.ball.rect.center = (self.width / 2, self.height / 2)
            self.ball.speed[0] = -self.ball.speed[0]

            # restaura la posición de la paleta izquierda
            self.left_paddle.rect.centery = self.height / 2
            self.left_paddle.rect.left = 40

            # restaura la posición de la paleta derecha
            self.rigth_paddle.rect.centery = self.height / 2
            self.rigth_paddle.rect.right = self.width - 40

            # pausa el juego
            self.pause()

    def draw(self, dt):
        screen = self.screen

        # dibuja la mesa
        self.table.draw(screen, dt)

        # dibuja la paleta izquierda
        self.left_paddle.draw(screen, dt)

        # dibuja la paleta derecha
        self.rigth_paddle.draw(screen, dt)

        # dibuja la bola
        self.ball.draw(screen, dt)

        # ¿mostrar bounding-boxes?
        if self.show_bounding_boxes:
            bounding_box_color = colors['bounding-box']

            # bounding-boxes de paletas
            pygame.draw.rect(screen, bounding_box_color, self.left_paddle.rect, 1)
            pygame.draw.rect(screen, bounding_box_color, self.rigth_paddle.rect, 1)

            # bounding-box de bola
            pygame.draw.rect(screen, bounding_box_color, self.ball.rect, 1)

            # bounding-boxes de paredes
            pygame.draw.rect(screen, bounding_box_color, self.top_wall, 1)
            pygame.draw.rect(screen, bounding_box_color, self.bottom_wall, 1)
            pygame.draw.rect(screen, bounding_box_color, self.left_wall, 1)
            pygame.draw.rect(screen, bounding_box_color, self.right_wall, 1)
            pygame.draw.rect(screen, bounding_box_color, self.middle_left_wall, 1)
            pygame.draw.rect(screen, bounding_box_color, self.middle_right_wall, 1)

        # ¿juego pausado?
        if self.is_paused:
            # dibuja los controles del jugador izquierdo
            self.left_controls.draw(screen, dt)

            # dibuja los controles del jugador derecho
            self.right_controls.draw(screen, dt)

            # dibuja los controles del juego
            self.game_controls.draw(screen, dt)

            # dibuja la puntuación
            score_text = '{}       {}'.format(self.left_score, self.right_score)
            score_image = self.font.render(score_text, True, colors['texto'])
            score_rect = score_image.get_rect()
            score_rect.y = 5
            score_rect.centerx = self.width / 2
            screen.blit(score_image, score_rect)

            # dibuja el mensaje de pausa
            self.pause_rect.centerx = self.width / 2
            self.pause_rect.bottom = self.height - 5
            screen.blit(self.pause_image, self.pause_rect)

        # actualiza la pantalla
        pygame.display.flip()


if __name__ == '__main__':
    Pong()