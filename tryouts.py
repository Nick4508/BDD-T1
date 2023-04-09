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

str_conect = "Driver={SQL Server};Server=LAPTOP-QKCFS38M\SQLEXPRESS;Database=Spot-USM;Trusted_Connection=True" #nick
# str_conect = "Driver={SQL Server};Server=LAPTOP-334LDJSK\SQLEXPRESS;Database=Spot-USM;Trusted_Connection=True" #mat



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
    query = cursor.execute("SELECT sum(top_10),artist_name FROM repositorio_musica GROUP BY artist_name")
    top = query.fetchall()
    new = sorted(top)
    new.reverse()
    print(str(new[:14]))
    # for i in top:
        # print(str(i))
    print(str(top[-15::]))

def busqueda_repositorio(cursor, opcion, nombre):
    if opcion == "1": # artista
        lista = cursor.execute("SELECT song_name, top_10, total_streams FROM mostrar_repositorio_artista WHERE artist_name = '"+ nombre+"'")
        b = lista.fetchall()
        for i in b:
            cancion = i[0]
            top = i[1]
            total = i[2]
            print(cancion,str(top), str(total))
    elif opcion == "2": #cancion
        lista = cursor.execute("SELECT artist_name, top_10, total_streams FROM mostrar_repositorio_artista where song_name = '"+nombre+"'")
        b = lista.fetchall()
        for i in b:
            artista = i[0]
            top = i[1]
            total = i[2]
            print(artista, str(top), str(total))

    # return

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
    cursor.execute("CREATE VIEW mostrar_repositorio_artista AS SELECT position, artist_name, song_name, top_10, total_streams FROM repositorio_musica")


    # cursor.execute("DELETE FROM repositorio_musica")
    

   
    opciones = True
    print("Bienvenido a Spot-USM, elija una de estas opciones para realizar:")


    while opciones:
        a = int(input("INGRESE OPCION: "))
        if a == 1:
            b
        elif a == 2:
            b
        elif a == 3:
            b
        elif a == 4:
            a
        elif a == 5:
            a
        # elif a == 6:
        # elif a == 7:
        elif a == 8:
            opcion = input("Desea buscar por artista o canción? (ingrese 1 para buscar por nombre de artista, 2 para buscar por nombre de canción) : ")
            nombre = input("ingrese nombre de artista/canción :")
            if opcion == "1" or opcion == "2":
                
                busqueda_repositorio(cursor, opcion, nombre)
            else: 
                print("Lo siento no escogiste una opción válida")
        elif a == 9:
            top_15(cursor)
        elif a == 10:
            opcion = input("Ingrese nombre del artista deseado: ")
            peak_artista(cursor, opcion)
        elif a == 11:
            print("Por favor ingrese el nombre del artista deseado:")
            artista = input()
            promedio_artista(cursor, artista)
        elif a == 12:
            print("Salir")
        else: 
            print("Error en opción ingresada, por favor ingrese una opción válida")

    #     a = 0
    
    cursor.commit()
    cursor.close()
    coneccion.close()

if __name__ == "__main__":
    main()