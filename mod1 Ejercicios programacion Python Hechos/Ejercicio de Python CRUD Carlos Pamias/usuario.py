class Usuario:
    # atributos de clase, con valores comunes para todos los usuarios
        
    # Método constructor:
    def __init__(self, id_usuario, nombre, email, edad, altura, estudiante, cumpleaños): # atributos de instancia
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.edad = edad
        self.altura = altura
        self.estudiante = estudiante
        self.cumpleaños = cumpleaños
        print("Usuario creado correctamente")
        
    def __str__(self):
        return f'Usuario: Codigo: {self.id_usuario}, Nombre: {self.nombre}, Email: {self.email}, Edad: {self.edad}, Altura: {self.altura}, Es estudiante: {self.estudiante}, Cumpleaños: {self.cumpleaños}.'
   
   