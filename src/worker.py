# worker.py

import socket
import threading
from m_video_splitter import divide_video
import worker_handler as wh

class Worker:
    def __init__(self, name:str, ip:str, port:int=5050, tasks:list | None = None ):
        self.name = name
        self.ip = ip
        self.port = port
        self.tasks = tasks or []
    

    def handle_connection(self, connection:socket.socket, address):
        # Manejador de comunicación con el main
        message = connection.recv(2048).decode().strip()

        if message.startswith("SPLIT"): wh.handle_split_task(self.name, message);
        elif message.startswith("COLLAGE"): wh.handle_collage_task(self.name, message);
        else:
            connection.close()
            return

        connection.send(b"DONE")
        connection.close()
    

    def start(self):
        # Crear el socker (TCP) alojador para este worker
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", self.port))
        sock.listen(5)

        print(f"[{self.name}] Listo en el puerto {self.port}")

        while True:
            connection, address = sock.accept()
            print(f"[{self.name}] Conectado desde {address}")
            thread = threading.Thread( target=self.handle_connection, args=(connection, address))
            thread.start()



# Leer argumentos desde ejecucion
if __name__ == "__main__":
    import sys
    from listener import register_with_main_udp

    name = sys.argv[1]
    ip = sys.argv[2]
    port = int(sys.argv[3])

    register_with_main_udp (
        name=name,
        ip=ip,
        port=port,
        main_ip="10.0.0.35",   
        main_port=6000
    )

    worker = Worker(name, ip, port)
    worker.start()


        
