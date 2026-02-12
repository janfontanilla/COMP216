# COMP 216 - Lab Assignment 5 - Part 1

import threading, time


def long_task(name):
   
    # Loop + tiny sleep to simulate waiting on I/O
    # 0.0001 sec sleep * 100,000 iterations
    for _ in range(100_000):
        time.sleep(0.0001)

    # Print when task finishes
    print(f'{name} finished')


def run_sequentially(times):
   
   # Runs long_task sequentially.
    start = time.perf_counter()  # start timer

    # Run tasks one by one
    for i in range(times):

        task_start = time.perf_counter()
        long_task(f'Sequential Task-{i + 1}')
        task_end = time.perf_counter()
        print(f'Task {i + 1} took {round(task_end - task_start, 2)} seconds')

    end = time.perf_counter()  # end timer

    print(f'Total time: {round(end - start, 2)} seconds')


def run_with_threads(times):
  
    #Runs long_task using multiple threads.
   

    start = time.perf_counter()  # start timer
    thread_list = []  # store threads to join later

    # Create + start threads
    for i in range(times):
        t = threading.Thread(
            target=long_task,
            args=(f'Threaded Task-{i + 1}',)
        )
        thread_list.append(t)
        t.start()

    # Shows how many threads are active
    print(f'Active threads: {threading.active_count()}')

    # Wait for all threads to finish
    for t in thread_list:
        t.join()

    end = time.perf_counter()  # end timer

    print(f'Threads total time: {round(end - start, 2)} seconds')


if __name__ == '__main__':


    print('Running 10 tasks sequentially...')
    print()
    run_sequentially(10)

    print()

    print()
    print('Running 10 tasks with threads...')
    print()
    run_with_threads(10)
    print()

    print('Done!')
