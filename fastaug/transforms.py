import numpy as np
import cv2


from .data import img_shape_checker
from .data import KeyPoints
from .base_transforms import BaseTransform, MatrixTransform


class RandomFlip(BaseTransform):
    """
    Performs a random flip of an image.

    """
    def __init__(self, p=0.5, axis=1):
        super(RandomFlip, self).__init__(p=p)
        self.__axis = axis

    def sample_transform(self):
        pass

    @img_shape_checker
    def _apply_img(self, img):
        img = cv2.flip(img, self.__axis)
        return img

    def _apply_mask(self, mask):
        mask_new = cv2.flip(mask, self.__axis)
        return mask_new

    def _apply_labels(self, labels):
        return labels

    def _apply_pts(self, pts):
        # We should guarantee that we do not change the original data.
        pts_data = pts.data.copy()
        if self.__axis == 0:
            pts_data[:, 1] = pts.H - 1 - pts_data[:, 1]
        if self.__axis == 1:
            pts_data[:, 0] = pts.W - 1 - pts_data[:, 0]
        return KeyPoints(pts=pts_data, H=pts.H, W=pts.W)


class RandomRotate(MatrixTransform):
    """
    Random rotation around the center.
    """
    def __init__(self, rotation_range, padding='z', interpolation='bilinear', p=0.5):
        """
        Constructor.

        Parameters
        ----------
        rotation_range : rotation range
        p : probability of using this transform
        """
        super(RandomRotate, self).__init__(interpolation=interpolation, padding=padding, p=p)

        self.__range = rotation_range

    def sample_transform(self):
        """
        Samples random rotation within specified range and saves it as an object state.

        """
        rot = np.random.uniform(self.__range[0], self.__range[1])
        M = np.array([np.cos(np.deg2rad(rot)), -np.sin(np.deg2rad(rot)), 0,
                     np.sin(np.deg2rad(rot)), np.cos(np.deg2rad(rot)), 0,
                     0, 0, 1
                     ]).reshape((3, 3)).astype(np.float32)

        self.state_dict = {'rot': rot, 'transform_matrix': M}


class RandomShear(MatrixTransform):
    """
    Random shear around the center.

    """
    def __init__(self, range_x, range_y, interpolation='bilinear', padding='z', p=0.5):
        """
        Constructor.

        Parameters
        ----------
        range_x : shearing range along X-axis
        range_y : shearing range along Y-axis
        p : probability of using the transform
        """
        super(RandomShear, self).__init__(p=p, padding=padding, interpolation=interpolation)
        if range_x is None:
            range_x = 1
        if range_y is None:
            range_y = 1

        if str(range_x).isdigit():
            range_x = (range_x, range_x)

        if str(range_y).isdigit():
            range_y = (range_x, range_y)

        self.__range_x = range_x
        self.__range_y = range_y

    def sample_transform(self):
        shear_x = np.random.uniform(self.__range_x[0], self.__range_x[1])
        shear_y = np.random.uniform(self.__range_y[0], self.__range_y[1])

        M = np.array([1, shear_y, 0,
                     shear_x, 1, 0,
                     0, 0, 1]).reshape((3, 3)).astype(np.float32)

        self.state_dict = {'shear_x': shear_x, 'shear_y': shear_y, 'transform_matrix': M}


class RandomScale(MatrixTransform):
    """
    Random scale transform.

    """
    def __init__(self, range_x=None, range_y=None, interpolation='bilinear', p=0.5):
        super(RandomScale, self).__init__(p=p, interpolation=interpolation, padding=None)
        if range_x is None:
            range_x = 1
        if range_y is None:
            range_y = 1

        if str(range_x).isdigit():
            range_x = (range_x, range_x)

        if str(range_y).isdigit():
            range_y = (range_x, range_y)

        self.__range_x = range_x
        self.__range_y = range_y

    def sample_transform(self):
        scale_x = np.random.uniform(self.__range_x[0], self.__range_x[1])
        scale_y = np.random.uniform(self.__range_y[0], self.__range_y[1])

        M = np.array([scale_x, 0, 0,
                      0, scale_y, 0,
                      0, 0, 1]).reshape((3, 3)).astype(np.float32)

        self.state_dict = {'scale_x': scale_x, 'scale_y': scale_y, 'transform_matrix': M}


class RandomCrop(BaseTransform):
    def __init__(self, crop_size, pad=None):
        super(RandomCrop, self).__init__(p=1)
        self.crop_size = crop_size

    def sample_transform(self):
        raise NotImplementedError

    @img_shape_checker
    def _apply_img(self, img):
        raise NotImplementedError

    def _apply_mask(self, mask):
        raise NotImplementedError

    def _apply_labels(self, labels):
        return labels

    def _apply_pts(self, pts):
        raise NotImplementedError


class RandomPerspective(MatrixTransform):
    def __init__(self, tilt_range, p=0.5):
        super(RandomPerspective, self).__init__(p)
        self.__tilt_range = tilt_range

    def sample_transform(self):
        raise NotImplementedError


class Pad(BaseTransform):
    def __init__(self, pad_to):
        super(Pad, self).__init__(p=1)
        self.__pad_to = pad_to

    def sample_transform(self):
        pass

    @img_shape_checker
    def _apply_img(self, img):
        raise NotImplementedError

    def _apply_mask(self, mask):
        raise NotImplementedError

    def _apply_labels(self, labels):
        return labels

    def _apply_pts(self, pts):
        raise NotImplementedError


class CenterCrop(BaseTransform):
    def __init__(self, crop_size):
        super(CenterCrop, self).__init__(p=1)
        self.crop_size = crop_size

    def sample_transform(self):
        pass

    @img_shape_checker
    def _apply_img(self, img):
        raise NotImplementedError

    def _apply_mask(self, mask):
        raise NotImplementedError

    def _apply_labels(self, labels):
        raise NotImplementedError

    def _apply_pts(self, pts):
        raise NotImplementedError

