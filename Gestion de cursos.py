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

    def __str__(self):
        return f"Curso: {self.nombre} (Código: {self.codigo})"
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

    # Ejemplo de uso
if __name__ == "__main__":
    inst = Instructor(1, "María", "maria@mail.com", "Ingeniera en Sistemas")
    curso_python = inst.crear_curso("C001", "Python Básico")

    est1 = Estudiante(101, "Ana", "ana@mail.com", "A123")
    est2 = Estudiante(102, "Juan", "juan@mail.com", "J456")
    try:
        curso_python.inscribir_estudiante(est1)
        curso_python.inscribir_estudiante(est2)
        curso_python.inscribir_estudiante(est1)
    except ValueError as e:
        print(e)

    print(curso_python)
    for est in curso_python.estudiantes:
        print(f"- {est.nombre} ({est.email})")

    # Crear evaluaciones
    ex1 = crear_evaluacion("Examen", "Parcial1", curso_python, 100)
    tarea1 = crear_evaluacion("Tarea", "Tarea1", curso_python, 20)

    # Guardar evaluaciones en el curso
    curso_python.evaluaciones.append(ex1)
    curso_python.evaluaciones.append(tarea1)

    print("\nEvaluaciones creadas:")
    print(f"- {ex1.tipo()}: {ex1.nombre} (Máx: {ex1.puntaje_maximo})")
    print(f"- {tarea1.tipo()}: {tarea1.nombre} (Máx: {tarea1.puntaje_maximo})")

    # Registrar notas
    ex1.registrar_nota(est1, 100)
    ex1.registrar_nota(est2, 75)
    tarea1.registrar_nota(est1, 20)
    tarea1.registrar_nota(est2, 10)

    print("\nNotas registradas:")
    for ev in [ex1, tarea1]:
        for est, nota in ev.notas.items():
            print(f"{est.nombre}, {ev.nombre} = {nota}")

    print()
    reporte_promedios(curso_python)
    alerta_bajo_rendimiento(curso_python, umbral=60)