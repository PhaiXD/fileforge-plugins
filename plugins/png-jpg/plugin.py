import argparse
import sys
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

def convert_image(input_path: str, output_path: str, target_format: str):
    try:
        with Image.open(input_path) as img:
            fmt = target_format.upper()
            if fmt == "JPG":
                fmt = "JPEG"
                
            if fmt in ("JPEG", "PDF") and img.mode in ("RGBA", "P", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                background.save(output_path, format=fmt, quality=95)
            elif fmt in ("JPEG", "PDF") and img.mode != "RGB":
                rgb_img = img.convert("RGB")
                rgb_img.save(output_path, format=fmt, quality=95)
            else:
                img.save(output_path, format=fmt)
        print(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
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
