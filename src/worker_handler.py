from m_video_splitter import divide_video
from m_video_collage import video_collage

# Separa los paths de los archivos para empezar a fragmentarlos
def handle_split_task(name:str, message: str):
    payload = message.replace("SPLIT:", "", 1)
    
    try:
        output_folder, csv_paths = payload.split("|", 1)
    except ValueError:
        print(f"[{name}] Formato SPLIT inválido: {message}")
        return

    video_paths = [p.strip() for p in csv_paths.split(",") if p.strip()]

    for path in video_paths:
        print(f"[{name}] empezó a fragmentar {path}")
        divide_video(10, path, output_folder)


def handle_collage_task(name:str, message: str):
    payload = message.replace("COLLAGE:", "", 1)

    try:
        segments_folder, collage_output_folder, rows, cols, segment_list = payload.split("|", 4)
    except ValueError:
        print(f"[{name}] Formato COLLAGE inválido: {message}")
        return

    rows = int(rows)
    cols = int(cols)

    segment_numbers = [int(s) for s in segment_list.split(",") if s.strip()]

    for n in segment_numbers:
        print(f"[{name}] empezó collage {n}")
        video_collage(
            segment_number=n,
            output_folder=segments_folder,
            collage_output_folder=collage_output_folder,
            rows=rows,
            cols=cols,
        )
