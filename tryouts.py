import pyodbc
<<<<<<< HEAD
=======

#str_conect = "Driver = {SQL Server}, Server = LAPTOP-QKCFS38M\SQLEXPRESS; Database = Spot-USM; Trusted_Connection = True" #nick
str_conect = "Driver={SQL Server};Server=LAPTOP-334LDJSK\SQLEXPRESS;Database=Spot-USM;Trusted_Connection=True" #mat
coneccion = pyodbc.connect(str_conect)
cursor = coneccion.cursor()

cursor.execute("CREATE TABLE repositorio_musica (id int IDENTITY(1,1) PRIMARY KEY, position int , artist_name VARCHAR(100), song_name VARCHAR(100), days int, top_10 int, peak_position int, peak_position_time VARCHAR(10), peak_streams int, total_streams int)")
cursor.execute("CREATE TABLE reproduccion (id int IDENTITY(1,1) PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_reproduccion DATE, can_reproducciones bigint, favorito bit)")
cursor.execute("CREATE TABLE lista_favoritos (id int IDENTITY(1,1) PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_agregada DATE)")
<<<<<<< Updated upstream
=======
>>>>>>> d3c245220071c3451d535774fb4dd95cfe6e2bb4
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
coneccion = pyodbc.connect("Driver={SQL Server};Server=LAPTOP-QKCFS38M\SQLEXPRESS;Database=Spot-USM;Trusted_Connection=True")
cursor = coneccion.cursor()

def existe_tabla(cursor, tabla):
    '''
    Determina si existe una tabla en la base de datos.

        Parametros:
            cursor (Cursor de pyodbc): Cursor de conección.
            tabla (str): Nombre de la tabla.
        Retorno:
            (bool): True si existe la tabla, False si no.
    '''
    return cursor.tables(table=tabla, tableType='TABLE').fetchone() 
if not existe_tabla(cursor, "repositorio_musica"):
    print("no existian")
    cursor.execute("CREATE TABLE repositorio_musica ( id int IDENTITY(1,1) PRIMARY KEY, position int , artist_name VARCHAR(100), song_name VARCHAR(100), days int, top_10 int, peak_position int, peak_position_time VARCHAR(10), peak_streams int, total_streams int)")
    cursor.execute("CREATE TABLE reproduccion ( id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_reproduccion DATE, cant_reproducciones int, favorito BIT)")
    cursor.execute("CREATE TABLE lista_favoritos (id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_agregada DATE)")


cursor.commit()
=======
>>>>>>> Stashed changes
archivo = open("song.csv", "r", encoding= "UTF-8")
i = 0
for linea in archivo:
    if i < 4:
        print(linea)
        i+=1
<<<<<<< Updated upstream
=======
>>>>>>> d3c245220071c3451d535774fb4dd95cfe6e2bb4
>>>>>>> Stashed changes
cursor.close()
coneccion.close()   