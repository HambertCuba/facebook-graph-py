from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError

 

directorio_credenciales = 'D:\\REQUERIMIENTOS\\2020-2021\\RONALD MEGO\\Documentacion Api Face\\Project\\facebook-graph-py\\credentials_module.json'

 


# INICIAR SESION
def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

 

    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

 

    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

 


def crear_archivo_texto(nombre_archivo, contenido, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'title': nombre_archivo, \
                                       'parents': [{"kind": "drive#fileLink", \
                                                    "id": id_folder}]})
    archivo.SetContentString(contenido)
    archivo.Upload()
    
    
def subir_archivo(ruta_archivo, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink", \
                                                    "id": id_folder}]})
    archivo['title'] = ruta_archivo.split("\\")[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()    