# -*- coding: utf8 -*-
import webbrowser
import requests
import re

class PythonChallenge:
    @staticmethod
    def level_0():
        # URL de inicio http://www.pythonchallenge.com/pc/def/0.html
        # Hay que sustituir el 0 por el resultado
        valor = 2**38
        # Abre la URL resuelta, que consiste en sustituir 0 por la solución
        webbrowser.open("http://www.pythonchallenge.com/pc/def/{}.html".format(str(valor)))

    @staticmethod
    def level_1():
        # URL de inicio http://www.pythonchallenge.com/pc/def/map.html
        # Hay que sustituir map por el resultado

        # Se lee la cadena cifrada
        r = requests.get("http://www.pythonchallenge.com/pc/def/map.html")
        # Extrae el criptograma, quitando retornos de carro
        criptograma = str(re.findall('<font color=\"\#f000f0\">(.*?)</tr></td>', r.text, re.DOTALL)[0]).strip()

        # El cifrado es un cifrado de césar, desplazando 2 posiciones, por lo que para descifrar,
        # podemos usar maketrans, que funciona de forma muy similar al comando de linux tr
        import string
        alfabeto_entrada = string.ascii_lowercase # abcdefghijklmnopqrstuvwxyz
        alfabeto_salida = alfabeto_entrada[2:] + alfabeto_entrada[:2] # Se puede cambiar el 2, para cambiar el desplazamiento
        tabla = string.maketrans(alfabeto_entrada, alfabeto_salida)
        texto = criptograma.translate(tabla)
        print "Criptograma:", criptograma
        print "Texto:", texto

        # Abre la URL resuelta, que consiste en cambiar map aplicando el algoritmo anterior:
        webbrowser.open("http://www.pythonchallenge.com/pc/def/{}.html".format("map".translate(tabla)))

    @staticmethod
    def level_2():
        # URL de inicio http://www.pythonchallenge.com/pc/def/ocr.html
        # Hay que sustituir ocr por el resultado

        # Se lee la cadena cifrada
        r = requests.get("http://www.pythonchallenge.com/pc/def/ocr.html")
        # Extrae el criptograma, quitando retornos de carro
        entrada = str(re.findall("<!--(.*?)-->", r.text, re.DOTALL)[-1]).strip()

        # Para contar las frecuencias de cada aparición
        frecuencias = dict()
        for caracter in entrada:
            frecuencias[caracter] = frecuencias.get(caracter, 0) + 1    # Suma 1 a ese caracter
        print frecuencias

        # Hay que descartar todos los caracteres, nos quedamos sólo con las letras.
        texto = "".join(re.findall("[a-z]", entrada))
        print "Texto:", texto

        # Abre la URL resuelta:
        webbrowser.open("http://www.pythonchallenge.com/pc/def/{}.html".format(texto))

    @staticmethod
    def level_3():
        # URL de inicio http://www.pythonchallenge.com/pc/def/equality.html
        # Hay que sustituir equality por el resultado

        # Se lee la cadena cifrada
        r = requests.get("http://www.pythonchallenge.com/pc/def/equality.html")
        # Extrae el criptograma, quitando retornos de carro
        entrada = str(re.findall("<!--(.*?)-->", r.text, re.DOTALL)[-1]).strip()

        # Hay que obtener las letras minúsculas rodeadas por 3 mayúsculas a cada lado: oOOOxOOOo
        texto = "".join(re.findall("[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]", entrada))
        print "Texto:", texto

        # Abre la URL resuelta:
        webbrowser.open("http://www.pythonchallenge.com/pc/def/{}.html".format(texto))

    @staticmethod
    def level_4(nothing):
        # type: (nothing) -> str
        # URL de inicio http://www.pythonchallenge.com/pc/def/linkedlist.html
        # Hay que sustituir linkedlist.html por el resultado

        # Sanitiza entrada
        nothing = str(nothing)

        # El punto de entrada indica que es linkedlist.php?nothing=12345, y como resultado obtendremos un texto con el
        # siguiente valor de nothing, hasta obtener una web
        # Puede fallar, porque según la lista que coja (puede coger varias), puede pedir hacer algo distinto
        # En una de las ejecuciones, el texto fue "Divide este número entre dos y continúa"

        salir = False
        patron = re.compile("next nothing is (\d+)")
        while not salir:
            print "Abriendo: " + nothing,
            r = requests.get("http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=" + nothing)
            texto = r.text
            print texto

            ocurrencia = patron.search(texto)
            if ocurrencia is None:  # Si no ha encontrado el número
                salir = True   # Hemos encontrado condición de salida, r.text contiene la URL
            else:
                nothing = ocurrencia.group(1)

        print "Texto:", texto

        # Abre la URL resuelta:
        webbrowser.open("http://www.pythonchallenge.com/pc/def/{}".format(texto))

    @staticmethod
    def level_5():
        # URL de inicio http://www.pythonchallenge.com/pc/def/peak.html
        # Hay que sustituir peak por el resultado

        # Deserializa con pickle los datos en el archivo banner.p, según indica el código de la página
        r = requests.get("http://www.pythonchallenge.com/pc/def/banner.p")
        import pickle
        datos = pickle.loads(r.text)
        # Imprime el mensaje, que es channel en mapa de caracteres (mapa de bits, pero con caracteres)
        for linea in datos:
            print "".join(k * v for k, v in linea)

        # Abre la URL resuelta:
        webbrowser.open("http://www.pythonchallenge.com/pc/def/{}.html".format("channel"))

    @staticmethod
    def level_6():
        # URL de inicio http://www.pythonchallenge.com/pc/def/channel.html
        # Hay que sustituir linkedlist.html por el resultado

        # Hay que descargar un fichero zip, saca el contenido, y luego lo borra:
        r = requests.get("http://www.pythonchallenge.com/pc/def/channel.zip")
        import io, zipfile
        zip_content = zipfile.ZipFile(io.BytesIO(r.content))

        # Lee el archivo readme, para sacar el primer archivo a seguir
        a = zip_content.open("readme.txt")
        nothing = a.readlines()[2].strip().rpartition(" ")[2] + ".txt"

        salir = False
        colecta_comentarios = ""
        patron = re.compile("Next nothing is (\d+)")
        while not salir:
            print "Abriendo: " + nothing,
            a = zip_content.open(nothing)
            colecta_comentarios += zip_content.getinfo(nothing).comment
            texto = a.readline()
            print texto

            ocurrencia = patron.search(texto)
            if ocurrencia is None:  # Si no ha encontrado el número
                salir = True  # Hemos encontrado condición de salida, r.text contiene la URL
            else:
                nothing = ocurrencia.group(1) + ".txt"

        # Llegados a este punto, se consigue un mensaje "Collect the comments", se miran los comentarios del ZIP
        print colecta_comentarios
        # Abre la URL resuelta:
        webbrowser.open("http://www.pythonchallenge.com/pc/def/{}.html".format("hockey"))

def abre_la_cancion(num):
    if num == 1:
        webbrowser.open("https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwiC-MqfteveAhUKY6wKHUg6BBMQyCkwAHoECAUQBA&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DixMUdYubMHk&usg=AOvVaw0cRPXj6eoxFz90lbWeSzkT")
    elif num == 2:
        webbrowser.open("https://www.youtube.com/watch?v=BGa3AqeqRy0")
