# Implementación segura de protocolos basados en criptografía de clave pública para organización Teletón.

Hoy en día, es cada vez más evidente que las actividades que lleva a cabo cada individuo o una organización involucran la intervención de elementos relacionados con Seguridad Informática y Criptografía buscando contramedidas que no afecten el desempeño del algoritmo criptográfico utilizado, manteniendo así un protocolo criptográfico eficiente y seguro. El objetivo principal del código presentado es implementar protocolos de criptografía de clave pública para proteger ambientes que requieren rápido intercambio y almacenamiento de información. En el presente repositorio se presentará a la organización socio-formadora Teletón una implementación de firmado digital para documentos a través de algoritmos de criptografía de clave pública implementado en Jupyter Notebooks (Python 3.3).

## Archivos en el repositorio

## **Librerías**

## **Funciones del código**

### *generarCertificado*
Esta función, recibe como parámetros las variables *usuario* (la persona que se registra), *ruta* (directorio de donde se registrará el certificado) y *psw* (contraseña del usuario). Lo primero que sucede dentro de esta función es que se genera la clave privada utilizando el algoritmo de firmado ed25519, después se encripta la llave privada con la contraseña otorgada y por último se crea un archivo con la llave privada encriptada, en este caso le llamaremos certificado, este archivo se guardará en la ruta otorgada con el nombre del usuario como un archivo de texto.

### *cargarPrivateKey*
Esta función recibe como parámetros las variables *ruta* (directorio del certificado que contiene la clave privada encriptada) y *psw* (contraseña con la que la clave privada fue encriptada previamente). Esta función primeramente abre y lee el archivo que contiene el certificado posteriormente desencripta la clave privada con ayuda de la contraseña y finalmente devuelve la clave privada almacenándola en la variable *private_key*.

### *hashea*
Esta función recibe como parámetros la variable *ruta* (directorio donde se localiza el documento a firmar). La función abre el archivo y, con ayuda del algoritmo Hash 256, lee y actualiza el valor del string de hash en bloques de 4K. Por último devuelve el hash en formato hexadecimal.

#parte de isa

### *verifica*
Esta función recibe como parámetros *ruta* (dirección de donde se encuentra el documento a verificar), *ruta_firma* (la ruta donde se encuentra el archivo de texto con la firma y *ruta_df*(ruta donde se encuentra la base de datos con las contraseñas de los usuarios). Primero se lee la base de datos y el archivo de la firma y se genera una separación de usuarios con tres intros. Después, ya que la función tiene la firma del documento y los bytes públicos de cada usuario separados, separa la  firma de los public bytes. Luego se genera el hash de la clave pública, para hacer la comparación de la base de datos, genera la clave pública  a través de los bytes y hace un hash del documento que queremos verificar. Teniendo la clave pública, la función verifica que esta sea válida y con el hash de la clave pública verifica que existe un usuario en la base de datos que tenga esa clave pública. Si esto es correcto, la función imprime el nombre del usuario con su clave pública junto con el hecho de que la firma es válida. Por otro lado, hay dos maneras por las cuales la función regresaría que la firma es inválida:
- Que la firma no sea válida si es que quieres verificar con un documento donde no esté esa firma.
- Que no exista ningún usuario con esa clave pública en el dataframe.

### *unificarFirmas*
Esta función recibe los parámetros *rutas* (lista de rutas que se desean unificar) y *rutaunificada* (donde se planea guardar el documento que contenga las firmas unificadas). A través de esta función se busca unificar la firma principal que será utilizada para verificar un documento y todas las firmas a la vez. Al pasarle las rutas de las firmas, la función  regresa un documento llamado "Firmas Unificadas", en el que se encuentra la firma del documento, tres tabulaciones y tres intros, y así sigue la siguiente firma hasta que estén todas las firmas unificadas en el documento.

### *cambiarContraseña*
Esta función recibe como parámetros *ruta_certificado* (dirección donde se encuentra el certificado a utilizar), *ruta_contra* (ruta donde se encuentra la base de datos con las contraseñas de los usuarios) y *emp_id* (el ID del usuario). Primeramente, la función le pide al usuario su contraseña actual y se dirige a la ruta del certificado para extraer la clave privada. En el caso de que la contraseña ingresada sea incorrecta, pedirá que se vuelva a ingresar. Si se llega a exceder el número de intentos al ingresar la contraseña y siempre sea incorrecta, la función te regresa el mensaje: "Se excedió el número de intentos máximo" y se pedirá ingresar una nueva contraseña. Una vez verificado el usuario con la contraseña correcta la función extrae la llave privada y la convierte a bytes. Finalmente, la función regresa el ID del empleado junto con su nueva contraseña y se actualiza la base de datos. 

### *borrar*
Esta función fue generada con el fin de que un administrador pueda eliminar a algún usuario y recibe como parámetros *ruta_df* (el directorio donde está almacenada la base de datos que contiene a todos los usuarios) y *ruta_certificado*. Primeramente pide al administrador su contraseña y en caso de que esta sea incorrecta, vuelve a intentarlo. Luego, pregunta el ID del usuario que se desea eliminar. Una vez obtenido el ID, la función se encarga que en la columna de la base de datos llamada "Vigente" aparezca el número 0 en el ID correspondiente, esto indicando que ya no es un usuario vigente, finalmente se actualiza la base de datos.
