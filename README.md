# Processing Webservice

Webservice providing raster-file and time-series processing

## Raster file processing

* https://\<url>/rasters/

You can upload a a valid [gdal-raster-file](https://gdal.org/drivers/raster/index.html) over the web-frontend 
or a POST-request.

Uploading a valid file will generate the following answer-structure:

```
{
    "status": 200, 
    "hash": "46f670f9-395d-4dde-b146-2506b8244ab2_jpg", 
    "get_metadata": "/46f670f9-395d-4dde-b146-2506b8244ab2_jpg", 
    "get_data": "/46f670f9-395d-4dde-b146-2506b8244ab2_jpg/data", 
    "get_scaled_data": "/46f670f9-395d-4dde-b146-2506b8244ab2_jpg/data"
}

```

To get the raster-metadata:

* https://\<url>/rasters/\<get_metadata_id>

```
{
    "driver": "JPEG", 
    "rasterXSize": 1005, 
    "rasterYSize": 718, 
    "rasterCount": 3, 
    "projection": "", 
    "origin": [0.0, 0.0], 
    "pixelSize": [1.0, 1.0]
}
```

To get the raw-data:

* https://\<url>/rasters/\<get_metadata_id>/data

To retrieve the scaled data with an optional interpolation method:

* https://\<url>/rasters/\<get_metadata_id>/data/\<width>/\<height>/\<method>

With the following Interpolation Methods from [skimage.transform.warp](https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.warp):

```
    0: Nearest-neighbor  
    1: Bi-linear (default)  
    2: Bi-quadratic  
    3: Bi-cubic  
    4: Bi-quartic  
    5: Bi-quintic
```  
 

## Time series processing

Time series processing implements the [pandas.DataFrame.resample](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html) function.

You can send a POST-request to:

* https://\<url>/timeseries/resample?rule=\<rule>&interpolation_method=\<interpolation_method>

Data structure: 

```
[
  {
    "timeStamp": <int>,
    "value": <float>
  },
  ...,
```

Parameters:

```
    rule: p.e. 1d, 1w, 1y, 2w, 2d 

    interpolation method: p.e. time, cubic, etc.
``` 



