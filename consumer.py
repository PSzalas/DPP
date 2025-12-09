import csv
import os
import time
from datetime import datetime

base_path = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(base_path, "tasks.csv")
LOCK_FILE = os.path.join(base_path, "tasks.lock")

def acquire_lock():
    while True:
        try:
            fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(fd)
            return
        except FileExistsError:
            time.sleep(0.1)

def release_lock():
    try:
        os.remove(LOCK_FILE)
    except FileNotFoundError:
        pass

def read_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', newline='', encoding='utf-8') as f:
        return list(csv.reader(f))

def write_tasks(rows):
    with open(TASKS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def process_tasks():
    print("Consumer started. Press Ctrl+C to stop.")
    while True:
        task_found = None
        
        acquire_lock()
        try:
            rows = read_tasks()
            header = []
            data = rows
            if rows and len(rows) > 0 and not rows[0][0].isdigit():
                header = rows[0]
                data = rows[1:]

            now = datetime.now()
            for i, row in enumerate(data):
                if len(row) < 4: 
                    continue
                
                status = row[1]
                last_mod_str = row[3]
                
                should_pick = False
                
                seconds_elapsed = 0
                try:
                    last_mod_time = datetime.strptime(last_mod_str, "%Y-%m-%d %H:%M:%S")
                    seconds_elapsed = (now - last_mod_time).total_seconds()
                except ValueError:
                    seconds_elapsed = 999999

                if status == 'pending':
                    should_pick = True
                elif status == 'in_progress':
                    if seconds_elapsed > 45:
                        print(f"Found stalled task {row[0]} (last update: {seconds_elapsed:.1f}s ago)")
                        should_pick = True
                
                if should_pick:
                    row[1] = 'in_progress'
                    row[3] = now.strftime("%Y-%m-%d %H:%M:%S")
                    
                    task_found = row
                    print(f"task {row[0]} -> in_progress")
                    break
            
            if task_found:
                all_rows = [header] + data if header else data
                write_tasks(all_rows)
        finally:
            release_lock()

        if task_found:
            print(f"Processing task {task_found[0]} (30s)...")
            time.sleep(30)
            
            acquire_lock()
            try:
                rows = read_tasks()
                header = []
                data = rows
                if rows and len(rows) > 0 and not rows[0][0].isdigit():
                    header = rows[0]
                    data = rows[1:]
                
                for row in data:
                    if row[0] == task_found[0]:
                        row[1] = 'done'
                        if len(row) >= 4:
                            row[3] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"task {row[0]} -> done")
                        break
                
                all_rows = [header] + data if header else data
                write_tasks(all_rows)
            finally:
                release_lock()
                
        else:
            print("No pending tasks found. Sleeping 5s...")
            time.sleep(5)

if __name__ == "__main__":
    process_tasks()
