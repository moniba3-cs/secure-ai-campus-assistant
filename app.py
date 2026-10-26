"""Flask web app: chat UI, /api/chat, approval queue and security dashboard."""
from flask import Flask, jsonify, render_template_string, request

import monitor
import security as sec
import tools
from assistant import handle_chat

app = Flask(__name__)

PAGE = """<!doctype html><title>Secure AI Campus Assistant</title>
<style>body{font-family:system-ui;max-width:760px;margin:30px auto;padding:0 12px}
#log{border:1px solid #ccc;border-radius:8px;padding:12px;height:340px;overflow:auto;white-space:pre-wrap}
input,select,button{padding:8px;margin:4px 0}input#m{width:62%}</style>
<h2>Secure AI Campus Assistant</h2>
<div>User: <select id=u>{% for k in users %}<option>{{k}}</option>{% endfor %}</select>
Mode: <select id=s><option value=1>secure</option><option value=0>vulnerable (baseline)</option></select>
<a href="/dashboard">Dashboard</a></div>
<div id=log></div>
<input id=m placeholder="Ask about extensions, fees, internships, your grades..." onkeydown="if(event.key=='Enter')go()">
<button onclick="go()">Send</button>
<script>
async function go(){const m=document.getElementById('m'),l=document.getElementById('log');
l.textContent+='\\nYou: '+m.value;
const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({user:u.value,message:m.value,secure:s.value=='1'})});
const j=await r.json();l.textContent+='\\nAssistant: '+j.answer+'\\n';m.value='';l.scrollTop=l.scrollHeight}
</script>"""

DASH = """<!doctype html><title>Security Dashboard</title>
<style>body{font-family:system-ui;max-width:900px;margin:30px auto;padding:0 12px}
td,th{border:1px solid #ccc;padding:6px;font-size:13px}table{border-collapse:collapse;width:100%}
.high{background:#fdd}.medium{background:#ffe9c4}</style>
<h2>Security Dashboard</h2><a href="/">Back to chat</a>
<p>Total events: <b>{{s.total}}</b> | Alerts: <b>{{s.alerts}}</b> | Pending approvals: <b>{{pending|length}}</b></p>
<h3>Events by type</h3><table>{% for k,v in s.by_type.items() %}<tr><td>{{k}}</td><td>{{v}}</td></tr>{% endfor %}</table>
<h3>Alerts by user</h3><table>{% for k,v in s.alerts_by_user.items() %}<tr><td>{{k}}</td><td>{{v}}</td></tr>{% endfor %}</table>
<h3>Recent alerts</h3><table><tr><th>Type</th><th>User</th><th>Mode</th><th>Severity</th><th>Details</th></tr>
{% for e in s.recent_alerts %}<tr class="{{e.severity}}"><td>{{e.type}}</td><td>{{e.user}}</td><td>{{e.mode}}</td>
<td>{{e.severity}}</td><td>{{e.details}}</td></tr>{% endfor %}</table>
<h3>Pending email approvals</h3><table>{% for p in pending %}<tr><td>{{loop.index0}}</td><td>{{p.user}}</td>
<td>{{p.args}}</td><td><form method=post action="/approve/{{loop.index0}}"><button>Approve</button></form></td></tr>{% endfor %}</table>"""


@app.get("/")
def index():
    return render_template_string(PAGE, users=list(sec.USERS))


@app.post("/api/chat")
def chat():
    d = request.get_json(force=True)
    res = handle_chat(d.get("user", ""), d.get("message", ""), secure=bool(d.get("secure", True)))
    return jsonify(res)


@app.get("/dashboard")
def dashboard():
    return render_template_string(DASH, s=monitor.summary(), pending=tools.PENDING)


@app.post("/approve/<int:i>")
def approve(i):
    if 0 <= i < len(tools.PENDING):
        p = tools.PENDING.pop(i)
        tools.run_tool(p["name"], p["args"])
        monitor.log_event("tool_approved", p["user"], "secure", name=p["name"])
    return dashboard()


if __name__ == "__main__":
    app.run(debug=False, port=5000)
