# listener.py
import socket

# Escucha registros de workers
# Codigo de chat, ni idea
def listen_for_workers_udp(main_port, expected_workers, worker_factory):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", main_port))

    print(f"[M] Esperando registro de {expected_workers} workers en puerto UDP {main_port}...")

    workers = {}

    while len(workers) < expected_workers:
        data, addr = sock.recvfrom(1024)
        msg = data.decode()

        if not msg.startswith("REGISTER:"):
            print(f"[M]: Mensaje inválido recibido: {msg}")
            continue

        payload = msg.replace("REGISTER:", "", 1)
        try:
            name, ip, port = payload.split("|")
            port = int(port)
        except ValueError:
            print(f"[M]: Error al parsear registro: {msg}")
            continue

        print(f"[M]: Worker registrado: {name} {ip}:{port}")

        workers[name] = worker_factory(name, ip, port)

    sock.close()
    return workers


# WORKER: envía registro al MAIN
def register_with_main_udp(name, ip, port, main_ip, main_port):
    """
    Envía un mensaje UDP de registro al MAIN:
        REGISTER:name|ip|port
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = f"REGISTER:{name}|{ip}|{port}"

    sock.sendto(msg.encode(), (main_ip, main_port))
    sock.close()

    print(f"[{name}] Enviado registro al MAIN {main_ip}:{main_port}")
