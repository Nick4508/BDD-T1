Nombre                  Rol                 Rut             Paralelo
Nicolas Rodriguez      202173515-1       20793631-6            201
Matias Barrera         202173539-9       21213159-8            201

Consideraciones:
    - Antes de establecer la conexion se pide haber creado la base de datos "Spot-USM", y poner los datos
    necesarios en el string de conexion para poder conectarse.
    - Se tomaron en cuenta la mayoria de casos bordes pero si llega en algún momento ocurrir un error
    que se salga del codigo por ejemplo "ValueError" no guardará los datos en la base de datos porque 
    el commit está al final del todo.
    - Al momento de interactuar con la mayoria de los puntos pedidos siempre se pedirá introducir el id
    de la canción con la que se quiere interactuar, siempre se tomará como correcto el id introducido
    incluso cuando se equivoque, solo que guardará la cancion correspondiente al Id introducido.
    - La mayoria de interacciones con el menú dado, están resguardadas tal y como se pidió en las especificaciones
    de la tarea.
    - Se creo una View y una Funcion SQL que fueron utilizadas en los puntos 8 y 5 respectivamente.
