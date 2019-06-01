from image_pipeline.configuration import OutputFormat, Configuration
from image_pipeline.image_wrapper import ImageWrapper


class Stage:
    def __init__(self, image_wrapper: ImageWrapper, configuration: Configuration, output_format: OutputFormat):
        self.image_wrapper = image_wrapper
        self.output_format = output_format
        self.configuration = configuration

    def is_required(self) -> bool:
        raise NotImplementedError()

    def run_stage(self) -> bytes:
        raise NotImplementedError()

    def image_from_bytes(self):
        pass

    @staticmethod
    def image_format():
        raise NotImplementedError()
