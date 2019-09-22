# -*- coding: utf8 -*-

def art():
    from PIL import Image

    img = Image.open(r"D:\GoogleDrive\Hacking\HTB\Challenges\art.png")

    c = [(0, 0), (290, 0), (290, 290), (0, 290), (0, 20)]

    # Recorre cuadro
    X, Y = 0, 1

    origen = 0, 0
    tamano = img.width, img.height
    salto = 10
    actual = origen
    cuadro = 1

    while True:
        print "Inicio de ciclo"
        # Fila superior
        cY = origen[Y] # Como es fila, la Y es fija
        for i in xrange(origen[X], tamano[X] + origen[X], salto):
            coord_pixel = (i, cY)
            print "{}-{}: {}".format(cuadro, coord_pixel, img.getpixel(coord_pixel))
            cuadro += 1
        # Columna derecha
        cX = tamano[X] + origen[X] - 10 # Como es columna, la X es fija
        for i in xrange(origen[Y] + 10, tamano[Y] + origen[Y], salto):
            coord_pixel = (cX, i)
            print "{}-{}: {}".format(cuadro, coord_pixel, img.getpixel(coord_pixel))
            cuadro += 1

        # Fila inferior
        cY = tamano[Y] + origen[Y]- 10
        for i in xrange(tamano[X] + origen[X] - 20, origen[X] - 10, -salto):
            coord_pixel = (i, cY)
            print "{}-{}: {}".format(cuadro, coord_pixel, img.getpixel(coord_pixel))
            cuadro += 1

        # Columna izquierda
        cX = origen[X]
        for i in xrange(tamano[Y] + origen[Y] - 20, origen[Y] + 10, -salto):
            coord_pixel = (cX, i)
            print "{}-{}: {}".format(cuadro, coord_pixel, img.getpixel(coord_pixel))
            cuadro += 1

        # Lee pixel suelto que queda a la derecha, debido a la fila negra que dibuja la espiral (espacio), y
        # así deja el punto de entrada igual, pero con una espiral menor
        coord_pixel = origen[X] + 10, origen[Y] + 20
        print "{}-{}: {}".format(cuadro, coord_pixel, img.getpixel(coord_pixel))
        cuadro += 1

        # Ajustamos variables para siguiente iteración de la espiral
        origen = origen[X] + 20, origen[Y] + 20
        tamano = tamano[X] - 40, tamano[Y] - 40
        if tamano[X] == 20:
            # Hemos terminado, lee tres cuadros restantes y sale
            origenn = [(origen[X], origen[Y]), (origen[X] + 10, origen[Y]), (origen[X] + 10, origen[Y] + 10)]

            for i in xrange(3):
                coord_pixel = origenn[i]
                print "{}-{}: {}".format(cuadro, coord_pixel, img.getpixel(coord_pixel))
                cuadro += 1

            break

def blue_shadow():
    import requests
    import bs4

    r = requests.get("https://twitter.com/blue_shad0w_?lang=es")
    pagina = bs4.BeautifulSoup(r, "html.parser")

def deadly_arthropod():
    newmap = {
        2:"PostFail",
        4: "a",
        5: "b",
        6: "c",
        7: "d",
        8: "e",
        9: "f",
        10: "g",
        11: "h",
        12: "i",
        13: "j",
        14: "k",
        15: "l",
        16: "m",
        17: "n",
        18: "o",
        19: "p",
        20: "q",
        21: "r",
        22: "s",
        23: "t",
        24: "u",
        25: "v",
        26: "w",
        27: "x",
        28: "y",
        29: "z",
        30: "1",
        31: "2",
        32: "3",
        33: "4",
        34: "5",
        35: "6",
        36: "7",
        37: "8",
        38: "9",
        39: "0",
        40: "Enter",
        41: "esc",
        42: "del",
        43: "tab",
        44: "space",
        45: "_",
        46: "=",
        47: "{",
        48: "}",
        49: "\\",
        52: "\'",
        54: ",",
        55: ".",
        56: " / ",
        57: "CapsLock",
        79: "RightArrow",
        80: "LetfArrow"
    }

    my_keys = open(r"D:\Descargas\htb\Forense\datos.txt")
    pos = 0
    cad = ""
    i = 1

    for line in my_keys:
        bytes_array = bytearray.fromhex(line.strip())
        # print "Line Number: " + str(i)
        for byte in bytes_array:
            key_val = None
            if byte != 0:
                key_val = int(byte)

                descartados = (2,0)
                if key_val in newmap:
                    # print "Value map : " + str(keyVal) + " — -> " + newmap[keyVal]
                    if key_val not in descartados:
                        if key_val == 79:
                            pos += 1
                        elif key_val == 80:
                            pos -= 1
                        else:
                            cad = cad[:pos] + newmap[key_val] + cad[pos:]
                            pos += 1
                        # print newmap[key_val],
                else:
                    if key_val not in descartados:
                        print "No map found for this value: " + str(key_val)

        # print format(byte, ‘02X’)
        i += 1
    print "Cadena: ", cad
    print "CadenaMayus: ", cad.upper()


if __name__ == "__main__":
    deadly_arthropod()


