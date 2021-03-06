import os
import numpy as np
import PIL.Image as Img
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def extract_image(filename: str):
    """
    extract the image from the mask, used for cvat results
    for colab using, the input is designed for situation where default path have
    both "SegmentationObject" and "JPEGImages" folders
    input:
        filename: str, the name under folder "SegmentationObject"(.png name)
    return:
        np.ndarray, the image extracted by the mask
    """
    assert filename[-3:] == "png"
    _pngname = filename
    _jpgname = filename[:-3] + "jpg"
    _mask_read_in = np.array(Img.open(os.path.join("SegmentationObject",_pngname)).convert("RGB"))
    _original_image_read_in = np.array(Img.open(os.path.join("JPEGImages",_jpgname)).convert("RGB"))
    _mask_convert = np.any(_mask_read_in, axis = 2)
    _original_image_read_in[_mask_convert == 0] = 0
    return _original_image_read_in

def crop_image(img):
    """
    crop all the 0 paddings aside
    input:
      img: np.ndarray, image to be cropped
    return:
      img: np.ndarray, image cropped
    """
    _x = np.nonzero(np.any(img, axis = (0,2)))[0]
    _y = np.nonzero(np.any(img, axis = (1,2)))[0]
    _xs,_xf = _x[0],_x[-1]
    _ys,_yf = _y[0],_y[-1]
    return img[_ys:_yf,_xs:_xf]

def visualize_result(collage, mask, dictionary):
    """
    A visualization of result generated

    Discrete legend part credit to
    https://stackoverflow.com/questions/40662475/matplot-imshow-add-label-to-each-color-and-put-them-in-legend/40666123#40666123

    input:
      collage, mask, dictionary, the output of collage generator's .generate() function, mask is the pixel mask
    """
    _f, _axarr = plt.subplots(1,2)
    _axarr[0].set_axis_off()
    _im1 = _axarr[0].imshow(collage)
    _axarr[1].set_axis_off()
    _mask = mask if mask.ndim == 2 else mask[:,:,0]
    _values = np.unique(_mask.ravel())
    _im2 = _axarr[1].imshow(_mask)
    # get the colors of the values, according to the colormap used by imshow
    _colors = [_im2.cmap(_im2.norm(value)) for value in _values]
    # create a patch (proxy artist) for every color
    _labels = ["background"] + [i for i in dictionary if dictionary[i] in values]
    _patches = [mpatches.Patch(color=_colors[i], label=_labels[i]) for i in range(len(_values))]
    # put those patched as legend-handles into the legend
    plt.legend(handles=_patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0 )
    plt.show()
    print(dictionary)

def extract_binary_mask(mask, dictionary):
    """
    convert a integer mask to multi-channel binary mask
    arg:
        mask, dictionary: output of col_gen.generate() method
    return:
        np.ndarray, the binary mask in different channel
    """
    return np.stack([np.where(mask == i, 1, 0)for i in list(dictionary.values())], axis=-1)
