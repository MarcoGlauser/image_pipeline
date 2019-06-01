from PIL import Image

from image_pipeline.image_wrapper import ImageHelper
from image_pipeline.stages.stage import Stage


class ResizeStage(Stage):

    @staticmethod
    def image_format():
        return 'TIFF'

    def is_required(self) -> bool:
        image = self.image_wrapper.image
        image_has_different_size = image.height != self.output_format.height or image.width != self.output_format.width
        keep_size = self.output_format.height is None and self.output_format.width is None
        return not keep_size and image_has_different_size

    def run_stage(self):
        image = self.image_wrapper.image
        if self.output_format.height is not None and self.output_format.width is not None:
            if image.height > image.width:
                ratio = self.output_format.width / image.width
            else:
                ratio = self.output_format.height / image.height
        elif self.output_format.height is not None:
            ratio = self.output_format.height / image.height
        else:
            ratio = self.output_format.width / image.width
        size = (round(image.width * ratio), round(image.height * ratio))
        resized_image = image.resize(size, Image.ANTIALIAS)
        return ImageHelper.to_bytes(resized_image, format=self.image_format())
