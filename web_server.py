#!/usr/bin/env python3
"""
Простой веб-сервер для healthcheck и мониторинга бота
"""
from flask import Flask, jsonify
import os
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Глобальные переменные для мониторинга
bot_start_time = None
last_activity = None
total_messages = 0

@app.route('/')
def health_check():
    """Health check endpoint"""
    global bot_start_time, last_activity, total_messages
    
    status = {
        "status": "healthy",
        "bot_running": bot_start_time is not None,
        "uptime": time.time() - bot_start_time if bot_start_time else 0,
        "last_activity": last_activity,
        "total_messages": total_messages,
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(status)

@app.route('/status')
def detailed_status():
    """Подробный статус бота"""
    global bot_start_time, last_activity, total_messages
    
    if bot_start_time:
        uptime_seconds = time.time() - bot_start_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        uptime_str = "Not running"
    
    status = {
        "bot_status": "Running" if bot_start_time else "Stopped",
        "uptime": uptime_str,
        "last_activity": last_activity or "No activity",
        "total_messages": total_messages,
        "environment": os.getenv('RAILWAY_ENVIRONMENT', 'local'),
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(status)

def update_bot_status(started=True, message_count=0):
    """Обновление статуса бота"""
    global bot_start_time, last_activity, total_messages
    
    if started:
        bot_start_time = time.time()
    
    if message_count > 0:
        total_messages += message_count
        last_activity = datetime.now().isoformat()

def run_web_server(host='0.0.0.0', port=5000):
    """Запуск веб-сервера в отдельном потоке"""
    def run():
        app.run(host=host, port=port, debug=False)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread

if __name__ == "__main__":
    run_web_server()
    print("🌐 Web server started on port 5000")
    print("📊 Health check: http://localhost:5000/")
    print("📈 Status: http://localhost:5000/status") 