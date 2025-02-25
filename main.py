import time
import halcon as ha
import numpy as np
#from frame_grabber_module_2_parallel import ImageCapture
import TIS
import image_utils  # Import the new module
import threading
import os
from modbus_server_2 import received_values_queue, run_modbus_server
# Compute timing for initialization of camera and deep_ocr
start = time.time()
import ocr_module  # Assuming this is your OCR module
end = time.time()

tt = time.time()
print(f'Time to initialize the camera: {tt - end:.2f} seconds')
print(f'Time to import and initialize DeepOcr: {end - start:.2f} seconds')

images_to_capture = 0
def process_received_values():
    global images_to_capture
    while True:
        address, values = received_values_queue.get()
        # Process the received values
        print(f"Processing values at address {address}: {values}")
        images_to_capture=values[0]
        # Mark the task as done
        received_values_queue.task_done()
        #return address,value
ocr_threads = []
halcon_img = []
filename_lst = []
timing = []
counter = 0
modbus_thread = threading.Thread(target=run_modbus_server, daemon=True)
modbus_thread.start()
tis = TIS.TIS()
tis.open_device("48420141", 7716, 5360, "143/20", TIS.SinkFormats.BGRA, True)
tis.set_property("FocusAuto","Off")
tis.set_property("Focus",600)
tis.start_pipeline()
path_saving = "saved_images/"
if not os.path.exists(path_saving):
    os.makedirs(path_saving)
# Initialize queues and threads using the new function
save_queue, delete_queue, result_queue, save_thread, delete_thread = image_utils.initialize_queues_and_threads()

processing_thread = threading.Thread(target=process_received_values, daemon=True)
processing_thread.start()

naming_counter = 0
try:
    while True:
        user_input = input("\nEnter something to take an image (type 'e' to quit): ")
        if user_input.lower() == 'e' or images_to_capture==0:#naming_counter>=(images_to_capture-1):
            print("Exiting program.")
            remaining_files = os.listdir("saved_images")
            if len(remaining_files) >0:
                for i in remaining_files:
                    os.remove(path_saving+i)
            break
        else:
            frame_, frame = tis.snap_image(0.1)
            filename = path_saving+f"image_{naming_counter}.jpg"
            save_queue.put((frame, filename))

            st = time.time()
            if frame is not None:
                timing.append(st)
                halcon_img.append(frame)
                filename_lst.append(filename)
                counter += 1

                ocr_thread = threading.Thread(target=image_utils.read_n_execute_ocr, args=(filename, result_queue, delete_queue))
                ocr_thread.start()
                ocr_threads.append(ocr_thread)

                naming_counter += 1
                images_to_capture=images_to_capture-1
            else:
                print("Failed to capture image.")
finally:
            # Wait for OCR threads to finish
    for ocr_thread in ocr_threads:
        ocr_thread.join()
    while not result_queue.empty():
        
        result = result_queue.get()
        print(f"OCR result from thread: {result}")

    # Calculate time intervals between captures
    if len(timing) > 1:
        intervals = np.diff(timing)
        print(f"Average time between captures: {np.mean(intervals):.4f} seconds")
    else:
        print("Not enough data to calculate timing.")

    image_utils.cleanup(tis, save_queue, save_thread, delete_queue, delete_thread)
    print("Cleanup done.")
