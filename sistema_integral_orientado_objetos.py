#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNAD - Ingenieria de Sistemas.

//Nombres: Juan Carlos Orozco Navarro, Santiago Pachon Moreno
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

import os
import re
import logging
from abc import ABC, abstractmethod


# ===========================================================================
# CONFIGURACION DEL ARCHIVO DE LOGS
# ===========================================================================
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "software_fj_paquete2.log")
logging.basicConfig(
    filename=RUTA_LOG, level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S", encoding="utf-8")
logger = logging.getLogger("SoftwareFJ.P2")


# ===========================================================================
# JERARQUIA DE EXCEPCIONES PERSONALIZADAS
# ===========================================================================
class SoftwareFJError(Exception):
    """Excepcion base de la aplicacion. Todas las demas heredan de ella."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos de cliente que no superan las validaciones."""


class ServicioInvalidoError(SoftwareFJError):
    """Servicio creado con parametros invalidos."""


class ReservaInvalidaError(SoftwareFJError):
    """Reserva que no cumple las condiciones minimas."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parametro obligatorio en una operacion."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Operacion no valida para el estado actual del objeto."""


class CalculoInconsistenteError(SoftwareFJError):
    """Un calculo de costos produjo un resultado invalido."""


# ===========================================================================
# CLASE ABSTRACTA BASE
# ===========================================================================
class EntidadBase(ABC):
    """Clase abstracta con identificador comun y metodo describir() abstracto."""

    def __init__(self, identificador):
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        raise NotImplementedError

    def __str__(self):
        return self.describir()


# ===========================================================================
# CLASE CLIENTE (validaciones robustas que lanzan excepciones)
# ===========================================================================
class Cliente(EntidadBase):
    """Cliente con validaciones estrictas de sus datos personales."""

    _PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, identificador, nombre, documento, email):
        super().__init__(identificador)
        # Cada dato se valida antes de asignarse; si falla, se lanza excepcion.
        self._nombre = self._validar_nombre(nombre)
        self._documento = self._validar_documento(documento)
        self._email = self._validar_email(email)

    def _validar_nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteInvalidoError("El nombre del cliente es obligatorio.")
        return nombre.strip()

    def _validar_documento(self, documento):
        texto = str(documento).strip()
        if not texto.isdigit() or not (6 <= len(texto) <= 12):
            raise ClienteInvalidoError(
                f"Documento invalido: '{documento}'. Debe ser numerico (6-12 digitos).")
        return texto

    def _validar_email(self, email):
        if not isinstance(email, str) or not self._PATRON_EMAIL.match(email.strip()):
            raise ClienteInvalidoError(f"Correo electronico invalido: '{email}'.")
        return email.strip().lower()

    @property
    def nombre(self):
        return self._nombre

    def describir(self):
        return f"Cliente #{self._identificador}: {self._nombre} <{self._email}>"


# ===========================================================================
# CLASE ABSTRACTA SERVICIO + TRES SERVICIOS ESPECIALIZADOS
# ===========================================================================
class Servicio(EntidadBase):
    """Clase abstracta base de los servicios; valida parametros al construirse."""

    IVA_POR_DEFECTO = 0.19

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible
        self.validar_parametros()   # Lanza excepcion si los parametros son invalidos.

    @property
    def disponible(self):
        return self._disponible

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def validar_parametros(self):
        raise NotImplementedError

    @abstractmethod
    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        raise NotImplementedError

    def _aplicar_impuesto_y_descuento(self, subtotal, impuesto, descuento):
        """Sobrecarga del calculo: impuesto y descuento son opcionales."""
        if impuesto is None:
            impuesto = self.IVA_POR_DEFECTO
        if descuento is None:
            descuento = 0.0
        if not (0 <= impuesto <= 1) or not (0 <= descuento <= 1):
            raise CalculoInconsistenteError(
                "Impuesto y descuento deben expresarse entre 0 y 1.")
        total = subtotal * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El costo calculado resulto negativo.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio de reserva de salas (cantidad en horas)."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad,
                 disponible=True):
        self._capacidad = capacidad
        super().__init__(identificador, nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        if self._tarifa_base <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser positiva.")
        if self._capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser positiva.")

    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        if cantidad <= 0:
            raise CalculoInconsistenteError("Las horas deben ser mayores a cero.")
        return self._aplicar_impuesto_y_descuento(
            self._tarifa_base * cantidad, impuesto, descuento)

    def describir(self):
        return (f"Sala '{self._nombre}' (cap. {self._capacidad}) - "
                f"${self._tarifa_base:,.0f}/hora")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (cantidad en dias)."""

    def __init__(self, identificador, nombre, tarifa_dia, tipo_equipo,
                 disponible=True):
        self._tipo_equipo = tipo_equipo
        super().__init__(identificador, nombre, tarifa_dia, disponible)

    def validar_parametros(self):
        if self._tarifa_base <= 0:
            raise ServicioInvalidoError("La tarifa por dia debe ser positiva.")
        if not str(self._tipo_equipo).strip():
            raise ServicioInvalidoError("El tipo de equipo es obligatorio.")

    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        if cantidad <= 0:
            raise CalculoInconsistenteError("Los dias deben ser mayores a cero.")
        return self._aplicar_impuesto_y_descuento(
            self._tarifa_base * cantidad, impuesto, descuento)

    def describir(self):
        return (f"Equipo '{self._nombre}' ({self._tipo_equipo}) - "
                f"${self._tarifa_base:,.0f}/dia")


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria especializada (cantidad en horas)."""

    def __init__(self, identificador, nombre, tarifa_hora, area,
                 recargo_experto=0.15, disponible=True):
        self._area = area
        self._recargo_experto = recargo_experto
        super().__init__(identificador, nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        if self._tarifa_base <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser positiva.")
        if self._recargo_experto < 0:
            raise ServicioInvalidoError("El recargo de experto no puede ser negativo.")

    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        if cantidad <= 0:
            raise CalculoInconsistenteError("Las horas deben ser mayores a cero.")
        subtotal = self._tarifa_base * (1 + self._recargo_experto) * cantidad
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (f"Asesoria '{self._nombre}' (area {self._area}) - "
                f"${self._tarifa_base:,.0f}/hora + {self._recargo_experto:.0%} experto")


# ===========================================================================
# CLASE RESERVA (control de estados con excepciones y encadenamiento)
# ===========================================================================
class Reserva(EntidadBase):
    """Reserva con ciclo de vida controlado mediante excepciones."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)
        if cliente is None or servicio is None:
            raise ParametroFaltanteError("La reserva requiere cliente y servicio.")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaInvalidaError("La duracion debe ser un numero positivo.")
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = self.PENDIENTE

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}.")
        self._estado = self.CONFIRMADA

    def procesar(self, impuesto=None, descuento=None):
        """Procesa la reserva; encadena la excepcion si el calculo falla."""
        if self._estado != self.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas confirmadas (estado: {self._estado}).")
        try:
            costo = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
        except CalculoInconsistenteError as error:
            # Encadenamiento: se conserva la causa original con 'from'.
            raise ReservaInvalidaError(
                "No se pudo procesar la reserva por un calculo invalido.") from error
        else:
            self._estado = self.PROCESADA
            return costo

    def describir(self):
        return (f"Reserva #{self._identificador} | {self._cliente.nombre} -> "
                f"{self._servicio.nombre} | {self._duracion}h | {self._estado}")


# ===========================================================================
# DEMOSTRACION DEL MANEJO DE EXCEPCIONES
# ===========================================================================
def main():
    """Muestra los distintos patrones de manejo de excepciones exigidos."""
    print("PAQUETE 2 - Manejo de excepciones del sistema 'Software FJ'\n")

    # 1) try/except sencillo: cliente con correo invalido.
    try:
        Cliente(1, "Luis Perez", "1000111222", "correo_malo")
    except ClienteInvalidoError as error:
        print("try/except        ->", error)
        logger.error("Cliente invalido: %s", error)

    # 2) try/except/else: si el cliente es valido, se ejecuta el else.
    try:
        cliente = Cliente(2, "Ana Gomez", "1090234567", "ana@softwarefj.com")
    except ClienteInvalidoError as error:
        print("try/except/else   -> error:", error)
    else:
        print("try/except/else   -> cliente OK:", cliente.describir())
        logger.info("Cliente valido: %s", cliente.describir())

    # 3) try/except/finally: el finally se ejecuta siempre.
    try:
        servicio = ReservaSala(10, "Sala Fantasma", -100, 5)   # tarifa invalida
    except ServicioInvalidoError as error:
        print("try/except/finally-> error:", error)
    finally:
        print("try/except/finally-> bloque finally ejecutado (limpieza).")
        logger.info("Bloque finally ejecutado en creacion de servicio.")

    # 4) Encadenamiento de excepciones (raise ... from).
    cliente_ok = Cliente(3, "Marta Ruiz", "1050998877", "marta@softwarefj.com")
    sala_ok = ReservaSala(11, "Sala Innovacion", 50000, 12)
    reserva = Reserva(100, cliente_ok, sala_ok, 3)
    reserva.confirmar()
    try:
        # Se fuerza un descuento invalido para provocar el encadenamiento.
        reserva.procesar(descuento=2.0)
    except ReservaInvalidaError as error:
        print("encadenamiento    ->", error)
        print("                     causa original:", repr(error.__cause__))
        logger.error("Reserva fallida: %s | causa: %s", error, error.__cause__)

    print(f"\nEventos y errores registrados en: {RUTA_LOG}")


if __name__ == "__main__":
    main()
