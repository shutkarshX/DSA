# ============================================================
#   Student Admission Record Management System
#   Backend: Python Flask | Storage: CSV Files
#   Author: Auto-generated | Version: 1.0
# ============================================================

from flask import Flask, request, redirect, url_for, flash, jsonify
from flask import render_template_string
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "admission_secret_key_2024"

# ─────────────────────────────────────────────
#  FILE PATHS
# ─────────────────────────────────────────────
STUDENTS_FILE  = "students.csv"
COURSES_FILE   = "courses.csv"
ADMISSIONS_FILE = "admissions.csv"

STUDENT_FIELDS   = ["student_id","name","age","gender","contact","address"]
COURSE_FIELDS    = ["course_id","course_name","department","duration"]
ADMISSION_FIELDS = ["admission_id","student_id","course_id","admission_date","status"]

# ─────────────────────────────────────────────
#  CSV HELPERS
# ─────────────────────────────────────────────
def init_csv(filepath, fieldnames):
    """Create CSV with headers if it does not exist."""
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

def read_csv(filepath, fieldnames):
    """Read all rows from a CSV file into a list of dicts."""
    init_csv(filepath, fieldnames)
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows

def write_csv(filepath, fieldnames, rows):
    """Overwrite CSV file with the given list of dicts."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# ─────────────────────────────────────────────
#  DSA — Quick Sort  (manual implementation)
# ─────────────────────────────────────────────
def quick_sort(arr, key_func, reverse=False):
    """
    Quick-sort a list of dicts by key_func.
    Average O(n log n) time complexity.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    pivot_val = key_func(pivot)
    left   = [x for x in arr if (key_func(x) < pivot_val if not reverse else key_func(x) > pivot_val)]
    middle = [x for x in arr if key_func(x) == pivot_val]
    right  = [x for x in arr if (key_func(x) > pivot_val if not reverse else key_func(x) < pivot_val)]
    return quick_sort(left, key_func, reverse) + middle + quick_sort(right, key_func, reverse)

# ─────────────────────────────────────────────
#  DSA — HashMap / Dictionary Lookups
# ─────────────────────────────────────────────
def build_student_map(students):
    """Build a hashmap { student_id -> student_dict } for O(1) lookup."""
    return {s["student_id"]: s for s in students}

def build_course_map(courses):
    """Build a hashmap { course_id -> course_dict } for O(1) lookup."""
    return {c["course_id"]: c for c in courses}

# ─────────────────────────────────────────────
#  DSA — Linear Search (manual implementation)
# ─────────────────────────────────────────────
def search_students(students, query):
    """Search students by ID, name, or matching course (linear search O(n))."""
    query = query.strip().lower()
    if not query:
        return students
    return [s for s in students
            if query in s["student_id"].lower()
            or query in s["name"].lower()]

def search_courses(courses, query):
    """Search courses by name or department (linear search O(n))."""
    query = query.strip().lower()
    if not query:
        return courses
    return [c for c in courses
            if query in c["course_name"].lower()
            or query in c["department"].lower()]

# ─────────────────────────────────────────────
#  DASHBOARD STATS
# ─────────────────────────────────────────────
def get_stats():
    students   = read_csv(STUDENTS_FILE,   STUDENT_FIELDS)
    courses    = read_csv(COURSES_FILE,    COURSE_FIELDS)
    admissions = read_csv(ADMISSIONS_FILE, ADMISSION_FIELDS)
    confirmed  = sum(1 for a in admissions if a.get("status","").lower() == "confirmed")
    pending    = sum(1 for a in admissions if a.get("status","").lower() == "pending")
    rejected   = sum(1 for a in admissions if a.get("status","").lower() == "rejected")
    return {
        "total_students":   len(students),
        "total_courses":    len(courses),
        "total_admissions": len(admissions),
        "confirmed":        confirmed,
        "pending":          pending,
        "rejected":         rejected,
    }

# ─────────────────────────────────────────────────────────────────────────────
#  HTML TEMPLATE  (render_template_string — single-file, no external templates)
# ─────────────────────────────────────────────────────────────────────────────
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{{ page_title }} — SARMS</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
/* ── Reset & Variables ──────────────────────────────── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0d1117;
  --surface:#161b22;
  --surface2:#1c2333;
  --surface3:#21262d;
  --border:#30363d;
  --primary:#2ea043;
  --primary-glow:rgba(46,160,67,.25);
  --accent:#58a6ff;
  --accent-glow:rgba(88,166,255,.2);
  --warning:#d29922;
  --danger:#f85149;
  --danger-glow:rgba(248,81,73,.2);
  --text:#e6edf3;
  --text-muted:#8b949e;
  --text-subtle:#484f58;
  --radius:10px;
  --radius-lg:16px;
  --shadow:0 8px 32px rgba(0,0,0,.4);
  --font:'Outfit',sans-serif;
  --mono:'JetBrains Mono',monospace;
  --transition:all .2s ease;
}
html{scroll-behavior:smooth}
body{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh;line-height:1.6}

/* ── Scrollbar ──────────────────────────────────────── */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--surface)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--text-subtle)}

/* ── Navbar ─────────────────────────────────────────── */
.navbar{
  position:sticky;top:0;z-index:100;
  background:rgba(22,27,34,.92);
  backdrop-filter:blur(14px);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  padding:.75rem 2rem;gap:1rem;
}
.nav-brand{display:flex;align-items:center;gap:.75rem;text-decoration:none}
.nav-brand .logo{
  width:38px;height:38px;border-radius:10px;
  background:linear-gradient(135deg,var(--primary),var(--accent));
  display:flex;align-items:center;justify-content:center;
  font-size:1.1rem;color:#fff;flex-shrink:0;
  box-shadow:0 0 16px var(--primary-glow);
}
.nav-brand span{font-weight:700;font-size:1.05rem;color:var(--text);letter-spacing:-.3px}
.nav-links{display:flex;gap:.25rem;align-items:center}
.nav-link{
  display:flex;align-items:center;gap:.45rem;
  padding:.45rem .9rem;border-radius:8px;
  text-decoration:none;color:var(--text-muted);
  font-size:.88rem;font-weight:500;
  transition:var(--transition);
}
.nav-link:hover{background:var(--surface2);color:var(--text)}
.nav-link.active{background:rgba(46,160,67,.15);color:var(--primary)}
.nav-link i{font-size:.85rem}
.nav-search{
  display:flex;align-items:center;gap:.5rem;
  background:var(--surface2);border:1px solid var(--border);
  border-radius:8px;padding:.4rem .8rem;
}
.nav-search input{
  background:none;border:none;outline:none;
  color:var(--text);font-family:var(--font);font-size:.85rem;
  width:180px;
}
.nav-search input::placeholder{color:var(--text-subtle)}
.nav-search button{
  background:var(--primary);border:none;
  color:#fff;padding:.25rem .6rem;border-radius:6px;
  cursor:pointer;font-size:.78rem;font-weight:600;
  transition:var(--transition);
}
.nav-search button:hover{filter:brightness(1.15)}

/* ── Page Layout ────────────────────────────────────── */
.page{max-width:1300px;margin:0 auto;padding:2rem 1.5rem}
.page-header{margin-bottom:2rem}
.page-header h1{font-size:1.75rem;font-weight:800;letter-spacing:-.5px;color:var(--text)}
.page-header h1 i{color:var(--primary);margin-right:.5rem}
.page-header p{color:var(--text-muted);font-size:.9rem;margin-top:.3rem}
.breadcrumb{display:flex;align-items:center;gap:.4rem;font-size:.78rem;color:var(--text-subtle);margin-bottom:.75rem}
.breadcrumb a{color:var(--text-subtle);text-decoration:none}
.breadcrumb a:hover{color:var(--accent)}
.breadcrumb i{font-size:.65rem}

/* ── Flash Messages ─────────────────────────────────── */
.flash-container{position:fixed;top:70px;right:1.5rem;z-index:200;display:flex;flex-direction:column;gap:.5rem;width:320px}
.flash{
  padding:.85rem 1.1rem;border-radius:var(--radius);
  display:flex;align-items:flex-start;gap:.6rem;
  font-size:.85rem;font-weight:500;
  animation:slideIn .3s ease;
  box-shadow:var(--shadow);
  border-left:3px solid;
}
.flash.success{background:rgba(46,160,67,.15);border-color:var(--primary);color:#7ee787}
.flash.error{background:rgba(248,81,73,.12);border-color:var(--danger);color:#ffa198}
.flash.info{background:rgba(88,166,255,.12);border-color:var(--accent);color:#a5c6ff}
.flash i{margin-top:.1rem;flex-shrink:0}
@keyframes slideIn{from{transform:translateX(40px);opacity:0}to{transform:translateX(0);opacity:1}}

/* ── Stats Cards ─────────────────────────────────────── */
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin-bottom:2rem}
.stat-card{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius-lg);padding:1.25rem 1.5rem;
  display:flex;align-items:center;gap:1rem;
  transition:var(--transition);cursor:default;
}
.stat-card:hover{border-color:var(--primary);box-shadow:0 0 24px var(--primary-glow);transform:translateY(-2px)}
.stat-icon{
  width:46px;height:46px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-size:1.2rem;flex-shrink:0;
}
.stat-icon.green{background:rgba(46,160,67,.15);color:var(--primary)}
.stat-icon.blue{background:rgba(88,166,255,.15);color:var(--accent)}
.stat-icon.orange{background:rgba(210,153,34,.15);color:var(--warning)}
.stat-icon.red{background:rgba(248,81,73,.12);color:var(--danger)}
.stat-icon.purple{background:rgba(163,113,247,.15);color:#a371f7}
.stat-icon.teal{background:rgba(56,201,200,.12);color:#39c5c5}
.stat-label{font-size:.78rem;color:var(--text-muted);font-weight:500;text-transform:uppercase;letter-spacing:.5px}
.stat-value{font-size:1.9rem;font-weight:800;line-height:1;color:var(--text);font-family:var(--mono)}

/* ── Cards ──────────────────────────────────────────── */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;margin-bottom:1.5rem}
.card-header{
  padding:1rem 1.5rem;
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  background:var(--surface2);
}
.card-header h2{font-size:1rem;font-weight:700;color:var(--text);display:flex;align-items:center;gap:.5rem}
.card-header h2 i{color:var(--primary)}
.card-body{padding:1.5rem}

/* ── Nav Section Cards (Home) ───────────────────────── */
.section-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.25rem;margin-bottom:2rem}
.section-card{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius-lg);padding:1.5rem;
  text-decoration:none;color:var(--text);
  transition:var(--transition);
  display:flex;flex-direction:column;gap:.75rem;
  position:relative;overflow:hidden;
}
.section-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--primary),var(--accent));
  transform:scaleX(0);transition:transform .3s ease;transform-origin:left;
}
.section-card:hover{border-color:var(--accent);box-shadow:0 0 30px var(--accent-glow);transform:translateY(-3px)}
.section-card:hover::before{transform:scaleX(1)}
.section-card-icon{
  width:52px;height:52px;border-radius:12px;
  display:flex;align-items:center;justify-content:center;
  font-size:1.4rem;background:var(--surface2);
}
.section-card-icon.green{color:var(--primary);background:rgba(46,160,67,.12)}
.section-card-icon.blue{color:var(--accent);background:rgba(88,166,255,.12)}
.section-card-icon.orange{color:var(--warning);background:rgba(210,153,34,.12)}
.section-card-icon.purple{color:#a371f7;background:rgba(163,113,247,.12)}
.section-card h3{font-size:1.1rem;font-weight:700;margin-bottom:.2rem}
.section-card p{font-size:.83rem;color:var(--text-muted);line-height:1.5}
.section-card .arrow{
  margin-top:.5rem;font-size:.8rem;color:var(--text-subtle);
  display:flex;align-items:center;gap:.3rem;transition:var(--transition);
}
.section-card:hover .arrow{color:var(--accent);gap:.6rem}

/* ── Forms ──────────────────────────────────────────── */
.form-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.25rem}
.form-group{display:flex;flex-direction:column;gap:.4rem}
.form-group label{font-size:.8rem;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px}
.form-group label i{margin-right:.35rem;color:var(--primary);font-size:.75rem}
.form-control{
  background:var(--surface2);border:1px solid var(--border);
  border-radius:8px;padding:.6rem .9rem;
  color:var(--text);font-family:var(--font);font-size:.88rem;
  outline:none;transition:var(--transition);width:100%;
}
.form-control:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-glow)}
.form-control::placeholder{color:var(--text-subtle)}
select.form-control option{background:var(--surface2)}
.form-actions{display:flex;gap:.75rem;justify-content:flex-end;margin-top:1.5rem;padding-top:1.25rem;border-top:1px solid var(--border)}
.btn{
  display:inline-flex;align-items:center;gap:.45rem;
  padding:.55rem 1.2rem;border-radius:8px;border:none;
  font-family:var(--font);font-size:.85rem;font-weight:600;
  cursor:pointer;transition:var(--transition);text-decoration:none;
  white-space:nowrap;
}
.btn-primary{background:var(--primary);color:#fff}
.btn-primary:hover{filter:brightness(1.15);box-shadow:0 4px 16px var(--primary-glow)}
.btn-accent{background:var(--accent);color:#0d1117}
.btn-accent:hover{filter:brightness(1.1);box-shadow:0 4px 16px var(--accent-glow)}
.btn-danger{background:rgba(248,81,73,.15);color:var(--danger);border:1px solid rgba(248,81,73,.3)}
.btn-danger:hover{background:rgba(248,81,73,.25)}
.btn-warning{background:rgba(210,153,34,.12);color:var(--warning);border:1px solid rgba(210,153,34,.25)}
.btn-warning:hover{background:rgba(210,153,34,.25)}
.btn-ghost{background:transparent;color:var(--text-muted);border:1px solid var(--border)}
.btn-ghost:hover{background:var(--surface2);color:var(--text)}
.btn-sm{padding:.35rem .75rem;font-size:.78rem}

/* ── Tables ──────────────────────────────────────────── */
.table-wrapper{overflow-x:auto;border-radius:var(--radius-lg)}
table{width:100%;border-collapse:collapse;font-size:.85rem}
thead{background:var(--surface2);position:sticky;top:0;z-index:1}
thead th{
  padding:.8rem 1rem;text-align:left;
  font-size:.72rem;font-weight:700;
  text-transform:uppercase;letter-spacing:.7px;
  color:var(--text-muted);border-bottom:1px solid var(--border);
  white-space:nowrap;
}
tbody tr{border-bottom:1px solid var(--surface3);transition:var(--transition)}
tbody tr:hover{background:var(--surface2)}
tbody td{padding:.75rem 1rem;vertical-align:middle;color:var(--text)}
tbody td:first-child{font-family:var(--mono);font-size:.78rem;color:var(--text-muted)}
.actions-cell{display:flex;gap:.4rem;align-items:center}

/* ── Badges ──────────────────────────────────────────── */
.badge{
  display:inline-flex;align-items:center;gap:.3rem;
  padding:.22rem .65rem;border-radius:20px;font-size:.72rem;font-weight:600;
}
.badge-confirmed{background:rgba(46,160,67,.15);color:#7ee787;border:1px solid rgba(46,160,67,.3)}
.badge-pending{background:rgba(210,153,34,.15);color:#e3b341;border:1px solid rgba(210,153,34,.3)}
.badge-rejected{background:rgba(248,81,73,.12);color:#ffa198;border:1px solid rgba(248,81,73,.2)}

/* ── Search Bar ──────────────────────────────────────── */
.search-bar{
  display:flex;align-items:center;gap:.75rem;
  background:var(--surface2);border:1px solid var(--border);
  border-radius:10px;padding:.6rem 1rem;margin-bottom:1.25rem;
  transition:var(--transition);
}
.search-bar:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-glow)}
.search-bar i{color:var(--text-subtle)}
.search-bar input{
  flex:1;background:none;border:none;outline:none;
  color:var(--text);font-family:var(--font);font-size:.88rem;
}
.search-bar input::placeholder{color:var(--text-subtle)}
.sort-controls{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1.25rem;align-items:center}
.sort-controls span{font-size:.78rem;color:var(--text-muted);font-weight:500}
.sort-btn{
  padding:.3rem .7rem;border-radius:6px;border:1px solid var(--border);
  background:var(--surface2);color:var(--text-muted);
  font-size:.78rem;font-weight:600;cursor:pointer;
  text-decoration:none;transition:var(--transition);
}
.sort-btn:hover,.sort-btn.active{background:rgba(88,166,255,.12);border-color:var(--accent);color:var(--accent)}

/* ── Empty State ─────────────────────────────────────── */
.empty-state{text-align:center;padding:3rem 1rem;color:var(--text-muted)}
.empty-state i{font-size:2.5rem;color:var(--text-subtle);margin-bottom:.75rem;display:block}
.empty-state p{font-size:.9rem}

/* ── Modal (edit) ────────────────────────────────────── */
.modal-overlay{
  display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);
  z-index:300;align-items:center;justify-content:center;padding:1rem;
}
.modal-overlay.open{display:flex}
.modal{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius-lg);width:100%;max-width:640px;
  max-height:90vh;overflow-y:auto;
  box-shadow:0 24px 64px rgba(0,0,0,.6);
  animation:modalIn .25s ease;
}
@keyframes modalIn{from{transform:scale(.95);opacity:0}to{transform:scale(1);opacity:1}}
.modal-header{
  padding:1.1rem 1.5rem;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  background:var(--surface2);
}
.modal-header h3{font-size:1rem;font-weight:700;color:var(--text);display:flex;align-items:center;gap:.5rem}
.modal-header h3 i{color:var(--accent)}
.modal-close{background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:1.1rem;padding:.3rem;border-radius:6px;transition:var(--transition)}
.modal-close:hover{background:var(--surface3);color:var(--text)}
.modal-body{padding:1.5rem}

/* ── Tabs ────────────────────────────────────────────── */
.tabs{display:flex;gap:.25rem;border-bottom:1px solid var(--border);margin-bottom:1.5rem}
.tab-btn{
  padding:.6rem 1.1rem;border-radius:8px 8px 0 0;border:none;
  background:none;color:var(--text-muted);font-family:var(--font);
  font-size:.85rem;font-weight:600;cursor:pointer;
  transition:var(--transition);
  border-bottom:2px solid transparent;margin-bottom:-1px;
}
.tab-btn.active{color:var(--primary);border-bottom-color:var(--primary);background:rgba(46,160,67,.06)}
.tab-content{display:none}
.tab-content.active{display:block}

/* ── Recent Activity Table on Home ─────────────────── */
.activity-row td{padding:.6rem 1rem}
.chip{
  display:inline-flex;align-items:center;gap:.3rem;
  padding:.18rem .5rem;border-radius:6px;
  font-size:.72rem;font-family:var(--mono);
  background:var(--surface2);color:var(--text-muted);border:1px solid var(--border);
}

/* ── Responsive ──────────────────────────────────────── */
@media(max-width:768px){
  .navbar{padding:.6rem 1rem;flex-wrap:wrap}
  .nav-brand span{display:none}
  .nav-search{display:none}
  .page{padding:1.25rem .75rem}
  .stats-grid{grid-template-columns:repeat(2,1fr)}
  .section-grid{grid-template-columns:1fr}
  .form-grid{grid-template-columns:1fr}
}
</style>
</head>
<body>

<!-- ── NAVBAR ─────────────────────────────────────────── -->
<nav class="navbar">
  <a href="/" class="nav-brand">
    <div class="logo"><i class="fa-solid fa-graduation-cap"></i></div>
    <span>SARMS</span>
  </a>
  <div class="nav-links">
    <a href="/"           class="nav-link {% if active=='home'       %}active{% endif %}"><i class="fa-solid fa-house"></i> Home</a>
    <a href="/students"   class="nav-link {% if active=='students'   %}active{% endif %}"><i class="fa-solid fa-user-graduate"></i> Students</a>
    <a href="/courses"    class="nav-link {% if active=='courses'    %}active{% endif %}"><i class="fa-solid fa-book-open"></i> Courses</a>
    <a href="/admissions" class="nav-link {% if active=='admissions' %}active{% endif %}"><i class="fa-solid fa-file-lines"></i> Admissions</a>
  </div>
  <form class="nav-search" method="GET" action="/students">
    <i class="fa-solid fa-magnifying-glass" style="color:var(--text-subtle);font-size:.8rem"></i>
    <input type="text" name="q" placeholder="Quick search students…" value="{{ request.args.get('q','') }}"/>
    <button type="submit">Go</button>
  </form>
</nav>

<!-- ── FLASH MESSAGES ─────────────────────────────────── -->
<div class="flash-container">
{% with messages = get_flashed_messages(with_categories=true) %}
  {% for category, message in messages %}
  <div class="flash {{ category }}">
    <i class="fa-solid {% if category=='success' %}fa-circle-check{% elif category=='error' %}fa-circle-exclamation{% else %}fa-circle-info{% endif %}"></i>
    <span>{{ message }}</span>
  </div>
  {% endfor %}
{% endwith %}
</div>

<div class="page">
{{ content | safe }}
</div>

<script>
// Auto-dismiss flash messages after 4 s
setTimeout(()=>{
  document.querySelectorAll('.flash').forEach(el=>{
    el.style.transition='opacity .4s';
    el.style.opacity='0';
    setTimeout(()=>el.remove(),400);
  });
},4000);

// Modal helpers
function openModal(id){document.getElementById(id).classList.add('open')}
function closeModal(id){document.getElementById(id).classList.remove('open')}

// Tab switching
function switchTab(group,name){
  document.querySelectorAll('[data-tab-group="'+group+'"]').forEach(el=>{
    el.classList.toggle('active', el.dataset.tab===name);
  });
  document.querySelectorAll('[data-tab-content="'+group+'"]').forEach(el=>{
    el.classList.toggle('active', el.dataset.tab===name);
  });
}
</script>
</body>
</html>
"""

def render_page(content, page_title="Dashboard", active="home"):
    return render_template_string(
        BASE_TEMPLATE,
        content=content,
        page_title=page_title,
        active=active,
    )

# ═══════════════════════════════════════════════════════════
#  ROUTES
# ═══════════════════════════════════════════════════════════

# ─────────────────────────────────────────────
#  HOME  /
# ─────────────────────────────────────────────
@app.route("/")
def home():
    stats      = get_stats()
    students   = read_csv(STUDENTS_FILE,   STUDENT_FIELDS)
    courses    = read_csv(COURSES_FILE,    COURSE_FIELDS)
    admissions = read_csv(ADMISSIONS_FILE, ADMISSION_FIELDS)
    smap = build_student_map(students)
    cmap = build_course_map(courses)
    recent = admissions[-6:][::-1]  # last 6

    content = f"""
<div class="page-header">
  <h1><i class="fa-solid fa-chart-line"></i>Dashboard</h1>
  <p>Student Admission Record Management System — Overview</p>
</div>

<!-- Stats -->
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-icon green"><i class="fa-solid fa-users"></i></div>
    <div><div class="stat-label">Total Students</div><div class="stat-value">{stats['total_students']}</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon blue"><i class="fa-solid fa-book-open"></i></div>
    <div><div class="stat-label">Total Courses</div><div class="stat-value">{stats['total_courses']}</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon orange"><i class="fa-solid fa-file-lines"></i></div>
    <div><div class="stat-label">Admissions</div><div class="stat-value">{stats['total_admissions']}</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon green"><i class="fa-solid fa-circle-check"></i></div>
    <div><div class="stat-label">Confirmed</div><div class="stat-value">{stats['confirmed']}</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon orange"><i class="fa-solid fa-clock"></i></div>
    <div><div class="stat-label">Pending</div><div class="stat-value">{stats['pending']}</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon red"><i class="fa-solid fa-circle-xmark"></i></div>
    <div><div class="stat-label">Rejected</div><div class="stat-value">{stats['rejected']}</div></div>
  </div>
</div>

<!-- Section Links -->
<div class="section-grid">
  <a href="/students/add" class="section-card">
    <div class="section-card-icon green"><i class="fa-solid fa-user-plus"></i></div>
    <div>
      <h3>Student Registration</h3>
      <p>Register new students with personal details, contact info and address.</p>
    </div>
    <div class="arrow"><i class="fa-solid fa-arrow-right"></i> Register Now</div>
  </a>
  <a href="/courses/add" class="section-card">
    <div class="section-card-icon blue"><i class="fa-solid fa-book-medical"></i></div>
    <div>
      <h3>Course Management</h3>
      <p>Add and manage academic courses, departments and durations.</p>
    </div>
    <div class="arrow"><i class="fa-solid fa-arrow-right"></i> Add Course</div>
  </a>
  <a href="/admissions/add" class="section-card">
    <div class="section-card-icon orange"><i class="fa-solid fa-file-circle-plus"></i></div>
    <div>
      <h3>Admission Management</h3>
      <p>Create and manage admission records linking students to courses.</p>
    </div>
    <div class="arrow"><i class="fa-solid fa-arrow-right"></i> New Admission</div>
  </a>
  <a href="/students" class="section-card">
    <div class="section-card-icon purple"><i class="fa-solid fa-table-list"></i></div>
    <div>
      <h3>Student Records</h3>
      <p>Browse, search, sort and manage all student and admission records.</p>
    </div>
    <div class="arrow"><i class="fa-solid fa-arrow-right"></i> View Records</div>
  </a>
</div>

<!-- Recent Admissions -->
<div class="card">
  <div class="card-header">
    <h2><i class="fa-solid fa-clock-rotate-left"></i> Recent Admissions</h2>
    <a href="/admissions" class="btn btn-ghost btn-sm"><i class="fa-solid fa-eye"></i> View All</a>
  </div>
  <div class="card-body" style="padding:0">
    <div class="table-wrapper">
"""
    if recent:
        content += """
      <table>
        <thead><tr>
          <th>Admission ID</th><th>Student</th><th>Course</th><th>Date</th><th>Status</th>
        </tr></thead>
        <tbody>
"""
        for a in recent:
            s = smap.get(a.get("student_id",""), {})
            c = cmap.get(a.get("course_id",""), {})
            sname = s.get("name","—")
            cname = c.get("course_name","—")
            status = a.get("status","Pending")
            badge_cls = "badge-"+status.lower()
            content += f"""
          <tr class="activity-row">
            <td><span class="chip">{a.get('admission_id','')}</span></td>
            <td><b>{sname}</b><br/><span style="font-size:.75rem;color:var(--text-muted)">{a.get('student_id','')}</span></td>
            <td>{cname}</td>
            <td style="font-family:var(--mono);font-size:.78rem">{a.get('admission_date','')}</td>
            <td><span class="badge {badge_cls}">{status}</span></td>
          </tr>
"""
        content += "</tbody></table>"
    else:
        content += '<div class="empty-state"><i class="fa-solid fa-inbox"></i><p>No admissions yet.</p></div>'

    content += "</div></div></div>"
    return render_page(content, "Dashboard", "home")


# ─────────────────────────────────────────────
#  STUDENTS LIST  /students
# ─────────────────────────────────────────────
@app.route("/students")
def students_list():
    q        = request.args.get("q","").strip()
    sort_by  = request.args.get("sort","")
    students = read_csv(STUDENTS_FILE, STUDENT_FIELDS)

    # Search
    if q:
        students = search_students(students, q)

    # Quick-Sort
    if sort_by == "name":
        students = quick_sort(students, key_func=lambda x: x.get("name","").lower())
    elif sort_by == "name_desc":
        students = quick_sort(students, key_func=lambda x: x.get("name","").lower(), reverse=True)
    elif sort_by == "age":
        students = quick_sort(students, key_func=lambda x: int(x.get("age","0") or 0))
    elif sort_by == "age_desc":
        students = quick_sort(students, key_func=lambda x: int(x.get("age","0") or 0), reverse=True)

    # Load admissions for status column
    admissions = read_csv(ADMISSIONS_FILE, ADMISSION_FIELDS)
    courses    = read_csv(COURSES_FILE,    COURSE_FIELDS)
    cmap = build_course_map(courses)
    # Build student→admission map (latest)
    adm_map = {}
    for a in admissions:
        adm_map[a.get("student_id","")] = a

    content = f"""
<div class="breadcrumb"><a href="/">Home</a><i class="fa-solid fa-chevron-right"></i> Students</div>
<div class="page-header">
  <h1><i class="fa-solid fa-user-graduate"></i>Student Records</h1>
  <p>View, search, sort and manage all registered students.</p>
</div>

<div style="display:flex;gap:.75rem;justify-content:space-between;flex-wrap:wrap;margin-bottom:1rem">
  <form method="GET" action="/students" style="flex:1;min-width:240px">
    <div class="search-bar">
      <i class="fa-solid fa-magnifying-glass"></i>
      <input type="text" name="q" value="{q}" placeholder="Search by ID, Name…"/>
    </div>
    <div class="sort-controls">
      <span><i class="fa-solid fa-sort"></i> Sort:</span>
      <a href="/students?q={q}&sort=name"      class="sort-btn {'active' if sort_by=='name'      else ''}">Name A→Z</a>
      <a href="/students?q={q}&sort=name_desc" class="sort-btn {'active' if sort_by=='name_desc' else ''}">Name Z→A</a>
      <a href="/students?q={q}&sort=age"       class="sort-btn {'active' if sort_by=='age'       else ''}">Age ↑</a>
      <a href="/students?q={q}&sort=age_desc"  class="sort-btn {'active' if sort_by=='age_desc'  else ''}">Age ↓</a>
      <a href="/students?q={q}"                class="sort-btn {'active' if not sort_by          else ''}">Default</a>
    </div>
  </form>
  <a href="/students/add" class="btn btn-primary" style="align-self:flex-start">
    <i class="fa-solid fa-user-plus"></i> Register Student
  </a>
</div>

<div class="card">
  <div class="card-header">
    <h2><i class="fa-solid fa-users"></i> All Students ({len(students)} records)</h2>
  </div>
  <div class="table-wrapper">
"""
    if students:
        content += """
    <table>
      <thead><tr>
        <th>Student ID</th><th>Name</th><th>Age</th><th>Gender</th>
        <th>Contact</th><th>Address</th><th>Course</th><th>Adm. Status</th><th>Actions</th>
      </tr></thead>
      <tbody>
"""
        for s in students:
            sid = s.get("student_id","")
            adm = adm_map.get(sid, {})
            course_name = cmap.get(adm.get("course_id",""), {}).get("course_name","—")
            status = adm.get("status","—")
            badge_cls = "badge-"+status.lower() if status != "—" else ""
            content += f"""
        <tr>
          <td><span class="chip">{sid}</span></td>
          <td><b>{s.get('name','')}</b></td>
          <td style="font-family:var(--mono)">{s.get('age','')}</td>
          <td>{s.get('gender','')}</td>
          <td><a href="tel:{s.get('contact','')}" style="color:var(--accent);text-decoration:none">{s.get('contact','')}</a></td>
          <td style="max-width:160px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="{s.get('address','')}">{s.get('address','')}</td>
          <td>{course_name}</td>
          <td>{'<span class="badge '+badge_cls+'">'+status+'</span>' if status!='—' else '<span style="color:var(--text-subtle);font-size:.8rem">—</span>'}</td>
          <td>
            <div class="actions-cell">
              <a href="/students/edit/{sid}" class="btn btn-warning btn-sm"><i class="fa-solid fa-pen"></i></a>
              <a href="/students/delete/{sid}" class="btn btn-danger btn-sm" onclick="return confirm('Delete student {sid}?')"><i class="fa-solid fa-trash"></i></a>
            </div>
          </td>
        </tr>
"""
        content += "</tbody></table>"
    else:
        content += '<div class="empty-state"><i class="fa-solid fa-users-slash"></i><p>No students found' + (f' for "{q}"' if q else '') + '.</p></div>'

    content += "</div></div>"
    return render_page(content, "Students", "students")


# ─────────────────────────────────────────────
#  ADD STUDENT  /students/add
# ─────────────────────────────────────────────
@app.route("/students/add", methods=["GET","POST"])
def student_add():
    if request.method == "POST":
        data = {
            "student_id": request.form.get("student_id","").strip(),
            "name":       request.form.get("name","").strip(),
            "age":        request.form.get("age","").strip(),
            "gender":     request.form.get("gender","").strip(),
            "contact":    request.form.get("contact","").strip(),
            "address":    request.form.get("address","").strip(),
        }
        if not data["student_id"] or not data["name"]:
            flash("Student ID and Name are required.", "error")
        else:
            students = read_csv(STUDENTS_FILE, STUDENT_FIELDS)
            smap = build_student_map(students)
            if data["student_id"] in smap:
                flash(f"Student ID '{data['student_id']}' already exists.", "error")
            else:
                students.append(data)
                write_csv(STUDENTS_FILE, STUDENT_FIELDS, students)
                flash(f"Student '{data['name']}' registered successfully!", "success")
                return redirect(url_for("students_list"))

    content = """
<div class="breadcrumb"><a href="/">Home</a><i class="fa-solid fa-chevron-right"></i><a href="/students">Students</a><i class="fa-solid fa-chevron-right"></i>Register</div>
<div class="page-header">
  <h1><i class="fa-solid fa-user-plus"></i>Register Student</h1>
  <p>Fill in the form below to register a new student.</p>
</div>
<div class="card">
  <div class="card-header"><h2><i class="fa-solid fa-id-card"></i> Student Information</h2></div>
  <div class="card-body">
    <form method="POST">
      <div class="form-grid">
        <div class="form-group">
          <label><i class="fa-solid fa-fingerprint"></i>Student ID</label>
          <input class="form-control" name="student_id" placeholder="e.g. STU001" required/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-user"></i>Full Name</label>
          <input class="form-control" name="name" placeholder="e.g. John Doe" required/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-calendar"></i>Age</label>
          <input class="form-control" name="age" type="number" min="10" max="100" placeholder="e.g. 20"/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-venus-mars"></i>Gender</label>
          <select class="form-control" name="gender">
            <option value="">— Select —</option>
            <option>Male</option><option>Female</option><option>Other</option>
          </select>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-phone"></i>Contact Info</label>
          <input class="form-control" name="contact" placeholder="e.g. +91 9876543210"/>
        </div>
        <div class="form-group" style="grid-column:1/-1">
          <label><i class="fa-solid fa-location-dot"></i>Address</label>
          <input class="form-control" name="address" placeholder="Full address"/>
        </div>
      </div>
      <div class="form-actions">
        <a href="/students" class="btn btn-ghost"><i class="fa-solid fa-xmark"></i> Cancel</a>
        <button type="submit" class="btn btn-primary"><i class="fa-solid fa-floppy-disk"></i> Register Student</button>
      </div>
    </form>
  </div>
</div>
"""
    return render_page(content, "Register Student", "students")


# ─────────────────────────────────────────────
#  EDIT STUDENT  /students/edit/<id>
# ─────────────────────────────────────────────
@app.route("/students/edit/<student_id>", methods=["GET","POST"])
def student_edit(student_id):
    students = read_csv(STUDENTS_FILE, STUDENT_FIELDS)
    smap = build_student_map(students)
    s = smap.get(student_id)
    if not s:
        flash("Student not found.", "error")
        return redirect(url_for("students_list"))

    if request.method == "POST":
        s["name"]    = request.form.get("name","").strip()
        s["age"]     = request.form.get("age","").strip()
        s["gender"]  = request.form.get("gender","").strip()
        s["contact"] = request.form.get("contact","").strip()
        s["address"] = request.form.get("address","").strip()
        updated = [smap[k] if k != student_id else s for k in smap]
        write_csv(STUDENTS_FILE, STUDENT_FIELDS, updated)
        flash(f"Student '{s['name']}' updated successfully!", "success")
        return redirect(url_for("students_list"))

    content = f"""
<div class="breadcrumb"><a href="/">Home</a><i class="fa-solid fa-chevron-right"></i><a href="/students">Students</a><i class="fa-solid fa-chevron-right"></i>Edit</div>
<div class="page-header">
  <h1><i class="fa-solid fa-user-pen"></i>Edit Student</h1>
  <p>Editing record for <b>{s['name']}</b> — <span style="font-family:var(--mono);color:var(--accent)">{student_id}</span></p>
</div>
<div class="card">
  <div class="card-header"><h2><i class="fa-solid fa-id-card"></i> Update Information</h2></div>
  <div class="card-body">
    <form method="POST">
      <div class="form-grid">
        <div class="form-group">
          <label><i class="fa-solid fa-fingerprint"></i>Student ID</label>
          <input class="form-control" value="{student_id}" disabled/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-user"></i>Full Name</label>
          <input class="form-control" name="name" value="{s.get('name','')}" required/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-calendar"></i>Age</label>
          <input class="form-control" name="age" type="number" value="{s.get('age','')}"/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-venus-mars"></i>Gender</label>
          <select class="form-control" name="gender">
            <option {'selected' if s.get('gender')=='' else ''}>— Select —</option>
            <option {'selected' if s.get('gender')=='Male' else ''}>Male</option>
            <option {'selected' if s.get('gender')=='Female' else ''}>Female</option>
            <option {'selected' if s.get('gender')=='Other' else ''}>Other</option>
          </select>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-phone"></i>Contact Info</label>
          <input class="form-control" name="contact" value="{s.get('contact','')}"/>
        </div>
        <div class="form-group" style="grid-column:1/-1">
          <label><i class="fa-solid fa-location-dot"></i>Address</label>
          <input class="form-control" name="address" value="{s.get('address','')}"/>
        </div>
      </div>
      <div class="form-actions">
        <a href="/students" class="btn btn-ghost"><i class="fa-solid fa-xmark"></i> Cancel</a>
        <button type="submit" class="btn btn-primary"><i class="fa-solid fa-floppy-disk"></i> Save Changes</button>
      </div>
    </form>
  </div>
</div>
"""
    return render_page(content, "Edit Student", "students")


# ─────────────────────────────────────────────
#  DELETE STUDENT  /students/delete/<id>
# ─────────────────────────────────────────────
@app.route("/students/delete/<student_id>")
def student_delete(student_id):
    students = read_csv(STUDENTS_FILE, STUDENT_FIELDS)
    updated  = [s for s in students if s["student_id"] != student_id]
    if len(updated) == len(students):
        flash("Student not found.", "error")
    else:
        write_csv(STUDENTS_FILE, STUDENT_FIELDS, updated)
        flash(f"Student '{student_id}' deleted.", "success")
    return redirect(url_for("students_list"))


# ─────────────────────────────────────────────
#  COURSES LIST  /courses
# ─────────────────────────────────────────────
@app.route("/courses")
def courses_list():
    q       = request.args.get("q","").strip()
    courses = read_csv(COURSES_FILE, COURSE_FIELDS)
    if q:
        courses = search_courses(courses, q)

    content = f"""
<div class="breadcrumb"><a href="/">Home</a><i class="fa-solid fa-chevron-right"></i>Courses</div>
<div class="page-header">
  <h1><i class="fa-solid fa-book-open"></i>Course Management</h1>
  <p>Manage academic courses offered by the institution.</p>
</div>

<div style="display:flex;gap:.75rem;justify-content:space-between;flex-wrap:wrap;margin-bottom:1rem">
  <form method="GET" action="/courses" style="flex:1;min-width:240px">
    <div class="search-bar">
      <i class="fa-solid fa-magnifying-glass"></i>
      <input type="text" name="q" value="{q}" placeholder="Search by Course Name or Department…"/>
    </div>
  </form>
  <a href="/courses/add" class="btn btn-primary" style="align-self:flex-start">
    <i class="fa-solid fa-plus"></i> Add Course
  </a>
</div>

<div class="card">
  <div class="card-header">
    <h2><i class="fa-solid fa-book-open"></i> All Courses ({len(courses)} records)</h2>
  </div>
  <div class="table-wrapper">
"""
    if courses:
        content += """
    <table>
      <thead><tr>
        <th>Course ID</th><th>Course Name</th><th>Department</th><th>Duration</th><th>Actions</th>
      </tr></thead>
      <tbody>
"""
        for c in courses:
            content += f"""
        <tr>
          <td><span class="chip">{c.get('course_id','')}</span></td>
          <td><b>{c.get('course_name','')}</b></td>
          <td><span class="badge" style="background:rgba(88,166,255,.1);color:var(--accent);border:1px solid rgba(88,166,255,.25)">{c.get('department','')}</span></td>
          <td style="font-family:var(--mono)">{c.get('duration','')}</td>
          <td>
            <div class="actions-cell">
              <a href="/courses/edit/{c.get('course_id','')}" class="btn btn-warning btn-sm"><i class="fa-solid fa-pen"></i></a>
              <a href="/courses/delete/{c.get('course_id','')}" class="btn btn-danger btn-sm" onclick="return confirm('Delete this course?')"><i class="fa-solid fa-trash"></i></a>
            </div>
          </td>
        </tr>
"""
        content += "</tbody></table>"
    else:
        content += '<div class="empty-state"><i class="fa-solid fa-book"></i><p>No courses found' + (f' for "{q}"' if q else '') + '.</p></div>'

    content += "</div></div>"
    return render_page(content, "Courses", "courses")


# ─────────────────────────────────────────────
#  ADD COURSE  /courses/add
# ─────────────────────────────────────────────
@app.route("/courses/add", methods=["GET","POST"])
def course_add():
    if request.method == "POST":
        data = {
            "course_id":   request.form.get("course_id","").strip(),
            "course_name": request.form.get("course_name","").strip(),
            "department":  request.form.get("department","").strip(),
            "duration":    request.form.get("duration","").strip(),
        }
        if not data["course_id"] or not data["course_name"]:
            flash("Course ID and Name are required.", "error")
        else:
            courses = read_csv(COURSES_FILE, COURSE_FIELDS)
            cmap = build_course_map(courses)
            if data["course_id"] in cmap:
                flash(f"Course ID '{data['course_id']}' already exists.", "error")
            else:
                courses.append(data)
                write_csv(COURSES_FILE, COURSE_FIELDS, courses)
                flash(f"Course '{data['course_name']}' added successfully!", "success")
                return redirect(url_for("courses_list"))

    content = """
<div class="breadcrumb"><a href="/">Home</a><i class="fa-solid fa-chevron-right"></i><a href="/courses">Courses</a><i class="fa-solid fa-chevron-right"></i>Add</div>
<div class="page-header">
  <h1><i class="fa-solid fa-book-medical"></i>Add New Course</h1>
  <p>Define a new academic course for the institution.</p>
</div>
<div class="card">
  <div class="card-header"><h2><i class="fa-solid fa-book"></i> Course Details</h2></div>
  <div class="card-body">
    <form method="POST">
      <div class="form-grid">
        <div class="form-group">
          <label><i class="fa-solid fa-fingerprint"></i>Course ID</label>
          <input class="form-control" name="course_id" placeholder="e.g. CS101" required/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-book"></i>Course Name</label>
          <input class="form-control" name="course_name" placeholder="e.g. Introduction to Python" required/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-building-columns"></i>Department</label>
          <input class="form-control" name="department" placeholder="e.g. Computer Science"/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-hourglass-half"></i>Duration</label>
          <input class="form-control" name="duration" placeholder="e.g. 6 Months / 1 Year"/>
        </div>
      </div>
      <div class="form-actions">
        <a href="/courses" class="btn btn-ghost"><i class="fa-solid fa-xmark"></i> Cancel</a>
        <button type="submit" class="btn btn-primary"><i class="fa-solid fa-floppy-disk"></i> Add Course</button>
      </div>
    </form>
  </div>
</div>
"""
    return render_page(content, "Add Course", "courses")


# ─────────────────────────────────────────────
#  EDIT COURSE  /courses/edit/<id>
# ─────────────────────────────────────────────
@app.route("/courses/edit/<course_id>", methods=["GET","POST"])
def course_edit(course_id):
    courses = read_csv(COURSES_FILE, COURSE_FIELDS)
    cmap = build_course_map(courses)
    c = cmap.get(course_id)
    if not c:
        flash("Course not found.", "error")
        return redirect(url_for("courses_list"))

    if request.method == "POST":
        c["course_name"] = request.form.get("course_name","").strip()
        c["department"]  = request.form.get("department","").strip()
        c["duration"]    = request.form.get("duration","").strip()
        updated = [cmap[k] if k != course_id else c for k in cmap]
        write_csv(COURSES_FILE, COURSE_FIELDS, updated)
        flash(f"Course '{c['course_name']}' updated!", "success")
        return redirect(url_for("courses_list"))

    content = f"""
<div class="breadcrumb"><a href="/">Home</a><i class="fa-solid fa-chevron-right"></i><a href="/courses">Courses</a><i class="fa-solid fa-chevron-right"></i>Edit</div>
<div class="page-header">
  <h1><i class="fa-solid fa-book-open"></i>Edit Course</h1>
  <p>Editing: <b>{c['course_name']}</b> — <span style="font-family:var(--mono);color:var(--accent)">{course_id}</span></p>
</div>
<div class="card">
  <div class="card-header"><h2><i class="fa-solid fa-book"></i> Update Course Details</h2></div>
  <div class="card-body">
    <form method="POST">
      <div class="form-grid">
        <div class="form-group">
          <label><i class="fa-solid fa-fingerprint"></i>Course ID</label>
          <input class="form-control" value="{course_id}" disabled/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-book"></i>Course Name</label>
          <input class="form-control" name="course_name" value="{c.get('course_name','')}" required/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-building-columns"></i>Department</label>
          <input class="form-control" name="department" value="{c.get('department','')}"/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-hourglass-half"></i>Duration</label>
          <input class="form-control" name="duration" value="{c.get('duration','')}"/>
        </div>
      </div>
      <div class="form-actions">
        <a href="/courses" class="btn btn-ghost"><i class="fa-solid fa-xmark"></i> Cancel</a>
        <button type="submit" class="btn btn-primary"><i class="fa-solid fa-floppy-disk"></i> Save Changes</button>
      </div>
    </form>
  </div>
</div>
"""
    return render_page(content, "Edit Course", "courses")


# ─────────────────────────────────────────────
#  DELETE COURSE  /courses/delete/<id>
# ─────────────────────────────────────────────
@app.route("/courses/delete/<course_id>")
def course_delete(course_id):
    courses = read_csv(COURSES_FILE, COURSE_FIELDS)
    updated = [c for c in courses if c["course_id"] != course_id]
    if len(updated) == len(courses):
        flash("Course not found.", "error")
    else:
        write_csv(COURSES_FILE, COURSE_FIELDS, updated)
        flash(f"Course '{course_id}' deleted.", "success")
    return redirect(url_for("courses_list"))


# ─────────────────────────────────────────────
#  ADMISSIONS LIST  /admissions
# ─────────────────────────────────────────────
@app.route("/admissions")
def admissions_list():
    q          = request.args.get("q","").strip()
    admissions = read_csv(ADMISSIONS_FILE, ADMISSION_FIELDS)
    students   = read_csv(STUDENTS_FILE,   STUDENT_FIELDS)
    courses    = read_csv(COURSES_FILE,    COURSE_FIELDS)
    smap = build_student_map(students)
    cmap = build_course_map(courses)

    # Search by student name, course name or admission ID
    if q:
        ql = q.lower()
        filtered = []
        for a in admissions:
            s = smap.get(a.get("student_id",""), {})
            c = cmap.get(a.get("course_id",""), {})
            if (ql in a.get("admission_id","").lower()
                or ql in a.get("student_id","").lower()
                or ql in s.get("name","").lower()
                or ql in c.get("course_name","").lower()):
                filtered.append(a)
        admissions = filtered

    content = f"""
<div class="breadcrumb"><a href="/">Home</a><i class="fa-solid fa-chevron-right"></i>Admissions</div>
<div class="page-header">
  <h1><i class="fa-solid fa-file-lines"></i>Admission Records</h1>
  <p>View and manage all student admission records.</p>
</div>

<div style="display:flex;gap:.75rem;justify-content:space-between;flex-wrap:wrap;margin-bottom:1rem">
  <form method="GET" action="/admissions" style="flex:1;min-width:240px">
    <div class="search-bar">
      <i class="fa-solid fa-magnifying-glass"></i>
      <input type="text" name="q" value="{q}" placeholder="Search by Admission ID, Student, Course…"/>
    </div>
  </form>
  <a href="/admissions/add" class="btn btn-primary" style="align-self:flex-start">
    <i class="fa-solid fa-plus"></i> New Admission
  </a>
</div>

<div class="card">
  <div class="card-header">
    <h2><i class="fa-solid fa-file-lines"></i> All Admissions ({len(admissions)} records)</h2>
  </div>
  <div class="table-wrapper">
"""
    if admissions:
        content += """
    <table>
      <thead><tr>
        <th>Admission ID</th><th>Student ID</th><th>Student Name</th>
        <th>Course ID</th><th>Course Name</th><th>Date</th><th>Status</th><th>Actions</th>
      </tr></thead>
      <tbody>
"""
        for a in admissions:
            aid = a.get("admission_id","")
            sid = a.get("student_id","")
            cid = a.get("course_id","")
            s = smap.get(sid, {})
            c = cmap.get(cid, {})
            status = a.get("status","Pending")
            badge_cls = "badge-"+status.lower()
            content += f"""
        <tr>
          <td><span class="chip">{aid}</span></td>
          <td><span class="chip">{sid}</span></td>
          <td><b>{s.get('name','—')}</b></td>
          <td><span class="chip">{cid}</span></td>
          <td>{c.get('course_name','—')}</td>
          <td style="font-family:var(--mono);font-size:.78rem">{a.get('admission_date','')}</td>
          <td><span class="badge {badge_cls}">{status}</span></td>
          <td>
            <div class="actions-cell">
              <a href="/admissions/edit/{aid}" class="btn btn-warning btn-sm"><i class="fa-solid fa-pen"></i></a>
              <a href="/admissions/delete/{aid}" class="btn btn-danger btn-sm" onclick="return confirm('Delete this admission record?')"><i class="fa-solid fa-trash"></i></a>
            </div>
          </td>
        </tr>
"""
        content += "</tbody></table>"
    else:
        content += '<div class="empty-state"><i class="fa-solid fa-file-circle-question"></i><p>No admissions found' + (f' for "{q}"' if q else '') + '.</p></div>'

    content += "</div></div>"
    return render_page(content, "Admissions", "admissions")


# ─────────────────────────────────────────────
#  ADD ADMISSION  /admissions/add
# ─────────────────────────────────────────────
@app.route("/admissions/add", methods=["GET","POST"])
def admission_add():
    students = read_csv(STUDENTS_FILE, STUDENT_FIELDS)
    courses  = read_csv(COURSES_FILE,  COURSE_FIELDS)

    if request.method == "POST":
        data = {
            "admission_id":   request.form.get("admission_id","").strip(),
            "student_id":     request.form.get("student_id","").strip(),
            "course_id":      request.form.get("course_id","").strip(),
            "admission_date": request.form.get("admission_date","").strip(),
            "status":         request.form.get("status","Pending").strip(),
        }
        if not data["admission_id"] or not data["student_id"] or not data["course_id"]:
            flash("Admission ID, Student ID and Course ID are required.", "error")
        else:
            admissions = read_csv(ADMISSIONS_FILE, ADMISSION_FIELDS)
            existing_ids = {a["admission_id"] for a in admissions}
            if data["admission_id"] in existing_ids:
                flash(f"Admission ID '{data['admission_id']}' already exists.", "error")
            else:
                admissions.append(data)
                write_csv(ADMISSIONS_FILE, ADMISSION_FIELDS, admissions)
                flash("Admission record created successfully!", "success")
                return redirect(url_for("admissions_list"))

    today = datetime.today().strftime("%Y-%m-%d")
    student_options = "".join(f'<option value="{s["student_id"]}">{s["student_id"]} — {s["name"]}</option>' for s in students)
    course_options  = "".join(f'<option value="{c["course_id"]}">{c["course_id"]} — {c["course_name"]}</option>' for c in courses)

    content = f"""
<div class="breadcrumb"><a href="/">Home</a><i class="fa-solid fa-chevron-right"></i><a href="/admissions">Admissions</a><i class="fa-solid fa-chevron-right"></i>New</div>
<div class="page-header">
  <h1><i class="fa-solid fa-file-circle-plus"></i>New Admission</h1>
  <p>Create an admission record linking a student to a course.</p>
</div>
<div class="card">
  <div class="card-header"><h2><i class="fa-solid fa-file-lines"></i> Admission Details</h2></div>
  <div class="card-body">
    <form method="POST">
      <div class="form-grid">
        <div class="form-group">
          <label><i class="fa-solid fa-fingerprint"></i>Admission ID</label>
          <input class="form-control" name="admission_id" placeholder="e.g. ADM001" required/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-user-graduate"></i>Student</label>
          <select class="form-control" name="student_id" required>
            <option value="">— Select Student —</option>
            {student_options}
          </select>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-book-open"></i>Course</label>
          <select class="form-control" name="course_id" required>
            <option value="">— Select Course —</option>
            {course_options}
          </select>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-calendar-days"></i>Admission Date</label>
          <input class="form-control" name="admission_date" type="date" value="{today}"/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-circle-half-stroke"></i>Status</label>
          <select class="form-control" name="status">
            <option value="Pending">Pending</option>
            <option value="Confirmed">Confirmed</option>
            <option value="Rejected">Rejected</option>
          </select>
        </div>
      </div>
      <div class="form-actions">
        <a href="/admissions" class="btn btn-ghost"><i class="fa-solid fa-xmark"></i> Cancel</a>
        <button type="submit" class="btn btn-primary"><i class="fa-solid fa-floppy-disk"></i> Create Admission</button>
      </div>
    </form>
  </div>
</div>
"""
    return render_page(content, "New Admission", "admissions")


# ─────────────────────────────────────────────
#  EDIT ADMISSION  /admissions/edit/<id>
# ─────────────────────────────────────────────
@app.route("/admissions/edit/<admission_id>", methods=["GET","POST"])
def admission_edit(admission_id):
    admissions = read_csv(ADMISSIONS_FILE, ADMISSION_FIELDS)
    adm_map    = {a["admission_id"]: a for a in admissions}
    a = adm_map.get(admission_id)
    if not a:
        flash("Admission not found.", "error")
        return redirect(url_for("admissions_list"))

    students = read_csv(STUDENTS_FILE, STUDENT_FIELDS)
    courses  = read_csv(COURSES_FILE,  COURSE_FIELDS)

    if request.method == "POST":
        a["student_id"]     = request.form.get("student_id","").strip()
        a["course_id"]      = request.form.get("course_id","").strip()
        a["admission_date"] = request.form.get("admission_date","").strip()
        a["status"]         = request.form.get("status","Pending").strip()
        updated = [adm_map[k] if k != admission_id else a for k in adm_map]
        write_csv(ADMISSIONS_FILE, ADMISSION_FIELDS, updated)
        flash("Admission record updated successfully!", "success")
        return redirect(url_for("admissions_list"))

    def sel(v, match): return "selected" if v == match else ""
    student_options = "".join(f'<option value="{s["student_id"]}" {sel(s["student_id"], a.get("student_id",""))}>{s["student_id"]} — {s["name"]}</option>' for s in students)
    course_options  = "".join(f'<option value="{c["course_id"]}"  {sel(c["course_id"],  a.get("course_id",""))}>{ c["course_id"]} — {c["course_name"]}</option>' for c in courses)

    content = f"""
<div class="breadcrumb"><a href="/">Home</a><i class="fa-solid fa-chevron-right"></i><a href="/admissions">Admissions</a><i class="fa-solid fa-chevron-right"></i>Edit</div>
<div class="page-header">
  <h1><i class="fa-solid fa-file-pen"></i>Edit Admission</h1>
  <p>Editing record <span style="font-family:var(--mono);color:var(--accent)">{admission_id}</span></p>
</div>
<div class="card">
  <div class="card-header"><h2><i class="fa-solid fa-file-lines"></i> Update Admission</h2></div>
  <div class="card-body">
    <form method="POST">
      <div class="form-grid">
        <div class="form-group">
          <label><i class="fa-solid fa-fingerprint"></i>Admission ID</label>
          <input class="form-control" value="{admission_id}" disabled/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-user-graduate"></i>Student</label>
          <select class="form-control" name="student_id" required>
            <option value="">— Select —</option>
            {student_options}
          </select>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-book-open"></i>Course</label>
          <select class="form-control" name="course_id" required>
            <option value="">— Select —</option>
            {course_options}
          </select>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-calendar-days"></i>Admission Date</label>
          <input class="form-control" name="admission_date" type="date" value="{a.get('admission_date','')}"/>
        </div>
        <div class="form-group">
          <label><i class="fa-solid fa-circle-half-stroke"></i>Status</label>
          <select class="form-control" name="status">
            <option value="Pending"   {sel('Pending',   a.get('status',''))}>Pending</option>
            <option value="Confirmed" {sel('Confirmed', a.get('status',''))}>Confirmed</option>
            <option value="Rejected"  {sel('Rejected',  a.get('status',''))}>Rejected</option>
          </select>
        </div>
      </div>
      <div class="form-actions">
        <a href="/admissions" class="btn btn-ghost"><i class="fa-solid fa-xmark"></i> Cancel</a>
        <button type="submit" class="btn btn-primary"><i class="fa-solid fa-floppy-disk"></i> Save Changes</button>
      </div>
    </form>
  </div>
</div>
"""
    return render_page(content, "Edit Admission", "admissions")


# ─────────────────────────────────────────────
#  DELETE ADMISSION  /admissions/delete/<id>
# ─────────────────────────────────────────────
@app.route("/admissions/delete/<admission_id>")
def admission_delete(admission_id):
    admissions = read_csv(ADMISSIONS_FILE, ADMISSION_FIELDS)
    updated    = [a for a in admissions if a["admission_id"] != admission_id]
    if len(updated) == len(admissions):
        flash("Admission not found.", "error")
    else:
        write_csv(ADMISSIONS_FILE, ADMISSION_FIELDS, updated)
        flash(f"Admission '{admission_id}' deleted.", "success")
    return redirect(url_for("admissions_list"))


# ─────────────────────────────────────────────
#  MAIN ENTRY
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Ensure all CSV files exist before starting
    init_csv(STUDENTS_FILE,   STUDENT_FIELDS)
    init_csv(COURSES_FILE,    COURSE_FIELDS)
    init_csv(ADMISSIONS_FILE, ADMISSION_FIELDS)
    print("=" * 60)
    print("  Student Admission Record Management System (SARMS)")
    print("  Running at → http://127.0.0.1:5000")
    print("  Storage    → students.csv | courses.csv | admissions.csv")
    print("=" * 60)
    app.run(debug=True, port=5000)
