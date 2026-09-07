from datetime import time,timedelta,datetime
from modelos.horario import Horario
from modelos.barbero import Barbero
from modelos.asignacion_barbero import AsignacionBarbero

class Sucursal:

    def __init__(self,nombre: str, direccion: str, telefono: str, hora_apertura: time, hora_cierre: time, duracion_minima_periodo: timedelta, descanso_minimo: timedelta,max_periodos_diarios: int):
        #asignando parametros informativos de la surcursal
        self._nombre = nombre
        self._direccion = direccion
        self._telefono = telefono
        #validamos parametros
        self._validar_parametros(nombre,hora_apertura, hora_cierre, duracion_minima_periodo, descanso_minimo,max_periodos_diarios)
        # Asignamos atributos validados
        self._hora_apertura = hora_apertura
        self._hora_cierre = hora_cierre
        self._duracion_minima_periodo = duracion_minima_periodo
        self._descanso_minimo = descanso_minimo
        self._periodos_diarios = max_periodos_diarios
        #almacenador de objetos barberos cambiarlo por lista de asignaciones
        self._asignaciones: list[AsignacionBarbero] = []


    def vincular_asignacion(self,asignacion: AsignacionBarbero) -> None:
        if not isinstance(asignacion,AsignacionBarbero):
            raise TypeError("El parámetro debe ser un objeto de tipo AsignacionBarbero.")

        if asignacion.sucursal != self:
            raise ValueError(f"EL barbero {asignacion.barbero.nombre} no esta asignado a esta sucursal {self.nombre}")

        #validamos el horario con nuestro metodo (ya validamos en GestorAsignaciones)
        # if not self.validar_horario_operativo(asignacion.horario):
        #     raise ValueError(f"El horario operativo asignado a {asignacion.barbero.nombre}" 
        #                      f"no cumple con las reglas establecidas por la sucursal {self.nombre}")

        self._asignaciones.append(asignacion)


    # Devolvera una lista con las asignaciones historicas
    def obtener_historico_asignaciones_por_barbero(self, id_barbero: int) -> list[AsignacionBarbero]:
        if not isinstance(id_barbero,int):
            raise TypeError("La id del barbero que desea buscar no es del tipo correcto (int)")

        if id_barbero <= 0:
            raise ValueError("La id del barbero que esta buscando no es valida")

        lista: list[AsignacionBarbero] = []
        #navegando en las lista de asignaciones
        for asignacion in self._asignaciones:
            if asignacion.barbero.id == id_barbero:
                lista.append(asignacion)

        if not lista:
            raise ValueError(f"No se encontro ninguna asignacion historica para el id {id_barbero}.")
        
        return lista

    # Devuelve la asignación (el contrato solo el primero e unico que este activo)
    def buscar_asignacion_activa_por_barbero(self, id_barbero: int) -> AsignacionBarbero:
        if not isinstance(id_barbero,int):
            raise TypeError("La id del barbero que desea buscar no es del tipo correcto (int)")

        if id_barbero <= 0:
            raise ValueError("La id del barbero que esta buscando no es valida")

        #navegando en las lista de asignaciones
        for asignacion in self._asignaciones:
            if asignacion.barbero.id == id_barbero:
                #comprobamos que este vigente
                if asignacion.esta_activa():
                    return asignacion

        raise ValueError(f"No se encontro la asignacion de barbero para el id en cuestion {id_barbero}")

    # 2. Devuelve solo al Barbero navegando a través de la asignación
    def buscar_barbero(self, id_barbero: int) -> Barbero:
        asignacion = self.buscar_asignacion_por_barbero(id_barbero)
        return asignacion.barbero

    def buscar_asignacion(self,id: int) -> Barbero:
        #comprovamos si existen barberos
        self.existen_barberos()

        for barbero in self._barberos: 
            if barbero.id == id:
                return barbero

        raise ValueError(f"El id barbero {id} no existe dentro de Sucursal {self.nombre}")

    def existen_barberos(self):
        if not self._barberos:
            raise ValueError(f"No hay barberos regitrados en la Sucursal {self.nombre}")
    
    def eliminar_barbero(self,id: int) -> Barbero: 
        #en caso de que ixista el barbero lo alamcenamos en otro caso pues tira el raise
        barbero = self.buscar_barbero(id)
        #eliminamos barbero
        self._barberos.remove(barbero)
        
    def listar_barberos(self) -> str:
        """Retorna una representación formateada en texto de los barberos asignados a la sucursal."""
        if not self._barberos:
            return f"La sucursal '{self.nombre}' no tiene barberos asignados."

        lineas = [f"Barberos asignados a la sucursal '{self.nombre}':"]
        for barbero in self._barberos:
            lineas.append(
                f"  - [ID: {barbero.id}] {barbero.nombre} {barbero.apellido} "
                f"| Doc: {barbero.documento} "
                f"| Estado: {barbero.estado.name}"
            )

        return "\n".join(lineas)
    
    def validar_horario_operativo(self, horario: Horario) -> bool:
        """Valida que todos los períodos de un horario respeten la apertura,
        cierre y tiempos de descanso de la sucursal.
        """
        for dia, lista_periodos in horario.periodos.items():
            if not lista_periodos:
                continue

            if len(lista_periodos) > self.periodos_diarios:
                raise ValueError(f"El numero de periodos del dia {dia.name} excede"
                                f"al numero de periodos ('{self.periodos_diarios}') maximo definidos en {self.nombre}")
            
            # 1. Validar apertura, cierre y duración mínima de cada período
            for periodo in lista_periodos:
                if periodo.hora_inicio < self.hora_apertura:
                    raise ValueError(
                        f"El inicio del período {periodo} el día {dia.name} está por "
                        f"debajo de la hora de apertura ({self.hora_apertura}) en {self.nombre}."
                    )

                if periodo.hora_fin > self.hora_cierre:
                    raise ValueError(
                        f"El cierre del período {periodo} el día {dia.name} excede "
                        f"la hora de cierre ({self.hora_cierre}) en {self.nombre}."
                    )

                if periodo.duracion() < self.duracion_minima_periodo:
                    raise ValueError(
                        f"El período {periodo} el día {dia.name} no cumple la duración "
                        f"mínima requerida ({self.duracion_minima_periodo})."
                    )

            # 2. Validar descanso entre períodos consecutivamente (una sola vez por día)
            if not self.validar_descanso_minimo(lista_periodos):
                raise ValueError(
                    f"El día {dia.name} no cumple con el descanso mínimo de "
                    f"{self.descanso_minimo} entre períodos."
                )

        return True

    def validar_descanso_minimo(self, lista_periodos: list) -> bool:
        """Comprueba que el tiempo libre entre bloques consecutivos respete el mínimo."""
        for i in range(len(lista_periodos) - 1):
            descanso = self._duracion_entre_periodos(
                lista_periodos[i], lista_periodos[i + 1]
            )

            if descanso < self._descanso_minimo:
                return False  # Se encontró un descanso inválido, corta y retorna False
        return True

    def _duracion_entre_periodos(self, p1, p2) -> timedelta:
        """Calcula el tiempo de descanso entre el fin del primer período y el inicio del segundo."""
        fecha_base = datetime.min
        dt1 = datetime.combine(fecha_base, p1.hora_fin)
        dt2 = datetime.combine(fecha_base, p2.hora_inicio)
        return dt2 - dt1

# --- PROPERTIES Y GETTERS ---
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def hora_apertura(self) -> time:
        return self._hora_apertura

    @property
    def hora_cierre(self) -> time:
        return self._hora_cierre

    @property
    def duracion_minima_periodo(self) -> timedelta:
        return self._duracion_minima_periodo

    @property
    def descanso_minimo(self) -> timedelta:
        return self._descanso_minimo

    @property
    def periodos_diarios(self) -> int:
        return self._periodos_diarios
    
    # --- VALIDAR PARAMETROS --- 

    def _validar_parametros(self, nombre, apertura: time, cierre: time, duracion_minima: timedelta, descanso_minimo: timedelta, periodos_diarios: int):

        #creamos las validaciones
        validaciones = [
            (apertura,time,f"Hora de apertura de la sucursal {nombre}"),
            (cierre,time,f"Hora de cierre de la sucursal {nombre}"),
            (duracion_minima, timedelta, f"Duracion minima de cada periodo en la sucursal {nombre}"),
            (descanso_minimo, timedelta, f"Duracion minima del descanso entre cada periodo en la sucursal {nombre}"),
            (periodos_diarios, int, f"EL maximo numero de periodos por cada dia en el horario de la sucursal {nombre}")
        ]

        #recorreomos las validaciones
        for parametro, instancia, etiqueta in validaciones:
            if parametro is None:
                raise ValueError(f"EL parametro {etiqueta} no puede estar vacio")

            if not isinstance(parametro,instancia):
                raise TypeError(f"El parámetro '{etiqueta}' debe ser de tipo {instancia.__name__}.")

        if apertura >= cierre:
            raise ValueError("La hora de apertura de la sucursal debe der extricamente menor a la de cierre")

        if periodos_diarios <= 0:
            raise ValueError("El numero maximo de periodos diarios debe ser un valor positivo y mayor a cero")

