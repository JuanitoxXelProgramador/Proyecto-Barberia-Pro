from datetime import datetime
from modelos.cliente import Cliente
from modelos.barbero import Barbero
from modelos.servicio import Servicio
from modelos.sucursal import Sucursal
from modelos.estado_cita import EstadoCita

class Cita:
    id_contador = 0

    def __init__(self,cliente: Cliente,barbero:Barbero,servicio:Servicio,fecha: datetime,sucursal: Sucursal ,estado: EstadoCita = EstadoCita.PENDIENTE):

        # 1. Validar parámetros que no esten vacios y de tipo correcto
        self._validar_parametros_instancias(cliente, barbero, servicio, sucursal)

        #validando fecha
        self.fecha = fecha

        #aumentamos el contador en cita y asignamos al id de cada objeto
        Cita.id_contador += 1
        self._id = Cita.id_contador

        #asignando atributos
        self._cliente = cliente
        self._barbero = barbero
        self._servicio = servicio
        self._sucursal = sucursal

        # Asignación usando el Setter validado
        self.estado = estado

    def _validar_parametros_instancias(self, cliente, barbero, servicio,sucursal):
        # Lista de tuplas: (valor_recibido, tipo_esperado, "nombre_del_parametro")
        validaciones = [
            (cliente, Cliente, "cliente"),
            (barbero, Barbero, "barbero"),
            (servicio, Servicio, "servicio"),
            (sucursal, Sucursal, "sucursal")

        ]
        
        for valor, tipo_esperado, nombre in validaciones:
            if valor is None:
                raise ValueError(f"El parámetro '{nombre}' no puede estar vacío.")
            if not isinstance(valor, tipo_esperado):
                raise TypeError(f"El parámetro '{nombre}' debe ser de tipo {tipo_esperado.__name__}.")
            
            
    #falta hacer el resto de getters y setters 
    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def barbero(self) -> Barbero:
        return self._barbero

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def sucursal(self) -> Sucursal:
        return self._sucursal

    @property
    def id(self) -> int:
        return self._id
    #uso de getter y setter de estado
    @property 
    def estado(self) -> EstadoCita:
        return self._estado
    
    #validando que sea instancia de la clase EstadoCIta
    @estado.setter
    def estado(self,nuevo_estado: EstadoCita):
        if not isinstance(nuevo_estado,EstadoCita):
            raise TypeError(f"El estado debe ser una instancia de EstadoCita, no {type(nuevo_estado).__name__}.")
        self._estado = nuevo_estado

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self,nueva_fecha):
        # Aquí ejecutamos la validación antes de guardar en la variable privada _fecha
        self._validar_fecha(nueva_fecha)
        self._fecha = nueva_fecha

    def _validar_fecha(self, fecha):
        if not isinstance(fecha, datetime):
            raise TypeError(f"La fecha debe ser una instancia Datetime, no {type(fecha).__name__}.")
        if  datetime.now() > fecha:
            raise ValueError("La fecha no es valida")

    #Metodos especiales

    def __str__(self):
        return f"Cita #{self._id} [{self.estado.value.upper()}]\nCliente: {self.cliente}\nBarbero: {self.barbero}\nServicio: {self.servicio}\nFecha: {self.fecha}\nSucursal: {self.sucursal}"

        
