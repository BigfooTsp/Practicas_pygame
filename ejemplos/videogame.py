# coding=utf-8

# importa la librería Pygame
import pygame


class VideoGame(object):
    """
    Provee las funcionalidades mínimas que posee un videojuego.
    """

    def __init__(self, title='', width=300, height=300, is_resizable=False, fullscreen=False, max_fps=60):
        # título de ventana
        self.title = title

        # dimensiones de ventana
        self.width, self.height = width, height

        # ¿es redimensionable la ventana?
        self.is_resizable = is_resizable

        # ¿pantalla completa?
        self.fullscreen = fullscreen

        # máximos cuadros por segundo (FPS: frames per second)
        self.max_fps = max_fps

        # reloj
        self.clock = pygame.time.Clock()

        # lista de eventos
        self.events = []

        # lista de teclas pulsadas
        self.keyboard = {}

        # bandera usada para disparar el evento 'mouse_dragged()'
        self.is_dragged = False

        # ¿videojuego en marcha?
        self.is_running = True

        # ¿videojuego pausado?
        self.is_paused = False

        # inicializa Pygame
        pygame.init()

        # establece el título de ventana
        pygame.display.set_caption(self.title)

        # establece si la ventana es redimensionable
        if self.is_resizable:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))

        # inicializa el videojuego
        self.initialize()

        # bucle principal del videojuego (maneja los eventos, actualizaciones de estado y dibujos)
        self.main_loop()

        # finaliza el videojuego
        self.finalize()

        # finaliza Pygame
        pygame.quit()

    def initialize(self):
        """
        Este método se usará para inicilializar el videojuego
        """
        pass

    def finalize(self):
        """
        Este método se usará para finalizar el videojuego
        """
        pass

    def pause(self):
        """
        Pausa el videojuego
        """
        self.is_paused = True

    def unpause(self):
        """
        Reanuda el videojuego
        """
        self.is_paused = False

    def key_pressed(self, key, modifier, scancode):
        """
        Este método se usará cuando una tecla es presionada
        """
        pass

    def key_released(self, key, modifier, scancode):
        """
        Este método se usará cuando una tecla es soltada
        """
        pass

    def mouse_pressed(self, button, (x, y)):
        """
        Este método se usará cuando un botón del mouse es presionado
        """
        pass

    def mouse_released(self, button, (x, y)):
        """
        Este método se usará cuando un botón del mouse es soltado
        """
        pass

    def mouse_moved(self, buttons, (x, y), (dx, dy)):
        """
        Este método se usará cuando el mouse es movido
        """
        pass

    def mouse_dragged(self, botones, (x, y), (dx, dy)):
        """
        Este método se usará cuando el mouse arrastra algo
        """
        pass

    def update_physics(self, dt):
        """
        Este método se usará para actualizar la física en el videojuego
        """
        pass

    def update_collisions(self, dt):
        """
        Este método se usará para actualizar las colisiones en el videojuego
        """
        pass

    def update_ai(self, dt):
        """
        Este método se usará para actualizar la inteligencia artificial en el videojuego
        """
        pass

    def update(self, dt):
        self.update_physics(dt)
        self.update_ai(dt)
        self.update_collisions(dt)

    def draw(self, dt):
        """
        Este método se usará para dibujar todos los objetos visibles en el videojuego
        """
        pass

    def resize(self, width, height):
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False

        if event.type == pygame.KEYDOWN:
            self.keyboard[event.key] = True

            # finaliza el videojuego al presionar la tecla ESCAPE o la combinación de teclas ALT + F4
            if event.key == pygame.K_ESCAPE:
                self.is_running = False
            if event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                self.is_running = False

            # cambia de modo pantalla completa/ventana al presionar la combinación de teclas ALT + F5
            if event.key == pygame.K_F5 and (event.mod & pygame.KMOD_ALT):
                self.fullscreen = not self.fullscreen

                if self.fullscreen:
                    # pantalla completa
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

                    # oculta el cursor del mouse
                    pygame.mouse.set_visible(False)
                else:
                    # ventana
                    self.screen = pygame.display.set_mode((self.width, self.height))

                    # muestra el cursor del mouse
                    pygame.mouse.set_visible(True)

            self.key_pressed(event.key, event.mod, event.scancode)

        if event.type == pygame.KEYUP:
            self.keyboard[event.key] = False

            self.key_released(event.key, event.mod, event.scancode)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pressed(event.button, event.pos)
            self.is_dragged = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_released(event.button, event.pos)
            self.is_dragged = False

        if event.type == pygame.MOUSEMOTION:
            self.mouse_moved(event.buttons, event.pos, event.rel)
            if self.is_dragged:
                self.mouse_dragged(event.buttons, event.pos, event.rel)

        if event.type == pygame.VIDEORESIZE:
            self.resize(*event.size)

    def main_loop(self):
        """
        Bucle principal del videojuego (maneja los eventos, actualizaciones de estado y dibujos).
        """
        while self.is_running:
            # fracción de tiempo
            dt = self.clock.tick(self.max_fps) / 1000.0

            # obtiene todos los eventos de la cola de eventos
            for event in pygame.event.get():
                self.handle_event(event)

            # actualiza el estado del videojuego si no está pausado
            if not self.is_paused:
                self.update(dt)

            # dibujar los objetos visibles
            self.draw(dt)

            # muestra el número de cuadros por segundo (FPS) en el título de la ventana
            pygame.display.set_caption('{} (FPS: {:.1f})'.format(self.title, self.fps()))

    def fps(self):
        """
        Retorna el número de cuadros por segundo (FPS) actual
        """
        return self.clock.get_fps()


class VideoGameDemo(VideoGame):
    def __init__(self):
        super(VideoGameDemo, self).__init__(title='Videojuego Demo',  # título del videojuego
                                            width=400, height=400,  # dimensiones de la pantalla
                                            is_resizable=True,  # establece que la ventana es redimensionable
                                            max_fps=30)  # establece el máximo número de cuadros por segundo

    def initialize(self):
        # color de fondo
        self.background_color = (0, 130, 200)

    def draw(self, dt):
        # cambia el color de fondo
        self.screen.fill(self.background_color)

        # actualiza la pantalla
        pygame.display.flip()


if __name__ == '__main__':
    VideoGameDemo()