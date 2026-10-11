import argparse
import sys
import io
import pymupdf
from PIL import Image

def svg_to_format(input_path: str, output_path: str, target_format: str, width: int = None):
    try:
        doc = pymupdf.open(input_path)
        page = doc[0]
        rect = page.rect
        
        target_fmt = target_format.upper()
        is_png = (target_fmt == "PNG")
        
        if width and width > 0 and rect.width > 0:
            zoom = width / rect.width
            mat = pymupdf.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=is_png)
        else:
            pix = page.get_pixmap(alpha=is_png)
            
        png_bytes = pix.tobytes("png")
        doc.close()
        
        with Image.open(io.BytesIO(png_bytes)) as img:
            if target_fmt in ("JPG", "JPEG"):
                if img.mode in ("RGBA", "P", "LA"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                    background.save(output_path, format="JPEG", quality=95)
                else:
                    rgb_img = img.convert("RGB")
                    rgb_img.save(output_path, format="JPEG", quality=95)
            else:
                img.save(output_path, format=target_fmt)
        print(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SVG Tools")
    parser.add_argument("tool", choices=["svg-png", "svg-jpg", "svg-webp"])
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")
    parser.add_argument("--width", type=int, default=None, help="Output width for SVG")
    
    args = parser.parse_args()
    
    if args.tool == "svg-png":
        svg_to_format(args.input, args.output, "PNG", args.width)
    elif args.tool == "svg-jpg":
        svg_to_format(args.input, args.output, "JPEG", args.width)
    elif args.tool == "svg-webp":
        svg_to_format(args.input, args.output, "WEBP", args.width)
