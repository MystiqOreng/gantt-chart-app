# 🎯 Features Guide - Version 2.1

## Interactive Gantt Chart

### Drag and Drop Tasks
1. **Move a task**: Click and drag any task bar left or right to change dates
2. **Resize a task**: Drag the left or right edge of a task bar to adjust start/end dates
3. **Auto-save**: Changes save automatically to the database
4. **Validation**: If you set an invalid date (end before start), you'll get an error

### Adjust Progress
- Some Gantt chart libraries support dragging progress - check if yours does!
- Progress can also be set when creating/editing tasks

## Task Management

### Edit Task Dates
1. Click the **"Edit"** button next to any task
2. A form appears with current start and end dates
3. Change the dates
4. Click **"Save Changes"**
5. ⚠️ You'll get an error if end date is before start date

### Mark Tasks as Done
1. Click the **"✓ Done"** button next to any task
2. 🔔 You'll hear a pleasant "ding" sound
3. The task gets marked complete (strikethrough, grayed out)
4. Progress automatically sets to 100%
5. The task still shows in your list but looks different

### Remove Completed Tasks
- Completed tasks show a **"Remove"** button
- This permanently deletes the task from the database
- Active tasks don't have this button - you must mark them done first

## Tips & Tricks

### Best Practices
- ✅ Use the Gantt chart for quick date adjustments (drag and drop)
- ✅ Use the Edit button for precise date entry
- ✅ Mark tasks "Done" instead of deleting them (keeps history)
- ✅ Only remove tasks you really don't need anymore

### Keyboard Shortcuts
- The date picker supports keyboard navigation
- Tab through form fields
- Enter to submit forms

### Visual Feedback
- **Active tasks**: Normal styling, green progress bar
- **Completed tasks**: Strikethrough text, gray, "✓ Completed" badge
- **Edit mode**: Yellow background on edit form

## Workflow Example

1. **Create a new task** - Use the Quick Add form
2. **Adjust on timeline** - Drag the task bar to the right dates
3. **Work on it** - Update progress as you go
4. **Mark done** - Click "✓ Done" when finished (hear the ding!)
5. **Review later** - Completed tasks stay visible but grayed out
6. **Clean up** - Remove old completed tasks you don't need

## Audio Notification

The "ding" sound when completing tasks:
- Uses Web Audio API (works in all modern browsers)
- Pleasant, non-intrusive tone
- Gives instant feedback that your action succeeded
- No external files needed - generated in the browser

## Date Validation

**Client-side (instant feedback):**
- Shows error message immediately when you enter invalid dates
- Prevents form submission until fixed

**Server-side (backup):**
- Double-checks dates before saving
- Returns error if validation fails

## Troubleshooting

### Gantt chart not updating after drag?
- Check browser console for errors
- Make sure you have internet connection (for saving)
- Try refreshing the page

### Edit form won't open?
- Make sure JavaScript is enabled
- Try refreshing the page
- Check for browser console errors

### No sound when clicking Done?
- Some browsers block audio until user interaction
- Make sure your device volume is on
- Try clicking Done a second time

### Date validation not working?
- Make sure JavaScript is enabled
- Try typing dates instead of using the picker
- Check that dates are in YYYY-MM-DD format

## Feature Comparison

| Feature | Before v2.1 | After v2.1 |
|---------|------------|------------|
| Edit dates | ❌ Delete & recreate | ✅ Edit button or drag |
| Complete tasks | ❌ Just delete | ✅ Mark done with sound |
| Gantt interaction | 👁️ View only | 🖱️ Fully interactive |
| Date validation | ❌ No checks | ✅ Client + server |
| Task history | ❌ Deleted = gone | ✅ Completed = kept |

---

**Enjoy the new features!** 🎉

For more details, see the main README.md or CHANGELOG.md
