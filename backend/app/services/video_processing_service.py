import subprocess
import os


def get_video_duration(file_path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            file_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return float(result.stdout.strip())



def get_file_size_mb(file_path: str) -> float:
    file_size_bytes = os.path.getsize(file_path)
    return file_size_bytes / (1024 * 1024)


def compress_video(input_path: str, output_path: str):
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            input_path,
            "-c:v",
            "libx264",
            "-crf",
            "28",
            "-c:a",
            "aac",
            output_path,
        ],
        check=True,
    )



def delete_temp_file(file_path: str):
    if os.path.exists(file_path):
        os.unlink(file_path)
