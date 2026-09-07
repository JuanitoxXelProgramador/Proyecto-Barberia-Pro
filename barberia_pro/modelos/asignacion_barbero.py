from datetime import time,timedelta,datetime,date
from modelos.horario import Horario
from modelos.vigencia import Vigencia
from modelos.sucursal import Sucursal
from modelos.barbero import Barbero
class AsignacionBarbero:

    def __init__(self,barbero: Barbero,sucursal: Sucursal, horario: Horario, vigencia: Vigencia):
        self._validar_parametros(barbero, sucursal,horario,vigencia)

        self._barbero = barbero
        self._sucursal = sucursal
        self._horario = horario
        self._vigencia = vigencia

    
    def esta_activa(self, fecha: date | None = None) -> bool:
        return self.vigencia.esta_vigente_en(fecha)
    
    # ====== properties y setters
    @property
    def barbero(self):
        return self._barbero

    @property
    def sucursal(self):
        return self._sucursal

    @property
    def horario(self):
        return self._horario

    @property
    def vigencia(self):
        return self._vigencia

    def _validar_parametros(self,barbero: Barbero,sucursal: Sucursal, horario: Horario, vigencia: Vigencia):

        #creamos las validaciones
        validaciones = [
            (barbero, Barbero,f"Barbero al que pertenece la asignacion"),
            (sucursal,Sucursal,f"Sucursal asignada al barbero "),
            (horario,Horario,f"Horario asignado al barbero"),
            (vigencia, Vigencia, f"Vigencia asignada al barbero")
        ]

        #recorreomos las validaciones
        for parametro, instancia, etiqueta in validaciones:
            if parametro is None:
                raise ValueError(f"EL parametro {etiqueta} no puede estar vacio")

            if not isinstance(parametro,instancia):
                raise TypeError(f"El parámetro '{etiqueta}' debe ser de tipo {instancia.__name__}.")
