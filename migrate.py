"""
Migration script to add description and completed fields to existing tasks.

Run this if you already have a gantt.db database from the previous version.
"""

import sqlite3

def migrate_database():
    """Add description and completed columns to tasks table if they don't exist."""
    try:
        conn = sqlite3.connect('gantt.db')
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [column[1] for column in cursor.fetchall()]
        
        changes_made = False
        
        if 'description' not in columns:
            print("Adding 'description' column to tasks table...")
            cursor.execute("ALTER TABLE tasks ADD COLUMN description VARCHAR(500)")
            changes_made = True
            print("✅ Description field added.")
        
        if 'completed' not in columns:
            print("Adding 'completed' column to tasks table...")
            cursor.execute("ALTER TABLE tasks ADD COLUMN completed INTEGER DEFAULT 0")
            changes_made = True
            print("✅ Completed field added.")
        
        if changes_made:
            conn.commit()
            print("✅ Migration successful!")
        else:
            print("✅ Database already up to date. No migration needed.")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Error during migration: {e}")
        return False
    
    return True


if __name__ == '__main__':
    print("🔄 Running database migration...")
    if migrate_database():
        print("🎉 Database is up to date!")
    else:
        print("⚠️  Migration failed. You may need to recreate the database.")
        print("    To start fresh, delete gantt.db and run: python main.py")
