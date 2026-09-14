from modelos.barbero import Barbero
from modelos.horario import Horario
from modelos.sucursal import Sucursal
from modelos.vigencia import Vigencia
from modelos.asignacion_barbero import AsignacionBarbero

class GestorAsignaciones:
    """Coordinador de dominio encargado de orquestar la creación y vinculación
    atómica de una AsignacionBarbero entre Barbero y Sucursal.
    """

    def __init__(self):
        # Si en el futuro necesitas un repositorio central de asignaciones
        # o un registro global, se inicializa aquí.
        pass

        #las validaciones que debe seguir este metodo son en este orden
        #se valida el horario con el metodo de sucursal, _validar_horario_operativo
        #se valida que la vigencia no se solape con otras vigencias
        #se valida que barbero no tenga este vigente en otra sucursal
        #se asigna en barbero
        # se asigna en sucursal

    def cancelar_asignacion_activa(self, sucursal: Sucursal, id_barbero: int) -> AsignacionBarbero:
        # === 1. FASE DE VALIDACIÓN Y BÚSQUEDA (Sin mutar estado) ===
        if not isinstance(sucursal, Sucursal):
            raise TypeError("El parámetro 'sucursal' debe ser una instancia de Sucursal.")

        # Validamos que exista el barbero y que tenga una asignación activa en la sucursal
        # (Si no existe o el ID es inválido, lanzarás la excepción aquí antes de modificar nada)
        barbero = sucursal.buscar_barbero(id_barbero)
        asignacion_activa = sucursal.buscar_asignacion_activa_por_barbero(id_barbero)

        # Validamos que la asignación esté realmente en la lista del barbero
        if asignacion_activa not in barbero.asignaciones:
            raise ValueError(
                f"Error de inconsistencia: La asignación activa no se encuentra en el historial del barbero {barbero.nombre}."
            )

        # === 2. FASE DE EJECUCIÓN COORDINA (Mutación atómica) ===
        # Una vez todo está verificado a salvo, procedemos a desvincular en ambos lados:
        sucursal.eliminar_asignacion_activa_por_barbero(id_barbero)
        barbero.remover_asignacion(asignacion_activa)

        print(f"✔️ Asignación de {barbero.nombre} desvinculada exitosamente de {sucursal.nombre}.")
        
        return asignacion_activa

    def crear_asignacion(self,barbero: Barbero,sucursal: Sucursal,horario: Horario,vigencia: Vigencia) -> AsignacionBarbero:
        #primero validamos los parametros recibidos
        self._validar_parametros_asignacion(barbero,sucursal,horario,vigencia)
        #validaciones sin modificar el estado
        #validamos el horario operativo
        sucursal.validar_horario_operativo(horario)
        #validamos el solapamiento
        barbero.validar_solapamiento_vigencia(vigencia)
        #si no pasa ningun error entonces creamos la asignacion
        asignacion = AsignacionBarbero(barbero,sucursal,horario,vigencia)
        barbero.agregar_asignacion(asignacion)
        sucursal.vincular_asignacion(asignacion)

        return asignacion
        
    def _validar_parametros_asignacion(self,barbero: Barbero,sucursal: Sucursal,horario: Horario,vigencia: Vigencia) -> None:
        """Valida que ningún parámetro de entrada sea nulo y que pertenezcan
        a sus respectivas clases de dominio.
        """
        validaciones = [
            (barbero, Barbero, "barbero"),
            (sucursal, Sucursal, "sucursal"),
            (horario, Horario, "horario"),
            (vigencia, Vigencia, "vigencia"),
        ]

        for parametro, clase_esperada, nombre_campo in validaciones:
            if parametro is None:
                raise ValueError(
                    f"El parámetro '{nombre_campo}' no puede ser nulo (None)."
                )

            if not isinstance(parametro, clase_esperada):
                raise TypeError(
                    f"El parámetro '{nombre_campo}' debe ser de tipo {clase_esperada.__name__}, "
                    f"se recibió {type(parametro).__name__}."
                )