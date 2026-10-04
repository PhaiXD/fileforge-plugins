import argparse
import sys
from PIL import Image
import cairosvg
import io

def svg_to_format(input_path: str, output_path: str, target_format: str, width: int = None):
    try:
        # Convert SVG to PNG bytes first
        with open(input_path, 'rb') as f:
            svg_bytes = f.read()
        
        png_bytes = cairosvg.svg2png(bytestring=svg_bytes, output_width=width)
        img = Image.open(io.BytesIO(png_bytes))
        
        if target_format == 'JPG' or target_format == 'JPEG':
            # Convert mode for JPEG
            if img.mode in ("RGBA", "P", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                img = background
        
        img.save(output_path, format=target_format)
        print(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def image_to_ico(input_path: str, output_path: str):
    try:
        img = Image.open(input_path)
        img.save(output_path, format="ICO", sizes=[(256, 256)])
        print(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Extra Tools")
    parser.add_argument("tool", choices=["svg-png", "svg-jpg", "svg-webp", "to-ico"])
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")
    parser.add_argument("--width", type=int, help="Output width for SVG")
    
    args = parser.parse_args()
    
    if args.tool == "svg-png":
        svg_to_format(args.input, args.output, "PNG", args.width)
    elif args.tool == "svg-jpg":
        svg_to_format(args.input, args.output, "JPEG", args.width)
    elif args.tool == "svg-webp":
        svg_to_format(args.input, args.output, "WEBP", args.width)
    elif args.tool == "to-ico":
        image_to_ico(args.input, args.output)
