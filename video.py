import os
import subprocess

def compress_video(input_file_path, fast=True):
    """Compresses the video using H.265 (HEVC) encoding to reduce size while maintaining quality."""
    
    output_file_path = f"compressed_{os.path.basename(input_file_path)}"
    
    # Adjust the CRF (Constant Rate Factor) for quality. Lower CRF gives better quality, 18-28 is typical.
    crf_value = '28' if fast else '24'  # '24' is high quality, '28' is faster and slightly more compressed.
    
    command = [
        'ffmpeg', '-i', input_file_path, '-c:v', 'libx265', '-crf', crf_value,
        '-preset', 'fast',  # Adjust preset for compression speed. 'fast' or 'medium' are good options.
        '-c:a', 'copy', 
        output_file_path
    ]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error compressing video: {e}")
        return None
    
    return output_file_path
