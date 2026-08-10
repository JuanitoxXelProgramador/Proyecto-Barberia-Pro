from datetime import timedelta

class Servicio:
    _contador_id = 0

    def __init__(self, nombre: str, precio: float, duracion: int, descripcion: str = "", estado: bool = True):
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
    def duracion_timedelta(self):
         return timedelta(minutes=self.duracion)

    def _validar_parametros(self, **kwargs):
            for nombre, valor in kwargs.items():
                if valor is None:
                    raise ValueError(f"El parámetro '{nombre}' no puede estar vacío.")

    #Metodos especiales

    def __str__(self):
        return f"ID: {self.id}\nNombre: {self.nombre}\nPrecio: {self.precio}\nDuracion: {self.duracion}\nDescripcion: {self.descripcion}\nEstado: {self.estado}"