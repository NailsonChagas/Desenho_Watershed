from matplotlib import cm
import numpy as np
import cv2

img = cv2.imread("./img/road.jpg")
img_copy = np.copy(img)
marker_image = np.zeros(img.shape[:2], dtype=np.int32)
segments = np.zeros(img.shape, dtype=np.uint8)

def create_rgb(i):
    """
    1: azul claro
    2: verde
    3: azul escuro
    4: salmão
    5: cinza azulado
    6: roza claro
    7: cinza
    8: azul esverdeado
    9: amarelo
    0: laranja
    """
    x = np.array(cm.tab10(i))[:3]*255
    return tuple(x)

colors = []
for i in range(10):
    colors.append(create_rgb(i))

n_markers = 10 #0 a 9
current_marker = 1
marks_updated = False

def mouse_callback(event, x, y, flags, param):
    global marks_updated
        
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(marker_image, (x,y), 10, (current_marker), -1)
        cv2.circle(img_copy, (x,y), 10, colors[current_marker], -1)
        marks_updated = True

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', mouse_callback)

while True:
    cv2.imshow('Watershed', segments)
    cv2.imshow('Image', img_copy)

    k = cv2.waitKey(1)
        
    #fechar
    if k == 27: break #space

    #limpar cores
    if k == ord('c'): 
        img_copy = img.copy()
        marker_image = np.zeros(img.shape[0:2], dtype=np.int32)
        segments = np.zeros(img.shape,dtype=np.uint8)
        
    #atualizar cores
    if k > 0 and chr(k).isdigit():
        current_marker = int(chr(k))

    #atualizar marks
    if marks_updated:
        marker_image_copy = marker_image.copy()
        cv2.watershed(img, marker_image_copy)
            
        segments = np.zeros(img.shape,dtype=np.uint8)

        for color_idx in range(n_markers):
            segments[marker_image_copy==(color_idx)] = colors[color_idx]
        marks_updated = False
cv2.destroyAllWindows()