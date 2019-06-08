from PIL import Image

from image_pipeline.configuration import Configuration, OutputFormat
from image_pipeline.image_wrapper import ImageHelper
from image_pipeline.stages.stage import Stage


class ResizeStage(Stage):

    image_format = 'TIFF'

    @classmethod
    def is_required(cls, image_data: bytes, configuration: Configuration, output_format: OutputFormat) -> bool:
        image = ImageHelper.from_bytes(image_data)
        image_has_different_size = image.height != output_format.height or image.width != output_format.width
        keep_size = output_format.height is None and output_format.width is None
        return not keep_size and image_has_different_size

    def run_stage(self) -> bytes:
        if self.output_format.height is not None and self.output_format.width is not None:
            if self.image.height > self.image.width:
                ratio = self.output_format.width / self.image.width
            else:
                ratio = self.output_format.height / self.image.height
        elif self.output_format.height is not None:
            ratio = self.output_format.height / self.image.height
        else:
            ratio = self.output_format.width / self.image.width
        size = (round(self.image.width * ratio), round(self.image.height * ratio))
        resized_image = self.image.resize(size, Image.ANTIALIAS)
        return ImageHelper.to_bytes(resized_image, format=self.image_format)
