import os

def create_list_dirs(base_path, list_of_dirs):
    for dir_name in list_of_dirs:
        dir_path = os.path.join(base_path, dir_name)
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"Directory '{dir_path}' created successfully.")
        except Exception as e:
            print(f"Error creating directory '{dir_path}': {e}")