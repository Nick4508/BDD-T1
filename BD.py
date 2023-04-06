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
coneccion = pyodbc.connect(str_conect)
cursor = coneccion.cursor()
#cursor.execute("CREATE TABLE reproduccion (id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_reproduccion DATE, can_reproducciones bigint, favorito bit)")
#cursor.execute("CREATE TABLE lista_favoritos (id int PRIMARY KEY, song_name VARCHAR(100), artist_name VARCHAR(100), fecha_agregada DATE)")





def main():
    #cursor.execute("CREATE TABLE repositorio_musica (id int IDENTITY(1,1) PRIMARY KEY, position int, artist_name VARCHAR(100), song_name VARCHAR(100), days int, top_10 int, peak_position bigint, peak_position_time VARCHAR(10), peak_streams bigint, total_streams bigint)")
    
    archivo = open("song.csv", "r", encoding= "UTF-8-sig")
    lineas = archivo.readlines()
    x = 1
    while x < len(lineas):
        lista = []
        for elemento in lineas:
            a = elemento.strip().split(";")
            for i in a:
                lista.append("'"+i+"'")
        print(lista,"\n")
        x+=1


    # for x in range(len(lineas)):
    #     a,b,c,d,e,f,g,h,i = tuple(lineas[x].strip().split(";"))
    #     # cursor.execute("INSERT INTO repositorio_musica (position,artist_name,song_name,days,top_10,peak_position,peak_time,peak_streams,total_streams) values ("+a+","+b+","+c+","+d+","+e+","+f+","+g+","+h+","+i+")")
    #     print(lineas[x])
    #     exit()
    
    
    cursor.commit()
    cursor.close()
    coneccion.close()
if __name__ == "__main__":
    main()