import hashlib
import io
import json
import os
from flask import abort, Blueprint, request, Response, redirect
from flask_cors import cross_origin
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

visualization = Blueprint(
    'visualization',
    __name__,
    url_prefix='/visualization',
    template_folder='templates',
    static_folder='static'
)

DATA_FOLDER = './data'


@visualization.route('/contour', methods=['POST'])
@cross_origin()
def post_contour():
    if request.content_type != 'application/json':
        abort(422, 'The content type is expected to be "application/json".')

    data = None
    try:
        data = np.asarray(request.json)
    except ValueError as e:
        abort(422, str(e))

    target_directory = os.path.join(DATA_FOLDER)
    os.makedirs(target_directory, exist_ok=True)
    json_string = json.dumps(data.tolist(), sort_keys=True)
    hash = hashlib.md5(json_string.encode("utf-8")).hexdigest()
    filepath = os.path.join(target_directory, hash + '.json')

    if not os.path.exists(filepath):
        with open(filepath, 'w') as outfile:
            json.dump(data.tolist(), outfile)

    return redirect('contour/' + hash)


@visualization.route('/contour/<hash>', methods=['GET'])
@cross_origin()
def get_contour(hash):
    file_path = os.path.join(DATA_FOLDER, hash + '.json')
    if not os.path.exists(file_path):
        abort(404)

    data = None
    try:
        data = np.asarray(read_json(file_path))
    except ValueError as e:
        abort(400, str(e))

    data[data == -1] = 9999

    x_min = float(request.args.get('xmin', default=0))
    x_max = float(request.args.get('xmax', default=np.shape(data)[0]))
    y_min = float(request.args.get('ymin', default=0))
    y_max = float(request.args.get('ymax', default=np.shape(data)[1]))
    z_min = np.amin(data)
    z_max = np.partition(np.unique(data.flatten().round(decimals=10)), -1)[-2]
    c_levels = int(request.args.get('clevels', 10))
    c_map = get_cmap(request.args.get('cmap', 'Greens'))
    c_label = request.args.get('clabel', '')
    x_label = request.args.get('xlabel', '')
    y_label = request.args.get('ylabel', '')
    target = request.args.get('target', 'web')

    x_axis = np.linspace(x_max, x_min, num=np.shape(data)[0])
    y_axis = np.linspace(y_max, y_min, num=np.shape(data)[1])
    X, Y = np.meshgrid(x_axis, y_axis)

    fig = get_figure_for_target(target)
    axis = fig.add_subplot(1, 1, 1)
    axis.plot()
    levels = np.linspace(z_min, z_max, c_levels)
    plt.contourf(X, Y, data, levels=levels, cmap=c_map)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if x_max < x_min:
        plt.gca().invert_xaxis()

    if y_max > y_min:
        plt.gca().invert_yaxis()
    clb = plt.colorbar(ticks=levels)
    clb.set_label(label=c_label, rotation=90, labelpad=0)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@visualization.route('/contour3d', methods=['POST'])
@cross_origin()
def post_contour_3d():
    if request.content_type != 'application/json':
        abort(422, 'The content type is expected to be "application/json".')

    data = None
    try:
        data = np.asarray(request.json)
    except ValueError as e:
        abort(422, str(e))

    target_directory = os.path.join(DATA_FOLDER)
    os.makedirs(target_directory, exist_ok=True)
    json_string = json.dumps(data.tolist(), sort_keys=True)
    hash = hashlib.md5(json_string.encode("utf-8")).hexdigest()
    filepath = os.path.join(target_directory, hash + '.json')

    if not os.path.exists(filepath):
        with open(filepath, 'w') as outfile:
            json.dump(data.tolist(), outfile)

    return redirect('contour3d/' + hash)


@visualization.route('/contour3d/<hash>', methods=['GET'])
@cross_origin()
def get_contour_3d(hash):
    file_path = os.path.join(DATA_FOLDER, hash + '.json')
    if not os.path.exists(file_path):
        abort(404)

    data = None
    try:
        data = np.asarray(read_json(file_path))
    except ValueError as e:
        abort(400, str(e))

    x_min = float(request.args.get('xmin', default=0))
    x_max = float(request.args.get('xmax', default=np.shape(data)[0]))
    y_min = float(request.args.get('ymin', default=0))
    y_max = float(request.args.get('ymax', default=np.shape(data)[1]))
    z_min = np.amin(data)
    z_max = np.partition(np.unique(data.flatten().round(decimals=10)), -1)[-2]
    c_levels = int(request.args.get('clevels', 10))
    c_map = get_cmap(request.args.get('cmap', 'Greens'))
    c_label = request.args.get('clabel', '')
    x_label = request.args.get('xlabel', '')
    y_label = request.args.get('ylabel', '')
    z_label = request.args.get('zlabel', '')
    target = request.args.get('target', 'web')

    x_axis = np.linspace(x_max, x_min, num=np.shape(data)[0])
    y_axis = np.linspace(y_max, y_min, num=np.shape(data)[1])
    X, Y = np.meshgrid(x_axis, y_axis)

    fig = get_figure_for_target(target)

    axes = plt.axes(projection='3d')
    levels = np.linspace(z_min, z_max, c_levels)
    plot_surface = axes.plot_surface(X, Y, data, cmap=c_map, vmin=z_min, vmax=z_max)
    color_bar = fig.colorbar(plot_surface, shrink=0.5, aspect=30, location='bottom', pad=0.05, anchor=(0.5, 0.5))

    # Font size for color bar
    color_bar.ax.tick_params(labelsize=5)

    color_bar.set_label(c_label, size=7)
    axes.set_xlabel(x_label, size=7)
    axes.set_ylabel(y_label, size=7)
    axes.set_zlabel(z_label, size=7)

    # Font size for x y z axes
    axes.tick_params(axis='both', which='major', labelsize=5)
    axes.tick_params(axis='both', which='minor', labelsize=5)

    if x_max < x_min:
        plt.gca().invert_xaxis()

    if y_max > y_min:
        plt.gca().invert_yaxis()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def get_cmap(cmap: str, default='Greens') -> str:
    valid_cmaps = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r',
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
                   'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']

    if cmap in valid_cmaps:
        return cmap

    return default


def get_figure_for_target(target: str):
    if target == 'web':
        return plt.figure()

    return plt.figure()


def read_json(file):
    with open(file) as file_data:
        data = json.loads(file_data.read())
    return data
