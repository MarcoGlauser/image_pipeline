import io
import os

from PIL import Image


class ImageWrapper:
    def __init__(self, path: str):
        self.path = path
        self.basename = os.path.basename(self.path)
        self.filename, self.extension = os.path.splitext(self.basename)
        self._image = None
        self._bytes = None

        with open(self.path, 'rb') as image_file:
            self.raw = image_file.read()

        self.original_format = self.image.format
        self.format = self.original_format

    def convert_to(self, image_format: str):
        if image_format == 'JPEG':
            self.convert_to_jpeg()
        else:
            buffered = io.BytesIO()
            self.image.save(buffered, format=image_format)
            self.raw = buffered.getvalue()
            self.format = image_format

    def convert_to_jpeg(self, quality: int = 95, optimize: bool = False):
        buffered = io.BytesIO()
        rgb_image = self.image.convert('RGB')
        rgb_image.save(buffered, quality=quality, optimize=optimize, format="JPEG")
        self.raw = buffered.getvalue()
        self.format = 'JPEG'

    @property
    def image(self) -> Image.Image:
        return self._image

    @property
    def raw(self) -> bytes:
        buffered = io.BytesIO()
        self.image.save(buffered, format=self.format)
        return buffered.getvalue()

    @raw.setter
    def raw(self, data: bytes):
        self._bytes = data
        self._image = Image.open(io.BytesIO(data))


class ImageHelper:

    @staticmethod
    def to_bytes(image: Image, format: str = 'JPEG', **options) -> bytes:
        bytestream = io.BytesIO()
        image.save(bytestream, format=format, **options)
        return bytestream.getvalue()

    @staticmethod
    def from_bytes(data: bytes):
        return Image.open(io.BytesIO(data))

    @staticmethod
    def from_filename(path: str):
        return Image.open(path)
