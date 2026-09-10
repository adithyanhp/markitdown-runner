#python code to batch convert files in a folder to Markdown using MarkItDown
# Features: Single file or batch folder conversion, isolated virtual environment support, custom or automatic timestamped output directories, subfolder structure preservation, duplicate filename auto-numbering, interactive handling for 0-byte empty files, console progress counters (e.g., "3 of 15"), infinite-loop safe directory pre-scanning, comprehensive system session logging (OS, hostname, user, file metadata), and an interactive post-execution log manager menu (View/Read/Delete).

import os
import sys
import platform
import getpass
import socket
from datetime import datetime
from markitdown import MarkItDown

def manage_logs(logs_folder):
    """Interactive utility menu to view, read, and delete system log records."""
    while True:
        if not os.path.exists(logs_folder):
            print("\nNo log directory found yet.")
            break
            
        log_files = [f for f in os.listdir(logs_folder) if f.endswith('.log')]
        log_files.sort(reverse=True) # Show newest logs first
        
        print("\n=================================================================")
        print("                      LOG MANAGEMENT MENU")
        print("=================================================================")
        if not log_files:
            print("[ No active log files available to view or manage ]")
            print("=================================================================")
            input("\nPress Enter to return to main exit...")
            break
            
        print("Available Log Files:")
        for idx, file_name in enumerate(log_files, 1):
            file_path = os.path.join(logs_folder, file_name)
            file_size = os.path.getsize(file_path)
            print(f" [{idx}] {file_name} ({file_size} bytes)")
        print("-----------------------------------------------------------------")
        print(" Options: Type log number to READ | 'd' + number to DELETE (e.g., d1) | 'q' to QUIT")
        
        choice = input("\nEnter choice: ").strip().lower()
        
        if choice == 'q' or choice == '':
            break
            
        elif choice.startswith('d'):
            try:
                num_part = int(choice[1:])
                if 1 <= num_part <= len(log_files):
                    target_file = log_files[num_part - 1]
                    target_path = os.path.join(logs_folder, target_file)
                    os.remove(target_path)
                    print(f"\n[+] Successfully deleted: {target_file}")
                else:
                    print("\n[X] Error: Invalid log number chosen for deletion.")
            except ValueError:
                print("\n[X] Error: Use format 'd1', 'd2' to delete specific logs.")
                
        else:
            try:
                num_part = int(choice)
                if 1 <= num_part <= len(log_files):
                    target_file = log_files[num_part - 1]
                    target_path = os.path.join(logs_folder, target_file)
                    
                    print(f"\n--- START OF LOG FILE: {target_file} ---")
                    with open(target_path, "r", encoding="utf-8") as lf:
                        print(lf.read())
                    print(f"--- END OF LOG FILE: {target_file} ---")
                    input("\nPress Enter to return to Log Menu...")
                else:
                    print("\n[X] Error: Invalid log selection number.")
            except ValueError:
                print("\n[X] Error: Please enter a valid number, deletion code, or 'q'.")
def batch_convert():
    # 1. Ask for the file path or folder path
    input_path_raw = input("Enter the full path of the file OR folder to convert: ").strip().strip('"').strip("'")
    if not os.path.exists(input_path_raw):
        print(f"Error: The path '{input_path_raw}' does not exist.")
        input("\nPress Enter to exit...")
        return

    is_file_mode = os.path.isfile(input_path_raw)
    
    # Establish source folder context for tracking layout structures
    if is_file_mode:
        source_folder = os.path.dirname(input_path_raw)
    else:
        source_folder = input_path_raw

    # 2. Ask where to save the files (Press Enter for automatic timestamped folder)
    print("\nWhere should the Markdown files be saved?")
    print("-> Type a full path OR just press ENTER to automatically create a timestamped folder inside the source directory.")
    output_input = input("Destination path: ").strip().strip('"').strip("'")
    
    start_time = datetime.now()
    timestamp_str = start_time.strftime("%Y-%m-%d_%H-%M-%S")
    
    if output_input == "":
        output_folder = os.path.join(source_folder, f"Converted_{timestamp_str}")
    else:
        output_folder = output_input
    
    # 3. Ask how to handle empty files up front
    print("\n*How should the script handle empty (0-byte) files?")
    empty_choice = input("-> Type 's' to automatically SKIP them OR press ENTER to CONVERT them: ").strip().lower()

    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"Created destination directory: {output_folder}")
        except Exception as e:
            print(f"Error creating destination folder: {e}")
            input("\nPress Enter to exit...")
            return

    # 4. Define target file extensions
    supported_extensions = (
        '.pdf', '.docx', '.xlsx', '.pptx', '.jpg', '.jpeg', '.png',
        '.html', '.py', '.js', '.css', '.jsx', '.txt'
    )

    # 5. Initialize MarkItDown
    try:
        md = MarkItDown()
    except Exception as e:
        print(f"Error initializing MarkItDown: {e}")
        print("Make sure you are running this from your virtual environment.")
        input("\nPress Enter to exit...")
        return

    print("\nScanning input paths...")
    files_to_convert = []
    output_folder_abs = os.path.abspath(output_folder)
    
    if is_file_mode:
        if input_path_raw.lower().endswith(supported_extensions):
            files_to_convert.append(input_path_raw)
    else:
        for root, dirs, files in os.walk(source_folder):
            dirs[:] = [d for d in dirs if os.path.abspath(os.path.join(root, d)) != output_folder_abs]
            if os.path.abspath(root) == output_folder_abs:
                continue
                
            for file in files:
                if file.lower().endswith(supported_extensions):
                    files_to_convert.append(os.path.join(root, file))
                
    total_files = len(files_to_convert)
    if total_files == 0:
        print("No supported files found to convert.")
        input("\nPress Enter to exit...")
        return

    print(f"Found {total_files} file(s) to process. Starting conversion...\n")

    log_records = []
    current_count = 0

    # 6. Process files
    for input_path in files_to_convert:
        current_count += 1
        file = os.path.basename(input_path)
        
        if os.path.getsize(input_path) == 0 and empty_choice == 's':
            print(f"[{current_count} of {total_files}] Skipped empty file: {file}")
            log_records.append({
                "source": input_path, "dest": "N/A", "status": "SKIPPED", "details": "Skipped empty (0-byte) file"
            })
            continue

        relative_dir = os.path.relpath(os.path.dirname(input_path), source_folder)
        if relative_dir == ".":
            target_dir = output_folder
        else:
            target_dir = os.path.join(output_folder, relative_dir)
            
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        base_name = f"{file}.md"
        output_path = os.path.join(target_dir, base_name)
        
        counter = 1
        name_part, ext_part = os.path.splitext(base_name)
        while os.path.exists(output_path):
            new_filename = f"{name_part} ({counter}){ext_part}"
            output_path = os.path.join(target_dir, new_filename)
            counter += 1
        
        final_filename = os.path.basename(output_path)
        clean_relative_dir = relative_dir.replace('\\', '/')
        display_name = f"{clean_relative_dir}/{file}" if relative_dir != "." else file
        
        print(f"[{current_count} of {total_files}] Converting: {display_name} -> {final_filename}...")
        
        try:
            result = md.convert(input_path)
            content = result.text_content if result and result.text_content else ""
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            log_records.append({
                "source": input_path, "dest": output_path, "status": "SUCCESS", "details": "Converted successfully"
            })
        except Exception as e:
            print(f" [X] Failed to convert {file}. Error: {e}")
            log_records.append({
                "source": input_path, "dest": output_path, "status": "FAILED", "details": str(e)
            })

    # 7. Create Session Log File in the Local 'logs' Folder
    software_dir = os.path.dirname(os.path.abspath(sys.argv[0] if sys.argv else __file__))
    software_log_folder = os.path.join(software_dir, "logs")
    os.makedirs(software_log_folder, exist_ok=True)
    
    session_log_path = os.path.join(software_log_folder, f"session_{timestamp_str}.log")
    
    try:
        with open(session_log_path, "w", encoding="utf-8") as log_file:
            log_file.write("=================================================================\n")
            log_file.write("                  MARKITDOWN BATCH CONVERSION LOG\n")
            log_file.write("=================================================================\n\n")
            
            log_file.write("--- SYSTEM METADATA ---\n")
            log_file.write(f"Date & Time : {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"OS Platform : {platform.system()} {platform.release()} (v{platform.version()})\n")
            log_file.write(f"System Name : {platform.node()}\n")
            log_file.write(f"User Name   : {getpass.getuser()}\n")
            log_file.write(f"Host Name   : {socket.gethostname()}\n")
            log_file.write(f"Software Dir: {software_dir}\n\n")
            
            success_count = sum(1 for r in log_records if r["status"] == "SUCCESS")
            failed_count = sum(1 for r in log_records if r["status"] == "FAILED")
            skipped_count = sum(1 for r in log_records if r["status"] == "SKIPPED")
            
            log_file.write("--- EXECUTION METRICS ---\n")
            log_file.write(f"Total Found : {total_files}\n")
            log_file.write(f"Successful  : {success_count}\n")
            log_file.write(f"Failed      : {failed_count}\n")
            log_file.write(f"Skipped     : {skipped_count}\n\n")
            
            log_file.write("--- ITEMISED FILE PROCESS HISTORY ---\n")
            for idx, record in enumerate(log_records, 1):
                log_file.write(f"[{idx}] Status: {record['status']}\n")
                log_file.write(f"    Source File : {record['source']}\n")
                log_file.write(f"    Dest File   : {record['dest']}\n")
                log_file.write(f"    Details     : {record['details']}\n")
                log_file.write(f"    {'-'*30}\n")
                
        print(f"\n[+] Detailed session log file created cleanly at:\n    {session_log_path}")
    except Exception as log_err:
        print(f"Could not generate centralized system log file: {log_err}")

    print(f"\nConversion complete! Files are saved in:\n{output_folder}")
    
    manage_logs(software_log_folder)

if __name__ == "__main__":
    batch_convert()

