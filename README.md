# Implementación segura de protocolos basados en criptografía de clave pública para organización Teletón.

Hoy en día, es cada vez más evidente que las actividades que lleva a cabo cada individuo o una organización involucran la intervención de elementos relacionados con Seguridad Informática y Criptografía buscando contramedidas que no afecten el desempeño del algoritmo criptográfico utilizado, manteniendo así un protocolo criptográfico eficiente y seguro. El objetivo principal del código presentado es implementar protocolos de criptografía de clave pública para proteger ambientes que requieren rápido intercambio y almacenamiento de información. En el presente repositorio se presentará a la organización socio-formadora Teletón una implementación de firmado digital para documentos a través de algoritmos de criptografía de clave pública implementado en Jupyter Notebooks (Python 3.3).

## Archivos en el repositorio
En el repositorio se cuenta con los siguientes archivos y carpetas que son escenciales para la corrida exitosa y total comprensión del código.
### *firma.ipynb*
Archivo que contiene el código completo.

### *Contraseña admin.csv*
Base de datos con el número de identificación del administrador y su contraseña.

### *Admin.csv*
Base de datos con el número de identificación del administrador, su nombre, clave prública, su puesto y contraseña.

### *Contraseña usuarios.csv*
Base de datos con el número de identificación de los usuarios, sus nombres y contraseñas.

### *Usuarios y claves publicas.csv*
Base de datos que contiene la siguiente información de todos los usuarios: ID, Nombre, Clave Pública, Puesto y la columna "Vigente" explica si el usuario es válido o no conteniendo un 1 en caso de serlo y, de lo contrario, un 0.

### *Carpeta "Admins"*
Contiene los certificados que se generan para las firmas de los administradores.

### *Carpeta "Pruebas firma"*
Contiene los siguientes docuemtos (archivos de texto): los certificados de cada uno de los usuarios, los documentos que ya han sido firmados y las firmas unificadas

## **Librerías**

## **Funciones del código**

### *generarCertificado*
Esta función, recibe como parámetros las variables *usuario* (la persona que se registra), *ruta* (directorio de donde se registrará el certificado) y *psw* (contraseña del usuario). Lo primero que sucede dentro de esta función es que se genera la clave privada utilizando el algoritmo de firmado ed25519, después se encripta la llave privada con la contraseña otorgada y por último se crea un archivo con la llave privada encriptada, en este caso le llamaremos certificado, este archivo se guardará en la ruta otorgada con el nombre del usuario como un archivo de texto.

### *cargarPrivateKey*
Esta función recibe como parámetros las variables *ruta* (directorio del certificado que contiene la clave privada encriptada) y *psw* (contraseña con la que la clave privada fue encriptada previamente). Esta función primeramente abre y lee el archivo que contiene el certificado posteriormente desencripta la clave privada con ayuda de la contraseña y finalmente devuelve la clave privada almacenándola en la variable *private_key*.

### *hashea*
Esta función recibe como parámetros la variable *ruta* (directorio donde se localiza el documento a firmar). La función abre el archivo y, con ayuda del algoritmo Hash 256, lee y actualiza el valor del string de hash en bloques de 4K. Por último devuelve el hash en formato hexadecimal.

### *hashea_clavepub

Esta función recibe como parámetro la variable *clave_pub* (clave pública en bytes) . Utilizando la librería hashlib, se pasa la variable *clave_pub* por la función *hashlib.sha256* para convertirla en un hash y por último devolverla en formato hexadecimal. 

### *firmar

Esta función recibe como parámetros las variables *rutas* (directorios de los documentos a firmar), *directorio_firma* (directorio de la carpeta donde está ubicado el certificado) y *ruta_certificado* (directorio del certificado del usuario que firmará). El primer paso es pedir la contraseña para desencriptar la clave privada del certificado, esta se convierte a bytes y se compara con las que se encuentran en el directorio del certificado del usuario que firmará, si la contraseña es incorrecta después de tres intentos se niega el acceso. Seguido de esto se obtiene la clave pública en función de la privada, se serializa y se convierte en un objeto tipo bytes. Por último se crea una lista de rutas de los documentos, se hashea la ruta, se firma en bytes y se crea un archivo que contiene el documento firmado y la clave pública en bytes.

### *registro

Esta función recibe como parámetros las variables *ruta_df* (directorio del csv con los datos de los usuarios o de los administradores), *ruta_df_contrasena* (directorio del csv con las contraseñas de usuario encriptadas), *ruta_carpeta*, *ruta_certificado* (directorio del certificado del usuario que firmará) y *tipo* (tipo de registro) y se utiliza para registrar a un usuario o administrador. En primer lugar se leen los csv con la información de los usuarios y las contraseñas, después se le pide al usuario que ingrese su nombre, su ID que se compara en la base de datos para revisar si  ya había sido registrado y el puesto. A continuación se ingresa la contraseña y se convierte en bytes para después generar el certificado, cargar la clave privada y siguiendo los mismos pasos de la función generar, se genera la clave pública en función de la privada, se serializa y se convierte en un objeto tipo bytes. El último paso es poner el registro como usuario o administrador y actualizar los directorios del csv.

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
