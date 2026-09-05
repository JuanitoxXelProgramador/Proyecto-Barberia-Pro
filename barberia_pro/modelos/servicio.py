from datetime import timedelta

class Servicio:
    _contador_id = 0

    def __init__(self, nombre: str, precio: float, duracion: timedelta, descripcion: str = "", estado: bool = True):
         #validando parametros 
        self._validar_parametros(nombre,precio,duracion,descripcion,estado)
        #aumentar el contador cada vez aque se cree una nueva instancia
        Servicio._contador_id += 1

        # Asignamos el ID único a esta instancia
        self._id = Servicio._contador_id
        self.nombre = nombre
        self.precio = precio
        self.duracion = duracion
        self.descripcion = descripcion

        #validando fecha
        self.estado = estado

    # --- Properties y setters ---
    @property
    def id(self):
        return self.id
    
    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def estado(self):
        return self._estado

    @property
    def duracion_timedelta(self):
        return self._duracion

    def _validar_parametros(self,nombre: str,precio: float,duracion: timedelta,descripcion: str = "", estado: bool = True):
        validaciones = [
            (nombre, str, "Nombre"),
            (precio, float, "Apellido"),
            (duracion, timedelta, "Documento"),
            (descripcion, str, "Teléfono"),
            (estado, bool, "Estado"),
        ]

        for parametro, instancia, etiqueta in validaciones:
            if parametro is None:
                raise ValueError(f"El parámetro '{etiqueta}' no puede estar vacío.")
            if not isinstance(parametro, instancia):
                raise TypeError(
                    f"El parámetro '{etiqueta}' debe ser de tipo {instancia.__name__}."
                )

        self._validar_duracion(duracion)
        self._validar_precio(precio)

    def _validar_duracion(self,duracion: timedelta):
        if duracion < timedelta(minutes=15):
            raise ValueError(f"La duracion es de un minimo de 15 minutos, duracion actual {duracion}")

    def _validar_precio(self,precio: float):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
    #Metodos especiales

    def __str__(self):
        return f"ID: {self.id}\nNombre: {self.nombre}\nPrecio: {self.precio}\nDuracion: {self.duracion}\nDescripcion: {self.descripcion}\nEstado: {self.estado}"