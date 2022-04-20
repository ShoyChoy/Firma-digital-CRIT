from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives import serialization
import hashlib

#usuario: quien se registra
#ruta: directorio de donde se depositará el certificado
#psw: contraseña del usuario


def generarCertificado(usuario,ruta,psw): 
    #Genera la llave privada utilizando ed25519 como algoritmo de firmado
    private_key = ed25519.Ed25519PrivateKey.generate()
    #Encripta la llave privada utilizando la contraseña
    private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm= serialization.BestAvailableEncryption(psw)) 
    #Se crea un archivo con la llave privada encriptada (Certificado)
    with open(ruta + "\\Certificado_" + str(usuario) +".txt","wb+") as f: 
        f.write(private_bytes) 
        f.close()

#ruta: directorio del certificado que contiene la clave privada encriptada
#psw: contraseña con la que se encriptó la clave privada

def cargarPrivateKey(ruta, psw):
    #Abre el certificado y desencripta la llave privada utilizando la contraseña
    with open(ruta,"rb") as f:
        pk =f.read()
    private_key = serialization.load_pem_private_key(pk, psw)
    return private_key

#Devuelve la clave privada

#ruta: directorio del documento a firmar

def hashea(ruta):
    filename = ruta
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

#Devuelve el hash en formato hexadecimal

#función que haseha la clave pública.
#clave_pub: clave pública en bytes.

def hashea_clavepub(clave_pub):
    sha256_hash = hashlib.sha256(clave_pub)
    return sha256_hash.hexdigest()

#Devuelve el hash en formato hexadecimal

#rutas: directorios de los documentos a firmar
#directorio_firma: directorio de la carpeta donde está ubicado el certificado
#ruta_certificado: directorio del certificado del usuario que firmará

def firmar(rutas, directorio_firma, ruta_certificado):
    
    usuario = ruta_certificado.split('_')[-1].split(".")[0]
    #Contador de intentos
    i = 0
    #Petición de contraseña para desencriptar la clave privada del certificado, con límite de 3 intentos como máximo
    while True:
        try:
            psw = bytes(input("Ingrese su contraseña: "), 'utf-8')
            private_key = cargarPrivateKey(ruta_certificado, psw)
        except ValueError:
            print("Contraseña incorrecta")
            i += 1
            if i == 3:
                return "Se excedió el número de intentos máximo"
            continue
        else:
            break
    
    #Obtención de clave pública en función de la privada.
    public_key = private_key.public_key()
    #Conversión de la clave pública a un objeto tipo bytes.
    public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw)
    
    #Crea lista de las rutas de documentos
    lista_rutas = rutas.split("\n")
    #Itera sobre cada ruta de documento
    for i, doc in enumerate(lista_rutas):
        #Hashea la ruta
        hasheo = hashea(doc)
        #Firma el haseho en bytes
        signature = private_key.sign(bytes(hasheo, 'utf-8'))
        #Crea un archivo que contiene el documento firmado y después de 3 tabs la clave pública en bytes.
        nombre_archivo_firma = lista_rutas[i].split("\\")[-1].split(".")[0] + "_firma_" + str(usuario)
        with open(directorio_firma + "\\" + nombre_archivo_firma + ".txt","wb+") as f:
            f.write(signature)
            f.write(b"\t\t\t")
            f.write(public_bytes)
            f.close()

#ruta_df: directorio del csv con los datos de los usuarios o de los administradores
#ruta_df_contrasena: directorio del csv 
#ruta_carpeta: 
#ruta_certificado:
#tipo:

def registro(ruta_df,ruta_df_contrasena,ruta_carpeta, ruta_certificado, tipo):
    df = pd.read_csv(ruta_df)
    dfc = pd.read_csv(ruta_df_contrasena)
    
    nombre = input('Nombre: ')
   
    while True:
        emp_id = int(input('ID: '))
        if emp_id in df['ID']:
            print('Usuario ya registrado')
        else: 
            break
    puesto = input('Puesto: ')
    
    
    psw = bytes(input("Ingrese su contraseña: "), 'utf-8')
    while True:
        generarCertificado(nombre, ruta_carpeta,psw)
        private_key = cargarPrivateKey(ruta_certificado, psw)
        public_key = private_key.public_key()
        public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw)
        hash_clavepub = hashea_clavepub(public_bytes)
        if hash_clavepub in df['Clave Pública']:
            continue
        else:
            break
    
    if tipo == 1:
        df2 = {'ID': emp_id, 'Usuario': nombre, 'Clave Pública': hash_clavepub, 'Puesto': puesto, 
               'Vigente' : 1}
        dfcontra = {'ID': emp_id, 'Usuario': nombre, 'Contraseña': psw, 'Tipo de Usuario':tipo}
        
    else:
        df2 = {'ID': emp_id, 'Administrador': nombre, 'Clave Pública': hash_clavepub, 'Puesto': puesto}
        dfcontra = {'ID': emp_id, 'Usuario': nombre, 'Contraseña': psw, 'Tipo de Usuario':0}
        
    df = df.append(df2, ignore_index = True)
    df.to_csv(ruta_df,index = False)
    
    dfc = dfc.append(dfcontra, ignore_index = True)
    dfc.to_csv(ruta_df_contrasena, index =  False)
    #print(df)
    #print(dfc)

#ruta: del documento
#ruta_firma: directorio de la firma
#ruta_df: directorio del excel
def verifica(ruta, ruta_firma, ruta_df):
    df = pd.read_csv(ruta_df)
    with open(ruta_firma,"rb") as f:
        contents = f.read().split(b"\n\n\n")
        hasheo = hashea(ruta)
        for i, content in enumerate(contents):
            content = content.split(b"\t\t\t")
            #separa la firma de los bytes de la clave pública
            firma = content[0]
            public_bytes = content[1]
            hash_public = hashlib.sha256(public_bytes)
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes) 
            df = df[df['Vigente']==1]
            try:
                public_key.verify(firma, bytes(hasheo, 'utf-8'))
                usuario = df['Usuario'][df.index[df['Clave Pública'] == hashea_clavepub(public_bytes)]].tolist()[0]
                print("Firma de " + usuario + " válida")
            except ValueError:
                print("Firma invalida")

#rutas: directorios de las firmas que vas a unificar 
#rutaunificada: en dónde se depositará el archivo con las firmas unificadas
def unificar_firmas(rutas, rutaunificada):
    firmas = b""
    lista_rutas = rutas.split("\n")
    for i, doc in enumerate(lista_rutas):
        with open(doc, "rb") as f:
            content = f.read()
        firmas = firmas + b"\n\n\n" + content
    firmas = firmas[3:]
    with open(rutaunificada + "\Firmas_unificadas.txt","wb+") as f:
            f.write(firmas)
            f.close()

def borrar(ruta_df, ruta_certificado,):
    while True:
        try:
            psw = bytes(input("Ingrese su contraseña: "), 'utf-8')
            private_key = cargarPrivateKey(ruta_certificado, psw)
        except ValueError:
            print("Contraseña incorrecta")
            continue
        else:
            break
    id_borrar = int(input('Ingrese el ID del usuario a eliminar: '))
    df = pd.read_csv(ruta_df)
    #print(df)
    id_index=df.index[df['ID'] == id_borrar].tolist()[0]
    #print(id_index)
    #df=df.drop(df.index[id_index])
    df.at[id_index,'Vigente'] = 0
    df.to_csv(ruta_df,index = False)
    print(df)
    
    #Borrar entre comillas, marcarlo como no utilizable, conservar la información borrada. Política de retención de documentos.

def cambiarcontraseña(ruta_certificado,ruta_contra, emp_id):
    i = 0
    while True:
        try:
            psw = bytes(input("Ingrese la contraseña actual: "), 'utf-8')
            privatekey = cargarPrivateKey(ruta_certificado, psw)
        except ValueError:
            print("Contraseña incorrecta")
            i+=1
            if i ==3:
                return "Se excedió el número de intentos máximo"
            continue
        else:
            break
    
    psw_new = bytes(input("Ingrese contraseña nueva:"), 'utf-8')
    privatekey = cargarPrivateKey(ruta_certificado, psw)
    private_bytes = privatekey.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm= serialization.BestAvailableEncryption(psw_new))
    print(private_bytes)
    with open(ruta_certificado,"wb+") as f:
        f.write(private_bytes)
        f.close()
    df = pd.read_csv(ruta_contra)
    id_index=df.index[df['ID'] == emp_id].tolist()[0]
    df.at[id_index,'Contraseña'] = psw_new
    df.to_csv(ruta_contra,index = False)
    print(df)