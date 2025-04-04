# Local File Integrity Checker (Buggy Version)

This is a simplistic file integrity checker for testing AI models. It intentionally includes flaws to verify how well your AI or automation scripts can catch errors.

## Run Instructions

```bash
pip install -r requirements.txt
mkdir test_folder
echo "hello world" > test_folder/sample.txt
python checker.py update test_folder
python app.py
