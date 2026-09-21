from datetime import datetime, timedelta
from modelos.cliente import Cliente
from modelos.barbero import Barbero
from modelos.servicio import Servicio
from modelos.sucursal import Sucursal
from modelos.estado_cita import EstadoCita

class Cita:
    id_contador = 0

    def __init__(self, cliente: Cliente, barbero: Barbero, lista_servicios: list[Servicio], fecha: datetime, sucursal: Sucursal, estado: EstadoCita = EstadoCita.PENDIENTE):
        self._validar_parametros_instancias(cliente, barbero, lista_servicios, sucursal)
        Servicio.validar_lista_servicios(lista_servicios)

        self.fecha = fecha
        
        Cita.id_contador += 1
        self._id = Cita.id_contador

        self._cliente = cliente
        self._barbero = barbero
        self._lista_servicios = list(lista_servicios)
        self._sucursal = sucursal
        self._estado = estado
        self._duracion_total_servicios = Cita.duracion_total(lista_servicios)

    @property
    def duracion_total(self) -> timedelta:
        return self._duracion_total_servicios

    @staticmethod
    def duracion_total(lista_servicios: list[Servicio]) -> timedelta:
        """Calcula la duración total de la cita sumando sus servicios."""
        return sum((s.duracion_timedelta for s in lista_servicios), timedelta())

    @property
    def lista_servicios(self) -> list[Servicio]:
        """Devuelve una copia defensiva de la lista de servicios."""
        return list(self._lista_servicios)

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def barbero(self) -> Barbero:
        return self._barbero

    @property
    def sucursal(self) -> Sucursal:
        return self._sucursal

    @property
    def id(self) -> int:
        return self._id

    @property 
    def estado(self) -> EstadoCita:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: EstadoCita):
        if not isinstance(nuevo_estado, EstadoCita):
            raise TypeError(f"El estado debe ser una instancia de EstadoCita, no {type(nuevo_estado).__name__}.")
        self._estado = nuevo_estado

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @fecha.setter
    def fecha(self, nueva_fecha: datetime):
        self._validar_fecha(nueva_fecha)
        self._fecha = nueva_fecha

    def _validar_fecha(self, fecha: datetime):
        if not isinstance(fecha, datetime):
            raise TypeError(f"La fecha debe ser una instancia de datetime, no {type(fecha).__name__}.")
        if fecha < datetime.now():
            raise ValueError("La fecha de la cita no puede ser en el pasado.")

    def _validar_parametros_instancias(self, cliente: Cliente, barbero: Barbero, lista_servicios: list[Servicio], sucursal: Sucursal) -> None:
        validaciones = [
            (cliente, Cliente, "cliente"),
            (barbero, Barbero, "barbero"),
            (lista_servicios, list, "lista de servicio"),
            (sucursal, Sucursal, "sucursal")
        ]
        
        for valor, tipo_esperado, nombre in validaciones:
            if valor is None:
                raise ValueError(f"El parámetro '{nombre}' no puede estar vacío.")
            if not isinstance(valor, tipo_esperado):
                raise TypeError(f"El parámetro '{nombre}' debe ser de tipo {tipo_esperado.__name__}.")

    def __str__(self) -> str:
        nombres_servicios = ", ".join([s.nombre for s in self._lista_servicios])
        return (
            f"Cita #{self._id} [{self.estado.value.upper()}]\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Barbero: {self.barbero.nombre}\n"
            f"Servicios: {nombres_servicios}\n"
            f"Duracion: {self._duracion_total_servicios}\n" 
            f"Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M')}\n"
            f"Sucursal: {self.sucursal.nombre}"
        )