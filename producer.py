import csv
import os
import time
import argparse

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

def get_next_id():
    if not os.path.exists(TASKS_FILE):
        return 1
    
    with open(TASKS_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        if not data:
            return 1
        
        try:
            headers = data[0]
            if not headers[0].isdigit():
                if len(data) == 1:
                    return 1
                last_row = data[-1]
                return int(last_row[0]) + 1
            else:
                last_row = data[-1]
                return int(last_row[0]) + 1
        except (IndexError, ValueError):
            return 1

def produce_tasks(count):
    acquire_lock()
    try:
        file_exists = os.path.exists(TASKS_FILE)
        next_id = get_next_id()
        
        new_tasks = []
        for i in range(count):
            task_id = next_id + i
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            new_tasks.append([task_id, 'pending', timestamp, timestamp])
        
        with open(TASKS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['id', 'status', 'created_at', 'modified_at'])
            
            writer.writerows(new_tasks)
            
        print(f"Added {count} tasks staring from ID {next_id}.")
        
    finally:
        release_lock()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Produce tasks for the queue.")
    parser.add_argument("--count", type=int, default=1, help="Number of tasks to produce")
    args = parser.parse_args()
    
    produce_tasks(args.count)
