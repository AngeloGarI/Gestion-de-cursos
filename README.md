📚 Sistema de Gestión de cursos

Este proyecto implementa un sistema académico en Python, dividido por módulos según cada integrante del equipo:

Integrante 1 – Módulo de Usuarios y Cursos

Integrante 2 – Módulo de Evaluaciones y Reportes

🧑‍💻 Integrante 1 – Módulo de Usuarios y Cursos
✔️ Análisis y diseño

Clases base: Usuario, Estudiante, Instructor.

Herencia entre usuarios.

Clase Curso con atributos: nombre, código, instructor.

Funciones para inscripción de estudiantes a cursos.

Manejo de errores:

Inscripción repetida.

Instructor inexistente.

Uso de *args y **kwargs en constructores.

📌 Desarrollo

Encapsulamiento y validaciones en los atributos.

Inscripción de estudiantes a cursos.

Ejemplo de uso incluido.

📝 Integrante 2 – Módulo de Evaluaciones y Reportes
✔️ Análisis y diseño

Clase abstracta Evaluacion.

Clases hijas: Examen, Tarea (polimorfismo).

Métodos principales:

Registrar calificaciones.

Calcular promedios.

Alertar estudiantes con bajo rendimiento.

📌 Desarrollo

Registro de calificaciones con validaciones (curso válido, nota en rango).

Reportes generados desde los datos del curso.

Uso de diccionarios para almacenar evaluaciones y notas.

🚀 Ejemplo de uso
inst = Instructor(1, "María", "maria@mail.com", "Ingeniera en Sistemas")
curso_python = inst.crear_curso("C001", "Python Básico")

est1 = Estudiante(101, "Ana", "ana@mail.com", "A123")
est2 = Estudiante(102, "Juan", "juan@mail.com", "J456")

curso_python.inscribir_estudiante(est1)
curso_python.inscribir_estudiante(est2)

# Crear evaluaciones
ex1 = crear_evaluacion("Examen", "Parcial1", curso_python, 100)
tarea1 = crear_evaluacion("Tarea", "Tarea1", curso_python, 20)

# Registrar notas
ex1.registrar_nota(est1, 85)
ex1.registrar_nota(est2, 75)
tarea1.registrar_nota(est1, 15)
tarea1.registrar_nota(est2, 10)

# Reportes
reporte_promedios(curso_python)
alerta_bajo_rendimiento(curso_python, umbral=60)

🖥️ Ejemplo de salida en consola
Curso creado: Python Básico (Código: C001)
Estudiantes inscritos:
- Ana (ana@mail.com)
- Juan (juan@mail.com)

Evaluaciones creadas:
- Examen: Parcial1 (Máx: 100)
- Tarea: Tarea1 (Máx: 20)

Notas registradas:
Ana → Parcial1 = 85
Ana → Tarea1 = 15
Juan → Parcial1 = 75
Juan → Tarea1 = 10

Reporte de promedios del curso: Python Básico
Ana: 50.00
Juan: 42.50

Alerta estudiantes con promedio bajo (60) en Python Básico
Ana: 50.00
Juan: 42.50

📂 Estructura del repositorio
proyecto_academico/
│── usuarios_cursos.py    # Código del módulo de Persona 1
│── evaluaciones.py       # Código del módulo de Persona 2
│── main.py               # Ejemplo de integración
│── README.md             # Documentación

👥 Autores

Sarai Montejo: Usuario y Cursos

Angelo García: Evaluaciones y Reportes, registrar nota para estudiante no inscrito → debe lanzar error.