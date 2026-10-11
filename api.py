
from flask import Flask, jsonify, request, render_template_string
import os
import requests
from datetime import datetime

app = Flask(__name__)
AQ_API_KEY = os.environ.get("AQ_API_KEY", "")

BUSINESSES = [
    {"id": 1, "name": "Glow Salon", "category": "Salon", "tagline": "Hair | Beauty | Bridal", "rating": 4.8},
    {"id": 2, "name": "Ravi Tutors", "category": "Tutor", "tagline": "Maths & Science", "rating": 4.9},
]
BOOKINGS = [
    {"id": 1, "customer": "Priya S", "service": "Haircut + Facial", "date": "2026-10-12", "time": "11:00 AM", "status": "confirmed", "amount": 799},
    {"id": 2, "customer": "Anita R", "service": "Bridal Trial", "date": "2026-10-12", "time": "2:00 PM", "status": "pending", "amount": 1499},
]
CUSTOMERS = [
    {"id": 1, "name": "Priya S", "phone": "9876543210", "bookings": 8, "spent": 6400},
    {"id": 2, "name": "Anita R", "phone": "9876543211", "bookings": 3, "spent": 3200},
]
INVOICES = [
    {"id": "INV-001", "customer": "Priya S", "amount": 799, "status": "paid", "date": "2026-10-08"},
    {"id": "INV-002", "customer": "Anita R", "amount": 1499, "status": "due", "date": "2026-10-10"},
]
ORDERS = [
    {"id": "ORD-101", "customer": "Kiran H", "items": "Hair Serum x1", "amount": 349, "pay_status": "paid", "track": "shipped"},
]
SERVICES = [
    {"id": 1, "name": "Haircut", "price": 299, "duration": "30 min", "active": True},
    {"id": 2, "name": "Facial", "price": 799, "duration": "60 min", "active": True},
]

def aq_generate(prompt_text):
    if not AQ_API_KEY:
        return None
    try:
        headers = {"Authorization": "Bearer " + AQ_API_KEY, "Content-Type": "application/json"}
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {"model": "llama-3.1-8b-instant",
                   "messages": [{"role": "user", "content": prompt_text}],
                   "temperature": 0.4, "max_tokens": 400}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return None
    except Exception:
        return None

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NammaBiz - Digital Storefront Platform</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#fff;font-family:sans-serif;min-height:100vh}
.glass{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:20px;padding:20px;margin:12px}
.header{text-align:center;padding:30px 20px}
.header h1{font-size:2.2rem;background:linear-gradient(135deg,#a78bfa,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.btn{background:linear-gradient(135deg,#8b5cf6,#6366f1);border:none;color:#fff;padding:12px;border-radius:12px;font-weight:800;width:100%;margin:6px 0;cursor:pointer}
input,select{width:100%;padding:11px;border-radius:10px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff;margin:5px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;padding:10px}
.row{background:rgba(255,255,255,.05);border-radius:12px;padding:10px;margin:6px 0;display:flex;justify-content:space-between;align-items:center}
.badge{display:inline-block;background:rgba(34,197,94,.18);border:1px solid rgba(34,197,94,.35);padding:5px 12px;border-radius:20px;font-size:.78rem;font-weight:800;margin:3px}
</style>
</head>
<body>
<div class="header">
<h1>NAMMABIZ - DIGITAL STOREFRONT</h1>
<p>Business page | Bookings | Customers | Invoices | Orders | Services</p>
<p style="margin-top:8px"><span class="badge">Vercel Only</span><span class="badge">Flask Top-Level</span><span class="badge">Not Found Fixed</span><span class="badge">AQ 3.8</span></p>
<p style="color:#a78bfa;margin-top:8px;font-weight:700">Turn any skill into a storefront in minutes - SaaS Rs.299/mo</p>
</div>
<div class="grid">
<div class="glass">
<h2>Create Storefront</h2>
<input id="bn" placeholder="Business name" value="Glow Salon">
<select id="bc"><option>Salon</option><option>Tutor</option><option>Home Baker</option><option>Plumber</option><option>Tailor</option></select>
<button class="btn" onclick="publish()">Publish Storefront</button>
<div id="pr" style="margin-top:8px"></div>
<button class="btn" style="background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#000" onclick="aiGen()">AI Generate (AQ 3.8)</button>
<div id="ai" style="margin-top:8px;font-size:.9rem;color:#cbd5e1"></div>
</div>
<div class="glass">
<h2>Dashboard - Bookings</h2>
<div id="dash">Loading...</div>
<button class="btn" onclick="loadDash()">Refresh</button>
<div style="margin-top:10px">
<button class="btn" style="background:#334155" onclick="window.open('/api/health','_blank')">Open /api/health</button>
</div>
</div>
</div>
<div class="glass">
<h2>All APIs</h2>
<p style="color:#94a3b8;font-size:.9rem">/api/businesses | /api/bookings | /api/customers | /api/invoices | /api/orders | /api/services | /api/aq</p>
</div>
<script>
async function publish(){
  var n=document.getElementById('bn').value;
  var r=await fetch('/api/businesses/create?name='+encodeURIComponent(n));
  var d=await r.json();
  document.getElementById('pr').innerHTML='Live: <b>'+d.link+'</b>';
}
async function aiGen(){
  var n=document.getElementById('bn').value;
  document.getElementById('ai').innerHTML='Generating...';
  var r=await fetch('/api/aq?type=business&name='+encodeURIComponent(n));
  var d=await r.json();
  var t=d.response||d.fallback||'';
  document.getElementById('ai').innerHTML=t.substring(0,500);
}
async function loadDash(){
  var r=await fetch('/api/bookings');
  var d=await r.json();
  var html='';
  d.bookings.forEach(function(x){
    html+='<div class="row"><div><b>'+x.customer+'</b><br><small>'+x.service+'</small></div><div>Rs.'+x.amount+'<br>'+x.status+'</div></div>';
  });
  document.getElementById('dash').innerHTML=html;
}
loadDash();
</script>
</body>
</html>
'''

@app.route('/')
@app.route('/api')
@app.route('/api/')
@app.route('/api/index')
@app.route('/api/index/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/health')
@app.route('/api/health/')
def health():
    return jsonify({
        "status": "ok",
        "project": "NammaBiz - Digital Storefront Platform",
        "vercel": True,
        "flask_app": "defined at top-level",
        "build": "fixed",
        "not_found_fixed": "Fixed - catch-all + /api/index routes",
        "aq_key_present": bool(AQ_API_KEY),
        "counts": {"businesses": len(BUSINESSES), "bookings": len(BOOKINGS),
                   "customers": len(CUSTOMERS), "invoices": len(INVOICES)},
        "endpoints": ["/", "/api/health", "/api/businesses", "/api/bookings",
                      "/api/customers", "/api/invoices", "/api/orders",
                      "/api/services", "/api/aq"]
    })

@app.route('/api/businesses')
@app.route('/api/businesses/')
def get_biz():
    return jsonify({"businesses": BUSINESSES, "count": len(BUSINESSES)})

@app.route('/api/businesses/create')
@app.route('/api/businesses/create/')
def create_biz():
    name = request.args.get('name', 'My Business')
    slug = name.lower().replace(' ', '-')
    nb = {"id": len(BUSINESSES) + 1, "name": name,
          "category": request.args.get('category', 'Salon'), "rating": 5.0}
    BUSINESSES.append(nb)
    return jsonify({"success": True, "business": nb, "link": "nammabiz.in/" + slug})

@app.route('/api/bookings')
@app.route('/api/bookings/')
def get_bookings():
    return jsonify({"bookings": BOOKINGS, "count": len(BOOKINGS)})

@app.route('/api/bookings/create')
@app.route('/api/bookings/create/')
def create_booking():
    nb = {"id": len(BOOKINGS) + 1,
          "customer": request.args.get('customer', 'New Customer'),
          "service": request.args.get('service', 'General'),
          "date": "2026-10-12", "time": "11:00 AM",
          "status": "pending",
          "amount": int(request.args.get('amount', 499))}
    BOOKINGS.append(nb)
    return jsonify({"success": True, "booking": nb})

@app.route('/api/customers')
@app.route('/api/customers/')
def get_customers():
    return jsonify({"customers": CUSTOMERS, "count": len(CUSTOMERS)})

@app.route('/api/invoices')
@app.route('/api/invoices/')
def get_invoices():
    return jsonify({"invoices": INVOICES, "count": len(INVOICES)})

@app.route('/api/invoices/create')
@app.route('/api/invoices/create/')
def create_invoice():
    nid = "INV-%03d" % (len(INVOICES) + 1)
    ni = {"id": nid, "customer": request.args.get('customer', 'Customer'),
          "amount": int(request.args.get('amount', 500)),
          "status": "due", "date": datetime.now().strftime("%Y-%m-%d")}
    INVOICES.append(ni)
    return jsonify({"success": True, "invoice": ni})

@app.route('/api/orders')
@app.route('/api/orders/')
def get_orders():
    return jsonify({"orders": ORDERS, "count": len(ORDERS)})

@app.route('/api/services')
@app.route('/api/services/')
def get_services():
    return jsonify({"services": SERVICES, "count": len(SERVICES)})

@app.route('/api/aq')
@app.route('/api/aq/')
def aq():
    name = request.args.get('name', 'Glow Salon')
    category = request.args.get('category', 'Salon')
    prompt = "Create a digital storefront for '%s' (%s). Give tagline, 3 services with INR prices, welcome message. Short." % (name, category)
    resp = aq_generate(prompt)
    if resp:
        return jsonify({"type": "business", "name": name, "response": resp, "aq_key_present": True})
    return jsonify({"type": "business", "name": name,
                    "fallback": "Welcome to %s! Best %s in town. Services from Rs.299. Book in 30 seconds via WhatsApp." % (name, category),
                    "aq_key_present": bool(AQ_API_KEY),
                    "note": "Set AQ_API_KEY in Vercel env for live AI"})

@app.route('/<path:path>')
def catch_all(path):
    if path.startswith('api/'):
        return jsonify({"error": "API /%s not found" % path,
                        "hint": "Use /api/health, /api/businesses, /api/bookings, /api/customers, /api/invoices, /api/orders, /api/services, /api/aq"}), 404
    return render_template_string(HTML_TEMPLATE)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found - NammaBiz running",
                    "hint": "Use /, /api/index, /api/health"}), 404
