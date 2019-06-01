from PIL import Image

from image_pipeline.image_wrapper import ImageHelper
from image_pipeline.stages.stage import Stage


class CropStage(Stage):
    def is_required(self) -> bool:
        if self.output_format.width is None or self.output_format.height is None:
            return False
        image = self.image_wrapper.image
        image_ratio = image.width / image.height
        output_ratio = self.output_format.width / self.output_format.height
        return abs(image_ratio - output_ratio) > 0.01

    def run_stage(self) -> Image.Image:
        image = self.image_wrapper.image
        left = (image.width - self.output_format.width) / 2
        top = (image.height - self.output_format.height) / 2
        right = (image.width + self.output_format.width) / 2
        bottom = (image.height + self.output_format.height) / 2
        cropped_image = image.crop((left, top, right, bottom))
        return ImageHelper.to_bytes(cropped_image, format=self.image_format())

    @staticmethod
    def image_format():
        return 'TIFF'
