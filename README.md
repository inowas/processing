# Processing Webservice

Webservice providing raster-file and time-series processing

## Raster file processing

* https://\<url>/rasters/

You can upload a a valid [gdal-raster-file](https://gdal.org/drivers/raster/index.html) over the web-frontend or a
POST-request.

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

With the following Interpolation Methods
from [skimage.transform.warp](https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.warp):

```
    0: Nearest-neighbor  
    1: Bi-linear (default)  
    2: Bi-quadratic  
    3: Bi-cubic  
    4: Bi-quartic  
    5: Bi-quintic
```  

## Time series processing

Time series processing implements
the [pandas.DataFrame.resample](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html)
function.

You can send a POST-request to:

* https://\<url>/timeseries/resample?rule=\<rule>&interpolation_method=\<interpolation_method>&aggregate=\<aggregate>

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
    aggregate: true, false
```

## Visualisation

We have implemented some image generation with mathplotlib.

### Contour

You can send a POST-request to:

* https://\<url>/visualization/contour

The data structure must be a 2D array:

```
[
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

Parameters:

```
    xmin: reference as float, default 0
    xmax: reference as float, default np.shape(data)[0]
    ymin: reference as float, default 0
    ymax: reference as float, default np.shape(data)[1]
    clevels: number of contours shown, default 10
    cmap: contour map string, default: Greens
    clabel: contour label, default: ""
    target: the target size/format, default: web
```

#### Valid contour map strings

```
'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r',
'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r',
'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1',
'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r',
'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r',
'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r',
'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu',
'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn',
'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis',
'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix',
'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r',
'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r',
'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r',
'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet',
'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink',
'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r',
'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b',
'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight',
'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
```

#### CURL Example for contour

```shell
curl --location --request POST 'https://<url>/visualization/contour?xmin=100&xmax=200&ymin=100&ymax=200&clevels=4&cmap=Spectral&target=web&clabel=test' \
--header 'Content-Type: application/json' \
--data-raw '[
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]'


```

