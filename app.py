# app.py
import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from scanner import scan_network

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

SETTINGS_FILE = '/app/smtp/settings.json'

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

@app.route('/')
def dashboard():
    try:
        with open('/app/data/scan_results.json', 'r') as f:
            scan_results = json.load(f)
    except FileNotFoundError:
        scan_results = []

    return render_template('dashboard.html', scan_results=scan_results)

@app.route('/scan', methods=['POST'])
def on_demand_scan():
    ip_range = request.form['ip_range']
    network_type = request.form.get('network_type', 'host')
    try:
        scan_results = scan_network(ip_range, network_type)
        hosts = [{'ip': host, 'status': state, 'open_ports': open_ports} for host, state, open_ports in scan_results]
        with open('/app/data/scan_results.json', 'w') as f:
            json.dump(hosts, f)
        return jsonify(hosts)
    except Exception as e:
        logging.error(f"An error occurred during the on-demand network scan: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        smtp_settings = {
            'SMTP_SERVER': request.form['smtp_server'],
            'SMTP_PORT': request.form['smtp_port'],
            'SMTP_USER': request.form['smtp_user'],
            'SMTP_PASSWORD': request.form['smtp_password'],
            'IP_RANGE': request.form['ip_range']
        }
        save_settings(smtp_settings)
        return redirect(url_for('dashboard'))
    settings = load_settings()
    return render_template('settings.html', settings=settings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
