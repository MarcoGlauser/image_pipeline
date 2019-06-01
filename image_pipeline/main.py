import time

from image_pipeline.configuration import ConfigurationLoader
from image_pipeline.task_executor import TaskExecutor


def main():
    configuration_filename = "example.yaml"
    configuration = ConfigurationLoader.load_configuration(configuration_filename)
    task_executor = TaskExecutor(configuration)

    for source_directory in configuration.directories:
        source_directory.output_configuration.create_output_folder()
        task_executor.create_tasks_from_source_directory(source_directory)

    task_executor.start()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    elapsed = end - start
    print(f'pipeline took {elapsed} seconds')