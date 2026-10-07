import os
import sys
import re
from datetime import datetime, date
from decimal import Decimal
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Ensure db module is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from db import get_db_connection, test_db_connection, init_db_schema

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Campus Placement Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling & Glassmorphic Tech Theme
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"], [class*="st-"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

code, kbd, samp, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* App Header styling */
.main-header {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-title-container {
    display: flex;
    flex-direction: column;
}

.header-title {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #FFFFFF 0%, #93C5FD 50%, #60A5FA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.header-subtitle {
    font-size: 14px;
    color: #94A3B8;
    margin-top: 4px;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
    background: rgba(16, 185, 129, 0.12);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-badge.error {
    background: rgba(239, 68, 68, 0.12);
    color: #F87171;
    border-color: rgba(239, 68, 68, 0.3);
}

.pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #10B981;
    box-shadow: 0 0 8px #10B981;
}

/* KPI Card styling */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.kpi-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.7) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(96, 165, 250, 0.4);
}

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.kpi-title {
    font-size: 13px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-icon {
    font-size: 18px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 6px;
    display: inline-flex;
}

.kpi-value {
    font-size: 26px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
    margin-bottom: 2px;
}

.kpi-caption {
    font-size: 12px;
    color: #64748B;
    font-weight: 500;
}

/* Pill status tags */
.pill {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.pill-placed, .pill-selected {
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.pill-unplaced, .pill-pending {
    background: rgba(245, 158, 11, 0.15);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.pill-rejected {
    background: rgba(239, 68, 68, 0.15);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.pill-shortlisted {
    background: rgba(139, 92, 246, 0.15);
    color: #A78BFA;
    border: 1px solid rgba(139, 92, 246, 0.3);
}

.pill-applied {
    background: rgba(14, 165, 233, 0.15);
    color: #38BDF8;
    border: 1px solid rgba(14, 165, 233, 0.3);
}

/* Glass Card */
.glass-panel {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}

/* Job Card styling */
.job-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 14px;
    transition: all 0.2s ease;
}

.job-card:hover {
    border-color: rgba(59, 130, 246, 0.5);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

/* Sidebar Branding */
.sidebar-brand {
    padding: 12px 0 20px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 18px;
}

.sidebar-title {
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(90deg, #60A5FA, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.sidebar-desc {
    font-size: 12px;
    color: #94A3B8;
    margin-top: 4px;
}

/* Custom button tweaks */
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* Dataframe clean styling */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.06);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Database Helper Utilities
# ---------------------------------------------------------
@st.cache_resource(ttl=60)
def check_connection():
    return test_db_connection()

def run_query(query, params=None):
    """Executes a SELECT query and returns a pandas DataFrame."""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        if not records:
            return pd.DataFrame()
        df = pd.DataFrame(records)
        return df
    except Exception as e:
        if conn:
            conn.close()
        st.error(f"SQL Error: {e}")
        return pd.DataFrame()

def execute_dml(query, params=None):
    """Executes an INSERT, UPDATE, or DELETE query."""
    conn = get_db_connection()
    if conn is None:
        return False, "Could not connect to database."
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        conn.close()
        return True, rowcount
    except Exception as e:
        if conn:
            conn.close()
        return False, str(e)

# ---------------------------------------------------------
# Sidebar Layout
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2 class="sidebar-title">🎓 Campus Placement</h2>
        <div class="sidebar-desc">DBMS PBL Web Portal</div>
    </div>
    """, unsafe_allow_html=True)

    # Database connectivity check
    is_connected, conn_msg = check_connection()
    if is_connected:
        st.markdown("""
        <div class="status-badge" style="margin-bottom: 16px;">
            <div class="pulse-dot"></div>
            <span>MySQL Online (3306)</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-badge error" style="margin-bottom: 16px;">
            <span>⚠️ MySQL Offline: {conn_msg}</span>
        </div>
        """, unsafe_allow_html=True)

    menu_options = [
        "📊 Executive Dashboard",
        "👨‍🎓 Students Directory",
        "🏢 Partner Companies",
        "💼 Job Postings & Drives",
        "📄 Applications Pipeline",
        "🗓️ Interview Management",
        "📑 Advanced Reports & Views",
        "⚙️ Database & Demo Data"
    ]
    
    choice = st.radio("Navigation", menu_options, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Quick Snapshot in Sidebar
    try:
        stats_df = run_query("""
            SELECT 
                (SELECT COUNT(*) FROM students) AS total_students,
                (SELECT COUNT(*) FROM students WHERE status = 'Placed') AS placed_students,
                (SELECT COUNT(*) FROM companies) AS total_companies,
                (SELECT COUNT(*) FROM job_postings) AS total_jobs,
                (SELECT COUNT(*) FROM applications) AS total_apps
        """)
        if not stats_df.empty:
            s_row = stats_df.iloc[0]
            st.caption("SYSTEM QUICK STATS")
            col_sb1, col_sb2 = st.columns(2)
            col_sb1.metric("Students", int(s_row['total_students']))
            col_sb2.metric("Placed", int(s_row['placed_students']))
            col_sb1.metric("Companies", int(s_row['total_companies']))
            col_sb2.metric("Jobs", int(s_row['total_jobs']))
    except Exception:
        pass

    st.markdown("---")
    st.caption("Developed by **Farhan Ansari**")
    st.caption("DBMS Course Project • 3NF Normalized MySQL")

# Ensure schema view and trigger are ready
try:
    init_db_schema()
except Exception:
    pass

# ---------------------------------------------------------
# Top Header Banner
# ---------------------------------------------------------
st.markdown("""
<div class="main-header">
    <div class="header-title-container">
        <h1 class="header-title">Campus Recruitment & Placement System</h1>
        <div class="header-subtitle">Centralized Relational Database Management Portal for TPO, Students & Recruiters</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# MODULE 1: EXECUTIVE DASHBOARD
# =========================================================
if choice == "📊 Executive Dashboard":
    st.subheader("📈 Placement Analytics & Overview")
    
    # Fetch Core Metrics
    overview_query = """
    SELECT 
        (SELECT COUNT(*) FROM students) AS total_students,
        (SELECT COUNT(*) FROM students WHERE status = 'Placed') AS placed_students,
        (SELECT COUNT(*) FROM companies) AS total_companies,
        (SELECT COUNT(*) FROM job_postings) AS total_jobs,
        (SELECT COUNT(*) FROM applications) AS total_apps,
        (SELECT COUNT(*) FROM interviews) AS total_interviews,
        (SELECT MAX(package_lpa) FROM job_postings) AS max_package,
        (SELECT AVG(package_lpa) FROM job_postings) AS avg_package
    """
    metrics_df = run_query(overview_query)
    
    if not metrics_df.empty:
        row = metrics_df.iloc[0]
        total_students = int(row['total_students']) if pd.notnull(row['total_students']) else 0
        placed_students = int(row['placed_students']) if pd.notnull(row['placed_students']) else 0
        total_companies = int(row['total_companies']) if pd.notnull(row['total_companies']) else 0
        total_jobs = int(row['total_jobs']) if pd.notnull(row['total_jobs']) else 0
        total_apps = int(row['total_apps']) if pd.notnull(row['total_apps']) else 0
        total_interviews = int(row['total_interviews']) if pd.notnull(row['total_interviews']) else 0
        max_package = float(row['max_package']) if pd.notnull(row['max_package']) else 0.0
        avg_package = float(row['avg_package']) if pd.notnull(row['avg_package']) else 0.0
        placement_rate = (placed_students / total_students * 100) if total_students > 0 else 0.0
        
        # Display KPI Grid
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Total Students</span>
                    <span class="kpi-icon">👨‍🎓</span>
                </div>
                <div class="kpi-value">{total_students}</div>
                <div class="kpi-caption">Registered Candidates</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Placement Rate</span>
                    <span class="kpi-icon">🏆</span>
                </div>
                <div class="kpi-value">{placement_rate:.1f}%</div>
                <div class="kpi-caption">{placed_students} of {total_students} Placed</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Highest Package</span>
                    <span class="kpi-icon">💰</span>
                </div>
                <div class="kpi-value">{max_package:.2f} <span style="font-size: 16px; color: #93C5FD;">LPA</span></div>
                <div class="kpi-caption">Top Compensation Offered</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Average Package</span>
                    <span class="kpi-icon">📈</span>
                </div>
                <div class="kpi-value">{avg_package:.2f} <span style="font-size: 16px; color: #93C5FD;">LPA</span></div>
                <div class="kpi-caption">Mean of Offered Roles</div>
            </div>
            """, unsafe_allow_html=True)
            
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Recruiting Companies</span>
                    <span class="kpi-icon">🏢</span>
                </div>
                <div class="kpi-value">{total_companies}</div>
                <div class="kpi-caption">Corporate Partners</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col6:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Job Postings</span>
                    <span class="kpi-icon">💼</span>
                </div>
                <div class="kpi-value">{total_jobs}</div>
                <div class="kpi-caption">Active Opportunities</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col7:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Applications</span>
                    <span class="kpi-icon">📄</span>
                </div>
                <div class="kpi-value">{total_apps}</div>
                <div class="kpi-caption">Student Submissions</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col8:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Interview Rounds</span>
                    <span class="kpi-icon">🗓️</span>
                </div>
                <div class="kpi-value">{total_interviews}</div>
                <div class="kpi-caption">Evaluations Conducted</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Interactive Plots Section
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 💼 Package (LPA) by Company & Role")
        jobs_chart_df = run_query("""
            SELECT c.company_name, j.job_title, j.package_lpa, j.min_cgpa_required
            FROM job_postings j
            JOIN companies c ON j.company_id = c.company_id
            ORDER BY j.package_lpa DESC
        """)
        if not jobs_chart_df.empty:
            jobs_chart_df['Role_Company'] = jobs_chart_df['job_title'] + " (" + jobs_chart_df['company_name'] + ")"
            fig_salary = px.bar(
                jobs_chart_df,
                x='package_lpa',
                y='Role_Company',
                orientation='h',
                color='package_lpa',
                color_continuous_scale='Viridis',
                labels={'package_lpa': 'Package (LPA)', 'Role_Company': 'Role & Company'},
                text='package_lpa'
            )
            fig_salary.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=320,
                coloraxis_showscale=False
            )
            fig_salary.update_traces(texttemplate='%{text:.1f} LPA', textposition='outside')
            st.plotly_chart(fig_salary, use_container_width=True)
        else:
            st.info("No job posting data available yet.")

    with chart_col2:
        st.markdown("#### 🎓 Department Placement Distribution")
        dept_df = run_query("""
            SELECT department, 
                   SUM(CASE WHEN status = 'Placed' THEN 1 ELSE 0 END) AS Placed,
                   SUM(CASE WHEN status = 'Unplaced' THEN 1 ELSE 0 END) AS Unplaced
            FROM students
            GROUP BY department
        """)
        if not dept_df.empty:
            fig_dept = go.Figure(data=[
                go.Bar(name='Placed', x=dept_df['department'], y=dept_df['Placed'], marker_color='#10B981'),
                go.Bar(name='Unplaced', x=dept_df['department'], y=dept_df['Unplaced'], marker_color='#64748B')
            ])
            fig_dept.update_layout(
                barmode='stack',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=320,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_dept, use_container_width=True)
        else:
            st.info("No department placement records available.")

    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.markdown("#### 📑 Applications Pipeline Funnel")
        pipeline_df = run_query("""
            SELECT status, COUNT(*) AS count 
            FROM applications 
            GROUP BY status
        """)
        if not pipeline_df.empty:
            color_map = {
                'Applied': '#38BDF8',
                'Shortlisted': '#A78BFA',
                'Rejected': '#F87171'
            }
            fig_funnel = px.pie(
                pipeline_df,
                names='status',
                values='count',
                hole=0.45,
                color='status',
                color_discrete_map=color_map
            )
            fig_funnel.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=300
            )
            st.plotly_chart(fig_funnel, use_container_width=True)
        else:
            st.info("No application status records yet.")

    with col_chart4:
        st.markdown("#### 🗓️ Interview Results Breakdown")
        interview_res_df = run_query("""
            SELECT result, COUNT(*) AS count
            FROM interviews
            GROUP BY result
        """)
        if not interview_res_df.empty:
            res_colors = {
                'Selected': '#10B981',
                'Pending': '#F59E0B',
                'Rejected': '#EF4444'
            }
            fig_res = px.pie(
                interview_res_df,
                names='result',
                values='count',
                hole=0.45,
                color='result',
                color_discrete_map=res_colors
            )
            fig_res.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=300
            )
            st.plotly_chart(fig_res, use_container_width=True)
        else:
            st.info("No interview results recorded yet.")

    # Recent Placed Hall of Fame
    st.markdown("---")
    st.markdown("#### 🌟 Placement Hall of Fame (`placement_summary` View)")
    view_data = run_query("SELECT * FROM placement_summary")
    if not view_data.empty:
        st.dataframe(view_data, use_container_width=True, hide_index=True)
    else:
        st.info("No placed candidates recorded in `placement_summary` yet. As interviews are marked 'Selected', placed students will appear here automatically!")


# =========================================================
# MODULE 2: STUDENTS DIRECTORY
# =========================================================
elif choice == "👨‍🎓 Students Directory":
    st.subheader("👨‍🎓 Students Management")
    
    tab_view, tab_add, tab_edit, tab_delete = st.tabs([
        "📋 Student Directory", 
        "➕ Register New Student", 
        "✏️ Edit Student", 
        "🗑️ Remove Student"
    ])
    
    with tab_view:
        # Filter & Search bar
        search_col, dept_col, status_col = st.columns([2, 1, 1])
        with search_col:
            search_term = st.text_input("🔍 Search by Student ID, Name, or Email", placeholder="e.g., Farhan, STU001, AIML...")
        with dept_col:
            all_depts_df = run_query("SELECT DISTINCT department FROM students WHERE department IS NOT NULL AND department != ''")
            dept_options = ["All Departments"] + (all_depts_df['department'].tolist() if not all_depts_df.empty else [])
            selected_dept = st.selectbox("Department", dept_options)
        with status_col:
            selected_status = st.selectbox("Placement Status", ["All", "Placed", "Unplaced"])
            
        cgpa_slider = st.slider("Filter by Minimum CGPA", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        
        # Build query
        base_query = "SELECT student_id, first_name, last_name, email, phone, department, cgpa, status FROM students WHERE 1=1"
        query_params = []
        
        if search_term:
            base_query += " AND (student_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR email LIKE %s)"
            wildcard = f"%{search_term}%"
            query_params.extend([wildcard, wildcard, wildcard, wildcard])
            
        if selected_dept != "All Departments":
            base_query += " AND department = %s"
            query_params.append(selected_dept)
            
        if selected_status != "All":
            base_query += " AND status = %s"
            query_params.append(selected_status)
            
        base_query += " AND (cgpa >= %s OR cgpa IS NULL) ORDER BY student_id"
        query_params.append(cgpa_slider)
        
        students_df = run_query(base_query, query_params)
        
        if not students_df.empty:
            st.dataframe(
                students_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "student_id": st.column_config.TextColumn("Student ID", width="small"),
                    "first_name": "First Name",
                    "last_name": "Last Name",
                    "email": "Email Address",
                    "phone": "Contact Phone",
                    "department": "Department",
                    "cgpa": st.column_config.NumberColumn("CGPA", format="%.2f"),
                    "status": st.column_config.TextColumn("Status", width="small")
                }
            )
            # CSV Download
            csv = students_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Students CSV",
                data=csv,
                file_name=f"students_report_{date.today()}.csv",
                mime="text/csv"
            )
        else:
            st.info("No student records match the specified filters.")
            
    with tab_add:
        st.markdown("##### 📝 Register a New Student")
        with st.form("add_student_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                stu_id = st.text_input("Student ID *", placeholder="e.g., STU101").strip()
                first_name = st.text_input("First Name *", placeholder="First Name").strip()
                email = st.text_input("Email *", placeholder="student@example.edu").strip()
                department = st.text_input("Department *", placeholder="e.g., AIML, CSE, ECE").strip()
            with f_col2:
                last_name = st.text_input("Last Name *", placeholder="Last Name").strip()
                phone = st.text_input("Phone Number", placeholder="e.g., +91 9876543210").strip()
                cgpa = st.number_input("CGPA (0.0 to 10.0) *", min_value=0.0, max_value=10.0, value=7.5, step=0.01)
                status = st.selectbox("Initial Status", ["Unplaced", "Placed"])
                
            submitted = st.form_submit_button("➕ Register Student", use_container_width=True)
            if submitted:
                if not stu_id or not first_name or not last_name or not email or not department:
                    st.error("Please fill in all required fields marked with *.")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("Please enter a valid email address.")
                else:
                    insert_q = """
                    INSERT INTO students (student_id, first_name, last_name, email, phone, department, cgpa, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    success, res = execute_dml(insert_q, (stu_id, first_name, last_name, email, phone or None, department, cgpa, status))
                    if success:
                        st.success(f"✅ Student {first_name} {last_name} ({stu_id}) registered successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to add student: {res}")
                        
    with tab_edit:
        st.markdown("##### ✏️ Update Student Information")
        all_stu = run_query("SELECT student_id, first_name, last_name FROM students ORDER BY student_id")
        if not all_stu.empty:
            stu_options = {f"{r['student_id']} - {r['first_name']} {r['last_name']}": r['student_id'] for _, r in all_stu.iterrows()}
            selected_stu_label = st.selectbox("Select Student to Edit", list(stu_options.keys()))
            selected_stu_id = stu_options[selected_stu_label]
            
            curr_data = run_query("SELECT * FROM students WHERE student_id = %s", (selected_stu_id,))
            if not curr_data.empty:
                c_row = curr_data.iloc[0]
                with st.form("edit_student_form"):
                    e_col1, e_col2 = st.columns(2)
                    with e_col1:
                        new_first_name = st.text_input("First Name", value=c_row['first_name'])
                        new_email = st.text_input("Email", value=c_row['email'])
                        new_dept = st.text_input("Department", value=c_row['department'])
                    with e_col2:
                        new_last_name = st.text_input("Last Name", value=c_row['last_name'])
                        new_phone = st.text_input("Phone", value=c_row['phone'] if pd.notnull(c_row['phone']) else "")
                        new_cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=float(c_row['cgpa']) if pd.notnull(c_row['cgpa']) else 7.0, step=0.01)
                    
                    status_idx = 0 if c_row['status'] == 'Unplaced' else 1
                    new_status = st.selectbox("Placement Status", ["Unplaced", "Placed"], index=status_idx)
                    
                    update_submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)
                    if update_submitted:
                        up_q = """
                        UPDATE students 
                        SET first_name = %s, last_name = %s, email = %s, phone = %s, department = %s, cgpa = %s, status = %s
                        WHERE student_id = %s
                        """
                        up_ok, up_msg = execute_dml(up_q, (new_first_name, new_last_name, new_email, new_phone or None, new_dept, new_cgpa, new_status, selected_stu_id))
                        if up_ok:
                            st.success(f"✅ Student {selected_stu_id} updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error updating student: {up_msg}")
        else:
            st.info("No students found in the database.")
            
    with tab_delete:
        st.markdown("##### 🗑️ Remove Student Record")
        del_stu_list = run_query("SELECT student_id, first_name, last_name FROM students ORDER BY student_id")
        if not del_stu_list.empty:
            del_options = {f"{r['student_id']} - {r['first_name']} {r['last_name']}": r['student_id'] for _, r in del_stu_list.iterrows()}
            del_label = st.selectbox("Select Student to Remove", list(del_options.keys()), key="del_stu_select")
            del_id = del_options[del_label]
            
            st.warning(f"⚠️ Warning: Deleting student **{del_label}** will cascade and permanently delete all their submitted applications and interview records.")
            if st.button("🚨 Confirm Delete Student", type="primary"):
                del_ok, del_msg = execute_dml("DELETE FROM students WHERE student_id = %s", (del_id,))
                if del_ok:
                    st.success(f"✅ Student {del_id} removed successfully.")
                    st.rerun()
                else:
                    st.error(f"❌ Could not delete student: {del_msg}")
        else:
            st.info("No students available to delete.")


# =========================================================
# MODULE 3: PARTNER COMPANIES
# =========================================================
elif choice == "🏢 Partner Companies":
    st.subheader("🏢 Recruiting Partner Companies")
    
    comp_tab_dir, comp_tab_add, comp_tab_edit, comp_tab_del = st.tabs([
        "📋 Company Directory",
        "➕ Register Company",
        "✏️ Edit Company",
        "🗑️ Remove Company"
    ])
    
    with comp_tab_dir:
        comp_search = st.text_input("🔍 Search Company Name, Industry, or HR Email", placeholder="e.g., Tech, Finance, Google...")
        c_query = """
        SELECT c.company_id, c.company_name, c.hr_email, c.industry, c.website,
               COUNT(DISTINCT j.job_id) AS total_jobs_posted
        FROM companies c
        LEFT JOIN job_postings j ON c.company_id = j.company_id
        WHERE 1=1
        """
        c_params = []
        if comp_search:
            c_query += " AND (c.company_name LIKE %s OR c.industry LIKE %s OR c.hr_email LIKE %s)"
            c_wild = f"%{comp_search}%"
            c_params.extend([c_wild, c_wild, c_wild])
        c_query += " GROUP BY c.company_id, c.company_name, c.hr_email, c.industry, c.website ORDER BY c.company_name"
        
        comp_df = run_query(c_query, c_params)
        if not comp_df.empty:
            st.dataframe(
                comp_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "company_id": st.column_config.NumberColumn("ID", width="small"),
                    "company_name": "Company Name",
                    "hr_email": "HR Contact Email",
                    "industry": "Industry / Sector",
                    "website": st.column_config.LinkColumn("Website URL"),
                    "total_jobs_posted": st.column_config.NumberColumn("Jobs Posted", width="small")
                }
            )
        else:
            st.info("No companies found.")
            
    with comp_tab_add:
        st.markdown("##### ➕ Register New Recruiting Partner")
        with st.form("add_company_form", clear_on_submit=True):
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                comp_name = st.text_input("Company Name *", placeholder="e.g., Google, Amazon, Deloitte").strip()
                hr_email = st.text_input("HR Contact Email *", placeholder="recruitment@company.com").strip()
            with col_c2:
                industry = st.text_input("Industry / Domain", placeholder="e.g., IT, AI / ML, Fintech, Consulting").strip()
                website = st.text_input("Website URL", placeholder="https://www.company.com").strip()
                
            sub_comp = st.form_submit_button("🏢 Register Company", use_container_width=True)
            if sub_comp:
                if not comp_name or not hr_email:
                    st.error("Company Name and HR Email are required.")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", hr_email):
                    st.error("Please enter a valid HR email address.")
                else:
                    ins_c = """
                    INSERT INTO companies (company_name, hr_email, industry, website)
                    VALUES (%s, %s, %s, %s)
                    """
                    c_ok, c_res = execute_dml(ins_c, (comp_name, hr_email, industry or None, website or None))
                    if c_ok:
                        st.success(f"✅ Company '{comp_name}' registered successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Error adding company: {c_res}")
                        
    with comp_tab_edit:
        st.markdown("##### ✏️ Edit Company Details")
        companies_list = run_query("SELECT company_id, company_name FROM companies ORDER BY company_name")
        if not companies_list.empty:
            c_opts = {f"{r['company_name']} (ID: {r['company_id']})": r['company_id'] for _, r in companies_list.iterrows()}
            selected_c_label = st.selectbox("Select Company", list(c_opts.keys()))
            selected_c_id = c_opts[selected_c_label]
            
            c_info = run_query("SELECT * FROM companies WHERE company_id = %s", (selected_c_id,))
            if not c_info.empty:
                c_row = c_info.iloc[0]
                with st.form("edit_comp_form"):
                    e_cname = st.text_input("Company Name", value=c_row['company_name'])
                    e_hremail = st.text_input("HR Email", value=c_row['hr_email'])
                    e_ind = st.text_input("Industry", value=c_row['industry'] if pd.notnull(c_row['industry']) else "")
                    e_web = st.text_input("Website", value=c_row['website'] if pd.notnull(c_row['website']) else "")
                    
                    if st.form_submit_button("💾 Save Company Details", use_container_width=True):
                        up_cq = """
                        UPDATE companies 
                        SET company_name = %s, hr_email = %s, industry = %s, website = %s
                        WHERE company_id = %s
                        """
                        up_cok, up_cmsg = execute_dml(up_cq, (e_cname, e_hremail, e_ind or None, e_web or None, selected_c_id))
                        if up_cok:
                            st.success(f"✅ Company {e_cname} updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error updating company: {up_cmsg}")
        else:
            st.info("No companies registered yet.")
            
    with comp_tab_del:
        st.markdown("##### 🗑️ Remove Company")
        del_comps = run_query("SELECT company_id, company_name FROM companies ORDER BY company_name")
        if not del_comps.empty:
            del_c_opts = {f"{r['company_name']} (ID: {r['company_id']})": r['company_id'] for _, r in del_comps.iterrows()}
            del_c_label = st.selectbox("Select Company to Remove", list(del_c_opts.keys()), key="del_c_box")
            del_cid = del_c_opts[del_c_label]
            
            st.warning(f"⚠️ Warning: Deleting **{del_c_label}** will cascade and delete all associated job postings, student applications, and interviews!")
            if st.button("🚨 Confirm Delete Company", type="primary"):
                del_cok, del_cmsg = execute_dml("DELETE FROM companies WHERE company_id = %s", (del_cid,))
                if del_cok:
                    st.success(f"✅ Company removed successfully.")
                    st.rerun()
                else:
                    st.error(f"❌ Error deleting company: {del_cmsg}")
        else:
            st.info("No companies to remove.")


# =========================================================
# MODULE 4: JOB POSTINGS & DRIVES
# =========================================================
elif choice == "💼 Job Postings & Drives":
    st.subheader("💼 Campus Job Postings & Recruitment Drives")
    
    j_tab_view, j_tab_add, j_tab_edit, j_tab_del = st.tabs([
        "📋 Available Job Postings",
        "➕ Post New Job",
        "✏️ Edit Job Posting",
        "🗑️ Remove Job Posting"
    ])
    
    with j_tab_view:
        col_jf1, col_jf2 = st.columns(2)
        with col_jf1:
            min_lpa_filter = st.slider("Filter by Minimum Package (LPA)", min_value=0.0, max_value=50.0, value=0.0, step=1.0)
        with col_jf2:
            all_comp_names = ["All Companies"] + run_query("SELECT DISTINCT company_name FROM companies ORDER BY company_name")['company_name'].tolist()
            sel_comp_filter = st.selectbox("Filter by Company", all_comp_names)
            
        jobs_query = """
        SELECT j.job_id, c.company_name, j.job_title, j.package_lpa, j.min_cgpa_required, j.deadline,
               COUNT(a.application_id) AS total_applicants
        FROM job_postings j
        JOIN companies c ON j.company_id = c.company_id
        LEFT JOIN applications a ON j.job_id = a.job_id
        WHERE j.package_lpa >= %s
        """
        j_params = [min_lpa_filter]
        if sel_comp_filter != "All Companies":
            jobs_query += " AND c.company_name = %s"
            j_params.append(sel_comp_filter)
        jobs_query += " GROUP BY j.job_id, c.company_name, j.job_title, j.package_lpa, j.min_cgpa_required, j.deadline ORDER BY j.package_lpa DESC"
        
        all_jobs_df = run_query(jobs_query, j_params)
        if not all_jobs_df.empty:
            st.dataframe(
                all_jobs_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "job_id": st.column_config.NumberColumn("Job ID", width="small"),
                    "company_name": "Company",
                    "job_title": "Role / Position",
                    "package_lpa": st.column_config.NumberColumn("Package (LPA)", format="%.2f LPA"),
                    "min_cgpa_required": st.column_config.NumberColumn("Min CGPA Cutoff", format="%.2f"),
                    "deadline": st.column_config.DateColumn("Application Deadline"),
                    "total_applicants": st.column_config.NumberColumn("Applicants", width="small")
                }
            )
        else:
            st.info("No job postings found matching criteria.")
            
    with j_tab_add:
        st.markdown("##### ➕ Create New Job Posting")
        comp_df = run_query("SELECT company_id, company_name FROM companies ORDER BY company_name")
        if not comp_df.empty:
            c_select_map = {f"{r['company_name']} (ID: {r['company_id']})": r['company_id'] for _, r in comp_df.iterrows()}
            with st.form("add_job_form", clear_on_submit=True):
                chosen_comp_label = st.selectbox("Select Recruiting Company *", list(c_select_map.keys()))
                job_title_input = st.text_input("Job Title / Role *", placeholder="e.g., Software Development Engineer, ML Engineer").strip()
                col_j1, col_j2 = st.columns(2)
                with col_j1:
                    package_input = st.number_input("Compensation Package (LPA) *", min_value=1.0, max_value=100.0, value=12.0, step=0.5)
                with col_j2:
                    cgpa_cutoff_input = st.number_input("Minimum CGPA Eligibility *", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
                deadline_input = st.date_input("Application Deadline *", value=date.today())
                
                job_submit = st.form_submit_button("💼 Post Job Role", use_container_width=True)
                if job_submit:
                    if not job_title_input:
                        st.error("Please enter a valid job title.")
                    else:
                        chosen_cid = c_select_map[chosen_comp_label]
                        ins_jq = """
                        INSERT INTO job_postings (company_id, job_title, package_lpa, min_cgpa_required, deadline)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        j_ok, j_res = execute_dml(ins_jq, (chosen_cid, job_title_input, package_input, cgpa_cutoff_input, deadline_input))
                        if j_ok:
                            st.success(f"✅ Job '{job_title_input}' posted successfully with package {package_input} LPA!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error creating job posting: {j_res}")
        else:
            st.warning("⚠️ No companies found! Please register at least one company first before posting jobs.")
            
    with j_tab_edit:
        st.markdown("##### ✏️ Edit Existing Job Posting")
        edit_jobs_list = run_query("""
            SELECT j.job_id, c.company_name, j.job_title 
            FROM job_postings j
            JOIN companies c ON j.company_id = c.company_id
            ORDER BY j.job_id DESC
        """)
        if not edit_jobs_list.empty:
            j_edit_opts = {f"Job #{r['job_id']}: {r['job_title']} @ {r['company_name']}": r['job_id'] for _, r in edit_jobs_list.iterrows()}
            sel_j_label = st.selectbox("Select Job to Edit", list(j_edit_opts.keys()))
            sel_jid = j_edit_opts[sel_j_label]
            
            curr_job = run_query("SELECT * FROM job_postings WHERE job_id = %s", (sel_jid,))
            if not curr_job.empty:
                j_row = curr_job.iloc[0]
                with st.form("edit_job_form"):
                    ej_title = st.text_input("Job Title", value=j_row['job_title'])
                    col_ej1, col_ej2 = st.columns(2)
                    with col_ej1:
                        ej_pkg = st.number_input("Package (LPA)", min_value=0.0, max_value=100.0, value=float(j_row['package_lpa']) if pd.notnull(j_row['package_lpa']) else 10.0, step=0.5)
                    with col_ej2:
                        ej_cgpa = st.number_input("Min CGPA Required", min_value=0.0, max_value=10.0, value=float(j_row['min_cgpa_required']) if pd.notnull(j_row['min_cgpa_required']) else 7.0, step=0.1)
                    
                    curr_dl = j_row['deadline']
                    if isinstance(curr_dl, datetime):
                        curr_dl = curr_dl.date()
                    elif not isinstance(curr_dl, date):
                        curr_dl = date.today()
                    ej_dl = st.date_input("Deadline", value=curr_dl)
                    
                    if st.form_submit_button("💾 Save Job Updates", use_container_width=True):
                        up_jq = """
                        UPDATE job_postings 
                        SET job_title = %s, package_lpa = %s, min_cgpa_required = %s, deadline = %s
                        WHERE job_id = %s
                        """
                        up_jok, up_jmsg = execute_dml(up_jq, (ej_title, ej_pkg, ej_cgpa, ej_dl, sel_jid))
                        if up_jok:
                            st.success("✅ Job posting updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error updating job: {up_jmsg}")
        else:
            st.info("No job postings available to edit.")
            
    with j_tab_del:
        st.markdown("##### 🗑️ Remove Job Posting")
        del_jobs_list = run_query("""
            SELECT j.job_id, c.company_name, j.job_title 
            FROM job_postings j
            JOIN companies c ON j.company_id = c.company_id
        """)
        if not del_jobs_list.empty:
            del_j_opts = {f"Job #{r['job_id']}: {r['job_title']} @ {r['company_name']}": r['job_id'] for _, r in del_jobs_list.iterrows()}
            del_j_label = st.selectbox("Select Job to Remove", list(del_j_opts.keys()), key="del_j_box")
            del_jid = del_j_opts[del_j_label]
            
            st.warning(f"⚠️ Deleting this job will remove all student applications submitted for it.")
            if st.button("🚨 Confirm Delete Job", type="primary"):
                del_jok, del_jmsg = execute_dml("DELETE FROM job_postings WHERE job_id = %s", (del_jid,))
                if del_jok:
                    st.success("✅ Job posting removed successfully.")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {del_jmsg}")
        else:
            st.info("No job postings to remove.")


# =========================================================
# MODULE 5: APPLICATIONS PIPELINE
# =========================================================
elif choice == "📄 Applications Pipeline":
    st.subheader("📄 Student Job Applications")
    
    app_tab_view, app_tab_submit, app_tab_status, app_tab_del = st.tabs([
        "📋 All Applications",
        "➕ Submit Application (with Live Eligibility Check)",
        "🔄 Update Status",
        "🗑️ Withdraw Application"
    ])
    
    with app_tab_view:
        filter_status = st.selectbox("Filter Status", ["All", "Applied", "Shortlisted", "Rejected"])
        app_q = """
        SELECT a.application_id, s.student_id, s.first_name, s.last_name, s.department, s.cgpa,
               c.company_name, j.job_title, j.package_lpa, a.application_date, a.status
        FROM applications a
        JOIN students s ON a.student_id = s.student_id
        JOIN job_postings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        WHERE 1=1
        """
        app_params = []
        if filter_status != "All":
            app_q += " AND a.status = %s"
            app_params.append(filter_status)
        app_q += " ORDER BY a.application_id DESC"
        
        apps_df = run_query(app_q, app_params)
        if not apps_df.empty:
            st.dataframe(
                apps_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "application_id": st.column_config.NumberColumn("App ID", width="small"),
                    "student_id": "Student ID",
                    "first_name": "First Name",
                    "last_name": "Last Name",
                    "department": "Department",
                    "cgpa": st.column_config.NumberColumn("CGPA", format="%.2f"),
                    "company_name": "Company",
                    "job_title": "Role",
                    "package_lpa": st.column_config.NumberColumn("LPA", format="%.2f LPA"),
                    "application_date": st.column_config.DateColumn("Date Applied"),
                    "status": st.column_config.TextColumn("Status", width="small")
                }
            )
        else:
            st.info("No applications found.")
            
    with app_tab_submit:
        st.markdown("##### 📝 Apply Student for a Job Role")
        
        # Load Students & Jobs
        stu_list = run_query("SELECT student_id, first_name, last_name, department, cgpa FROM students ORDER BY first_name")
        job_list = run_query("""
            SELECT j.job_id, c.company_name, j.job_title, j.package_lpa, j.min_cgpa_required 
            FROM job_postings j 
            JOIN companies c ON j.company_id = c.company_id 
            ORDER BY c.company_name
        """)
        
        if not stu_list.empty and not job_list.empty:
            stu_choices = {f"{r['student_id']} - {r['first_name']} {r['last_name']} ({r['department']}, CGPA: {r['cgpa']})": r for _, r in stu_list.iterrows()}
            job_choices = {f"Job #{r['job_id']}: {r['job_title']} @ {r['company_name']} ({r['package_lpa']} LPA, Min CGPA: {r['min_cgpa_required']})": r for _, r in job_list.iterrows()}
            
            sel_stu_key = st.selectbox("Select Candidate Student *", list(stu_choices.keys()))
            sel_job_key = st.selectbox("Select Target Job Opportunity *", list(job_choices.keys()))
            
            student_obj = stu_choices[sel_stu_key]
            job_obj = job_choices[sel_job_key]
            
            # Smart Eligibility Check
            stu_cgpa = float(student_obj['cgpa']) if pd.notnull(student_obj['cgpa']) else 0.0
            req_cgpa = float(job_obj['min_cgpa_required']) if pd.notnull(job_obj['min_cgpa_required']) else 0.0
            
            if stu_cgpa >= req_cgpa:
                st.success(f"✅ **Eligibility Check Passed:** Candidate's CGPA ({stu_cgpa:.2f}) meets or exceeds the minimum cutoff ({req_cgpa:.2f}).")
            else:
                st.warning(f"⚠️ **Eligibility Warning:** Candidate's CGPA ({stu_cgpa:.2f}) is lower than the job requirement ({req_cgpa:.2f}).")
                
            # Duplicate check
            existing_app = run_query("SELECT application_id FROM applications WHERE student_id = %s AND job_id = %s", (student_obj['student_id'], job_obj['job_id']))
            if not existing_app.empty:
                st.error(f"❌ This student has already submitted an application for this role (Application ID: {existing_app.iloc[0]['application_id']}).")
                
            with st.form("submit_app_form"):
                app_date_input = st.date_input("Application Date", value=date.today())
                app_status_input = st.selectbox("Application Status", ["Applied", "Shortlisted", "Rejected"])
                
                if st.form_submit_button("🚀 Submit Application", use_container_width=True):
                    if not existing_app.empty:
                        st.error("Duplicate application prevented. Cannot submit again.")
                    else:
                        ins_app_q = """
                        INSERT INTO applications (student_id, job_id, application_date, status)
                        VALUES (%s, %s, %s, %s)
                        """
                        a_ok, a_msg = execute_dml(ins_app_q, (student_obj['student_id'], job_obj['job_id'], app_date_input, app_status_input))
                        if a_ok:
                            st.success(f"🎉 Application submitted successfully for {student_obj['first_name']} {student_obj['last_name']}!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error submitting application: {a_msg}")
        else:
            st.warning("⚠️ Need both registered students and active job postings to submit applications.")
            
    with app_tab_status:
        st.markdown("##### 🔄 Update Application Pipeline Status")
        active_apps = run_query("""
            SELECT a.application_id, s.first_name, s.last_name, c.company_name, j.job_title, a.status
            FROM applications a
            JOIN students s ON a.student_id = s.student_id
            JOIN job_postings j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
            ORDER BY a.application_id DESC
        """)
        if not active_apps.empty:
            app_dict = {f"App #{r['application_id']}: {r['first_name']} {r['last_name']} -> {r['company_name']} ({r['job_title']}) [Current: {r['status']}]": r for _, r in active_apps.iterrows()}
            selected_app_label = st.selectbox("Select Application", list(app_dict.keys()))
            selected_app = app_dict[selected_app_label]
            
            with st.form("update_app_status_form"):
                curr_stat = selected_app['status']
                stat_index = 0 if curr_stat == 'Applied' else (1 if curr_stat == 'Shortlisted' else 2)
                new_app_status = st.selectbox("New Status", ["Applied", "Shortlisted", "Rejected"], index=stat_index)
                
                if st.form_submit_button("💾 Update Status", use_container_width=True):
                    up_app_q = "UPDATE applications SET status = %s WHERE application_id = %s"
                    up_aok, up_amsg = execute_dml(up_app_q, (new_app_status, selected_app['application_id']))
                    if up_aok:
                        st.success(f"✅ Application #{selected_app['application_id']} status changed to '{new_app_status}'.")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {up_amsg}")
        else:
            st.info("No applications to update.")
            
    with app_tab_del:
        st.markdown("##### 🗑️ Withdraw / Delete Application")
        del_apps = run_query("""
            SELECT a.application_id, s.first_name, s.last_name, c.company_name, j.job_title
            FROM applications a
            JOIN students s ON a.student_id = s.student_id
            JOIN job_postings j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
        """)
        if not del_apps.empty:
            del_app_opts = {f"App #{r['application_id']}: {r['first_name']} {r['last_name']} -> {r['company_name']}": r['application_id'] for _, r in del_apps.iterrows()}
            del_app_lbl = st.selectbox("Select Application to Withdraw", list(del_app_opts.keys()), key="del_app_box")
            del_appid = del_app_opts[del_app_lbl]
            
            st.warning("⚠️ Deleting an application will cascade delete any scheduled interview rounds for it.")
            if st.button("🚨 Withdraw Application", type="primary"):
                del_aok, del_amsg = execute_dml("DELETE FROM applications WHERE application_id = %s", (del_appid,))
                if del_aok:
                    st.success("✅ Application withdrawn successfully.")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {del_amsg}")
        else:
            st.info("No applications to withdraw.")


# =========================================================
# MODULE 6: INTERVIEW MANAGEMENT
# =========================================================
elif choice == "🗓️ Interview Management":
    st.subheader("🗓️ Interview Rounds & Selection Tracking")
    
    int_tab_view, int_tab_schedule, int_tab_result, int_tab_del = st.tabs([
        "📋 Interview Schedule & Results",
        "➕ Schedule Interview Round",
        "🏆 Update Result & Selection Trigger",
        "🗑️ Cancel Interview"
    ])
    
    with int_tab_view:
        int_q = """
        SELECT i.interview_id, s.student_id, s.first_name, s.last_name, 
               c.company_name, j.job_title, i.round_number, i.interview_date, 
               i.interviewer_name, i.result
        FROM interviews i
        JOIN applications a ON i.application_id = a.application_id
        JOIN students s ON a.student_id = s.student_id
        JOIN job_postings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY i.interview_date DESC
        """
        int_df = run_query(int_q)
        if not int_df.empty:
            st.dataframe(
                int_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "interview_id": st.column_config.NumberColumn("Int ID", width="small"),
                    "student_id": "Student ID",
                    "first_name": "First Name",
                    "last_name": "Last Name",
                    "company_name": "Company",
                    "job_title": "Role",
                    "round_number": st.column_config.NumberColumn("Round #", width="small"),
                    "interview_date": st.column_config.DatetimeColumn("Interview Date & Time", format="YYYY-MM-DD HH:mm"),
                    "interviewer_name": "Interviewer",
                    "result": st.column_config.TextColumn("Result", width="small")
                }
            )
        else:
            st.info("No interview rounds scheduled yet.")
            
    with int_tab_schedule:
        st.markdown("##### ➕ Schedule an Interview Round")
        # Get applications that can be interviewed
        available_apps = run_query("""
            SELECT a.application_id, s.first_name, s.last_name, c.company_name, j.job_title, a.status
            FROM applications a
            JOIN students s ON a.student_id = s.student_id
            JOIN job_postings j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
            ORDER BY a.application_id DESC
        """)
        if not available_apps.empty:
            app_select_map = {f"App #{r['application_id']}: {r['first_name']} {r['last_name']} -> {r['company_name']} ({r['job_title']})": r['application_id'] for _, r in available_apps.iterrows()}
            with st.form("schedule_int_form", clear_on_submit=True):
                chosen_app_lbl = st.selectbox("Select Application *", list(app_select_map.keys()))
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    i_date = st.date_input("Interview Date *", value=date.today())
                    i_time = st.time_input("Interview Time *", value=datetime.now().time())
                with col_i2:
                    interviewer = st.text_input("Interviewer Name *", placeholder="e.g., Tech Lead / HR Director").strip()
                    round_num = st.number_input("Round Number", min_value=1, max_value=10, value=1, step=1)
                initial_result = st.selectbox("Interview Outcome", ["Pending", "Selected", "Rejected"])
                
                if st.form_submit_button("🗓️ Schedule Interview", use_container_width=True):
                    if not interviewer:
                        st.error("Please enter the Interviewer's Name.")
                    else:
                        chosen_appid = app_select_map[chosen_app_lbl]
                        dt_combined = datetime.combine(i_date, i_time)
                        ins_iq = """
                        INSERT INTO interviews (application_id, interview_date, interviewer_name, round_number, result)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        i_ok, i_msg = execute_dml(ins_iq, (chosen_appid, dt_combined, interviewer, round_num, initial_result))
                        if i_ok:
                            # If result is Selected, ensure student status is Placed
                            if initial_result == "Selected":
                                execute_dml("""
                                    UPDATE students 
                                    SET status = 'Placed' 
                                    WHERE student_id = (SELECT student_id FROM applications WHERE application_id = %s)
                                """, (chosen_appid,))
                                st.balloons()
                            st.success("✅ Interview successfully scheduled!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error scheduling interview: {i_msg}")
        else:
            st.warning("⚠️ No applications found. Please submit an application before scheduling an interview.")
            
    with int_tab_result:
        st.markdown("##### 🏆 Update Interview Outcome & Trigger Placement")
        active_ints = run_query("""
            SELECT i.interview_id, s.student_id, s.first_name, s.last_name, c.company_name, j.job_title, 
                   i.round_number, i.result, a.application_id
            FROM interviews i
            JOIN applications a ON i.application_id = a.application_id
            JOIN students s ON a.student_id = s.student_id
            JOIN job_postings j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
            ORDER BY i.interview_id DESC
        """)
        if not active_ints.empty:
            int_map = {f"Int #{r['interview_id']}: {r['first_name']} {r['last_name']} -> {r['company_name']} (Round {r['round_number']}, Current: {r['result']})": r for _, r in active_ints.iterrows()}
            sel_int_lbl = st.selectbox("Select Interview Record", list(int_map.keys()))
            sel_int = int_map[sel_int_lbl]
            
            with st.form("update_int_result_form"):
                res_idx = 0 if sel_int['result'] == 'Pending' else (1 if sel_int['result'] == 'Selected' else 2)
                new_result = st.selectbox("Final Result", ["Pending", "Selected", "Rejected"], index=res_idx)
                
                st.info("💡 **DBMS Automation Note:** Changing result to **Selected** will fire the MySQL trigger or synchronization logic, instantly marking the student as **'Placed'**!")
                
                if st.form_submit_button("💾 Save Result", use_container_width=True):
                    up_int_q = "UPDATE interviews SET result = %s WHERE interview_id = %s"
                    up_iok, up_imsg = execute_dml(up_int_q, (new_result, sel_int['interview_id']))
                    if up_iok:
                        if new_result == "Selected":
                            # Ensure placed status in students table
                            execute_dml("UPDATE students SET status = 'Placed' WHERE student_id = %s", (sel_int['student_id'],))
                            st.balloons()
                            st.success(f"🎉 Student {sel_int['first_name']} {sel_int['last_name']} has been SELECTED! Status updated to 'Placed' in database.")
                        else:
                            st.success(f"✅ Interview outcome updated to '{new_result}'.")
                        st.rerun()
                    else:
                        st.error(f"❌ Error updating interview: {up_imsg}")
        else:
            st.info("No interview records found.")
            
    with int_tab_del:
        st.markdown("##### 🗑️ Cancel Interview")
        del_ints = run_query("""
            SELECT i.interview_id, s.first_name, s.last_name, c.company_name, i.round_number
            FROM interviews i
            JOIN applications a ON i.application_id = a.application_id
            JOIN students s ON a.student_id = s.student_id
            JOIN job_postings j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
        """)
        if not del_ints.empty:
            del_int_opts = {f"Int #{r['interview_id']}: {r['first_name']} {r['last_name']} ({r['company_name']}, Round {r['round_number']})": r['interview_id'] for _, r in del_ints.iterrows()}
            del_int_lbl = st.selectbox("Select Interview to Delete", list(del_int_opts.keys()), key="del_int_box")
            del_int_id = del_int_opts[del_int_lbl]
            
            if st.button("🚨 Cancel and Delete Interview", type="primary"):
                del_iok, del_imsg = execute_dml("DELETE FROM interviews WHERE interview_id = %s", (del_int_id,))
                if del_iok:
                    st.success("✅ Interview canceled and deleted.")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {del_imsg}")
        else:
            st.info("No interviews available to delete.")


# =========================================================
# MODULE 7: ADVANCED REPORTS & VIEWS
# =========================================================
elif choice == "📑 Advanced Reports & Views":
    st.subheader("📑 Advanced DBMS Reports & Multi-Table Joins")
    
    rep_tab_5join, rep_tab_view, rep_tab_sql = st.tabs([
        "🔗 5-Table Master Report",
        "👁️ SQL View: placement_summary",
        "⚡ Custom SQL Explorer"
    ])
    
    with rep_tab_5join:
        st.markdown("##### 📊 Comprehensive 5-Table JOIN Placement Report")
        st.caption("Demonstrating multi-table relational JOIN across `students`, `companies`, `job_postings`, `applications`, and `interviews`.")
        
        master_q = """
        SELECT 
            i.interview_id,
            s.student_id,
            CONCAT(s.first_name, ' ', s.last_name) AS student_name,
            s.department,
            s.cgpa,
            c.company_name,
            c.industry,
            j.job_title,
            j.package_lpa,
            a.application_date,
            i.round_number,
            i.interview_date,
            i.interviewer_name,
            i.result AS interview_result,
            s.status AS student_status
        FROM interviews i
        JOIN applications a ON i.application_id = a.application_id
        JOIN students s ON a.student_id = s.student_id
        JOIN job_postings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY i.interview_date DESC
        """
        master_df = run_query(master_q)
        if not master_df.empty:
            st.dataframe(master_df, use_container_width=True, hide_index=True)
            csv_master = master_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Full 5-Table Report to CSV",
                data=csv_master,
                file_name=f"placement_master_report_{date.today()}.csv",
                mime="text/csv"
            )
        else:
            st.info("No completed interview cycles to display in the master JOIN report.")
            
    with rep_tab_view:
        st.markdown("##### 👁️ Output of Database VIEW: `placement_summary`")
        st.caption("Directly querying `SELECT * FROM placement_summary` created in MySQL schema.")
        
        ps_df = run_query("SELECT * FROM placement_summary")
        if not ps_df.empty:
            st.dataframe(ps_df, use_container_width=True, hide_index=True)
            
            # Summary Metrics for View
            tot_placed_pkg = ps_df['package_lpa'].sum()
            avg_placed_pkg = ps_df['package_lpa'].mean()
            c_p1, c_p2, c_p3 = st.columns(3)
            c_p1.metric("Total Placed Candidates", len(ps_df))
            c_p2.metric("Total Package Value", f"{tot_placed_pkg:.2f} LPA")
            c_p3.metric("Average Placed Package", f"{avg_placed_pkg:.2f} LPA")
        else:
            st.info("No candidates selected yet in `placement_summary` view.")
            
    with rep_tab_sql:
        st.markdown("##### ⚡ Interactive SQL Query Explorer")
        st.caption("Run read-only analytical queries directly on the MySQL database.")
        
        sample_queries = {
            "Top 5 Highest Paying Roles": """
                SELECT c.company_name, j.job_title, j.package_lpa, j.min_cgpa_required 
                FROM job_postings j
                JOIN companies c ON j.company_id = c.company_id
                ORDER BY j.package_lpa DESC LIMIT 5;
            """,
            "Department Placement Statistics": """
                SELECT department, 
                       COUNT(*) AS total_students,
                       SUM(CASE WHEN status = 'Placed' THEN 1 ELSE 0 END) AS placed_count,
                       ROUND(SUM(CASE WHEN status = 'Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS placement_percentage
                FROM students 
                GROUP BY department;
            """,
            "Unplaced Students with CGPA >= 8.0": """
                SELECT student_id, first_name, last_name, department, cgpa, email 
                FROM students 
                WHERE status = 'Unplaced' AND cgpa >= 8.0 
                ORDER BY cgpa DESC;
            """,
            "Companies by Total Applications Received": """
                SELECT c.company_name, COUNT(a.application_id) AS total_applications
                FROM companies c
                JOIN job_postings j ON c.company_id = j.company_id
                LEFT JOIN applications a ON j.job_id = a.job_id
                GROUP BY c.company_id, c.company_name
                ORDER BY total_applications DESC;
            """
        }
        
        preset_choice = st.selectbox("Choose a Pre-built Analytical Query", list(sample_queries.keys()))
        custom_sql = st.text_area("SQL Statement (SELECT Only)", value=sample_queries[preset_choice].strip(), height=120)
        
        if st.button("▶️ Execute Query", type="primary"):
            cleaned = custom_sql.strip().upper()
            if not cleaned.startswith("SELECT") and not cleaned.startswith("SHOW") and not cleaned.startswith("DESCRIBE"):
                st.error("⚠️ Only read-only queries (SELECT, SHOW, DESCRIBE) are permitted in the SQL Explorer.")
            else:
                start_time = datetime.now()
                res_df = run_query(custom_sql)
                elapsed = (datetime.now() - start_time).total_seconds()
                
                if not res_df.empty:
                    st.success(f"Query returned {len(res_df)} rows in {elapsed:.3f} seconds.")
                    st.dataframe(res_df, use_container_width=True)
                else:
                    st.info("Query returned 0 rows.")


# =========================================================
# MODULE 8: DATABASE & DEMO DATA
# =========================================================
elif choice == "⚙️ Database & Demo Data":
    st.subheader("⚙️ Database Diagnostics & Sample Dataset Generator")
    
    # Live Diagnostics
    st.markdown("#### 🩺 Live Connection Status")
    conn = get_db_connection()
    if conn and conn.is_connected():
        col_db1, col_db2, col_db3, col_db4 = st.columns(4)
        col_db1.metric("Database Name", "campus_placement")
        col_db2.metric("Host Server", "localhost:3306")
        col_db3.metric("MySQL Version", getattr(conn, 'server_info', '8.0+'))
        col_db4.metric("Connection Status", "🟢 Connected")
        conn.close()
    else:
        st.error("Database is currently disconnected. Please verify MySQL service status.")
        
    st.markdown("---")
    
    # Demo Seed Data Generator
    st.markdown("#### 🌟 1-Click Realistic Demo Data Generator")
    st.write("""
    Need rich data for project presentation or evaluation? Click the button below to populate the database with realistic sample records:
    - 👥 **8+ Diverse Students** across AIML, CSE, ECE, Data Science with varied CGPAs
    - 🏢 **5+ Global Tech & Finance Companies** (Google, Microsoft, Amazon, Goldman Sachs, TCS)
    - 💼 **6+ Varied Job Postings** with packages ranging from 7 LPA to 45 LPA
    - 📄 **10+ Applications** with varied statuses (`Applied`, `Shortlisted`, `Rejected`)
    - 🗓️ **Multiple Interview Rounds** with realistic outcomes triggering placements
    """)
    
    if st.button("🚀 Seed Sample Demo Records", type="primary"):
        with st.spinner("Seeding demo records into MySQL..."):
            # Sample Companies
            demo_companies = [
                ("Google India", "careers@google.com", "Big Tech / Software", "https://careers.google.com"),
                ("Microsoft IDC", "campus@microsoft.com", "Enterprise Cloud", "https://careers.microsoft.com"),
                ("Amazon AWS", "aws-hiring@amazon.com", "Cloud Infrastructure", "https://amazon.jobs"),
                ("Goldman Sachs", "recruiting@gs.com", "Fintech & Investment", "https://goldmansachs.com"),
                ("TCS Digital", "campus@tcs.com", "IT Consulting", "https://tcs.com")
            ]
            for c_name, hr_mail, ind, web in demo_companies:
                chk = run_query("SELECT company_id FROM companies WHERE company_name = %s", (c_name,))
                if chk.empty:
                    execute_dml("INSERT INTO companies (company_name, hr_email, industry, website) VALUES (%s, %s, %s, %s)", (c_name, hr_mail, ind, web))
                    
            # Sample Students
            demo_students = [
                ("STU101", "Aarav", "Sharma", "aarav.sharma@woxsen.edu.in", "9876501234", "AIML", 9.40, "Unplaced"),
                ("STU102", "Priya", "Patel", "priya.patel@woxsen.edu.in", "9876501235", "CSE", 8.85, "Unplaced"),
                ("STU103", "Rahul", "Verma", "rahul.verma@woxsen.edu.in", "9876501236", "ECE", 7.90, "Unplaced"),
                ("STU104", "Ananya", "Reddy", "ananya.reddy@woxsen.edu.in", "9876501237", "Data Science", 9.10, "Unplaced"),
                ("STU105", "Karan", "Mehta", "karan.mehta@woxsen.edu.in", "9876501238", "CSE", 8.20, "Unplaced"),
                ("STU106", "Sneha", "Nair", "sneha.nair@woxsen.edu.in", "9876501239", "AIML", 7.45, "Unplaced"),
                ("STU107", "Vikram", "Iyer", "vikram.iyer@woxsen.edu.in", "9876501240", "IT", 8.60, "Unplaced"),
                ("STU108", "Riya", "Sen", "riya.sen@woxsen.edu.in", "9876501241", "CSE", 9.75, "Unplaced")
            ]
            for sid, fn, ln, em, ph, dp, cg, stt in demo_students:
                chk = run_query("SELECT student_id FROM students WHERE student_id = %s", (sid,))
                if chk.empty:
                    execute_dml("INSERT INTO students (student_id, first_name, last_name, email, phone, department, cgpa, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (sid, fn, ln, em, ph, dp, cg, stt))
                    
            # Sample Jobs
            google_row = run_query("SELECT company_id FROM companies WHERE company_name = 'Google India'")
            ms_row = run_query("SELECT company_id FROM companies WHERE company_name = 'Microsoft IDC'")
            amazon_row = run_query("SELECT company_id FROM companies WHERE company_name = 'Amazon AWS'")
            gs_row = run_query("SELECT company_id FROM companies WHERE company_name = 'Goldman Sachs'")
            
            if not google_row.empty:
                gid = int(google_row.iloc[0]['company_id'])
                if run_query("SELECT job_id FROM job_postings WHERE company_id = %s AND job_title = 'AI Research Associate'", (gid,)).empty:
                    execute_dml("INSERT INTO job_postings (company_id, job_title, package_lpa, min_cgpa_required, deadline) VALUES (%s, %s, %s, %s, %s)", (gid, "AI Research Associate", 38.00, 8.50, date(2026, 12, 15)))
            if not ms_row.empty:
                msid = int(ms_row.iloc[0]['company_id'])
                if run_query("SELECT job_id FROM job_postings WHERE company_id = %s AND job_title = 'Software Engineer II'", (msid,)).empty:
                    execute_dml("INSERT INTO job_postings (company_id, job_title, package_lpa, min_cgpa_required, deadline) VALUES (%s, %s, %s, %s, %s)", (msid, "Software Engineer II", 32.00, 8.00, date(2026, 12, 20)))
            if not amazon_row.empty:
                amid = int(amazon_row.iloc[0]['company_id'])
                if run_query("SELECT job_id FROM job_postings WHERE company_id = %s AND job_title = 'Cloud Support Engineer'", (amid,)).empty:
                    execute_dml("INSERT INTO job_postings (company_id, job_title, package_lpa, min_cgpa_required, deadline) VALUES (%s, %s, %s, %s, %s)", (amid, "Cloud Support Engineer", 24.00, 7.50, date(2026, 11, 30)))
            if not gs_row.empty:
                gsid = int(gs_row.iloc[0]['company_id'])
                if run_query("SELECT job_id FROM job_postings WHERE company_id = %s AND job_title = 'Quantitative Analyst'", (gsid,)).empty:
                    execute_dml("INSERT INTO job_postings (company_id, job_title, package_lpa, min_cgpa_required, deadline) VALUES (%s, %s, %s, %s, %s)", (gsid, "Quantitative Analyst", 28.00, 8.00, date(2026, 12, 10)))
                    
            # Sample Applications & Interviews
            # Let's link STU101 to Google AI Research Associate
            ai_job = run_query("SELECT job_id FROM job_postings WHERE job_title = 'AI Research Associate'")
            if not ai_job.empty:
                jid = int(ai_job.iloc[0]['job_id'])
                app_chk = run_query("SELECT application_id FROM applications WHERE student_id = 'STU101' AND job_id = %s", (jid,))
                if app_chk.empty:
                    execute_dml("INSERT INTO applications (student_id, job_id, application_date, status) VALUES ('STU101', %s, %s, 'Shortlisted')", (jid, date.today()))
                    new_appid_row = run_query("SELECT application_id FROM applications WHERE student_id = 'STU101' AND job_id = %s", (jid,))
                    if not new_appid_row.empty:
                        app_id = int(new_appid_row.iloc[0]['application_id'])
                        execute_dml("INSERT INTO interviews (application_id, interview_date, interviewer_name, round_number, result) VALUES (%s, %s, 'Dr. Sundar / HR', 1, 'Selected')", (app_id, datetime.now()))
                        execute_dml("UPDATE students SET status = 'Placed' WHERE student_id = 'STU101'")
                        
            # Link STU108 (9.75 CGPA) to Microsoft
            ms_job = run_query("SELECT job_id FROM job_postings WHERE job_title = 'Software Engineer II'")
            if not ms_job.empty:
                jid = int(ms_job.iloc[0]['job_id'])
                app_chk = run_query("SELECT application_id FROM applications WHERE student_id = 'STU108' AND job_id = %s", (jid,))
                if app_chk.empty:
                    execute_dml("INSERT INTO applications (student_id, job_id, application_date, status) VALUES ('STU108', %s, %s, 'Shortlisted')", (jid, date.today()))
                    new_appid_row = run_query("SELECT application_id FROM applications WHERE student_id = 'STU108' AND job_id = %s", (jid,))
                    if not new_appid_row.empty:
                        app_id = int(new_appid_row.iloc[0]['application_id'])
                        execute_dml("INSERT INTO interviews (application_id, interview_date, interviewer_name, round_number, result) VALUES (%s, %s, 'Satya / Lead Arch', 1, 'Selected')", (app_id, datetime.now()))
                        execute_dml("UPDATE students SET status = 'Placed' WHERE student_id = 'STU108'")

            st.balloons()
            st.success("✅ Demo sample dataset successfully seeded! Switch to the Executive Dashboard to view analytics.")
            st.rerun()