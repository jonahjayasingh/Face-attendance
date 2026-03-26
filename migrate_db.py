"""
Migration script to update existing database to use foreign keys.
This will:
1. Backup existing data
2. Drop and recreate tables with foreign keys
3. Restore data with proper relationships
"""

from model import Session, StudentData, Attendance, Base, engine
from datetime import datetime
import os

def migrate_database():
    db = Session()
    
    print("Starting database migration...")
    
    # Step 1: Backup existing data
    print("Step 1: Backing up existing data...")
    try:
        old_students = db.query(StudentData).all()
        old_attendances = db.execute("SELECT * FROM attendances").fetchall()
        
        students_backup = [(s.registration_id, s.name, s.image) for s in old_students]
        # Old attendance has: id, Name, Date, Time
        attendances_backup = [(a[0], a[1], a[2], a[3]) for a in old_attendances]
        
        print(f"  - Backed up {len(students_backup)} students")
        print(f"  - Backed up {len(attendances_backup)} attendance records")
    except Exception as e:
        print(f"  - No existing data to backup or error: {e}")
        students_backup = []
        attendances_backup = []
    
    # Step 2: Drop and recreate tables
    print("Step 2: Recreating tables with foreign keys...")
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("  - Tables recreated successfully")
    except Exception as e:
        print(f"  - Error recreating tables: {e}")
        db.close()
        return False
    
    # Step 3: Restore students
    print("Step 3: Restoring student data...")
    student_map = {}  # Map old names to registration_ids
    for reg_id, name, image in students_backup:
        try:
            student = StudentData(registration_id=reg_id, name=name, image=image)
            db.add(student)
            student_map[name.upper()] = reg_id
        except Exception as e:
            print(f"  - Error restoring student {name}: {e}")
    
    try:
        db.commit()
        print(f"  - Restored {len(students_backup)} students")
    except Exception as e:
        print(f"  - Error committing students: {e}")
        db.rollback()
        db.close()
        return False
    
    # Step 4: Restore attendance with foreign keys
    print("Step 4: Restoring attendance data with foreign keys...")
    restored_count = 0
    skipped_count = 0
    
    for att_id, name, att_date, att_time in attendances_backup:
        name_upper = name.upper()
        if name_upper in student_map:
            try:
                attendance = Attendance(
                    student_id=student_map[name_upper],
                    Date=att_date,
                    Time=att_time
                )
                db.add(attendance)
                restored_count += 1
            except Exception as e:
                print(f"  - Error restoring attendance for {name}: {e}")
                skipped_count += 1
        else:
            print(f"  - Skipping attendance for unknown student: {name}")
            skipped_count += 1
    
    try:
        db.commit()
        print(f"  - Restored {restored_count} attendance records")
        if skipped_count > 0:
            print(f"  - Skipped {skipped_count} records (orphaned or errors)")
    except Exception as e:
        print(f"  - Error committing attendance: {e}")
        db.rollback()
        db.close()
        return False
    
    db.close()
    print("\n✓ Migration completed successfully!")
    print(f"  - Students: {len(students_backup)}")
    print(f"  - Attendance: {restored_count}/{len(attendances_backup)}")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MIGRATION TOOL")
    print("=" * 60)
    print("\nThis will update your database to use foreign key relationships.")
    print("Attendance records will now reference student IDs instead of names.")
    print("\nBenefits:")
    print("  - Updating a student's name will automatically update all attendance")
    print("  - Deleting a student will automatically delete their attendance")
    print("  - Attendance is only marked ONCE per day (no time updates)")
    print("\n" + "=" * 60)
    
    response = input("\nProceed with migration? (yes/no): ").strip().lower()
    if response == 'yes':
        migrate_database()
    else:
        print("Migration cancelled.")
