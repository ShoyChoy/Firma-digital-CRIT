# Implementación segura de protocolos basados en criptografía de clave pública para organización Teletón.

Hoy en día, es cada vez mas evidente que las actividades que lleva a cabo cada individuo o una organización involucran la intervención de elementos relacionados con Seguridad Informática y Criptografía se busca que tan pronto dichas contramedidas contra potenciales nuevas vulnerabilidades se implementen, tales contramedidas no deberían afectar el desempeño del algoritmo criptográfico, manteniendo así un protocolo criptográfico eficiente y seguro. En el presente repositorio se presentará a la organización socio-formadora Teletón.


### registro(*ruta_df, ruta_carpeta, tipo, datos_reg*)

Utilizada para registrar a un usuario o administrador. En primer lugar se leen los datos necesarios para registrar al usuario . Se genera su certificado y se revisa si el hash de la clave pública no se encuentra ya en la base de datos, si es así se genera un certificado nuevo. Finalmente la base de datos correspondiente (ya sea usuario o administrador) se actualiza.

**Parámetros:** 
- ***ruta_df:*** *str*, directorio del csv con los datos de los usuarios o de los administradores.
- ***ruta_carpeta:*** *str*, directorio de la carpeta donde se desea almacenar el certificado del registro.
- ***tipo*** *bool*, indica si el usuario es un usuario regular o administrador (0: admin, 1: usuario regular).
- ***datos_reg:*** *lst*, lista de datos necesarios necesarios para generar un registro (correo, nombre, puesto y contraseña).
              
