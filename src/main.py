# main.py

import os
import sys
from server import Server
from worker import Worker
from listener import listen_for_workers_udp

def print_video_list(video_paths):
    GREEN = "\033[92m"
    RESET = "\033[0m"

    print("[")
    for v in video_paths:
        # Extrae solo el nombre de archivo
        name = os.path.basename(v)

        print(f'    "{GREEN}{name}{RESET}",')
    print("]")

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Uso: python3 main.py <input_folder> <output_folder>")
        sys.exit(1)
    
    input_folder = os.path.expanduser(sys.argv[1])
    output_folder = os.path.expanduser(sys.argv[2])

    if not os.path.isdir(input_folder):
        print(f"[MAIN] Carpeta de entrada no existe: {input_folder}")
        sys.exit(1)

    # Lista de videos en la carpeta de inputs
    video_files = [
        f for f in os.listdir(input_folder)
        if f.endswith((".mp4", ".mov"))
    ]

    # Lista de rutas
    video_paths = [
        os.path.join(input_folder, f)
        for f in video_files
    ]

    print(f"[MAIN] Videos detectados:")
    print_video_list(video_paths)
    
    workers = listen_for_workers_udp (
        main_port= 6000,
        expected_workers=4,
        worker_factory= lambda name,ip,port: Worker(name, ip, port)
    )

    # [1] Fragmentador de videos
    frag_server = Server(workers, video_paths, output_folder)
    frag_server.start()

    collage_output_folder = os.path.join(output_folder, "collages")
    rows, cols = 2, 4 # Para 8 videos

    # [2] Collage de videos
    collage_server = Server(workers, list(range(12)), collage_output_folder, "collage")

    collage_server.segments_folder = output_folder  
    collage_server.rows = rows
    collage_server.cols = cols
    
    collage_server.start()



    
