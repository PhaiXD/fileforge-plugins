import argparse
import sys
import os
import subprocess
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

def convert_image(input_path: str, output_path: str, target_format: str):
    fmt = target_format.upper()
    if fmt == "JPG":
        fmt = "JPEG"
    try:
        with Image.open(input_path) as img:
            if fmt in ("JPEG", "PDF") and img.mode in ("RGBA", "P", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                background.save(output_path, format=fmt, quality=95)
            elif fmt in ("JPEG", "PDF") and img.mode != "RGB":
                rgb_img = img.convert("RGB")
                rgb_img.save(output_path, format=fmt, quality=95)
            elif fmt == "AVIF":
                img.save(output_path, format="AVIF", quality=90)
            else:
                img.save(output_path, format=fmt)
        print(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        # Fallback to FFmpeg if Pillow encounters any issue
        try:
            args = ["ffmpeg", "-y", "-i", input_path]
            if fmt == "AVIF":
                args.extend(["-c:v", "libsvtav1", output_path])
            else:
                args.append(output_path)
            res = subprocess.run(args, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"Successfully converted {input_path} to {output_path}")
                return
        except Exception:
            pass
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Format Converter")
    parser.add_argument("tool")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")
    
    args = parser.parse_args()
    target_ext = args.tool.split("-")[-1]
    convert_image(args.input, args.output, target_ext)
