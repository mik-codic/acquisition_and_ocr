import time
import halcon as ha
import numpy as np
#from frame_grabber_module_2_parallel import ImageCapture
import TIS
import image_utils  # Import the new module
import threading

# Compute timing for initialization of camera and deep_ocr
start = time.time()
import ocr_module  # Assuming this is your OCR module
end = time.time()

tt = time.time()
print(f'Time to initialize the camera: {tt - end:.2f} seconds')
print(f'Time to import and initialize DeepOcr: {end - start:.2f} seconds')

ocr_threads = []
halcon_img = []
filename_lst = []
timing = []
counter = 0

tis = TIS.TIS()
tis.open_device("48420141", 7716, 5360, "143/20", TIS.SinkFormats.BGRA, True)
tis.set_property("FocusAuto","Off")
tis.set_property("Focus",600)
tis.start_pipeline()

# Initialize queues and threads using the new function
save_queue, delete_queue, result_queue, save_thread, delete_thread = image_utils.initialize_queues_and_threads()

naming_counter = 0
try:
    while True:
        user_input = input("\nEnter something to take an image (type 'e' to quit): ")
        if user_input.lower() == 'e':
            print("Exiting program.")
            break
        else:
            frame_, frame = tis.snap_image(0.1)
            filename = f"image_{naming_counter}.jpg"
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
            else:
                print("Failed to capture image.")

    while not result_queue.empty():
        result = result_queue.get()
        print(f"OCR result from thread: {result}")

    # Calculate time intervals between captures
    if len(timing) > 1:
        intervals = np.diff(timing)
        print(f"Average time between captures: {np.mean(intervals):.4f} seconds")
    else:
        print("Not enough data to calculate timing.")
finally:
    image_utils.cleanup(tis, save_queue, save_thread, delete_queue, delete_thread)
    print("Cleanup done.")
