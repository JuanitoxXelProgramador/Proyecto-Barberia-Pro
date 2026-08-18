
from datetime import datetime,date, time, timedelta

class PeriodoHorario:

    def __init__(self,hora_inicio: time, hora_fin: time):
        #validamos lol parametros
        self._validar_parametros(hora_inicio,hora_fin)
        self._hora_inicio = hora_inicio
        self._hora_fin = hora_fin

    def duracion(self) -> timedelta:
        fecha_hoy = date.today()
        dt_inicio = datetime.combine(fecha_hoy, self._hora_inicio)
        dt_fin = datetime.combine(fecha_hoy, self._hora_fin)

        return dt_fin - dt_inicio
    
    # --- PROPERTIES Y SETTERS

    @property
    def hora_inicio(self):
        return self._hora_inicio
    
    @property
    def hora_fin(self):
        return self._hora_fin
    
    # --- VALIDACIONES ---
    def _validar_parametros(self,hora_inicio: time, hora_fin: time):

        validaciones = [
            (hora_inicio,time,"hora de inicio"),
            (hora_fin, time, "hora de cierre")
        ]

        for parametro, instancia, nombre in validaciones:
            if parametro is None:
                raise ValueError(f"EL parametro {nombre} no puede estar vacio")

            if not isinstance(parametro,instancia):
                raise TypeError(f"El parámetro '{nombre}' debe ser de tipo {instancia.__name__}.")

        if hora_fin <= hora_inicio:
            raise ValueError(
                "La hora de cierre debe ser posterior a la hora de inicio."
            )

    #metodos especiales
    def __str__(self):
        return f"{self._hora_inicio.strftime('%H:%M')} - {self._hora_fin.strftime('%H:%M')}"

# pr1 = PeriodoHorario(time(8,30), time(12,0))

# print(pr1.__str__())
# pr1.duracion()