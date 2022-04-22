from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives import serialization
import hashlib
import datetime
import os
import pandas as pd

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
    ruta_cer=ruta + "\\Certificado_" + str(usuario) +".txt"
    with open(ruta_cer,"wb+") as f: 
        f.write(private_bytes) 
        f.close()
    
    return ruta_cer

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

def firmar(rutas, ruta_certificado, psw):
    psw = bytes(psw, 'utf-8')
    usuario = ruta_certificado.split('_')[-1].split(".")[0]
    directorio_firma=os.path.dirname(os.path.abspath(ruta_certificado))

    private_key = cargarPrivateKey(ruta_certificado, psw)
    
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
        #nombre_archivo_firma = lista_rutas[i].split("\\")[-1].split(".")[0] + "_firma_" + str(usuario)
        nombre_archivo_firma = os.path.basename(doc) + "_firma_" + str(usuario)
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

def registro(ruta_df,ruta_carpeta, tipo, datos_reg):
    df = pd.read_csv(ruta_df)
    
    emp_id, nombre, puesto, psw=datos_reg
    
    psw = bytes(psw, 'utf-8')
    while True:
        ruta_certificado=generarCertificado(nombre, ruta_carpeta,psw)
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
    else:
        df2 = {'ID': emp_id, 'Administrador': nombre, 'Clave Pública': hash_clavepub, 'Puesto': puesto}
        
    df = df.append(df2, ignore_index = True)
    df.to_csv(ruta_df,index = False)
    

    #print(df)
    #print(dfc)

#ruta: del documento
#ruta_firma: directorio de la firma
#ruta_df: directorio del excel
def verifica(ruta, ruta_firma, ruta_df,ruta_df_admn):
    print(ruta_firma)
    ln=[]
    df = pd.read_csv(ruta_df)
    dfa= pd.read_csv(ruta_df_admn)

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
                try:
                    usuario = df['Usuario'][df.index[df['Clave Pública'] == hashea_clavepub(public_bytes)]].tolist()[0]
                    ln.append(usuario)
                except:
                    
                    usuario = dfa['Administrador'][dfa.index[dfa['Clave Pública'] == hashea_clavepub(public_bytes)]].tolist()[0]
                    ln.append(usuario)
            except ValueError:
                return []

    return ln

#rutas: directorios de las firmas que vas a unificar 
#rutaunificada: en dónde se depositará el archivo con las firmas unificadas

def all_same(items):
    return all(x == items[0] for x in items)

def unificar_firmas(rutas, rutaunificada):
    firmas = b""
    lista_rutas = rutas.split("\n")

    nomdocs=[os.path.basename(ruta).split(".")[0] for ruta in lista_rutas]
    print(nomdocs)
    exts=[os.path.basename(ruta).split(".")[-1] for ruta in lista_rutas]
    print(exts)

    if all_same(nomdocs) and all_same(exts) and exts[0]=='txt':
        for i, doc in enumerate(lista_rutas):
            with open(doc, "rb") as f:
                content = f.read()
            firmas = firmas + b"\n\n\n" + content
        firmas = firmas[3:]
        with open(f"{rutaunificada}\{nomdocs[1]}_firmas_unificadas.txt","wb+") as f:
                f.write(firmas)
                f.close()

        return True
    else:
        False

def borrar(ruta_df, ruta_certificado,id_borrar):

    df = pd.read_csv(ruta_df)

    #print(df)
    id_index=df.index[df['ID'] == id_borrar].tolist()[0]
    #print(id_index)
    #df=df.drop(df.index[id_index])
    df.at[id_index,'Vigente'] = 0
    df = df.astype({"ID anterior": str})
    df.at[id_index,'ID anterior'] = str(id_borrar)+'/'+str(datetime.date.today())
    df.at[id_index,'ID'] = None
    df.to_csv(ruta_df,index = False)

    try:
        os.remove(ruta_certificado)
    except:
        print('no existe ese archivo')
    #print(df)
    
    #Borrar entre comillas, marcarlo como no utilizable, conservar la información borrada. Política de retención de documentos.

def cambiarcontraseña(ruta_certificado,psw,psw_new):
    psw = bytes(psw, 'utf-8')
    psw_new = bytes(psw_new, 'utf-8')
    privatekey = cargarPrivateKey(ruta_certificado, psw)
    private_bytes = privatekey.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm= serialization.BestAvailableEncryption(psw_new))
    print(private_bytes)
    with open(ruta_certificado,"wb+") as f:
        f.write(private_bytes)
        f.close()
