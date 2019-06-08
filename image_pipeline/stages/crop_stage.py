from PIL import Image

from image_pipeline.configuration import Configuration, OutputFormat
from image_pipeline.image_wrapper import ImageHelper
from image_pipeline.stages.stage import Stage


class CropStage(Stage):

    image_format = 'TIFF'

    @classmethod
    def is_required(cls, image_data: bytes, configuration: Configuration, output_format: OutputFormat) -> bool:
        if output_format.width is None or output_format.height is None:
            return False
        image = ImageHelper.from_bytes(image_data)
        image_ratio = image.width / image.height
        output_ratio = output_format.width / output_format.height
        return abs(image_ratio - output_ratio) > 0.01

    def run_stage(self) -> bytes:
        left = (self.image.width - self.output_format.width) / 2
        top = (self.image.height - self.output_format.height) / 2
        right = (self.image.width + self.output_format.width) / 2
        bottom = (self.image.height + self.output_format.height) / 2
        cropped_image = self.image.crop((left, top, right, bottom))
        return ImageHelper.to_bytes(cropped_image, format=self.image_format)
