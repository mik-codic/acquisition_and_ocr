# image_utils.py
import threading
import queue
import cv2
import os
import halcon as ha
import time
import ocr_module

def save_img(save_queue):
    while True:
        try:
            frame, filename = save_queue.get()
            if frame is None:
                # Exit signal received
                save_queue.task_done()
                break
            cv2.imwrite(filename, frame)
            print(f'Saved {filename}')
            save_queue.task_done()
        except Exception as e:
            print(f"Error saving image: {e}")

def read_n_execute_ocr(filename, result_queue, delete_queue):
    retries = 0
    flag = False
    
    while retries < 5 and not flag:
        try:
            halcon_img_ = ha.read_image(filename)
            start_t = time.time()
            txt = ocr_module.run_ocr(halcon_img_)
            result_queue.put(txt)
            flag = True
            end_t = time.time()
            print("\nactual time of execution of the thread", end_t - start_t)
            delete_queue.put(filename)  # Add filename to delete queue
            return
        except Exception as e:
            time.sleep(0.2)
            print(f"Error in OCR processing: {e}")
            retries += 1
    print("\nfailed to read and ocr")
    result_queue.put(None)

def delete_file(delete_queue):
    while True:
        filename = delete_queue.get()
        if filename is None:
            # Exit signal received
            delete_queue.task_done()
            break
        try:
            os.remove(filename)
            print(f"Deleted {filename}")
        except Exception as e:
            print(f"Error deleting file: {e}")
        delete_queue.task_done()

def initialize_queues_and_threads():
    save_queue = queue.Queue()
    delete_queue = queue.Queue()
    result_queue = queue.Queue()
    
    # Start the image-saving thread
    save_thread = threading.Thread(target=save_img, args=(save_queue,))
    save_thread.daemon = True  # Daemonize thread
    save_thread.start()

    # Start the file-deleting thread
    delete_thread = threading.Thread(target=delete_file, args=(delete_queue,))
    delete_thread.daemon = True  # Daemonize thread
    delete_thread.start()

    return save_queue, delete_queue, result_queue, save_thread, delete_thread

def cleanup(tis, save_queue, save_thread, delete_queue, delete_thread):
    # Signal the saving thread to exit
    save_queue.put((None, None))
    save_queue.join()
    save_thread.join()
    tis.stop_pipeline()
    delete_queue.put(None)
    delete_queue.join()
    delete_thread.join()
    print("Pipeline and threads cleaned up")
