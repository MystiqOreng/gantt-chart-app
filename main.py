"""Projects123 - Keep all your balls in the air
Professional project management with Kanban boards and Gantt timelines.
"""

from fasthtml.common import *
from datetime import datetime
from database import init_db, get_db, Project, Task, seed_sample_data
from auth import check_password, is_authenticated
import os

# Initialize database
init_db()
seed_sample_data()

# Projects123 Logo - Multiple balls in the air
LOGO_SVG = """
<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
    <circle cx="20" cy="12" r="4" fill="#FF6B35"/>
    <circle cx="12" cy="24" r="4" fill="#FF6B35"/>
    <circle cx="28" cy="24" r="4" fill="#FF6B35"/>
    <circle cx="20" cy="32" r="4" fill="#FF8C42"/>
    <line x1="20" y1="16" x2="14" y2="21" stroke="#FF6B35" stroke-width="2"/>
    <line x1="20" y1="16" x2="26" y2="21" stroke="#FF6B35" stroke-width="2"/>
    <line x1="14" y1="26" x2="20" y2="28" stroke="#FF8C42" stroke-width="2"/>
    <line x1="26" y1="26" x2="20" y2="28" stroke="#FF8C42" stroke-width="2"/>
</svg>
"""

LOGO_LARGE = """
<svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
    <circle cx="60" cy="36" r="12" fill="#FF6B35"/>
    <circle cx="36" cy="72" r="12" fill="#FF6B35"/>
    <circle cx="84" cy="72" r="12" fill="#FF6B35"/>
    <circle cx="60" cy="96" r="12" fill="#FF8C42"/>
    <line x1="60" y1="48" x2="42" y2="63" stroke="#FF6B35" stroke-width="4"/>
    <line x1="60" y1="48" x2="78" y2="63" stroke="#FF6B35" stroke-width="4"/>
    <line x1="42" y1="78" x2="60" y2="84" stroke="#FF8C42" stroke-width="4"/>
    <line x1="78" y1="78" x2="60" y2="84" stroke="#FF8C42" stroke-width="4"/>
</svg>
"""

# App setup with Frappe Gantt and Projects123 theme
app, rt = fast_app(
    hdrs=(
        Script(src="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js"),
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.css"),
        Style("""
            /* Projects123 Theme - Professional Orange on Dark */
            :root {
                --p123-orange: #FF6B35;
                --p123-orange-light: #FF8C42;
                --p123-dark-bg: #1a1a1a;
                --p123-card-bg: #242424;
                --p123-input-bg: #2d2d2d;
                --p123-border: rgba(255, 107, 53, 0.2);
                --p123-text: #ffffff;
                --p123-text-muted: #b0b0b0;
                --p123-success: #4CAF50;
                --p123-danger: #f44336;
            }
            
            * { box-sizing: border-box; }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
                background: var(--p123-dark-bg);
                color: var(--p123-text);
                line-height: 1.6;
            }
            
            /* Landing Page */
            .landing-hero {
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, var(--p123-dark-bg) 0%, #2a1810 100%);
                text-align: center;
                padding: 40px 20px;
            }
            
            .logo-float { animation: float 3s ease-in-out infinite; }
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }
            
            .landing-title {
                font-size: 4em;
                font-weight: bold;
                margin: 20px 0;
                background: linear-gradient(135deg, var(--p123-orange), var(--p123-orange-light));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .landing-tagline {
                font-size: 1.5em;
                color: var(--p123-text-muted);
                margin-bottom: 40px;
                max-width: 600px;
            }
            
            .cta-btn {
                background: var(--p123-orange);
                color: white;
                padding: 15px 40px;
                font-size: 1.2em;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s;
                font-weight: 600;
            }
            .cta-btn:hover {
                background: var(--p123-orange-light);
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(255, 107, 53, 0.4);
            }
            
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 30px;
                max-width: 1000px;
                margin: 60px auto;
                padding: 0 20px;
            }
            
            .feature-card {
                background: var(--p123-card-bg);
                padding: 30px;
                border-radius: 12px;
                border: 1px solid var(--p123-border);
                text-align: left;
            }
            .feature-icon { font-size: 3em; margin-bottom: 15px; }
            .feature-card h3 { color: var(--p123-orange); margin: 15px 0; }
            .feature-card p { color: var(--p123-text-muted); margin: 0; }
            
            /* App Container */
            .app-container {
                max-width: 1600px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .app-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                padding: 20px;
                background: var(--p123-card-bg);
                border-radius: 12px;
                border: 1px solid var(--p123-border);
            }
            
            .app-branding {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .app-title {
                margin: 0;
                font-size: 24px;
                color: var(--p123-orange);
            }
            
            .app-subtitle {
                margin: 0;
                font-size: 12px;
                color: var(--p123-text-muted);
            }
            
            /* Buttons */
            button, .btn {
                background: var(--p123-orange);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: all 0.2s;
            }
            button:hover, .btn:hover {
                background: var(--p123-orange-light);
                transform: translateY(-1px);
            }
            
            .btn-outline {
                background: transparent;
                border: 1px solid var(--p123-orange);
                color: var(--p123-orange);
            }
            .btn-outline:hover {
                background: var(--p123-orange);
                color: white;
            }
            
            .btn-sm { padding: 6px 12px; font-size: 12px; }
            .btn-danger { background: var(--p123-danger); }
            .btn-danger:hover { background: #da190b; }
            .btn-success { background: var(--p123-success); }
            .btn-success:hover { background: #45a049; }
            
            /* Forms */
            input, select, textarea {
                width: 100%;
                padding: 10px 12px;
                border: 1px solid var(--p123-border);
                border-radius: 6px;
                background: var(--p123-input-bg);
                color: var(--p123-text);
                font-size: 14px;
            }
            input:focus, select:focus, textarea:focus {
                outline: none;
                border-color: var(--p123-orange);
            }
            
            label {
                display: block;
                margin-bottom: 5px;
                color: var(--p123-text-muted);
                font-size: 13px;
                font-weight: 500;
            }
            
            .form-group { margin-bottom: 15px; }
            
            /* Kanban Board */
            .kanban-container {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin: 20px 0;
            }
            
            @media (max-width: 968px) {
                .kanban-container {
                    grid-template-columns: 1fr;
                }
            }
            
            .kanban-column {
                background: var(--p123-card-bg);
                border-radius: 12px;
                padding: 20px;
                border-top: 4px solid;
                min-height: 500px;
            }
            .kanban-column.not-started { border-top-color: #6B7280; }
            .kanban-column.in-progress { border-top-color: var(--p123-orange); }
            .kanban-column.completed { border-top-color: var(--p123-success); }
            
            .kanban-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid var(--p123-border);
            }
            
            .kanban-title {
                font-size: 16px;
                font-weight: 600;
                color: var(--p123-text);
            }
            
            .kanban-count {
                background: var(--p123-input-bg);
                padding: 2px 10px;
                border-radius: 12px;
                font-size: 12px;
                color: var(--p123-text-muted);
            }
            
            .kanban-card {
                background: var(--p123-input-bg);
                border: 1px solid var(--p123-border);
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 12px;
                cursor: pointer;
                transition: all 0.2s;
            }
            .kanban-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(255, 107, 53, 0.2);
            }
            .kanban-card.completed { opacity: 0.7; }
            
            .kanban-card-title {
                font-weight: 500;
                margin-bottom: 8px;
                color: var(--p123-text);
            }
            .kanban-card.completed .kanban-card-title {
                text-decoration: line-through;
            }
            
            .kanban-card-desc {
                font-size: 12px;
                color: var(--p123-text-muted);
                margin-bottom: 10px;
            }
            
            .kanban-card-meta {
                font-size: 11px;
                color: var(--p123-text-muted);
                margin-bottom: 10px;
            }
            
            .kanban-progress {
                height: 4px;
                background: var(--p123-dark-bg);
                border-radius: 2px;
                overflow: hidden;
                margin-bottom: 10px;
            }
            .kanban-progress-fill {
                height: 100%;
                background: var(--p123-orange);
                transition: width 0.3s;
            }
            
            .kanban-actions {
                display: flex;
                gap: 8px;
                margin-top: 10px;
            }
            
            /* Gantt View */
            #gantt-container {
                background: var(--p123-card-bg);
                padding: 20px;
                border-radius: 12px;
                border: 1px solid var(--p123-border);
                overflow-x: auto;
            }
            
            /* View Toggle */
            .view-toggle {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                background: var(--p123-card-bg);
                padding: 10px;
                border-radius: 8px;
                border: 1px solid var(--p123-border);
            }
            .view-toggle button {
                background: transparent;
                color: var(--p123-text-muted);
                border: none;
            }
            .view-toggle button.active {
                background: var(--p123-orange);
                color: white;
            }
            
            /* Project Selector */
            .project-selector {
                background: var(--p123-card-bg);
                padding: 20px;
                border-radius: 12px;
                border: 1px solid var(--p123-border);
                margin-bottom: 20px;
            }
            
            /* Modals */
            .modal-overlay {
                position: fixed;
                inset: 0;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
                animation: fadeIn 0.2s;
            }
            
            .modal-content {
                background: var(--p123-card-bg);
                border-radius: 12px;
                border: 1px solid var(--p123-border);
                padding: 30px;
                max-width: 500px;
                width: 90%;
                max-height: 90vh;
                overflow-y: auto;
                animation: slideIn 0.2s;
            }
            
            @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
            @keyframes slideIn { from { transform: translateY(-20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
            
            /* Utilities */
            .section { margin-bottom: 30px; }
            .section-title {
                font-size: 18px;
                font-weight: 600;
                color: var(--p123-orange);
                margin-bottom: 15px;
            }
            
            /* Audio ding */
            .ding-sound { display: none; }
        """)
    )
)

# Force HTTPS redirect (for production deployment)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse as StarletteRedirect

class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Only redirect in production (when not localhost)
        if request.url.scheme == "http" and "localhost" not in request.url.hostname:
            url = request.url.replace(scheme="https")
            return StarletteRedirect(str(url), status_code=301)
        return await call_next(request)

app.add_middleware(HTTPSRedirectMiddleware)

# ── Helper Functions ──────────────────────────────────────────────────

def categorize_tasks(tasks):
    """Categorize tasks into Kanban columns."""
    not_started = [t for t in tasks if t.progress == 0 and not t.completed]
    in_progress = [t for t in tasks if 0 < t.progress < 100 and not t.completed]
    completed = [t for t in tasks if t.completed == 1]
    return not_started, in_progress, completed


def task_card_kanban(task, project_id, view="kanban"):
    """Render a task card for Kanban view."""
    is_completed = task.completed == 1
    
    # Determine which actions to show
    actions = []
    
    if task.progress == 0 and not is_completed:
        # Not Started - show Start button
        actions.append(
            Form(
                Button("▶ Start", cls="btn btn-sm"),
                method="post",
                action=f"/tasks/{task.id}/start?project_id={project_id}&view={view}",
                style="display: inline;"
            )
        )
    elif not is_completed:
        # In Progress - show Done button
        actions.append(
            Form(
                Button("✓ Done", cls="btn btn-success btn-sm", onclick="playDingSound()"),
                method="post",
                action=f"/tasks/{task.id}/complete?project_id={project_id}&view={view}",
                style="display: inline;"
            )
        )
    else:
        # Completed - show Remove button
        actions.append(
            Form(
                Button("✕ Remove", cls="btn btn-danger btn-sm"),
                method="post",
                action=f"/tasks/{task.id}/delete?project_id={project_id}&view={view}",
                onsubmit="return confirm('Permanently delete this task?')",
                style="display: inline;"
            )
        )
    
    return Div(
        Div(task.name, cls="kanban-card-title"),
        Div(task.description or "No description", cls="kanban-card-desc"),
        Div(f"{task.start_date.strftime('%m/%d')} → {task.end_date.strftime('%m/%d')}", cls="kanban-card-meta"),
        Div(
            Div(style=f"width: {task.progress}%", cls="kanban-progress-fill"),
            cls="kanban-progress"
        ) if not is_completed else "",
        Div(*actions, cls="kanban-actions"),
        cls=f"kanban-card {'completed' if is_completed else ''}"
    )


# ── Routes ────────────────────────────────────────────────────────────

@rt('/')
def get(request):
    """Landing page or redirect to app if authenticated."""
    if is_authenticated(request):
        return RedirectResponse('/app', status_code=303)
    
    return Title("Projects123 - Keep All Your Balls in the Air"), Main(
        # Hero
        Div(
            Div(NotStr(LOGO_LARGE), cls="logo-float"),
            H1("Projects", cls="landing-title", style="display: inline;"),
            H1("123", cls="landing-title", style="display: inline; margin-left: -30px;"),
            P("Keep all your balls in the air with visual project management", cls="landing-tagline"),
            A("Get Started →", href="/login", cls="cta-btn"),
            cls="landing-hero"
        ),
        
        # Features
        Div(
            Div(
                Div(
                    Div("📋", cls="feature-icon"),
                    H3("Kanban Boards"),
                    P("Visualize workflow across Not Started, In Progress, and Completed stages.")
                , cls="feature-card"),
                Div(
                    Div("📊", cls="feature-icon"),
                    H3("Gantt Timeline"),
                    P("Interactive timelines with drag-and-drop date adjustments.")
                , cls="feature-card"),
                Div(
                    Div("🎯", cls="feature-icon"),
                    H3("Multiple Projects"),
                    P("Manage multiple projects effortlessly. Switch with one click.")
                , cls="feature-card"),
                cls="feature-grid"
            ),
            style="padding: 60px 20px; background: var(--p123-dark-bg);"
        ),
        
        # CTA
        Div(
            H2("Ready to get organized?", style="color: var(--p123-text); margin-bottom: 20px; font-size: 2em;"),
            A("Start Managing Projects", href="/login", cls="cta-btn"),
            style="text-align: center; padding: 80px 20px; background: var(--p123-card-bg);"
        )
    )


@rt('/login')
def get():
    """Login page."""
    return Title("Login - Projects123"), Main(
        Div(
            Div(
                Div(NotStr(LOGO_SVG), style="width: 80px; height: 80px; margin: 0 auto 20px;"),
                H1("Projects123", style="color: var(--p123-orange); text-align: center; margin-bottom: 10px; font-size: 2em;"),
                P("Please log in to access your projects", style="color: var(--p123-text-muted); margin-bottom: 30px; text-align: center;"),
                
                Form(
                    Div(
                        Label("Username"),
                        Input(type="text", name="username", placeholder="Enter username", required=True, autofocus=True),
                        cls="form-group"
                    ),
                    Div(
                        Label("Password"),
                        Input(type="password", name="password", placeholder="Enter password", required=True),
                        cls="form-group"
                    ),
                    Button("Login", type="submit", style="width: 100%; padding: 12px; font-size: 16px;"),
                    method="post",
                    action="/login"
                ),
                
                Div(
                    A("← Back to Home", href="/", style="color: var(--p123-orange); text-decoration: none; font-size: 14px;"),
                    style="text-align: center; margin-top: 20px;"
                ),
                
                style="background: var(--p123-card-bg); padding: 40px; border-radius: 12px; max-width: 400px; width: 100%; border: 1px solid var(--p123-border);"
            ),
            style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px;"
        )
    )


@rt('/login')
def post(username: str, password: str, request):
    """Handle login."""
    if check_password(username, password):
        request.session['authenticated'] = True
        return RedirectResponse('/app', status_code=303)
    else:
        return Title("Login - Projects123"), Main(
            Div(
                Div(
                    P("Invalid username or password", style="color: var(--p123-danger); text-align: center; margin-bottom: 20px;"),
                    A("← Try Again", href="/login", cls="btn btn-outline"),
                    style="background: var(--p123-card-bg); padding: 40px; border-radius: 12px; max-width: 400px; text-align: center;"
                ),
                style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px;"
            )
        )


@rt('/logout')
def post(request):
    """Handle logout."""
    request.session.clear()
    return RedirectResponse('/', status_code=303)


@rt('/app')
def get(request, project_id: int = None, view: str = "kanban"):
    """Main application - Kanban or Gantt view."""
    if not is_authenticated(request):
        return RedirectResponse('/login', status_code=303)
    
    db = get_db()
    projects = db.query(Project).all()
    
    # Auto-select first project
    if not project_id and projects:
        project_id = projects[0].id
    
    # Get selected project and tasks
    selected_project = None
    selected_tasks = []
    if project_id:
        selected_project = db.query(Project).filter(Project.id == project_id).first()
        if selected_project:
            selected_tasks = db.query(Task).filter(Task.project_id == project_id).all()
    
    # Categorize for Kanban
    not_started, in_progress, completed = categorize_tasks(selected_tasks)
    
    # Project data
    project_data = []
    for p in projects:
        project_data.append({
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'task_count': len(p.tasks)
        })
    
    db.close()
    
    return Title("Projects123"), Main(
        Div(
            # Header
            Div(
                Div(
                    Div(NotStr(LOGO_SVG)),
                    Div(
                        H1("Projects123", cls="app-title"),
                        P("Keep all your balls in the air", cls="app-subtitle")
                    ),
                    cls="app-branding"
                ),
                Form(
                    Button("🚪 Logout", cls="btn btn-danger", type="submit"),
                    method="post",
                    action="/logout"
                ),
                cls="app-header"
            ),
            
            # Project Selector
            Div(
                Div("📁 Select Project", cls="section-title"),
                Select(
                    *[Option(p['name'], value=p['id'], selected=(p['id'] == project_id)) for p in project_data],
                    name="project_id",
                    onchange=f"window.location.href='/app?project_id=' + this.value + '&view={view}'",
                    style="padding: 12px; font-size: 16px;"
                ) if project_data else P("No projects. Create one in project management below.", style="color: var(--p123-text-muted);"),
                cls="project-selector"
            ) if project_data else "",
            
            # View Toggle
            Div(
                Button("📋 Kanban Board", 
                       onclick=f"window.location.href='/app?project_id={project_id}&view=kanban'",
                       cls="active" if view == "kanban" else ""),
                Button("📊 Gantt Timeline", 
                       onclick=f"window.location.href='/app?project_id={project_id}&view=gantt'",
                       cls="active" if view == "gantt" else ""),
                cls="view-toggle"
            ) if selected_project else "",
            
            # Kanban View
            Div(
                Div(
                    # Not Started Column
                    Div(
                        Div(
                            Div(
                                Span("Not Started", cls="kanban-title"),
                                Span(str(len(not_started)), cls="kanban-count"),
                                style="display: flex; align-items: center; gap: 10px;"
                            ),
                            cls="kanban-header"
                        ),
                        *[task_card_kanban(t, project_id, view) for t in not_started],
                        P("No tasks", style="color: var(--p123-text-muted); text-align: center;") if not not_started else "",
                        cls="kanban-column not-started"
                    ),
                    
                    # In Progress Column
                    Div(
                        Div(
                            Div(
                                Span("In Progress", cls="kanban-title"),
                                Span(str(len(in_progress)), cls="kanban-count"),
                                style="display: flex; align-items: center; gap: 10px;"
                            ),
                            cls="kanban-header"
                        ),
                        *[task_card_kanban(t, project_id, view) for t in in_progress],
                        P("No tasks", style="color: var(--p123-text-muted); text-align: center;") if not in_progress else "",
                        cls="kanban-column in-progress"
                    ),
                    
                    # Completed Column
                    Div(
                        Div(
                            Div(
                                Span("✓ Completed", cls="kanban-title"),
                                Span(str(len(completed)), cls="kanban-count"),
                                style="display: flex; align-items: center; gap: 10px;"
                            ),
                            cls="kanban-header"
                        ),
                        *[task_card_kanban(t, project_id, view) for t in completed],
                        P("No completed tasks yet", style="color: var(--p123-text-muted); text-align: center;") if not completed else "",
                        cls="kanban-column completed"
                    ),
                    
                    cls="kanban-container"
                ),
                cls="section"
            ) if selected_project and view == "kanban" else "",
            
            # Gantt View
            Div(
                Div(f"📊 Gantt Timeline - {selected_project.name}", cls="section-title"),
                Div(id="gantt-container"),
                Script(f"""
                    const tasks = {[task.to_dict() for task in selected_tasks]};
                    if (tasks.length > 0) {{
                        new Gantt("#gantt-container", tasks, {{
                            view_mode: 'Week',
                            bar_height: 30,
                            bar_corner_radius: 3,
                            arrow_curve: 5,
                            padding: 18,
                            date_format: 'YYYY-MM-DD',
                            custom_popup_html: function(task) {{
                                return `
                                    <div style="padding: 12px; min-width: 200px; background: var(--p123-card-bg); color: var(--p123-text); border-radius: 8px;">
                                        <h5 style="margin: 0 0 8px 0;">${{task.name}}</h5>
                                        <p style="margin: 0 0 6px 0; font-size: 12px; color: var(--p123-text-muted);">${{task.description || 'No description'}}</p>
                                        <p style="margin: 0; font-size: 13px;"><strong>Progress:</strong> ${{task.progress}}%</p>
                                        <p style="margin: 4px 0 0 0; font-size: 12px;">${{task.start}} → ${{task.end}}</p>
                                    </div>
                                `;
                            }},
                            on_date_change: function(task, start, end) {{
                                fetch('/tasks/' + task.id + '/update-dates', {{
                                    method: 'POST',
                                    headers: {{'Content-Type': 'application/json'}},
                                    body: JSON.stringify({{
                                        start_date: start.toISOString().split('T')[0],
                                        end_date: end.toISOString().split('T')[0]
                                    }})
                                }}).then(() => window.location.reload());
                            }}
                        }});
                    }}
                """) if selected_tasks else "",
                cls="section"
            ) if selected_project and view == "gantt" else "",
            
            # Quick Add Task
            Div(
                Div("➕ Quick Add Task", cls="section-title"),
                Form(
                    Input(type="hidden", name="project_id", value=str(project_id) if project_id else ""),
                    Div(
                        Div(
                            Label("Task Name *"),
                            Input(name="name", placeholder="e.g., Design mockups", required=True),
                            cls="form-group"
                        ),
                        Div(
                            Label("Description"),
                            Input(name="description", placeholder="What needs to be done?"),
                            cls="form-group"
                        ),
                        style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;"
                    ),
                    Div(
                        Div(
                            Label("Start Date *"),
                            Input(type="date", name="start_date", required=True),
                            cls="form-group"
                        ),
                        Div(
                            Label("End Date *"),
                            Input(type="date", name="end_date", required=True),
                            cls="form-group"
                        ),
                        Div(
                            Label("Progress (%) *"),
                            Input(type="number", name="progress", value="0", min="0", max="100", required=True),
                            cls="form-group"
                        ),
                        style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;"
                    ),
                    Button("Add Task", type="submit"),
                    method="post",
                    action=f"/tasks/add?view={view}",
                    style="background: var(--p123-card-bg); padding: 20px; border-radius: 12px; border: 1px solid var(--p123-border);"
                ),
                cls="section"
            ) if selected_project else "",
            
            # Project Management
            Div(
                Div("⚙️ Project Management", cls="section-title"),
                Div(
                    H3("Create New Project", style="color: var(--p123-text); margin-bottom: 15px;"),
                    Form(
                        Div(
                            Label("Project Name *"),
                            Input(name="name", placeholder="e.g., Website Redesign", required=True),
                            cls="form-group"
                        ),
                        Div(
                            Label("Description"),
                            Input(name="description", placeholder="Brief description"),
                            cls="form-group"
                        ),
                        Button("Create Project", type="submit"),
                        method="post",
                        action="/projects/add"
                    ),
                    style="background: var(--p123-card-bg); padding: 20px; border-radius: 12px; border: 1px solid var(--p123-border); margin-bottom: 20px;"
                ),
                
                Div(
                    H3("All Projects", style="color: var(--p123-text); margin-bottom: 15px;"),
                    *[Div(
                        Div(
                            Div(p['name'], style="font-weight: 600; margin-bottom: 5px;"),
                            Div(p['description'] or "No description", style="font-size: 13px; color: var(--p123-text-muted);"),
                            Div(f"{p['task_count']} tasks", style="font-size: 12px; color: var(--p123-text-muted); margin-top: 5px;")
                        ),
                        Form(
                            Button("Delete", cls="btn btn-danger btn-sm", type="submit"),
                            method="post",
                            action=f"/projects/{p['id']}/delete",
                            onsubmit="return confirm('Delete this project and all its tasks?')"
                        ),
                        style="display: flex; justify-content: space-between; align-items: center; background: var(--p123-input-bg); padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid var(--p123-border);"
                    ) for p in project_data],
                    style="background: var(--p123-card-bg); padding: 20px; border-radius: 12px; border: 1px solid var(--p123-border);"
                ) if project_data else "",
                cls="section"
            ),
            
            # Audio for completion ding
            Script("""
                function playDingSound() {
                    const ctx = new (window.AudioContext || window.webkitAudioContext)();
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.frequency.value = 800;
                    osc.type = 'sine';
                    gain.gain.setValueAtTime(0.3, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);
                    osc.start(ctx.currentTime);
                    osc.stop(ctx.currentTime + 0.5);
                }
            """),
            
            cls="app-container"
        )
    )


# ── CRUD Routes ───────────────────────────────────────────────────────

@rt('/projects/add')
def post(request, name: str, description: str = ""):
    if not is_authenticated(request):
        return RedirectResponse('/login', status_code=303)
    db = get_db()
    project = Project(name=name, description=description)
    db.add(project)
    db.commit()
    new_id = project.id
    db.close()
    return RedirectResponse(f'/app?project_id={new_id}', status_code=303)


@rt('/projects/{project_id}/delete')
def post(request, project_id: int):
    if not is_authenticated(request):
        return RedirectResponse('/login', status_code=303)
    db = get_db()
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
    db.close()
    return RedirectResponse('/app', status_code=303)


@rt('/tasks/add')
def post(request, project_id: int, name: str, start_date: str, end_date: str, 
         progress: int = 0, description: str = "", view: str = "kanban"):
    if not is_authenticated(request):
        return RedirectResponse('/login', status_code=303)
    db = get_db()
    task = Task(
        project_id=project_id,
        name=name,
        description=description,
        start_date=datetime.strptime(start_date, '%Y-%m-%d'),
        end_date=datetime.strptime(end_date, '%Y-%m-%d'),
        progress=progress,
        completed=0
    )
    db.add(task)
    db.commit()
    db.close()
    return RedirectResponse(f'/app?project_id={project_id}&view={view}', status_code=303)


@rt('/tasks/{task_id}/start')
def post(request, task_id: int, project_id: int, view: str = "kanban"):
    if not is_authenticated(request):
        return RedirectResponse('/login', status_code=303)
    db = get_db()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.progress = 10  # Move to In Progress
        db.commit()
    db.close()
    return RedirectResponse(f'/app?project_id={project_id}&view={view}', status_code=303)


@rt('/tasks/{task_id}/complete')
def post(request, task_id: int, project_id: int, view: str = "kanban"):
    if not is_authenticated(request):
        return RedirectResponse('/login', status_code=303)
    db = get_db()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completed = 1
        task.progress = 100
        db.commit()
    db.close()
    return RedirectResponse(f'/app?project_id={project_id}&view={view}', status_code=303)


@rt('/tasks/{task_id}/delete')
def post(request, task_id: int, project_id: int = None, view: str = "kanban"):
    if not is_authenticated(request):
        return RedirectResponse('/login', status_code=303)
    db = get_db()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        if not project_id:
            project_id = task.project_id
        db.delete(task)
        db.commit()
    db.close()
    return RedirectResponse(f'/app?project_id={project_id}&view={view}' if project_id else '/app', status_code=303)


@rt('/tasks/{task_id}/update-dates')
async def post(task_id: int, request):
    from fasthtml.common import JSONResponse
    if not is_authenticated(request):
        return JSONResponse({'success': False}, status_code=401)
    try:
        data = await request.json()
        db = get_db()
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
            task.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
            db.commit()
        db.close()
        return JSONResponse({'success': True})
    except:
        return JSONResponse({'success': False})


if __name__ == '__main__':
    serve(port=5502)
