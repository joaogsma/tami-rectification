import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button
import sys
from line_builder import Line_Builder
from point import Point
from rectification import remove_projective_distortion
from rectification import stratified_metric_rect
from scipy import misc

## Close window and change progress in code
def press(event):
    print('press', event.key)
    if event.key == 'enter':
        plt.close()

# =============================================================================
# ============================== LOAD THE IMAGE ===============================
# =============================================================================
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Click to build line segments')

f = misc.imread(sys.argv[1], mode = 'RGB')

(row_num, col_num, _) = f.shape
# -----------------------------------------------------------------------------



# =============================================================================
# ==================== CREATE LISTENERS FOR POINT CAPTURE =====================
# =============================================================================
line_builder = Line_Builder(fig, ax, 8, col_num, row_num)
# -----------------------------------------------------------------------------


fig.canvas.set_window_title('Original Image')
fig.canvas.mpl_connect('key_press_event', press)
plt.imshow(f)
plt.show()


# =============================================================================
# ========================= COMPUTE THE INFINITY LINE =========================
# =============================================================================
(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16) = line_builder.get_points()

(line1, line2, line3, line4, line5, line6, line7, line8) = line_builder.get_lines()

# Compute points in the Infinity Line
PF1 = line1.cross(line2)
PF2 = line3.cross(line4)

# Compute the Infinity Line
horizon = PF1.cross(PF2)
horizon.normalize()
# -----------------------------------------------------------------------------



# =============================================================================
# ============================= UPDATE THE IMAGE ==============================
# =============================================================================
p1_px = p1.get_pixel_coord(col_num, row_num)
p2_px = p2.get_pixel_coord(col_num, row_num)
p3_px = p3.get_pixel_coord(col_num, row_num)
p4_px = p4.get_pixel_coord(col_num, row_num)
p5_px = p5.get_pixel_coord(col_num, row_num)
p6_px = p6.get_pixel_coord(col_num, row_num)
p7_px = p7.get_pixel_coord(col_num, row_num)
p8_px = p8.get_pixel_coord(col_num, row_num)

pf1_px = PF1.get_pixel_coord(col_num, row_num)
pf2_px = PF2.get_pixel_coord(col_num, row_num)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(p1_px[1] , p1_px[0], c='r')
ax.scatter(p2_px[1] , p2_px[0], c='r')
ax.plot( [p1_px[1], p2_px[1]], [p1_px[0], p2_px[0]], color="r", linewidth=2.0)
ax.scatter(p3_px[1] , p3_px[0], c='r')
ax.scatter(p4_px[1] , p4_px[0], c='r')
ax.plot( [p3_px[1], p4_px[1]], [p3_px[0], p4_px[0]], color="r", linewidth=2.0)

ax.plot( [p2_px[1], pf1_px[1]], [p2_px[0], pf1_px[0]], "r--", linewidth=2.0)
ax.plot( [p4_px[1], pf1_px[1]], [p4_px[0], pf1_px[0]], "r--", linewidth=2.0)

ax.scatter(p5_px[1] , p5_px[0], c='g')
ax.scatter(p6_px[1] , p6_px[0], c='g')
ax.plot( [p5_px[1], p6_px[1]], [p5_px[0], p6_px[0]], color="g", linewidth=2.0)
ax.scatter(p7_px[1] , p7_px[0], c='g')
ax.scatter(p8_px[1] , p8_px[0], c='g')
ax.plot( [p7_px[1], p8_px[1]], [p7_px[0], p8_px[0]], color="g", linewidth=2.0)

ax.plot( [p6_px[1], pf2_px[1]], [p6_px[0], pf2_px[0]], "g--", linewidth=2.0)
ax.plot( [p8_px[1], pf2_px[1]], [p8_px[0], pf2_px[0]], "g--", linewidth=2.0)


# Draw the horizon (Infinity Line)
ax.scatter(pf1_px[1] , pf1_px[0], c='b')
ax.scatter(pf2_px[1] , pf2_px[0], c='b')
ax.plot( [pf1_px[1], pf2_px[1]], [pf1_px[0], pf2_px[0]], color="b")
fig.canvas.set_window_title('Original Image with Infinity Line')
fig.canvas.mpl_connect('key_press_event', press)
plt.imshow(f)
plt.show()
# -----------------------------------------------------------------------------



# =============================================================================
# ============================== RECTIFICATION ================================
# =============================================================================
f_ = remove_projective_distortion(f, [(line1, line2), (line3, line4)])
# -----------------------------------------------------------------------------
fig = plt.figure()
fig.canvas.set_window_title('Removed Projective Distortion')
fig.canvas.mpl_connect('key_press_event', press)
plt.imshow(f_)
plt.show()


# =============================================================================
# ============================== STRATIFIED_METRIC_RECT ================================
# =============================================================================
f__ = stratified_metric_rect(f, [(line1, line2), (line3, line4)], [(line5, line6), (line7, line8)])
# -----------------------------------------------------------------------------
fig = plt.figure()
fig.canvas.set_window_title('Stratified Metric Rectification')
fig.canvas.mpl_connect('key_press_event', press)
plt.imshow(f__)
plt.show()