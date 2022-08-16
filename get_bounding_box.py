from matplotlib.widgets import RectangleSelector
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img

# image = img.imread('00001.jpg')
# from matplotlib.widgets import RectangleSelector
# import numpy as np
# import matplotlib.pyplot as plt


bounds = []

def line_select_callback(eclick, erelease):

    # Callback for line selection.
    # *eclick * and * erelease *
    # are the press and release events.
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    bounds.append([x1, y1, x2, y2])
    print("(% 3.2f, % 3.2f) --> (% 3.2f, % 3.2f)" % (x1, y1, x2, y2))
    # print(" The button you used were: % s % s" % (eclick.button,
                                                #   erelease.button))
    


def toggle_selector(event):

    print(' Key pressed.')

    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)


def get_bounding_box(image):

    # make a new plotting range
    fig, current_ax = plt.subplots()

    plt.xticks([])
    plt.yticks([])
    plt.title("Draw a rectangle to the scan area, then exit this window")
    plt.imshow(image)

    print("\n      click  -->  release")

    # drawtype is 'box' or 'line' or 'none'
    toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                        drawtype ='box',
                                        useblit = True,
                                        button =[1, 3],  # don't use middle button
                                        minspanx = 5, minspany = 5,
                                        spancoords ='pixels',
                                        interactive = True)

    plt.connect('key_press_event', toggle_selector)

    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()

    plt.show()
    print(bounds)
    return(bounds[-1])
    print(f" your bounds are {bounds[-1]}")
