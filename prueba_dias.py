from barberia_pro.modelos.dias_semana import DiasSemana
from barberia_pro.modelos.horario import Horario
from datetime import datetime,time,date
from barberia_pro.modelos.periodo_horario import PeriodoHorario




mi_horario = Horario()

# Creación de franjas de tiempo
p_manana = PeriodoHorario(time(8, 0), time(12, 0))
p_tarde = PeriodoHorario(time(14, 0), time(18, 0))
p_noche = PeriodoHorario(time(18, 30), time(21, 0))

# 1. Agregar periodos desordenados (Lunes se inserta tarde primero, luego mañana)
mi_horario.agregar_periodo(DiasSemana.LUNES, p_tarde)
mi_horario.agregar_periodo(DiasSemana.LUNES, p_manana)
mi_horario.agregar_periodo(DiasSemana.MIERCOLES, p_manana)
mi_horario.agregar_periodo(DiasSemana.VIERNES, p_noche)

# 2. Prueba de duracion()
print(f"\nDuración del turno mañana: {p_manana.duracion()}")

# 3. Mostrar el esquema ordenado
mi_horario.mostrar_horario()

# 4. Prueba de error por solapamiento
print("\n--- PRUEBA DE CONTROL DE ERRORES ---")


ahora = datetime(2026,5,12)
# # Usar isoweekday() (lunes = 1, domingo = 7)
# numero_dia_1_7 = ahora.isoweekday()
# print(f"Número (1-7): {numero_dia_1_7} +  tipo: {type(numero_dia_1_7)}")
# dia = DiasSemana(numero_dia_1_7)
# print(dia)

print(Horario.obtener_dia_semana())
