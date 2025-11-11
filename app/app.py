from flask import Flask, request
import psycopg2
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'postgres'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password')
    )

@app.route('/')
def index():
    return 'Hello! Use /ping and /visits endpoints.'

@app.route('/ping')
def ping():
    ip = request.remote_addr
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO visits (ip) VALUES (%s)', (ip,))
    return 'pong'

@app.route('/visits')
def visits():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM visits')
            count = cur.fetchone()[0]
    return str(count)

if __name__ == '__main__':
    logger.info("Starting flask app")
    app.run(host='0.0.0.0', port=5000)