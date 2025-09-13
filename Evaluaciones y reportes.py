from abc import ABC, abstractmethod
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
    prof = Profesor(1, "Luis", "luis@mail.com", "Ingeniero")
    curso_python = prof.crear_curso("C001", "Progra avanzada")

    est1 = Estudiante (101, "Ana", "ana@mail.com", "A123")
    est2 = Estudiante(102, "Juan", "juan@mail.com", "J456")

    curso_python.inscribir_estudiante(est1)
    curso_python.inscribir_estudiante(est2)

    #Crear evalu
    ex1 = crear_evaluacion("Examen", "Parcial1", curso_python, 100)
    tarea1 = crear_evaluacion("Tarea", "Tarea1", curso_python, 20)

    ex1.registrar_nota( est1, 85)
    ex1.registrar_nota(est2, 75)
    tarea1.registrar_nota(est1, 15)
    tarea1.registrar_nota(est2, 10)

    #reportes
    reporte_promedios(curso_python)
    alerta_bajo_rendimiento(curso_python, umbral = 80)