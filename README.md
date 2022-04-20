# Implementación segura de protocolos basados en criptografía de clave pública para organización Teletón.

Hoy en día, es cada vez mas evidente que las actividades que lleva a cabo cada individuo o una organización involucran la intervención de elementos relacionados con Seguridad Informática y Criptografía buscando contramedidas que no afecten el desempeño del algoritmo criptográfico utilizado, manteniendo así un protocolo criptográfico eficiente y seguro. El objetivo principal del código presentado es implementar protocolos de criptografía de clave pública para proteger ambientes que requieren rápido intercambio y almacenamiento de información. En el presente repositorio se presentará a la organización socio-formadora Teletón una implementación de firmado digital para documentos a través de algoritmos de criptografía de clave pública implementado en Jupyter Notebooks (Python 3.3).

## Archivos en el repositorio

## **Librerías**

## **Funciones del código**

### *generarCertificado*
Esta función, recibe como parámetros las variables usuario (la persona que se registra), ruta (directorio de donde se registrará el certificado) y psw (contraseña del usuario). Lo primero que sucede dentro de esta función es que se genera la clave privada utilizando el algoritmo de firmado ed25519, después se encripta la llave privada con la contraseña otorgada y por último se crea un archivo con la llave privada encriptada, en este caso le llamaremos certificado, este archivo se guardará en la ruta otorgada con el nombre del usuario como un archivo de texto.

### *cargarPrivateKey*
