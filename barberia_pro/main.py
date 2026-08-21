from datetime import time, timedelta
from modelos.dias_semana import DiasSemana
from modelos.periodo_horario import PeriodoHorario
from modelos.horario import Horario
from modelos.sucursal import Sucursal


def probar_sucursal():
    print("=== INICIANDO PRUEBAS DE SUCURSAL Y HORARIOS ===\n")

    # 1. Crear la sucursal (Apertura: 8:00 AM, Cierre: 8:00 PM)
    # Min. por período: 1 hora, Min. descanso: 30 minutos
    sucursal_centro = Sucursal(
        nombre="Sucursal Centro",
        direccion="Calle 5 # 4-12",
        telefono="3001234567",
        hora_apertura=time(8, 0),
        hora_cierre=time(20, 0),
        duracion_minima_periodo=timedelta(hours=1),
        descanso_minimo=timedelta(minutes=30),
    )

    print(f"Sucursal creada: {sucursal_centro.nombre}")
    print(f"Horario de atención: {sucursal_centro.hora_apertura} - {sucursal_centro.hora_cierre}")
    print(f"Descanso mínimo requerido: {sucursal_centro.descanso_minimo}\n")

    # -------------------------------------------------------------
    # CASO 1: Horario totalmente válido
    # -------------------------------------------------------------
    print("--- Prueba 1: Horario Válido ---")
    h_valido = Horario()
    p1 = PeriodoHorario(time(8, 0), time(12, 0))   # Mañana (4 hrs)
    p2 = PeriodoHorario(time(13, 0), time(18, 0))  # Tarde (5 hrs) - Descanso de 1 hora (12:00 a 13:00)

    h_valido.agregar_periodo(DiasSemana.LUNES, p1)
    h_valido.agregar_periodo(DiasSemana.LUNES, p2)

    try:
        if sucursal_centro._validar_horario_operativo(h_valido):
            print("✅ Prueba 1 SUPERADA: El horario cumple con todas las reglas operativas.\n")
    except ValueError as e:
        print(f"❌ Prueba 1 FALLÓ: {e}\n")

    # -------------------------------------------------------------
    # CASO 2: Error por exceder el horario de cierre de la sucursal
    # -------------------------------------------------------------
    print("--- Prueba 2: Período Fuera de Límites ---")
    h_invalido_limite = Horario()
    p_tardio = PeriodoHorario(time(15, 0), time(21, 0)) # Cierra a las 21:00 (Sucursal cierra a las 20:00)

    h_invalido_limite.agregar_periodo(DiasSemana.MARTES, p_tardio)

    try:
        sucursal_centro._validar_horario_operativo(h_invalido_limite)
        print("❌ Prueba 2 FALLÓ: No se detectó que el período excede el horario de cierre.\n")
    except ValueError as e:
        print(f"✅ Prueba 2 SUPERADA (Error capturado correctamente):\n   --> {e}\n")

    # -------------------------------------------------------------
    # CASO 3: Error por descanso insuficiente entre turnos
    # -------------------------------------------------------------
    print("--- Prueba 3: Descanso Insuficiente ---")
    h_invalido_descanso = Horario()
    p_manana = PeriodoHorario(time(8, 0), time(12, 0))
    p_corto = PeriodoHorario(time(12, 15), time(16, 0)) # Descanso de solo 15 min (Mínimo es 30 min)

    h_invalido_descanso.agregar_periodo(DiasSemana.MIERCOLES, p_manana)
    h_invalido_descanso.agregar_periodo(DiasSemana.MIERCOLES, p_corto)

    try:
        sucursal_centro._validar_horario_operativo(h_invalido_descanso)
        print("❌ Prueba 3 FALLÓ: No se detectó la falta de descanso suficiente.\n")
    except ValueError as e:
        print(f"✅ Prueba 3 SUPERADA (Error capturado correctamente):\n   --> {e}\n")


if __name__ == "__main__":
    probar_sucursal()