import tkinter as tk
from tkinter import ttk
import time
from shot import Shot, Match
import numpy as np
import cv2, math
import tempfile


class AnalysisFrame(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.container = container

        # field options
        options = {"padx": 5, "pady": 0}

    def drawSeries(self):
        series = self.parent.match
        scheibentyp = self.parent.match.scheibentyp
        radiusTen = Match.radius_dict[scheibentyp][0]
        radiusInnerTen = Match.radius_dict[scheibentyp][1]
        incrementRing = Match.radius_dict[scheibentyp][2]
        radiusBlack = Match.radius_dict[scheibentyp][3]
        radiusCalibre = Match.radius_dict[scheibentyp][4]

        w = 2 * (radiusTen + 9 * incrementRing)
        scale = 400 / w
        center_coordinates = (w / 2, w / 2)
        image = np.zeros((400, 400, 1), np.float64)
        max_x = max([abs(s.x) for s in series])
        max_y = max([abs(s.y) for s in series])
        radius_worst = (max_x**2 + max_y**2) ** 0.5 + radiusCalibre
        rangemin = max(int((w / 2 - radius_worst) * scale + 0.5), 0)
        rangemax = min(int((w / 2 + radius_worst) * scale + 0.5), int(w * scale + 0.5))
        for i in range(rangemin, rangemax + 1):
            for j in range(rangemin, rangemax + 1):
                for e in series:
                    distance = math.sqrt(
                        (i - (e.y + center_coordinates[1]) * scale) ** 2
                        + (j - (e.x + center_coordinates[0]) * scale) ** 2
                    )

                    image[399 - i, j] += math.exp(
                        -((distance / (0.75 * radiusCalibre * scale)) ** 2)
                    )

        # return image[rangemin:rangemax, rangemin:rangemax]

        normimage = cv2.normalize(
            image[rangemin:rangemax, rangemin:rangemax],
            None,
            0,
            255,
            cv2.NORM_MINMAX,
            cv2.CV_8UC1,
        )
        cv2.imshow("title", normimage)
        color_image = cv2.applyColorMap(normimage, cv2.COLORMAP_JET)
        cv2.imshow("title1", color_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def reset(self, back=False):
        self.parent.back_button["state"] = "normal"
        self.parent.ok_button["state"] = "disabled"
        self.drawSeries()
