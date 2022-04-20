# Implementación segura de protocolos basados en criptografía de clave pública para organización Teletón.

Hoy en día, es cada vez mas evidente que las actividades que lleva a cabo cada individuo o una organización involucran la intervención de elementos relacionados con Seguridad Informática y Criptografía buscando contramedidas que no afecten el desempeño del algoritmo criptográfico utilizado, manteniendo así un protocolo criptográfico eficiente y seguro. El objetivo principal del código presentado es implementar protocolos de criptografía de clave pública para proteger ambientes que requieren rápido intercambio y almacenamiento de información. En el presente repositorio se presentará a la organización socio-formadora Teletón una implementación de firmado digital para documentos a través de algoritmos de criptografía de clave pública implementado en Jupyter Notebooks (Python 3.3).

## Archivos en el repositorio

## **Librerías**

## **Funciones del código**

### *generarCertificado*
Esta función, recibe como parámetros las variables usuario (la persona que se registra), ruta (directorio de donde se registrará el certificado) y psw (contraseña del usuario). Lo primero que sucede dentro de esta función es que se genera la clave privada utilizando el algoritmo de firmado ed25519, después se encripta la llave privada con la contraseña otorgada y por último se crea un archivo con la llave privada encriptada, en este caso le llamaremos certificado, este archivo se guardará en la ruta otorgada con el nombre del usuario como un archivo de texto.

### *cargarPrivateKey*

Función Cambiar Contraseña
Esta función recibe la ruta del certificado, la ruta de la contraseña y el ID del empleado. Primero la función te pide que
ingreses tu contraseña actual, así, se va a la ruta del certificado para extraer la clave privada de ese empleado. En el caso
de que la contraseña ingresada sea incorrecta, te pedirá que la vuelvas a ingresar. Si pasas el número de intentos al 
ingresar la contraseña y siempre sea correcta, la función te regresa el mensaje: "Se excedió el número de intentos máximo".
Volviendo a lo principal, la función te pedirá ingresar una nueva contraseña. Se extrae la private key y la convierte a bytes. 
Finalmente, la función te regresa el ID del empleado junto con su nueva contraseña.

### *Función Borrar*
Esta función recibe el directorio del dataframe que contiene a todos los usuarios y la ruta del certificado. Después, esta te pedirá
tu contraseña, en caso de que esta sea incorrecta, el programa te pedirá que la vuelvas a ingresar. Luego, te pedirá el ID del usuario
que queremos eliminar del dataframe. La función recorre el directorio con los usuarios para encontrar el usuario a borrar y lo elimina.

### *Función Unificar Firmas*
Esta función recibe las rutas de todas las firmas (directorios) que queremos unificar en una sola firma principal para solo usar
ese archivo para verificar un documento y verificar todas las firmas a la vez. Al pasarle las rutas de las firmas, la función 
regresa un documento llamado "Firmas Unificadas", en el que esta la firma del documento, tres tabs y tres enters, y así sigue 
la siguiente firma hasta que estén todas las firmas unificadas en el documento.

### *Función Verifica*
Esta función recibe la ruta del documento, el directorio de la firma unificada y el directorio del dataframe que contiene a todos
los usuarios. Primero lee el dataframe con los usuarios, lee las firmas y los separa por cada tres enters de la ruta unificada que es 
cada persona. Después, ya que la función tiene la firma del documento y los bytes públicos de cada persona separados, separa la 
firma de los public bytes. Luego genera el hash de la clave pública, para hacer la comparación del dataframe, genera la clave pública 
a través de los bytes y hace un hash del documento que queremos verificar. Teniendo la clave pública, la función verifica que esta sea
válida y con el hash de la clave pública verifica que existe un usuario en el dataframe que tenga esa clave pública. Si esto es correcto,
la función imprime el nombre del usuario con su clave pública junto con el hecho de que la firma es válida. Por otro lado, hay dos maneras 
por las cuales la función regresaría que la firma es invalida:
	- Que la firma no sea valida si es que quieres verificar con un documento donde no este esa firma.
	- Que no exista ningun usuario con esa clave pública en el dataframe.
