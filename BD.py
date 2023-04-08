import pyodbc

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
    # print(b, largo)
    # print(b)
    # print("El promedio de reproduciones de "+artista+" es : "+b)
    return

def buscar(cursor, nombre_cancion):
    lista = cursor.execute("SELECT song_name FROM repositorio_musica WHERE song_name = '"+nombre_cancion+"'")
    lista2 = cursor.execute("SELECT * FROM artistsong ('"+nombre_cancion+"')")
    print(list(lista2.fetchall()))
    if len(list(lista2.fetchall())) >= 1:
        canciones = []
        for i in list(lista2.fetchall()):
            print("Hay mas de una")
            # Si hay mas de una cancion igual ver que el artista sea diferente
    print("Coincidencias encontradas")
    for i in list(lista2.fetchall()):        
        print("Canción: "+i[0]+", del artista: "+i[1])

    return



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



    # cursor.execute("DELETE FROM repositorio_musica")
    
    opciones = True
    print("Bienvenido a Spot-USM, elija una de estas opciones para realizar:")
    cursor.execute("DROP FUNCTION artistsong")
    # cursor.execute("CREATE FUNCTION GetSong (@nombre_cancion VARCHAR(100))RETURNS table as RETURN(SELECT artist_name, cant_reproducciones, fecha_reproduccion FROM reproduccion WHERE song_name like '%'+@nombre_cancion+'%')")
    cursor.execute("CREATE FUNCTION artistsong (@nombre_cancion VARCHAR(100))RETURNS table as RETURN(SELECT song_name,artist_name FROM repositorio_musica WHERE song_name like '%'+@nombre_cancion+'%')")

    while opciones:
        a = int(input("INGRESE OPCION: "))
        if a == 1:
            opciones = False
        elif a == 2:
            opciones = False
        elif a == 3:
            opciones = False
        elif a == 4:
            opciones = False
        elif a == 5:
            nombre = input("Ingrese el nombre de la canción: ")
            buscar(cursor, nombre)
            opciones = False
        elif a == 6:
            nombre = input("Ingrese el nombre de la canción: ")

            opciones = False
        elif a == 11:
            print("Por favor ingrese el nombre del artista deseado:")
            artista = input()
            promedio_artista(cursor, artista)
    #         a
        # elif a == 6:
        # elif a == 7:
        # elif a == 8:
        # elif a == 9:
        # elif a == 10:
        # elif a == 11:

    #     a = 0
    
    cursor.commit()
    cursor.close()
    coneccion.close()

if __name__ == "__main__":
    main()