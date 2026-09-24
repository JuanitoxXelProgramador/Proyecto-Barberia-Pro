import string

class Cliente:
    """
    Representa un cliente registrado en Barbería Pro.
    """ 
    def __init__(self,nombre: str, apellido: str, correo: str, password: str, telefono: str, foto_perfil: "str"):

        self._validar_parametros(nombre, apellido, correo, password, telefono, foto_perfil)
    
        # 2. ASIGNACIÓN (Solo llegamos aquí si ninguna validación de arriba lanzó un error)
        self._nombre = nombre
        self._apellido = apellido
        self._correo = correo
        self._password = password
        self._telefono = telefono
        self._foto_perfil = foto_perfil

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
        self._validar_contrasena(nueva_contraseña)
        self._password = nueva_contraseña
        

    # --- Validaciones ---
    def _validar_parametros(self,nombre: str, apellido: str, correo: str, password: str, telefono: str, foto_perfil: "str"):
        validaciones = [(nombre,str,"Nombre del cliente"),
                        (apellido, str,"Apellido del cliente"),
                        (correo, str,"Correo del cliente"),
                        (password,str,"Contrasena del cliente"),
                        (telefono,str,"Telefono del cliete"),
                        (foto_perfil,str,"Foto de perfil")]

        for parametro,instancia,etiqueta in validaciones:
            if not parametro:
                raise ValueError(f"El parametro {etiqueta} no puede estar vacio")

            if not isinstance(parametro,instancia):
                raise ValueError(f"EL parametro {etiqueta} no es del tipo correcto {instancia.__name__}")

        self._validar_correo(correo)
        self._validar_contrasena(password)

        
    def _validar_contrasena(self, password: str):
        password = password.strip()
        #validar longitud
        if len(password) < 8:
            raise ValueError(f"La contrasena debe contener al menos 8 caracteres")
        #validar letra mayuscula
        if not any(letra.isupper() for letra in password):
            raise ValueError(f"La contrasena debe contener almenos una mayuscula")
        #validar caracter especial
        if not any(letra in string.punctuation for letra in password):
            raise ValueError(f"La contrasena debe contener almenos un caracter especial")
        #validar numero 
        if not any(letra.isdigit() for letra in password):
            raise ValueError(f"La contrasena debe contener almenos un numero")

    def _validar_correo(self,email: str) :
    # 1. Verifica que tenga una sola arroba
        if email.count("@") != 1:
            raise ValueError(f"El correo {email} debe tener solo una arrova")

        usuario, dominio = email.split("@")

        # 2. Verifica que haya texto antes de la arroba
        if len(usuario) == 0:
            raise ValueError(f"El correo {email} no tiene nombre de email")

        # 3. Verifica que haya un punto en el dominio
        if "." not in dominio:
            raise ValueError(f"El correo {email} no tiene un punto en su dominio")

        dominio_nombre, extension = dominio.rsplit(".", 1)

        # 4. Verifica que el dominio y la extensión tengan texto
        if len(dominio_nombre) == 0 or len(extension) == 0:
            raise ValueError(f"El correo {email} debe tener su dominio y correo con nombre y dominio correcto")


    def __str__(self):
        return f"Nombre: {self.nombre}\nApellido: {self.apellido}\nCorreo: {self.correo}"
