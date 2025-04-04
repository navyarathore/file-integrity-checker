# Local File Integrity Checker
This is a simplistic file integrity checker for your local files.

## Run Instructions

```bash
pip install -r requirements.txt
mkdir test_folder
echo "hello world" > test_folder/sample.txt
python checker.py update test_folder
python app.py
