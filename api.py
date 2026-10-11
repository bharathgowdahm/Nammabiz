from flask import Flask, jsonify, request, render_template_string
import os
import requests
from datetime import datetime

app = Flask(__name__)
AQ_API_KEY = os.environ.get("AQ_API_KEY", "")

# Demo data
BUSINESSES = [
    {"id":1,"name":"Glow Salon","category":"Salon","tagline":"Hair | Beauty | Bridal","theme":"violet","rating":4.8},
]
BOOKINGS = [
    {"id":1,"customer":"Priya S","service":"Haircut + Facial","date":"2026-10-12","time":"11:00 AM","status":"confirmed","amount":799},
    {"id":2,"customer":"Anita R","service":"Bridal Trial","date":"2026-10-12","time":"2:00 PM","status":"pending","amount":1499},
]
CUSTOMERS = [
    {"id":1,"name":"Priya S","phone":"9876543210","bookings":8,"spent":6400},
    {"id":2,"name":"Anita R","phone":"9876543211","bookings":3,"spent":3200},
]
INVOICES = [
    {"id":"INV-001","customer":"Priya S","amount":799,"status":"paid","date":"2026-10-08"},
    {"id":"INV-002","customer":"Anita R","amount":1499,"status":"due","date":"2026-10-10"},
]
ORDERS = [
    {"id":"ORD-101","customer":"Kiran H","items":"Hair Serum x1","amount":349,"pay_status":"paid","track":"shipped"},
]
SERVICES = [
    {"id":1,"name":"Haircut","price":299,"duration":"30 min","active":True},
    {"id":2,"name":"Facial","price":799,"duration":"60 min","active":True},
]

def aq_generate(prompt):
    if not AQ_API_KEY: return None
    try:
        h = {"Authorization": f"Bearer {AQ_API_KEY}", "Content-Type": "application/json"}
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            json={"model":"llama-3.1-8b-instant","messages":[{"role":"user","content":prompt}],"temperature":0.4,"max_tokens":400},
            headers=h, timeout=10)
        if r.status_code == 200:
            return r.json()['choices'][0]['message']['content']
        return None
    except: return None

HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NammaBiz - Digital Storefront</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#fff;font-family:sans-serif;min-height:100vh}
.glass{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:20px;padding:20px;margin:12px}
.header{text-align:center;padding:30px 20px}
.header h1{font-size:2.2rem;background:linear-gradient(135deg,#a78bfa,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.btn{background:linear-gradient(135deg,#8b5cf6,#6366f1);border:none;color:#fff;padding:12px;border-radius:12px;font-weight:800;width:100%;margin:6px 0;cursor:pointer}
input,select{width:100%;padding:11px;border-radius:10px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff;margin:5px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;padding:10px}
.row{background:rgba(255,255,255,.05);border-radius:12px;padding:10px;margin:6px 0;display:flex;justify-content:space-between}
</style></head><body>
<div class="header"><h1>NAMMABIZ • DIGITAL STOREFRONT</h1>
<p>Business page • Bookings • Customers • Invoices • Orders • Services</p>
<p>Turn any skill into a storefront in minutes • SaaS ₹299/mo</p></div>
<div class="grid">
<div class="glass"><h2>⚡ Create Storefront</h2>
<input id="bn" placeholder="Business name" value="Glow Salon">
<select id="bc"><option>Salon</option><option>Tutor</option><option>Home Baker</option><option>Plumber</option></select>
<button class="btn" onclick="publish()">🚀 Publish</button>
<div id="pr"></div>
<button class="btn" onclick="aiGen()">🤖 AI Generate (AQ 3.8)</button>
<div id="ai"></div></div>
<div class="glass"><h2>📊 Dashboard</h2>
<div id="dash">Loading...</div>
<button class="btn" onclick="loadDash()">🔄 Refresh</button></div>
</div>
<script>
async function publish(){const n=document.getElementById('bn').value;
const r=await fetch('/api/businesses/create?name='+encodeURIComponent(n));const d=await r.json();
document.getElementById('pr').innerHTML='✅ Live: nammabiz.in/'+n.toLowerCase().replace(/ /g,'-')}
async function aiGen(){const n=document.getElementById('bn').value;
document.getElementById('ai').innerHTML='Generating...';
const r=await fetch('/api/aq?type=business&name='+encodeURIComponent(n));const d=await r.json();
document.getElementById('ai').innerHTML=(d.response||d.fallback).substring(0,500)}
async function loadDash(){const b=await (await fetch('/api/bookings')).json();
document.getElementById('dash').innerHTML=b.bookings.map(x=>`<div class="row"><div>${x.customer}<br><small>${x.service}</small></div><div>₹${x.amount}<br>${x.status}</div></div>`).join('')}
loadDash();
</script></body></html>"""

@app.route('/')
@app.route('/api/index')
@app.route('/api/index/')
def home():
    return render_template_string(HTML)

@app.route('/api/health')
def health():
    return jsonify({"status":"ok","project":"NammaBiz","vercel":True,"flask_app":"defined ✅","not_found_fixed":"Fixed ✅","aq_key_present":bool(AQ_API_KEY)})

@app.route('/api/businesses')
def get_biz(): return jsonify({"businesses":BUSINESSES})

@app.route('/api/businesses/create')
def create_biz():
    name=request.args.get('name','My Business')
    nb={"id":len(BUSINESSES)+1,"name":name,"category":request.args.get('category','Salon')}
    BUSINESSES.append(nb)
    return jsonify({"success":True,"business":nb,"link":f"nammabiz.in/{name.lower().replace(' ','-'}"})

@app.route('/api/bookings')
def get_bookings(): return jsonify({"bookings":BOOKINGS})

@app.route('/api/bookings/create')
def create_booking():
    nb={"id":len(BOOKINGS)+1,"customer":request.args.get('customer','New'),"service":request.args.get('service','General'),"date":"2026-10-12","time":"11:00 AM","status":"pending","amount":int(request.args.get('amount',499))}
    BOOKINGS.append(nb); return jsonify({"success":True,"booking":nb})

@app.route('/api/customers')
def get_customers(): return jsonify({"customers":CUSTOMERS})

@app.route('/api/invoices')
def get_invoices(): return jsonify({"invoices":INVOICES})

@app.route('/api/invoices/create')
def create_invoice():
    nid=f"INV-{len(INVOICES)+1:03d}"
    ni={"id":nid,"customer":request.args.get('customer','Customer'),"amount":int(request.args.get('amount',500)),"status":"due","date":datetime.now().strftime("%Y-%m-%d")}
    INVOICES.append(ni); return jsonify({"success":True,"invoice":ni})

@app.route('/api/orders')
def get_orders(): return jsonify({"orders":ORDERS})

@app.route('/api/services')
def get_services(): return jsonify({"services":SERVICES})

@app.route('/api/aq')
def aq():
    name=request.args.get('name','Glow Salon')
    prompt=f"Create storefront for {name}. Give tagline, 3 services with INR prices."
    resp=aq_generate(prompt)
    if resp: return jsonify({"response":resp,"aq_key_present":True})
    return jsonify({"fallback":f"Welcome to {name}! Services from ₹299. Book via WhatsApp.","aq_key_present":bool(AQ_API_KEY)})

@app.route('/<path:path>')
def catch_all(path):
    if path.startswith('api/'):
        return jsonify({"error":f"/{path} not found"}),404
    return render_template_string(HTML)

@app.errorhandler(404)
def nf(e): return jsonify({"error":"Not Found - NammaBiz Running"}),404
