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



def buscar(cursor, nombre_cancion):
    return 0



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

    # cursor.execute("CREATE FUNCTION GetSong (@nombre_cancion VARCHAR(100))RETURNS table as RETURN(SELECT artist_name, cant_reproducciones, fecha_reproduccion FROM reproduccion WHERE song_name like '%'+@nombre_cancion+'%')")
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
            opciones = False
        elif a == 6:
            nombre = input("Ingrese el nombre de la canción: ")
            cursor.execute("SELECT * FROM GetSong('"+nombre+"')")
            opciones = False

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