#!/usr/bin/env python3
"""
Admin User Management Tool
Create and manage administrator accounts for the Face Attendance System
"""

from model import Session, Admin
from werkzeug.security import generate_password_hash, check_password_hash
import getpass
import sys

def create_admin():
    """Create a new admin user"""
    print("\n" + "="*60)
    print("CREATE NEW ADMINISTRATOR")
    print("="*60 + "\n")
    
    # Get username
    while True:
        username = input("Enter username: ").strip()
        if not username:
            print("❌ Username cannot be empty!")
            continue
        if len(username) < 3:
            print("❌ Username must be at least 3 characters!")
            continue
        break
    
    # Check if username already exists
    db = Session()
    existing = db.query(Admin).filter_by(username=username).first()
    if existing:
        print(f"\n❌ Error: Username '{username}' already exists!")
        db.close()
        return False
    
    # Get password
    while True:
        password = getpass.getpass("Enter password: ")
        if not password:
            print("❌ Password cannot be empty!")
            continue
        if len(password) < 6:
            print("❌ Password must be at least 6 characters!")
            continue
        
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("❌ Passwords do not match!")
            continue
        break
    
    # Create admin
    try:
        hashed_password = generate_password_hash(password)
        new_admin = Admin(username=username, password=hashed_password)
        db.add(new_admin)
        db.commit()
        print(f"\n✅ Administrator '{username}' created successfully!")
        db.close()
        return True
    except Exception as e:
        print(f"\n❌ Error creating admin: {e}")
        db.rollback()
        db.close()
        return False

def list_admins():
    """List all admin users"""
    print("\n" + "="*60)
    print("ADMINISTRATOR ACCOUNTS")
    print("="*60 + "\n")
    
    db = Session()
    admins = db.query(Admin).all()
    
    if not admins:
        print("No administrators found.")
    else:
        print(f"{'ID':<5} {'Username':<20}")
        print("-" * 60)
        for admin in admins:
            print(f"{admin.id:<5} {admin.username:<20}")
        print(f"\nTotal: {len(admins)} administrator(s)")
    
    db.close()

def delete_admin():
    """Delete an admin user"""
    print("\n" + "="*60)
    print("DELETE ADMINISTRATOR")
    print("="*60 + "\n")
    
    db = Session()
    admins = db.query(Admin).all()
    
    if not admins:
        print("No administrators found.")
        db.close()
        return False
    
    # Show list
    print(f"{'ID':<5} {'Username':<20}")
    print("-" * 60)
    for admin in admins:
        print(f"{admin.id:<5} {admin.username:<20}")
    
    # Get admin to delete
    print()
    try:
        admin_id = int(input("Enter admin ID to delete (0 to cancel): "))
        if admin_id == 0:
            print("Cancelled.")
            db.close()
            return False
        
        admin = db.query(Admin).filter_by(id=admin_id).first()
        if not admin:
            print(f"❌ Admin with ID {admin_id} not found!")
            db.close()
            return False
        
        # Confirm deletion
        confirm = input(f"\n⚠️  Are you sure you want to delete '{admin.username}'? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Cancelled.")
            db.close()
            return False
        
        # Check if it's the last admin
        if len(admins) == 1:
            print("\n❌ Cannot delete the last administrator!")
            db.close()
            return False
        
        db.delete(admin)
        db.commit()
        print(f"\n✅ Administrator '{admin.username}' deleted successfully!")
        db.close()
        return True
        
    except ValueError:
        print("❌ Invalid input!")
        db.close()
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        db.close()
        return False

def change_password():
    """Change admin password"""
    print("\n" + "="*60)
    print("CHANGE ADMINISTRATOR PASSWORD")
    print("="*60 + "\n")
    
    db = Session()
    admins = db.query(Admin).all()
    
    if not admins:
        print("No administrators found.")
        db.close()
        return False
    
    # Show list
    print(f"{'ID':<5} {'Username':<20}")
    print("-" * 60)
    for admin in admins:
        print(f"{admin.id:<5} {admin.username:<20}")
    
    # Get admin
    print()
    try:
        admin_id = int(input("Enter admin ID (0 to cancel): "))
        if admin_id == 0:
            print("Cancelled.")
            db.close()
            return False
        
        admin = db.query(Admin).filter_by(id=admin_id).first()
        if not admin:
            print(f"❌ Admin with ID {admin_id} not found!")
            db.close()
            return False
        
        # Get new password
        while True:
            password = getpass.getpass("\nEnter new password: ")
            if not password:
                print("❌ Password cannot be empty!")
                continue
            if len(password) < 6:
                print("❌ Password must be at least 6 characters!")
                continue
            
            confirm = getpass.getpass("Confirm new password: ")
            if password != confirm:
                print("❌ Passwords do not match!")
                continue
            break
        
        admin.password = generate_password_hash(password)
        db.commit()
        print(f"\n✅ Password for '{admin.username}' changed successfully!")
        db.close()
        return True
        
    except ValueError:
        print("❌ Invalid input!")
        db.close()
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        db.close()
        return False

def main():
    """Main menu"""
    while True:
        print("\n" + "="*60)
        print("FACE ATTENDANCE SYSTEM - ADMIN MANAGEMENT")
        print("="*60)
        print("\n1. Create new administrator")
        print("2. List all administrators")
        print("3. Delete administrator")
        print("4. Change administrator password")
        print("5. Exit")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            create_admin()
        elif choice == '2':
            list_admins()
        elif choice == '3':
            delete_admin()
        elif choice == '4':
            change_password()
        elif choice == '5':
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice! Please enter 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
