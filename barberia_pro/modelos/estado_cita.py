from enum import Enum

class EstadoCita(str,Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    EN_PROCESO = "en_proceso"
    CANCELADA = "cancelada"
    FINALIZADA = "finalizada"
