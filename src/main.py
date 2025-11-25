# main.py

import os
import sys
from server import Server
from worker import Worker
from listener import listen_for_workers_udp
from m_video_splitter import video_collage


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

    workers = listen_for_workers_udp (
        main_port= 6000,
        expected_workers=4,
        worker_factory= lambda name,ip,port: Worker(name, ip, port)
    )

    #Crear el collage
    
    GRID_ROWS = 2
    GRID_COLS = 3
    
    # Ruta compartida para subir videos
    RUTA_COMPARTIDA = os.path.join("C:/Users/Santiago Vengoechea/Documents/Universidad/SEMESTRE VI/Estructuras del Computador")
    
    # Crear la carpeta si no existe
    os.makedirs(RUTA_COMPARTIDA, exist_ok=True)

    # Buscar todos los clips generados en output_folder
    clips_generados = [
        os.path.join(output_folder, f)
        for f in sorted(os.listdir(output_folder))
        if f.endswith(".mp4")
    ]
    
    if clips_generados:
        print(f"[MAIN] Se encontraron {len(clips_generados)} clips procesados")
        
        # Guardar collage en la ruta compartida
        collage_output = os.path.join(RUTA_COMPARTIDA, "collage_final.mp4")
        print(f"[MAIN] Guardando collage en: {collage_output}")
        
        video_collage(clips_generados, GRID_ROWS, GRID_COLS, collage_output)
    else:
        print("[MAIN] No se encontraron clips para crear collage")

    server = Server(workers, video_paths, output_folder)
    server.start()
