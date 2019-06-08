import os
from typing import Iterator

from image_pipeline.configuration import OutputConfiguration, OutputFormat, Configuration
from image_pipeline.image_wrapper import ImageWrapper
from image_pipeline.stages import pre_stages, compression_stages, post_stages
from image_pipeline.stages.stage import Stage


class Task:
    def __init__(self, filename: str, configuration: Configuration,  output_configuration: OutputConfiguration, output_format: OutputFormat):
        self.configuration = configuration
        self.output_format = output_format
        self.output_configuration = output_configuration
        self.image_wrapper = None
        self.filename = filename

    def prepare_task(self):
        self.image_wrapper = ImageWrapper(self.filename)

    def run_task(self):
            self.prepare_task()
            self._run_stages(pre_stages, keep_result=True)
            self._run_stages(self._get_compression_stages(), keep_result=True)
            self._save_result()
            self._run_stages(post_stages)

    def _get_compression_stages(self) -> Iterator[type(Stage)]:
        if self.output_configuration.file_format is None:
            file_format = self.image_wrapper.original_format
        else:
            file_format = self.output_configuration.file_format
        return [stage for stage in compression_stages if stage.image_format == file_format]

    def _run_stages(self, stages: Iterator[type(Stage)], keep_result=False):
        for stage_class in stages:
            if stage_class.is_required(self.image_wrapper.raw, self.configuration, self.output_format):
                if self.image_wrapper.format != stage_class.image_format:
                    print('Conversion Required from {input} to {output}'.format(
                        input=self.image_wrapper.format,
                        output=stage_class.image_format))
                    self.image_wrapper.convert_to(stage_class.image_format)
                stage = stage_class(self.image_wrapper.raw, self.configuration, self.output_format)
                print(stage_class.__name__, self.output_format.name)
                stage_result = stage.run_stage()
                if keep_result:
                    self.image_wrapper.raw = stage_result
        print()

    def _save_result(self):
        self._set_correct_output_format()
        output_path = os.path.join(self.output_configuration.path,
                                   self.output_format.output_filename(self.output_configuration.file_prefix, self.image_wrapper))
        with open(output_path, "wb") as output_file:
            output_file.write(self.image_wrapper.raw)

    def _set_correct_output_format(self):
        if self.output_configuration.file_format is None:
            if self.image_wrapper.format != self.image_wrapper.original_format:
                print('Conversion Required from {input} to {output}'.format(
                    input=self.image_wrapper.format,
                    output=self.image_wrapper.original_format))
                self.image_wrapper.convert_to(self.image_wrapper.original_format)
        else:
            if self.image_wrapper.format != self.output_configuration.file_format:
                print('Conversion Required from {input} to {output}'.format(
                    input=self.image_wrapper.format,
                    output=self.output_configuration.file_format))
                self.image_wrapper.convert_to(self.output_configuration.file_format)
