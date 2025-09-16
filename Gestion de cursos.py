from abc import ABC, abstractmethod

class Usuario:
    def __init__(self, id, nombre, email, *args, **kwargs):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if "@" not in email:
            raise ValueError("El email no es válido")
        self._id = id
        self._nombre = nombre
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def email(self):
        return self._email

    def __str__(self):
        return f"{self._nombre} ({self._email})"


class Estudiante(Usuario):
    def __init__(self, id, nombre, email, carnet, *args, **kwargs):
        super().__init__(id, nombre, email, *args, **kwargs)
        self._carnet = carnet
        self.cursos_inscritos = []
        self.calificaciones = {}

    def inscribir_curso(self, curso):
        if curso not in self.cursos_inscritos:
            self.cursos_inscritos.append(curso)
        else:
            raise ValueError(f"{self.nombre} ya está inscrito en {curso.nombre}")

    def obtener_promedio(self, curso_id = None):
        if curso_id:
            if curso_id in self.calificaciones and self.calificaciones[curso_id]:
                califs = self.calificaciones[curso_id].values()
                return sum(califs) / len(califs)
            return 0
        else:
            # Promedio general de todos los cursos
            promedios = []
            for curso_id, evaluaciones in self.calificaciones.items():
                if evaluaciones:
                    promedios.append(sum(evaluaciones.values()) / len(evaluaciones))
            return sum(promedios) / len(promedios) if promedios else 0

    def obtener_promedio_curso(self, curso_id):
        if curso_id in self.calificaciones and self.calificaciones[curso_id]:
            califs = self.calificaciones[curso_id].values()
            return sum(califs) / len(califs)
        return 0

class Instructor(Usuario):
    def __init__(self, id, nombre, email, profesion, *args, **kwargs):
        super().__init__(id, nombre, email, *args, **kwargs)
        self._profesion = profesion
        self.cursos = []

    def crear_curso(self, codigo, nombre):
        curso = Curso(codigo, nombre, self)
        self.cursos.append(curso)
        return curso


class Curso:
    def __init__(self, codigo, nombre, instructor, *args, **kwargs):
        if not isinstance(instructor, Instructor):
            raise TypeError("El instructor debe ser de tipo Instructor")
        self.codigo = codigo
        self.nombre = nombre
        self.instructor = instructor
        self.estudiantes = []
        self.evaluaciones = []

    def inscribir_estudiante(self, estudiante):
        if not isinstance(estudiante, Estudiante):
            raise TypeError("Solo se pueden inscribir estudiantes")
        if estudiante in self.estudiantes:
            raise ValueError(f"El estudiante {estudiante.nombre} ya está inscrito")
        self.estudiantes.append(estudiante)
        estudiante.inscribir_curso(self)

    def mostrar_estudiantes(self):
        if not self.estudiantes:
            print("No hay estudiantes inscritos.")
        else:
            print(f"Estudiantes en {self.nombre}:")
            for est in self.estudiantes:
                print(f" - {est}")

    def mostrar_evaluaciones(self):
        if not self.evaluaciones:
            print("No hay evaluaciones creadas.")
        else:
            for ev in self.evaluaciones:
                print(f" - {ev.nombre} ({ev.tipo()}) - Máx: {ev.puntaje_maximo}")

    def __str__(self):
        return f"Curso: {self.nombre} (Código: {self.codigo}) | Instructor: {self.instructor.nombre}"


# persona 2
class Evaluacion(ABC):
    def __init__(self, nombre, curso, puntaje_maximo):
        self.nombre = nombre
        self.curso = curso
        self.puntaje_maximo = puntaje_maximo
        self.notas = {}

    @abstractmethod
    def tipo(self):
        pass

    def registrar_nota(self, estudiante, nota):
        if estudiante not in self.curso.estudiantes:
            raise ValueError (f"Estudiante {estudiante.nombre} no inscrito "
                              f"en el curso {self.curso.nombre}")
        if nota < 0 or nota > self.puntaje_maximo:
            raise ValueError(f"Nota invalida: {nota}")
        self.notas[estudiante] = nota
        if self.curso.codigo not in estudiante.calificaciones:
            estudiante.calificaciones[self.curso.codigo] = {}
        estudiante.calificaciones[self.curso.codigo][self.nombre] = nota

    def obtener_promedio_curso(self):
        if self.notas:
            return sum(self.notas.values())/len(self.notas)
        return 0

# polimorfismo
class Examen(Evaluacion):
    def tipo(self):
        return "Examen"

class Tarea(Evaluacion):
    def tipo(self):
        return "Tarea"

#funcion de evalua
def crear_evaluacion(tipo, nombre, curso, puntaje_maximo):
    if tipo.lower() == "examen":
        return Examen(nombre, curso, puntaje_maximo)
    elif tipo.lower() == "tarea":
        return Tarea(nombre, curso, puntaje_maximo)
    else:
        raise ValueError(f"Tipo de evaluación invalida")

def reporte_promedios(curso):
    print(f"Reporte de promedios del curso: {curso.nombre}")
    for estudiante in curso.estudiantes:
        promedio = estudiante.obtener_promedio_curso(curso.codigo)
        print(f"{estudiante.nombre}: {promedio:.2f}")

def alerta_bajo_rendimiento(curso, umbral = 60):
    print(f"Alerta estudiantes con promedio bajo ({umbral}) en {curso.nombre}")
    for estudiante in curso.estudiantes:
        promedio = estudiante.obtener_promedio(curso.codigo)
        if promedio < umbral:
            print(f"{estudiante.nombre}: {promedio:.2f}")

 # ================== MENÚ PRINCIPAL ==================
def menu():
    cursos = {}  # Diccionario para manejar múltiples cursos

    while True:
        print("\n=== Menú Principal ===")
        print("1. Crear curso")
        print("2. Inscribir estudiante en curso")
        print("3. Crear evaluación en curso")
        print("4. Registrar calificación")
        print("5. Consultar cursos y detalles")
        print("6. Generar reportes")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            codigo = input("Código del curso: ")
            nombre_curso = input("Nombre del curso: ")

            print("\n--- Datos del Instructor ---")
            id_inst = input("ID del instructor: ")
            nombre_inst = input("Nombre: ")
            email_inst = input("Email: ")
            profesion = input("Profesión: ")

            try:
                instructor = Instructor(id_inst, nombre_inst, email_inst, profesion)
                curso = Curso(codigo, nombre_curso, instructor)
                cursos[codigo] = curso
                print(f"\nCurso '{nombre_curso}' creado con éxito.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "2":
            codigo = input("Código del curso: ")
            if codigo not in cursos:
                print("Curso no encontrado.")
            else:
                curso = cursos[codigo]
                id_est = input("ID del estudiante: ")
                nombre = input("Nombre: ")
                email = input("Email: ")
                carnet = input("Carnet: ")
                try:
                    estudiante = Estudiante(id_est, nombre, email, carnet)
                    curso.inscribir_estudiante(estudiante)
                    print(f"Estudiante {nombre} inscrito en {curso.nombre}.")
                except Exception as e:
                    print(f"Error: {e}")

        elif opcion == "3":
            codigo = input("Código del curso: ")
            if codigo not in cursos:
                print("Curso no encontrado.")
            else:
                curso = cursos[codigo]
                nombre_ev = input("Nombre de la evaluación: ")
                tipo = input("Tipo (examen/tarea): ")
                puntaje = int(input("Puntaje máximo: "))
                try:
                    ev = crear_evaluacion(tipo, nombre_ev, curso, puntaje)
                    curso.evaluaciones.append(ev)
                    print(f"Evaluación '{nombre_ev}' creada en {curso.nombre}.")
                except Exception as e:
                    print(f"Error: {e}")

        elif opcion == "4":
            codigo = input("Código del curso: ")
            if codigo not in cursos:
                print("Curso no encontrado.")
            else:
                curso = cursos[codigo]
                curso.mostrar_evaluaciones()
                nombre_ev = input("Nombre de la evaluación: ")
                evaluacion = next((ev for ev in curso.evaluaciones if ev.nombre == nombre_ev), None)
                if evaluacion is None:
                    print("Evaluación no encontrada.")
                else:
                    curso.mostrar_estudiantes()
                    id_est = input("ID del estudiante: ")
                    estudiante = next((est for est in curso.estudiantes if est.id == id_est), None)
                    if estudiante is None:
                        print("Estudiante no encontrado.")
                    else:
                        nota = float(input("Ingrese la nota: "))
                        try:
                            evaluacion.registrar_nota(estudiante, nota)
                            print("Nota registrada con éxito.")
                        except Exception as e:
                            print(f"Error: {e}")

        elif opcion == "5":
            print("\nCursos disponibles:")
            for curso in cursos.values():
                print(curso)
                print(curso.mostrar_estudiantes())
                curso.mostrar_evaluaciones()

        elif opcion == "6":
            codigo = input("Código del curso: ")
            if codigo not in cursos:
                print("Curso no encontrado.")
            else:
                curso = cursos[codigo]
                reporte_promedios(curso)
                alerta_bajo_rendimiento(curso)

        elif opcion == "7":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()