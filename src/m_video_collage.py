import os
import gc, glob
from moviepy import VideoFileClip, clips_array


def video_collage (segment_number: int, output_folder: str, collage_output_folder: str, rows: int, cols: int):
    
    print(f"\n[collage] Creando collage #{segment_number}")

    # Buscar todos los clips con ese número de segmento
    all_clips = sorted(glob.glob(os.path.join(output_folder, "*_*.mp4")))
    
    # Filtrar solo los clips del segmento específico
    segment_clips_path = [
        clip for clip in all_clips 
        if clip.endswith(f"_{segment_number}.mp4")
    ]
    
    if not segment_clips_path:
        print(f"[collage] No se encontraron clips para segmento {segment_number}")
        return False
    
    print(f"[collage] Clips encontrados para segmento {segment_number}: {len(segment_clips_path)}")
    for clip in segment_clips_path:
        print(f"  - {os.path.basename(clip)}")

    
    # Cargar todos los clips 
    clips = []
    for path in segment_clips_path:

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
