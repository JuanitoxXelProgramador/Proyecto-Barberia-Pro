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

    def crear_asignacion(self,barbero: Barbero,sucursal: Sucursal,horario: Horario,vigencia: Vigencia):
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