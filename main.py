import xml.etree.ElementTree as ET
from Lista import ListaEnlazada
import os

raiz=0
HistorialDimensiones = ListaEnlazada()
TodasLasRutas = ListaEnlazada()

def Recoger(ruta):
    """Datos del XML"""
    arbol = ET.parse(ruta)
    global raiz
    raiz = arbol.getroot()


def Procesar(nombre):
    """Obtener terrenos"""
    for terrenos in raiz:
        if(terrenos.attrib["nombre"]==nombre):
            """Determinar las dimensiones del terreno"""
            for dimension in terrenos.iter("m"):
                m = int(dimension.text)
            for dimension in terrenos.iter("n"):
                n = int(dimension.text)

            """Determinar entrada y salida del terreno"""
            iniciox = 0
            inicioy = 0
            finalx = 0
            finaly = 0
            for posicioninicial in terrenos.iter("posicioninicio"):
                for x in posicioninicial.iter("x"):
                    iniciox = int(x.text)
                for y in posicioninicial.iter("y"):
                    inicioy = int(y.text)

            for posicionfinal in terrenos.iter("posicionfin"):
                for x in posicionfinal.iter("x"):
                    finalx = int(x.text)
                for y in posicionfinal.iter("y"):
                    finaly = int(y.text)

            if finalx>iniciox:
                cambiox=1
            else:
                cambiox=-1

            if finaly>inicioy:
                cambioy=1
            else:
                cambioy=-1

            """Arreglo con posiciones con y como columnas y x como filas"""
            contador = 0
            Gasolinas = ListaEnlazada()
            for gasolina in terrenos.iter("posicion"):
                posx = int(gasolina.attrib["x"])
                posy = int(gasolina.attrib["y"])
                if (contador == (posx - 1) * n + (posy - 1)):
                    Gasolinas.Append(gasolina.text)
                    contador += 1

            """Mostrar mapa"""
            Mapa = ""
            for i in range(m):
                for j in range(n):
                    Mapa += (Gasolinas.Seleccionar((i * m) + j) + " ")
                Mapa += "\n"

            print(Mapa)

            i = inicioy - 1
            j = iniciox - 1
            suma = 0
            Recorrido1 = ListaEnlazada()
            while (i != (finalx - 1) or j != (finaly - 1)):
                if (j == (finaly - 1)):
                    Recorrido1.Append(i)
                    Recorrido1.Append(j)
                    suma += int(Gasolinas.Seleccionar(((i * m) + j) + 1))
                    i += cambioy
                elif (i == (finalx - 1)):
                    Recorrido1.Append(i)
                    Recorrido1.Append(j)
                    suma += int(Gasolinas.Seleccionar(((i * m) + j) + m))
                    j += cambiox
                elif (int(Gasolinas.Seleccionar(((i * m) + j) + (m*cambiox))) > int(Gasolinas.Seleccionar(((i * m) + j) + cambioy))):
                    Recorrido1.Append(i)
                    Recorrido1.Append(j)
                    suma += int(Gasolinas.Seleccionar(((i * m) + j) + 1))
                    j += cambioy
                else:
                    Recorrido1.Append(i)
                    Recorrido1.Append(j)
                    suma += int(Gasolinas.Seleccionar(((i * m) + j) + m))
                    i += cambiox
                Recorrido1.Append(suma)

    ListaRuta = ListaEnlazada()
    String=""
    print(Recorrido1)
    for i in range(m*n):
        for j in range(2,len(Recorrido1),3):
            if(((int(Recorrido1.Seleccionar(j-2)))*m+int(Recorrido1.Seleccionar(j-1)))==i or i == (((finalx-1)*m)+finaly-1)):
                positivo=True
                break;
            else:
                positivo=False

        if(positivo==True):
            ListaRuta.Append(1)
        else:
            ListaRuta.Append(0)
    ultimo=len(Recorrido1)-1
    totalGasolina=int(Recorrido1.Seleccionar(ultimo))
    totalGasolina+=int(Gasolinas.Seleccionar(0))
    print("El total de gasolina ocupado es de: " + str(totalGasolina))

    print(Mapa)

    print(ListaRuta)
    MostrarLista=""
    for i in range(m):
        for j in range(n):
            MostrarLista += (ListaRuta.Seleccionar((i * m) + j) + " ")
        MostrarLista += "\n"

    print(MostrarLista)
    HistorialDimensiones.Append(m)
    HistorialDimensiones.Append(n)
    dimensionInicial = 0
    dimensionFinal = 0

    for i in range(len(ListaRuta)):
        TodasLasRutas.Append(ListaRuta.Seleccionar(i))

    for i in range(len(HistorialDimensiones)):
        if(i+1 == len(HistorialDimensiones) or i+2 == len(HistorialDimensiones)):
            if(i%2==0):
                anterior = int(HistorialDimensiones.Seleccionar(i))
            else:
                dimensionFinal += (anterior * int(HistorialDimensiones.Seleccionar(i))) + dimensionInicial
        elif(i%2==0):
            anterior=int(HistorialDimensiones.Seleccionar(i))
        else:
            dimensionInicial+=(anterior*int(HistorialDimensiones.Seleccionar(i)))
    dato=""
    print(HistorialDimensiones)
    for i in range(dimensionInicial,dimensionFinal):
        dato+=str(TodasLasRutas.Seleccionar(i))+" "
    print(dato)

def Seleccionar():
    print("1. Ingresar mapa: ")
    print("2. Procesar archivo")
    print("3. Escribir archivo salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar gráfica")
    print("6. Salida")
    opcion = int(input("Ingrese una opción: "))
    if(opcion==1):
        ruta = input("Digite una ruta: ")
        Recoger(ruta)
    elif(opcion==2):
        nombre = input("Digite el nombre del mapa: ")
        Procesar(nombre)
    elif(opcion==3):
        ArchivoSalida()
    elif(opcion==4):
        MostrarDatos()
    elif(opcion==5):
        nombre = input("Ingrese el nombre")
    elif(opcion==6):
        quit()

def ArchivoSalida():
    ruta=input("Digite la ruta de salida del archivo: ")
    file = open(ruta, "w")
    String="<terrenos>"

    """Obtener terrenos"""
    for terrenos in raiz:
        String+= """\n\t<terreno nombre=\"""" + terrenos.attrib["nombre"] +"""\">"""
        """Determinar las dimensiones del terreno"""
        for dimension in terrenos.iter("m"):
            m = int(dimension.text)
        for dimension in terrenos.iter("n"):
            n = int(dimension.text)

        """Determinar entrada y salida del terreno"""
        iniciox = 0
        inicioy = 0
        finalx = 0
        finaly = 0
        String+="\n\t\t<posicioninicio>"
        for posicioninicial in terrenos.iter("posicioninicio"):
            for x in posicioninicial.iter("x"):
                iniciox = int(x.text)
                String+="""\n\t\t\t<x>""" + str(x.text) + """</x>"""
            for y in posicioninicial.iter("y"):
                inicioy = int(y.text)
                String+="""\n\t\t\t<y>""" + str(y.text) + """</y>"""
        String += """
\t\t</posicioninicio>"""
        String+="""
\t\t<posicionfinal>"""
        for posicionfinal in terrenos.iter("posicionfin"):
            for x in posicionfinal.iter("x"):
                finalx = int(x.text)
                String += """
\t\t\t<x>""" + str(x.text) + """</x>"""
            for y in posicionfinal.iter("y"):
                finaly = int(x.text)
                String += """ 
\t\t\t<y>""" + str(y.text) + """</y>"""
        String += """
\t\t</posicionfinal>"""

        if finalx > iniciox:
            cambiox = 1
        else:
            cambiox = -1

        if finaly > inicioy:
            cambioy = 1
        else:
            cambioy = -1

        """Arreglo con posiciones con y como columnas y x como filas"""
        contador = 0
        Gasolinas = ListaEnlazada()
        for gasolina in terrenos.iter("posicion"):
            posx = int(gasolina.attrib["x"])
            posy = int(gasolina.attrib["y"])
            if (contador == (posx - 1) * n + (posy - 1)):
                Gasolinas.Append(gasolina.text)
                contador += 1


        i = inicioy - 1
        j = iniciox - 1
        suma = 0
        print(Gasolinas)
        StringPendiente= ""

        while (i != (finaly - 1) or j != (finalx - 1)):
            if (i == (finaly - 1)):
                StringPendiente+="""\n\t\t<posicion x=\"""" + str(i+1) + """\" y=\"""" + str(j+1) + """\">"""+ str(Gasolinas.Seleccionar(((i * m) + j))) + """</posicion>"""
                suma += int(Gasolinas.Seleccionar(((i * m) + j) + 1))
                j += cambioy
            elif (j == (finalx - 1)):
                StringPendiente+="""\n\t\t<posicion x=\"""" + str(i+1) + """\" y=\"""" + str(j+1) + """\">"""+ str(Gasolinas.Seleccionar(((i * m) + j))) + """</posicion>"""
                suma += int(Gasolinas.Seleccionar(((i * m) + j) + m))
                i += cambiox
            elif (int(Gasolinas.Seleccionar(((i * m) + j) + (m * cambiox))) > int(Gasolinas.Seleccionar(((i * m) + j) + cambioy))):
                StringPendiente+="""\n\t\t<posicion x=\"""" + str(i+1) + """\" y=\"""" + str(j+1) + """\">"""+ str(Gasolinas.Seleccionar(((i * m) + j))) + """</posicion>"""
                suma += int(Gasolinas.Seleccionar(((i * m) + j) + 1))
                j += cambioy
            else:
                StringPendiente+="""\n\t\t<posicion x=\"""" + str(i+1) + """\" y=\"""" + str(j+1) + """\">"""+ str(Gasolinas.Seleccionar(((i * m) + j))) + """</posicion>"""
                suma += int(Gasolinas.Seleccionar(((i * m) + j) + m))
                i += cambiox

        StringPendiente += """\n\t\t<posicion x=\"""" + str(finalx) + """\" y=\"""" + str(finaly) + """\">""" + str(Gasolinas.Seleccionar((finalx-1)*m+(finaly-1))) + """</posicion>"""
        String += """\n\t\t<combustible>""" + str(int(suma) + int(Gasolinas.Seleccionar(0))) + """</combustible>"""
        String+=StringPendiente
        String+="""\n\t</terreno>"""
    String+="""
</terrenos>"""
    file.write(String)
    file.close()


def MostrarDatos():
    print("Cristian Raúl Vega Rodríguez")
    print("202010942")
    print("Introducción a la Programación y Computación 2 sección A")
    print("Ingeniería en Ciencias y Sistemas")
    print("4to. semestre")

if __name__ == '__main__':
    while(True):
        Seleccionar()
