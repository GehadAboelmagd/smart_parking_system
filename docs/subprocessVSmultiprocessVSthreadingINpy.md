> #  explanation and comparison 
<sub> ( we possibly gonna use one or more of those in next ocr update after fixing some skew issues ) </sub>

#### 1. Subprocess:

The subprocess module allows you to spawn new processes, connect to their input while not result_queue.empty(): print(result_queue.get()) /output/error pipes, and obtain their return codes.
It is used to run external commands or executables, which are separate from the Python script```
In this example, we use the subprocess module to call the Tesseract OCR command-line tool directly itself.
It does not provide any parallelism or concurrency within the Python script, as it is focused on managing external processes.

#### 2. Multiprocess:

 The ocr_image function takes an image queue and a result queuerocessing:
The multiprocessing module provides a way to parallelize your Python code by creating multiple processes, each with its own Python interpreter as arguments. It processes.
It is useful for CPU-bound tasks, as it allows you to take advantage of multiple CPU cores.
It uses inter-process communication (IPC) to share the images using the Tesseract command and data between processes, which can be slower than sharing data between threads.
It avoids the Global Interpreter Lock (GIL) issue in CPython, which puts the OCR results in the result queue. The main part of the script prevents multiple threads from executing Python bytecodes simultaneously.

#### 3. Threading:

The threading module allows you to create multiple threads creates a pool of worker threads that process the images concurrently. The results are within a single process, sharing the same memory space.
It is useful for I/O-bound tasks, where waiting for external resources (e.g., network or then printed to the console. disk I/O) is the primary bottleneck.
Threads share the same memory space, which can lead to easier data sharing but also requires careful synchronization to avoid race conditions.
Due to the GIL in CPython, threads do not provide true parallelism for CPU-bound tasks, as only one thread can execute Python bytecodes at a time.

### Summary :

In summary, use subprocess when you need to run external commands or executables, use multiprocessing for parallelizing CPU-bound tasks, and use threading for I/O-bound tasks or when you need lightweight concurrency within a single process.


> #  examples using pytesseract  
<sub> this examples not for real use its only for sake of clearify diff</sub>



#### Multiprocessing example:

```python


import pytesseract
from PIL import Image
import os
from multiprocessing import Pool

def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

if __name__ == '__main__':
    image_paths = ['image1.png', 'image2.png', 'image3.png', 'image4.png']
    with Pool() as pool:
        results = pool.map(ocr_image, image_paths)

    for result in results:
        print(result)
```		
		
#### Threading example:
```python


import pytesseract
from PIL import Image
import os
from threading import Thread
from queue import Queue

def ocr_image(image_queue, result_queue):
    while not image_queue.empty():
        image_path = image_queue.get()
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        result_queue.put(text)

if __name__ == '__main__':
    image_paths = ['image1.png', 'image2.png', 'image3.png', 'image4.png']
    image_queue = Queue()
    result_queue = Queue()

    for image_path in image_paths:
        image_queue.put(image_path)

    threads = []
    for _ in range(4):
        thread = Thread(target=ocr_image, args=(image_queue, result_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    while not result_queue.empty():
        print(result_queue.get())
```
##### In both examples, we process a list of image paths (image_paths) using pytesseract to perform OCR. The multiprocessing example uses the Pool class to create a pool of worker processes, while the threading example uses the Thread class to create a pool of worker threads. The results are then printed to the console.


#### Subprocess Example:

```python

import pytesseract
from PIL import Image
import os
import subprocess
from queue import Queue
from threading import Thread

def ocr_image(image_queue, result_queue):
    while not image_queue.empty():
        image_path = image_queue.get()
        command = ['tesseract', image_path, 'stdout', '--psm', '6']
        text = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
        result_queue.put(text)

if __name__ == '__main__':
    image_paths = ['image1.png', 'image2.png' , 'image4.png']
	image_queue = Queue()
	result_queue = Queue()
	
	for image_path in image_paths:
		image_queue.put(image_path)

	threads = []
	for _ in range(4):
		thread = Thread(target=ocr_image, args=(image_queue, result_queue))
		thread.start()
		threads.append(thread)

	for thread in threads:
		thread.join()
```

> #  imp. Sources :

1. https://realpython.com/async-io-python/

2. https://stackoverflow.com/questions/2629680/deciding-among-subprocess-multiprocessing-and-thread-in-python

3. https://towardsdatascience.com/multithreading-multiprocessing-python-180d0975ab29

4. GPT4