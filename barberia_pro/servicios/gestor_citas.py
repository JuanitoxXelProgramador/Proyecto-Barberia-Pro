from datetime import datetime, timedelta
from modelos.cliente import Cliente
from modelos.barbero import Barbero
from modelos.servicio import Servicio
from modelos.sucursal import Sucursal
from modelos.cita import Cita
from modelos.estado_cita import EstadoCita
from modelos.asignacion_barbero import AsignacionBarbero

class GestorCitas:

    def __init__(self):
        self._citas: dict[int, Cita] = {}

    def crear_cita(self, cliente: Cliente, lista_servicios: list[Servicio], barbero: Barbero, fecha: datetime, sucursal: Sucursal) -> Cita:
        # 1. Validar parámetros de entrada e integridad de servicios
        self._validar_parametros(cliente, lista_servicios, barbero, fecha, sucursal) 
        self._validar_servicios_activos(lista_servicios)

        # Validar que la cita sea a futuro (opcionalmente con un margen mínimo, ej. 15 min)
        if fecha < datetime.now():
            raise ValueError("No se pueden programar citas en fechas u horas pasadas.")
        
        # 2. Comprobar que el barbero esté activo
        if not barbero.esta_activo:
            raise ValueError(f"El barbero {barbero.nombre} no se encuentra activo.")

        
        #comprobar si barbero tiene alguna asignacion activa en fecha
        asignacion = barbero.obtener_asignacion_en_fecha(fecha.date())

        if asignacion is None:
            raise ValueError(f"El barbero {barbero.nombre} no tiene asignación vigente en la fecha {fecha.date()}.")
        # 3. Asignación vigente en la sucursal

        # Comparación directa de objetos Sucursal (o por nombre)
        if asignacion.sucursal != sucursal:
            raise ValueError(f"El barbero {barbero.nombre} no trabaja en la sucursal {sucursal.nombre} en la fecha {fecha.date()}.")

        duracion_cita = Cita.duracion_total(lista_servicios)
        
        # 5. Validar horario comercial de la sucursal (inicio y fin)
        fin_cita = self._obtener_fin_cita(fecha, duracion_cita)
        if fecha.time() < sucursal.hora_apertura or fin_cita.time() > sucursal.hora_cierre:
            raise ValueError("La cita (inicio o fin) está fuera del horario de atención de la sucursal.")

        
        # validar que la fecha y hora de la cita este dentro del horario del barbero en un dia x
        if not self.comprobar_disponibilidad_horario_dia_barbero(fecha,asignacion,duracion_cita):
            raise ValueError("La hora de la cita esta por fuera del horario del barbero")
        
        # 6. Validar solapamiento con citas existentes
        if self._hay_conflicto_horario(barbero, fecha, duracion_cita):
            raise ValueError("Lastimosamente ese horario ya se encuentra ocupado.")
        
        # 4. Validar si el barbero puede realizar los servicios (rápido en memoria)
        if not self.barbero_puede_realizar_servicios(barbero, lista_servicios):
            raise ValueError(f"El barbero {barbero.nombre} no realiza uno o más de los servicios solicitados.")
        

        # 7. Creación de la cita
        cita = Cita(cliente=cliente, barbero=barbero, lista_servicios=lista_servicios, fecha=fecha, sucursal=sucursal) 
        self._citas[cita.id] = cita
        return cita

    # def comprobar_disponibilidad_horario_dia_barbero(self, fecha: datetime, asignacion: AsignacionBarbero, duracion: timedelta) -> bool:
    #     fin_cita = self._obtener_fin_cita(fecha, duracion)
        
    #     if asignacion.horario.dia_sin_periodos(asignacion.horario.obtener_dia_semana(fecha)):
    #         raise ValueError(f"El barbero {asignacion.barbero.nombre} no trabaja el día de hoy.")
            
    #     return asignacion.horario.esta_disponible_en(fecha, fin_cita)

    def comprobar_disponibilidad_horario_dia_barbero(self,fecha: datetime,asignacion: AsignacionBarbero,duracion: timedelta) -> bool:
        fin_cita = self._obtener_fin_cita(fecha,duracion)
        dia = asignacion.horario.obtener_dia_semana(fecha)

        if asignacion.horario.dia_sin_periodos(dia):
            raise ValueError(f"El barbero {asignacion.barbero.nombre} " f"no trabaja el día {dia.name}.")

        return asignacion.horario.esta_disponible_en(fecha,fin_cita)

    # de momento todos los servicios que el cliente selecciona deben estar dentro de barbero caso contrario no se podra continuar
    def barbero_puede_realizar_servicios(self, barbero: Barbero,lista_servicios: list[Servicio]) -> bool:
        for servicio in lista_servicios:
            if not barbero.puede_realizar_servicio(servicio):
                return False

        return True

    def _validar_servicios_activos(self,lista_servicios: list[Servicio]) -> None:
        for servicio in lista_servicios:
            if not servicio.estado:
                raise ValueError(f"El servicio '{servicio.nombre}' " f"se encuentra inactivo.")
            
    def _obtener_fin_cita(self, fecha_cita: datetime, duracion: timedelta) -> datetime:
        return fecha_cita + duracion

    def _hay_conflicto_horario(self, barbero: Barbero, fecha: datetime, duracion_nueva: timedelta) -> bool:
  
        for cita_existente in self._citas.values():
            if cita_existente.barbero == barbero and cita_existente.estado != EstadoCita.CANCELADA:
                if self._intervalos_superpuestos(cita_existente, fecha, duracion_nueva):
                    return True

        return False

    def _intervalos_superpuestos(self, cita_existente: Cita, fecha_cita_nueva: datetime, duracion_cita_nueva: timedelta) -> bool:
        inicio_existente = cita_existente.fecha
        fin_existente = self._obtener_fin_cita(cita_existente.fecha, cita_existente.duracion_total)

        inicio_nueva = fecha_cita_nueva
        fin_nueva = self._obtener_fin_cita(fecha_cita_nueva, duracion_cita_nueva)

        return inicio_nueva < fin_existente and fin_nueva > inicio_existente

    def _validar_parametros(self, cliente: Cliente, lista_servicios: list[Servicio], barbero: Barbero, fecha: datetime, sucursal: Sucursal):
        validaciones = [
            (cliente, Cliente, "cliente"),
            (lista_servicios, list, "lista de servicios que desea el cliente"),
            (barbero, Barbero, "barbero"),
            (fecha, datetime, "fecha"),
            (sucursal, Sucursal, "sucursal")
        ]

        for parametro, instancia, nombre in validaciones:
            if parametro is None:
                raise ValueError(f"El parámetro '{nombre}' no puede estar vacío.")
            if not isinstance(parametro, instancia):
                raise TypeError(f"El parámetro '{nombre}' debe ser de tipo {instancia.__name__}.")