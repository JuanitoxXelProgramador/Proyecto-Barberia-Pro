from modelos.estado_barbero import EstadoBarbero
from modelos.servicio import Servicio
from modelos.vigencia import Vigencia
from datetime import date

class Barbero:
    contador_id = 1  # Iniciamos en 1 para IDs más naturales

    def __init__(self,nombre: str,apellido: str, documento: str,telefono: str,correo: str,estado: EstadoBarbero = EstadoBarbero.ACTIVO):
        # 1. Validamos tipos y formatos
        self._validar_parametros(
            nombre, apellido, documento, telefono, correo, estado
        )

        # 2. Asignamos atributos
        self._nombre = nombre.strip().title()
        self._apellido = apellido.strip().title()
        self._documento = documento.strip()
        self._telefono = telefono.strip()
        self._correo = correo.strip().lower()
        self._estado = estado
        self._servicios = []
        self._asignaciones = []

        # 3. Asignación de ID auto-incremental
        self._id = Barbero.contador_id
        Barbero.contador_id += 1

    def puede_realizar_servicio(self, servicio: Servicio) -> bool:

        # 1. Validar que sea un Servicio
        if not isinstance(servicio, Servicio):
            raise TypeError("El parámetro debe ser un objeto de tipo Servicio.")

        # 2. Comprobar si está dentro de los servicios del barbero
        return servicio in self._servicios

    def agregar_servicio(self,servicio: Servicio):
        if not isinstance(servicio,Servicio):
            raise TypeError("El parámetro debe ser un objeto de tipo Servicio.")

        if not servicio.estado:
            raise ValueError(f"El servicio '{servicio.nombre}' está inactivo.")

        if servicio in self._servicios:
            raise ValueError(f"El servicio '{servicio.nombre}' ya está asignado al barbero {self.nombre}.")
        
        self._servicios.append(servicio)

    def eliminar_servicio(self, id: int) -> Servicio:
        if not isinstance(id, int):
            raise TypeError("El id que busca debe ser de tipo int")

        if id <= 0:
            raise ValueError("El id no es valido")

        servicio = self.buscar_servicio(id)
        if servicio:
            self._servicios.remove(servicio)
            return servicio

        raise ValueError(f"El servicio con ID {id} no fue encontrado.")

    def buscar_servicio(self, id: int) -> Servicio:
        if not self.existen_servicios:  # Funciona como @property
            raise ValueError(
                f"El barbero {self.nombre} no cuenta con servicios asignados."
            )

        for servicio in self._servicios:
            if servicio.id == id:
                return servicio

        return None  # Si no lo encuentra, retorna None de forma explícita
    
    def listar_servicios(self) -> str:
        """Retorna una representación formateada en texto de los servicios asignados al barbero."""
        if not self.existen_servicios:
            return f"El barbero {self.nombre} {self.apellido} no tiene servicios asignados."

        lineas = [f"Servicios de {self.nombre} {self.apellido}:"]
        for servicio in self._servicios:
            lineas.append(
                f"  - [ID: {servicio.id}] {servicio.nombre} "
                f"| Duración: {servicio.duracion} min "
                f"| Precio: ${servicio.precio:,.0f}"
            )

        return "\n".join(lineas)
    
    # Elimina una asignación específica de la lista interna del barbero
    def remover_asignacion(self, asignacion) -> None:
        if type(asignacion).__name__ != "AsignacionBarbero":
            raise TypeError("El parámetro debe ser un objeto de tipo AsignacionBarbero.")

        if asignacion not in self._asignaciones:
            raise ValueError(f"La asignación no pertenece al barbero {self.nombre}.")

        self._asignaciones.remove(asignacion)

    def obtener_asignacion_en_fecha(self, fecha: date | None = None) -> "AsignacionBarbero | None":
        """Busca la asignación activa del barbero para una fecha determinada (por defecto hoy)."""
        fecha_consulta = fecha or date.today()
        for asignacion in self._asignaciones:
            if asignacion.esta_activa(fecha_consulta):
                return asignacion
        return None

    def obtener_asignaciones_por_sucursal(self, nombre_sucursal: str) -> list:
        """Devuelve todas las asignaciones del barbero en una sucursal específica."""

        if not isinstance(nombre_sucursal,str):
            raise TypeError("Nombre de la sucursal pasado por parametro obligatoria")

        nombre_sucursal = nombre_sucursal.strip()
        if nombre_sucursal is None or nombre_sucursal == "":
            raise ValueError(f"EL parametro del nombre de la sucursal no puede estar vacio")
        
        return [asig for asig in self._asignaciones if asig.sucursal.nombre == nombre_sucursal]
    
    #FUncion para validar el solapamiento en barbero y gestor asignaciones
    def validar_solapamiento_vigencia(self,vigencia: Vigencia) -> None:
        if not isinstance(vigencia,Vigencia):
            raise TypeError(f"El parámetro debe ser un objeto de tipo Vigencia")

        for asignacion in self._asignaciones:
            if vigencia.se_solapa_con(asignacion.vigencia):
                raise ValueError("Se solapa con otra vigencia de asignacion")
            
    #agregamos la asignacion
    def agregar_asignacion(self, otra_asignacion):
        # Opción A: Validación directa por tipo sin necesidad de import global
        if type(otra_asignacion).__name__ != "AsignacionBarbero":
            raise TypeError("El parámetro debe ser de tipo AsignacionBarbero.")
        
        # Validamos solapamiento y agregamos
        self.validar_solapamiento_vigencia(otra_asignacion.vigencia)
        self._asignaciones.append(otra_asignacion)

    @property
    def existen_servicios(self) -> bool:
        return len(self._servicios) > 0

    @property
    def servicios(self) -> list[Servicio]:
        return self._servicios.copy()  # Protege la lista contra mutaciones externas
    
    # --- PROPERTIES Y SETTERS ---
    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellido(self) -> str:
        return self._apellido

    @property
    def documento(self) -> str:
        return self._documento
 
    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def correo(self) -> str:
        return self._correo

    @property
    def estado(self) -> EstadoBarbero:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: EstadoBarbero):
        if not isinstance(nuevo_estado, EstadoBarbero):
            raise TypeError("El estado debe ser una instancia de EstadoBarbero.")
        self._estado = nuevo_estado

    @property
    def esta_activo(self) -> bool:
        return self._estado == EstadoBarbero.ACTIVO
    
    def cambiar_estado(self):
        """Alterna el estado del barbero fácilmente."""
        if self._estado == EstadoBarbero.ACTIVO:
            self._estado = EstadoBarbero.INACTIVO
        else:
            self._estado = EstadoBarbero.ACTIVO

    # --- VALIDACIONES ---
    def _validar_parametros(self,nombre: str,apellido: str,documento: str,telefono: str,correo: str,estado: EstadoBarbero):
        validaciones = [
            (nombre, str, "Nombre"),
            (apellido, str, "Apellido"),
            (documento, str, "Documento"),
            (telefono, str, "Teléfono"),
            (correo, str, "Correo"),
            (estado, EstadoBarbero, "Estado"),
        ]

        for parametro, instancia, etiqueta in validaciones:
            if parametro is None:
                raise ValueError(f"El parámetro '{etiqueta}' no puede estar vacío.")
            if not isinstance(parametro, instancia):
                raise TypeError(
                    f"El parámetro '{etiqueta}' debe ser de tipo {instancia.__name__}."
                )

        # Usamos not porque si retorna False significa que NO es válido
        if not self._validar_correo(correo):
            raise ValueError(f"El correo '{correo}' no tiene un formato válido.")

        if not self._validar_documento(documento):
            raise ValueError(f"El documento '{documento}' debe contener 10 dígitos numéricos.")

        if not self._validar_telefono(telefono):
            raise ValueError(f"El teléfono '{telefono}' debe contener 10 dígitos numéricos.")

    def _validar_correo(self, email: str) -> bool:
        email = email.strip()
        if email.count("@") != 1:
            return False

        usuario, dominio = email.split("@")
        if not usuario or "." not in dominio:
            return False

        dominio_nombre, extension = dominio.rsplit(".", 1)
        if not dominio_nombre or not extension:
            return False

        return True

    def _validar_documento(self, doc: str) -> bool:
        doc = doc.strip()
        return doc.isdigit() and len(doc) == 10

    def _validar_telefono(self, telf: str) -> bool:
        telf = telf.strip()
        return telf.isdigit() and len(telf) == 10