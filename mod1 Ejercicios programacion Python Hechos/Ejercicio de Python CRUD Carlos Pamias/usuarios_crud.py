from usuario import Usuario
import usuarios_valida as val
import random 
from datetime import datetime, timedelta
import csv
import os

usuarios = []


menu_modificacion = """
Indique que información de usuario desdea modificar:
          1 - Nombre de usuario.
          2 - Email usuario
          3 - Edad usuario
          4 - Altura usuario
          5 - Estado estudiante
          6 - Fecha de cumpleaños
          7 - Salir y actualizar
        
          """

def obtener_id_nuevo_usuario():
    maximo = 0
    for usuario in usuarios:
        if usuario.id_usuario >= maximo:
            maximo = usuario.id_usuario
    return maximo

# Funciones principales
def generar_datos_prueba():
    nombres = ["Ana", "Luis", "Maria", "Carlos", "Marta", "Javier", "Sofia", "Pedro", "Laura", "Alberto"]
    for i in range(10):
        nombre = nombres[i]
        email = f"{nombre.lower()}@gmail.com"
        edad = random.randint(18, 60)
        altura = round(random.uniform(1.5, 2.0), 2)
        estudiante = random.choice([True, False])
        fecha = datetime.now() - timedelta(days=random.randint(18*365, 60*365))
        cumpleaños = fecha.strftime('%Y-%m-%d')
        nuevo_usuario = Usuario(id_usuario=i+1, nombre=nombre, email=email, edad=edad, altura=altura, estudiante=estudiante, cumpleaños=cumpleaños)
        usuarios.append(nuevo_usuario)
    
def ver_todos_usuarios():
    if not usuarios: 
        print("No hay usuarios disponibles.")
        return
        
    for usuario in usuarios:
        print(usuario)
        
    print("")
def ver_todos_usuarios_ordenados_por_edad():
    while True:
        tipo = input('Pulse a(ascendente) o d(descendente): ').lower()
        if tipo == "a":
            ver_todos_usuarios_ordenados_por_edad_ascd()
            return
        elif tipo == "d":
            ver_todos_usuarios_ordenados_por_edad_desc()
            return
    
def ver_todos_usuarios_ordenados_por_edad_desc():
    usuarios_ordenado_por_edad = sorted(usuarios, key=lambda u: u.edad, reverse=True) # desc
    for usuario in usuarios_ordenado_por_edad:
        print(usuario)
        
def ver_todos_usuarios_ordenados_por_edad_ascd():
    usuarios_ordenado_por_edad = sorted(usuarios, key=lambda u: u.edad) # Asc
    for usuario in usuarios_ordenado_por_edad:
        print(usuario)
        
def ver_usuario_por_Id(tipo):
    try:
        identificador = int(input(f"Introduce el código del usuario {'para borrar' if tipo == 'borrar' else ''}: "))
    except ValueError:
        print("Identificador no válido.")
        return True, identificador

    for usuario in usuarios:
        if identificador == usuario.id_usuario:
            if tipo == 'consulta':
                print(usuario)
            elif tipo == 'borrar':
                usuarios.remove(usuario)
                print(f"Usuario con Código {identificador} eliminado.")
            return False, identificador

    return True, identificador

def crear_usuario():
    id_usuario = obtener_id_nuevo_usuario() 
    nombre = input("Introduce el nombre del usuario: ")
    premail = input("Introduce el código para el email: ")
    email = f"{premail.lower()}@gmail.com"
    edad = val.obtener_edad()
    altura = val.obtener_altura()
    estudiante = val.obtener_estudiante()
    cumpleaños = val.obtener_fecha_cumpleaños()
    nuevo_usuario = Usuario(id_usuario=id_usuario + 1, nombre=nombre, email=email, edad=edad, altura=altura, estudiante=estudiante, cumpleaños=cumpleaños)
    usuarios.append(nuevo_usuario)
        
def actualizar_usuario():
    
    nohay, identificador = ver_usuario_por_Id('Modificacion')
    if nohay:
        print(f'No se ha encuntrado ningun usuario con esta identificación: {identificador}')
        return
    
    # cariables para saner qu cambios se han hecho      
    caso1 = False
    caso2 = False
    caso3 = False
    caso4 = False
    caso5 = False
    caso6 = False
    nuevo_nombre = nuevo_email = nueva_edad = nueva_altura = nuevo_estudiante = nuevo_cumpleaños = None

    while True:
        try:
           option = int(input(menu_modificacion))
        except ValueError:
            print("Opción incorrecta")
        
        match option:
            case 1:
                nuevo_nombre = input("Introduce el nombre del usuario: ")
                caso1 = True
            case 2:
                premail = input("Introduce el código para el email: ")
                nuevo_email = f"{premail.lower()}@gmail.com"
                caso2 = True
            case 3:
                nueva_edad = val.obtener_edad()
                caso3 = True
            case 4:
                nueva_altura = val.obtener_altura()
                caso4 = True
            case 5:
                nuevo_estudiante = val.obtener_estudiante()
                caso5 = True
            case 6:
                nuevo_cumpleaños = val.obtener_fecha_cumpleaños()
                caso6 = True
            case 7:
                for usuario in usuarios:
                    if usuario.id_usuario == identificador:
                        if caso1:
                           usuario.nombre = nuevo_nombre
                        if caso2:
                           usuario.email = nuevo_email
                        if caso3:
                           usuario.edad = nueva_edad
                        if caso4:
                           usuario.altura = nueva_altura
                        if caso5:
                           usuario.estudiante = nuevo_estudiante
                        if caso6:
                           usuario.cumpleaños = nuevo_cumpleaños
                        
                print(f'El usuario {identificador} se ha modificado correctamente')
                break
            case _:
                print("Opción incorrecta")
   
def borrar_usuarios():
    print("Borrando lista de usuarios")
    usuarios.clear()
    print("Usuarios eliminados correctamente.")

def leer_csv():
    pass


def generar_archivo_csv():
    import os

    print("Directorio actual de trabajo:", os.getcwd())

    with open('usuarios.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for usuario in usuarios:
            writer.writerow([usuario.id_usuario, usuario.nombre, usuario.email, usuario.edad, usuario.altura, usuario.estudiante, usuario.cumpleaños])

def cargar_lista_usuarios(reader):

    for row in reader:
        id_usuario, nombre, email, edad, altura, estudiante, cumpleaños = row
        nuevo_usuario = Usuario(
            id_usuario=int(id_usuario),
            nombre=nombre,
            email=email,
            edad=int(edad),
            altura=float(altura),
            estudiante=estudiante,
            cumpleaños=cumpleaños
        )
        usuarios.append(nuevo_usuario)
    

def cargar_archivo_csv():
    try:
        print("Directorio actual de trabajo:", os.getcwd())
        with open('usuarios.csv', 'r') as file:
            reader = csv.reader(file)
            cargar_lista_usuarios(reader)
    except FileNotFoundError:
        print("El archivo 'usuarios.csv' no se encontró. Se crea un archivo vacio.")
        with open('usuarios.csv', 'w') as file:
            pass
            
