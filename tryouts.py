import pyodbc
from datetime import datetime
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

str_conect = "Driver={SQL Server};Server=LAPTOP-QKCFS38M\SQLEXPRESS;Database=Spot-USM;Trusted_Connection=True" #nick
# str_conect = "Driver={SQL Server};Server=LAPTOP-334LDJSK\SQLEXPRESS;Database=Spot-USM;Trusted_Connection=True" #mat



def mostrar_opciones():
    print("******************  MENÚ  ******************")
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


    return

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
        

    # return

def hacer_favorito(cursor,song_name):
    query = cursor.execute("SELECT id, song_name, artist_name FROM repositorio_musica WHERE song_name like '"+song_name+"%'")
    canciones = query.fetchall()

    print("Elija el numero de la cancion que quiere hacer favorita")
    for i in canciones:
        print(str(i[0])+")",str(i[1]), "del artista :", str(i[2]))
    id = int(input("Cancion numero: "))

    query2 = cursor.execute("SELECT id, song_name, artist_name FROM repositorio_musica WHERE id = '"+str(id)+"'")
    cancion = query2.fetchall()
    
    cursor.execute("INSERT INTO lista_favoritos (id,song_name,artist_name,fecha_agregada) VALUES (?,?,?,?)",cancion[0][0],cancion[0][1],cancion[0][2],datetime.now())
    print("Se ha añadido a favoritos la canción escogida")
    return

def mostrar_favoritos(cursor):
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
        

    return

def quitar_favorito(cursor):
    query = cursor.execute("SELECT * FROM lista_favoritos")
    favoritos = query.fetchall()


    for i in favoritos:
        print(str(i[0])+")",i[1],"del artista",i[2])
    a = int(input("Elija la cancion que quiere quitar :"))
    cursor.execute("DELETE FROM lista_favoritos WHERE id = ? ",a)    

def main():
    coneccion = pyodbc.connect(str_conect)
    cursor = coneccion.cursor()    
    # cursor.execute("DROP TABLE repositorio_musica")
    # cursor.execute("DROP TABLE lista_favoritos")
    # cursor.execute("DROP TABLE reproduccion")
    # cursor.execute("DROP VIEW mostrar_repositorio_artista")

    if not cursor.tables(table = "repositorio_musica").fetchone():
        cursor.execute("CREATE TABLE repositorio_musica (id int IDENTITY(1,1) PRIMARY KEY, position int, artist_name VARCHAR(100), song_name VARCHAR(100), days int, top_10 int, peak_position bigint, peak_position_time VARCHAR(10), peak_streams bigint, total_streams bigint)")
        primera_carga(cursor=cursor)

        cursor.execute("CREATE TABLE lista_favoritos (id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_agregada DATE)")
        cursor.execute("CREATE TABLE reproduccion (id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_reproduccion DATE, cant_reproducciones bigint, favorito bit)")
        cursor.execute("CREATE VIEW mostrar_repositorio_artista AS SELECT position, artist_name, song_name, top_10, total_streams FROM repositorio_musica")

    cursor.commit()
    # cursor.execute("DELETE FROM repositorio_musica")
    

   
    opciones = True
    print("Bienvenido a Spot-USM, elija una de estas opciones para realizar:")
    mostrar_opciones()

    while opciones:
        a = input("INGRESE OPCION: ")
        print("**********************************")
        try:
            a = int(a)
        except ValueError:
            pass
        if a == 1:
            b
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
            a
        # elif a == 6:
        # elif a == 7:
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

    #     a = 0
    
    cursor.commit()
    cursor.close()
    coneccion.close()

if __name__ == "__main__":
    main()