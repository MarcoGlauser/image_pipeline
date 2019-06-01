import multiprocessing
import os

import yaml
from logging import getLogger
from typing import List

from image_pipeline.image_wrapper import ImageWrapper

logger = getLogger(__name__)

SOURCE_FILE_ENDINGS = ('.jpg', '.jpeg', '.png')

default_values = {
    'multiprocessing': {
        'active': True,
        'processes': multiprocessing.cpu_count()
    },
    'mozjpeg': {
        'active': True,
        'path': '/opt/mozjpeg/bin'
    },
    'directories': {
        'output': {
            'file_format': None,
            'placeholder': False,
            'remove_metadata': True,
            'progressive': True,
            'prefix': '',
            'formats': {
                'quality': 80,
                'height': None,
                'width': None
            }
        }
    }
}


class Configuration:
    def __init__(self, configuration: dict):
        self.directories = []  # type: List[SourceDirectory]
        self.multiprocessing = MultiProcessingConfiguration.from_dict(configuration)  # type: MultiProcessingConfiguration
        self.mozjpeg = MozJpegConfiguration.from_dict(configuration)  # type: MozJpegConfiguration
        self._configure_directories(configuration)

    def _configure_directories(self, configuration: dict) -> None:
        for directory in configuration.get('directories', []):
            try:
                source_directory = SourceDirectory.from_dict(directory)
                self.directories.append(source_directory)
            except KeyError as e:
                # Todo proper error handling
                logger.error(e)


class MultiProcessingConfiguration:
    def __init__(self, active: bool, processes: int):
        self.processes = processes
        self.active = active

    @staticmethod
    def from_dict(data: dict):
        multiprocessing_configuration = data.get('multiprocessing', default_values['multiprocessing'])
        active = multiprocessing_configuration.get('active', default_values['multiprocessing']['active'])
        processes = multiprocessing_configuration.get('processes', default_values['multiprocessing']['processes'])
        return MultiProcessingConfiguration(active, processes)


class MozJpegConfiguration:
    def __init__(self, active: bool, path: str):
        self.path = path
        self.active = active

    @staticmethod
    def from_dict(data: dict):
        mozjpeg_configuration = data.get('mozjpeg', default_values['mozjpeg'])
        active = mozjpeg_configuration.get('active', default_values['mozjpeg']['active'])
        path = mozjpeg_configuration.get('path', default_values['mozjpeg']['path'])
        return MozJpegConfiguration(active, path)


class OutputFormat:
    def __init__(self, name: str, quality: int or None, width: int, height: int):
        self.height = height
        self.width = width
        self.quality = quality
        self.name = name

    def output_filename(self, prefix: str, image_wrapper: ImageWrapper):
        filename = image_wrapper.filename
        file_extension = '.' + image_wrapper.format.lower()
        return f'{prefix}{filename}_{self.name}{file_extension}'

    @staticmethod
    def from_dict(data: dict):
        name = data['name']
        quality = data.get('quality', default_values['directories']['output']['formats']['quality'])
        width = data.get('width', default_values['directories']['output']['formats']['width'])
        height = data.get('height', default_values['directories']['output']['formats']['height'])
        return OutputFormat(name, quality, width, height)


class OutputConfiguration:
    def __init__(self, path: str, file_prefix: str, file_format: str, placeholder: bool, remove_metadata: bool, output_formats: List[OutputFormat]):
        self.output_formats = output_formats
        self.file_prefix = file_prefix
        self.file_format = file_format
        self.remove_metadata = remove_metadata
        self.placeholder = placeholder
        self.path = path

    def create_output_folder(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    @staticmethod
    def from_dict(data: dict):
        path = data['path']
        file_prefix = data.get('prefix', default_values['directories']['output']['prefix'])
        file_format = data.get('fileFormat', default_values['directories']['output']['file_format'])
        placeholder = data.get('placeholder', default_values['directories']['output']['placeholder'])
        remove_exif = data.get('removeMetadata', default_values['directories']['output']['remove_metadata'])
        output_formats = [OutputFormat.from_dict(output_format) for output_format in data['formats']]
        return OutputConfiguration(path, file_prefix, file_format, placeholder, remove_exif, output_formats)


class SourceDirectory:
    def __init__(self, path: str, output_configuration: OutputConfiguration):
        self.output_configuration = output_configuration
        self.path = path

    def search_source_files(self):
        source_files = os.listdir(self.path)
        for source_file in source_files:
            if source_file.lower().endswith(SOURCE_FILE_ENDINGS):
                yield os.path.join(self.path, source_file)

    @staticmethod
    def from_dict(data: dict):
        path = data['path']
        output_configuration = OutputConfiguration.from_dict(data['output'])

        return SourceDirectory(path, output_configuration)


class ConfigurationLoader:
    @staticmethod
    def load_configuration(filename: str) -> Configuration:
        with open(filename, 'r') as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)
            return Configuration(config)

