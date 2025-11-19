# server.py

import socket
import threading
from worker import Worker

class Server:
    def __init__(self, workers:dict, videos:list, output_folder:str ):
        self.workers = workers
        self.workers_tasks = []
        self.video_paths = videos
        self.output_folder = output_folder


    def split_tasks(self):
        # Basado en el numero de workers, hallar la relación directa
        num_workers = len(self.workers)
        num_videos = len(self.video_paths)

        if num_workers == 0: raise ValueError("No hay trabajadores definidos")

        if num_videos == 0:
            self.workers_tasks = [[] for _ in range(num_workers)]
            return

        # Calcular el numero optimo de divisiones simultaneas
        import math
        split_range = math.ceil(num_videos / num_workers)

        self.workers_tasks = [self.video_paths[i:i + split_range] for i in range(0, num_videos, split_range)]


    def manage_worker(self, worker:Worker ):
        print(f"[M]: Conexión establecida con {worker.name}")

        try:
            # Crear un socket donde alojar al worker
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((worker.ip, worker.port))

            # Asignarle su tareita, testar la conexion con un string
            message = f" Task:{self.output_folder}|{",".join(worker.tasks)}"
            sock.send(message.encode())

            # Esperar a respuesta
            res = sock.recv(1024).decode()

            if res.startswith("DONE"): print(f"[M]: {worker.name} terminó sus tareas") 
            sock.close()
        
        except Exception as e:
            print(f"[M]: [ERROR] {worker.name} tuvo un error inesperado", e)
    

    def threader(self):
        # Iniciar listado de threads
        threads : list[threading.Thread] = []

        # Por cada trabajador con su task generarle un hilo
        for worker, task in zip(self.workers.values(), self.workers_tasks):
            worker.tasks = task 
            print(f"[M]: Cargadas las tasks del {worker.name}: {worker.tasks}")
            thread = threading.Thread(
                target= self.manage_worker,
                args=(worker,)
            )

            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print("[M]: Todos los worker terminaron")
    

    def start(self):
        # Generar las particiones 
        self.split_tasks()
        self.threader()


            
