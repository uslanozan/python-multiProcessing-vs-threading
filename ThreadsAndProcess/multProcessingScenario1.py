import multiprocessing
import requests
import os
import time
import psutil


# This function downloads jpgs from urls
def download_file(url, counter, directory, times, cpu_usages, memory_usages):
    start_time = time.time()  # To calculate time
    process = psutil.Process(os.getpid())
    response = requests.get(url, allow_redirects=True)

    file_name = f"Image{counter}.jpg"
    file_path = os.path.join(directory, file_name)

    # "200" means successful for response code
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Error occurred while downloading Image {counter}.")

    end_time = time.time()
    times[counter - 1] = end_time - start_time

    # Store CPU and memory usage
    cpu_usages[counter - 1] = process.cpu_percent()
    memory_info = process.memory_info()
    memory_usages[counter - 1] = memory_info.rss / (1024 * 1024)  # Convert to MB


# Downloading path to separate multiProcessing and Threading directories
download_directory = "Images/ImageFromMultiprocessing"

# Create directory if it doesn't exist
os.makedirs(download_directory, exist_ok=True)

# URLs list
urls = [
    'https://astonmartin.com.tr/uploads/2023/4/jpg-small-key-visual-background-dbs-770-ultimate-imagery-productkey-visual-background-dbs-770-ultimate-imagery-product-1-2023-04-06-103038.jpg',
    'https://astonmartin.com.tr/uploads/2023/4/jpg-small-key-visual-background-dbs-770-ultimate-imagery-product-2-2023-04-06-111036.jpg',
    'https://www.bentleymotors.com/content/dam/bm/websites/bmcom/bentleymotors-com/models/24my/continental-gt/continental-gt-speed/Performance%20Gallery%20Slide%203.jpg/_jcr_content/renditions/original.image_file.1074.604.file/Performance%20Gallery%20Slide%203.jpg',
    'https://www.bentleymotors.com/content/dam/bm/websites/bmcom/bentleymotors-com/models/24my/continental-gt/continental-gt-speed/GT-Speed-Gallery-Media-5-16x9.jpg/_jcr_content/renditions/original.image_file.1074.604.file/GT-Speed-Gallery-Media-5-16x9.jpg',
    'https://www.audi.com.tr/content/dam/nemo/models/a6/rs-6-avant-performance/my-2023/feature-gallery/RS_6_2022_4345-L.jpg?imwidth=1920&imdensity=1',
    'https://www.audi.com.tr/content/dam/nemo/models/a6/rs-6-avant-performance/my-2023/feature-gallery/RS_6_2022_4373-L.jpg?imwidth=1920&imdensity=1',
    'https://www.lamborghini.com/sites/it-en/files/DAM/lamborghini/facelift_2019/model_detail/huracan/sterrato/s/2023/ex2.jpg',
    'https://www.lamborghini.com/sites/it-en/files/DAM/lamborghini/facelift_2019/model_detail/huracan/sterrato/gallery/2023/ext_1_1.jpg',
    'https://www.mercedes-benz.com.tr/content/turkey/tr/passengercars/models/coupe/new/amg-gt/_jcr_content/root/responsivegrid/media_slider/media_slider_item_531012189/image.component.damq6.3384590700859.jpg/mercedes-amg-gt-c192-pad-higlights-exterior-3302x1858-06-2023.jpg',
    'https://www.mercedes-benz.com.tr/content/turkey/tr/passengercars/models/coupe/new/amg-gt/_jcr_content/root/responsivegrid/media_gallery_copy_c/media_gallery_item_937733884/image.component.damq6.3384594893189.jpg/mercedes-amg-gt-c192-pad-exterior-gt63-front-2176x1224-06-2023.jpg'
]

# It doesn't necessary right now (if __name__ ...)
if __name__ == '__main__':
    print("--IMAGE DOWNLOADING WITH MULTI PROCESSING (SCENARIO 1)--")
    processes = []  # List of processes
    manager = multiprocessing.Manager()  # Returns a started SyncManager object which can be used for sharing objects
    # between processes.
    times = manager.list([0] * len(urls))  # List to store download times for each image
    cpu_usages = manager.list([0] * len(urls))  # List to store CPU usage for each image
    memory_usages = manager.list([0] * len(urls))  # List to store memory usage for each image
    counter = 1

    # Create a process for each URL and start downloading
    for url in urls:
        process = multiprocessing.Process(target=download_file, args=(url, counter, download_directory, times, cpu_usages, memory_usages))
        # It creates a new process. It starts a process with the target function download_file
        # and args is necessary for parameter of target (download_function)
        processes.append(process)
        process.start()
        counter += 1

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Print download times, CPU and memory usage for each image
    for i, t in enumerate(times):
        print(f"Image {i + 1} download time: {t:.2f} seconds, CPU usage: {cpu_usages[i]:.2f}%, Memory usage: {memory_usages[i]:.2f} MB")

    # Calculate and print total download time, average CPU and total memory usage
    total_time = sum(times)
    average_cpu_usage = sum(cpu_usages) / len(cpu_usages)
    total_memory_usage = sum(memory_usages)

    print("-" * 40)
    print(f"Total download time for all files: {total_time:.2f} seconds")
    print(f"Average CPU usage for all files: {average_cpu_usage:.2f}%")
    print(f"Total memory usage for all files: {total_memory_usage:.2f} MB")
