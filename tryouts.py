import pyodbc

#str_conect = "Driver = {SQL Server}, Server = LAPTOP-QKCFS38M\SQLEXPRESS; Database = Spot-USM; Trusted_Connection = True" #nick
str_conect = "Driver={SQL Server};Server=LAPTOP-334LDJSK\SQLEXPRESS;Database=Spot-USM;Trusted_Connection=True" #mat
coneccion = pyodbc.connect(str_conect)
cursor = coneccion.cursor()

cursor.execute("CREATE TABLE repositorio_musica (id int IDENTITY(1,1) PRIMARY KEY, position int , artist_name VARCHAR(100), song_name VARCHAR(100), days int, top_10 int, peak_position int, peak_position_time VARCHAR(10), peak_streams int, total_streams int)")
cursor.execute("CREATE TABLE reproduccion (id int IDENTITY(1,1) PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_reproduccion DATE, can_reproducciones bigint, favorito bit)")
cursor.execute("CREATE TABLE lista_favoritos (id int IDENTITY(1,1) PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_agregada DATE)")
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
archivo = open("song.csv", "r", encoding= "UTF-8")
i = 0
for linea in archivo:
    if i < 4:
        print(linea)
        i+=1
cursor.close()
coneccion.close()