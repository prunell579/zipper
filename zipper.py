import os
import zipfile

# form lists of files to zip. Condition: they should account to less than 9gb

FILES_TO_ZIP_DIR = '/Volumes/999 Gigs/switzerland_raw/raw_files'

def bytes_to_gb(bytes):
    gb = bytes / (1024 ** 3)
    return gb

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size

def compress_files(zip_filename, files_to_compress, progress_interval = 5):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        total_files = len(files_to_compress)
        for i, file in enumerate(files_to_compress):
            zipf.write(file)
            if (i + 1) % progress_interval == 0 or (i + 1) == total_files:
                print(f"Added {i + 1} of {total_files} files to {zip_filename}")



if __name__ == '__main__':
    file_lists = {}
    filelist = []
    filelist_size_in_gb = 0


    print('Total folder size: {} GB'.format(bytes_to_gb(get_folder_size(FILES_TO_ZIP_DIR))))

    total_file_count = 0
    for filepath in os.listdir(FILES_TO_ZIP_DIR):
        total_file_count += 1

        abs_filepath = os.path.join(FILES_TO_ZIP_DIR, filepath)

        filelist_size_in_gb += bytes_to_gb(os.path.getsize(abs_filepath))
        if filelist_size_in_gb < 8:
            filelist.append(abs_filepath)
        else:
            file_list_idx = len(list(file_lists.keys())) + 1
            file_list_key = 'part{}'.format(file_list_idx)
            file_lists[file_list_key] = filelist.copy()
            print('{} has {} files, and has a cumulative size of {}'.format(file_list_key, len(filelist), filelist_size_in_gb))
            filelist = []
            filelist_size_in_gb = 0


    for file_list_key, file_list in file_lists.items():
        compress_files(os.path.join(FILES_TO_ZIP_DIR, '..', 'zip', 'switzerland_raw_' + file_list_key + '.zip'), file_list)