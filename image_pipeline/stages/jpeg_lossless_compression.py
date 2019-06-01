import os
import subprocess

from image_pipeline.stages.stage import Stage


class JPEGLossLessCompressionStage(Stage):
    def is_required(self) -> bool:
        return self.configuration.mozjpeg.active and self.output_format.quality is None

    def run_stage(self) -> bytes:
        return self._mozjpeg_compression(self.image_wrapper.raw)

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

    @staticmethod
    def image_format():
        return 'JPEG'
