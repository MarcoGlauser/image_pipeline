# Image Pipeline
The goal of this project is to provide an easily configurable pipeline to process images
for web publishing.

**Features**:
* Resizing and cropping of images
* Easily resize and image to various sizes for responsive websites
* JPEG optimization with mozjpeg
* Multiprocessing
* Conversion between formats (including WebP)


## Configuration Options

### Example
This configuration will take all pictures from the folder exmaple-data
and create 3 variants for each picture. `example-data/test.jpeg` will
become
`example-data/output/test-small.jpeg`,
`example-data/output/test-medium.jpeg` and
`example-data/output/test-large.jpeg`
with the correct resolution. It will make use of multiprocessing and
the mozjpeg library to achieve the best result.


```yaml
multiprocessing:
  active: true
  processes: 4
mozjpeg:
  active: true
directories:
  - path: "example-data"
    output:
      fileFormat: 'JPEG'
      path: "example-data/output"
      prefix: ''
      formats:
        - name: small
          width: 200
          quality: 70
        - name: medium
          width: 400
          quality: 80
        - name: large
          width: 800
          quality: 80
```

### Multiprocessing
Turn multiprocessing on or off
```yaml
multiprocessing:
  active: true|false
  processes: 4
```
### Mozjpeg
configure the use of the mozjpeg library for jpeg compression
```yaml
mozjpeg:
  path: /opt/mozjpeg/bin/
  active: true
```

### Directory
```yaml
path: 'example-data'
output: OutputDirectory
```

### Output Directory
If `fileFormat` is empty, the pipeline try to output it in the same
format.

```yaml
fileFormat: 'JPEG'|'PNG'|'WEBP'
path: 'example-data/output'
prefix: ''
formats: [OutputFormat]
```


### Output Format
Quality is only respected for JPEG compression. If quality is set to
null, image-pipeline will try to use lossless compression for JPEG.
Default quality is 80, if not specified.
```yaml
name: 'asdf'
width: 200
height: 200
quality: 80 | null
```


# Todo
* Caching
* Dockerfile
* PNG optimization
* Hanlde EXIF data
* Add SVG placeholder functionality