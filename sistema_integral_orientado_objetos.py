#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNAD - Ingenieria de Sistemas.

//Nombre: Juan Carlos Orozco Navarro
//Programa: Ingenieria de Sistemas
//Codigo fuente: Autoria Juan Carlos Orozco Navarro
//Fecha: 2026-07-17
//Descripcion: Fase 4 - PAQUETE 1 (ESTRUCTURA). Se suben  estructura
//             de clases y metodos del sistema de reservas "Software FJ":
//             clase abstracta base, Cliente, clase abstracta Servicio con tres
//             servicios especializados, Reserva y el gestor central. En este
//             paquete todavia NO se incorporan las excepciones personalizadas
//             ni el registro en logs (eso se agrega en el paquete 2).

Curso: Programacion (213023A_2203) - Fase 4 (RAC3)
"""

from abc import ABC, abstractmethod


# ===========================================================================
# CLASE ABSTRACTA BASE (entidades generales del sistema)
# ===========================================================================
class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad del sistema.

    Aporta un identificador comun y obliga a las subclases a implementar el
    metodo describir(), base del comportamiento polimorfico.
    """

    def __init__(self, identificador):
        self._identificador = identificador   # Atributo protegido (encapsulacion).

    @property
    def identificador(self):
        """Identificador de solo lectura."""
        return self._identificador

    @abstractmethod
    def describir(self):
        """Metodo abstracto que cada entidad concreta debe implementar."""
        raise NotImplementedError

    def __str__(self):
        return self.describir()


# ===========================================================================
# CLASE CLIENTE (encapsulacion de datos personales)
# ===========================================================================
class Cliente(EntidadBase):
    """Representa a un cliente con sus datos personales encapsulados."""

    def __init__(self, identificador, nombre, documento, email):
        super().__init__(identificador)
        # Datos personales privados (encapsulacion).
        self._nombre = nombre
        self._documento = documento
        self._email = email

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
# CLASE ABSTRACTA SERVICIO + TRES SERVICIOS ESPECIALIZADOS
# ===========================================================================
class Servicio(EntidadBase):
    """Clase abstracta que define el contrato comun de todos los servicios.

    Cada servicio concreto implementa calcular_costo(), describir() y
    validar_parametros(), demostrando herencia y polimorfismo.
    """

    IVA_POR_DEFECTO = 0.19   # Impuesto por defecto aplicado a los costos.

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible

    @property
    def disponible(self):
        return self._disponible

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def validar_parametros(self):
        """Valida los parametros propios del servicio."""
        raise NotImplementedError

    @abstractmethod
    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        """Metodo sobrecargado: acepta parametros opcionales de impuesto/descuento."""
        raise NotImplementedError

    def _aplicar_impuesto_y_descuento(self, subtotal, impuesto, descuento):
        """Aplica descuento e impuesto. Los parametros opcionales permiten la
        sobrecarga del calculo de costos (con o sin impuesto/descuento)."""
        if impuesto is None:
            impuesto = self.IVA_POR_DEFECTO
        if descuento is None:
            descuento = 0.0
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio de reserva de salas (la cantidad representa horas)."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        self._capacidad = capacidad

    def validar_parametros(self):
        # En el paquete 1 la validacion es una simple comprobacion booleana.
        return self._tarifa_base > 0 and self._capacidad > 0

    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        subtotal = self._tarifa_base * cantidad
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (f"Sala '{self._nombre}' (cap. {self._capacidad}) - "
                f"${self._tarifa_base:,.0f}/hora")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (la cantidad representa dias)."""

    def __init__(self, identificador, nombre, tarifa_dia, tipo_equipo,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_dia, disponible)
        self._tipo_equipo = tipo_equipo

    def validar_parametros(self):
        return self._tarifa_base > 0 and bool(str(self._tipo_equipo).strip())

    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        subtotal = self._tarifa_base * cantidad
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (f"Equipo '{self._nombre}' ({self._tipo_equipo}) - "
                f"${self._tarifa_base:,.0f}/dia")


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria especializada (la cantidad representa horas)."""

    def __init__(self, identificador, nombre, tarifa_hora, area,
                 recargo_experto=0.15, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        self._area = area
        self._recargo_experto = recargo_experto

    def validar_parametros(self):
        return self._tarifa_base > 0 and self._recargo_experto >= 0

    def calcular_costo(self, cantidad, impuesto=None, descuento=None):
        # El recargo por experticia se suma a la tarifa base.
        subtotal = self._tarifa_base * (1 + self._recargo_experto) * cantidad
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self):
        return (f"Asesoria '{self._nombre}' (area {self._area}) - "
                f"${self._tarifa_base:,.0f}/hora + {self._recargo_experto:.0%} experto")


# ===========================================================================
# CLASE RESERVA (integra cliente, servicio, duracion y estado)
# ===========================================================================
class Reserva(EntidadBase):
    """Reserva que vincula un cliente con un servicio por una duracion dada."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = self.PENDIENTE
        self._costo_total = None

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        """Confirma la reserva (cambia el estado a CONFIRMADA)."""
        self._estado = self.CONFIRMADA

    def cancelar(self):
        """Cancela la reserva (cambia el estado a CANCELADA)."""
        self._estado = self.CANCELADA

    def procesar(self, impuesto=None, descuento=None):
        """Procesa la reserva calculando su costo mediante el servicio."""
        self._costo_total = self._servicio.calcular_costo(
            self._duracion, impuesto, descuento)
        self._estado = self.PROCESADA
        return self._costo_total

    def describir(self):
        return (f"Reserva #{self._identificador} | {self._cliente.nombre} -> "
                f"{self._servicio.nombre} | {self._duracion}h | {self._estado}")


# ===========================================================================
# GESTOR CENTRAL (listas internas)
# ===========================================================================
class GestorSoftwareFJ:
    """Administra las listas internas de clientes, servicios y reservas."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    def registrar_cliente(self, cliente):
        self._clientes.append(cliente)
        return cliente

    def registrar_servicio(self, servicio):
        self._servicios.append(servicio)
        return servicio

    def registrar_reserva(self, reserva):
        self._reservas.append(reserva)
        return reserva

    def resumen(self):
        return {"clientes": len(self._clientes),
                "servicios": len(self._servicios),
                "reservas": len(self._reservas)}


# ===========================================================================
# DEMOSTRACION DE LA ESTRUCTURA
# ===========================================================================
def main():
    """Crea una instancia de cada clase para evidenciar la estructura y el
    polimorfismo. El manejo de excepciones se implementa en el paquete 2."""
    print("PAQUETE 1 - Estructura de clases del sistema 'Software FJ'\n")
    gestor = GestorSoftwareFJ()

    cliente = gestor.registrar_cliente(
        Cliente(1, "Ana Gomez", "1090234567", "ana@softwarefj.com"))
    sala = gestor.registrar_servicio(ReservaSala(10, "Sala Innovacion", 50000, 12))
    equipo = gestor.registrar_servicio(AlquilerEquipo(11, "Videobeam 4K", 30000, "Proyector"))
    asesoria = gestor.registrar_servicio(
        AsesoriaEspecializada(12, "Asesoria Cloud", 80000, "DevOps"))

    # Polimorfismo: el mismo metodo describir() responde distinto por clase.
    for entidad in (cliente, sala, equipo, asesoria):
        print(" -", entidad.describir())

    # Reserva de ejemplo confirmada y procesada.
    reserva = gestor.registrar_reserva(Reserva(100, cliente, sala, 3))
    reserva.confirmar()
    costo = reserva.procesar()
    print("\n", reserva.describir(), "| Costo:", costo)
    print("\nResumen:", gestor.resumen())


if __name__ == "__main__":
    main()
