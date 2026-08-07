class Cliente:
    """
    Representa un cliente registrado en Barbería Pro.
    """ 
    def __init__(self,nombre, apellido, correo, password, telefono, foto_perfil = None):
        self._nombre = None 
        self._apellido = None
        self._correo = None
        self._password = None
        self._telefono = None
        self._foto_perfil = None

        if nombre.strip() == "" or apellido.strip() == "":
            raise ValueError("El nombre o apellido son obligatorios")

        if correo.strip() == "" or password.strip() == "":
            raise ValueError("El correo y la contraseña son obligatorios.")
    
        # 2. ASIGNACIÓN (Solo llegamos aquí si ninguna validación de arriba lanzó un error)
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.password = password
        self.telefono = telefono
        self.foto_perfil = foto_perfil


    #propiedades de cliente
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self,nuevo_nombre):
        nuevo_nombre = nuevo_nombre.strip()
        if not nuevo_nombre.replace(" ", "").isalpha():
            raise ValueError("El nombre solo puede contener letras y espacios.")

        self._nombre = nuevo_nombre
        
    @property 
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, nuevo_apellido):
        if not nuevo_apellido.replace(" ","").isalpha():
            raise ValueError("EL apelluido solo puede llevar letras y espacios")

        self._apellido = nuevo_apellido

    @property 
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self,nuevo_correo):
        #validamos el correo
        if not self._validar_correo(nuevo_correo):
            raise ValueError("El correo es invalido")
        
        self._correo = nuevo_correo

    #aun es solo de prueba
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, nueva_contraseña):
        if len(nueva_contraseña.strip()) < 8:
            raise ValueError("La contraseña debe tener minimo 8 caracteres ")

        self._password = nueva_contraseña
        

    #funciones espeficas

    def _validar_correo(self,email):
    # 1. Verifica que tenga una sola arroba
        if email.count("@") != 1:
            return False

        usuario, dominio = email.split("@")

        # 2. Verifica que haya texto antes de la arroba
        if len(usuario) == 0:
            return False

        # 3. Verifica que haya un punto en el dominio
        if "." not in dominio:
            return False

        dominio_nombre, extension = dominio.rsplit(".", 1)

        # 4. Verifica que el dominio y la extensión tengan texto
        if len(dominio_nombre) == 0 or len(extension) == 0:
            return False

        return True

    def __str__(self):
        return f"Nombre: {self.nombre}\nApellido: {self.apellido}\nCorreo: {self.correo}"

# c1 = Cliente("juan","bargas","holasoyjuan@gmail.com", "equisde432", 3188775972)
# print(c1)



