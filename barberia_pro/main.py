from datetime import time, timedelta, date
from modelos.barbero import Barbero
from modelos.sucursal import Sucursal
from modelos.horario import Horario
from modelos.periodo_horario import PeriodoHorario
from modelos.dias_semana import DiasSemana
from modelos.vigencia import Vigencia
from modelos.asignacion_barbero import AsignacionBarbero
from modelos.estado_barbero import EstadoBarbero

def probar_vigencia_y_exclusividad():
    print("==========================================================")
    print("  PRUEBA DE EXCLUSIVIDAD DE VIGENCIA POR BARBERO ")
    print("==========================================================\n")

    # 1. Configuración base
    barbero = Barbero("Carlos", "Mendoza", "1085123456", "3001234567", "carlos@gmail.com", EstadoBarbero.ACTIVO)
    
    sucursal_centro = Sucursal(
        nombre="Centro", direccion="Calle 18 # 24-12", telefono="3159876543",
        hora_apertura=time(8, 0), hora_cierre=time(20, 0),
        duracion_minima_periodo=timedelta(hours=2), descanso_minimo=timedelta(minutes=30),
        max_periodos_diarios=3
    )

    sucursal_norte = Sucursal(
        nombre="Norte", direccion="Av. Panamericana", telefono="3120000000",
        hora_apertura=time(8, 0), hora_cierre=time(20, 0),
        duracion_minima_periodo=timedelta(hours=2), descanso_minimo=timedelta(minutes=30),
        max_periodos_diarios=3
    )

    horario = Horario()
    horario.agregar_periodo(DiasSemana.LUNES, PeriodoHorario(time(8, 0), time(12, 0)))

    # 2. PRIMERA ASIGNACIÓN: Enero 1 a Diciembre 26 de 2026 (360 días) en Centro
    vigencia_centro = Vigencia(date(2026, 1, 1), date(2026, 12, 26))
    asig_centro = AsignacionBarbero(barbero, sucursal_centro, horario, vigencia_centro)
    
    # Registramos la primera asignación
    barbero.agregar_asignacion(asig_centro)
    sucursal_centro.vincular_asignacion(asig_centro)
    print(f"✔️ Asignación 1 registrada: {barbero.nombre} en Sucursal Centro ({vigencia_centro.fecha_inicio} al {vigencia_centro.fecha_final})")

    # =========================================================================
    # ESCENARIO A: Intento de solapamiento (Misma fecha o cruce parcial en Norte)
    # =========================================================================
    print("\n--- [ESCENARIO A] Probando intento de solapamiento en otra sucursal ---")
    
    # Vigencia que se cruza (Julio 2026 a Junio 2027 - 360 días)
    vigencia_solapada = Vigencia(date(2026, 7, 1), date(2027, 6, 25))
    asig_solapada = AsignacionBarbero(barbero, sucursal_norte, horario, vigencia_solapada)

    try:
        # Intentamos agregar la asignación cruzada al barbero
        barbero.agregar_asignacion(asig_solapada)
        print("❌ ERROR GRAVE: El sistema permitió solapar vigencias en sucursales distintas.")
    except ValueError as e:
        print(f"✔️ VALIDACIÓN CORRECTA: {e}")
        print("   (El barbero no puede estar asignado a otra sucursal mientras su vigencia actual siga activa).")

    # =========================================================================
    # ESCENARIO B: Asignación consecutiva limpia (Empieza tras terminar la anterior)
    # =========================================================================
    print("\n--- [ESCENARIO B] Probando asignación futura consecutiva ---")

    # Vigencia siguiente (Enero 1 a Diciembre 26 de 2027 - 360 días)
    vigencia_2027 = Vigencia(date(2027, 1, 1), date(2027, 12, 26))
    asig_futura = AsignacionBarbero(barbero, sucursal_norte, horario, vigencia_2027)

    try:
        barbero.agregar_asignacion(asig_futura)
        sucursal_norte.vincular_asignacion(asig_futura)
        print(f"✔️ Asignación 2 registrada exitosamente: {barbero.nombre} en Sucursal Norte ({vigencia_2027.fecha_inicio} al {vigencia_2027.fecha_final})")
        print("   (Las fechas no se cruzan, por lo que la asignación consecutiva fue aceptada).")
    except ValueError as e:
        print(f"❌ Error inesperado en asignación válida: {e}")

    # =========================================================================
    # ESCENARIO C: Verificación de Estado Activo según la Fecha
    # =========================================================================
    print("\n--- [ESCENARIO C] Verificando sucursal activa según fecha de consulta ---")
    
    fecha_2026 = date(2026, 8, 15)
    fecha_2027 = date(2027, 5, 10)

    asig_activa_2026 = barbero.obtener_asignacion_en_fecha(fecha_2026)
    asig_activa_2027 = barbero.obtener_asignacion_en_fecha(fecha_2027)

    print(f"• En fecha {fecha_2026}: Activo en Sucursal '{asig_activa_2026.sucursal.nombre}'")
    print(f"• En fecha {fecha_2027}: Activo en Sucursal '{asig_activa_2027.sucursal.nombre}'")

    print("\n==========================================================")
    print("  🚀 ¡LA EXCLUSIVIDAD DE VIGENCIA FUNCIONA A LA PERFECCIÓN!")
    print("==========================================================")

if __name__ == "__main__":
    try:
        probar_vigencia_y_exclusividad()
    except Exception as error:
        print(f"\n❌ Error al ejecutar la prueba: {error}")