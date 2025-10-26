cd ~/path/to/customer-care-bot

git init
echo "# customer-care-bot" > README.md
mkdir app tests
touch requirements.txt docker-compose.yml Dockerfile .env

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

mkdir -p app/services
touch app/{__init__.py,main.py,config.py,models.py,workflow.py,tasks.py}
touch app/services/{__init__.py,apis.py,agent.py}


<!-- run project using docker-compose  -->
docker-compose up --build 


<!-- run project without docker-compose -->
# On macOS (using Homebrew)
brew install redis

# Start Redis server
redis-server

cd /Users/Ali/Documents/customer-care-bot

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

<!-- Terminal 1 -->
redis-server

<!-- Terminal 2 -->
cd /Users/Ali/Documents/customer-care-bot
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

<!-- Terminal 3 -->
cd /Users/Ali/Documents/customer-care-bot
source venv/bin/activate
export REDIS_URL=redis://redis:6379/0 
celery -A app.tasks.celery worker --loglevel=info -Q celery

<!-- For Hot Reload -->
watchmedo auto-restart --directory=./ --pattern="*.py" --recursive -- \
    celery -A app.tasks.celery worker --loglevel=info -Q celery