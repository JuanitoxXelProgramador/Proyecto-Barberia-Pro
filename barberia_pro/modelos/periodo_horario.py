from datetime import datetime, date, time, timedelta


class PeriodoHorario:

    def __init__(self, hora_inicio: time, hora_fin: time):
        # validamos los parametros
        self._validar_parametros(hora_inicio, hora_fin)
        self._hora_inicio = hora_inicio
        self._hora_fin = hora_fin

    def contiene_intervalo(self, inicio: time, fin: time) -> bool:
        """Comprueba si un intervalo completo está contenido dentro de este período.
        """
        if not isinstance(inicio, time) or not isinstance(fin, time):
            raise TypeError("El inicio y fin deben ser de tipo time.")

        return self.hora_inicio <= inicio and fin <= self.hora_fin

    def duracion(self) -> timedelta:
        fecha_hoy = date.today()

        dt_inicio = datetime.combine(fecha_hoy, self._hora_inicio)
        dt_fin = datetime.combine(fecha_hoy, self._hora_fin)

        return dt_fin - dt_inicio

    # --- PROPERTIES Y SETTERS

    @property
    def hora_inicio(self) -> time:
        return self._hora_inicio

    @property
    def hora_fin(self) -> time:
        return self._hora_fin

    # --- VALIDACIONES ---

    def _validar_parametros(self, hora_inicio: time, hora_fin: time):

        validaciones = [
            (hora_inicio, time, "hora de inicio"),
            (hora_fin, time, "hora de cierre")
        ]

        for parametro, instancia, nombre in validaciones:

            if parametro is None:
                raise ValueError(
                    f"El parámetro {nombre} no puede estar vacío."
                )

            if not isinstance(parametro, instancia):
                raise TypeError(
                    f"El parámetro '{nombre}' debe ser de tipo "
                    f"{instancia.__name__}."
                )

        if hora_fin <= hora_inicio:
            raise ValueError(
                "La hora de cierre debe ser posterior a la hora de inicio."
            )

    # metodos especiales

    def __str__(self):
        return (
            f"{self._hora_inicio.strftime('%H:%M')} - "
            f"{self._hora_fin.strftime('%H:%M')}"
        )