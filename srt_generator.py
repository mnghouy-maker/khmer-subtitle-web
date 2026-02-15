def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:06.3f}".replace(".", ",")


def generate_srt(segments, translate_func, output_file):
    """
    Generate .srt subtitle file
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_time(seg["start"])
            end = format_time(seg["end"])
            text = translate_func(seg["text"].strip())

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")
