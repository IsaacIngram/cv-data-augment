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
    Represents a potential direction of a flip.
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


def main():
    img = cv2.imread('IMG_2386.jpeg')
    bb_2386 = BoundingBox(122, 373, 550, 651)
    bb_color = (0, 0, 255)
    bb_thickness = 3


    cv2.rectangle(img, bb_2386.get_start_point(), bb_2386.get_end_point(), bb_color, bb_thickness)
    cv2.imshow("Before", img)

    img_after, bb_after = flip(img, [bb_2386], FlipDirection.VERTICAL_AND_HORIZONTAL)

    cv2.rectangle(img, bb_after[0].get_start_point(), bb_after[0].get_end_point(), bb_color, bb_thickness)
    cv2.imshow("After", img_after)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # bbox = cv2.selectROI("Select", img, fromCenter=False, showCrosshair=True)
    # x, y, w, h = bbox
    # print(f"Box coordinates: x={x}, y={y}, w={w}, h={h}")




if __name__ == '__main__':
    main()