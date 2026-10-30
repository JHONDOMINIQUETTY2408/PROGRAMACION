#Nombre: JHON JAIRO PENARANDA DOMINIQUETTY
#Fecha: 29/10/2026
from abc import ABC, abstractmethod
from datetime import datetime
# registra eventos y errores
def registrar_log(mensaje):
    archivo = open("registro.txt", "a", encoding="utf-8")
    archivo.write(str(datetime.now()) + " - " + mensaje + "\n")
    archivo.close()
# excepciones personalizadas
class ErrorSistema(Exception):
    pass
class ErrorCliente(ErrorSistema):
    pass
class ErrorServicio(ErrorSistema):
    pass
class ErrorReserva(ErrorSistema):
    pass
# clase abstracta
class Entidad(ABC):
    def __init__(self, identificacion):
        self._identificacion = identificacion
    @abstractmethod
    def mostrar_informacion(self):
        pass
# clase cliente
class Cliente(Entidad):
    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)
        if not identificacion or not nombre:
            raise ErrorCliente("Identificacion y nombre obligatorios")
        if "@" not in correo or "." not in correo:
            raise ErrorCliente("Correo electronico invalido")
        if not telefono.isdigit() or len(telefono) < 7:
            raise ErrorCliente("Telefono invalido")
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono
    def mostrar_informacion(self):
        return "Cliente: " + self.__nombre + " - " + self.__correo
    def obtener_nombre(self):
        return self.__nombre
# clase abstracta servicio
class Servicio(Entidad):
    def __init__(self, identificacion, nombre, precio):
        super().__init__(identificacion)
        if precio <= 0:
            raise ErrorServicio("El precio debe ser mayor que cero")
        self.nombre = nombre
        self.precio = precio
    @abstractmethod
    def calcular_costo(self, cantidad=1):
        pass
    @abstractmethod
    def describir(self):
        pass
    @abstractmethod
    def validar(self):
        pass
    def mostrar_informacion(self):
        return self.describir()
# servicio 1: reserva de salas
class ReservaSala(Servicio):
    def __init__(self, identificacion, precio, capacidad):
        super().__init__(identificacion, "Reserva de sala", precio)
        if capacidad <= 0:
            raise ErrorServicio("Capacidad invalida")
        self.capacidad = capacidad
    def calcular_costo(self, cantidad=1):
        if cantidad <= 0:
            raise ErrorServicio("Cantidad de horas invalida")
        return self.precio * cantidad
    def describir(self):
        return "Sala con capacidad para " + str(self.capacidad) + " personas"
    def validar(self):
        return self.capacidad > 0
# servicio 2: alquiler de equipos
class AlquilerEquipo(Servicio):
    def __init__(self, identificacion, precio, equipo):
        super().__init__(identificacion, "Alquiler de equipos", precio)
        if not equipo:
            raise ErrorServicio("Debe indicar el equipo")
        self.equipo = equipo
    def calcular_costo(self, cantidad=1):
        if cantidad <= 0:
            raise ErrorServicio("Cantidad de dias invalida")
        return self.precio * cantidad
    def describir(self):
        return "Alquiler del equipo: " + self.equipo
    def validar(self):
        return self.precio > 0
# servicio 3: asesorias especializadas
class Asesoria(Servicio):
    def __init__(self, identificacion, precio, especialidad):
        super().__init__(identificacion, "Asesoria especializada", precio)
        if not especialidad:
            raise ErrorServicio("Debe indicar una especialidad")
        self.especialidad = especialidad
    def calcular_costo(self, cantidad=1):
        if cantidad <= 0:
            raise ErrorServicio("Cantidad de horas invalida")
        return self.precio * cantidad
    def describir(self):
        return "Asesoria en: " + self.especialidad
    def validar(self):
        return self.precio > 0
# clase reserva
class Reserva:
    def __init__(self, codigo, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Cliente no valido")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Servicio no valido")
        if duracion <= 0:
            raise ErrorReserva("Duracion incorrecta")
        if not servicio.validar():
            raise ErrorReserva("Servicio no disponible")
        self.codigo = codigo
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
    # calcula el costo con impuesto y descuento
    def procesar(self, impuesto=0, descuento=0):
        try:
            if impuesto < 0 or descuento < 0 or descuento > 100:
                raise ErrorReserva("Impuesto o descuento invalido")
            costo = self.servicio.calcular_costo(self.duracion)
            costo = costo + (costo * impuesto / 100)
            costo = costo - (costo * descuento / 100)
            if costo < 0:
                raise ErrorReserva("Calculo de costo incorrecto")
            registrar_log("Reserva procesada: " + str(self.codigo))
            return costo
        except ErrorSistema as error:
            registrar_log("Error al procesar reserva: " + str(error))
            raise ErrorReserva("No se pudo procesar la reserva") from error
        finally:
            print("Finalizando procesamiento de reserva")
    def confirmar(self):
        if self.estado != "Pendiente":
            raise ErrorReserva("La reserva no esta pendiente")
        self.estado = "Confirmada"
        registrar_log("Reserva confirmada: " + str(self.codigo))
    def cancelar(self):
        if self.estado == "Cancelada":
            raise ErrorReserva("La reserva ya esta cancelada")
        self.estado = "Cancelada"
        registrar_log("Reserva cancelada: " + str(self.codigo))
# clase principal del sistema
class SoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
    def registrar_cliente(self, cliente):
        for c in self.clientes:
            if c._identificacion == cliente._identificacion:
                raise ErrorCliente("El cliente ya existe")
        self.clientes.append(cliente)
        registrar_log("Cliente registrado correctamente")
    def registrar_servicio(self, servicio):
        for s in self.servicios:
            if s._identificacion == servicio._identificacion:
                raise ErrorServicio("El servicio ya existe")
        self.servicios.append(servicio)
        registrar_log("Servicio registrado correctamente")
    def registrar_reserva(self, reserva):
        for r in self.reservas:
            if r.codigo == reserva.codigo:
                raise ErrorReserva("Codigo de reserva repetido")
        self.reservas.append(reserva)
        registrar_log("Reserva registrada correctamente")
    def mostrar_clientes(self):
        print("\n--- CLIENTES ---")
        for c in self.clientes:
            print(c.mostrar_informacion())
    def mostrar_servicios(self):
        print("\n--- SERVICIOS ---")
        for s in self.servicios:
            print(s.describir())
    def mostrar_reservas(self):
        print("\n--- RESERVAS ---")
        for r in self.reservas:
            print("Codigo:", r.codigo)
            print("Cliente:", r.cliente.obtener_nombre())
            print("Servicio:", r.servicio.nombre)
            print("Estado:", r.estado)
# ejecucion y pruebas
sistema = SoftwareFJ()
print(" SISTEMA DE GESTION SOFTWARE FJ")
# operacion 1: registro de cliente
try:
    cliente1 = Cliente("1001", "Carlos Perez", "carlos@gmail.com", "3001234567")
    sistema.registrar_cliente(cliente1)
    print("Operacion 1: Cliente registrado")
except Exception as error:
    print("Error:", error)
    registrar_log("Error operacion 1: " + str(error))
# operacion 2: cliente invalido
try:
    cliente2 = Cliente("1002", "Maria Lopez", "correoincorrecto", "123")
    sistema.registrar_cliente(cliente2)
except Exception as error:
    print("Operacion 2: Error de cliente:", error)
    registrar_log("Error operacion 2: " + str(error))
# operacion 3: segundo cliente
try:
    cliente3 = Cliente("1003", "Ana Torres", "ana@gmail.com", "3104567890")
    sistema.registrar_cliente(cliente3)
    print("Operacion 3: Segundo cliente registrado")
except Exception as error:
    print("Error:", error)
    registrar_log("Error operacion 3: " + str(error))
# operacion 4: servicio de sala
try:
    sala = ReservaSala("S01", 50000, 20)
    sistema.registrar_servicio(sala)
    print("Operacion 4: Sala creada correctamente")
except Exception as error:
    print("Error:", error)
    registrar_log("Error operacion 4: " + str(error))
# operacion 5: alquiler de equipo
try:
    equipo = AlquilerEquipo("E01", 80000, "Proyector")
    sistema.registrar_servicio(equipo)
    print("Operacion 5: Equipo creado correctamente")
except Exception as error:
    print("Error:", error)
    registrar_log("Error operacion 5: " + str(error))
# operacion 6: asesoria
try:
    asesoria = Asesoria("A01", 100000, "Automatizacion")
    sistema.registrar_servicio(asesoria)
    print("Operacion 6: Asesoria creada correctamente")
except Exception as error:
    print("Error:", error)
    registrar_log("Error operacion 6: " + str(error))
# operacion 7: servicio invalido
try:
    servicio_invalido = ReservaSala("S02", -50000, 0)
    sistema.registrar_servicio(servicio_invalido)
except Exception as error:
    print("Operacion 7: Servicio invalido:", error)
    registrar_log("Error operacion 7: " + str(error))
# operacion 8: reserva correcta
try:
    reserva1 = Reserva("R001", cliente1, sala, 2)
    sistema.registrar_reserva(reserva1)
    print("Operacion 8: Reserva creada correctamente")
except Exception as error:
    print("Error:", error)
    registrar_log("Error operacion 8: " + str(error))
# operacion 9: procesar reserva
try:
    costo = reserva1.procesar(19, 10)
    print("Operacion 9: Costo de reserva:", costo)
    reserva1.confirmar()
    print("Reserva confirmada")
except Exception as error:
    print("Error:", error)
    registrar_log("Error operacion 9: " + str(error))
# operacion 10: reserva invalida
try:
    reserva2 = Reserva("R002", cliente1, sala, -2)
    sistema.registrar_reserva(reserva2)
except Exception as error:
    print("Operacion 10: Reserva invalida:", error)
    registrar_log("Error operacion 10: " + str(error))
# operacion 11: cancelar reserva
try:
    reserva1.cancelar()
    print("Operacion 11: Reserva cancelada")
except Exception as error:
    print("Error:", error)
    registrar_log("Error operacion 11: " + str(error))
# operacion 12: costo invalido
try:
    costo = reserva1.procesar(19, 150)
except Exception as error:
    print("Operacion 12: Error controlado:", error)
    registrar_log("Error operacion 12: " + str(error))
# resultados finales
sistema.mostrar_clientes()
sistema.mostrar_servicios()
sistema.mostrar_reservas()
print("\n")
print(" SISTEMA SOFTWARE FJ FINALIZADO")
print(" Los errores fueron registrados")
registrar_log("Ejecucion del sistema finalizada")