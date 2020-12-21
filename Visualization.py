from matplotlib import colors
from matplotlib import pyplot


def visualize(board):


    colormap = colors.ListedColormap(["white", "black"])
    pyplot.imshow(board,cmap=colormap)
    pyplot.show()
