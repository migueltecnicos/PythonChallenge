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
        # Hay que sustituir channel.html por el resultado

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
        webbrowser.open("http://www.pythonchallenge.com/pc/def/{}.html".format("oxygen"))

    @staticmethod
    def level_7():
        # URL de inicio http://www.pythonchallenge.com/pc/def/oxygen.html
        # Hay que sustituir oxygen por el resultado

        # Descarga la imagen
        r = requests.get("http://www.pythonchallenge.com/pc/def/oxygen.png")

        # La carga con pillow
        from PIL import Image
        from io import BytesIO
        img = Image.open(BytesIO(r.content))

        # Extrae el mensaje oculto en los píxeles, quitando duplicados mediante el acceso por índices
        indices = [0] + range(5, img.width, 7)
        msg = "".join(chr(img.getpixel((x, img.height / 2))[0]) for x in indices)
        print "Mensaje extraido:", msg

        # El mensaje anterior contiene la solución también codificada, la descodifica
        import ast
        a = re.findall("\[(.*?)\]", msg, re.DOTALL)[0]
        solucion = "".join(chr(x) for x in ast.literal_eval(a)) # Convierte la representación textual de la lista, en lista
        print a, "-->", solucion

        # Otra opción para extraer la lista de números desde msg y convertirla a caracteres:
        solucion = "".join((map(chr, map(int, re.findall("\d+", msg)))))
        print "Segunda opción:", solucion

        # Abre la URL resuelta:
        webbrowser.open("http://www.pythonchallenge.com/pc/def/{}.html".format(solucion))

    @staticmethod
    def level_8():
        # URL de inicio http://www.pythonchallenge.com/pc/def/integrity.html
        # Hay que averiguar nombre de usuario y contraseña, y acceder a http://www.pythonchallenge.com/pc/return/good.html

        # Descarga comentario para decodificar nombre de usuario y contraseña
        r = requests.get("http://www.pythonchallenge.com/pc/def/integrity.html")
        un = re.findall("un: '(.*?)'\n", r.text, re.DOTALL)[0]
        pw = re.findall("pw: '(.*?)'\n", r.text, re.DOTALL)[0]

        # Se convierte el texto para poder pasárselo a BZ2
        un = eval("'%s'" % un)
        pw = eval("'%s'" % pw)

        import bz2
        username = bz2.decompress(un)
        password = bz2.decompress(pw)

        # No se puede automatizar el acceso con
        print "Credenciales: \n\tUsername: " + username + "\n\tPassword: " + password
        webbrowser.open("http://www.pythonchallenge.com/pc/return/good.html?un={}&pw={}".format(username, password))
        print "Solución: http://www.pythonchallenge.com/pcc/return/good.html:huge:file"
    @staticmethod
    def level_9():
        # URL de inicio http://www.pythonchallenge.com/pc/return/good.html:huge:file
        # Hay que averiguar qué significan los números, dibujándolos con alguna herramienta gráfica

        from requests.auth import HTTPBasicAuth
        # Descarga first y second
        r = requests.get("http://www.pythonchallenge.com/pc/return/good.html", auth=HTTPBasicAuth("huge", "file"))
        first = map(int, re.findall("first:\s+(.*)\s+second:", r.text, re.DOTALL)[0].strip().replace('\n', '').split(',')) # Con map, se convierten todos los números de STR a INT
        second = map(int, re.findall("second:\s+(.*)\s+-->", r.text, re.DOTALL)[0].strip().replace('\n', '').split(','))

        from PIL import Image, ImageDraw
        im = Image.new('RGB', (500,500))
        draw = ImageDraw.Draw(im)
        draw.polygon(first, fill='white')
        draw.polygon(second, fill='white')
        im.show()

        print "Se dibuja una vaca. Al entrar en cow.html, indica que es el macho, que es el toro --> bull.html"
        webbrowser.open("http://www.pythonchallenge.com/pc/return/{}.html".format("bull"))

    @staticmethod
    def level_10():
        # URL de inicio http://www.pythonchallenge.com/pc/return/bull.html
        # Hay que averiguar la longitud del 30 elemento de la serie 1, 11, 21, 1211, 111221, etc (look-and-say)

        import itertools
        x = "1"
        for n in range(30):
            x = "".join([str(len(list(j))) + i for i, j in itertools.groupby(x)])
        print x
        print len(x)

        webbrowser.open("http://www.pythonchallenge.com/pc/return/{}.html".format(len(x)))

    @staticmethod
    def level_11():
        # URL de inicio http://www.pythonchallenge.com/pc/return/5808.html
        # Por el título de la página (impar-par), y la foto borrosa, parece que hay que separar la imagen en 2, o
        # descartar algunos de los píxels

        from requests.auth import HTTPBasicAuth
        r = requests.get("http://www.pythonchallenge.com/pc/return/cave.jpg", auth=HTTPBasicAuth("huge","file"))
        # La carga con pillow
        from PIL import Image
        from io import BytesIO
        img = Image.open(BytesIO(r.content))

        ancho, alto = img.size

        img_par = Image.new(img.mode, (ancho // 2, alto // 2))
        img_impar = Image.new(img.mode, (ancho // 2, alto // 2))

        for i in range(ancho):
            for j in range(alto):
                pixel = img.getpixel((i,j))
                if (i + j) % 2 == 1:
                    img_impar.putpixel((i // 2, j // 2), pixel)
                else:
                    img_par.putpixel((i // 2, j // 2), pixel)

        img_impar.show()
        img_par.show()

        # En la imagen par, se puede leer la palabra evil
        webbrowser.open("http://www.pythonchallenge.com/pc/return/{}.html".format("evil"))

    @staticmethod
    def level_12():
        # URL de inicio http://www.pythonchallenge.com/pc/return/evil.html
        # dealing evil. Se descarga la imagen evil1.jpg. Se prueba con evil2.jpg, que indica que no es evil2.jpg, sino evil2.gfx

        from requests.auth import HTTPBasicAuth
        r = requests.get("http://www.pythonchallenge.com/pc/return/evil1.jpg", auth=HTTPBasicAuth("huge","file"))
        r2 = requests.get("http://www.pythonchallenge.com/pc/return/evil2.gfx", auth=HTTPBasicAuth("huge","file"))

        # Analizando la imagen, se observa que en realidad son 5 imágenes en una, por lo que se visualizan las 5
        img = [None] * 5
        # La carga con pillow
        from PIL import Image
        from io import BytesIO
        for imagen in range(5):
            try:
                img[imagen] = Image.open(BytesIO(r2.content[imagen::5]))
                img[imagen].show()
            except:
                open("%d.jpg" % imagen, 'wb').write(r2.content[imagen::5]) # La cuarta imagen está corrupta y da error, se guarda a pelo en el archivo

        # Componiendo las imágenes se deduce el texto dis pro port ional
        webbrowser.open("http://www.pythonchallenge.com/pc/return/{}.html".format("disproportional"))

    @staticmethod
    def level_13():
        """
        Al pulsar el número 5, lleva a un php que devuelve XML en lo que parece un formato de XMLRPC
        Además, dice de llamar al Remote Evil. En el reto anterior, evil4.jpg indicaba algo sobre el malvado Bert...
        :return:
        """
        import xmlrpclib
        conn = xmlrpclib.Server("http://www.pythonchallenge.com/pc/phonebook.php")
        print conn.system.listMethods()
        print conn.system.methodHelp("phone")
        print conn.system.methodSignature("phone")
        print conn.phone("Bert")
        webbrowser.open("http://www.pythonchallenge.com/pc/return/{}.html".format("italy"))

    @staticmethod
    def level_14():
        """
        Se observa la forma de espiral del bollo.
        Se carga con PIL la imagen debajo del bollo.
        :return:
        """
        import requests
        from PIL import Image
        from io import BytesIO
        from requests.auth import HTTPBasicAuth

        r = requests.get("http://www.pythonchallenge.com/pc/return/wire.png", auth=HTTPBasicAuth("huge", "file"))
        img = Image.open(BytesIO(r.content))
        print "Tamaño de la imagen original:", img.size

        # Compone imagen de 100x100:
        img2 = Image.new("RGB", (100, 100))
        for npixel in xrange(10000):
            pixel = img.getpixel((npixel, 0))
            img2.putpixel((npixel % 100, npixel // 100), pixel)

        # Saca un texto BIT. Se entra en bit.html, pero dice que no es correcto.

        # Se prueba a componer los pixels en espiral, de la esquina superior izquierda en el sentido de las agujas del reloj
        delta = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        x, y, p = -1, 0, 0
        d = 200
        while d / 2 > 0:
            for v in delta:
                steps = d // 2
                for s in range(steps):
                    x, y = x + v[0], y + v[1]
                    img2.putpixel((x, y), img.getpixel((p, 0)))
                    p += 1
                d -= 1

        img2.show()
        webbrowser.open("http://www.pythonchallenge.com/pc/return/{}.html".format("cat"))
