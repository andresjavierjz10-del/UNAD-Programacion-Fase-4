# Sistema de Gestión de Reservas "Software FJ" 🏢

Proyecto de la **Fase 4 (RAC3)** del curso de **Programación (213023A_2203)** de la
UNAD. Implementa un sistema orientado a objetos con **manejo avanzado de
excepciones**, sin base de datos, para gestionar clientes, servicios y reservas.

> **Objetivo:** construir una aplicación estable, modular y extensible que aplique
> abstracción, herencia, polimorfismo, encapsulación y manejo robusto de errores,
> garantizando que el sistema siga funcionando aun cuando ocurran fallos.

- **Curso:** Programación (213023A_2203)
- **Grupo:** 213023_15
- **Universidad:** Universidad Nacional Abierta y a Distancia (UNAD)
- **Año:** 2026

---

## 📦 Estructura del repositorio

El proyecto está organizado en **tres paquetes progresivos**:

| Paquete | Archivo | Descripción |
|---------|---------|-------------|
| **1. Estructura** | `sistema_integral_orientado_objetos.py` | Estructura de clases y métodos (clase abstracta base, `Cliente`, `Servicio` y sus 3 servicios, `Reserva`, gestor central). |
| **2. Excepciones** | `sistema_integral_orientado_objetos.py` | Agrega excepciones personalizadas, logging y los patrones `try/except`, `try/except/else`, `try/except/finally` y encadenamiento. |
| **3. Completo** | `sistema_integral_orientado_objetos.py` | Integra todo y ejecuta una simulación de **18 operaciones** (válidas e inválidas). |

Otros archivos:
- `Documento_Fase4_Manejo_Excepciones.docx` — Documento en Word (normas APA).
- `software_fj_eventos.log` — Archivo de logs generado por el paquete 3.

---

## ▶️ Cómo ejecutar

Requiere **Python 3** (no usa librerías externas ni base de datos):

```bash
# Paquete 1 - demostración de la estructura de clases
python3 sistema_integral_orientado_objetos.py con paquete1 estructura

# Paquete 2 - demostración del manejo de excepciones
python3 sistema_integral_orientado_objetos.py con paquete2 excepciones

# Paquete 3 - sistema completo con la simulación de 18 operaciones
python3 sistema_integral_orientado_objetos.py con paquete3 sistema completo(Aca podemos interactuar todos por commit's)
```

Al ejecutar el paquete 3 se genera/actualiza el archivo `software_fj_eventos.log`
con todos los eventos y errores registrados.

---

## 👥 Equipo de trabajo y asignación de tareas

Cada integrante tiene **como mínimo 3 tareas**. Marca `[x]` cuando completes una
tarea para reflejar el avance directamente en este README.

### 🧑‍💻 Integrante 1 — Juan Carlos Orozco Navarro *(Desarrollador 1)*
- [OK] **T1.1** Definir la arquitectura y la estructura de los 3 paquetes del proyecto.
- [] **T1.2** Integrar el paquete 3 (sistema completo) y la simulación de 10+ operaciones.
- [OK] **T1.3** Configurar el repositorio GitHub: ramas, `README.md` y control de versiones.

### 🧑‍💻 Integrante 2 — Santiago Pachon Moreno *(Modelo de dominio - Paquete 1)*
- [OK] **T2.1** Implementar la clase abstracta `EntidadBase` y la clase `Cliente` con validaciones y encapsulación.
- [OK] **T2.2** Implementar la clase abstracta `Servicio` (contrato común de los servicios).
- [OK] **T2.3** Documentar en español (comentarios y docstrings) todas las clases del paquete 1.

### 🧑‍💻 Integrante 3 — *[Desarrollador 3]* *(Herencia y polimorfismo)*
- [ ] **T3.1** Implementar los 3 servicios: `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`.
- [ ] **T3.2** Implementar los métodos sobrecargados de cálculo de costos (impuestos, descuentos y parámetros opcionales).
- [ ] **T3.3** Probar el polimorfismo de `describir()` y `calcular_costo()` en los tres servicios.

### 🧑‍💻 Integrante 4 — *[Desarrollador 4]* *(Excepciones y logging - Paquete 2)*
- [ ] **T4.1** Diseñar la jerarquía de excepciones personalizadas (`SoftwareFJError` y derivadas).
- [ ] **T4.2** Implementar `try/except`, `try/except/else`, `try/except/finally` y el encadenamiento (`raise ... from`).
- [ ] **T4.3** Configurar el archivo de logs y registrar todos los eventos y errores.

### 🧑‍💻 Integrante 5 — *[Desarrollador 5]* *(Reserva, simulación y documento)*
- [ ] **T5.1** Implementar la clase `Reserva` (estados, `confirmar`, `cancelar`, `procesar`).
- [ ] **T5.2** Diseñar y ejecutar la simulación de 10+ operaciones (válidas e inválidas).
- [ ] **T5.3** Elaborar el documento Word con normas APA (portada, introducción, conclusiones y referencias).

---

## 📊 Tablero de avances

Actualiza el **estado** y el **% de avance** de cada tarea. Estados sugeridos:
`⬜ Pendiente` · `🟨 En progreso` · `✅ Completada`.

| Tarea | Responsable | Estado | Avance |
|-------|-------------|--------|--------|
| T1.1 | Juan Carlos Orozco | ✅ Completada | 100% |
| T1.2 | Juan Carlos Orozco | ✅ Completada | 100% |
| T1.3 | Juan Carlos Orozco | ✅ Completada | 100% |
| T2.1 | Santiago Pachon Moreno | ✅ Completada| 100% |
| T2.2 | Santiago Pachon Moreno | ✅ Completada| 100% |
| T2.3 | Santiago Pachon Moreno | ✅ Completada | 100% |
| T3.1 | [Juan Carlos Orozco] | ✅ Completada | 90% |
| T3.2 | [Juan Carlos Orozco] | ✅ Completada | 90% |
| T3.3 | [Juan Carlos Orozco] | ✅ Completada | 90% |
| T4.1 | [Juan Carlos Orozco] | ✅ Completada | 90% |
| T4.2 | [Juan Carlos Orozco] | ✅ Completada | 90% |
| T4.3 | [Juan Carlos Orozco] | ✅ Completada | 90% |
| T5.1 | [Juan Carlos Orozco] | ✅ Completada | 90% |
| T5.2 | [Juan Carlos Orozco] | ✅ Completada | 90% |
| T5.3 | [Juan Carlos Orozco] | ✅ Completada | 90% |
| T6.1 | Andres Javier Uribe Jimenez | ✅ Completada | 100% |
**Avance global del proyecto:** `13 / 15 tareas completadas (80%)`

---

## 📝 Bitácora de avances

Registrar aquí cada avance con fecha, integrante y descripción (lo más reciente arriba).

| Fecha | Integrante | Avance realizado |
|-------|------------|------------------|
| 2026-07-17 | Juan Carlos Orozco | Estructura inicial del repositorio y los 3 paquetes creada. |
| 2026-07-22 | Santiago Pachon Moreno | Acceso al proyecto, validación del mismo, análisis y creación de la clase abstracta EntidadBase |
| 2026-07-22 | Juan Carlos Orozco |  Jerarquia de excepciones personalizadas segun la logica del negocio. |
| 2026-07-23 | Juan Carlos Orozco |  Unificacion de codigo, simulacion final de operaciones. |
| 2026-07-24 | Santiago Pachon Moreno | Detalles finalizados junto con explicación en clase abstracta EntidadBase, clase Cliente, clase abstracta Servicio |
| _2026-07-26_ | Andres Javier Uribe Jimenez | crear el menu y resto del codigo implementado tkinter |

---

## 🌿 Convenciones de Git (trabajo colaborativo)

Para mantener el orden y la trazabilidad del trabajo en equipo:

- **Rama principal:** `main` (código estable).
- **Ramas de trabajo:** una por integrante o por tarea, p. ej. `feature/integrante-v01`.
- **Mensajes de commit** claros y en español, referenciando la tarea:
  ```
  git commit -m "T4.1: agrega jerarquia de excepciones personalizadas"
  ```
- Integrar cambios mediante **Pull Requests** revisados por al menos otro compañero.
- Cada integrante actualiza su **checklist** y el **tablero de avances** al terminar una tarea.

---

*Elaborado por el Grupo 213023_15 — UNAD, 2026.*
