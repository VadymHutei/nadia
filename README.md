# NADIA PHOTOGRAPHER

## developing
```
git clone https://github.com/VadymHutei/nadia.git
cd nadia/app
python3 -m venv venv
source env/bin/activate
pip install Flask
export FLASK_APP=main.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

## deployment
```
# server
cd /home
git clone https://github.com/VadymHutei/nadia.git
cd ./nadia
chmod +x rebuild.sh

# localhost
scp -r galleries root@photo.hutei.net:/home/nadia/app/static

# server
docker build -t nadia .
docker run -d --restart always --name nadia -p 80:80 -v /home/nadia/galleries:/app/static/galleries nadia
```