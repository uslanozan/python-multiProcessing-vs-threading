import os
from threading import Thread
import time
import psutil


# This function merges a txt and images that belong to txt
def merge_files(txt_file, img_files, output_file, merge_times, merge_cpu_usages, merge_memory_usages, index):
    process = psutil.Process(os.getpid())
    start_time = time.time()

    with open(txt_file, 'r') as txt:
        txt_content = txt.read()

    # Create the output folder (if not exists)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'wb') as output:
        output.write(txt_content.encode('utf-8'))

        for img_file in img_files:
            with open(img_file, 'rb') as img:
                img_content = img.read()
                output.write(img_content)
                output.write(b'\n')

    end_time = time.time()
    merge_times[index] = end_time - start_time
    merge_cpu_usages[index] = process.cpu_percent()
    merge_memory_usages[index] = process.memory_info().rss / (1024 * 1024)  # Convert to MB


# It counts every 'a' and 'A' in merged txt
def count_a_in_txt(txt_file, count_times, count_cpu_usages, count_memory_usages, index):
    process = psutil.Process(os.getpid())
    start_time = time.time()

    try:
        with open(txt_file, 'rb') as file:
            content = file.read().decode(errors='ignore')
        content_lower = content.lower()
        a_count = content_lower.count('a')
        print(f"The number of 'a' characters in {txt_file} is: {a_count}")
    except FileNotFoundError:
        print(f"The file {txt_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    end_time = time.time()
    count_times[index] = end_time - start_time
    count_cpu_usages[index] = process.cpu_percent()
    count_memory_usages[index] = process.memory_info().rss / (1024 * 1024)  # Convert to MB


# It doesn't necessary right now (if __name__ ...)
if __name__ == "__main__":
    print("--MERGING TXT AND JPGs WITH THREADING (SCENARIO 2)--")
    # File directories
    txt_files_dir = "TargetFiles/txt"
    img_files_dir = "TargetFiles/jpg"
    output_files_dir = "Outputs/OutputsFromThreading"

    # Get the start time before the process
    start_time = time.time()

    # List all txt files in the directory
    txt_files = [f for f in os.listdir(txt_files_dir) if f.endswith('.txt')]

    threads = []
    merged_files = []

    # Initialize lists for performance metrics
    merge_times = [0] * len(txt_files)
    merge_cpu_usages = [0] * len(txt_files)
    merge_memory_usages = [0] * len(txt_files)
    count_times = [0] * len(txt_files)
    count_cpu_usages = [0] * len(txt_files)
    count_memory_usages = [0] * len(txt_files)

    for index, txt_file in enumerate(txt_files):
        base_name = os.path.splitext(txt_file)[0]

        # Find all matching image files
        img_files = [os.path.join(img_files_dir, f) for f in os.listdir(img_files_dir) if
                     f.startswith(base_name) and f.endswith('.jpg')]

        if img_files:
            txt_file_path = os.path.join(txt_files_dir, txt_file)
            output_file_path = os.path.join(output_files_dir, f"{base_name}_merged.txt")
            t = Thread(target=merge_files, args=(
                txt_file_path, img_files, output_file_path, merge_times, merge_cpu_usages, merge_memory_usages, index))
            merged_files.append(output_file_path)
            threads.append(t)
            t.start()

    # Wait for all merge threads to complete
    for t in threads:
        t.join()

    threads = []  # Clear the thread list for count threads

    # Counting 'a's in merged files
    for index, merged_file in enumerate(merged_files):
        time.sleep(1)  # To see time clearly
        t = Thread(target=count_a_in_txt, args=(merged_file, count_times, count_cpu_usages, count_memory_usages, index))
        threads.append(t)
        t.start()

    # Wait for all count threads to complete
    for t in threads:
        t.join()

    # Get the end time after the process
    end_time = time.time()

    # Calculate the total time taken
    total_time = end_time - start_time

    # Calculate and print performance metrics for merge and count operations
    total_merge_time = sum(merge_times)
    avg_merge_cpu_usage = sum(merge_cpu_usages) / len(merge_cpu_usages)
    total_merge_memory_usage = sum(merge_memory_usages)

    total_count_time = sum(count_times)
    avg_count_cpu_usage = sum(count_cpu_usages) / len(count_cpu_usages)
    total_count_memory_usage = sum(count_memory_usages)

    print("-" * 40)
    print("All files merged and new files created in:", output_files_dir)
    print("\nTotal time:", total_time, "seconds")

    print("\nMerge Operation Performance Metrics:")
    print(f"Total merge time: {total_merge_time:.2f} seconds")
    print(f"Average merge CPU usage: {avg_merge_cpu_usage:.2f}%")
    print(f"Total merge memory usage: {total_merge_memory_usage:.2f} MB")

    print("\nCount Operation Performance Metrics:")
    print(f"Total count time: {total_count_time:.2f} seconds")
    print(f"Average count CPU usage: {avg_count_cpu_usage:.2f}%")
    print(f"Total count memory usage: {total_count_memory_usage:.2f} MB")
