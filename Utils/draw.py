import plotly.graph_objects as go
from numpy import random


class DrawTool:

    def __init__(self,surface_size):
        # initialize the figure
        self.fig = go.Figure()

        # set the x and y axis limits
        self.fig.update_layout(
            xaxis=dict(range=[0, surface_size]),
            yaxis=dict(range=[0, surface_size])
        )

    @staticmethod
    def random_hex_color():
        # generate a random color in HEX format
        return '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def random_rgba_color(alpha=0.2):
        # generate a random color in RGBA format."""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'rgba({r}, {g}, {b}, {alpha})'

    def draw_point(self,point,label = "",color = 'red') -> None:
        # add a point to the graph
        self.fig.add_trace(go.Scatter(
            x=[point.x],
            y=[point.y],
            mode='markers+text',
            marker=dict(size=10, color=color),
            name = label
        ))


    # draw polygon in figure,
    def draw_convex_hulls(self,points,convex_hull,label) -> None:

        # extract points coordinates
        x_cords, y_cords = zip(*[(point.x, point.y) for point in points])
        # plot the group of points
        self.fig.add_trace(go.Scatter(
            x=x_cords,
            y=y_cords,
            mode='markers',
            showlegend=False,
            marker=dict(size=5, color=self.random_hex_color())
        ))

        # extract convex hull coordinates
        hull_x, hull_y = convex_hull.exterior.xy

        #Fill the convex hull area
        self.fig.add_trace(go.Scatter(
            x=tuple(hull_x),
            y=tuple(hull_y),
            mode='lines',
            fill='toself',
            fillcolor=self.random_rgba_color(),
            line=dict(color=self.random_hex_color()),
            name = label
        ))


    def show(self) -> None:
        # Show the plot
        self.fig.show()


    def draw_line_between_points(self,point_a,point_b) -> None:

        # unpack the points into x and y coordinates
        x_values = [point_a.x, point_b.x]
        y_values = [point_a.y, point_b.y]

        # plot the line and the points using Plotly
        self.fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines',
            line=dict(color='blue', dash='dash'),  # Line style
            marker=dict(size=8, color='blue'),  # Marker style
            name='Line between Points'
        ))

