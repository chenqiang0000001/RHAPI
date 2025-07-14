import os
import subprocess
import threading
import signal
from flask import Flask, send_from_directory, render_template_string, jsonify, Response, request, redirect, url_for, session
import glob
import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
import uuid

app = Flask(__name__)
app.secret_key = 'rh_secret_key_2024'  # 用于session

REPORT_ROOT = "allure-report"
MAIN_EXEC = "main_execute.py"
LOG_FILE = "run.log"

# 保存当前运行的进程对象
from typing import Optional
current_process: dict[str, Optional[subprocess.Popen]] = {'proc': None}

ADMIN_USER = 'admin'
ADMIN_PASS = 'rh123456'

LOGO_FILENAME = 'RH_logo.png'

SCHEDULE_CONFIG_FILE = 'schedule_config.json'
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))

def load_schedule_config():
    if os.path.exists(SCHEDULE_CONFIG_FILE):
        with open(SCHEDULE_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_schedule_config(cfg_list):
    with open(SCHEDULE_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg_list, f, ensure_ascii=False, indent=2)

def run_scheduled_test():
    subprocess.Popen([
        os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"), MAIN_EXEC
    ])

def update_scheduler():
    scheduler.remove_all_jobs()
    cfg_list = load_schedule_config()
    for task in cfg_list:
        if not isinstance(task, dict):
            continue
        if not task.get('enabled'):
            continue
        tid = task['id']
        if task['type'] == 'daily':
            trigger = CronTrigger(hour=task['hour'])
        elif task['type'] == 'weekly':
            trigger = CronTrigger(day_of_week=task['weekday'], hour=task['hour'])
        elif task['type'] == 'monthly':
            trigger = CronTrigger(day=task['day'], hour=task['hour'])
        else:
            continue
        scheduler.add_job(run_scheduled_test, trigger, id=tid, replace_existing=True)

update_scheduler()

def get_latest_report_url():
    try:
        # 按最后修改时间排序，取最新的报告目录
        dirs = [d for d in os.listdir(REPORT_ROOT) if os.path.isdir(os.path.join(REPORT_ROOT, d))]
        if not dirs:
            return None
        latest = max(dirs, key=lambda d: os.path.getmtime(os.path.join(REPORT_ROOT, d)))
        return f"/report/{latest}/index.html"
    except Exception:
        return None

def get_report_case_count(report_dir):
    try:
        summary_path = os.path.join(report_dir, 'widgets', 'summary.json')
        if os.path.exists(summary_path):
            with open(summary_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                stat = data.get('stat', {})
                if 'total' in stat:
                    return stat['total']
        # 尝试读取 suites.json
        suites_path = os.path.join(report_dir, 'widgets', 'suites.json')
        if os.path.exists(suites_path):
            with open(suites_path, 'r', encoding='utf-8') as f:
                suites = json.load(f)
                total = 0
                for suite in suites:
                    if 'children' in suite:
                        for child in suite['children']:
                            if 'children' in child:
                                for case in child['children']:
                                    total += 1
                return total
    except Exception:
        pass
    return 0

@app.route(f"/{LOGO_FILENAME}")
def logo():
    return send_from_directory('.', LOGO_FILENAME)

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            msg = '账号或密码错误'
    return render_template_string('''
{% raw %}
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>登录 - 瑞辉智测平台</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/RH_logo.png">
<style>
body {
    min-height: 100vh;
    margin: 0;
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
    font-family: 'Segoe UI', 'Arial', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
}
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: rgba(173, 216, 230, 0.9);
    display: flex;
    align-items: center;
    padding: 0 30px;
    backdrop-filter: blur(10px);
}
.navbar-title {
    color: white;
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 1px;
}
.login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 400px;
    padding: 20px;
}
.login-form {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    width: 100%;
    backdrop-filter: blur(10px);
}
.logo-container {
    text-align: center;
    margin-bottom: 20px;
}
.login-logo {
    height: 60px;
    width: auto;
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}
.form-title {
    text-align: center;
    font-size: 1.8rem;
    font-weight: 600;
    color: #1976d2;
    margin-bottom: 30px;
}
.input-group {
    margin-bottom: 20px;
}
.input-group input {
    width: 100%;
    padding: 15px;
    border: 2px solid #bbdefb;
    border-radius: 10px;
    font-size: 1rem;
    background: rgba(255, 255, 255, 0.9);
    color: #1976d2;
    box-sizing: border-box;
    transition: border-color 0.3s ease;
}
.input-group input:focus {
    outline: none;
    border-color: #64b5f6;
    box-shadow: 0 0 0 3px rgba(100, 181, 246, 0.1);
}
.login-btn {
    width: 100%;
    padding: 15px;
    background: #81d4fa;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.login-btn:hover {
    background: #4fc3f7;
}
</style>
</head>
<body>
<div class="navbar">
    <div class="navbar-title">瑞辉智测平台</div>
</div>
<div class="login-container">
    <div class="login-form">
        <div class="logo-container">
            <img src="/{% endraw %}{{ logo }}{% raw %}" alt="瑞辉智测平台" class="login-logo">
        </div>
        <div class="form-title">用户登录</div>
        <form method="post">
            <div class="input-group">
                <input name="username" placeholder="用户名" autocomplete="username" required autofocus>
            </div>
            <div class="input-group">
                <input name="password" type="password" placeholder="密码" autocomplete="current-password" required>
            </div>
            <button class="login-btn" type="submit">登录</button>
        </form>
    </div>
</div>
</body></html>
{% endraw %}
''', logo=LOGO_FILENAME)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route("/")
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>瑞辉智测平台</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/RH_logo.png">
<style>
body { margin:0; font-family: 'Segoe UI', 'Arial', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #e3f2fd; }
.navbar { width:100%; height:60px; background:rgba(173,216,230,0.9); display:flex; align-items:center; padding:0 30px; box-shadow:0 2px 10px rgba(0,0,0,0.1); }
.navbar-title { color:white; font-size:1.5rem; font-weight:600; letter-spacing:1px; }
.menu { width:220px; background:#0d2236; min-height:100vh; position:fixed; top:0; left:0; color:#fff; }
.menu-title { font-size:1.3rem; font-weight:600; padding:30px 0 20px 0; text-align:center; letter-spacing:2px; }
.menu-list { list-style:none; padding:0; margin:0; }
.menu-list li { padding:18px 40px; cursor:pointer; font-size:1.1rem; transition:background 0.2s; }
.menu-list li.active, .menu-list li:hover { background:#1976d2; color:#fff; }
.main { margin-left:220px; padding:40px 20px; max-width:1200px; }
.operation-panel { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px); }
.panel-title { text-align: center; font-size: 1.8rem; font-weight: 600; color: #1976d2; margin-bottom: 30px; }
.btn-container { display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
.btn { padding: 15px 30px; border: none; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; min-width: 180px; }
.btn-run { background: #ffcdd2; color: #d32f2f; }
.btn-run:hover:not(:disabled) { background: #ef9a9a; transform: translateY(-2px); }
.btn-stop { background: #fff9c4; color: #f57f17; }
.btn-stop:hover:not(:disabled) { background: #fff59d; transform: translateY(-2px); }
.btn-report { background: #c8e6c9; color: #388e3c; }
.btn-report:hover:not(:disabled) { background: #a5d6a7; transform: translateY(-2px); }
.btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
.status-msg { text-align: center; font-size: 1.2rem; font-weight: 500; color: #f8bbd9; margin: 20px 0; min-height: 30px; }
.log-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 30px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px); }
.log-title { font-size: 1.3rem; font-weight: 600; color: #1976d2; margin-bottom: 20px; }
#log { background: rgba(255, 255, 255, 0.8); border: 2px solid #bbdefb; border-radius: 12px; padding: 20px; height: 400px; overflow-y: auto; font-family: 'Consolas', 'Monaco', 'Courier New', monospace; font-size: 0.9rem; line-height: 1.6; color: #1976d2; white-space: pre-wrap; word-wrap: break-word; }
@media (max-width: 768px) { .btn-container { flex-direction: column; align-items: center; } .btn { min-width: 200px; } .main { padding: 20px 10px; } .operation-panel, .log-container { padding: 20px; } }
</style>
</head>
<body>
<div class="navbar"><div class="navbar-title">瑞辉智测平台</div></div>
<div class="menu">
    <div class="menu-title">瑞辉智测平台</div>
    <ul class="menu-list">
        <li onclick="location.href='/'" class="active">测试面板</li>
        <li onclick="location.href='/schedule'">定时任务</li>
        <li onclick="location.href='/logout'">退出登录</li>
    </ul>
</div>
<div class="main">
    <div class="operation-panel">
        <div class="panel-title">测试操作面板</div>
        <div class="btn-container">
            <button class="btn btn-run" id="runBtn" onclick="runTest()">执行 main_execute.py</button>
            <button class="btn btn-stop" id="stopBtn" onclick="stopTest()">停止</button>
            <button class="btn btn-report" id="reportBtn" onclick="viewReport()" style="display:none">查看最新报告</button>
        </div>
        <div class="status-msg" id="msg"></div>
    </div>
    <div class="log-container">
        <div class="log-title">测试日志
            <select id="logSelect" style="margin-left:20px; padding:4px 10px; border-radius:8px; border:1px solid #bbdefb; font-size:1rem; background:#f5fafd; color:#1976d2;">
                <option value="run.log">run.log</option>
            </select>
            <button id="refreshLogBtn" style="margin-left:20px; padding:4px 16px; border-radius:8px; border:1px solid #bbdefb; font-size:1rem; background:#e3f2fd; color:#1976d2; cursor:pointer;">刷新</button>
        </div>
        <pre id="log"></pre>
    </div>
</div>
<script>
let logTimer = null;
let running = false;
let currentLog = 'run.log';
function fetchLogList() {
    fetch('/logs/list').then(r=>r.json()).then(data=>{
        const sel = document.getElementById('logSelect');
        sel.innerHTML = '';
        data.logs.forEach(f=>{
            const opt = document.createElement('option');
            opt.value = f;
            opt.textContent = f;
            sel.appendChild(opt);
        });
        sel.value = currentLog;
    });
}
document.addEventListener('DOMContentLoaded', function() {
    fetchLogList();
    document.getElementById('logSelect').addEventListener('change', function() {
        currentLog = this.value;
        if(logTimer) clearInterval(logTimer);
        loadLog();
        if(currentLog === 'run.log') startLog();
    });
});
function loadLog() {
    fetch(`/log?filename=${encodeURIComponent(currentLog)}`).then(r=>r.text()).then(txt=>{
        let logElem = document.getElementById('log');
        logElem.innerText = txt;
        logElem.scrollTop = logElem.scrollHeight;
    });
}
function runTest() {
    document.getElementById('msg').innerText = '正在执行，请稍候...';
    document.getElementById('reportBtn').style.display = 'none';
    document.getElementById('runBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;
    running = true;
    fetch('/run-tests', {method: 'POST'})
    .then(r => r.json())
    .then(data => {
        if(data.success){
            currentLog = 'run.log';
            document.getElementById('logSelect').value = 'run.log';
            startLog();
        }else{
            document.getElementById('msg').innerText = '执行失败：' + data.error;
            document.getElementById('runBtn').disabled = false;
        }
    });
}
function stopTest() {
    fetch('/stop-tests', {method: 'POST'})
    .then(r => r.json())
    .then(data => {
        if(data.success){
            document.getElementById('msg').innerText = '已请求停止';
        }else{
            document.getElementById('msg').innerText = '停止失败：' + data.error;
        }
        document.getElementById('stopBtn').disabled = true;
    });
}
function startLog() {
    if(logTimer) clearInterval(logTimer);
    logTimer = setInterval(()=>{
        if(currentLog !== 'run.log') { clearInterval(logTimer); return; }
        fetch(`/log?filename=run.log`).then(r=>r.text()).then(txt=>{
            let logElem = document.getElementById('log');
            logElem.innerText = txt;
            logElem.scrollTop = logElem.scrollHeight;
            if(txt.includes('===TEST_FINISHED===')) {
                clearInterval(logTimer);
                document.getElementById('msg').innerText = '测试已完成！';
                document.getElementById('reportBtn').style.display = '';
                document.getElementById('runBtn').disabled = false;
                document.getElementById('stopBtn').disabled = true;
                running = false;
            }
        });
    }, 2000);
}
function viewReport() {
    fetch('/latest-report').then(r=>r.json()).then(data=>{
        if(data.url){
            window.open(data.url, '_blank');
        }else{
            alert('未找到最新报告');
        }
    });
}
loadLog();
document.getElementById('runBtn').disabled = false;
document.getElementById('stopBtn').disabled = true;
document.getElementById('refreshLogBtn').addEventListener('click', function() {
    loadLog();
});
if(currentLog === 'run.log') startLog();
</script>
</body></html>
''', logo=LOGO_FILENAME)

@app.route("/run-tests", methods=["POST"])
def run_tests():
    def run_script():
        try:
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                f.write('')
        except Exception:
            pass
        proc = subprocess.Popen([
            os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"), MAIN_EXEC
        ])
        current_process['proc'] = proc
        proc.wait()
        current_process['proc'] = None
    t = threading.Thread(target=run_script, daemon=True)
    t.start()
    return jsonify({"success": True})

@app.route("/stop-tests", methods=["POST"])
def stop_tests():
    proc = current_process.get('proc')
    if proc and proc.poll() is None:
        try:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            current_process['proc'] = None
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    else:
        return jsonify({"success": False, "error": "没有正在运行的测试进程"})

@app.route("/logs/list")
def list_logs():
    log_files = glob.glob(os.path.join("Log", "*.log"))
    log_files = [os.path.basename(f) for f in log_files]
    if os.path.exists("run.log"):
        log_files = ["run.log"] + [f for f in log_files if f != "run.log"]
    return jsonify({"logs": log_files})

@app.route("/reports/list")
def list_reports():
    report_root = REPORT_ROOT
    dirs = [d for d in os.listdir(report_root) if os.path.isdir(os.path.join(report_root, d))]
    reports = []
    for d in sorted(dirs, reverse=True):
        path = os.path.join(report_root, d)
        count = get_report_case_count(path)
        reports.append({"dir": d, "count": count})
    return jsonify({"reports": reports})

@app.route("/log")
def get_log():
    filename = request.args.get("filename", "run.log")
    if filename == "run.log":
        path = "run.log"
    else:
        path = os.path.join("Log", filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()[-5000:]
        return Response(content, mimetype="text/plain; charset=utf-8")
    except Exception as e:
        return Response(str(e), mimetype="text/plain; charset=utf-8")

@app.route("/latest-report")
def latest_report():
    url = get_latest_report_url()
    return jsonify({"url": url})

@app.route("/report")
def report_root():
    url = get_latest_report_url()
    if url:
        return redirect(url)
    return "未找到测试报告", 404

@app.route("/report/<path:subpath>")
def report(subpath):
    return send_from_directory(REPORT_ROOT, subpath)

@app.route("/schedule", methods=["GET"])
def schedule_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>定时任务 - 瑞辉智测平台</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/png" href="/RH_logo.png">
<style>
body { margin:0; font-family: 'Segoe UI', 'Arial', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f5fafd; }
.navbar { width:100%; height:60px; background:rgba(173,216,230,0.9); display:flex; align-items:center; padding:0 30px; box-shadow:0 2px 10px rgba(0,0,0,0.1); }
.navbar-title { color:white; font-size:1.5rem; font-weight:600; letter-spacing:1px; }
.menu { width:220px; background:#0d2236; min-height:100vh; position:fixed; top:0; left:0; color:#fff; }
.menu-title { font-size:1.3rem; font-weight:600; padding:30px 0 20px 0; text-align:center; letter-spacing:2px; }
.menu-list { list-style:none; padding:0; margin:0; }
.menu-list li { padding:18px 40px; cursor:pointer; font-size:1.1rem; transition:background 0.2s; }
.menu-list li.active, .menu-list li:hover { background:#1976d2; color:#fff; }
.main { margin-left:220px; padding:40px 20px; max-width:700px; }
.panel { background:#fff; border-radius:18px; box-shadow:0 4px 24px rgba(0,0,0,0.08); padding:40px; }
.panel-title { font-size:1.6rem; font-weight:600; color:#1976d2; margin-bottom:30px; text-align:center; }
.status { font-size:1.1rem; color:#388e3c; margin-bottom:18px; text-align:center; }
.btn { padding:10px 32px; border:none; border-radius:10px; background:#1976d2; color:white; font-size:1.1rem; font-weight:600; cursor:pointer; transition:background 0.2s; }
.btn:disabled { opacity:0.6; cursor:not-allowed; }
.task-list { margin-bottom:30px; }
.task-item { background:#f5fafd; border-radius:10px; padding:18px 20px; margin-bottom:16px; box-shadow:0 2px 8px rgba(0,0,0,0.04); display:flex; align-items:center; justify-content:space-between; }
.task-info { font-size:1.1rem; color:#1976d2; }
.task-actions button { margin-left:10px; }
.form-row { display:flex; align-items:center; margin-bottom:18px; }
.form-label { width:120px; font-size:1.1rem; color:#1976d2; }
input[type="number"], select { padding:8px 16px; border-radius:8px; border:1px solid #bbdefb; font-size:1rem; margin-right:16px; }
.switch { position:relative; display:inline-block; width:52px; height:28px; }
.switch input { opacity:0; width:0; height:0; }
.slider { position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background:#ccc; transition:.4s; border-radius:28px; }
.slider:before { position:absolute; content:""; height:22px; width:22px; left:3px; bottom:3px; background:white; transition:.4s; border-radius:50%; }
input:checked + .slider { background:#1976d2; }
input:checked + .slider:before { transform:translateX(24px); }
</style>
</head>
<body>
<div class="navbar"><div class="navbar-title">瑞辉智测平台</div></div>
<div class="menu">
    <div class="menu-title">瑞辉智测平台</div>
    <ul class="menu-list">
        <li onclick="location.href='/'">测试面板</li>
        <li onclick="location.href='/schedule'" class="active">定时任务</li>
        <li onclick="location.href='/logout'">退出登录</li>
    </ul>
</div>
<div class="main">
    <div class="panel">
        <div class="panel-title">定时任务配置</div>
        <div class="status" id="status"></div>
        <div class="task-list" id="taskList"></div>
        <div style="border-top:1px solid #e3e3e3; margin:30px 0;"></div>
        <div style="font-size:1.2rem; color:#1976d2; margin-bottom:18px;">新增/编辑任务</div>
        <div class="form-row">
            <span class="form-label">周期类型</span>
            <select id="typeSelect">
                <option value="daily">每天</option>
                <option value="weekly">每周</option>
                <option value="monthly">每月</option>
            </select>
        </div>
        <div class="form-row" id="hourRow">
            <span class="form-label">小时(0-23)</span>
            <input type="number" id="hourInput" min="0" max="23">
        </div>
        <div class="form-row" id="weekdayRow" style="display:none;">
            <span class="form-label">星期(0=周一,6=周日)</span>
            <select id="weekdayInput">
                <option value="0">周一</option><option value="1">周二</option><option value="2">周三</option><option value="3">周四</option><option value="4">周五</option><option value="5">周六</option><option value="6">周日</option>
            </select>
        </div>
        <div class="form-row" id="dayRow" style="display:none;">
            <span class="form-label">日期(1-28)</span>
            <input type="number" id="dayInput" min="1" max="28">
        </div>
        <div class="form-row">
            <span class="form-label">启用</span>
            <label class="switch">
                <input type="checkbox" id="enableSwitch">
                <span class="slider"></span>
            </label>
        </div>
        <div style="text-align:center; margin-top:20px;">
            <button class="btn" id="saveBtn">保存任务</button>
            <button class="btn" id="resetBtn" style="background:#bdbdbd;">重置</button>
        </div>
    </div>
</div>
<script>
let editingId = null;
function showStatus(msg, ok) {
    let s = document.getElementById('status');
    s.innerText = msg;
    s.style.color = ok ? '#388e3c' : '#d32f2f';
}
function updateForm(task) {
    document.getElementById('typeSelect').value = task.type;
    document.getElementById('hourInput').value = task.hour;
    document.getElementById('weekdayInput').value = task.weekday || 0;
    document.getElementById('dayInput').value = task.day || 1;
    document.getElementById('enableSwitch').checked = !!task.enabled;
    document.getElementById('weekdayRow').style.display = task.type==='weekly' ? '' : 'none';
    document.getElementById('dayRow').style.display = task.type==='monthly' ? '' : 'none';
}
document.getElementById('typeSelect').addEventListener('change', function() {
    let t = this.value;
    document.getElementById('weekdayRow').style.display = t==='weekly' ? '' : 'none';
    document.getElementById('dayRow').style.display = t==='monthly' ? '' : 'none';
});
document.getElementById('saveBtn').onclick = function() {
    let task = {
        id: editingId || null,
        type: document.getElementById('typeSelect').value,
        hour: parseInt(document.getElementById('hourInput').value)||0,
        weekday: parseInt(document.getElementById('weekdayInput').value)||0,
        day: parseInt(document.getElementById('dayInput').value)||1,
        enabled: document.getElementById('enableSwitch').checked
    };
    fetch('/schedule/task', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(task)})
    .then(r=>r.json()).then(data=>{
        showStatus(data.msg, data.success);
        if(data.success) { loadTasks(); document.getElementById('resetBtn').click(); }
    });
};
document.getElementById('resetBtn').onclick = function() {
    editingId = null;
    updateForm({type:'daily', hour:0, weekday:0, day:1, enabled:true});
};
function loadTasks() {
    fetch('/schedule/task').then(r=>r.json()).then(list=>{
        let html = '';
        if(list.length===0) html = '<div style="color:#bdbdbd;text-align:center;">暂无定时任务</div>';
        list.forEach(t=>{
            let desc = t.type==='daily' ? `每天 ${t.hour}:00` : t.type==='weekly' ? `每周${['一','二','三','四','五','六','日'][t.weekday]} ${t.hour}:00` : `每月${t.day}日 ${t.hour}:00`;
            html += `<div class='task-item'><div class='task-info'>${desc} ${t.enabled?'<span style='color:#388e3c;'>(启用)</span>':'<span style='color:#d32f2f;'>(停用)</span>'}</div><div class='task-actions'><button class='btn' onclick='editTask("${t.id}")'>编辑</button><button class='btn' style='background:#bdbdbd;' onclick='delTask("${t.id}")'>删除</button><button class='btn' style='background:${t.enabled?'#bdbdbd':'#388e3c'};' onclick='toggleTask("${t.id}",${!t.enabled})'>${t.enabled?'停用':'启用'}</button></div></div>`;
        });
        document.getElementById('taskList').innerHTML = html;
    });
}
function editTask(id) {
    fetch('/schedule/task?id='+id).then(r=>r.json()).then(t=>{
        editingId = t.id;
        updateForm(t);
    });
}
function delTask(id) {
    if(!confirm('确定要删除该任务吗？')) return;
    fetch('/schedule/task?id='+id, {method:'DELETE'}).then(r=>r.json()).then(data=>{
        showStatus(data.msg, data.success); loadTasks();
    });
}
function toggleTask(id, enable) {
    fetch('/schedule/task/toggle', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({id, enable})})
    .then(r=>r.json()).then(data=>{ showStatus(data.msg, data.success); loadTasks(); });
}
loadTasks();
document.getElementById('resetBtn').click();
</script>
</body></html>
''')

@app.route("/schedule/task", methods=["GET", "POST", "DELETE"])
def schedule_task():
    if request.method == 'GET':
        tid = request.args.get('id')
        cfg_list = load_schedule_config()
        if tid:
            for t in cfg_list:
                if t['id'] == tid:
                    return jsonify(t)
            return jsonify({}), 404
        else:
            return jsonify(cfg_list)
    elif request.method == 'POST':
        task = request.get_json()
        cfg_list = load_schedule_config()
        if not task.get('id'):
            task['id'] = str(uuid.uuid4())
            cfg_list.append(task)
        else:
            for i, t in enumerate(cfg_list):
                if t['id'] == task['id']:
                    cfg_list[i] = task
                    break
            else:
                cfg_list.append(task)
        save_schedule_config(cfg_list)
        update_scheduler()
        return jsonify({"success": True, "msg": "任务已保存"})
    elif request.method == 'DELETE':
        tid = request.args.get('id')
        cfg_list = load_schedule_config()
        cfg_list = [t for t in cfg_list if t['id'] != tid]
        save_schedule_config(cfg_list)
        update_scheduler()
        return jsonify({"success": True, "msg": "任务已删除"})
    # 兜底，理论不会走到这里
    return jsonify({}), 404

@app.route("/schedule/task/toggle", methods=["POST"])
def schedule_task_toggle():
    data = request.get_json()
    tid = data.get('id')
    enable = data.get('enable')
    cfg_list = load_schedule_config()
    for t in cfg_list:
        if t['id'] == tid:
            t['enabled'] = enable
    save_schedule_config(cfg_list)
    update_scheduler()
    return jsonify({"success": True, "msg": "任务状态已更新"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 