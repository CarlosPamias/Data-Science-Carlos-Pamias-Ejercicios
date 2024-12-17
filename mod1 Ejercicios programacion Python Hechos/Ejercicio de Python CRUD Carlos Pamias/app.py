import usuarios_crud as crud

menu = """
Te damos la bienvenida a la App de usuarios, estas son las opciones:
          1 - Ver todos los usuarios
          2 - Ver todos los usuarios ordenados por edad
          3 - Ver un usuarios por código
          4 - Crear nuevo usuario
          5 - Actualizar usuario existente
          6 - Borrar un usuario por código
          7 - Borrar todos los usuarios
          8 - Salir
          9 - Generar Usuarios
          
          """
crud.cargar_archivo_csv()

while True:
    try:
        option = int(input(menu))
    except ValueError:
        print("Opción incorrecta")
    match option:
        case 1:
            crud.ver_todos_usuarios()
        case 2:
            crud.ver_todos_usuarios_ordenados_por_edad()
        case 3:
            nohay, identificador = crud.ver_usuario_por_Id('consulta')
            if nohay:
                print(f'No se ha encuntrado ningun usuario con esta identificación: {identificador}')
        case 4:
            crud.crear_usuario()
        case 5:
            crud.actualizar_usuario()
        case 6:
            nohay, identificador = crud.ver_usuario_por_Id('borrar')
            if nohay:
                print(f'No se ha encuntrado ningun usuario con esta identificación: {identificador}')
        case 7:
            crud.borrar_usuarios()
        case 8:
            print("Hasta pronto.")
            crud.generar_archivo_csv()
            break
        case 9:
            crud.generar_datos_prueba()
        case _:
            print("Opción incorrecta")

