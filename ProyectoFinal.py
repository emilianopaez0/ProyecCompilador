import math
import os
import sys
import re

# VARIABLES GLOBALES
matriz_fuente = []
matriz_var_etiquetas = []
ruta = ""
nombre_archivo_sinext = ""
n_archivo_errores = ""
matriz_objeto = []
matriz_objeto_color = []
num_bytes_renglon = 16

lista_mnemonicos = ["aba","abx","aby","adca","adcb","adda","addb","addd","anda","andb","asl","asla","aslb","asld","asr","asra","asrb","bcc","bclr","bcs","beq","bge","bgt","bhi","bhs","bita","bitb","ble","blo","bls","blt","bmi","bne","bpl","bra","brclr","brn","brset","bset","bsr","bvc","bvs","cba","clc","cli","clr","clra","clrb","clv","cmpa","cmpb","com","coma","comb","cpd","cpx","cpy","daa","dec","deca","decb","des","dex","dey","eora","eorb","fdiv","idiv","inc","inca","incb","ins","inx","iny","jmp","jsr","ldaa","ldab","ldd","lds","ldx","ldy","lsl","lsla","lslb","lsld","lsr","lsra","lsrb","lsrd","mul","neg","nega","negb","nop","oraa","orab","psha","pshb","pshx","pshy","pula","pulb","pulx","puly","rol","rola","rolb","ror","rora","rorb","rti","rts","sba","sbca","sbcb","sec","sei","sev","staa","stab","std","stop","sts","stx","sty","suba","subb","subd","swi","tab","tap","tba","tpa","tst","tsta","tstb","tsx","tsy","txs","tys","wai","xgdx","xgdy"]

# CORRECCIÓN #7: Opcodes con letra O cambiados a cero (0D, 0F, 0B)
# CORRECCIÓN #9: Eliminado "tets" que era un typo
lista_INH = {
    "aba":"1B","abx":"3A","aby":"18 3A","asla":"48","aslb":"58","asld":"05",
    "asra":"47","asrb":"57","cba":"11","clc":"0C","cli":"0E","clra":"4F",
    "clrb":"5F","clv":"0A","coma":"43","comb":"53","daa":"19","deca":"4A",
    "decb":"5A","des":"34","dex":"09","dey":"18 09","fdiv":"03","idiv":"02",
    "inca":"4C","incb":"5C","ins":"31","inx":"08","iny":"18 08","lsla":"48",
    "lslb":"58","lsld":"05","lsra":"44","lsrb":"54","lsrd":"04","mul":"3D",
    "nega":"40","negb":"50","nop":"01","psha":"36","pshb":"37","pshx":"3C",
    "pshy":"18 3C","pula":"32","pulb":"33","pulx":"38","puly":"18 38",
    "rola":"49","rolb":"59","rora":"46","rorb":"56","rti":"3B","rts":"39",
    "sba":"10","sec":"0D","sei":"0F","sev":"0B","stop":"CF","swi":"3F",  # CORREGIDO #7
    "tab":"16","tap":"06","tba":"17","tpa":"07","tsta":"4D","tstb":"5D",
    "tsx":"30","tsy":"18 30","txs":"35","tys":"18 35","wai":"3E",
    "xgdx":"8F","xgdy":"18 8F"
}

lista_INM = {
    "adca":"89","adcb":"C9","adda":"8B","addb":"CB","addd":"C3","anda":"84",
    "andb":"C4","bita":"85","bitb":"C5","cmpa":"81","cmpb":"C1","cpd":"1A 83",
    "cpx":"8C","cpy":"18 8C","eora":"88","eorb":"C8","ldaa":"86","ldab":"C6",
    "ldd":"CC","lds":"8E","ldx":"CE","ldy":"18 CE","oraa":"8A","orab":"CA",
    "sbca":"82","sbcb":"C2","suba":"80","subb":"C0","subd":"83"
}

lista_DIR = {
    "adca":"99","adcb":"D9","adda":"9B","addb":"DB","addd":"D3","anda":"94",
    "andb":"D4","bclr":"15","bita":"95","bitb":"D5","brclr":"13","brset":"12",
    "bset":"14","cmpa":"91","cmpb":"D1","cpd":"1A 93","cpx":"9C","cpy":"18 9C",
    "eora":"98","eorb":"D8","jsr":"9D","ldaa":"96","ldab":"D6","ldd":"DC",
    "lds":"9E","ldx":"DE","ldy":"18 DE","oraa":"9A","orab":"DA","sbca":"92",
    "sbcb":"D2","staa":"97","stab":"D7","std":"DD","sts":"9F","stx":"DF",
    "sty":"18 DF","suba":"90","subb":"D0","subd":"93"
}

# CORRECCIÓN #8: sty corregido a "18 FF" (era "FF" igual que stx)
lista_EXT = {
    "adca":"B9","adcb":"F9","adda":"BB","addb":"FB","addd":"F3","anda":"B4",
    "andb":"F4","asl":"78","asr":"77","bita":"B5","bitb":"F5","clr":"7F",
    "cmpa":"B1","cmpb":"F1","com":"73","cpd":"1A B3","cpx":"BC","cpy":"18 BC",
    "dec":"7A","eora":"B8","eorb":"F8","inc":"7C","jmp":"7E","jsr":"BD",
    "ldaa":"B6","ldab":"F6","ldd":"FC","lds":"BE","ldx":"FE","ldy":"18 FE",
    "lsl":"78","lsr":"74","neg":"70","oraa":"BA","orab":"FA","rol":"79",
    "ror":"76","sbca":"B2","sbcb":"F2","staa":"B7","stab":"F7","std":"FD",
    "sts":"BF","stx":"FF","sty":"18 FF",   # CORREGIDO #8
    "suba":"B0","subb":"F0","subd":"B3","tst":"7D"
}

lista_INDX = {
    "adca":"A9","adcb":"E9","adda":"AB","addb":"EB","addd":"E3","anda":"B4",
    "andb":"E4","asl":"68","asr":"67","bclr":"1D","bita":"A5","bitb":"E5",
    "brclr":"1F","brset":"1E","bset":"1C","clr":"6F","cmpa":"A1","cmpb":"E1",
    "com":"63","cpd":"1A A3","cpx":"AC","cpy":"1A AC","dec":"6A","eora":"A8",
    "eorb":"E8","inc":"6C","jmp":"6E","jsr":"AD","ldaa":"A6","ldab":"E6",
    "ldd":"EC","lds":"AE","ldx":"EE","ldy":"1A EE","lsl":"68","lsr":"64",
    "neg":"60","oraa":"AA","orab":"EA","rol":"69","ror":"66","sbca":"A2",
    "sbcb":"E2","staa":"A7","stab":"E7","std":"ED","sts":"AF","stx":"EF",
    "sty":"1A EF","suba":"A0","subb":"E0","subd":"A3","tst":"6D"
}

lista_INDY = {
    "adca":"18 A9","adcb":"18 E9","adda":"18 AB","addb":"18 EB","addd":"18 E3",
    "anda":"18 A4","andb":"18 E4","asl":"18 68","asr":"18 67","bclr":"18 1D",
    "bita":"18 A5","bitb":"18 E5","brclr":"18 1F","brset":"18 1E","bset":"18 1C",
    "clr":"18 6F","cmpa":"18 A1","cmpb":"18 E1","com":"18 63","cpd":"CD A3",
    "cpx":"CD AC","cpy":"18 AC","dec":"18 6A","eora":"18 A8","eorb":"18 E8",
    "inc":"18 6C","jmp":"18 6E","jsr":"18 AD","ldaa":"18 A6","ldab":"18 E6",
    "ldd":"18 EC","lds":"18 AE","ldx":"CD EE","ldy":"18 EE","lsl":"18 68",
    "lsr":"18 64","neg":"18 60","oraa":"18 AA","orab":"18 EA","rol":"18 69",
    "ror":"18 66","sbca":"18 A2","sbcb":"18 E2","staa":"18 A7","stab":"18 E7",
    "std":"18 ED","sts":"18 AF","stx":"CD EF","sty":"18 EF","suba":"18 A0",
    "subb":"18 E0","subd":"18 A3","tst":"18 6D"
}

lista_REL = {
    "bcc":"24","bcs":"25","beq":"27","bge":"2C","bgt":"2E","bhi":"22",
    "bhs":"24","ble":"2F","blo":"25","bls":"23","blt":"2D","bmi":"2B",
    "bne":"26","bpl":"2A","bra":"20","brn":"21","bsr":"8D","bvc":"28","bvs":"29"
}

tipo_direccionamiento = ""
compilacion_exitosa = True
es_etiqueta = False
direccion_inicio = "8000"
existe_END = False
etiqueta_duplicada = False


def quitar_comentario(linea_archivo):
    posicion_comentario = linea_archivo.find("*")
    if posicion_comentario == -1:
        return linea_archivo
    else:
        return linea_archivo[:posicion_comentario]


def obtener_elementos(numero_linea, linea_archivo):
    etiqueta = ""
    instruccion = ""
    operando1 = ""
    comentario = ""
    operando2 = ""
    operando3 = ""
    tipo_dir = ""
    valor_instruccion = ""
    valor_operando1 = ""
    valor_operando2 = ""
    valor_operando3 = ""
    errores = ""
    direccion = ""

    lista_elementos = []

    primera_letra = linea_archivo[:1]

    if primera_letra == "*":
        comentario = linea_archivo

    elif primera_letra == " " or primera_letra == "\t":
        posicion_comentario = linea_archivo.find("*")
        if posicion_comentario > -1:
            comentario = linea_archivo[posicion_comentario:]
            linea_archivo_sincom = linea_archivo[:posicion_comentario]
        else:
            linea_archivo_sincom = linea_archivo

        lista_palabras = linea_archivo_sincom.split()
        if len(lista_palabras) == 1:
            instruccion = lista_palabras[0]
        elif len(lista_palabras) == 2:
            instruccion = lista_palabras[0]
            operando1 = lista_palabras[1]
        elif len(lista_palabras) == 3:
            instruccion = lista_palabras[0]
            operando1 = lista_palabras[1]
            operando2 = lista_palabras[2]
        elif len(lista_palabras) >= 4:
            instruccion = lista_palabras[0]
            operando1 = lista_palabras[1]
            operando2 = lista_palabras[2]
            operando3 = lista_palabras[3]

    else:
        posicion_comentario = linea_archivo.find("*")
        if posicion_comentario > -1:
            comentario = linea_archivo[posicion_comentario:]
            linea_archivo_sincom = linea_archivo[:posicion_comentario]
        else:
            linea_archivo_sincom = linea_archivo

        lista_palabras = linea_archivo_sincom.split()
        if len(lista_palabras) == 1:
            etiqueta = lista_palabras[0]
        elif len(lista_palabras) == 2:
            etiqueta = lista_palabras[0]
            instruccion = lista_palabras[1]
        elif len(lista_palabras) == 3:
            etiqueta = lista_palabras[0]
            instruccion = lista_palabras[1]
            operando1 = lista_palabras[2]
        elif len(lista_palabras) >= 4:
            etiqueta = lista_palabras[0]
            instruccion = lista_palabras[1]
            operando1 = lista_palabras[2]
            operando2 = lista_palabras[3]

    lista_elementos.append(numero_linea)
    lista_elementos.append(etiqueta)
    lista_elementos.append(instruccion)
    lista_elementos.append(operando1)
    lista_elementos.append(operando2)
    lista_elementos.append(comentario)
    lista_elementos.append(tipo_dir)
    lista_elementos.append(valor_instruccion)
    lista_elementos.append(valor_operando1)
    lista_elementos.append(valor_operando2)
    lista_elementos.append(errores)
    lista_elementos.append(direccion)

    return lista_elementos


def busca_valor_etiqueta(operando_etiqueta):
    global matriz_var_etiquetas
    global es_etiqueta
    es_etiqueta = False
    valor = ""
    for linea in matriz_var_etiquetas:
        if operando_etiqueta == linea[1]:
            valor = linea[2]
            es_etiqueta = True
    return valor


def obten_valor_operando(operando, linea_fuente):
    global es_etiqueta
    es_etiqueta = False

    valor = ""
    valor_hexa = "00"
    valor_decimal = 0
    valor_final = ""
    valor_bytes = ""
    primer_caracter = ""
    segundo_caracter = ""
    cadena_tipos_valor = "$,%,&"
    es_par = 0

    if operando.find(",") == -1:
        lista_valores = [operando]
    else:
        lista_valores = operando.split(",")

    i = 0
    for elemento in lista_valores:

        valor_hexa = "00"
        valor_decimal = 0
        primer_caracter = lista_valores[i][:1]
        segundo_caracter = lista_valores[i][1:2]

        if primer_caracter == "":
            valor_hexa = "00"
            valor_final = valor_final + valor_hexa

        elif primer_caracter.upper() != "X" and primer_caracter.upper() != "Y":

            if primer_caracter == "#":
                if segundo_caracter in cadena_tipos_valor or segundo_caracter == "\'":
                    valor = lista_valores[i][2:]
                else:
                    valor = lista_valores[i][1:]
            else:
                if primer_caracter in cadena_tipos_valor or primer_caracter == "\'":
                    valor = lista_valores[i][1:]
                else:
                    valor = lista_valores[i]

            valor_etiqueta = busca_valor_etiqueta(valor)
            if valor_etiqueta != "":
                primer_caracter = valor_etiqueta[:1]
                segundo_caracter = valor_etiqueta[1:2]

                if primer_caracter == "#":
                    if segundo_caracter in cadena_tipos_valor or segundo_caracter == "\'":
                        valor = valor_etiqueta[2:]
                    else:
                        valor = valor_etiqueta[1:]
                else:
                    if primer_caracter in cadena_tipos_valor or primer_caracter == "\'":
                        valor = valor_etiqueta[1:]
                    else:
                        valor = valor_etiqueta

                es_etiqueta = False

            if es_etiqueta == False:

                if primer_caracter == "$" or segundo_caracter == "$":
                    valor_decimal = int(valor, 16)
                    valor_hexa = valor.upper()

                elif primer_caracter == "%" or segundo_caracter == "%":
                    valor_decimal = int(valor, 2)
                    valor_hexa = "{:X}".format(valor_decimal)

                elif primer_caracter == "&" or segundo_caracter == "&":
                    valor_decimal = int(valor, 8)
                    valor_hexa = "{:X}".format(valor_decimal)

                elif primer_caracter == "\'" or segundo_caracter == "\'":
                    if len(valor) > 1:
                        valor_hexa = "10000"
                        valor_decimal = "65536"
                    else:
                        valor_decimal = ord(valor)
                        valor_hexa = "{:X}".format(valor_decimal)

                else:
                    if valor.isdigit():
                        valor_decimal = int(valor, 10)
                        valor_hexa = "{:X}".format(valor_decimal)
                    else:
                        if primer_caracter == "#":
                            escribe_muestra_error(linea_fuente, 1)
                            valor_decimal = 0
                            valor_hexa = "00"
                        else:
                            escribe_muestra_error(linea_fuente, 2)
                            valor_decimal = 0
                            valor_hexa = "00"

            es_par = len(valor_hexa) % 2
            while es_par == 1:
                valor_hexa = "0" + valor_hexa
                es_par = len(valor_hexa) % 2

            valor_final = valor_final + valor_hexa
            i = i + 1

    return valor_final


def escribe_muestra_error(linea_fuente, clave_error):
    global compilacion_exitosa
    global matriz_fuente

    texto_error = ""
    lineas = ""
    lista_lineas = []
    num_linea = 0

    if clave_error != 12:
        numero_linea = linea_fuente[0]
        etiqueta = linea_fuente[1]
        instruccion = linea_fuente[2]
        operando1 = linea_fuente[3]
        operando2 = linea_fuente[4]
        comentario = linea_fuente[5]

    compilacion_exitosa = False

    if clave_error == 1:
        texto_error = "ERROR 001: CONSTANTE INEXISTENTE: LINEA "
    elif clave_error == 2:
        texto_error = "ERROR 002: VARIABLE INEXISTENTE: LINEA "
    elif clave_error == 3:
        texto_error = "ERROR 003: ETIQUETA INEXISTENTE: LINEA "
    elif clave_error == 4:
        texto_error = "ERROR 004: MNEMONICO INEXISTENTE: LINEA "
    elif clave_error == 5:
        texto_error = "ERROR 005: INSTRUCCION CARECE DE OPERANDO(S): LINEA "
    elif clave_error == 6:
        texto_error = "ERROR 006: INSTRUCCION NO LLEVA OPERANDO(S): LINEA "
    elif clave_error == 7:
        texto_error = "ERROR 007: MAGNITUD DE OPERANDO ERRONEA: LINEA "
    elif clave_error == 8:
        texto_error = "ERROR 008: SALTO RELATIVO MUY LEJANO: LINEA "
    elif clave_error == 9:
        texto_error = "ERROR 009: INSTRUCCION CARECE DE AL MENOS UN ESPACIO RELATIVO AL MARGEN: LINEA "
    elif clave_error == 10:
        texto_error = "ERROR 010: NO SE ENCUENTRA END: LINEA "
    elif clave_error == 11:
        texto_error = "ERROR 011: COMENTARIO EN LA MISMA LINEA DE UNA ETIQUETA: LINEA "
    elif clave_error == 12:
        texto_error = "ERROR 012: ETIQUETA DUPLICADA: LINEA(S) "

    if clave_error != 12:
        texto_error = texto_error + str(numero_linea) + " " + etiqueta + " " + instruccion + " " + operando1 + " " + operando2 + " " + comentario + " " + "\n"
        matriz_fuente[numero_linea - 1][10] = matriz_fuente[numero_linea - 1][10] + str(clave_error) + ","
    else:
        texto_error = texto_error + linea_fuente
        lineas = linea_fuente.split()[0]
        lista_lineas = lineas.split(",")
        for linea in lista_lineas:
            if linea.isdigit():
                num_linea = int(linea) - 1
                matriz_fuente[num_linea][10] = matriz_fuente[num_linea][10] + str(clave_error) + ","

    print(texto_error)


def obtiene_texto_error(claves_errores):
    texto_error = ""
    texto_error_final = ""
    clave_error = 0
    lista_claves = []

    lista_claves = claves_errores.split(",")

    for clave in lista_claves:
        if clave.isdigit():
            clave_error = int(clave)

            if clave_error == 1:
                texto_error = "ERROR 001: CONSTANTE INEXISTENTE."
            elif clave_error == 2:
                texto_error = "ERROR 002: VARIABLE INEXISTENTE."
            elif clave_error == 3:
                texto_error = "ERROR 003: ETIQUETA INEXISTENTE."
            elif clave_error == 4:
                texto_error = "ERROR 004: MNEMONICO INEXISTENTE."
            elif clave_error == 5:
                texto_error = "ERROR 005: INSTRUCCION CARECE DE OPERANDO(S)."
            elif clave_error == 6:
                texto_error = "ERROR 006: INSTRUCCION NO LLEVA OPERANDO(S)."
            elif clave_error == 7:
                texto_error = "ERROR 007: MAGNITUD DE OPERANDO ERRONEA."
            elif clave_error == 8:
                texto_error = "ERROR 008: SALTO RELATIVO MUY LEJANO."
            elif clave_error == 9:
                texto_error = "ERROR 009: INSTRUCCION CARECE DE AL MENOS UN ESPACIO RELATIVO AL MARGEN."
            elif clave_error == 10:
                texto_error = "ERROR 010: NO SE ENCUENTRA END."
            elif clave_error == 11:
                texto_error = "ERROR 011: COMENTARIO EN LA MISMA LINEA DE UNA ETIQUETA."
            elif clave_error == 12:
                texto_error = "ERROR 012: ETIQUETA DUPLICADA."

            texto_error_final = texto_error_final + texto_error + " "
            clave_error = 0

    return texto_error_final


def define_direccionamiento(instruccion, operando, linea_fuente):
    global tipo_direccionamiento

    instruccion_estandar = instruccion.lower()
    valor_instruccion = ""
    tipo_direccionamiento = ""
    valor_operando = ""
    valor_operando_decimal = 0

    if operando == "":  # DIRECCIONAMIENTO INHERENTE
        if lista_INH.get(instruccion_estandar, "") != "":
            tipo_direccionamiento = "INH"
            valor_instruccion = lista_INH.get(instruccion_estandar)
        else:
            if instruccion_estandar in lista_mnemonicos:
                escribe_muestra_error(linea_fuente, 5)
            else:
                escribe_muestra_error(linea_fuente, 4)
    else:
        if lista_INH.get(instruccion_estandar, "") != "":
            tipo_direccionamiento = "INH"
            valor_instruccion = lista_INH.get(instruccion_estandar)
            escribe_muestra_error(linea_fuente, 6)

        elif ",X" in operando or ",x" in operando:  # INDEXADO EN X
            if lista_INDX.get(instruccion_estandar, "") != "":
                tipo_direccionamiento = "INDX"
                valor_instruccion = lista_INDX.get(instruccion_estandar)
                lista_operando = operando.split(",")
                if lista_operando[0] == "":
                    lista_operando[0] = "0"
                valor_operando = obten_valor_operando(lista_operando[0], linea_fuente)
                valor_operando_decimal = int(valor_operando, 16)
                if valor_operando_decimal > 255:
                    escribe_muestra_error(linea_fuente, 7)
            else:
                escribe_muestra_error(linea_fuente, 4)

        elif ",Y" in operando or ",y" in operando:  # INDEXADO EN Y
            if lista_INDY.get(instruccion_estandar, "") != "":
                tipo_direccionamiento = "INDY"
                valor_instruccion = lista_INDY.get(instruccion_estandar)
                lista_operando = operando.split(",")
                if lista_operando[0] == "":
                    lista_operando[0] = "0"
                valor_operando = obten_valor_operando(lista_operando[0], linea_fuente)
                valor_operando_decimal = int(valor_operando, 16)
                if valor_operando_decimal > 255:
                    escribe_muestra_error(linea_fuente, 7)
            else:
                escribe_muestra_error(linea_fuente, 4)

        elif operando[0] == "#":  # INMEDIATO
            if lista_INM.get(instruccion_estandar, "") != "":
                tipo_direccionamiento = "INM"
                valor_instruccion = lista_INM.get(instruccion_estandar)
                valor_operando = obten_valor_operando(operando, linea_fuente)
                valor_operando_decimal = int(valor_operando, 16)
                if valor_operando_decimal > 65535:
                    escribe_muestra_error(linea_fuente, 7)
            else:
                escribe_muestra_error(linea_fuente, 4)

        elif lista_REL.get(instruccion_estandar, "") != "":  # RELATIVO
            tipo_direccionamiento = "REL"
            valor_instruccion = lista_REL.get(instruccion_estandar)
            # CORRECCIÓN #5: condición invertida (!= en lugar de ==)
            if busca_valor_etiqueta(operando) != "" and es_etiqueta == True:
                valor_operando = "00"
            else:
                escribe_muestra_error(linea_fuente, 3)

        else:
            valor_operando = obten_valor_operando(operando, linea_fuente)
            valor_operando_decimal = int(valor_operando, 16)
            tipo_direccionamiento = "DIR"

            if 0 <= valor_operando_decimal <= 255:
                if lista_DIR.get(instruccion_estandar, "") != "":
                    tipo_direccionamiento = "DIR"
                    valor_instruccion = lista_DIR.get(instruccion_estandar)
                else:
                    if lista_EXT.get(instruccion_estandar, "") != "":
                        tipo_direccionamiento = "EXT"
                        valor_instruccion = lista_EXT.get(instruccion_estandar)
                    else:
                        escribe_muestra_error(linea_fuente, 4)

            elif 255 < valor_operando_decimal <= 65535:
                if lista_EXT.get(instruccion_estandar, "") != "":
                    tipo_direccionamiento = "EXT"
                    valor_instruccion = lista_EXT.get(instruccion_estandar)
                else:
                    escribe_muestra_error(linea_fuente, 4)

            elif valor_operando_decimal > 65535:
                escribe_muestra_error(linea_fuente, 7)

            if tipo_direccionamiento == "":
                escribe_muestra_error(linea_fuente, 4)

    return valor_instruccion + "," + valor_operando


def procesa_linea_fuente(linea_fuente):
    global matriz_fuente
    global matriz_var_etiquetas
    global direccion_inicio
    global existe_END
    global tipo_direccionamiento

    tipo_direccionamiento = ""
    numero_linea = linea_fuente[0]
    etiqueta = linea_fuente[1]
    instruccion = linea_fuente[2]
    operando1 = linea_fuente[3]
    operando2 = linea_fuente[4]
    comentario = linea_fuente[5]
    tipo_direccion = linea_fuente[6]
    valor_instruccion = linea_fuente[7]
    valor_operando1 = linea_fuente[8]
    valor_operando2 = linea_fuente[9]
    instruccion_estandar = instruccion.lower()
    valor_operando = 0
    lista_resultados = []
    lista_matriz_etiquetas = []

    if etiqueta.lower() in lista_mnemonicos:
        escribe_muestra_error(linea_fuente, 9)

    else:
        if instruccion != "EQU" and instruccion != "" and etiqueta != "":
            lista_matriz_etiquetas = []
            lista_matriz_etiquetas.append(numero_linea)
            lista_matriz_etiquetas.append(etiqueta)
            lista_matriz_etiquetas.append("")
            lista_matriz_etiquetas.append("")
            matriz_var_etiquetas.append(lista_matriz_etiquetas)

        elif instruccion == "" and etiqueta != "":
            lista_matriz_etiquetas = []
            lista_matriz_etiquetas.append(numero_linea)
            lista_matriz_etiquetas.append(etiqueta)
            lista_matriz_etiquetas.append("")
            lista_matriz_etiquetas.append("")
            matriz_var_etiquetas.append(lista_matriz_etiquetas)
            if comentario != "":
                escribe_muestra_error(linea_fuente, 11)

        if instruccion.upper() == "EQU":
            if etiqueta != "" and operando1 != "":
                lista_matriz_etiquetas = []
                lista_matriz_etiquetas.append(numero_linea)
                lista_matriz_etiquetas.append(etiqueta)
                lista_matriz_etiquetas.append(operando1)
                lista_matriz_etiquetas.append("")
                matriz_var_etiquetas.append(lista_matriz_etiquetas)
            else:
                escribe_muestra_error(linea_fuente, 5)

        elif instruccion.upper() == "ORG":
            if operando1 != "":
                direccion_ini = obten_valor_operando(operando1, linea_fuente)
                while len(direccion_ini) < 4:
                    direccion_ini = "0" + direccion_ini
                if int(direccion_ini.replace(" ", ""), 16) > 65535:
                    escribe_muestra_error(linea_fuente, 7)
                else:
                    direccion_inicio = direccion_ini.replace(" ", "")
            else:
                escribe_muestra_error(linea_fuente, 5)

        elif instruccion.upper() == "FCB":
            if operando1 != "":
                valor_operando1 = obten_valor_operando(operando1, linea_fuente)
            else:
                escribe_muestra_error(linea_fuente, 5)

        elif instruccion.upper() == "END":
            existe_END = True

        elif instruccion.upper() == "BCLR" or instruccion.upper() == "BSET":
            if operando1 != "":
                lista_operandos = operando1.split(",")
                if ",X" in operando1 or ",x" in operando1:
                    tipo_direccionamiento = "INDX"
                    valor_instruccion = lista_INDX.get(instruccion_estandar)
                elif ",Y" in operando1 or ",y" in operando1:
                    tipo_direccionamiento = "INDY"
                    valor_instruccion = lista_INDY.get(instruccion_estandar)
                else:
                    tipo_direccionamiento = "DIR"
                    valor_instruccion = lista_DIR.get(instruccion_estandar)

                for i in range(len(lista_operandos)):
                    valor_operando = obten_valor_operando(lista_operandos[i], linea_fuente)
                    if valor_operando.isdigit():
                        valor_decimal = int(valor_operando, 16)
                    else:
                        valor_decimal = 0
                    if valor_decimal > 65535:
                        escribe_muestra_error(linea_fuente, 7)
                    if i == len(lista_operandos) - 1:
                        if valor_decimal > 255:
                            escribe_muestra_error(linea_fuente, 7)
                    valor_operando1 = valor_operando1 + valor_operando + " "
            else:
                escribe_muestra_error(linea_fuente, 5)

        elif instruccion.upper() == "BRCLR" or instruccion.upper() == "BRSET":
            if operando1 != "":
                lista_operandos = operando1.split(",")
                if ",X" in operando1 or ",x" in operando1:
                    tipo_direccionamiento = "INDX"
                    valor_instruccion = lista_INDX.get(instruccion_estandar)
                elif ",Y" in operando1 or ",y" in operando1:
                    tipo_direccionamiento = "INDY"
                    valor_instruccion = lista_INDY.get(instruccion_estandar)
                else:
                    tipo_direccionamiento = "DIR"
                    valor_instruccion = lista_DIR.get(instruccion_estandar)

                for i in range(len(lista_operandos)):
                    valor_operando = obten_valor_operando(lista_operandos[i], linea_fuente)
                    if valor_operando.isdigit():
                        valor_decimal = int(valor_operando, 16)
                    else:
                        valor_decimal = 0
                    if valor_decimal > 65535:
                        escribe_muestra_error(linea_fuente, 7)
                    if i == len(lista_operandos) - 1:
                        if valor_decimal > 255:
                            escribe_muestra_error(linea_fuente, 7)
                    valor_operando1 = valor_operando1 + valor_operando + " "
            else:
                escribe_muestra_error(linea_fuente, 5)

            if operando2 != "":
                # CORRECCIÓN #6: condición invertida (!=  en lugar de ==)
                if busca_valor_etiqueta(operando2) != "" and es_etiqueta == True:
                    valor_operando2 = "00"
                else:
                    escribe_muestra_error(linea_fuente, 3)
            else:
                escribe_muestra_error(linea_fuente, 5)

        else:  # UN SOLO OPERANDO
            if instruccion.upper() == "JMP" or instruccion.upper() == "JSR":
                if busca_valor_etiqueta(operando1) == "" and es_etiqueta == True:
                    operando1 = "$" + direccion_inicio

            if instruccion != "":
                lista_resultados = define_direccionamiento(instruccion, operando1, linea_fuente).split(",")
                valor_instruccion = lista_resultados[0]
                valor_operando1 = lista_resultados[1]

    # ACTUALIZAR LA MATRIZ FUENTE
    for linea in matriz_fuente:
        if linea[0] == numero_linea:
            linea[6] = tipo_direccionamiento
            linea[7] = valor_instruccion
            linea[8] = valor_operando1
            linea[9] = valor_operando2


def busca_etiquetas_duplicadas():
    global matriz_var_etiquetas
    global etiqueta_duplicada

    lista_etiquetas = []
    cadena_lineas = ""
    cadena_etiquetas = ""
    cadena_etiquetas_duplicadas = ""
    etiqueta_duplicada = False

    for etiqueta in matriz_var_etiquetas:
        if etiqueta[2] == "":
            lista_etiquetas.append(etiqueta[1])
            cadena_etiquetas = cadena_etiquetas + etiqueta[1] + ","

    for elemento in lista_etiquetas:
        if cadena_etiquetas.count(elemento) > 1:
            etiqueta_duplicada = True
            cadena_etiquetas_duplicadas = cadena_etiquetas_duplicadas + elemento + ","

    for etiqueta in matriz_var_etiquetas:
        if etiqueta[1] in cadena_etiquetas_duplicadas:
            cadena_lineas = cadena_lineas + str(etiqueta[0]) + ","

    if cadena_lineas != "":
        cadena_lineas = cadena_lineas + " ETIQUETAS: " + cadena_etiquetas_duplicadas

    return cadena_lineas


def separa_bytes(cadena_hexa):
    cadena_bytes = ""
    cadena_h = cadena_hexa.replace(" ", "")
    for j in range(0, len(cadena_h), 2):
        cadena_bytes = cadena_bytes + cadena_h[j:j+2] + " "
    return cadena_bytes


def calcula_complemento_a2(numero_base10):
    numero_binario = ""
    numero_binario_negado = ""
    numero_decimal = 0
    numero_hexadecimal = ""
    es_par = 0

    numero_binario = bin(abs(numero_base10))
    numero_binario = numero_binario[2:]

    while len(numero_binario) < 8:
        numero_binario = "0" + numero_binario

    for i in range(0, len(numero_binario), 1):
        if numero_binario[i:i+1] == "1":
            numero_binario_negado = numero_binario_negado + "0"
        elif numero_binario[i:i+1] == "0":
            numero_binario_negado = numero_binario_negado + "1"

    numero_decimal = int(numero_binario_negado, 2) + 1
    numero_hexadecimal = "{:X}".format(numero_decimal)

    es_par = len(numero_hexadecimal) % 2
    while es_par == 1:
        numero_hexadecimal = "0" + numero_hexadecimal
        es_par = len(numero_hexadecimal) % 2

    return numero_hexadecimal


def busca_direccion_etiqueta(operando_etiqueta):
    global matriz_var_etiquetas
    global es_etiqueta
    es_etiqueta = False
    valor = ""
    for linea in matriz_var_etiquetas:
        if operando_etiqueta == linea[1]:
            valor = linea[3]
            es_etiqueta = True
    return valor


def genera_codigo_objeto():
    global matriz_objeto
    global matriz_fuente
    global direccion_inicio
    global es_etiqueta
    linea_etiqueta_anterior = 0
    etiqueta_anterior = ""
    cadena_hexa = ""
    cadena_bytes = ""
    lista_bytes = []
    lista_matriz_objeto = []
    contador_direccion = direccion_inicio
    contador_direccion_decimal = 0

    es_etiqueta = False
    direccion_etiqueta = ""
    direccion_inicial_modificar = ""

    # PRIMER CICLO: ARMAR TABLA DE CODIGO OBJETO SIN SALTOS
    for linea_fuente in matriz_fuente:
        numero_linea = linea_fuente[0]
        etiqueta = linea_fuente[1]
        instruccion = linea_fuente[2]
        operando1 = linea_fuente[3]
        operando2 = linea_fuente[4]
        comentario = linea_fuente[5]
        tipo_direccion = linea_fuente[6]
        valor_instruccion = linea_fuente[7]
        valor_operando1 = linea_fuente[8]
        valor_operando2 = linea_fuente[9]

        instruccion_estandar = instruccion.upper()
        cadena_hexa = ""
        cadena_bytes = ""
        lista_bytes = []
        lista_matriz_objeto = []

        if etiqueta != "" or instruccion != "":
            if etiqueta != "" and instruccion != "EQU":
                linea_etiqueta_anterior = numero_linea
                etiqueta_anterior = etiqueta

            if instruccion_estandar != "ORG" and instruccion_estandar != "EQU" and instruccion_estandar != "END" and instruccion != "":
                cadena_hexa = valor_instruccion + valor_operando1 + valor_operando2
                cadena_bytes = separa_bytes(cadena_hexa)
                lista_bytes = cadena_bytes.split()
                i = 1
                for byte in lista_bytes:
                    lista_matriz_objeto = []
                    if linea_etiqueta_anterior > 0 and i == 1:
                        for linea_etiqueta in matriz_var_etiquetas:
                            if linea_etiqueta[0] == linea_etiqueta_anterior and linea_etiqueta[1] == etiqueta_anterior:
                                linea_etiqueta[3] = contador_direccion
                                linea_etiqueta_anterior = 0
                                etiqueta_anterior = ""
                    lista_matriz_objeto.append(numero_linea)
                    lista_matriz_objeto.append(contador_direccion)
                    lista_matriz_objeto.append(byte)
                    matriz_objeto.append(lista_matriz_objeto)

                    if i == 1:
                        linea_fuente[11] = contador_direccion

                    i = i + 1
                    contador_direccion_decimal = int(contador_direccion, 16) + 1
                    contador_direccion = "{:X}".format(contador_direccion_decimal)
                    while len(contador_direccion) < 4:
                        contador_direccion = "0" + contador_direccion

    # SEGUNDO CICLO: CALCULAR SALTOS Y ACTUALIZAR TABLA DE CODIGO OBJETO
    for linea_fuente in matriz_fuente:
        numero_linea = linea_fuente[0]
        etiqueta = linea_fuente[1]
        instruccion = linea_fuente[2]
        operando1 = linea_fuente[3]
        operando2 = linea_fuente[4]
        comentario = linea_fuente[5]
        tipo_direccion = linea_fuente[6]
        valor_instruccion = linea_fuente[7]
        valor_operando1 = linea_fuente[8]
        valor_operando2 = linea_fuente[9]
        instruccion_estandar = instruccion.upper()
        cadena_hexa = ""
        cadena_bytes = ""
        lista_bytes = []

        es_etiqueta = False
        direccion_etiqueta = ""
        direccion_inicial_modificar = ""
        contador_direccion_decimal = 0
        i = 1
        salto = 0
        salto_hexa = ""

        if instruccion.upper() == "JMP" or instruccion.upper() == "JSR":
            if tipo_direccion == "EXT":
                direccion_etiqueta = busca_direccion_etiqueta(operando1)
                if direccion_etiqueta != "" and es_etiqueta == True:
                    linea_fuente[8] = direccion_etiqueta
                    cadena_bytes = separa_bytes(direccion_etiqueta)
                    lista_bytes = cadena_bytes.split()

                    for linea_objeto in matriz_objeto:
                        if linea_objeto[0] == numero_linea:
                            if i == 2:
                                linea_objeto[2] = lista_bytes[0]
                            elif i == 3:
                                linea_objeto[2] = lista_bytes[1]
                            i = i + 1

        # CORRECCIÓN #4: .upper() con paréntesis
        elif instruccion.upper() == "BRCLR" or instruccion.upper() == "BRSET" or tipo_direccion == "REL":
            for linea_objeto in matriz_objeto:
                if linea_objeto[0] == numero_linea:
                    direccion_inicial_modificar = linea_objeto[1]

            if instruccion.upper() == "BRCLR" or instruccion.upper() == "BRSET":
                direccion_etiqueta = busca_direccion_etiqueta(operando2)
            else:
                direccion_etiqueta = busca_direccion_etiqueta(operando1)

            if direccion_etiqueta == "":
                direccion_etiqueta = "0000"
            if direccion_inicial_modificar == "":
                direccion_inicial_modificar = "0000"

            salto = int(direccion_etiqueta, 16) - (int(direccion_inicial_modificar, 16) + 1)

            if salto < 0:
                salto_hexa = calcula_complemento_a2(salto)
            elif salto >= 0:
                salto_hexa = "{:X}".format(salto)

            cadena_bytes = separa_bytes(salto_hexa)
            lista_bytes = cadena_bytes.split()

            for linea_objeto in matriz_objeto:
                if linea_objeto[1] == direccion_inicial_modificar:
                    linea_objeto[2] = lista_bytes[len(lista_bytes) - 1]

            if instruccion.upper() == "BRCLR" or instruccion.upper() == "BRSET":
                linea_fuente[9] = lista_bytes[len(lista_bytes) - 1]
            else:
                linea_fuente[8] = lista_bytes[len(lista_bytes) - 1]

            if salto < -127 or salto > 128:
                escribe_muestra_error(linea_fuente, 8)


def genera_archivo_LST():
    global nombre_archivo_sinext
    global ruta
    global matriz_fuente

    n_archivo_LST = ruta + nombre_archivo_sinext + ".LST"
    f_archivo_LST = open(n_archivo_LST, 'w', encoding="utf-8")
    f_archivo_LST.close()

    f_archivo_LST = open(n_archivo_LST, 'a', encoding="utf-8")

    for linea_fuente in matriz_fuente:
        numero_linea = linea_fuente[0]
        etiqueta = linea_fuente[1]
        instruccion = linea_fuente[2]
        operando1 = linea_fuente[3]
        operando2 = linea_fuente[4]
        comentario = linea_fuente[5]
        tipo_direccion = linea_fuente[6]
        valor_instruccion = linea_fuente[7]
        valor_operando1 = linea_fuente[8]
        valor_operando2 = linea_fuente[9]
        errores = linea_fuente[10]
        direccion = linea_fuente[11]

        linea_archivo1 = ""
        linea_archivo2 = ""
        cadena_bytes = ""

        cadena_bytes = separa_bytes(valor_instruccion + valor_operando1 + valor_operando2)
        cadena_bytes = cadena_bytes.replace(" ", "")

        cadena_num_linea = str(numero_linea)
        while len(cadena_num_linea) < 3:
            cadena_num_linea = cadena_num_linea + " "

        if direccion != "" and cadena_bytes != "":
            linea_archivo1 = cadena_num_linea + ": " + direccion + "(" + cadena_bytes + ")"
        else:
            linea_archivo1 = cadena_num_linea + ": Vacio"

        while len(linea_archivo1) < 30:
            linea_archivo1 = linea_archivo1 + " "

        linea_archivo2 = linea_archivo1 + " :  " + etiqueta + " " + instruccion + " " + operando1 + " " + operando2 + " " + comentario.replace("\n", "") + "  " + obtiene_texto_error(errores) + "\n"

        f_archivo_LST.write(linea_archivo2)

    f_archivo_LST.close()
    print("ARCHIVO " + n_archivo_LST + " GENERADO.")


def genera_archivo_S19():
    global nombre_archivo_sinext
    global ruta
    global matriz_objeto
    global num_bytes_renglon

    n_archivo_S19 = ruta + nombre_archivo_sinext + ".S19"
    f_archivo_S19 = open(n_archivo_S19, 'w', encoding="utf-8")
    f_archivo_S19.close()

    f_archivo_S19 = open(n_archivo_S19, 'a', encoding="utf-8")

    i = 1
    cadena_bytes = ""
    direccion = ""

    for linea_objeto in matriz_objeto:
        if i == 1:
            direccion = "<" + linea_objeto[1] + ">"
        if i <= num_bytes_renglon:
            cadena_bytes = cadena_bytes + linea_objeto[2] + " "
            i = i + 1

        if i > num_bytes_renglon:
            i = 1
            linea_archivo = direccion + " " + cadena_bytes + "\n"
            f_archivo_S19.write(linea_archivo)
            cadena_bytes = ""
            direccion = ""

    if cadena_bytes != "":
        linea_archivo = direccion + " " + cadena_bytes + "\n"
        f_archivo_S19.write(linea_archivo)

    f_archivo_S19.close()
    print("ARCHIVO " + n_archivo_S19 + " GENERADO.")


def genera_archivo_LST_COLOR():
    global nombre_archivo_sinext
    global ruta
    global matriz_fuente

    rojo = "\033[31m"
    azul = "\033[34m"
    magenta = "\033[35m"
    reset = "\033[0m"

    n_archivo_LST = ruta + nombre_archivo_sinext + "_COLOR.LST"
    f_archivo_LST = open(n_archivo_LST, 'w', encoding="utf-8")
    f_archivo_LST.close()

    f_archivo_LST = open(n_archivo_LST, 'a', encoding="utf-8")

    for linea_fuente in matriz_fuente:
        numero_linea = linea_fuente[0]
        etiqueta = linea_fuente[1]
        instruccion = linea_fuente[2]
        operando1 = linea_fuente[3]
        operando2 = linea_fuente[4]
        comentario = linea_fuente[5]
        tipo_direccion = linea_fuente[6]
        valor_instruccion = linea_fuente[7]
        valor_operando1 = linea_fuente[8]
        valor_operando2 = linea_fuente[9]
        errores = linea_fuente[10]
        direccion = linea_fuente[11]

        linea_archivo1 = ""
        linea_archivo2 = ""
        cadena_bytes = ""
        cadena_bytes1 = ""
        cadena_bytes2 = ""

        cadena_bytes1 = separa_bytes(valor_instruccion)
        cadena_bytes1 = cadena_bytes1.replace(" ", "")
        cadena_bytes1 = rojo + cadena_bytes1 + reset

        cadena_bytes2 = separa_bytes(valor_operando1 + valor_operando2)
        cadena_bytes2 = cadena_bytes2.replace(" ", "")
        cadena_bytes2 = azul + cadena_bytes2 + reset

        cadena_num_linea = str(numero_linea)
        while len(cadena_num_linea) < 3:
            cadena_num_linea = cadena_num_linea + " "

        cadena_bytes = cadena_bytes1 + cadena_bytes2

        if direccion != "" and cadena_bytes != "":
            linea_archivo1 = cadena_num_linea + ": " + direccion + "(" + cadena_bytes + ")"
        else:
            linea_archivo1 = cadena_num_linea + ": Vacio"

        while len(linea_archivo1) < 30:
            linea_archivo1 = linea_archivo1 + " "

        linea_archivo2 = linea_archivo1 + " :  " + etiqueta + " " + instruccion + " " + operando1 + " " + operando2 + " " + comentario.replace("\n", "") + "  " + magenta + obtiene_texto_error(errores) + reset + "\n"

        f_archivo_LST.write(linea_archivo2)

    f_archivo_LST.close()
    print("ARCHIVO " + n_archivo_LST + " GENERADO.")
    muestra_archivo(n_archivo_LST)


def muestra_archivo(nombre_archivo):
    f_archivo = open(nombre_archivo, 'r', encoding="utf-8")
    linea_archivo = f_archivo.readline()
    while linea_archivo != "":
        print(linea_archivo)
        linea_archivo = f_archivo.readline()
    f_archivo.close()


def genera_codigo_objeto_COLOR():
    global matriz_objeto_color
    global matriz_fuente
    global direccion_inicio
    global es_etiqueta

    contador_direccion = direccion_inicio
    contador_direccion_decimal = 0
    es_etiqueta = False

    for linea_fuente in matriz_fuente:
        numero_linea = linea_fuente[0]
        etiqueta = linea_fuente[1]
        instruccion = linea_fuente[2]
        operando1 = linea_fuente[3]
        operando2 = linea_fuente[4]
        tipo_direccion = linea_fuente[6]
        valor_instruccion = linea_fuente[7]
        valor_operando1 = linea_fuente[8]
        valor_operando2 = linea_fuente[9]
        instruccion_estandar = instruccion.upper()

        if etiqueta != "" or instruccion != "":
            if instruccion_estandar != "ORG" and instruccion_estandar != "EQU" and instruccion_estandar != "END" and instruccion != "":
                # Bytes de instruccion (I)
                cadena_hexa = valor_instruccion
                cadena_bytes = separa_bytes(cadena_hexa)
                lista_bytes = cadena_bytes.split()

                for byte in lista_bytes:
                    lista_matriz_objeto = []
                    lista_matriz_objeto.append(numero_linea)
                    lista_matriz_objeto.append(contador_direccion)
                    lista_matriz_objeto.append(byte)
                    lista_matriz_objeto.append("I")
                    matriz_objeto_color.append(lista_matriz_objeto)

                    contador_direccion_decimal = int(contador_direccion, 16) + 1
                    contador_direccion = "{:X}".format(contador_direccion_decimal)
                    while len(contador_direccion) < 4:
                        contador_direccion = "0" + contador_direccion

                # Bytes de operandos (O)
                cadena_hexa = valor_operando1 + valor_operando2
                cadena_bytes = separa_bytes(cadena_hexa)
                lista_bytes = cadena_bytes.split()

                for byte in lista_bytes:
                    lista_matriz_objeto = []
                    lista_matriz_objeto.append(numero_linea)
                    lista_matriz_objeto.append(contador_direccion)
                    lista_matriz_objeto.append(byte)
                    lista_matriz_objeto.append("O")
                    matriz_objeto_color.append(lista_matriz_objeto)

                    contador_direccion_decimal = int(contador_direccion, 16) + 1
                    contador_direccion = "{:X}".format(contador_direccion_decimal)
                    while len(contador_direccion) < 4:
                        contador_direccion = "0" + contador_direccion


def genera_archivo_S19_MOTOROLA():
    global nombre_archivo_sinext
    global ruta
    global matriz_objeto
    global num_bytes_renglon

    n_archivo_S19 = ruta + nombre_archivo_sinext + "_MOTOROLA.S19"
    f_archivo_S19 = open(n_archivo_S19, 'w', encoding="utf-8")
    f_archivo_S19.close()
    f_archivo_S19 = open(n_archivo_S19, 'a', encoding="utf-8")

    i = 1
    cadena_bytes = ""
    direccion = ""
    contador_bytes = 0
    contador_bytes_hexa = ""
    direccion_bytes = ""
    byte_decimal = 0
    suma_decimal = 0
    suma_hexa = ""
    suma_binaria = ""
    suma_binaria_invertida = ""
    check_sum = ""

    for linea_objeto in matriz_objeto:
        if i == 1:
            direccion = linea_objeto[1]
            direccion_bytes = separa_bytes(direccion).split()
            for j in range(len(direccion_bytes)):
                suma_decimal = suma_decimal + int(direccion_bytes[j], 16)
                contador_bytes = contador_bytes + 1

        if i <= num_bytes_renglon:
            cadena_bytes = cadena_bytes + linea_objeto[2]
            i = i + 1
            byte_decimal = int(linea_objeto[2], 16)
            suma_decimal = suma_decimal + byte_decimal
            contador_bytes = contador_bytes + 1

        if i > num_bytes_renglon:
            i = 1
            contador_bytes = contador_bytes + 1
            suma_decimal = suma_decimal + contador_bytes
            contador_bytes_hexa = "{:X}".format(contador_bytes)
            while len(contador_bytes_hexa) % 2 == 1:
                contador_bytes_hexa = "0" + contador_bytes_hexa

            suma_binaria = bin(suma_decimal)
            suma_binaria_invertida = ""
            for b in range(len(suma_binaria)):
                if suma_binaria[b:b+1] == "1":
                    suma_binaria_invertida = suma_binaria_invertida + "0"
                elif suma_binaria[b:b+1] == "0":
                    suma_binaria_invertida = suma_binaria_invertida + "1"
            suma_hexa = "{:X}".format(int(suma_binaria_invertida, 2))
            check_sum = suma_hexa[len(suma_hexa)-2:]

            linea_archivo = "S1" + contador_bytes_hexa + direccion + cadena_bytes + check_sum + "\n"
            f_archivo_S19.write(linea_archivo)

            contador_bytes = 0
            contador_bytes_hexa = ""
            direccion_bytes = ""
            byte_decimal = 0
            suma_decimal = 0
            suma_hexa = ""
            suma_binaria = ""
            suma_binaria_invertida = ""
            check_sum = ""
            cadena_bytes = ""
            direccion = ""

    if cadena_bytes != "":
        contador_bytes = contador_bytes + 1
        suma_decimal = suma_decimal + contador_bytes
        contador_bytes_hexa = "{:X}".format(contador_bytes)
        while len(contador_bytes_hexa) % 2 == 1:
            contador_bytes_hexa = "0" + contador_bytes_hexa

        suma_binaria = bin(suma_decimal)
        suma_binaria_invertida = ""
        for b in range(len(suma_binaria)):
            if suma_binaria[b:b+1] == "1":
                suma_binaria_invertida = suma_binaria_invertida + "0"
            elif suma_binaria[b:b+1] == "0":
                suma_binaria_invertida = suma_binaria_invertida + "1"
        suma_hexa = "{:X}".format(int(suma_binaria_invertida, 2))
        check_sum = suma_hexa[len(suma_hexa)-2:]

        linea_archivo = "S1" + contador_bytes_hexa + direccion + cadena_bytes + check_sum + "\n"
        f_archivo_S19.write(linea_archivo)

    f_archivo_S19.write("S9030000FC")
    f_archivo_S19.close()
    print("ARCHIVO " + n_archivo_S19 + " GENERADO.")


def genera_archivo_S19_MOTOROLA_COLOR():
    global nombre_archivo_sinext
    global ruta
    global matriz_objeto_color
    global num_bytes_renglon

    rojo = "\033[31m"
    azul = "\033[34m"
    reset = "\033[0m"

    n_archivo_S19 = ruta + nombre_archivo_sinext + "_MOTOROLA_COLOR.S19"
    f_archivo_S19 = open(n_archivo_S19, 'w', encoding="utf-8")
    f_archivo_S19.close()
    f_archivo_S19 = open(n_archivo_S19, 'a', encoding="utf-8")
    genera_codigo_objeto_COLOR()

    i = 1
    cadena_bytes = ""
    direccion = ""
    contador_bytes = 0
    contador_bytes_hexa = ""
    direccion_bytes = ""
    byte_decimal = 0
    suma_decimal = 0
    suma_hexa = ""
    suma_binaria = ""
    suma_binaria_invertida = ""
    check_sum = ""

    for linea_objeto in matriz_objeto_color:
        if i == 1:
            direccion = linea_objeto[1]
            direccion_bytes = separa_bytes(direccion).split()
            for j in range(len(direccion_bytes)):
                suma_decimal = suma_decimal + int(direccion_bytes[j], 16)
                contador_bytes = contador_bytes + 1

        if i <= num_bytes_renglon:
            if linea_objeto[3] == "I":
                cadena_bytes = cadena_bytes + rojo + linea_objeto[2] + reset
            if linea_objeto[3] == "O":
                cadena_bytes = cadena_bytes + azul + linea_objeto[2] + reset
            i = i + 1
            byte_decimal = int(linea_objeto[2], 16)
            suma_decimal = suma_decimal + byte_decimal
            contador_bytes = contador_bytes + 1

        if i > num_bytes_renglon:
            i = 1
            contador_bytes = contador_bytes + 1
            suma_decimal = suma_decimal + contador_bytes
            contador_bytes_hexa = "{:X}".format(contador_bytes)
            while len(contador_bytes_hexa) % 2 == 1:
                contador_bytes_hexa = "0" + contador_bytes_hexa

            suma_binaria = bin(suma_decimal)
            suma_binaria_invertida = ""
            for b in range(len(suma_binaria)):
                if suma_binaria[b:b+1] == "1":
                    suma_binaria_invertida = suma_binaria_invertida + "0"
                elif suma_binaria[b:b+1] == "0":
                    suma_binaria_invertida = suma_binaria_invertida + "1"
            suma_hexa = "{:X}".format(int(suma_binaria_invertida, 2))
            check_sum = suma_hexa[len(suma_hexa)-2:]

            linea_archivo = "S1" + contador_bytes_hexa + direccion + cadena_bytes + check_sum + "\n"
            f_archivo_S19.write(linea_archivo)

            contador_bytes = 0
            contador_bytes_hexa = ""
            direccion_bytes = ""
            byte_decimal = 0
            suma_decimal = 0
            suma_hexa = ""
            suma_binaria = ""
            suma_binaria_invertida = ""
            check_sum = ""
            cadena_bytes = ""
            direccion = ""

    if cadena_bytes != "":
        contador_bytes = contador_bytes + 1
        suma_decimal = suma_decimal + contador_bytes
        contador_bytes_hexa = "{:X}".format(contador_bytes)
        while len(contador_bytes_hexa) % 2 == 1:
            contador_bytes_hexa = "0" + contador_bytes_hexa

        suma_binaria = bin(suma_decimal)
        suma_binaria_invertida = ""
        for b in range(len(suma_binaria)):
            if suma_binaria[b:b+1] == "1":
                suma_binaria_invertida = suma_binaria_invertida + "0"
            elif suma_binaria[b:b+1] == "0":
                suma_binaria_invertida = suma_binaria_invertida + "1"
        suma_hexa = "{:X}".format(int(suma_binaria_invertida, 2))
        check_sum = suma_hexa[len(suma_hexa)-2:]

        linea_archivo = "S1" + contador_bytes_hexa + direccion + cadena_bytes + check_sum + "\n"
        f_archivo_S19.write(linea_archivo)

    f_archivo_S19.write("S9030000FC")
    f_archivo_S19.close()
    print("ARCHIVO " + n_archivo_S19 + " GENERADO.")
    muestra_archivo(n_archivo_S19)


def main():
    global ruta
    global matriz_fuente
    global matriz_var_etiquetas
    global nombre_archivo_sinext
    global n_archivo_errores
    global lista_mnemonicos
    global lista_INH
    global lista_INM
    global lista_DIR
    global lista_EXT
    global lista_INDX
    global lista_INDY
    global lista_REL
    global tipo_direccionamiento
    global direccion_inicio
    global existe_END
    global compilacion_exitosa
    global etiqueta_duplicada

    existe_END = False
    etiqueta_duplicada = False
    ruta = "/Users/emilianopaez/PyCharmMiscProject/"
    num_linea = 0

    nombre_archivo = input("Introduce el nombre del archivo a compilar: ")
    nombre_archivo_ext = nombre_archivo.split(".")
    nombre_archivo_sinext = nombre_archivo_ext[0]
    n_archivo_fuente = ruta + nombre_archivo

    f_archivo_fuente = open(n_archivo_fuente, 'r', encoding="utf-8")
    linea_archivo_fuente = f_archivo_fuente.readline()

    num_linea = num_linea + 1
    while linea_archivo_fuente != "":
        matriz_fuente.append(obtener_elementos(num_linea, linea_archivo_fuente))
        linea_archivo_fuente = f_archivo_fuente.readline()
        num_linea = num_linea + 1

    f_archivo_fuente.close()

    # CORRECCIÓN #1 y #2: bucle correctamente indentado, procesa_linea_fuente llamada dentro del if
    for linea_fuente in matriz_fuente:
        tipo_direccionamiento = ""
        if (linea_fuente[1] != "" or linea_fuente[2] != "" or
                linea_fuente[3] != "" or linea_fuente[4] != "" or linea_fuente[5] != ""):
            procesa_linea_fuente(linea_fuente)

    # CORRECCIÓN #2: llamadas que estaban fuera de main ahora correctamente dentro
    lineas_etiq_duplicadas = busca_etiquetas_duplicadas()

    if existe_END == False:
        escribe_muestra_error(matriz_fuente[len(matriz_fuente) - 1], 10)

    if etiqueta_duplicada == True:
        escribe_muestra_error(lineas_etiq_duplicadas, 12)

    genera_codigo_objeto()

    if compilacion_exitosa == False:
        print("LA COMPILACION DEL CODIGO FUENTE NO FUE EXITOSA, GENERANDO ARCHIVO .LST:", ruta + nombre_archivo_sinext + ".LST")
        genera_archivo_LST()
        genera_archivo_LST_COLOR()
    else:
        print("LA COMPILACION DEL CODIGO FUENTE FUE EXITOSA, GENERANDO LOS ARCHIVOS .LST y .S19")
        genera_archivo_LST()
        genera_archivo_S19()
        genera_archivo_LST_COLOR()
        genera_archivo_S19_MOTOROLA()
        genera_archivo_S19_MOTOROLA_COLOR()


# CORRECCIÓN #3: __name__ completo y correctamente escrito
if __name__ == "__main__":
    main()