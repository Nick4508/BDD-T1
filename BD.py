import pyodbc
import datetime

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

fecha = datetime.datetime.utcnow()
print(fecha)


def mostrar_opciones():
    print("1) Mostrar canciones reproducidas.")
    print("2) Mostrar canciones favoritas.")
    print("3) Hacer favorita una canción.")
    print("4) Quitar el favorito de una canción.")
    print("5) Reproducir una canción.")
    print("5) Buscar una canción en la lista de canciones reproducidas.")
    print("6)")


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


def query_1(cursor, orden):
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


def promedio_artista(cursor, artista):
    b = 0
    lista = cursor.execute("SELECT total_streams FROM repositorio_musica WHERE artist_name = '"+artista+"'")
    largo = 0
    for i in list(lista.fetchall()):
        largo+=1
        b = b+i[0]
    if b == 0:
        print("No se encontraron reproducciones asociadas a ese artista")
    else:
        print(artista+ " tiene "+str(b//largo)+" en promedio de sus reproducciones.")


def query_5(cursor, nombre_cancion):
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
        a = query3.fetchone()
    else:
        cursor.execute("UPDATE reproduccion SET cant_reproducciones = (cant_reproducciones + 1) WHERE id = "+ id +"")
        query2 = cursor.execute("SELECT id, song_name, artist_name FROM repositorio_musica WHERE id = "+ id +"")
        datos_canciones = list(query2.fetchall())
        print("Se esta reproduciendo: "+ datos_canciones[0][1] + " del artista "+ datos_canciones[0][2])


def query_6(cursor,nombre):
    query = cursor.execute("SELECT song_name, artist_name, cant_reproducciones, fecha_reproduccion FROM reproduccion WHERE song_name = ?", nombre)
    datos = list(query.fetchall())
    for i in datos:
        print("Canción:", i[0],"Artista: ", i[1],"Veces reproducciones: ", i[2])


def query_7(cursor, X):
    '''
    Función que muestra las canciones que el usuario haya escuchado en los X días
        Parametros:
            X(String): Categoria por la cual se quiere ordenar la lista de reproduccion puede ser fecha o cantidad
            order(String): Orden por el cual se desea ordenar la lista puede ser ASC/DESC
    '''
    query = cursor.execute("SELECT song_name, artist_name FROM reproduccion WHERE fecha_reproduccion BETWEEN ? and ?",X , fecha)
    datos = list(query.fetchall())
    if len(datos) > 0:
        print("Las canciones entre las fechas",X,"y",fecha,":")
        for i in datos:
            print(i[0],"de",i[1])
    else:
        print("No hay canciones registradas hace",X,"días")




def main():
    coneccion = pyodbc.connect(str_conect)
    cursor = coneccion.cursor()
    # cursor.execute("DROP TABLE repositorio_musica")
    # cursor.execute("DROP TABLE lista_favoritos")
    # cursor.execute("DROP TABLE reproduccion")

    if not cursor.tables(table = "repositorio_musica").fetchone():
        cursor.execute("CREATE TABLE repositorio_musica (id int IDENTITY(1,1) PRIMARY KEY, position int, artist_name VARCHAR(100), song_name VARCHAR(100), days int, top_10 int, peak_position bigint, peak_position_time VARCHAR(10), peak_streams bigint, total_streams bigint)")
        primera_carga(cursor=cursor)
        cursor.execute("CREATE TABLE lista_favoritos (id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_agregada DATE)")
        cursor.execute("CREATE TABLE reproduccion (id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_reproduccion DATE, cant_reproducciones bigint, favorito bit)")
    
    opciones = True
    print("Bienvenido a Spot-USM, elija una de estas opciones para realizar:")
    cursor.execute("DROP FUNCTION artistsong")
    cursor.execute("CREATE FUNCTION artistsong (@nombre_cancion VARCHAR(100))RETURNS table as RETURN(SELECT song_name,artist_name,id FROM repositorio_musica WHERE song_name like '%'+@nombre_cancion+'%')")

    while opciones:
        a = int(input("INGRESE OPCION: "))
        if a == 1:
            orden = input("Seleccione el orden de su lista de reproducciones (1/2) \n 1) cantidad de reproducciones \n 2) fecha \n")
            query_1(cursor, orden)
        elif a == 2:
            opciones = False
        elif a == 3:
            nombre_c = input("Ingrese la canción que desea agregar a la lista de favoritos: ")
            cursor.execute("INSERT INTO lista_favoritos")
            opciones = False
        elif a == 4:
            opciones = False
        elif a == 5:
            nombre = input("Ingrese el nombre de la canción: ")
            query_5(cursor, nombre)
        elif a == 6:
            nombre = input("Ingrese el nombre de la canción: ")
            query_6(cursor,nombre)
        elif a == 7:
            X = int(input("Las canciones que has escuchado desde hace cuantos días?\n"))
            x_dia = fecha - datetime.timedelta(days=X)
            query_7(cursor,x_dia)
        elif a == 11:
            print("Por favor ingrese el nombre del artista deseado:")
            artista = input()
            promedio_artista(cursor, artista)
    
    cursor.commit()
    cursor.close()
    coneccion.close()

if __name__ == "__main__":
    main()