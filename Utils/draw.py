import matplotlib.pyplot as plt


class DrawTool:

    def __init__(self,surface_size):
        # Initialize the figure and axes inside the constructor
        self.plt = plt
        self.fig, self.ax = plt.subplots()

        # Set the x and y axis limits
        self.ax.set_xlim(0, surface_size)
        self.ax.set_ylim(0, surface_size)

    def draw_point(self,point,label = ""):

        # plot the point
        self.ax.plot(point.x,point.y,'o',label = label)

        # Add text label near the point
        self.ax.text(point.x, point.y, label, fontsize=12, ha='right')

    # draw polygon in figure,
    def draw_convex_hulls(self,points,convex_hull):
        # Plot the group of points
        x, y = zip(*[(point.x, point.y) for point in points])
        self.ax.plot(x, y, '.', label='Points Group 1')

        hull1_x, hull1_y = convex_hull.exterior.xy
        self.ax.plot(hull1_x, hull1_y, 'r--', label='Convex Hull Group 1')
        self.ax.fill(hull1_x, hull1_y, 'r', alpha=0.2)

    def show(self):
        # Show the plot
        self.plt.show()


    def draw_line_between_points(self,point_a,point_b):

        # Unpack the points into x and y coordinates
        x_values = [point_a[0], point_b[0]]
        y_values = [point_a[1], point_b[1]]
        # Plot the points and the line
        plt.plot(x_values, y_values, 'bo--')

