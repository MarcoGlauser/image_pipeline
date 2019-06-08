import os
import subprocess

from image_pipeline.configuration import Configuration, OutputFormat
from image_pipeline.stages.stage import Stage


class JPEGLossLessCompressionStage(Stage):

    image_format = 'JPEG'

    @classmethod
    def is_required(cls, image_data: bytes, configuration: Configuration, output_format: OutputFormat) -> bool:
        return configuration.mozjpeg.active and output_format.quality is None

    def run_stage(self) -> bytes:
        return self._mozjpeg_compression(self.image_data)

    def _mozjpeg_compression(self, image: bytes):
        command = (
            os.path.join(self.configuration.mozjpeg.path, 'jpegtran')
        )
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = process.communicate(input=image)
        if process.returncode != 0:
            print(stderr)
            raise Exception()
        return stdout
