"""FastHTML Gantt Chart Application with CRUD functionality."""

from fasthtml.common import *
from datetime import datetime
from database_old import init_db, get_db, Project, Task, seed_sample_data

# Initialize database
init_db()
seed_sample_data()

# FastHTML app with custom headers for Frappe Gantt
app, rt = fast_app(
    hdrs=(
        Script(src="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js"),
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.css"),
        Style("""
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 { color: #333; margin-bottom: 10px; }
            .subtitle { color: #666; margin-bottom: 30px; }
            .section { margin-bottom: 40px; }
            .section-title { 
                font-size: 18px; 
                font-weight: 600; 
                margin-bottom: 15px;
                color: #444;
            }
            .quick-add-form {
                background: #f9f9f9;
                padding: 20px;
                border-radius: 6px;
                margin-bottom: 20px;
            }
            .form-row {
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
                flex-wrap: wrap;
            }
            .form-group {
                flex: 1;
                min-width: 200px;
            }
            label {
                display: block;
                font-size: 13px;
                font-weight: 500;
                margin-bottom: 5px;
                color: #555;
            }
            input, select, textarea {
                width: 100%;
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }
            textarea {
                resize: vertical;
                min-height: 60px;
            }
            button {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
            }
            button:hover {
                background: #45a049;
            }
            .delete-btn {
                background: #f44336;
                padding: 5px 10px;
                font-size: 12px;
            }
            .delete-btn:hover {
                background: #da190b;
            }
            .project-list {
                list-style: none;
                padding: 0;
            }
            .project-item {
                background: white;
                border: 1px solid #e0e0e0;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 4px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .project-info h3 {
                margin: 0 0 5px 0;
                font-size: 16px;
                color: #333;
            }
            .project-info p {
                margin: 0;
                font-size: 13px;
                color: #666;
            }
            #gantt-container {
                background: white;
                padding: 20px;
                border-radius: 6px;
                overflow-x: auto;
                margin-bottom: 20px;
            }
            .gantt {
                overflow: visible !important;
            }
            .task-list {
                margin-top: 20px;
            }
            .task-item {
                background: #fafafa;
                border-left: 4px solid #4CAF50;
                padding: 12px;
                margin-bottom: 8px;
                border-radius: 4px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .task-info {
                flex: 1;
            }
            .task-name {
                font-weight: 500;
                color: #333;
                margin-bottom: 4px;
            }
            .task-description {
                font-size: 13px;
                color: #666;
                margin-bottom: 6px;
                font-style: italic;
            }
            .task-dates {
                font-size: 12px;
                color: #888;
            }
            .progress-bar {
                width: 100px;
                height: 20px;
                background: #e0e0e0;
                border-radius: 10px;
                overflow: hidden;
                margin: 0 15px;
            }
            .progress-fill {
                height: 100%;
                background: #4CAF50;
                transition: width 0.3s;
            }
        """)
    )
)


@rt('/')
def get(project_id: int = None):
    """Main page with project-focused view."""
    db = get_db()
    projects = db.query(Project).all()
    
    # Select first project by default if none specified
    if not project_id and projects:
        project_id = projects[0].id
    
    # Get tasks for selected project only
    selected_tasks = []
    selected_project = None
    if project_id:
        selected_project = db.query(Project).filter(Project.id == project_id).first()
        if selected_project:
            selected_tasks = db.query(Task).filter(Task.project_id == project_id).all()
    
    # Load task counts for all projects BEFORE closing the session
    project_data = []
    for p in projects:
        task_count = len(p.tasks)  # Access while session is still open
        project_data.append({
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'task_count': task_count
        })
    
    db.close()
    
    return Title("Gantt Chart Manager"), Main(
        Div(
            H1("📊 Gantt Chart Manager"),
            P("Manage your projects and tasks with visual timeline", cls="subtitle"),
            
            # Project Selector at Top
            Div(
                Div("📁 Select Project", cls="section-title"),
                Form(
                    Div(
                        Select(
                            *[Option(
                                p['name'], 
                                value=p['id'], 
                                selected=(p['id'] == project_id)
                            ) for p in project_data],
                            name="project_id",
                            id="project-selector",
                            onchange="this.form.submit()",
                            style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #4CAF50; border-radius: 6px;"
                        ) if project_data else P("No projects yet. Create one below!", style="color: #999; padding: 10px;"),
                        cls="form-group"
                    ),
                    method="get",
                    action="/",
                    style="margin-bottom: 0;"
                ),
                cls="section"
            ) if project_data else "",
            
            # Gantt Chart for Selected Project
            Div(
                Div(f"📅 Timeline - {selected_project.name if selected_project else 'No Project Selected'}", cls="section-title"),
                Div(id="gantt-container") if selected_tasks else P(
                    "No tasks in this project yet. Add some below!" if selected_project else "Select or create a project to get started.", 
                    style="color: #999; padding: 20px;"
                ),
                
                # Gantt initialization script
                Script(f"""
                    const tasks = {[task.to_dict() for task in selected_tasks]};
                    
                    if (tasks.length > 0) {{
                        const gantt = new Gantt("#gantt-container", tasks, {{
                            view_mode: 'Week',
                            bar_height: 30,
                            bar_corner_radius: 3,
                            arrow_curve: 5,
                            padding: 18,
                            date_format: 'YYYY-MM-DD',
                            language: 'en',
                            custom_popup_html: function(task) {{
                                const description = task.description || 'No description';
                                return `
                                    <div style="padding: 12px; min-width: 200px;">
                                        <h5 style="margin: 0 0 8px 0; color: #333;">${{task.name}}</h5>
                                        <p style="margin: 0 0 6px 0; font-size: 12px; color: #666;">${{description}}</p>
                                        <p style="margin: 0; font-size: 13px;"><strong>Progress:</strong> ${{task.progress}}%</p>
                                        <p style="margin: 4px 0 0 0; font-size: 12px; color: #888;">${{task.start}} → ${{task.end}}</p>
                                    </div>
                                `;
                            }}
                        }});
                    }}
                """) if selected_tasks else "",
                cls="section"
            ) if project_data else "",
            
            # Quick Add Task Form (for selected project)
            Div(
                Div("➕ Quick Add Task" + (f" to {selected_project.name}" if selected_project else ""), cls="section-title"),
                Form(
                    Input(type="hidden", name="project_id", value=str(project_id) if project_id else ""),
                    Div(
                        Div(
                            Label("Task Name *"),
                            Input(name="name", placeholder="e.g., Design mockups", required=True),
                            cls="form-group"
                        ),
                        cls="form-row"
                    ),
                    Div(
                        Div(
                            Label("Description"),
                            Textarea(name="description", placeholder="What needs to be done?", rows="2"),
                            cls="form-group"
                        ),
                        cls="form-row"
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
                        cls="form-row"
                    ),
                    Button("Add Task", type="submit"),
                    method="post",
                    action="/tasks/add",
                    cls="quick-add-form"
                ) if selected_project else P("Select or create a project first.", style="color: #999; padding: 10px;"),
                cls="section"
            ) if project_data else "",
            
            # Task List for Selected Project
            Div(
                Div(f"📋 Tasks in {selected_project.name if selected_project else 'Project'}", cls="section-title"),
                Div(
                    *[Div(
                        Div(
                            Div(task.name, cls="task-name"),
                            Div(task.description or "No description", cls="task-description"),
                            Div(f"{task.start_date.strftime('%Y-%m-%d')} → {task.end_date.strftime('%Y-%m-%d')}", cls="task-dates"),
                            cls="task-info"
                        ),
                        Div(
                            Div(style=f"width: {task.progress}%", cls="progress-fill"),
                            cls="progress-bar",
                            title=f"{task.progress}%"
                        ),
                        Form(
                            Button("Delete", cls="delete-btn", type="submit"),
                            method="post",
                            action=f"/tasks/{task.id}/delete?project_id={project_id}",
                            onsubmit="return confirm('Delete this task?')"
                        ),
                        cls="task-item"
                    ) for task in selected_tasks],
                    cls="task-list"
                ) if selected_tasks else P("No tasks yet. Add one above!", style="color: #999; padding: 10px;"),
                cls="section"
            ) if selected_project else "",
            
            # Divider
            Hr(style="margin: 40px 0; border: none; border-top: 2px solid #e0e0e0;") if project_data else "",
            
            # Project Management Section (moved to bottom)
            Div(
                Div("⚙️ Manage Projects", cls="section-title"),
                
                # Quick Add Project Form
                Div(
                    Div("➕ Create New Project", style="font-size: 15px; font-weight: 500; margin-bottom: 10px; color: #555;"),
                    Form(
                        Div(
                            Div(
                                Label("Project Name *"),
                                Input(name="name", placeholder="e.g., Website Redesign", required=True),
                                cls="form-group"
                            ),
                            Div(
                                Label("Description (optional)"),
                                Textarea(name="description", placeholder="Brief description of the project", rows="2"),
                                cls="form-group"
                            ),
                            cls="form-row"
                        ),
                        Button("Create Project", type="submit"),
                        method="post",
                        action="/projects/add",
                        cls="quick-add-form"
                    ),
                    style="margin-bottom: 30px;"
                ),
                
                # Projects List
                Div(
                    Div("📂 All Projects", style="font-size: 15px; font-weight: 500; margin-bottom: 10px; color: #555;"),
                    Ul(
                        *[Li(
                            Div(
                                H3(p['name']),
                                P(p['description'] or "No description"),
                                P(f"{p['task_count']} task{'s' if p['task_count'] != 1 else ''}", 
                                  style="font-size: 12px; color: #888; margin-top: 5px;"),
                                cls="project-info"
                            ),
                            Form(
                                Button("Delete", cls="delete-btn", type="submit"),
                                method="post",
                                action=f"/projects/{p['id']}/delete",
                                onsubmit="return confirm('Delete this project and all its tasks?')"
                            ),
                            cls="project-item"
                        ) for p in project_data],
                        cls="project-list"
                    ) if project_data else P("No projects yet.", style="color: #999; padding: 10px;"),
                ),
                cls="section",
                style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin-top: 20px;"
            ),
            
            cls="container"
        )
    )


@rt('/projects/add')
def post(name: str, description: str = ""):
    """Add a new project."""
    db = get_db()
    project = Project(name=name, description=description)
    db.add(project)
    db.commit()
    db.close()
    return RedirectResponse('/', status_code=303)


@rt('/projects/{project_id}/delete')
def post(project_id: int):
    """Delete a project and all its tasks."""
    db = get_db()
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
    db.close()
    return RedirectResponse('/', status_code=303)


@rt('/tasks/add')
def post(project_id: int, name: str, start_date: str, end_date: str, progress: int = 0, description: str = ""):
    """Add a new task."""
    db = get_db()
    task = Task(
        project_id=project_id,
        name=name,
        description=description,
        start_date=datetime.strptime(start_date, '%Y-%m-%d'),
        end_date=datetime.strptime(end_date, '%Y-%m-%d'),
        progress=progress
    )
    db.add(task)
    db.commit()
    db.close()
    return RedirectResponse(f'/?project_id={project_id}', status_code=303)


@rt('/tasks/{task_id}/delete')
def post(task_id: int, project_id: int = None):
    """Delete a task."""
    db = get_db()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        if not project_id:
            project_id = task.project_id
        db.delete(task)
        db.commit()
    db.close()
    return RedirectResponse(f'/?project_id={project_id}' if project_id else '/', status_code=303)


if __name__ == '__main__':
    serve(port=5501)
