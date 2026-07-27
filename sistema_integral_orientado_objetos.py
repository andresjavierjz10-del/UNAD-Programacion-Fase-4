#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNAD - Ingenieria de Sistemas.

//Nombres: Juan Carlos Orozco Navarro, Santiago Pachon Moreno, Andres Javier Uribe Jimenez
//Programa: Ingenieria de Sistemas
//Codigo fuente: Autoria Juan Carlos Orozco Navarro
//Fecha: 2026-07-17
//Descripcion: Fase 4 - PAQUETE 2 (ESTRUCTURA + EXCEPCIONES). Toma la estructura
//             de clases del paquete 1 y le incorpora el manejo de excepciones
//             solicitado por la rubrica: excepciones personalizadas,
//             validaciones estrictas que las lanzan, registro en un archivo de
//             logs y ejemplos de try/except, try/except/else, try/except/finally
//             y encadenamiento de excepciones (raise ... from).

Curso: Programacion (213023A_2203) - Fase 4 (RAC3)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import re
import logging
from abc import ABC, abstractmethod
from datetime import datetime


# ===========================================================================
# CONFIGURACION DEL ARCHIVO DE LOGS
# ===========================================================================
# El log se guarda junto al script para registrar cada evento y cada error,
# de modo que la aplicacion pueda seguir funcionando y dejar trazabilidad.
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "software_fj_eventos.log")

logging.basicConfig(
    filename=RUTA_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)
logger = logging.getLogger("SoftwareFJ")


# ===========================================================================
# JERARQUIA DE EXCEPCIONES PERSONALIZADAS
# ===========================================================================
class SoftwareFJError(Exception):
    """Excepcion base de la aplicacion. Todas las demas heredan de ella."""


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no superan las validaciones."""


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando un servicio se crea con parametros invalidos."""


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no cumple las condiciones minimas."""


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parametro obligatorio en una operacion."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operacion no valida para el estado actual."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un calculo de costos produce un resultado invalido."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio marcado como no disponible."""


# ===========================================================================
# CLASE ABSTRACTA BASE (entidades generales del sistema)
# ===========================================================================
class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema de gestión.

    Su propósito es servir como base para todas las entidades del programa, proporcionando
    un identificador único común y definiendo una estructura que las clases derivadas deben
    seguir. Al ser una clase abstracta, no puede instanciarse directamente, sino que obliga
    a las subclases a implementar el método describir(), garantizando que cada entidad
    proporcione su propia representación de acuerdo con sus características. Además,
    favorece la reutilización de código, la aplicación de la herencia y el polimorfismo,
    permitiendo que diferentes tipos de entidades compartan un comportamiento común sin
    perder su funcionalidad específica.
    """

    def __init__(self, identificador):
        # Atributo protegido: identificador unico de la entidad.
        self._identificador = identificador

    @property
    def identificador(self):
        """Expone el identificador de solo lectura (encapsulacion)."""
        return self._identificador

    @abstractmethod
    def describir(self):
        """Metodo abstracto: cada entidad describe su informacion propia."""
        raise NotImplementedError

    def __str__(self):
        """Representacion legible: delega en el metodo polimorfico describir()."""
        return self.describir()


# ===========================================================================
# CLASE CLIENTE (validaciones robustas y encapsulacion de datos personales)
# ===========================================================================
class Cliente(EntidadBase):
    """Representa a un cliente de la empresa Software FJ, almacenando de forma
    segura su información personal, como el nombre, el documento de identidad
    y el correo electrónico. Todos estos datos se encapsulan mediante atributos
    privados y son validados desde el momento en que se crea el objeto, con el
    fin de garantizar la integridad y consistencia de la información. Si alguno
    de los datos ingresados no cumple las condiciones establecidas, se lanza la
    excepción personalizada ClienteInvalidoError, evitando que se registren
    clientes con información incorrecta dentro del sistema. Además, la clase
    hereda de EntidadBase, por lo que comparte un identificador único e
    implementa el método describir(), proporcionando una representación propia
    del cliente y demostrando la aplicación de los principios de herencia,
    encapsulación y polimorfismo de la programación orientada a objetos.
    """

    # Expresion regular sencilla para validar el formato del correo.
    _PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, identificador, nombre, documento, email):
        super().__init__(identificador)
        # Se validan los datos antes de asignarlos (fail-fast).
        self._nombre = self._validar_nombre(nombre)
        self._documento = self._validar_documento(documento)
        self._email = self._validar_email(email)

    # --- Validaciones privadas y estrictas ---
    def _validar_nombre(self, nombre):
        """El nombre no puede estar vacio ni ser solo espacios."""
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteInvalidoError("El nombre del cliente es obligatorio.")
        return nombre.strip()

    def _validar_documento(self, documento):
        """El documento debe ser numerico y tener entre 6 y 12 digitos."""
        texto = str(documento).strip()
        if not texto.isdigit() or not (6 <= len(texto) <= 12):
            raise ClienteInvalidoError(
                f"Documento invalido: '{documento}'. Debe ser numerico (6-12 digitos).")
        return texto

    def _validar_email(self, email):
        """El correo debe cumplir un formato basico usuario@dominio.ext."""
        if not isinstance(email, str) or not self._PATRON_EMAIL.match(email.strip()):
            raise ClienteInvalidoError(f"Correo electronico invalido: '{email}'.")
        return email.strip().lower()

    # --- Acceso de solo lectura a los datos personales ---
    @property
    def nombre(self):
        return self._nombre

    @property
    def email(self):
        return self._email

    def describir(self):
        """Implementacion polimorfica del metodo abstracto."""
        return f"Cliente #{self._identificador}: {self._nombre} <{self._email}>"


# ===========================================================================
# CLASE ABSTRACTA SERVICIO (base de los tres servicios especializados)
# ===========================================================================
class Servicio(EntidadBase):
    """Clase abstracta que define la estructura y el comportamiento común de todos
    los servicios ofrecidos por Software FJ. Su función es establecer un contrato
    que todas las clases derivadas deben cumplir, garantizando que cada servicio
    implemente sus propios métodos para validar parámetros, calcular costos y
    describir su información de acuerdo con sus características particulares.
    Además, incorpora atributos compartidos, como el nombre, la tarifa base y la
    disponibilidad del servicio, junto con funcionalidades comunes para el cálculo
    de impuestos y descuentos. Al ser una clase abstracta, no puede instanciarse
    directamente, sino que sirve como base para clases especializadas, promoviendo
    la reutilización de código y la correcta aplicación de los principios de
    abstracción, herencia y polimorfismo de la programación orientada a objetos.
    """

    # Impuesto por defecto (IVA 19 %) usado en el calculo de costos.
    IVA_POR_DEFECTO = 0.19

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible
        # La validacion de parametros se ejecuta al construir el servicio.
        self.validar_parametros()

    @property
    def disponible(self):
        return self._disponible

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def validar_parametros(self):
        """Valida los parametros propios del servicio. Lanza excepcion si fallan."""
        raise NotImplementedError

    @abstractmethod
    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        """Calcula el costo del servicio. Metodo sobrecargado (ver subclases)."""
        raise NotImplementedError

    def _aplicar_impuesto_y_descuento(self, subtotal, impuesto, descuento):
        """Metodo auxiliar comun que aplica descuento y luego impuesto.

        Demuestra la sobrecarga: los parametros impuesto y descuento son
        opcionales, por lo que el mismo metodo sirve para varios escenarios:
          - calcular_costo(cantidad)                      -> solo subtotal + IVA
          - calcular_costo(cantidad, impuesto)            -> impuesto propio
          - calcular_costo(cantidad, impuesto, descuento) -> impuesto y descuento
        """
        # Si no se indica impuesto, se usa el IVA por defecto de la clase.
        if impuesto is None:
            impuesto = self.IVA_POR_DEFECTO
        if descuento is None:
            descuento = 0.0

        # Validaciones defensivas para evitar calculos inconsistentes.
        if not (0 <= impuesto <= 1) or not (0 <= descuento <= 1):
            raise CalculoInconsistenteError(
                "Impuesto y descuento deben expresarse entre 0 y 1.")

        total = subtotal * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El costo calculado resulto negativo.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio de reserva de salas. La cantidad representa horas de uso."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad,
                 disponible=True):
        self._capacidad = capacidad
        super().__init__(identificador, nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        """La tarifa y la capacidad deben ser positivas."""
        if self._tarifa_base <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser positiva.")
        if self._capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser positiva.")

    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        """Costo = tarifa_hora * horas, con impuestos y descuentos opcionales."""
        if cantidad <= 0:
            raise CalculoInconsistenteError("Las horas deben ser mayores a cero.")
        subtotal = self._tarifa_base * cantidad
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (f"Sala '{self._nombre}' (cap. {self._capacidad}) - "
                f"${self._tarifa_base:,.0f}/hora")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos. La cantidad representa dias de alquiler."""

    def __init__(self, identificador, nombre, tarifa_dia, tipo_equipo,
                 disponible=True):
        self._tipo_equipo = tipo_equipo
        super().__init__(identificador, nombre, tarifa_dia, disponible)

    def validar_parametros(self):
        """La tarifa por dia debe ser positiva y el tipo no puede estar vacio."""
        if self._tarifa_base <= 0:
            raise ServicioInvalidoError("La tarifa por dia debe ser positiva.")
        if not str(self._tipo_equipo).strip():
            raise ServicioInvalidoError("El tipo de equipo es obligatorio.")

    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        """Costo = tarifa_dia * dias, con impuestos y descuentos opcionales."""
        if cantidad <= 0:
            raise CalculoInconsistenteError("Los dias deben ser mayores a cero.")
        subtotal = self._tarifa_base * cantidad
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (f"Equipo '{self._nombre}' ({self._tipo_equipo}) - "
                f"${self._tarifa_base:,.0f}/dia")


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria especializada. La cantidad representa horas."""

    def __init__(self, identificador, nombre, tarifa_hora, area,
                 recargo_experto=0.15, disponible=True):
        self._area = area
        self._recargo_experto = recargo_experto
        super().__init__(identificador, nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        """La tarifa debe ser positiva y el recargo no puede ser negativo."""
        if self._tarifa_base <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser positiva.")
        if self._recargo_experto < 0:
            raise ServicioInvalidoError("El recargo de experto no puede ser negativo.")

    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        """Costo con recargo por experticia sobre la tarifa base."""
        if cantidad <= 0:
            raise CalculoInconsistenteError("Las horas deben ser mayores a cero.")
        # El recargo de experto se suma a la tarifa antes de calcular.
        subtotal = self._tarifa_base * (1 + self._recargo_experto) * cantidad
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (f"Asesoria '{self._nombre}' (area {self._area}) - "
                f"${self._tarifa_base:,.0f}/hora + {self._recargo_experto:.0%} experto")


# ===========================================================================
# CLASE RESERVA (integra cliente, servicio, duracion y estado)
# ===========================================================================
class Reserva(EntidadBase):
    """Reserva que vincula un cliente con un servicio por una duracion dada.

    Maneja su ciclo de vida mediante estados y controla las transiciones con
    excepciones para impedir operaciones no permitidas.
    """

    # Estados posibles del ciclo de vida de la reserva.
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)
        # Validaciones de integridad de la reserva.
        if cliente is None or servicio is None:
            raise ParametroFaltanteError("La reserva requiere cliente y servicio.")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaInvalidaError("La duracion debe ser un numero positivo.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no esta disponible.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = self.PENDIENTE
        self._costo_total = None

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self):
        """Confirma la reserva. Solo es valido desde el estado PENDIENTE."""
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}.")
        self._estado = self.CONFIRMADA

    def cancelar(self):
        """Cancela la reserva. No se puede cancelar si ya fue procesada."""
        if self._estado == self.PROCESADA:
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva ya procesada.")
        self._estado = self.CANCELADA

    def procesar(self, impuesto=None, descuento=None):
        """Procesa la reserva calculando su costo final (usa try/except/else).

        Solo se puede procesar una reserva CONFIRMADA. El calculo del costo se
        delega al servicio (polimorfismo) y cualquier error de calculo se
        encadena para conservar la causa original.
        """
        if self._estado != self.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas confirmadas (estado actual: {self._estado}).")
        try:
            costo = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
        except CalculoInconsistenteError as error:
            # Encadenamiento de excepciones: se conserva la causa original.
            raise ReservaInvalidaError(
                "No se pudo procesar la reserva por un calculo invalido.") from error
        else:
            # El bloque else se ejecuta solo si no hubo excepcion.
            self._costo_total = costo
            self._estado = self.PROCESADA
            return costo

    def describir(self):
        return (f"Reserva #{self._identificador} | {self._cliente.nombre} -> "
                f"{self._servicio.nombre} | {self._duracion}h | {self._estado}")


# ===========================================================================
# GESTOR CENTRAL (listas internas y orquestacion con manejo de excepciones)
# ===========================================================================
class GestorSoftwareFJ:
    """Administra las listas internas de clientes, servicios y reservas.

    Cada operacion registra eventos y errores en el archivo de logs y mantiene
    la aplicacion estable capturando las excepciones que puedan producirse.
    """

    def __init__(self):
        self._clientes = []     # Lista interna de clientes registrados.
        self._servicios = []    # Lista interna de servicios creados.
        self._reservas = []     # Lista interna de reservas gestionadas.
        logger.info("Sistema Software FJ iniciado.")

    def registrar_cliente(self, cliente):
        """Agrega un cliente ya validado a la lista interna."""
        self._clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.describir())
        return cliente

    def registrar_servicio(self, servicio):
        """Agrega un servicio ya validado a la lista interna."""
        self._servicios.append(servicio)
        logger.info("Servicio creado: %s", servicio.describir())
        return servicio

    def registrar_reserva(self, reserva):
        """Agrega una reserva a la lista interna."""
        self._reservas.append(reserva)
        logger.info("Reserva creada: %s", reserva.describir())
        return reserva

    def resumen(self):
        """Devuelve un conteo del estado actual del sistema."""
        return {
            "clientes": len(self._clientes),
            "servicios": len(self._servicios),
            "reservas": len(self._reservas),
        }


# ===========================================================================
# SIMULACION DE OPERACIONES (10+ operaciones validas e invalidas)
# ===========================================================================
def ejecutar(descripcion, funcion):
    """Ejecuta una operacion capturando cualquier error para no detener el programa.

    Aplica el patron try/except/finally: si la operacion falla, se informa y se
    registra en el log, pero la simulacion continua con la siguiente operacion.
    """
    print(f"\n> {descripcion}")
    try:
        resultado = funcion()
    except SoftwareFJError as error:
        # Errores esperados del dominio: se informan de forma controlada.
        print(f"  [CONTROLADO] {type(error).__name__}: {error}")
        logger.error("%s -> %s: %s", descripcion, type(error).__name__, error)
    except Exception as error:  # Red de seguridad para errores inesperados.
        print(f"  [INESPERADO] {type(error).__name__}: {error}")
        logger.critical("%s -> %s: %s", descripcion, type(error).__name__, error)
    else:
        print(f"  [OK] {resultado}")
        return resultado
    finally:
        # El finally se ejecuta siempre, haya o no error.
        logger.info("Operacion finalizada: %s", descripcion)


def main():
    """Punto de entrada: corre la simulacion de al menos 10 operaciones."""
    print("=" * 70)
    print(" SIMULACION - SISTEMA DE RESERVAS 'SOFTWARE FJ' (Fase 4)")
    print(" Manejo avanzado de excepciones sin base de datos")
    print(" Integrantes: Juan Carlos Orozco Navarro, Santiago Pachon Moreno")
    print("=" * 70)

    gestor = GestorSoftwareFJ()

    # --- Operaciones con CLIENTES (validas e invalidas) ---
    c1 = ejecutar("1. Registrar cliente valido",
                  lambda: gestor.registrar_cliente(
                      Cliente(1, "Ana Gomez", "1090234567", "ana@softwarefj.com")))
    ejecutar("2. Registrar cliente con correo invalido",
             lambda: gestor.registrar_cliente(
                 Cliente(2, "Luis Perez", "1000111222", "luis#correo")))
    ejecutar("3. Registrar cliente con documento invalido",
             lambda: gestor.registrar_cliente(
                 Cliente(3, "Marta Ruiz", "ABC", "marta@softwarefj.com")))

    # --- Operaciones con SERVICIOS (validas e invalidas) ---
    s1 = ejecutar("4. Crear servicio de sala valido",
                  lambda: gestor.registrar_servicio(
                      ReservaSala(10, "Sala Innovacion", 50000, 12)))
    s2 = ejecutar("5. Crear servicio de alquiler de equipo valido",
                  lambda: gestor.registrar_servicio(
                      AlquilerEquipo(11, "Videobeam 4K", 30000, "Proyector")))
    s3 = ejecutar("6. Crear servicio de asesoria valido",
                  lambda: gestor.registrar_servicio(
                      AsesoriaEspecializada(12, "Asesoria Cloud", 80000, "DevOps")))
    ejecutar("7. Crear servicio con tarifa invalida (negativa)",
             lambda: gestor.registrar_servicio(
                 ReservaSala(13, "Sala Fantasma", -1000, 5)))
    # Servicio no disponible para probar reservas fallidas mas adelante.
    s_no_disp = ejecutar("8. Crear servicio marcado como NO disponible",
                         lambda: gestor.registrar_servicio(
                             AlquilerEquipo(14, "Laptop en mantenimiento", 25000,
                                            "Laptop", disponible=False)))

    # --- Operaciones con RESERVAS (exitosas y fallidas) ---
    r1 = ejecutar("9. Crear reserva valida (sala, 3 horas)",
                  lambda: gestor.registrar_reserva(Reserva(100, c1, s1, 3)))
    ejecutar("10. Confirmar y procesar la reserva (costo con IVA)",
             lambda: (r1.confirmar(), r1.procesar())[1])
    ejecutar("11. Procesar de nuevo la reserva ya procesada (no permitido)",
             lambda: r1.procesar())
    ejecutar("12. Crear reserva con duracion invalida (0 horas)",
             lambda: gestor.registrar_reserva(Reserva(101, c1, s2, 0)))
    ejecutar("13. Crear reserva sobre servicio NO disponible",
             lambda: gestor.registrar_reserva(Reserva(102, c1, s_no_disp, 2)))

    # --- Demostracion de metodos sobrecargados (calculo de costos) ---
    ejecutar("14. Costo asesoria 5h SOLO IVA por defecto",
             lambda: s3.calcular_costo(5))
    ejecutar("15. Costo asesoria 5h con impuesto 5% y descuento 10%",
             lambda: s3.calcular_costo(5, 0.05, 0.10))

    # --- Reserva adicional: confirmar y luego cancelar ---
    r2 = ejecutar("16. Crear segunda reserva (equipo, 2 dias)",
                  lambda: gestor.registrar_reserva(Reserva(103, c1, s2, 2)))
    ejecutar("17. Cancelar la segunda reserva",
             lambda: (r2.cancelar(), "Reserva cancelada")[1])
    ejecutar("18. Procesar reserva cancelada (operacion no permitida)",
             lambda: r2.procesar())

    # --- Cierre de la simulacion ---
    print("\n" + "=" * 70)
    print(" RESUMEN FINAL:", gestor.resumen())
    print(f" Eventos y errores registrados en: {RUTA_LOG}")
    print("=" * 70)
    logger.info("Simulacion finalizada. Resumen: %s", gestor.resumen())


if __name__ == "__main__":
    main()

# ===========================================================================
# INTERFAZ GRÁFICA DE USUARIO (GUI) - CORREGIDA
# ===========================================================================
class AplicacionGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Software FJ - Digitalizar Campos (Clientes)")
        self.geometry("600x450")
        self.resizable(False, False)

        # Contenedor principal de campos
        frame_campos = ttk.LabelFrame(self, text=" Captura de Campos en Tiempo Real ")
        frame_campos.pack(fill="x", padx=15, pady=15, ipady=5)
        
        # Configurar pesos de columnas para que los Entry se expandan correctamente
        frame_campos.columnconfigure(1, weight=1)

        # Construcción de las entradas de texto (Se cambió fill/expand por sticky="ew")
        ttk.Label(frame_campos, text="ID de Entidad:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.txt_id = ttk.Entry(frame_campos)
        self.txt_id.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame_campos, text="Nombre del Cliente:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txt_nombre = ttk.Entry(frame_campos)
        self.txt_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame_campos, text="Documento (6-12 números):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.txt_doc = ttk.Entry(frame_campos)
        self.txt_doc.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame_campos, text="Correo Electrónico:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.txt_email = ttk.Entry(frame_campos)
        self.txt_email.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Botón para detonar las validaciones originales
        btn_procesar = ttk.Button(self, text="Validar y Crear Instancia", command=self._procesar_campos_usuario)
        btn_procesar.pack(pady=10)

        # Consola visual para retroalimentación
        ttk.Label(self, text="Estado de las Validaciones / Consola de Errores:").pack(anchor="w", padx=15)
        self.txt_resultado = tk.Text(self, height=8, wrap="word", bg="#f4f4f4")
        self.txt_resultado.pack(fill="both", padx=15, pady=5, expand=True)

    def _procesar_campos_usuario(self):
        self.txt_resultado.delete("1.0", tk.END)

        # Recolecta lo que el usuario digita en la ventana
        usuario_id = self.txt_id.get()
        usuario_nombre = self.txt_nombre.get()
        usuario_doc = self.txt_doc.get()
        usuario_email = self.txt_email.get()

        # Conexión directa con la clase Cliente original
        try:
            nuevo_cliente = Cliente(usuario_id, usuario_nombre, usuario_doc, usuario_email)
            resultado_exito = f"¡ÉXITO EN VALIDACIÓN!\nObjeto guardado en memoria:\n{nuevo_cliente.describir()}"
            self.txt_resultado.insert(tk.END, resultado_exito)
            messagebox.showinfo("Campos Correctos", "El cliente supera las validaciones del sistema.")

        except ClienteInvalidoError as error:
            # Captura el error exacto de validación
            resultado_error = f"ERROR CONTROLADO (ClienteInvalidoError):\n{error}"
            self.txt_resultado.insert(tk.END, resultado_error)
            messagebox.showerror("Error en Campos", str(error))

        except Exception as error:
            resultado_critico = f"ERROR INESPERADO:\n{error}"
            self.txt_resultado.insert(tk.END, resultado_critico)
            messagebox.showerror("Fatal Error", "Ocurrió un fallo en el sistema.")
