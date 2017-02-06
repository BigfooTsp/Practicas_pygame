# coding=utf-8

import json
import os
from collections import OrderedDict

# importa la librería Pygame
import pygame


class JSON:
    """
    Abre archivos JSON.
    """

    @staticmethod
    def open(path, encoding='utf-8', preserve_order=False):
        """
        Abre un archivo JSON y retorna una lista (list) o un diccionario (dict).
        """
        object_pairs_hook = None
        # preserva el orden de ingreso de los atributos-valores
        if preserve_order:
            object_pairs_hook = OrderedDict
        with open(path) as f:
            return json.load(f, encoding=encoding, object_pairs_hook=object_pairs_hook)


class TiledLayer:
    """
    Representa una capa (layer).
    Puede extraer las propiedades de una capa dentro del archivo JSON generado con 'Tiled'. Las capas se encuentra en
    una lista llamada "layers".

    Nota:
    Para el renderizado del tilemap, solo algunas propiedades de la capa (layer) son cargadas.
    """

    def __init__(self, node):
        # almacena los tiles
        self.tiles = []

        # almacena los tiles en orden
        self.arranged_tiles = {}

        # nombre de la capa
        self.name = ''

        # opacidad
        self.opacity = 1

        # visibilidad
        self.visible = True

        # extrae las propiedades de la capa (layer)
        self.__load(node)

    def __load(self, node):
        """
        Extrae las propiedades de la capa (layer).
        """

        self.tiles = node['data']
        self.name = node['name']
        self.opacity = node['opacity']
        self.visible = node['visible']


class TiledTileset:
    """
    Representa un tileset.
    Puede extraer las propiedades de un tileset dentro del archivo JSON generado con 'Tiled'. Los tilesets se encuentra
    en una lista llamada "tilesets".

    Nota:
    Para nuestros propósitos, asumimos que las propiedades 'tilewidth' y 'tileheight' del tileset son las mismas
    que las propiedades del mismo nombre del tilemap.
    """

    def __init__(self, node, path):
        # primer id global del tileset
        self.firstgid = 0

        # ruta de la imagen
        self.image_path = ''

        # margen externo del tileset
        self.margin = 0

        # espaciamiento entre tiles
        self.spacing = 0

        # extrae las propiedades del tileset
        self.__load(node, path)

    def __load(self, node, path):
        """
        Extrae las propiedades del tileset.
        """

        self.firstgid = node['firstgid']
        self.margin = node['margin']
        self.spacing = node['spacing']

        # convierte la ruta de la imagen en una ruta relativa al proyecto
        directory = os.path.dirname(path)
        self.image_path = os.path.join(directory, *node['image'].split(r'\/'))
        self.image_path = os.path.normpath(self.image_path)


class TiledJSONTilemap:
    """
    Abre mapas creados en 'Tiled' y exportados en formato JSON.
    """

    def __init__(self, path):
        # ancho y alto del tilemap
        self.width = 0
        self.height = 0

        # ancho y alto de los tiles
        self.tilewidth = 0
        self.tileheight = 0

        # lista de tilesets, capas (layers) y sprites
        self.tilesets = []
        self.layers = []
        self.tiles = {}

        # rectángulo que ocupa el tilemap
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.open(path)

    def open(self, path):
        """
        Extrae las propiedades del tilemap.
        """

        # abre el tilemap en formato JSON
        data = JSON.open(path)

        # número de tiles en 'x' y 'y'
        self.width = data['width']
        self.height = data['height']

        # ancho y alto de los tiles
        self.tilewidth = data['tilewidth']
        self.tileheight = data['tileheight']

        # calcula las dimensiones del tilemap en pixeles
        self.rect.w = self.width * self.tilewidth
        self.rect.h = self.height * self.tileheight

        # extrae los tilesets
        tilesets = self.tilesets
        for tileset_node in data['tilesets']:
            tileset = TiledTileset(tileset_node, path)
            tilesets.append(tileset)
            self.split_tileset(tileset)

        # extrae las capas (layers)
        layers = self.layers
        for layer_node in data['layers']:
            layer = TiledLayer(layer_node)
            layers.append(layer)
            self.arrange_tiles(layer)

    def split_tileset(self, tileset):
        """
        Divide el tileset en tiles que pueden ser accedidos mediante una fila y una columna.
        """

        tiles = self.tiles
        firstgid = tileset.firstgid
        tilewidth = self.tilewidth
        tileheight = self.tileheight
        margin = tileset.margin

        # carga la imagen del tileset y obtiene sus dimensiones
        image = pygame.image.load(tileset.image_path).convert_alpha()
        image_width, image_height = image.get_size()

        # calcula el número de columnas
        cols = image_width // tilewidth

        # calcula el espaciamiento entre cada tile en cada eje
        tx = tilewidth + tileset.spacing
        ty = tileheight + tileset.spacing

        # calcula la máxima distancia a iterar en cada eje
        max_y = image_height - tileheight + 1
        max_x = image_width - tilewidth + 1

        # divide una imagen en tiles
        for row, y in enumerate(xrange(margin, max_y, ty)):
            for col, x in enumerate(xrange(margin, max_x, tx)):
                tile = image.subsurface((x, y, tilewidth, tileheight))
                tiles[firstgid + row * cols + col] = tile

    def arrange_tiles(self, layer):
        """
        Ordena una lista de tiles en un diccionario donde pueden ser accedidos mediante una fila y una columna.
        """

        # número de tiles en 'x'
        width = self.width
        arranged_tiles = layer.arranged_tiles

        row = -1

        # convierte una lista en un diccionario
        for col, tile in enumerate(layer.tiles):
            # calcula la ubicación en dos dimensiones (fila y columna) de cada tile,
            # los tiles originalmente están ordenados en línea
            col %= width
            if col == 0:
                row += 1

            # excluye los tiles con id 0,
            # id 0 representa un espacio vacío en el tilemap
            if tile != 0:
                arranged_tiles[(row, col)] = tile

        # libera la memoria ocupada por la lista de tiles
        layer.tiles = None

    def draw(self, screen, camera):
        """
        Dibuja solo los tiles dentro del campo visual de la cámara.
        """

        tilewidth = self.tilewidth
        tileheight = self.tileheight
        tiles = self.tiles

        # si el rectángulo que ocupa el tilemap no se encuentra en el campo visual de la cámara, no se dibuja nada
        if not camera.colliderect(self.rect):
            return

        # calcula la región del tilemap que es visible
        max_left = max(camera.left, self.rect.left)
        min_right = min(camera.right, self.rect.right) + tilewidth
        max_top = max(camera.top, self.rect.top)
        min_bottom = min(camera.bottom, self.rect.bottom) + tileheight

        # itera a través de todas las capas del tilemap
        for layer in self.layers:
            # no dibuja las capas ocultas
            if not layer.visible:
                continue

            arranged_tiles = layer.arranged_tiles

            # itera a través de todos los tiles visible en el eje 'y'
            for y in xrange(max_top, min_bottom, tileheight):
                # calcula la fila actual
                row = y // tileheight

                # itera a través de todos los tiles visible en el eje 'x'
                for x in xrange(max_left, min_right, tilewidth):
                    # calcula la columna actual
                    col = x // tilewidth

                    # itera a través de todos los tiles de la capa actual
                    if (row, col) in arranged_tiles:
                        # obtiene el id del tile
                        tile_id = arranged_tiles[(row, col)]

                        # dibuja solo los tiles dentro del campo visual de la cámara
                        screen.blit(tiles[tile_id], (-camera.x + col * tilewidth, -camera.y + row * tileheight))


# colores
black = (0, 0, 0)


def main():
    # inicializa Pygame
    pygame.init()

    # crea una ventana redimensioable y establece sus propiedades
    screen_width, screen_height = 640, 640
    pygame.display.set_caption('Tiled tilemap ({} x {})'.format(screen_width, screen_height))  # título
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # tamaño

    # crea un tilemap a partir de un archivo JSON creado con 'Tiled'
    tilemap = TiledJSONTilemap(os.path.join('tilemaps', 'checkers.json'))

    # crea y centra el campo visual de la cámara
    camera = pygame.Rect(0, 0, screen_width, screen_height)
    camera.center = tilemap.rect.center

    # bucle principal (maneja los eventos)
    while True:
        # retorna un solo evento de la cola de eventos
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            # detiene el bucle cuando el botón CERRAR de la ventana es presionado
            break
        elif event.type == pygame.KEYDOWN:
            # detiene el bucle cuando la tecla ESCAPE es presionada
            if event.key == pygame.K_ESCAPE:
                break
            # centra la cámara cuando la tecla RETURN es presionada
            if event.key == pygame.K_RETURN:
                camera.center = tilemap.rect.center
        elif event.type == pygame.MOUSEMOTION:
            # mueve la cámara cuando se arrastra el mouse con su BOTÓN IZQUIERDO presionado
            if event.buttons[0] == 1:
                dx, dy = event.rel
                camera.x -= dx
                camera.y -= dy

        # redimensiona la ventana y el campo de visualización de la cámara
        elif event.type == pygame.VIDEORESIZE:
            # obtiene el nuevo tamaño de la ventana
            new_size = event.size

            # redimensiona la ventana y actualiza su título
            screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)
            pygame.display.set_caption('Tiled tilemap ({} x {})'.format(*new_size))

            # redimensiona y centra la cámara
            camera.size = new_size
            camera.center = tilemap.rect.center

        # establece el color de fondo
        screen.fill(black)

        # dibuja el tilemap
        tilemap.draw(screen, camera)

        # actualiza la pantalla
        pygame.display.flip()

    # finaliza Pygame
    pygame.quit()


if __name__ == '__main__':
    main()