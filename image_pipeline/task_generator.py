from image_pipeline.configuration import Configuration
from image_pipeline.task import Task


class TaskGenerator:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def __iter__(self) -> Task:
        for source_directory in self.configuration.directories:
            for source_image in source_directory.search_source_files():
                for output_format in source_directory.output_configuration.output_formats:
                    yield Task(source_image, self.configuration, source_directory.output_configuration, output_format)
