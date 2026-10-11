import argparse
import sys
from PIL import Image

def image_to_ico(input_path: str, output_path: str):
    try:
        with Image.open(input_path) as img:
            img.save(output_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
        print(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image to ICO Tool")
    parser.add_argument("tool", choices=["to-ico", "png-ico", "jpg-ico"])
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")
    
    args = parser.parse_args()
    image_to_ico(args.input, args.output)
