from modelos.servicio import Servicio

class GestorServicios:

    def __init__(self):
        self._servicios = {}

    def agregar_servicio(self, servicio):
        self._validar_servicio(servicio)
        self._servicios[servicio.id] = servicio

    def _validar_servicio(self, servicio):
        self._comprobar_instancia(servicio)
        self._validar_id(servicio)
        self._validar_nombre(servicio)

    def buscar_por_id(self, id_servicio: int):
        # 1. Validamos si hay servicios guardados en general
        self._servicios_existentes()

        # 2. Validamos si el ID específico existe dentro del diccionario
        self._validar_existencia_id(id_servicio)

        # 3. Retornamos el servicio asegurado
        return self._servicios[id_servicio]

    def listar_servicios(self):
        self._validar_catalogo_no_vacio()
        # Retornamos la lista de objetos Servicio guardados
        return list(self._servicios.values())

    def eliminar_servicio(self, id_servicio: int):
        # 1. Verificamos que el diccionario no esté vacío
        self._validar_catalogo_no_vacio()

        # 2. Verificamos si el ID NO está guardado
        if id_servicio not in self._servicios:
            raise ValueError(f"No se encontró ningún servicio con el ID {id_servicio}.")

        # 3. Borramos la entrada directamente de la colección usando su clave
        servicio = self._servicios.pop(id_servicio)
        return servicio
        
    # --- MÉTODOS PRIVADOS DE VALIDACIÓN ---

    def _comprobar_instancia(self, servicio):
        if not isinstance(servicio, Servicio):
            raise TypeError("El objeto no es una instancia de la clase Servicio.")

    def _validar_id(self, servicio):
        if servicio.id in self._servicios:
            raise ValueError(f"El servicio con ID {servicio.id} ya existe.")

    def _validar_nombre(self, servicio):
        for agregado in self._servicios.values():
            if servicio.nombre.lower() == agregado.nombre.lower():
                raise ValueError(f"Ya existe un servicio con el nombre '{servicio.nombre}'.")

    def _validar_catalogo_no_vacio(self):
        if not self._servicios:  # Forma 'pitónica' de evaluar si un dict   está vacío
            raise ValueError("Aún no contamos con servicios registrados.")

    def _validar_existencia_id(self, id_servicio: int):
        if id_servicio not in self._servicios:
            raise ValueError(f"No existe ningún servicio registrado con el ID {id_servicio}.")