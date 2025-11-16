import os
from moviepy import VideoFileClip
import gc

def divideVideo():
    # --- Configuración ---
    input_folder = "videos_originales"
    output_folder = "videos_cortados"
    segment_duration = 10  # Duración de cada segmento en segundos
    # ---------------------

    # Listar todos los archivos de video en la carpeta de entrada
    try:
        source_filenames = [
            f for f in os.listdir(input_folder) 
            if f.endswith((".mp4", ".mov")) #agregan el tipo si ponen otro tipo de video idk
        ]
    except FileNotFoundError:
        print(f"Error: La carpeta '{input_folder}' no existe.")
        exit()

   

    # procesa cada video encontrado
    for filename in source_filenames:
        input_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0] # Nombre sin extensión


        try:
            # Cargar el video temporalmente para obtener la duración
            temp_video = VideoFileClip(input_path)
            duration = temp_video.duration # Duración total (120s más o menos)
            temp_video.close()
            del temp_video 
            gc.collect()

            segment = 1

            for start_time in range(0, int(duration), segment_duration):
                
                # El tiempo final es el inicio + duración
                end_time = min(start_time + segment_duration, duration)
                
                # Nombre del archivo de salida (ej: "video1_segmento_1.mp4")
                output_filename = f"{base_name}_{segment}.mp4"
                output_path = os.path.join(output_folder, output_filename)

                # Cargar el video completo
                video = VideoFileClip(input_path)
                # Cortar el clip
                clip = video.subclipped(start_time, end_time)
                
                # Escribir el nuevo archivo de video
                clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
                
                clip.close()
                video.close()
                del video
                del clip

                segment += 1

        except Exception as e:
            print(f" Error al procesar {filename}: {e}")
            import traceback
            traceback.print_exc()
            
    print("Videos cortados y guardados en la carpeta de salida")


if __name__ == "__main__":
    divideVideo()