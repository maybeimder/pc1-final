# main.py

import os
import sys
from server import Server
from worker import Worker


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

    print(f"[MAIN] Videos detectados: {video_paths}")

    server = Server(
        workers = {
            "worker8" : Worker("worker8" , "10.0.0.35", 5050),
            "worker9" : Worker("worker9" , "10.0.0.36", 5050),
            "worker10": Worker("worker10", "10.0.0.37", 5050),
            "worker11": Worker("worker11", "10.0.0.38", 5050),
        },
        videos =video_paths,
        output_folder = output_folder
    )

    server.start()
