from image_pipeline.stages.crop_stage import CropStage
from image_pipeline.stages.jpeg_lossless_compression import JPEGLossLessCompressionStage
from image_pipeline.stages.jpeg_lossy_compression import JPEGLossyCompressionStage
from image_pipeline.stages.resize_stage import ResizeStage


pre_stages = [
    ResizeStage,
    CropStage,
]  # List[_Stage]

compression_stages = [
    JPEGLossyCompressionStage,
    JPEGLossLessCompressionStage,
]  # List[_Stage]

post_stages = [
    # PlaceholderGenerationStage,
]  # List[_Stage]

stages = pre_stages + compression_stages + post_stages