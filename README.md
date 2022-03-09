# Stream Disk Usage Clean Up
Clean up older screenshots from Stream folder when disk is getting used up
> Ensure you are using the default image format:  
> `image_format = $(camera)_screenshots/%y-%m-%d/%H-%M-%S.%f.jpg`

## Setup

1. Build the image
```bash
docker build --tag platerecognizer/stream-cleaner .
```

2. Run Image 
```bash
docker run --rm -t -v /tmp/stream-template-0:/user-data/  -e INTERVAL=3 -e PERCENTAGE=90 -e LOGGING=DEBUG platerecognizer/stream-cleaner

```

3. Configuration Parameters

| Arg | Default | Description |
| --- | ----------- | --------- |
| -v | **Required** | Stream folder, `config.ini` location |
| -e | INTERVAL=30 | Interval between usage checks. In seconds |
| -e | PERCENTAGE=90 | Screenshots are deleted when percentage is passed |
| -e | LOGGING=INFO | Enable more verbose logging with `DEBUG` |


