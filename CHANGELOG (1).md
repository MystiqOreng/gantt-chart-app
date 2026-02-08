# Changelog

## Version 2.1 - Interactive Enhancements (2025-02-08)

### ✨ New Features

**Interactive Gantt Chart:**
- 🖱️ **Drag and drop** task bars to change start/end dates
- 📏 **Resize** task bars to adjust duration
- 📊 **Interactive progress** - adjust progress on the chart
- ✅ **Real-time updates** - changes sync to database immediately
- ⚠️ **Date validation** - prevents end date before start date

**Enhanced Task Management:**
- ✏️ **Edit button** - Edit task dates inline with validation
- ✅ **Done button** - Mark tasks as complete (replaces delete for active tasks)
- 🔔 **Audio notification** - Pleasant "ding" sound when marking tasks done
- 🗑️ **Remove button** - Permanently delete completed tasks only
- 👁️ **Visual feedback** - Completed tasks shown with strikethrough and gray styling

**Improved Workflow:**
- Tasks can be edited directly from the task list
- Gantt chart bars are now fully interactive
- Date validation prevents invalid date ranges
- Completed tasks are visually distinct but still visible

### 🛠 Technical Changes

**Database:**
- Added `completed` field to Task model (0 = active, 1 = done)
- Migration script updated to add completed field
- Progress auto-sets to 100% when marking task done

**New API Endpoints:**
- `/tasks/{id}/update-dates` - AJAX endpoint for Gantt drag/drop
- `/tasks/{id}/update-progress` - AJAX endpoint for progress changes
- `/tasks/{id}/update` - Form endpoint for edit functionality
- `/tasks/{id}/complete` - Mark task as done

**UI/UX:**
- Web Audio API for completion sound
- Inline edit forms with toggle functionality
- Client-side date validation with error messages
- Improved button styling and layout
- Completed task styling (strikethrough, grayed out)

---

## Version 2.0.1 - Bugfix (2025-02-08)

### 🐛 Bug Fixes
- Fixed SQLAlchemy `DetachedInstanceError` when displaying project task counts
- Database session now properly managed to prevent lazy-loading errors

---

## Version 2.0 - Layout Redesign (2025-02-08)

### 🎨 Major UI/UX Improvements

**New Project-Focused Workflow:**
- ✨ **Project selector at the top** - Select which project to work on from a dropdown
- 📊 **Filtered Gantt chart** - Shows only tasks for the selected project
- ⚡ **Smart task form** - Automatically uses the selected project (no more dropdown in task form)
- 🔄 **Seamless switching** - Change projects instantly with the dropdown

**Enhanced Task Management:**
- 📝 **Task descriptions** - Add detailed descriptions to tasks
- 👀 **Better visibility** - Descriptions shown in both Gantt popup and task list
- 💬 **Contextual information** - Understand what each task involves at a glance

**Reorganized Layout:**
- 🔝 **Top:** Project selector
- 📅 **Middle:** Gantt chart + Task form + Task list (all for selected project)
- ⚙️ **Bottom:** Project management (create/delete projects)
- 🎯 **Focus:** Work on one project at a time without distraction

### 🛠 Technical Changes

**Database:**
- Added `description` field to Task model
- Migration script (`migrate.py`) for existing databases
- Sample data includes task descriptions

**Routing:**
- GET parameter `?project_id=X` to maintain project selection
- Redirects preserve selected project after add/delete operations
- Auto-select first project if none specified

**UI/Styling:**
- New `.task-description` CSS class
- Enhanced Gantt popup with description display
- Improved project selector styling
- Visual separation between work area and project management

### 📦 New Files

- `migrate.py` - Database migration script for existing users
- `CHANGELOG.md` - This file

### 🔧 Modified Files

- `database.py` - Added description field to Task model
- `main.py` - Complete layout reorganization, new routing logic
- `README.md` - Updated usage instructions and features
- `PROJECT_SUMMARY.txt` - Updated feature list

---

## Version 1.0 - Initial Release

### Features

- Projects and Tasks management
- Interactive Gantt chart with Frappe Gantt
- Quick-add forms
- SQLite database
- FastHTML + Python backend
- Clean, modern UI

