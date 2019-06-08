from image_pipeline.configuration import OutputFormat, Configuration
from image_pipeline.image_wrapper import ImageHelper


class Stage:

    image_format = NotImplementedError()

    def __init__(self, image_data: bytes, configuration: Configuration, output_format: OutputFormat):
        self.image_data = image_data
        self.image = ImageHelper.from_bytes(image_data)
        self.output_format = output_format
        self.configuration = configuration

    @classmethod
    def is_required(cls, image_data: bytes, configuration: Configuration, output_format: OutputFormat) -> bool:
        raise NotImplementedError()

    def run_stage(self) -> bytes:
        raise NotImplementedError()

    def image_from_bytes(self):
        pass

