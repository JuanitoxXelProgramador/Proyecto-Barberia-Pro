from datetime import datetime,timedelta
from modelos.cliente import Cliente
from modelos.barbero import Barbero
from modelos.servicio import Servicio
from modelos.sucursal import Sucursal
from modelos.cita import Cita
from modelos.estado_cita import EstadoCita

class GestorCitas:

    def __init__(self):
        self._citas = {}

    #     GestorCitas
    # │
    # ├── ¿Ya existe esta cita?
    # ├── ¿El barbero está disponible?
    # ├── ¿El horario entra en las reglas?
    # └── ¿Puedo registrarla?

    def crear_cita(self, cliente:Cliente,servicio: Servicio, barbero: Barbero, fecha: datetime, sucursal: Sucursal):
        # 1. Validar que los datos permitan crear una cita.
        self._validar_parametros(cliente,servicio,barbero,fecha, sucursal) 
        #validar si hay disponibilidad
        if self._hay_conflicto_horario(barbero,fecha,servicio):
            raise ValueError("Lastimosamente ese horario ya se encuentra ocupado")
        # 2. Crear el objeto Cita.
        cita = Cita(
            cliente=cliente,
            barbero=barbero,
            servicio=servicio,
            fecha=fecha,
            sucursal=sucursal
            ) 
        # 3. Guardarlo en el diccionario.
        self._citas[cita.id] = cita
        # 4. Retornar la cita creada.

        return cita
    
    def _obtener_fin_cita(self,fecha_cita, servicio_cita):
        return fecha_cita + servicio_cita

    def _hay_conflicto_horario(self, barbero,fecha,servicio):
        #recorremos las citas agregadas
        for cita_existente in self._citas.values():

            if barbero == cita_existente.barbero:
                #comprobamos los intervalos
                if self._intervalos_superpuestos(cita_existente,fecha,servicio):
                    return True

        return False

    # --- METODOS DISPONIBLIDIDAD ---

    def _intervalos_superpuestos(self,cita_existente,fecha_cita_nueva,servicio_cita_nueva):
        #obtenemos el intervalo de la cita en iteracion
        inicio_existente = cita_existente.fecha
        fin_existente = self._obtener_fin_cita(cita_existente.fecha,cita_existente.servicio.duracion_timedelta)

        #obtenemos el intervalo de la cita nueva
        inicio_nueva = fecha_cita_nueva
        fin_nueva = self._obtener_fin_cita(fecha_cita_nueva, servicio_cita_nueva.duracion_timedelta)

        #si se cumple estan superpuestos
        return (inicio_nueva < fin_existente and fin_nueva > inicio_existente)

    # --- PROPERTIES AND SETTERS ---

    # --- MÉTODOS PRIVADOS DE VALIDACIÓN ---
    def _validar_parametros(self,cliente,servicio, barbero, fecha, sucursal):
        # Lista de tuplas: (valor_recibido, tipo_esperado, "nombre_del_parametro")
        validaciones = [
            (cliente, Cliente, "cliente"),
            (servicio, Servicio, "servicio"),
            (barbero, Barbero, "barbero"),
            (fecha,datetime,"fecha"),
            (sucursal, Sucursal, "sucursal")

        ]

        for parametro, instacia, nombre in validaciones:
            if parametro is None:
                raise ValueError(f"El parámetro '{nombre}' no puede estar vacío.")
            if not isinstance(parametro, instacia):
                raise TypeError(f"El parámetro '{nombre}' debe ser de tipo {instacia.__name__}.")
        
#     Agregar ID automático a Cita.
# Implementar crear_cita() en GestorCitas.
# Guardar las citas en un diccionario usando su ID.
# Seguir evaluando el Validador común, pero todavía no extraerlo apresuradamente.

