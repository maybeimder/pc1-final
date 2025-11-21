# worker.py

import socket
import threading
from m_video_splitter import divide_video

class Worker:
    def __init__(self, name:str, ip:str, port:int=5050, tasks:list | None = None ):
        self.name = name
        self.ip = ip
        self.port = port
        self.tasks = tasks or []
    

    def handle_connection(self, connection:socket.socket, address):
        # Manejador de comunicación con el main
        message = connection.recv(2048).decode()

        if "Task" in message:
            payload = message.replace(" Task:", "", 1)

            try:
                output_folder, csv_paths = payload.split("|", 1)
            except ValueError:
                print(f"[{self.name}] Formato de mensaje inválido: {message}")
                connection.close()
                return

            video_paths = [p.strip() for p in csv_paths.split(",") if p.strip()]

            for path in video_paths:
                print(f"[{self.name}] empezó a procesar {path}")
                divide_video( 10, path, output_folder )

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


        
