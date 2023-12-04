class RecipientesDAO:
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = self.conexion.cursor()

    def crear(self, recipiente):
        if not recipiente.nombre_recipiente or not recipiente.longitud:
            raise Exception("Campos incompletos")
        sql = "INSERT INTO recipientes(nombre_recipiente, longitud) VALUES(%s, %s)"
        val = (recipiente.nombre_recipiente, recipiente.longitud)
        try:
            self.cursor.execute(sql, val)
            self.conexion.commit()
            recipiente.recipiente_id = self.cursor.lastrowid
        except:
            print("No se pudo guardar el recipiente en la base de datos")
        finally:
            print(self.cursor.rowcount, "Recipiente agregado")
            self.cursor.close()
        return recipiente

    def obtener_todos(self):
        sql = "SELECT * FROM recipientes"
        try:
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            recipientes = []
            for resultado in resultados:
                recipiente = {
                    "recipiente_id": resultado[0],
                    "nombre_recipiente": resultado[1],
                    "longitud": resultado[2]
                }
                recipientes.append(recipiente)
            return recipientes
        except:
            print("No se pudo guardar la cantidad en la base de datos")


class CantidadesDAO:
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = self.conexion.cursor()

    def crear(self, cantidad):
        if not cantidad.cantidad or not cantidad.recipiente_id:
            raise Exception("Campos incompletos")
        sql = "INSERT INTO cantidades(cantidad, recipiente_id) VALUES(%s, %s)"
        val = (cantidad.cantidad, cantidad.recipiente_id)
        try:
            self.cursor.execute(sql, val)
            self.conexion.commit()
            cantidad.cantidad_id = self.cursor.lastrowid
        except:
            print("No se pudo guardar la cantidad en la base de datos")
        finally:
            print(self.cursor.rowcount, "Cantidad agregado")
        return cantidad

    def obtener_todos(self):
        sql = "SELECT * FROM cantidades ORDER BY fecha DESC LIMIT 10"
        try:
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            cantidades = []
            for resultado in resultados:
                cantidad = {
                    "cantidad_id": resultado[0],
                    "cantidad": resultado[1],
                    "fecha": resultado[2],
                    "recipiente_id": resultado[3]
                }
                cantidades.append(cantidad)
            return cantidades
        except:
            print("No se pudo obtener las cantidades")
