import os
import sys

def check_and_create_structure():
    """Check if the required directory structure exists and create missing folders."""
    
    # Define required structure
    required_files = [
        'main.py',
        'database.py',
        'requirements.txt'
    ]
    
    required_folders = [
        'checkout',
        'templates'
    ]
    
    required_nested_files = [
        'checkout/__init__.py'
    ]
    
    print("Checking directory structure...")
    print("-" * 50)
    
    # Check files
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} is missing")
            missing_files.append(file)
    
    # Check and create folders
    created_folders = []
    for folder in required_folders:
        if os.path.exists(folder):
            print(f"✓ {folder}/ exists")
        else:
            print(f"✗ {folder}/ is missing - creating...")
            os.makedirs(folder, exist_ok=True)
            created_folders.append(folder)
            print(f"  Created {folder}/")
    
    # Check nested files
    missing_nested = []
    for file in required_nested_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} is missing")
            missing_nested.append(file)
    
    print("-" * 50)
    
    # Summary
    if created_folders:
        print(f"\n✓ Created {len(created_folders)} folder(s): {', '.join(created_folders)}")
    
    if missing_files or missing_nested:
        print(f"\n⚠ Warning: {len(missing_files + missing_nested)} file(s) are missing")
        if missing_files:
            print(f"  Missing files: {', '.join(missing_files)}")
        if missing_nested:
            print(f"  Missing nested files: {', '.join(missing_nested)}")
        return False
    
    if not created_folders and not missing_files and not missing_nested:
        print("\n✓ All required files and folders are present!")
    
    return True

if __name__ == "__main__":
    success = check_and_create_structure()
    sys.exit(0 if success else 1)
