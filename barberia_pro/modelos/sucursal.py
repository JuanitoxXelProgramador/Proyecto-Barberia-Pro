from datetime import time,timedelta,datetime,date
from modelos.horario import Horario
from modelos.dias_semana import DiasSemana
from modelos.periodo_horario import PeriodoHorario

class Sucursal:

    def __init__(self,nombre: str, direccion: str, telefono: str, hora_apertura: time, hora_cierre: time, duracion_minima_periodo: timedelta, descanso_minimo: timedelta,max_periodos_diarios: int):
        #asignando parametros informativos de la surcursal
        self._nombre = nombre
        self._direccion = direccion
        self._telefono = telefono
        #validamos parametros
        self._validar_parametros(hora_apertura, hora_cierre, duracion_minima_periodo, descanso_minimo,max_periodos_diarios)
        # Asignamos atributos validados
        self._hora_apertura = hora_apertura
        self._hora_cierre = hora_cierre
        self._duracion_minima_periodo = duracion_minima_periodo
        self._descanso_minimo = descanso_minimo
        self._periodos_diarios = max_periodos_diarios


    def _validar_horario_operativo(self, horario: Horario) -> bool:
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

    def _validar_parametros(self, apertura: time, cierre: time, duracion_minima: timedelta, descanso_minimo: timedelta, periodos_diarios: int):

        #creamos las validaciones
        validaciones = [
            (apertura,time,f"Hora de apertura de la sucursal {self.nombre}"),
            (cierre,time,f"Hora de cierre de la sucursal {self.nombre}"),
            (duracion_minima, timedelta, f"Duracion minima de cada periodo en la sucursal {self.nombre}"),
            (descanso_minimo, timedelta, f"Duracion minima del descanso entre cada periodo en la sucursal {self.nombre}"),
            (periodos_diarios, int, f"EL maximo numero de periodos por cada dia en el horario de la sucursal {self.nombre}")
        ]

        #recorreomos las validaciones
        for parametro, instancia, nombre in validaciones:
            if parametro is None:
                raise ValueError(f"EL parametro {nombre} no puede estar vacio")

            if not isinstance(parametro,instancia):
                raise TypeError(f"El parámetro '{nombre}' debe ser de tipo {instancia.__name__}.")


        if apertura >= cierre:
            raise ValueError("La hora de apertura de la sucursal debe der extricamente menor a la de cierre")

        if periodos_diarios <= 0:
            raise ValueError("El numero maximo de periodos diarios debe ser un valor positivo y mayor a cero")

