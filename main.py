###############################################################################
#
# Author: Isaac Ingram
#
###############################################################################
from pathlib import Path
from enum import Enum
from typing import List, Tuple
import cv2


def get_img_width_height(img) -> Tuple[int, int]:
    """
    Get the width and height of an OpenCV image
    :param img: OpenCV image object
    :return: Tuple of width and height (integers)
    """
    height, width = img.shape[:2]
    return width, height


class BoundingBox:
    """
    Represents a bounding box.

    Coordinates are written such that the top left of the image is (0,0).
    Coordinates (x,y) and width and height are all in pixels.
    """

    x: int
    y: int
    width: int
    height: int


    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_start_point(self) -> Tuple[int, int]:
        return self.x, self.y

    def get_end_point(self) -> Tuple[int, int]:
        return self.x + self.width, self.y + self.height


class FlipDirection(Enum):
    """
    Represents directions of a flip.
    VERTICAL = upside down
    HORIZONTAL = left-right mirror
    VERTICAL_AND_HORIZONTAL = both upside down and left-right mirror
    """
    VERTICAL = 0 # upside down
    HORIZONTAL = 1 # left-right mirror
    VERTICAL_AND_HORIZONTAL = -1 # both upside down and left-right mirror


def flip(img, bounding_boxes: List[BoundingBox], direction: FlipDirection):
    """
    Flip an image and its bounding boxes
    :param img: OpenCV image to flip
    :param bounding_boxes: List of bounding boxes to flip
    :param direction: Direction/type of flip
    :return: Tuple of (new image, list of bounding boxes)
    """
    width, height = get_img_width_height(img)
    flipped_img = cv2.flip(img, direction.value)
    for bounding_box in bounding_boxes:
        if direction == FlipDirection.VERTICAL or direction == FlipDirection.VERTICAL_AND_HORIZONTAL:
            bounding_box.y = height - bounding_box.y
        if direction == FlipDirection.HORIZONTAL or direction == FlipDirection.VERTICAL_AND_HORIZONTAL:
            bounding_box.x = width - bounding_box.x
    return flipped_img, bounding_boxes


class RotateBasicDirection(Enum):
    """
    Represents directions of a basic rotation.
    CLOCKWISE_90
    COUNTERCLOCKWISE_90
    ROTATE_180
    """
    CLOCKWISE_90 = cv2.ROTATE_90_CLOCKWISE
    COUNTERCLOCKWISE_90 = cv2.ROTATE_90_COUNTERCLOCKWISE
    ROTATE_180 = cv2.ROTATE_180


def rotate_basic(img, bounding_boxes: List[BoundingBox], direction: RotateBasicDirection):
    """
    Apply a basic rotation to an image and its bounding boxes, rotating it in 90 degree increments.
    :param img: OpenCV image to flip
    :param bounding_boxes: List of bounding boxes to flip
    :param direction: Rotation type of flip
    :return: Tuple of (new image, list of bounding boxes)
    """
    width, height = get_img_width_height(img)
    rotate_code = direction.value
    flipped_img = cv2.rotate(img, rotate_code)

    for bounding_box in bounding_boxes:
        if direction == RotateBasicDirection.CLOCKWISE_90:
            # Calculate new coordinates
            new_x = height - bounding_box.y + bounding_box.height
            new_y = width - bounding_box.x + bounding_box.width
            # Store width/height for swap
            new_bb_width = bounding_box.height
            new_bb_height = bounding_box.width
        elif direction == RotateBasicDirection.COUNTERCLOCKWISE_90:
            # Calculate new coordinates
            new_x = bounding_box.y
            new_y = bounding_box.x
            # Store width/height for swap
            new_bb_width = bounding_box.height
            new_bb_height = bounding_box.width
        else: # direction == ROTATE_180
            new_x = width - bounding_box.x - bounding_box.width
            new_y = height - bounding_box.y - bounding_box.height
            new_bb_width = bounding_box.width
            new_bb_height = bounding_box.height

        # Assign new bounding box
        bounding_box.x = new_x
        bounding_box.y = new_y
        bounding_box.height = new_bb_height
        bounding_box.width = new_bb_width

    return flipped_img, bounding_boxes


def main():
    img = cv2.imread('IMG_2386.jpeg')
    bb_2386 = BoundingBox(122, 373, 550, 651)
    bb_color = (0, 0, 255)
    bb_thickness = 3


    cv2.rectangle(img, bb_2386.get_start_point(), bb_2386.get_end_point(), bb_color, bb_thickness)
    cv2.imshow("Before", img)

    # img_after, bb_after = flip(img, [bb_2386], FlipDirection.VERTICAL_AND_HORIZONTAL)
    img_after, bb_after = rotate_basic(img, [bb_2386], RotateBasicDirection.CLOCKWISE_90)

    cv2.rectangle(img, bb_after[0].get_start_point(), bb_after[0].get_end_point(), bb_color, bb_thickness)
    cv2.imshow("After", img_after)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # bbox = cv2.selectROI("Select", img, fromCenter=False, showCrosshair=True)
    # x, y, w, h = bbox
    # print(f"Box coordinates: x={x}, y={y}, w={w}, h={h}")




if __name__ == '__main__':
    main()