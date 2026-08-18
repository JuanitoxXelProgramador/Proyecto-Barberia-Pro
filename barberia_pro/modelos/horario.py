from periodo_horario import PeriodoHorario
from dias_semana import DiasSemana
from datetime import time

class Horario:

    def __init__(self):
        self.periodos = {}

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

p1 = PeriodoHorario(time(8,0),time(12,0))
p2 = PeriodoHorario(time(12,1),time(18,0))
p3 = PeriodoHorario(time(13,0),time(18,0))
p4 = PeriodoHorario(time(15,0),time(19,0))
p5 = PeriodoHorario(time(1,0),time(7,0))
p6 = PeriodoHorario(time(11,0),time(18,0))
p7 = PeriodoHorario(time(22,0),time(23,0))

h1 = Horario()
h1.agregar_periodo(DiasSemana.LUNES, p1)
h1.agregar_periodo(DiasSemana.LUNES, p2)
h1.agregar_periodo(DiasSemana.LUNES,p7)
# h1.agregar_periodo(DiasSemana.MARTES, p3)
# h1.agregar_periodo(DiasSemana.MIERCOLES, p4)
# h1.agregar_periodo(DiasSemana.JUEVES, p5)
# h1.agregar_periodo(DiasSemana.VIERNES, p6)
# h1.agregar_periodo(DiasSemana.SABADO, p7)

h1.mostrar_horario()