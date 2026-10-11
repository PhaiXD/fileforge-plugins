import argparse
import sys
import subprocess
import os

def convert_media(input_file: str, output_file: str, target_format: str):
    try:
        args = ["ffmpeg", "-y", "-i", input_file]
        
        if target_format in ["ogg", "flac"]:
            args.extend(["-vn", output_file])
        elif target_format in ["mkv", "avi"]:
            args.extend(["-preset", "fast", output_file])
        else:
            args.append(output_file)
            
        print(f"Running: {' '.join(args)}")
        result = subprocess.run(args, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error during conversion: {result.stderr}", file=sys.stderr)
            sys.exit(1)
            
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Media Converter Tools")
    parser.add_argument("tool", choices=["to-ogg", "to-flac", "to-mkv", "to-avi"])
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")
    
    args = parser.parse_args()
    
    fmt_map = {
        "to-ogg": "ogg",
        "to-flac": "flac",
        "to-mkv": "mkv",
        "to-avi": "avi",
    }
    convert_media(args.input, args.output, fmt_map.get(args.tool, "mp4"))
