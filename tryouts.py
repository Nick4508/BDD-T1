import pyodbc


coneccion_nick = "Driver = {SQL Server}, Server = LAPTOP-QKCFS38M\SQLEXPRESS; Database = Spot-USM; Trusted_Connection = True"
coneccion = pyodbc.connect(coneccion_nick)
cursor = coneccion.cursor()

cursor.execute("CREATE TABLE repositorio_musica ( id int IDENTITY(1,1) PRIMARY KEY, position int , artist_name VARCHAR(100), song_name VARCHAR(100), days int, top_10 int, peak_position int, peak_position_time VARCHAR(10), peak_streams int, total_streams int)")
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

cursor.close()
coneccion.close()