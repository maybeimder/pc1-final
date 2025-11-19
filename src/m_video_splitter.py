import os
from moviepy import VideoFileClip
import gc

def ensure_path( input_path:str, output_path:str ):
    # Asegurar que exista un directorio de salida
    os.makedirs(output_path, exist_ok=True)

    if not os.path.exists(input_path):
        print(f"[divide_video] No se encuentra la ruta {input_path}")
        return

    return os.path.splitext(os.path.basename(input_path))[0]


def divide_video( segment_duration:int, input_path:str, output_path:str ):
    base_name = ensure_path(input_path, output_path)
    
    if base_name is None:
        return

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
            output = os.path.join(output_path, output_filename)

            # Cargar el video completo
            video = VideoFileClip(input_path)

            # Cortar el clip
            clip = video.subclipped(start_time, end_time)
            
            # Escribir el nuevo archivo de video
            clip.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)
            
            clip.close()
            video.close()
            del video
            del clip
            gc.collect()

            segment += 1

    except Exception as e:
        print(f" Error al procesar {input_path}: {e}")
        import traceback
        traceback.print_exc()
            
    print(f"    [d:] Video cortado y guardado en la carpeta {output_path}")
