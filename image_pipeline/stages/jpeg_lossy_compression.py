import os

from image_pipeline.image_wrapper import ImageHelper
from image_pipeline.stages.stage import Stage
import subprocess


class JPEGLossyCompressionStage(Stage):
    def is_required(self) -> bool:
        return self.output_format.quality is not None

    def run_stage(self) -> bytes:
        if self.configuration.mozjpeg.active:
            return self._mozjpeg_compression(self.image_wrapper.raw)
        else:
            image = self.image_wrapper.image
            return ImageHelper.to_bytes(image, quality=self.output_format.quality, optimize=True, format='JPEG')

    def _mozjpeg_compression(self, image: bytes):
        command = (
            os.path.join(self.configuration.mozjpeg.path, 'cjpeg'),
            '-quality', str(self.output_format.quality),
        )
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = process.communicate(input=image)
        if process.returncode != 0:
            print(stderr)
            raise Exception()
        return stdout

    @staticmethod
    def image_format():
        return 'JPEG'
