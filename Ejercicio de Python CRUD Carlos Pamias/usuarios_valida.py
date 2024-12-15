from datetime import datetime


# Hacemos las validaciones de entrada de los datos

def obtener_estudiante():
    # Solicita al usuario que ingrese si es estudiante (si/no).
    input_usuario = input("¿El usuario es estudiante?(si/no): ").strip().lower()
    
    valores_true = ["s","si", "1"]
    valores_false = ["n","no", "0"]
    
    # Validar y convertir el input
    if input_usuario in valores_true:
        return True
    elif input_usuario in valores_false:
        return False
    else:
        return False        

def obtener_edad():
    while True:
        try:
            numero = int(input("Introduce la edad del usuario: "))
            # Valida que la edad esté entre 16 y 72 años.
            if numero >= 16 and numero <= 72:
                return numero
            else:
                print(f'La edad introducida: {numero} es incorrecta.')
            
        except ValueError:
            print(f'La edad introducida: {numero} es incorrecta.')

def obtener_altura():
    while True:
        try:
            numero = float(input("Introduce la altura del usuario: "))
            if numero >= 1.5 and numero <= 2.5:
                return numero
            else:
                print(f'La altura introducida: {numero} es incorrecta.')
        except ValueError:
            print(f'La altura introducida: {numero} es incorrecta.')

def obtener_fecha_cumpleaños():
    dia_correcto = False
    mes_correcto = False
    año_correcto = False 
    while True:
        try:
            while True:
                dia = int(input("Introduce el dia del cumpleaños del usuario: "))
                if dia >= 1 and dia <= 31:
                    dia_correcto = True
                    break
                else:
                    print(f'El dia introducido: {dia} es incorrecto.')
            
            while True:
                mes = int(input("Introduce el mes del cumpleaños del usuario: "))
                if mes >= 1 and mes <= 12:
                    mes_correcto = True
                    break
                else:
                    print(f'El mes introducido: {mes} es incorrecto.')
            
            while True:
                año = int(input("Introduce el año del cumpleaños del usuario: "))
                fecha_actual = datetime.now()
                año_actual = fecha_actual.year
                año_validacion = año_actual - año
                if año_validacion >= 16 and año_validacion <= 72:
                    año_correcto = True
                    break
                else:
                    print(f'El año introducido: {año} es incorrecto.')
        except ValueError:
            print(f'El dato introducido es incorrecto.')
        if dia_correcto and mes_correcto and año_correcto:
            fecha = datetime(año, mes, dia)
            return fecha.strftime('%Y-%m-%d') 
        

