
python3 -m pip install virtualenv
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

python build_ata.py
python build_jasc.py