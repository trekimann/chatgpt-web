import os
import fnmatch

def summarize_code(project_path, output_file, exclude_folders):
    with open(output_file, 'w') as out:
        for foldername, subfolders, filenames in os.walk(project_path):
            # Skip excluded folders
            if any(excl in foldername for excl in exclude_folders):
                continue
            for filename in filenames:
                if fnmatch.fnmatch(filename, '*.svelte'):  # Check if it's a Svelte file
                    out.write(f'--- {filename}\n')
                    with open(os.path.join(foldername, filename), 'r') as file:
                        file_content = file.read()
                    out.write(f'{file_content.strip()}\n\n')

# Call the script with your parameters
summarize_code('./', 'out.txt', ['src-tauri'])