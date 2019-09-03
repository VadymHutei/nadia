# NADIA PHOTOGRAPHER

git clone https://github.com/VadymHutei/nadia.git
cd nadia/app
python3 -m venv venv
source env/bin/activate
pip install Flask
export FLASK_APP=main.py
flask run --host=0.0.0.0