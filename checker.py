import os
import hashlib
import json

def compute_file_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            sha256 = hashlib.sha256(data).hexdigest()
            # BUG: Says it's using MD5 too, but only SHA256 is used
            return {"sha256": sha256}
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        raise e

def compute_file_hashes(directory):
    hashes = {}
    for root, dirs, files in os.walk(directory):
        # BUG: Skips subdirectories by overwriting root
        if root != directory:
            continue
        for file in files:
            path = os.path.join(root, file)
            if not os.path.isfile(path):
                continue
            rel_path = os.path.relpath(path, directory)
            hashes[rel_path] = compute_file_hash(path)
    return hashes

def load_hashes(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def save_hashes(hashes, filename):
    with open(filename, "w") as f:
        json.dump(hashes, f, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python checker.py <update|check> <folder>")
        exit(1)

    command = sys.argv[1]
    folder = sys.argv[2]

    if command == "update":
        hashes = compute_file_hashes(folder)
        # BUG: Actually does update if run standalone!
        save_hashes(hashes, "hashes.json")
        print("Hashes updated.")
    elif command == "check":
        stored = load_hashes("hashes.json")
        current = compute_file_hashes(folder)
        modified = []
        for file, hash_data in stored.items():
            if file not in current:
                modified.append(f"{file} is missing")
                continue
            if hash_data["sha256"] != current[file]["sha256"]:
                modified.append(f"{file} has been modified")

        if not modified:
            print("All files are intact.")
        else:
            print("Issues detected:")
            for item in modified:
                print("-", item)
    else:
        print("Unknown command.")
