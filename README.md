# 📊 Gantt Chart Manager

A simple, fast Gantt chart application built with FastHTML (Python) and Frappe Gantt. Perfect for managing projects and tasks with a visual timeline.

## ✨ Features

- **Projects & Tasks**: Organize tasks under projects
- **Visual Timeline**: Interactive Gantt chart with Frappe Gantt
- **Quick Add Forms**: Fast data entry for projects and tasks
- **Drag & Drop**: Adjust task dates visually on the chart
- **Progress Tracking**: Monitor task completion percentage
- **SQLite Database**: Simple file-based database (easy to migrate to PostgreSQL)

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open your browser**
   Navigate to: `http://localhost:5001`

That's it! The app will automatically:
- Create the SQLite database (`gantt.db`)
- Set up the database tables
- Add sample data (optional)

## 📁 Project Structure

```
gantt-app/
├── main.py              # FastHTML application with routes and UI
├── database.py          # Database models and setup (SQLAlchemy)
├── requirements.txt     # Python dependencies
├── gantt.db            # SQLite database (created on first run)
└── README.md           # This file
```

## 🎯 Usage

### Adding a Project
1. Fill in the "Quick Add Project" form at the top
2. Click "Add Project"
3. Your project appears in the projects list

### Adding a Task
1. Select a project from the dropdown
2. Enter task details (name, dates, progress)
3. Click "Add Task"
4. The task appears in the Gantt chart and task list

### Deleting Items
- Use the "Delete" button next to any project or task
- Deleting a project removes all its tasks

### Viewing the Gantt Chart
- All tasks are displayed visually with their durations
- Click on any task bar to see details in a popup
- The chart automatically updates when you add/delete tasks

## 🔧 Customization

### Change the Port
Edit `main.py`, find the last line and modify:
```python
serve(port=5001)  # Change to your preferred port
```

### Modify Database Location
Edit `database.py`, change the `DATABASE_URL`:
```python
DATABASE_URL = "sqlite:///./gantt.db"  # Change path as needed
```

### Adjust Gantt View Mode
In `main.py`, find the Gantt initialization and change `view_mode`:
```javascript
view_mode: 'Week',  // Options: 'Day', 'Week', 'Month', 'Year'
```

## 🌐 Deploying to Digital Ocean

### Option 1: Digital Ocean App Platform (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create a new App in Digital Ocean**
   - Go to [Digital Ocean App Platform](https://cloud.digitalocean.com/apps)
   - Click "Create App"
   - Select your GitHub repository
   - Digital Ocean will auto-detect the Python app

3. **Configure the app**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python main.py`
   - HTTP Port: `5001` (or your custom port)

4. **Add environment variables** (if needed)
   - You can add production settings later

5. **Deploy!**
   - Click "Deploy" and wait for the build

### Option 2: Droplet (VPS)

1. **SSH into your droplet**
   ```bash
   ssh root@your-droplet-ip
   ```

2. **Install Python and dependencies**
   ```bash
   apt update
   apt install python3 python3-pip git
   ```

3. **Clone your repository**
   ```bash
   git clone <your-repo-url>
   cd gantt-app
   ```

4. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run with a process manager (recommended)**
   ```bash
   # Install supervisor or systemd service
   # Example with nohup (simple but not recommended for production):
   nohup python3 main.py &
   ```

### Migrating to PostgreSQL (for production)

When you're ready to use PostgreSQL on Digital Ocean:

1. **Install psycopg2**
   ```bash
   pip install psycopg2-binary
   ```

2. **Update `database.py`**
   ```python
   DATABASE_URL = "postgresql://user:password@host:5432/dbname"
   ```

3. **That's it!** SQLAlchemy handles the rest.

## 📝 License & Data Privacy

### Application Code
- **Frappe Gantt**: MIT License (you can use it anywhere, including commercial projects)
- **Your Code**: If you make this project public on GitHub, add a license (MIT recommended)

### Your Data
- ✅ **Your data is private** - only your application code needs to be public
- ✅ The SQLite database (`gantt.db`) stays on your server
- ✅ User data, projects, and tasks are NOT shared publicly
- ✅ Add `gantt.db` to `.gitignore` to keep it out of version control

### What to Make Public (for free use)
- ✅ Source code (`main.py`, `database.py`, etc.)
- ✅ README and documentation
- ❌ **NOT** your database file
- ❌ **NOT** your production environment variables
- ❌ **NOT** your user data

## 🛠 Troubleshooting

### Database Errors
- Delete `gantt.db` and restart the app to recreate fresh database

### Port Already in Use
- Change the port in `main.py` or stop the other application using port 5001

### Dependencies Not Installing
- Make sure you have Python 3.10+: `python --version`
- Try: `pip install --upgrade pip` then reinstall requirements

### Gantt Chart Not Showing
- Check browser console for JavaScript errors
- Ensure tasks have valid start/end dates
- Verify Frappe Gantt CDN is accessible

## 🎨 Next Steps

Want to enhance this app? Consider adding:
- [ ] Task dependencies (task A must finish before task B)
- [ ] User authentication
- [ ] Task editing (not just delete)
- [ ] Export to PDF/CSV
- [ ] Task assignment to team members
- [ ] Dark mode
- [ ] Calendar view
- [ ] Email notifications

## 💡 Tips

- Start with a few test projects to familiarize yourself
- The Gantt chart works best with 5-20 tasks visible at once
- Use meaningful project and task names for clarity
- Keep task durations realistic for better visualization
- Progress percentages help track project status at a glance

## 🤝 Contributing

This is your project! Feel free to:
- Modify the code to suit your needs
- Share improvements on GitHub
- Fork and customize for your specific use case

## 📧 Support

For FastHTML documentation: https://docs.fastht.ml/
For Frappe Gantt documentation: https://frappe.io/gantt

---

Built with ❤️ using FastHTML and Frappe Gantt
