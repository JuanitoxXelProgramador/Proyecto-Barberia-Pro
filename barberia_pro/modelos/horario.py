from barberia_pro.modelos.dias_semana import DiasSemana
from barberia_pro.modelos.periodo_horario import PeriodoHorario
from datetime import time,datetime

class Horario:

    def __init__(self):
        self._periodos = {}

    @property
    def periodos(self):
        return self._periodos

    def esta_disponible_en(self, inicio: datetime, fin: datetime) -> bool:

        if not isinstance(inicio, datetime):
            raise TypeError("El inicio debe ser de tipo datetime.")

        if not isinstance(fin, datetime):
            raise TypeError("El fin debe ser de tipo datetime.")

        if fin <= inicio:
            raise ValueError("La fecha y hora final debe ser posterior a la inicial.")

        # Una cita no puede comenzar un día y terminar otro.
        if inicio.date() != fin.date():
            return False

        dia = self.obtener_dia_semana(inicio)

        periodos = self.obtener_horario_dia(dia)

        return any(p.contiene_intervalo(inicio.time(),fin.time())for p in periodos)

    @staticmethod
    def obtener_dia_semana(fecha: datetime) -> DiasSemana:
        if not isinstance(fecha, datetime):
            raise TypeError("El parámetro debe ser obligatoriamente una fecha de tipo datetime.")

        return DiasSemana(fecha.isoweekday())
    
    def obtener_horario_dia(self,dia: DiasSemana) -> list[PeriodoHorario]:
        if not isinstance(dia, DiasSemana):
            raise ValueError("El parametro dia debe ser obligatoriamente del tipo DiasSemana")
        
        return self._periodos.get(dia, []) # Retorna lista vacía si no hay periodos

    def dia_sin_periodos(self, dia: DiasSemana) -> bool:
        if not isinstance(dia, DiasSemana):
            raise TypeError("El parámetro dia debe ser obligatoriamente del tipo DiasSemana.")

        return len(self.obtener_horario_dia(dia)) == 0

    def agregar_periodo(self,dia: DiasSemana,periodo: PeriodoHorario):
        #validando los parametros
        self._validar_parametros(dia,periodo)
        #formamos la estructura
        if dia not in self.periodos:
            self.periodos[dia] = []

        #validamos primero el solapamiento
        for periodo_existente in self.periodos[dia]:
            if self._hay_solapamiento(periodo_existente,periodo):
                raise ValueError(f"El periodo ingresado se solapa con el actual de {dia.name}")

        #agregamos el dia junto con el parametro
        self.periodos[dia].append(periodo)
        self.periodos[dia].sort(key=lambda p: p.hora_inicio)
        print("periodo agregado con exito")

    def _hay_solapamiento(self, periodo_existente: PeriodoHorario, nuevo_periodo: PeriodoHorario) -> bool:
        return not (
            periodo_existente.hora_fin <= nuevo_periodo.hora_inicio 
            or nuevo_periodo.hora_fin <= periodo_existente.hora_inicio
        )

    def mostrar_horario(self):
        print("\n=== ESQUEMA DE HORARIO ===")

        # 1. Recorremos los 7 días para no saltarnos ninguno
        for dia in DiasSemana:

            # 2. Si el día tiene períodos guardados...
            if dia in self.periodos and len(self.periodos[dia]) > 0:
                
                # Creamos un texto vacío para ir guardando los horarios
                texto_horarios = ""
                
                # Recorremos la lista de períodos de ese día
                for periodo in self.periodos[dia]:
                    # Usamos str(periodo) para llamar a tu __str__ de PeriodoHorario
                    texto_horarios += str(periodo) + "  "

                print(f"• {dia.name}: {texto_horarios}")

            else:
                # 3. Si el día no está en el diccionario o está vacío
                print(f"• {dia.name}: LIBRE")
    # --- VALIDACIONES ---

    def _validar_parametros(self,dia: DiasSemana,periodo: PeriodoHorario):

        validaciones = [
            (dia,DiasSemana,"Dia de la semana"),
            (periodo, PeriodoHorario, "Periodo de tiempo")
        ]

        for parametro, instancia, nombre in validaciones:
            if parametro is None:
                raise ValueError(f"EL parametro {nombre} no puede estar vacio")

            if not isinstance(parametro,instancia):
                raise TypeError(f"El parámetro '{nombre}' debe ser de tipo {instancia.__name__}.")

