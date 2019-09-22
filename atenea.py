# -+- coding: utf8 -*-
import base64
import hashlib


# Utilidades
def flag_md5(password):
    msg = hashlib.md5()
    msg.update(password)
    return "flag{" + msg.digest().encode("hex") + "}"


def sxor(msg, clave):
    # Convierte las cadenas en una lista de tuplas de pares de caracteres
    # Recorre cada tupla, convirtiendo los caracteres a código ASCII
    # Realiza XOR de ambos caracteres
    # Convierte el resultado de nuevo en ASCII
    # Y compone una cadena de caracteres con el resultado

    # Si la clave es más corta, rellena con 0 a la izquierda
    while len(clave) < len(msg):
        clave = '\0' + clave

    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(msg, clave))


def reto_xor():
    msg_in = "UGFzc3dvcmQ6IHhvFzYMACEfBiAgIA=="
    key = "encryptXOR"

    msg = base64.b64decode(msg_in)
    plain = sxor(msg, key)
    print plain

    return flag_md5(plain.partition(" ")[2])

def reto_entropia():
    import os
    import graph_file_entropy

    path = r"C:\Users\Miguel\Downloads\jpg_entropy"
    result = dict()
    for file in os.listdir(path):
        print graph_file_entropy.calcula_entropia(path + "\\" + file)

def reto_metadatos():
    from PyPDF2 import PdfFileReader
    pdf_toread = PdfFileReader(open("Descargas/LoremIpsum-1e40fa12a5e7ce47ebcaaace81f6fd06.pdf", "rb"))
    pdf_info = pdf_toread.getDocumentInfo()
    print(str(pdf_info))

def reto_python():
    import base64
    from Crypto import Random
    from Crypto.Cipher import AES

    AKEY = 'mysixteenbytekey'
    iv = 'what_a_cool_iv!!'

    def decode(cipher):
        obj2 = AES.new(AKEY, AES.MODE_CFB, iv)
        return obj2.decrypt(base64.urlsafe_b64decode(cipher))

    msg = decode("5fMfiISsxcG4gKWAXwkL1Bu6zW26FlhG1613")
    print msg
    print flag_md5(msg.rpartition(" ")[2])


