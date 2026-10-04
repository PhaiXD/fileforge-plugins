# 🧩 FileForge Plugins

The official plugin registry and ecosystem for [FileForge](https://github.com/PhaiXD/fileforge). 

FileForge's plugin system allows developers and users to easily extend the application's capabilities by adding new file conversion tools, AI processors, and media fetchers without modifying the core codebase.

## 🚀 How It Works

FileForge dynamically loads plugins from this repository's egistry.json. 
When a user installs a plugin via the FileForge UI:
1. FileForge downloads the latest release .zip for that plugin from this repository.
2. The plugin is extracted into the local %LOCALAPPDATA%\FileForge\plugins\ directory.
3. FileForge reads the plugin's manifest.json and dynamically generates the UI (Drop zones, buttons, inputs) based on the defined tool configurations.
4. When a user runs the tool, FileForge executes the plugin's plugin.bat script, passing the uploaded file and required arguments.

## 📦 Current Official Plugins

We maintain several core plugins that extend FileForge's native functionality:

- **Image Tools:** Extended image format conversions (e.g., SVG, ICO, HEIC support).
- **Audio Tools:** Extended audio conversions (e.g., OGG, FLAC).
- **Video Tools:** Extended video conversions (e.g., AVI, MKV).

*(Note: Many core tools like basic PDF, MP4, and MP3 conversions are now built natively into FileForge v2.0+ for better performance).*

---

## 🛠️ Developing a Custom Plugin

Creating a plugin for FileForge is simple. A plugin requires three basic files:

### 1. Directory Structure
`	ext
my-plugin/
├── manifest.json   # Defines the UI and tool configuration
├── plugin.bat      # Entry point executed by FileForge (Windows)
└── plugin.py       # Your actual logic (optional, but recommended)
`

### 2. manifest.json
This file tells FileForge how to render the UI and what command to run.
`json
{
  "id": "my-plugin",
  "name": "My Awesome Plugin",
  "version": "1.0.0",
  "description": "Does awesome things to your files.",
  "author": "YourName",
  "icon": "✨",
  "min_core_version": "2.0.0",
  "tools": [
    {
      "id": "magic-convert",
      "name": "Magic Converter",
      "description": "Converts files magically.",
      "icon": "🎩",
      "category": "document",
      "mode": "convert",
      "inputs": {
        "type": "file",
        "accept": [".txt", ".md"]
      },
      "command": "plugin.bat",
      "args": ["magic", "{input_file}", "{output_file}"],
      "output_ext": ".pdf"
    }
  ]
}
`

**Key Parameters:**
- mode: Determines which tab the tool appears in (convert, compress, etch, i).
- inputs.type: ile (creates a drag-and-drop zone) or url (creates a text input box).
- rgs: Variables like {input_file} and {output_file} are automatically replaced by FileForge at runtime with temporary file paths.

### 3. plugin.bat
FileForge executes this batch file. It usually just acts as a bridge to a Python script.
`at
@echo off
set ACTION=%1
set INPUT_FILE=%2
set OUTPUT_FILE=%3

:: Run the python script located in the same directory
python "%~dp0plugin.py" %ACTION% "%INPUT_FILE%" "%OUTPUT_FILE%"
`

### 4. plugin.py
Your actual logic using standard Python libraries or CLI tools like fmpeg.
`python
import sys
import shutil

action = sys.argv[1]
input_path = sys.argv[2]
output_path = sys.argv[3]

if action == "magic":
    # Do your magic here
    shutil.copyfile(input_path, output_path)
    print(f"Successfully converted to {output_path}")
`

## 🤝 Publishing Your Plugin

To add your plugin to the official FileForge Store:
1. Fork this repository.
2. Create a new folder for your plugin inside the plugins/ directory.
3. Add your manifest.json, plugin.bat, and plugin.py.
4. Add your plugin's metadata to the egistry.json file in the root directory.
5. Submit a Pull Request!

Once approved, your plugin will be packaged into a release and instantly available to all FileForge users globally via the in-app Plugin Store.
