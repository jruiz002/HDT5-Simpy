import simpy
import random
import csv

# Variables de clase
env = simpy.Environment() # Se levanta un ambiente environment
cpu = simpy.Resource(env, capacity=1)  # Un solo CPU con capacidad de ejecutar un proceso a la vez.
RAM = simpy.Container(env, init=100, capacity=100) # Creación de la RAM
random.seed(42)
INTERVAL = 10 # Intervalo
lista_procesos = [] # Se inicializa la lista para almacenar los procesos

class Proceso:
    def __init__(self, id, ramToUse, numberInstructions):
        self.id = id
        self.ramToUse = ramToUse
        self.numberInstructions = numberInstructions
        self.startTime = 0
        self.endTime = 0

def inicioPrograma(numberProcess):
    for i in range(numberProcess):
        env.process(creacionProceso(i))
    env.run()

def creacionProceso(id):
    # Primera Etapa y new: Se crea el proceso se agregan al entorno de simpy y se asignan sus parámetros
    # Se modela la creación de procesos con una distribución exponencial.
    yield env.timeout(random.expovariate(1.0 / INTERVAL))
    proceso = Proceso(id, random.randint(1, 10), random.randint(1, 10))
    proceso.startTime = env.now
    print(f'Proceso {proceso.id} está creado con {proceso.numberInstructions} intruccione(s) en el tiempo: {proceso.startTime}')
    yield from new(proceso)

def new(proceso):
    with RAM.get(proceso.ramToUse) as req:
        yield req
        RAM.get(proceso.ramToUse)
        while proceso.numberInstructions > 0:
            yield from ready(proceso)
            numberAleatory = random.randint(1,2)
            if(numberAleatory == 1):
                yield env.timeout(2)
        RAM.put(proceso.ramToUse)
            
def ready(proceso):
    with cpu.request() as req:
        yield req  # Esperar que el CPU este disponible
        yield from running(proceso)

def running(proceso):
    yield env.timeout(1)
    proceso.numberInstructions -=  3
    
    if (proceso.numberInstructions <= 0):
        proceso.numberInstructions = 0
        proceso.endTime = env.now
        print(f'Proceso {proceso.id} ha terminado en el tiempo: {proceso.endTime} con {proceso.numberInstructions} intruccione(s)')
        lista_procesos.append(proceso)

def saveDataCSV():
    # Al finalizar el programa, escribir la lista de objetos en un archivo CSV
    with open('procesos.csv', mode='w', newline='') as file:
        fieldnames = ['id', 'startTime', 'endTime']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Escribir encabezados
        writer.writeheader()

        lista_objetos_ordenada = sorted(lista_procesos, key=lambda x: x.id)

        # Escribir cada objeto en la lista en una nueva fila del CSV
        for proceso in lista_objetos_ordenada:
            writer.writerow({'id': proceso.id, 'startTime': proceso.startTime, 'endTime': proceso.endTime})