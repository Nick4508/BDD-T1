import pyodbc
import datetime
import time
###############################################################################################################################################
# archivo:   position   artist_name   song_name   days    top_10    peak_position    peak_position_time    peak_streams    total_streams
#               int         str         str        int      int         int                 str                 int             int
###############################################################################################################################################
# reproduccion:
#               id PK     song_name     artist_name     fecha_reproduccion      cant_reproducciones        favorito    
#               int          str           str              date                    int                       bit
# 
# lista_favoritos:
#               id PK      song_name    artist_name         fecha_agregada  
#               int          str            str                 date
###############################################################################################################################################

# str_conect = "Driver={SQL Server};Server=LAPTOP-QKCFS38M\SQLEXPRESS;Database=Spot-USM;Trusted_Connection=True" #nick
str_conect = "Driver={SQL Server};Server=LAPTOP-334LDJSK\SQLEXPRESS;Database=Spot-USM;Trusted_Connection=True" #mat

fecha = datetime.datetime.now()


def mostrar_opciones():
    print("******************  MENÚ  ******************")
    time.sleep(1)
    print("1) Mostrar canciones reproducidas.") 
    print("2) Mostrar canciones favoritas.")
    print("3) Hacer favorita una canción.")
    print("4) Quitar el favorito de una canción.")
    print("5) Reproducir una canción.")
    print("6) Buscar una canción en la lista de canciones reproducidas.")
    print("7) Mostrar las canciones reproducidas dentro de los dias que se elijan.")
    print("8) Buscar una canción ya sea por nombre o por artista.")
    print("9) Top 15 artistas con mayor cantidad de reproducciones dentro del top 10.")
    print("10) Mostrar el peak de un artista.")
    print("11) Promedio de streams de un artista.")
    print("12) Salir de Spot-USM")


def primera_carga(cursor):
    '''
    Función que genera la primera carga de la base de datos
        Parametros:
            cursor: Para hacer querys en la base de datos desde python
    '''
    flag = False
    archivo = open("song.csv", "r", encoding= "UTF-8-sig")
    for linea in archivo:
        if flag:
            a = linea.replace("'", "").strip().split(";")
            b = ""
            for i in a:
                b = b + "'"+ i+ "'"+ ","
            b = b[:-1]
            cursor.execute("INSERT INTO repositorio_musica (position, artist_name, song_name, days, top_10, peak_position, peak_position_time, peak_streams, total_streams) VALUES ("+ b+")")
        flag = True
    archivo.close()

def query_1(cursor, orden):
    '''
    Función que muestra las canciones que están en la tabla reproducción
        Parametros:
            orden(String): Orden por el cual se desea mostrar la lista (fecha/cant_reproducciones)
    '''
    if orden == "1":
        query = cursor.execute("SELECT * FROM reproduccion ORDER BY cant_reproducciones DESC")
        lista_ordenada = list(query.fetchall())
        for i in lista_ordenada:
            if i[-1] == False:
                fav = "no"
            else:
                fav = "si"
            print("Cantidad de veces reproducida:",i[4],"Nombre canción:",i[1],"de",i[2],"Primera reproduccion",i[3],"Favorito:",fav)
    elif orden == "2":
        query = cursor.execute("SELECT * FROM reproduccion ORDER BY fecha_reproduccion DESC")
        lista_ordenada = list(query.fetchall())
        for i in lista_ordenada:
            if i[-1] == False:
                fav = "si"
            else:
                fav = "no"
            print("Cantidad de veces reproducida:",i[4],"Nombre canción:",i[1],"de",i[2],"Primera reproduccion",i[3],"Favorito:",fav)

def query_5(cursor, nombre_cancion):
    '''
    Función que muestra las canciones que el usuario haya escuchado en los X días
        Parametros:
            nombre_cancion(String): Simula la reproduccion de una canción
    '''
    query = cursor.execute("SELECT * FROM artistsong ('"+nombre_cancion+"')")
    lista_canciones = list(query.fetchall())
    print("Coincidencias encontradas: ")
    for i in lista_canciones:
        print(str(i[2])+") Canción: "+i[0]+" del artista "+ i[1])
    id = input("Seleccione según el id de la canción: ")
    query3 = cursor.execute("SELECT id FROM reproduccion WHERE id = "+ id +"")
    a = query3.fetchone()
    
    if a == None:
        query2 = cursor.execute("SELECT id, song_name, artist_name FROM repositorio_musica WHERE id = "+ id +"")
        datos_canciones = list(query2.fetchall())
        cursor.execute("INSERT INTO reproduccion (id, song_name, artist_name, fecha_reproduccion, cant_reproducciones, favorito) VALUES (?,?,?,?,?,?)", datos_canciones[0][0], datos_canciones[0][1], datos_canciones[0][2], fecha, 1, False)
        print("Se esta reproduciendo: "+ datos_canciones[0][1] + " del artista "+ datos_canciones[0][2])
        query3 = cursor.execute("SELECT id FROM lista_favoritos WHERE id = "+ id +"")
        a = query3.fetchall()
        if len(a) > 0:
            cursor.execute("UPDATE reproduccion SET favorito = 'True' WHERE id = ?", id)
    else:
        cursor.execute("UPDATE reproduccion SET cant_reproducciones = (cant_reproducciones + 1) WHERE id = "+ id +"")
        query2 = cursor.execute("SELECT id, song_name, artist_name FROM repositorio_musica WHERE id = "+ id +"")
        datos_canciones = list(query2.fetchall())
        print("Se esta reproduciendo: "+ datos_canciones[0][1] + " del artista "+ datos_canciones[0][2])

def query_6(cursor,nombre):
    '''
    Función que  busca y muestra la cancion y su información de la tabla reproduccion
        Parametros:
            nombre(String): nombre de la cancion
    '''
    query = cursor.execute("SELECT song_name, artist_name, cant_reproducciones, fecha_reproduccion FROM reproduccion WHERE song_name = ?", nombre)
    datos = list(query.fetchall())

    if len(datos) == 0:
        print("Esta canción no esta en tu lista de reproducción")
    else:
        for i in datos:
            print("Canción:", i[0],"Artista:", i[1]+"Veces reproducida:", i[2])


def query_7(cursor, delta_fecha, dias):
    '''
    Función que muestra las canciones que el usuario haya escuchado en los X días
        Parametros:
            delta_fecha(String): Categoria por la cual se quiere ordenar la lista de reproduccion puede ser fecha o cantidad
            dias(String): Orden por el cual se desea ordenar la lista puede ser ASC/DESC
    '''
    query = cursor.execute("SELECT song_name, artist_name FROM reproduccion WHERE fecha_reproduccion >= ?",delta_fecha)
    datos = list(query.fetchall())
    if len(datos) > 0:
        print("Las canciones reproducidas hace",dias,"días son:")
        for i in datos:
            print(i[0],"de",i[1])
    else:
        print("No hay canciones registradas hace",dias,"días")

def promedio_artista(cursor, artista):
    lista = cursor.execute("SELECT avg(total_streams) FROM repositorio_musica WHERE artist_name = '"+artista+"'")
    b = lista.fetchall()
    if b[0][0] == None:
        print("No se encontraron reproducciones asociadas a ese artista")
    else:
        print("El promedio de reproduciones de "+artista+" es : "+str(b[0][0]))

def peak_artista(cursor, artista):   

    query = cursor.execute("SELECT min(peak_position) FROM repositorio_musica where artist_name ='"+artista+"'")
    peak = query.fetchone()
    if  peak[0] == None:
        print("El artista no exista en nuestros registros, lo sentimos.")
    elif peak[0] == 0 or peak[0] > 10 :
        print(artista,"no estuvo en el top 10")
    else:
        print("La posición máxima que alcanzó "+artista+" fue la numero: "+ str(peak[0]))


def top_15(cursor):
    query = cursor.execute("SELECT TOP 15 sum(top_10) AS suma_top ,artist_name FROM repositorio_musica GROUP BY artist_name ORDER BY suma_top DESC")
    top = query.fetchall()
    print("El top 15 artistas con mas reproducciones dentro del top 10 son:")
    x = 1
    for i in top:
        print(str(x)+")",str(i[1])+"con",str(i[0]),"streams dentro del top 10")
        x+=1

def busqueda_repositorio(cursor, opcion, nombre):
    if opcion == "1": # artista
        lista = cursor.execute("SELECT * FROM mostrar_repositorio_artista WHERE artist_name like '%"+ nombre+"%'")
        b = lista.fetchall()
        if len(b)== 0:
            print("Tal vez introdujiste mal el nombre del artista, intenta otra vez")
        else:
            print("Datos de las canciones del artista: posicion/nombre_cancion/total_reproducciones")
            for i in b:
                print(str(i[0])+")",i[2] ,i[4] )
    elif opcion == "2": #cancion
        lista = cursor.execute("SELECT * FROM mostrar_repositorio_artista where song_name like '%"+nombre+"%'")
        b = lista.fetchall()
        if len(b) == 0:
            print("No se encontraron canciones y/o artistas asociados")
        else:
            print("Datos de las canciones encontradas: posicion/nombre_cancion/nombre_artista/top_10")
            for i in b:
                print(str(i[0])+")",i[2],"del artista",i[1]+"la cual la estuvo",i[3],"veces dentro del top_10" )
        

def hacer_favorito(cursor,song_name):
    '''
    Función agrega la cancion seleccionada a la tabla de favoritos
        Parametros:
            song_name(String): nombre de la canción que se desea agregar
    '''
    query = cursor.execute("SELECT id, song_name, artist_name FROM repositorio_musica WHERE song_name like '"+song_name+"%'")
    canciones = query.fetchall()

    print("Elija el numero de la cancion que quiere hacer favorita")
    for i in canciones:
        print(str(i[0])+")",str(i[1]), "del artista :", str(i[2]))
    id = int(input("Cancion numero: "))

    query2 = cursor.execute("SELECT id, song_name, artist_name FROM repositorio_musica WHERE id = '"+str(id)+"'")
    cancion = query2.fetchall()
    comprobar = cursor.execute("SELECT id FROM lista_favoritos WHERE id = ?", id)
    if len(comprobar.fetchall()) > 0:
        print("Esta canción ya está en favoritos")
        return
    cursor.execute("INSERT INTO lista_favoritos (id,song_name,artist_name,fecha_agregada) VALUES (?,?,?,?)",cancion[0][0],cancion[0][1],cancion[0][2],fecha)
    query3 = cursor.execute("SELECT id FROM reproduccion WHERE id = ?", id)
    if len(query3.fetchall()) == 0:
        print("Se ha añadido a favoritos la canción escogida")
    else:
        cursor.execute("UPDATE reproduccion SET favorito = 'True' WHERE id = ?", id)
        print("Se ha añadido a favoritos la canción escogida")

def mostrar_favoritos(cursor):
    '''
    Función que muestra las canciones que se encuentran en favoritos
        Parametros:
            cursor: se hacen las querys para mostrar por pantalla la tabla
    '''
    query = cursor.execute("SELECT * FROM lista_favoritos")
    listado = query.fetchall()

    flag = True
    if len(listado) == 0:
        print("No tienes canciones en favorito")
    else:
        if flag:
            print("Tus canciones favoritas son :")
        for i in listado:
            print(str(i[0])+")"+i[1] , "del artista", i[2], "la cual fue agregada en la fecha: ",i[3])
        

def quitar_favorito(cursor):
    '''
    Función que quita las canciones de la tabla de favoritos
        Parametros:
            cursor: Hace las querys que se necesitan para actualizar la tabla
    '''
    query = cursor.execute("SELECT * FROM lista_favoritos")
    favoritos = query.fetchall()

    if len(favoritos) == 0:
        print("No tienes canciones en favorito")
    else:
        for i in favoritos:
            print(str(i[0])+")",i[1],"del artista",i[2])
        id = int(input("Elija el numero de la cancion que quiere quitar :"))
        cursor.execute("DELETE FROM lista_favoritos WHERE id = ? ",id)
        cursor.execute("UPDATE reproduccion SET favorito = 'False' WHERE id = ?", id)
        print("La canción se ha eliminado correctamente")


def main():
    coneccion = pyodbc.connect(str_conect)
    cursor = coneccion.cursor()    
    # cursor.execute("DROP TABLE repositorio_musica")
    # cursor.execute("DROP TABLE lista_favoritos")
    # cursor.execute("DROP TABLE reproduccion")
    # cursor.execute("DROP VIEW mostrar_repositorio_artista")
    # cursor.execute("DROP FUNCTION artistsong")
    if not cursor.tables(table = "repositorio_musica").fetchone():
        cursor.execute("CREATE TABLE repositorio_musica (id int IDENTITY(1,1) PRIMARY KEY, position int, artist_name VARCHAR(100), song_name VARCHAR(100), days int, top_10 int, peak_position bigint, peak_position_time VARCHAR(10), peak_streams bigint, total_streams bigint)")
        primera_carga(cursor=cursor)

        cursor.execute("CREATE TABLE lista_favoritos (id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_agregada DATE)")
        cursor.execute("CREATE TABLE reproduccion (id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_reproduccion DATE, cant_reproducciones bigint, favorito bit)")
        cursor.execute("CREATE VIEW mostrar_repositorio_artista AS SELECT position, artist_name, song_name, top_10, total_streams FROM repositorio_musica")
        cursor.execute("CREATE FUNCTION artistsong (@nombre_cancion VARCHAR(100))RETURNS table as RETURN SELECT song_name,artist_name,id FROM repositorio_musica WHERE song_name like @nombre_cancion+'%'")
    cursor.commit()
    # cursor.execute("DELETE FROM repositorio_musica")
    

   
    opciones = True
    print("Bienvenido a Spot-USM, elija una de estas opciones para realizar:")
    mostrar_opciones()
    while opciones:
        
        time.sleep(0.5)
        a = input("INGRESE OPCION: ")
        print("**********************************")
        try:
            a = int(a)
        except ValueError:
            pass
        if a == 1:
            orden = input("Seleccione el orden de su lista de reproducciones (1/2) \n 1) cantidad de reproducciones \n 2) fecha \n")
            query_1(cursor, orden)
            mostrar_opciones()
        elif a == 2:
            mostrar_favoritos(cursor)
            mostrar_opciones()

        elif a == 3:
            song_name = input("Ingrese nombre de la canción que desea hacer favorita: ")
            hacer_favorito(cursor, song_name)
            mostrar_opciones()

        elif a == 4:
            quitar_favorito(cursor)
            mostrar_opciones()

        elif a == 5:
            nombre = input("Ingrese el nombre de la canción: ")
            query_5(cursor, nombre)
            mostrar_opciones()
            
        elif a == 6:
            nombre = input("Ingrese el nombre de la canción: ")
            query_6(cursor,nombre)
            mostrar_opciones()
        elif a== 7:
            X = int(input("Las canciones que has escuchado desde hace cuantos días?\n"))
            x_dia = fecha - datetime.timedelta(days=X)

            query_7(cursor,x_dia,X)
            mostrar_opciones()
        elif a == 8:
            opcion = input("Desea buscar por artista o canción? (ingrese 1 para buscar por nombre de artista, 2 para buscar por nombre de canción) : ")
            if opcion == "1" or opcion == "2":
                nombre = input("ingrese nombre de artista/canción: ")
                busqueda_repositorio(cursor, opcion, nombre)
            else: 
                print("Lo siento no escogiste una opción válida")
            mostrar_opciones()

        elif a == 9:
            top_15(cursor)
            print("**********************************")
            mostrar_opciones()

        elif a == 10:
            opcion = input("Ingrese nombre del artista deseado: ")
            peak_artista(cursor, opcion)
            print("**********************************")
            mostrar_opciones()

        elif a == 11:
            print("Por favor ingrese el nombre del artista deseado:")
            artista = input()
            promedio_artista(cursor, artista)
            print("**********************************")
            mostrar_opciones()

        elif a == 12:
            print("Gracias por interactuar con Spot-USM")
            break

        else: 
            print("*********Error en opción ingresada, por favor ingrese una opción válida*********")
            mostrar_opciones()


    cursor.commit()
    cursor.close()
    coneccion.close()

if __name__ == "__main__":
    main()