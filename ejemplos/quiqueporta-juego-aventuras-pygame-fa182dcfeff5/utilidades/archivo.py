def extraer_nombre(ruta):
    ''' Extra el nombre de un archivo de una ruta. '''
    a = -1
    for i in range(len(ruta)):
        if ruta[i] == "/" or ruta[i] == "\\":
            a = i
    if a == -1:
        return ruta
    return ruta[a + 1:]