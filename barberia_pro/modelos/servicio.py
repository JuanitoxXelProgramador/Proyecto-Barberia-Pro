from datetime import timedelta

class Servicio:
    _contador_id = 0

    def __init__(self, nombre: str, precio: float, duracion: timedelta, descripcion: str = "", estado: bool = True):
        self._validar_parametros(nombre, precio, duracion, descripcion, estado)
        Servicio._contador_id += 1

        self._id = Servicio._contador_id
        self._nombre = nombre
        self._precio = precio
        self._duracion = duracion
        self._descripcion = descripcion
        self._estado = estado

    @staticmethod
    def validar_lista_servicios(lista_servicios: list['Servicio']) -> None:
        if not lista_servicios:
            raise ValueError("La cita debe contener al menos un servicio.")
    
        for servicio in lista_servicios:
            if not isinstance(servicio, Servicio):
                raise TypeError("El servicio debe ser obligatoriamente de tipo Servicio.")
            
        ids_servicios = [s.id for s in lista_servicios]
        if len(ids_servicios) != len(set(ids_servicios)):
            raise ValueError("La cita no puede tener servicios duplicados.")
        
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio(self) -> float:
        return self._precio

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def estado(self) -> bool:
        return self._estado

    @property
    def duracion_timedelta(self) -> timedelta:
        return self._duracion

    def _validar_parametros(self, nombre: str, precio: float, duracion: timedelta, descripcion: str, estado: bool): 
        validaciones = [
            (nombre, str, "Nombre"),
            (precio, (int, float), "Precio"),
            (duracion, timedelta, "Duracion"),
            (descripcion, str, "Descripcion"),
            (estado, bool, "Estado"),
        ]

        for parametro, instancia, etiqueta in validaciones:
            if parametro is None:
                raise ValueError(f"El parámetro '{etiqueta}' no puede estar vacío.")
            if not isinstance(parametro, instancia):
                nombre_tipo = (
                    "/".join([t.__name__ for t in instancia]) 
                    if isinstance(instancia, tuple) 
                    else instancia.__name__
                )
                raise TypeError(f"El parámetro '{etiqueta}' debe ser de tipo {nombre_tipo}.")

        self._validar_duracion(duracion)
        self._validar_precio(precio)

    def _validar_duracion(self, duracion: timedelta):
        if duracion < timedelta(minutes=15):
            raise ValueError(f"La duración mínima es de 15 minutos, duración actual: {duracion}")

    def _validar_precio(self, precio: float):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

    def __str__(self) -> str:
        return f"ID: {self.id} | Servicio: {self.nombre} | Precio: ${self.precio} | Duración: {self.duracion_timedelta}"