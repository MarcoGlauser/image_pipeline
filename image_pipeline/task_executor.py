import signal
from multiprocessing import Semaphore, Pool
from queue import Queue

from image_pipeline.configuration import Configuration, SourceDirectory
from image_pipeline.task import Task


class TaskExecutor:

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.tasks = Queue()
        self.stop = False
        if self.configuration.multiprocessing.active:
            self._workers = Semaphore(self.configuration.multiprocessing.processes + 1)
            self._pool = Pool(processes=self.configuration.multiprocessing.processes)

    def create_tasks_from_source_directory(self, source_directory: SourceDirectory):
        for source_image in source_directory.search_source_files():
            for output_format in source_directory.output_configuration.output_formats:
                task = Task(source_image, self.configuration, source_directory.output_configuration, output_format)
                self.tasks.put(task)

    def start(self):
        while not self.tasks.empty() and not self.stop:
            task = self.tasks.get()

            if self.configuration.multiprocessing.active:
                self._workers.acquire()
                self._pool.apply_async(task.run_task, callback=self._task_done)
            else:
                task.run_task()

        self._stop_multiprocessing()

    def _task_done(self, callback_value):
        self._workers.release()

    def _stop_multiprocessing(self):
        if self.configuration.multiprocessing.active:
            self._pool.close()
            self._pool.join()

    def _set_stop_signal_handler(self):
        signal.signal(signal.SIGTERM, self._handle_stop_signal)

    def _handle_stop_signal(self, signum, frame):
        self.stop = True

