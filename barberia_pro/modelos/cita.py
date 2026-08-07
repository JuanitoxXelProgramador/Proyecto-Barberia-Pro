from datetime import datetime

class Cita:
    def __init__(self,cliente,barbero,servicio,fecha,sucursal):

        #validando parametros 
        self._validar_parametros(cliente,barbero,servicio,fecha,sucursal)
        
        self.cliente = cliente
        self.barbero = barbero
        self.servicio = servicio
        self.sucursal = sucursal

        #validando fecha
        self.fecha = fecha

    def _validar_parametros(self, **kwargs):
        for nombre, valor in kwargs.items():
            if valor is None:
                raise ValueError(f"El parámetro '{nombre}' no puede estar vacío.")
            
    #falta hacer el resto de getters y setters 

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self,nueva_fecha):
        # Aquí ejecutamos la validación antes de guardar en la variable privada _fecha
        self._validar_fecha(nueva_fecha)
        self._fecha = nueva_fecha

    def _validar_fecha(self, fecha):
        if  datetime.now() > fecha:
            raise ValueError("La fecha no es valida")

    #Metodos especiales

    def __str__(self):
        return f"Cliente: {self.cliente}\nBarbero: {self.barbero}\nServicio: {self.servicio}\nFecha: {self.fecha}\nSucursal: {self.sucursal}"

        
