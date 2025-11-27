import os
from moviepy import VideoFileClip, clips_array
import gc, glob

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
    
    rutas_clips = []

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

            # Guardar la ruta del clip generado
            rutas_clips.append(output)
            
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
        return []

    print(f"    [d:] Video cortado y guardado en la carpeta {output_path}")        
    print(f"[divide_video] Se generaron {len(rutas_clips)} clips")
    
    return rutas_clips

def video_collage(segment_number: int, output_folder: str, collage_output_folder: str, rows: int, cols: int):
    
    print(f"\n[collage] Creando collage #{segment_number}")

    # Buscar todos los clips con ese número de segmento
    all_clips = sorted(glob.glob(os.path.join(output_folder, "*_*.mp4")))
    
    # Filtrar solo los clips del segmento específico
    segment_clips = [
        clip for clip in all_clips 
        if clip.endswith(f"_{segment_number}.mp4")
    ]
    
    if not segment_clips:
        print(f"[collage] No se encontraron clips para segmento {segment_number}")
        return False
    
    print(f"[collage] Clips encontrados para segmento {segment_number}: {len(segment_clips)}")
    for clip in segment_clips:
        print(f"  - {os.path.basename(clip)}")
    
    # Cargar todos los clips 
    clips = []
    for path in segment_clips:

        try:
            clip = VideoFileClip(path)
            clips.append(clip)
            print(f"[video_collage] Cargado: {os.path.basename(path)}")
        except Exception as e:
            print(f"[video_collage] Error cargando {path}: {e}")

    if len(clips) == 0:
        print(f"[collage] No se pudieron cargar clips para segmento {segment_number}")
        return
    
    total_needed = rows * cols
    print(f"[video_collage] Grid: {rows}x{cols} = {total_needed} posiciones")
    print(f"[video_collage] Clips disponibles: {len(clips)}")

    # Si faltan clips, repetir desde el inicio
    if len(clips) < total_needed:
        print(f"[video_collage] Faltan {total_needed - len(clips)} clips, se replicarán.")
        original_count = len(clips)
        while len(clips) < total_needed:
            # Clonar clips en orden cíclico
            idx = len(clips) % original_count
            clips.append(clips[idx])

    # Si sobran clips, usar solo los necesarios
    if len(clips) > total_needed:
        print(f"[video_collage] Sobran {len(clips) - total_needed} clips, se usarán los primeros {total_needed}")
        clips = clips[:total_needed]

    # Ajustar tamaño uniforme
    w, h = clips[0].size
    print(f"[video_collage] Tamaño de referencia: {w}x{h}")
    
    clips_resized = []
    for i, c in enumerate(clips):
        if c.size != (w, h):
            print(f"[video_collage] Redimensionando clip {i+1}")
            clips_resized.append(c.resized((w, h)))
        else:
            clips_resized.append(c)

    # Construir grilla 
    grid = []
    index = 0
    for r in range(rows):
        fila = []
        for c in range(cols):
            fila.append(clips_resized[index])
            index += 1
        grid.append(fila)

    print("[video_collage] Generando collage...")
    
    # Crear collage 
    final = clips_array(grid)

    # Guardar resultado 
    os.makedirs(collage_output_folder, exist_ok=True)
    output_path = os.path.join(collage_output_folder, f"collage_{segment_number}.mp4")
    print(f"[video_collage] Guardando en {output_path}...")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

    # Liberar memoria 
    for c in clips:
        try:
            c.close()
        except:
            pass

    for c in clips_resized:
        try:
            c.close()
        except:
            pass

    final.close()
    gc.collect()

    print(f"[video_collage] ✓ Collage generado en: {output_path}")
    return True   
