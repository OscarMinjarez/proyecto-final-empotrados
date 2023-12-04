class Recipiente:
    def __init__(self, nombre_recipiente, longitud):
        self.recipiente_id = None
        self.nombre_recipiente = nombre_recipiente
        self.longitud = longitud


class Cantidad:
    def __init__(self, cantidad, recipiente_id):
        self.cantidad_id = None
        self.cantidad = cantidad
        self.fecha = None
        self.recipiente_id = recipiente_id