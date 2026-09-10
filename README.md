# MarkItDown Batch & Single-File Runner

A highly scalable, self-contained Python CLI automation utility that extends Microsoft's **MarkItDown** library. It allows you to convert complex single file paths or multi-level nested folders into cleanly formatted Markdown (`.md`) files on Windows 11.

## ✍️ Author / Developer

* **Adithyan HP** - *Core Architecture & Wrapper Development* - [GitHub Profile](https://github.com)

---

## ✨ Features

* 📂 **Dual Processing Modes:** Automatically detects and processes either a specific individual file or scans an entire directory hierarchy.
* 🌿 **Subfolder Structure Preservation:** Recreates identical nested folder paths inside your output directories to match your original workspace.
* 🛡️ **Infinite-Loop Protection:** Dynamically targets and blocks recursive path scanning when output folders are generated inside the source path.
* 🔢 **Auto-Numbered File Names:** Intelligently checks for duplicate target file conflicts (e.g., `file (1).md`) to prevent critical data from being overwritten.
* ⚙️ **Centralized System Session Logging:** Automatically captures system metadata (OS platform, hostname, user account, execution times) and leaves a comprehensive report inside a dedicated local `logs` folder.
* 📋 **Interactive Log Dashboard:** Includes a post-execution CLI menu allowing users to search, view, read, or delete individual log records natively.

---

## 🛠️ Supported Extensions

The runner handles structural layouts, strips structural clutter, and extracts clear text blocks from:
* **Documents & Media:** `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.jpg`, `.jpeg`, `.png`
* **Code & Web Formats:** `.html`, `.py`, `.js`, `.css`, `.jsx`, `.txt`

---

## 🚀 Setup & Installation on Windows 11

### 1. Initialize the Isolated Environment
Open **Command Prompt** or **PowerShell** inside your project directory and run the following commands to create your isolated virtual environment:
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install markitdown[all]
```

### 2. Configure the Fast Launch Shortcut
Create a file named `run_converter.bat` alongside `markitdown run-script.py` and paste the following automated setup:
```cmd
@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
python "markitdown run-script.py"
pause
```

Now, you can execute all file operations by **double-clicking `run_converter.bat`**.

---

## 📖 How to Use

1. Double-click `run_converter.bat` to launch the terminal window.
2. **Input Source:** Paste the absolute path of the single file or the complete folder folder (e.g., `"C:\Users\adith\Documents\Syllabus.docx"`).
3. **Output Destination:** Type a target folder path (like `C:\Users\adith\Desktop`) or press **ENTER** to create an automated timestamped folder.
4. **Empty File Policy:** Press **ENTER** to process all data, or type **`s`** to skip empty 0-byte items instantly.

---

## 📦 Keeping Software Updated

If Microsoft pushes a new package build for MarkItDown, you can upgrade your local system library without altering your execution script:
```cmd
call .venv\Scripts\activate
pip install --upgrade markitdown[all]
```

## ⚖️ License

Distributed under the MIT License. Copyright (c) 2026 Adithyan HP. See `LICENSE` for more information.
