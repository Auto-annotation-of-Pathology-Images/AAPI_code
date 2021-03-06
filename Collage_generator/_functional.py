import PIL.Image as Img
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
import os

"""
All the public methods for the collage_generator not for the final generating
"""

class _functional():

    def add_label(self, new_label: str):
        """
        add a new label into the generator
        Args:
          new_label: string, the name of this label
        """
        if new_label in self._label_list:
            pass
        else:
            #add new label into the list
            self._label_list.append(new_label)
            #meanwhile update the label_dict and the image storage
            self._label_dict = dict(zip(self._label_list, range(1, len(self._label_list)+1)))
            self._image_list.append([])

    def add_image(self,
                  img,
                  label: str,
                  original_image_size = False,
                  size: Tuple[int,int] = (80,60),
                  pre_determined_size: bool = False):
        """
        add an image into the image storages with specified label and size.
        refresh the used_image flag for each image in _image_list
        Args:
          img: str/np.ndarray/PIL.Image object, the path of the image or the image object
          label: str, the label of the image, which must be in the label list
          original_image_size: bool, if True, will use the original image size
          size: tuple of int, the size of the image in the image storage
          pre_determined_size: bool, if False, will ask the user for a correct shape with preview
        """
        assert label in self._label_list

        if original_image_size == True:
            np_img = self._unify_image_format(img, output_format = "np")
            size = np_img.shape[:2]
        else:
            read_in = self._unify_image_format(img, output_format = "PIL")
            # confirm the correct size of the image
            if pre_determined_size == True:
                np_img = np.array(self._resize(read_in,*size))
            else:
                size_okay = False
                while (not size_okay):
                    # resize it and preview
                    np_img = np.array(self._resize(read_in,*size))
                    plt.imshow(self._single_image_preview(np_img, canvas_size = self._canvas_size))
                    plt.show()
                    # check if original size okay
                    size_okay_input = input("is the size okay? [y/n] ")

                    # if the size if acceptable, leave the loop
                    if size_okay_input == "y" or size_okay_input == "Y":
                        size_okay = True

                    # otherwise update a new shape
                    else:
                        print(f"current size is {size}, please specify a new one")
                        input_ok = False
                        while not input_ok:
                          new_x = input("new x: ")
                          new_y = input("new y: ")
                          try:
                            new_x = int(new_x)
                            new_y = int(new_y)
                            input_ok = True
                          except:
                            print("invalid input")
                        size = (new_x, new_y)
        size = np.array(size)
        self._image_list[self._label_dict[label]-1].append(np_img)
        self._max_component_size = np.max(np.vstack((self._max_component_size, size)), axis = 0)
        # It's a little bit dumb to have it here but I have no choice
        # create a "used" flag for each element in image_list
        # if it's used, the corresponding flag will be 1
        # the used flag will have a lower priority in the selection
        self._image_list_used = [np.zeros(len(i)) for i in self._image_list]
        print(f'image succesfully added to label "{label}" with size {size}')

    def _single_image_preview(self, img: np.ndarray, canvas_size: Tuple[int,int] = (1,1)):
        """
        Helper function for add_image, generate a size preview for single image vs canvas size
        args:
          img: np.ndarray, the image to be added
          canvas_size: tuple of int, length = 2, the size of canvas
        return:
          canvas: a canvas with img on the topleft corner
        """
        canvas = np.full(shape =(*self._canvas_size,3),
                         fill_value = 255,
                         dtype="uint8")
        canvas = self._canvas_append(canvas = canvas,
                                    add_point = (0,0),
                                    img = img)
        return canvas

    def import_images_from_directory(self, root_path):
        """
        directly import all the images class under root_path
        arg:
          root_path: the root path loading images
        """
        for label in sorted(os.listdir(root_path)):
            if label == "background" or label == ".ipynb_checkpoints" or label == ".DS_Store":
              continue
            for img in os.listdir(os.path.join(root_path, label)):
                try:
                    if label == "arteriole":
                        self.add_label(new_label = label)
                        self.add_image(img = os.path.join(root_path, label, img),
                                      label = label,
                                      original_image_size = False,
                                      size = (250,250),
                                      pre_determined_size = True
                                      )
                    elif label == "artery":
                        self.add_label(new_label = label)
                        self.add_image(img = os.path.join(root_path, label, img),
                                      label = label,
                                      original_image_size = False,
                                      size = (700,700),
                                      pre_determined_size = True
                                      )
                    elif label == "glomerulus":
                        self.add_label(new_label = label)
                        self.add_image(img = os.path.join(root_path, label, img),
                                      label = label,
                                      original_image_size = False,
                                      size = (700,700),
                                      pre_determined_size = True
                                      )
                    elif label == "proximal_tubule":
                        self.add_label(new_label = label)
                        self.add_image(img = os.path.join(root_path, label, img),
                                      label = label,
                                      original_image_size = False,
                                      size = (250,250),
                                      pre_determined_size = True
                                      )
                    elif label == "distal_tubule":
                        self.add_label(new_label = label)
                        self.add_image(img = os.path.join(root_path, label, img),
                                      label = label,
                                      original_image_size = False,
                                      size = (700,700),
                                      pre_determined_size = True
                                      )
                #else:
                #    self.add_image(img = os.path.join(root_path, label, img),
                #                  label = label,
                #                  original_image_size = True)
                except:
                  continue

    def import_images_from_directory_original_size(self, root_path):
        """
        directly import all the images class under root_path
        arg:
          root_path: the root path loading images
        """
        for label in sorted(os.listdir(root_path)):
            if label == "background" or label == ".ipynb_checkpoint" or label == ".DS_Store":
              continue

            for img in os.listdir(os.path.join(root_path, label)):
                try:
                    if label in ["arteriole", "artery", "glomerulus","proximal_tubule","distal_tubule"]:
                        self.add_label(new_label = label)
                        self.add_image(img = os.path.join(root_path, label, img),
                                       label = label,
                                       original_image_size = True
                                       )
                except:
                  continue
