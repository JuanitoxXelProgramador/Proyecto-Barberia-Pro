from datetime import date, timedelta


class Vigencia:

    def __init__(self, fecha_inicio: date, fecha_final: date):
        # Validar parámetros usando directamente las variables locales
        self._validar_parametros(fecha_inicio, fecha_final)

        # Asignación de atributos validados
        self._fecha_inicio = fecha_inicio
        self._fecha_final = fecha_final

    def esta_vigente_en(self, fecha: date | None = None) -> bool:
        """Comprueba si la vigencia aplica para una fecha dada (por defecto hoy)."""
        fecha_evaluar = fecha or date.today()
        return self.fecha_inicio <= fecha_evaluar <= self.fecha_final

    def dias_restantes(self) -> int:
        """Retorna los días que le quedan a la vigencia desde hoy."""
        if not self.esta_vigente_en():
                raise ValueError("La asignación no se encuentra vigente el día de hoy.")
        return (self.fecha_final - date.today()).days + 1

    def duracion_total(self) -> timedelta:
        """Calcula la duración total de esta vigencia."""
        return self.fecha_final - self.fecha_inicio

    # ====== PROPERTIES =====
    @property
    def fecha_inicio(self) -> date:
        return self._fecha_inicio

    @property
    def fecha_final(self) -> date:
        return self._fecha_final

    # ====== VALIDACIONES ====
    @staticmethod
    def _validar_dates(inicio: date, fin: date):
        if inicio > fin:
            raise ValueError(
                "La fecha de inicio debe ser obligatoriamente menor a la fecha de culminación."
            )
    @staticmethod
    def _validar_duracion(inicio: date, fin: date):
        # Sumamos 1 día para incluir ambos extremos (inclusive)
        dias_trabajados = (fin - inicio).days + 1
        
        if dias_trabajados < 15:
            raise ValueError("La vigencia mínima es de 15 días.")
            
        if dias_trabajados % 15 != 0:
            raise ValueError(f"La duración ({dias_trabajados} días) debe ser múltiplo de 15 días.")

    def _validar_parametros(self, inicio: date, fin: date):
        validar = [
            (inicio, date, "Inicio de la vigencia"),
            (fin, date, "Fin de la vigencia"),
        ]

        for parametro, instancia, etiqueta in validar:
            if not isinstance(parametro, instancia):
                raise TypeError(
                    f"El parámetro {etiqueta} no es del tipo date."
                )

        # Validar lógica pasando 'inicio' y 'fin'
        Vigencia._validar_dates(inicio, fin)
        Vigencia._validar_duracion(inicio, fin)