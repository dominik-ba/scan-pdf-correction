import os
import sys
import winreg

def create_registry_entry(name, command, key_path):
    try:
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
            winreg.SetValue(key, '', winreg.REG_SZ, name)
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command") as key:
            winreg.SetValue(key, '', winreg.REG_SZ, command)
        print(f"Registry entry '{name}' created successfully.")
    except Exception as e:
        print(f"Failed to create registry entry '{name}': {e}")

def delete_registry_entry(key_path):
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
        print(f"Registry entry '{key_path}' deleted successfully.")
    except Exception as e:
        print(f"Failed to delete registry entry '{key_path}': {e}")

def install_context_menu():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'correct.py')
    python_path = 'python'  # Assuming python is in the PATH

    file_key_path = r'*\shell\ProcessPDF'
    dir_key_path = r'Directory\shell\ProcessPDFs'

    create_registry_entry(file_key_path, python_path, script_path)
    create_registry_entry(dir_key_path, python_path, script_path)

def uninstall_context_menu():
    file_key_path = r'*\shell\ProcessPDF'
    dir_key_path = r'Directory\shell\ProcessPDFs'

    delete_registry_entry(file_key_path)
    delete_registry_entry(dir_key_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup_context_menu.py <install|uninstall>")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == 'install':
        install_context_menu()
    elif action == 'uninstall':
        uninstall_context_menu()
    else:
        print("Invalid action. Use 'install' or 'uninstall'.")
        sys.exit(1)
