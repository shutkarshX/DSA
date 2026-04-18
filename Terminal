import { useState, useMemo } from "react";

const DEPARTMENTS = ["Computer Science", "Engineering", "Business", "Medicine", "Arts & Humanities", "Law", "Sciences"];
const STATUSES = ["Pending", "Admitted", "Rejected", "Waitlisted"];

const STATUS_COLORS = {
  Pending:    { bg: "#FEF3C7", text: "#92400E", dot: "#F59E0B" },
  Admitted:   { bg: "#D1FAE5", text: "#065F46", dot: "#10B981" },
  Rejected:   { bg: "#FEE2E2", text: "#991B1B", dot: "#EF4444" },
  Waitlisted: { bg: "#EDE9FE", text: "#4C1D95", dot: "#8B5CF6" },
};

const INITIAL_STUDENTS = [
  { id: 1, name: "Aisha Nwosu",       dob: "2003-04-12", email: "aisha@email.com",    phone: "555-0101", department: "Medicine",          gpa: "3.92", status: "Admitted",   date: "2026-01-15", notes: "Outstanding research background." },
  { id: 2, name: "Carlos Mendez",     dob: "2004-07-23", email: "carlos@email.com",   phone: "555-0102", department: "Engineering",       gpa: "3.65", status: "Admitted",   date: "2026-01-18", notes: "Strong STEM portfolio." },
  { id: 3, name: "Priya Sharma",      dob: "2003-11-05", email: "priya@email.com",    phone: "555-0103", department: "Computer Science",  gpa: "3.80", status: "Pending",    date: "2026-02-02", notes: "Interview scheduled for March." },
  { id: 4, name: "James O'Brien",     dob: "2004-02-18", email: "james@email.com",    phone: "555-0104", department: "Law",               gpa: "3.45", status: "Waitlisted", date: "2026-02-10", notes: "Good essays, average GPA." },
  { id: 5, name: "Mei-Lin Zhou",      dob: "2003-09-30", email: "mei@email.com",      phone: "555-0105", department: "Business",          gpa: "3.71", status: "Admitted",   date: "2026-01-22", notes: "Top of cohort in economics." },
  { id: 6, name: "David Okafor",      dob: "2005-01-14", email: "david@email.com",    phone: "555-0106", department: "Sciences",          gpa: "2.90", status: "Rejected",   date: "2026-02-14", notes: "GPA below minimum threshold." },
  { id: 7, name: "Sophie Laurent",    dob: "2003-06-08", email: "sophie@email.com",   phone: "555-0107", department: "Arts & Humanities", gpa: "3.55", status: "Pending",    date: "2026-02-20", notes: "Exceptional portfolio submitted." },
];

let nextId = 8;

const emptyForm = { name: "", dob: "", email: "", phone: "", department: DEPARTMENTS[0], gpa: "", status: STATUSES[0], date: "", notes: "" };

export default function App() {
  const [students, setStudents] = useState(INITIAL_STUDENTS);
  const [view, setView] = useState("dashboard"); // dashboard | list | form | detail
  const [editingStudent, setEditingStudent] = useState(null);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [formErrors, setFormErrors] = useState({});
  const [search, setSearch] = useState("");
  const [filterDept, setFilterDept] = useState("All");
  const [filterStatus, setFilterStatus] = useState("All");
  const [sortBy, setSortBy] = useState("name");
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [toast, setToast] = useState(null);

  const showToast = (msg, type = "success") => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  };

  // Stats
  const stats = useMemo(() => {
    const total = students.length;
    const admitted = students.filter(s => s.status === "Admitted").length;
    const pending = students.filter(s => s.status === "Pending").length;
    const rejected = students.filter(s => s.status === "Rejected").length;
    const waitlisted = students.filter(s => s.status === "Waitlisted").length;
    const avgGpa = total ? (students.reduce((a, s) => a + parseFloat(s.gpa || 0), 0) / total).toFixed(2) : "N/A";
    return { total, admitted, pending, rejected, waitlisted, avgGpa };
  }, [students]);

  // Filtered list
  const filtered = useMemo(() => {
    let list = [...students];
    if (search) list = list.filter(s =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.email.toLowerCase().includes(search.toLowerCase()) ||
      s.department.toLowerCase().includes(search.toLowerCase())
    );
    if (filterDept !== "All") list = list.filter(s => s.department === filterDept);
    if (filterStatus !== "All") list = list.filter(s => s.status === filterStatus);
    list.sort((a, b) => {
      if (sortBy === "name") return a.name.localeCompare(b.name);
      if (sortBy === "gpa") return parseFloat(b.gpa) - parseFloat(a.gpa);
      if (sortBy === "date") return new Date(b.date) - new Date(a.date);
      return 0;
    });
    return list;
  }, [students, search, filterDept, filterStatus, sortBy]);

  // Dept breakdown for dashboard
  const deptBreakdown = useMemo(() => {
    return DEPARTMENTS.map(d => ({
      dept: d,
      count: students.filter(s => s.department === d).length,
    })).filter(d => d.count > 0).sort((a, b) => b.count - a.count);
  }, [students]);

  const validate = (f) => {
    const e = {};
    if (!f.name.trim()) e.name = "Name is required";
    if (!f.dob) e.dob = "Date of birth required";
    if (!f.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) e.email = "Valid email required";
    if (!f.gpa || isNaN(f.gpa) || f.gpa < 0 || f.gpa > 4) e.gpa = "GPA must be 0.00–4.00";
    if (!f.date) e.date = "Application date required";
    return e;
  };

  const openAdd = () => { setForm(emptyForm); setEditingStudent(null); setFormErrors({}); setView("form"); };
  const openEdit = (s) => { setForm({ ...s }); setEditingStudent(s.id); setFormErrors({}); setView("form"); };
  const openDetail = (s) => { setSelectedStudent(s); setView("detail"); };

  const handleSubmit = () => {
    const errors = validate(form);
    if (Object.keys(errors).length) { setFormErrors(errors); return; }
    if (editingStudent) {
      setStudents(prev => prev.map(s => s.id === editingStudent ? { ...form, id: editingStudent } : s));
      showToast("Student record updated successfully.");
    } else {
      setStudents(prev => [...prev, { ...form, id: nextId++ }]);
      showToast("New student admitted to records.");
    }
    setView("list");
  };

  const handleDelete = (id) => {
    setStudents(prev => prev.filter(s => s.id !== id));
    setDeleteConfirm(null);
    if (view === "detail") setView("list");
    showToast("Record deleted.", "error");
  };

  const handleStatusChange = (id, status) => {
    setStudents(prev => prev.map(s => s.id === id ? { ...s, status } : s));
    if (selectedStudent?.id === id) setSelectedStudent(prev => ({ ...prev, status }));
    showToast(`Status updated to ${status}.`);
  };

  const F = ({ label, name, type = "text", options, required }) => (
    <div style={{ marginBottom: 18 }}>
      <label style={{ display: "block", fontSize: 12, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: "#6B7280", marginBottom: 6 }}>
        {label}{required && <span style={{ color: "#EF4444" }}> *</span>}
      </label>
      {options ? (
        <select value={form[name]} onChange={e => setForm(f => ({ ...f, [name]: e.target.value }))}
          style={{ width: "100%", padding: "10px 14px", border: `1.5px solid ${formErrors[name] ? "#EF4444" : "#E5E7EB"}`, borderRadius: 8, fontSize: 14, background: "#fff", color: "#111827", outline: "none" }}>
          {options.map(o => <option key={o}>{o}</option>)}
        </select>
      ) : (
        <input type={type} value={form[name]} onChange={e => setForm(f => ({ ...f, [name]: e.target.value }))}
          style={{ width: "100%", padding: "10px 14px", border: `1.5px solid ${formErrors[name] ? "#EF4444" : "#E5E7EB"}`, borderRadius: 8, fontSize: 14, background: "#fff", color: "#111827", outline: "none", boxSizing: "border-box" }} />
      )}
      {formErrors[name] && <div style={{ color: "#EF4444", fontSize: 12, marginTop: 4 }}>{formErrors[name]}</div>}
    </div>
  );

  // ─── RENDER ───────────────────────────────────────────────────────────────
  return (
    <div style={{ fontFamily: "'Georgia', 'Times New Roman', serif", background: "#F8F7F4", minHeight: "100vh", color: "#111827" }}>

      {/* Toast */}
      {toast && (
        <div style={{ position: "fixed", top: 20, right: 20, zIndex: 9999, background: toast.type === "error" ? "#FEE2E2" : "#D1FAE5", color: toast.type === "error" ? "#991B1B" : "#065F46", padding: "12px 20px", borderRadius: 10, fontFamily: "sans-serif", fontSize: 14, fontWeight: 600, boxShadow: "0 4px 20px rgba(0,0,0,0.12)", border: `1px solid ${toast.type === "error" ? "#FCA5A5" : "#6EE7B7"}` }}>
          {toast.type === "error" ? "✕ " : "✓ "}{toast.msg}
        </div>
      )}

      {/* Delete Confirm Modal */}
      {deleteConfirm && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", zIndex: 1000, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <div style={{ background: "#fff", borderRadius: 16, padding: 32, maxWidth: 400, width: "90%", textAlign: "center", boxShadow: "0 20px 60px rgba(0,0,0,0.2)" }}>
            <div style={{ fontSize: 40, marginBottom: 12 }}>⚠️</div>
            <div style={{ fontSize: 20, fontWeight: 700, marginBottom: 8 }}>Delete Record?</div>
            <div style={{ color: "#6B7280", marginBottom: 24, fontFamily: "sans-serif", fontSize: 14 }}>This will permanently remove <strong>{deleteConfirm.name}</strong>'s admission record.</div>
            <div style={{ display: "flex", gap: 12, justifyContent: "center" }}>
              <button onClick={() => setDeleteConfirm(null)} style={{ padding: "10px 24px", border: "1.5px solid #E5E7EB", borderRadius: 8, background: "#fff", cursor: "pointer", fontFamily: "sans-serif", fontWeight: 600, fontSize: 14 }}>Cancel</button>
              <button onClick={() => handleDelete(deleteConfirm.id)} style={{ padding: "10px 24px", border: "none", borderRadius: 8, background: "#EF4444", color: "#fff", cursor: "pointer", fontFamily: "sans-serif", fontWeight: 600, fontSize: 14 }}>Delete</button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <header style={{ background: "#1A2332", color: "#fff", padding: "0 32px", display: "flex", alignItems: "center", justifyContent: "space-between", height: 64, boxShadow: "0 2px 12px rgba(0,0,0,0.15)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div style={{ width: 38, height: 38, background: "linear-gradient(135deg, #C8A96E, #E8C98A)", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20 }}>🎓</div>
          <div>
            <div style={{ fontSize: 17, fontWeight: 700, letterSpacing: "0.02em" }}>Academia</div>
            <div style={{ fontSize: 11, color: "#94A3B8", letterSpacing: "0.15em", textTransform: "uppercase", fontFamily: "sans-serif" }}>Admissions System</div>
          </div>
        </div>
        <nav style={{ display: "flex", gap: 4, fontFamily: "sans-serif" }}>
          {[["dashboard", "📊 Dashboard"], ["list", "📋 Records"]].map(([v, label]) => (
            <button key={v} onClick={() => setView(v)}
              style={{ padding: "8px 16px", borderRadius: 8, border: "none", cursor: "pointer", fontSize: 13, fontWeight: 600, background: view === v ? "rgba(200,169,110,0.2)" : "transparent", color: view === v ? "#C8A96E" : "#94A3B8", transition: "all 0.2s" }}>
              {label}
            </button>
          ))}
        </nav>
      </header>

      <main style={{ maxWidth: 1100, margin: "0 auto", padding: "32px 24px" }}>

        {/* ── DASHBOARD ── */}
        {view === "dashboard" && (
          <div>
            <div style={{ marginBottom: 28 }}>
              <h1 style={{ fontSize: 28, fontWeight: 700, margin: 0, color: "#1A2332" }}>Admissions Overview</h1>
              <p style={{ color: "#6B7280", margin: "6px 0 0", fontFamily: "sans-serif", fontSize: 14 }}>Academic Year 2026–2027 · Real-time data</p>
            </div>

            {/* Stat Cards */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))", gap: 16, marginBottom: 28 }}>
              {[
                { label: "Total Applicants", value: stats.total, icon: "👥", color: "#1A2332", accent: "#C8A96E" },
                { label: "Admitted", value: stats.admitted, icon: "✅", color: "#065F46", accent: "#10B981" },
                { label: "Pending Review", value: stats.pending, icon: "⏳", color: "#92400E", accent: "#F59E0B" },
                { label: "Waitlisted", value: stats.waitlisted, icon: "📋", color: "#4C1D95", accent: "#8B5CF6" },
                { label: "Rejected", value: stats.rejected, icon: "✕", color: "#991B1B", accent: "#EF4444" },
                { label: "Average GPA", value: stats.avgGpa, icon: "📈", color: "#1E3A5F", accent: "#3B82F6" },
              ].map(({ label, value, icon, color, accent }) => (
                <div key={label} style={{ background: "#fff", borderRadius: 14, padding: "20px", boxShadow: "0 1px 4px rgba(0,0,0,0.06)", borderTop: `3px solid ${accent}` }}>
                  <div style={{ fontSize: 26, marginBottom: 8 }}>{icon}</div>
                  <div style={{ fontSize: 32, fontWeight: 800, color, lineHeight: 1 }}>{value}</div>
                  <div style={{ fontSize: 12, color: "#6B7280", marginTop: 6, fontFamily: "sans-serif", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em" }}>{label}</div>
                </div>
              ))}
            </div>

            {/* Status Bar + Dept Breakdown */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
              {/* Status Distribution */}
              <div style={{ background: "#fff", borderRadius: 14, padding: 24, boxShadow: "0 1px 4px rgba(0,0,0,0.06)" }}>
                <h3 style={{ margin: "0 0 20px", fontSize: 15, fontWeight: 700, fontFamily: "sans-serif", color: "#1A2332" }}>Status Distribution</h3>
                {STATUSES.map(s => {
                  const count = students.filter(x => x.status === s).length;
                  const pct = stats.total ? Math.round((count / stats.total) * 100) : 0;
                  const c = STATUS_COLORS[s];
                  return (
                    <div key={s} style={{ marginBottom: 14 }}>
                      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5, fontFamily: "sans-serif", fontSize: 13 }}>
                        <span style={{ fontWeight: 600, color: "#374151" }}>{s}</span>
                        <span style={{ color: "#6B7280" }}>{count} ({pct}%)</span>
                      </div>
                      <div style={{ height: 8, background: "#F3F4F6", borderRadius: 99 }}>
                        <div style={{ height: "100%", width: `${pct}%`, background: c.dot, borderRadius: 99, transition: "width 0.5s" }} />
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Department Breakdown */}
              <div style={{ background: "#fff", borderRadius: 14, padding: 24, boxShadow: "0 1px 4px rgba(0,0,0,0.06)" }}>
                <h3 style={{ margin: "0 0 20px", fontSize: 15, fontWeight: 700, fontFamily: "sans-serif", color: "#1A2332" }}>By Department</h3>
                {deptBreakdown.map(({ dept, count }) => {
                  const pct = stats.total ? Math.round((count / stats.total) * 100) : 0;
                  return (
                    <div key={dept} style={{ marginBottom: 14 }}>
                      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5, fontFamily: "sans-serif", fontSize: 13 }}>
                        <span style={{ fontWeight: 600, color: "#374151" }}>{dept}</span>
                        <span style={{ color: "#6B7280" }}>{count}</span>
                      </div>
                      <div style={{ height: 8, background: "#F3F4F6", borderRadius: 99 }}>
                        <div style={{ height: "100%", width: `${pct}%`, background: "#C8A96E", borderRadius: 99 }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Recent */}
            <div style={{ background: "#fff", borderRadius: 14, padding: 24, boxShadow: "0 1px 4px rgba(0,0,0,0.06)", marginTop: 20 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
                <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700, fontFamily: "sans-serif", color: "#1A2332" }}>Recent Applications</h3>
                <button onClick={() => setView("list")} style={{ fontSize: 13, color: "#C8A96E", background: "none", border: "none", cursor: "pointer", fontFamily: "sans-serif", fontWeight: 600 }}>View All →</button>
              </div>
              {[...students].sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 4).map(s => {
                const c = STATUS_COLORS[s.status];
                return (
                  <div key={s.id} onClick={() => openDetail(s)} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "12px 0", borderBottom: "1px solid #F3F4F6", cursor: "pointer" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                      <div style={{ width: 36, height: 36, borderRadius: "50%", background: "#1A2332", color: "#C8A96E", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 700, fontSize: 14, fontFamily: "sans-serif" }}>
                        {s.name.split(" ").map(n => n[0]).join("").slice(0, 2)}
                      </div>
                      <div>
                        <div style={{ fontWeight: 700, fontSize: 14, fontFamily: "sans-serif" }}>{s.name}</div>
                        <div style={{ fontSize: 12, color: "#6B7280", fontFamily: "sans-serif" }}>{s.department}</div>
                      </div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                      <span style={{ fontSize: 12, color: "#6B7280", fontFamily: "sans-serif" }}>{s.date}</span>
                      <span style={{ padding: "3px 10px", borderRadius: 99, fontSize: 11, fontWeight: 700, background: c.bg, color: c.text, fontFamily: "sans-serif" }}>{s.status}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ── RECORDS LIST ── */}
        {view === "list" && (
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 24 }}>
              <div>
                <h1 style={{ fontSize: 26, fontWeight: 700, margin: 0, color: "#1A2332" }}>Student Records</h1>
                <p style={{ color: "#6B7280", margin: "4px 0 0", fontFamily: "sans-serif", fontSize: 14 }}>{filtered.length} of {students.length} records</p>
              </div>
              <button onClick={openAdd} style={{ padding: "10px 20px", background: "#1A2332", color: "#C8A96E", border: "none", borderRadius: 10, cursor: "pointer", fontFamily: "sans-serif", fontWeight: 700, fontSize: 14, display: "flex", alignItems: "center", gap: 8 }}>
                ＋ Add Student
              </button>
            </div>

            {/* Filters */}
            <div style={{ background: "#fff", borderRadius: 12, padding: 16, marginBottom: 20, display: "flex", gap: 12, flexWrap: "wrap", boxShadow: "0 1px 4px rgba(0,0,0,0.06)" }}>
              <input value={search} onChange={e => setSearch(e.target.value)} placeholder="🔍  Search by name, email, department..." style={{ flex: "1 1 220px", padding: "9px 14px", border: "1.5px solid #E5E7EB", borderRadius: 8, fontSize: 14, fontFamily: "sans-serif", outline: "none", minWidth: 180 }} />
              <select value={filterDept} onChange={e => setFilterDept(e.target.value)} style={{ padding: "9px 14px", border: "1.5px solid #E5E7EB", borderRadius: 8, fontSize: 13, fontFamily: "sans-serif", background: "#fff", color: "#374151" }}>
                <option value="All">All Departments</option>
                {DEPARTMENTS.map(d => <option key={d}>{d}</option>)}
              </select>
              <select value={filterStatus} onChange={e => setFilterStatus(e.target.value)} style={{ padding: "9px 14px", border: "1.5px solid #E5E7EB", borderRadius: 8, fontSize: 13, fontFamily: "sans-serif", background: "#fff", color: "#374151" }}>
                <option value="All">All Statuses</option>
                {STATUSES.map(s => <option key={s}>{s}</option>)}
              </select>
              <select value={sortBy} onChange={e => setSortBy(e.target.value)} style={{ padding: "9px 14px", border: "1.5px solid #E5E7EB", borderRadius: 8, fontSize: 13, fontFamily: "sans-serif", background: "#fff", color: "#374151" }}>
                <option value="name">Sort: Name</option>
                <option value="gpa">Sort: GPA ↓</option>
                <option value="date">Sort: Date ↓</option>
              </select>
            </div>

            {/* Table */}
            <div style={{ background: "#fff", borderRadius: 14, overflow: "hidden", boxShadow: "0 1px 4px rgba(0,0,0,0.06)" }}>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ background: "#F8F7F4", borderBottom: "2px solid #E5E7EB" }}>
                    {["Student", "Department", "GPA", "App. Date", "Status", "Actions"].map(h => (
                      <th key={h} style={{ padding: "13px 16px", textAlign: "left", fontSize: 11, fontWeight: 800, textTransform: "uppercase", letterSpacing: "0.1em", color: "#6B7280", fontFamily: "sans-serif" }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {filtered.length === 0 ? (
                    <tr><td colSpan={6} style={{ padding: 48, textAlign: "center", color: "#9CA3AF", fontFamily: "sans-serif", fontSize: 15 }}>No records found.</td></tr>
                  ) : filtered.map((s, i) => {
                    const c = STATUS_COLORS[s.status];
                    return (
                      <tr key={s.id} style={{ borderBottom: "1px solid #F3F4F6", background: i % 2 === 0 ? "#fff" : "#FAFAF9" }}>
                        <td style={{ padding: "13px 16px" }}>
                          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                            <div style={{ width: 34, height: 34, borderRadius: "50%", background: "#1A2332", color: "#C8A96E", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 700, fontSize: 12, fontFamily: "sans-serif", flexShrink: 0 }}>
                              {s.name.split(" ").map(n => n[0]).join("").slice(0, 2)}
                            </div>
                            <div>
                              <div style={{ fontWeight: 700, fontSize: 14, color: "#111827" }}>{s.name}</div>
                              <div style={{ fontSize: 12, color: "#9CA3AF", fontFamily: "sans-serif" }}>{s.email}</div>
                            </div>
                          </div>
                        </td>
                        <td style={{ padding: "13px 16px", fontFamily: "sans-serif", fontSize: 13, color: "#374151" }}>{s.department}</td>
                        <td style={{ padding: "13px 16px", fontFamily: "sans-serif", fontSize: 14, fontWeight: 700, color: parseFloat(s.gpa) >= 3.5 ? "#065F46" : parseFloat(s.gpa) >= 3.0 ? "#92400E" : "#991B1B" }}>{s.gpa}</td>
                        <td style={{ padding: "13px 16px", fontFamily: "sans-serif", fontSize: 13, color: "#6B7280" }}>{s.date}</td>
                        <td style={{ padding: "13px 16px" }}>
                          <select value={s.status} onChange={e => handleStatusChange(s.id, e.target.value)}
                            style={{ padding: "4px 10px", borderRadius: 99, fontSize: 11, fontWeight: 700, background: c.bg, color: c.text, border: "none", cursor: "pointer", fontFamily: "sans-serif" }}>
                            {STATUSES.map(st => <option key={st}>{st}</option>)}
                          </select>
                        </td>
                        <td style={{ padding: "13px 16px" }}>
                          <div style={{ display: "flex", gap: 6 }}>
                            <button onClick={() => openDetail(s)} title="View" style={{ padding: "5px 10px", border: "1px solid #E5E7EB", borderRadius: 6, background: "#fff", cursor: "pointer", fontSize: 12, fontFamily: "sans-serif" }}>👁</button>
                            <button onClick={() => openEdit(s)} title="Edit" style={{ padding: "5px 10px", border: "1px solid #E5E7EB", borderRadius: 6, background: "#fff", cursor: "pointer", fontSize: 12, fontFamily: "sans-serif" }}>✏️</button>
                            <button onClick={() => setDeleteConfirm(s)} title="Delete" style={{ padding: "5px 10px", border: "1px solid #FCA5A5", borderRadius: 6, background: "#FEF2F2", cursor: "pointer", fontSize: 12, fontFamily: "sans-serif" }}>🗑</button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ── FORM ── */}
        {view === "form" && (
          <div style={{ maxWidth: 700, margin: "0 auto" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 28 }}>
              <button onClick={() => setView("list")} style={{ background: "none", border: "1.5px solid #E5E7EB", borderRadius: 8, padding: "6px 14px", cursor: "pointer", fontFamily: "sans-serif", fontSize: 13, color: "#6B7280" }}>← Back</button>
              <div>
                <h1 style={{ margin: 0, fontSize: 22, fontWeight: 700, color: "#1A2332" }}>{editingStudent ? "Edit Student Record" : "New Application"}</h1>
                <p style={{ margin: "2px 0 0", color: "#9CA3AF", fontFamily: "sans-serif", fontSize: 13 }}>{editingStudent ? "Update student information" : "Add a new student to the system"}</p>
              </div>
            </div>
            <div style={{ background: "#fff", borderRadius: 16, padding: 32, boxShadow: "0 2px 12px rgba(0,0,0,0.07)" }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0 20px" }}>
                <div style={{ gridColumn: "1 / -1" }}><F label="Full Name" name="name" required /></div>
                <F label="Date of Birth" name="dob" type="date" required />
                <F label="Application Date" name="date" type="date" required />
                <F label="Email Address" name="email" type="email" required />
                <F label="Phone Number" name="phone" />
                <F label="Department" name="department" options={DEPARTMENTS} />
                <F label="GPA (0.00–4.00)" name="gpa" required />
                <F label="Admission Status" name="status" options={STATUSES} />
                <div style={{ gridColumn: "1 / -1", marginBottom: 18 }}>
                  <label style={{ display: "block", fontSize: 12, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: "#6B7280", marginBottom: 6 }}>Notes</label>
                  <textarea value={form.notes} onChange={e => setForm(f => ({ ...f, notes: e.target.value }))} rows={3}
                    style={{ width: "100%", padding: "10px 14px", border: "1.5px solid #E5E7EB", borderRadius: 8, fontSize: 14, fontFamily: "sans-serif", resize: "vertical", boxSizing: "border-box", outline: "none" }} />
                </div>
              </div>
              <div style={{ display: "flex", gap: 12, justifyContent: "flex-end" }}>
                <button onClick={() => setView("list")} style={{ padding: "11px 24px", border: "1.5px solid #E5E7EB", borderRadius: 10, background: "#fff", cursor: "pointer", fontFamily: "sans-serif", fontWeight: 600, fontSize: 14 }}>Cancel</button>
                <button onClick={handleSubmit} style={{ padding: "11px 28px", border: "none", borderRadius: 10, background: "#1A2332", color: "#C8A96E", cursor: "pointer", fontFamily: "sans-serif", fontWeight: 700, fontSize: 14 }}>
                  {editingStudent ? "Save Changes" : "Submit Application"}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ── DETAIL ── */}
        {view === "detail" && selectedStudent && (() => {
          const s = students.find(x => x.id === selectedStudent.id) || selectedStudent;
          const c = STATUS_COLORS[s.status];
          return (
            <div style={{ maxWidth: 720, margin: "0 auto" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
                <button onClick={() => setView("list")} style={{ background: "none", border: "1.5px solid #E5E7EB", borderRadius: 8, padding: "6px 14px", cursor: "pointer", fontFamily: "sans-serif", fontSize: 13, color: "#6B7280" }}>← Back</button>
                <div style={{ display: "flex", gap: 10 }}>
                  <button onClick={() => openEdit(s)} style={{ padding: "8px 18px", border: "1.5px solid #1A2332", borderRadius: 9, background: "#fff", cursor: "pointer", fontFamily: "sans-serif", fontWeight: 700, fontSize: 13, color: "#1A2332" }}>✏️ Edit</button>
                  <button onClick={() => setDeleteConfirm(s)} style={{ padding: "8px 18px", border: "none", borderRadius: 9, background: "#EF4444", color: "#fff", cursor: "pointer", fontFamily: "sans-serif", fontWeight: 700, fontSize: 13 }}>🗑 Delete</button>
                </div>
              </div>
              <div style={{ background: "#fff", borderRadius: 16, overflow: "hidden", boxShadow: "0 2px 16px rgba(0,0,0,0.08)" }}>
                {/* Hero */}
                <div style={{ background: "linear-gradient(135deg, #1A2332 60%, #2C3E55)", padding: "32px 32px 28px", display: "flex", alignItems: "center", gap: 20 }}>
                  <div style={{ width: 72, height: 72, borderRadius: "50%", background: "rgba(200,169,110,0.2)", border: "3px solid #C8A96E", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 26, fontWeight: 800, color: "#C8A96E", fontFamily: "sans-serif" }}>
                    {s.name.split(" ").map(n => n[0]).join("").slice(0, 2)}
                  </div>
                  <div>
                    <h2 style={{ margin: 0, color: "#fff", fontSize: 24, fontWeight: 700 }}>{s.name}</h2>
                    <p style={{ margin: "4px 0 0", color: "#94A3B8", fontFamily: "sans-serif", fontSize: 14 }}>{s.department} · ID #{s.id.toString().padStart(4, "0")}</p>
                    <span style={{ display: "inline-block", marginTop: 10, padding: "4px 14px", borderRadius: 99, fontSize: 12, fontWeight: 700, background: c.bg, color: c.text, fontFamily: "sans-serif" }}>{s.status}</span>
                  </div>
                </div>
                {/* Info Grid */}
                <div style={{ padding: "28px 32px" }}>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 20 }}>
                    {[
                      ["📧 Email", s.email],
                      ["📞 Phone", s.phone || "—"],
                      ["🎂 Date of Birth", s.dob],
                      ["📅 Applied On", s.date],
                      ["📊 GPA", s.gpa],
                    ].map(([label, val]) => (
                      <div key={label} style={{ background: "#F8F7F4", borderRadius: 10, padding: "14px 18px" }}>
                        <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "#9CA3AF", marginBottom: 5, fontFamily: "sans-serif" }}>{label}</div>
                        <div style={{ fontSize: 15, fontWeight: 600, color: "#111827", fontFamily: "sans-serif" }}>{val}</div>
                      </div>
                    ))}
                    <div style={{ background: "#F8F7F4", borderRadius: 10, padding: "14px 18px" }}>
                      <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "#9CA3AF", marginBottom: 8, fontFamily: "sans-serif" }}>🔖 Update Status</div>
                      <select value={s.status} onChange={e => handleStatusChange(s.id, e.target.value)}
                        style={{ padding: "6px 12px", border: "1.5px solid #E5E7EB", borderRadius: 7, fontSize: 13, fontFamily: "sans-serif", background: "#fff", cursor: "pointer", width: "100%" }}>
                        {STATUSES.map(st => <option key={st}>{st}</option>)}
                      </select>
                    </div>
                  </div>
                  {s.notes && (
                    <div style={{ background: "#FFFBF0", border: "1.5px solid #FEF3C7", borderRadius: 10, padding: "16px 18px" }}>
                      <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "#92400E", marginBottom: 6, fontFamily: "sans-serif" }}>📝 Notes</div>
                      <p style={{ margin: 0, color: "#374151", fontFamily: "sans-serif", fontSize: 14, lineHeight: 1.6 }}>{s.notes}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })()}
      </main>
    </div>
  );
}
