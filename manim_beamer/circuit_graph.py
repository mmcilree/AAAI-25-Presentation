from manim import *
from .constants import *
from math import sin, cos, sqrt


# Copied from Stackoverflow
def get_intersections(p0, r0, p1, r1):
    # circle 1: (x0, y0), radius r0
    x0 = p0[0]
    y0 = p0[1]

    # circle 2: (x1, y1), radius r1
    x1 = p1[0]
    y1 = p1[1]

    d = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        return None
    # One circle within other
    if d < abs(r0 - r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0**2 - r1**2 + d**2) / (2 * d)
        h = sqrt(r0**2 - a**2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        return [x3, y3, 0], [x4, y4, 0]


class LoopableEdge(VMobject):

    def __init__(self, start, end, loop_direction=UP, path_arc=None, **kwargs):
        super().__init__()
        self._loop_direction = loop_direction
        self._start_vertex = start
        self._end_vertex = end

        if start != end:
            if path_arc is not None:
                # Calculate nicer start and end points for edge arc by intersecting with the radii
                # of the vertices
                arc = ArcBetweenPoints(
                    start.get_center(), end.get_center(), angle=path_arc
                )

                # I think stroke_width = 1 corresponds to 0.01 units of overall length
                start_points = get_intersections(
                    arc.get_arc_center(),
                    arc.radius,
                    start.get_center(),
                    start.radius - start.get_stroke_width() / 100,
                )

                end_points = get_intersections(
                    arc.get_arc_center(),
                    arc.radius,
                    end.get_center(),
                    end.radius + start.get_stroke_width() / 100,
                )

                if start_points is None:
                    start_points = [start, start]
                if end_points is None:
                    end_points = [end, end]

                if path_arc >= 0:
                    self.edge = Line(
                        start_points[1], end_points[0], path_arc=path_arc, **kwargs
                    )
                else:
                    self.edge = Line(
                        start_points[0], end_points[1], path_arc=path_arc, **kwargs
                    )

            else:
                self.edge = Line(start, end, **kwargs)
        else:
            self.edge = Line(
                start.get_boundary_point(rotate_vector(loop_direction, PI / 4)),
                start.get_boundary_point(rotate_vector(loop_direction, -PI / 4)),
                path_arc=path_arc,
                **kwargs,
            )
        self.edge.set_z_index(-1)

        start.set_z_index(1)
        end.set_z_index(1)
        self.add(self.edge)

    def add_tip(self, *args, **kwargs):
        return self.edge.add_tip(*args, **kwargs)

    def pop_tips(self, *args, **kwargs):
        return self.edge.pop_tips(*args, **kwargs)

    def grow_from_start(self, run_time=0.5):
        return GrowFromPoint(self, self._start_vertex.get_center(), run_time=run_time)

    def set_color(self, *args, **kwargs):
        return self.edge.set_color(*args, **kwargs)


class CircuitGraph(DiGraph):

    def __init__(
        self,
        vertices,
        edges,
        vertex_config=GRAPH_NODE_STYLE,
        edge_config=GRAPH_EDGE_STYLE,
        labels=True,
        layout="circular",
        edge_type=LoopableEdge,
        loop_angle=-2 * TAU / 3,
        dont_update=False,
        **kwargs
    ):

        super().__init__(
            vertices,
            edges,
            vertex_config=vertex_config,
            edge_config=edge_config,
            labels=labels,
            layout=layout,
            edge_type=edge_type,
            **kwargs,
        )

        self.loop_angle = loop_angle
        for e in edges:
            if e[0] == e[1]:
                self._edge_config[e]["path_arc"] = loop_angle
                self._edge_config[e]["loop_direction"] = (
                    self.vertices[e[0]].get_center() - self.get_center()
                )

        if not dont_update:
            self.update_edges(self)
        self.triangles = []

    def _add_edge(self, edge, edge_type, edge_config):
        if edge_config is None:
            edge_config = GRAPH_EDGE_STYLE.copy()
            edge_config["stroke_color"] = UG_BLUE

        edge_config = edge_config.copy()
        tip_config = edge_config.pop("tip_config", {})

        u, v = edge

        if u == v:
            edge_config["path_arc"] = self.loop_angle
            edge_config["loop_direction"] = (
                self.vertices[u].get_center() - self.get_center()
            )

        self._edge_config[edge] = edge_config

        self._tip_config[edge] = tip_config

        added_mobjects = []

        self._graph.add_edge(u, v)

        if edge_type is LoopableEdge:
            edge_mobject = edge_type(self[u], self[v], **self._edge_config[edge])
        else:
            edge_mobject = edge_type(
                self[u].get_center(),
                self[v].get_center(),
                z_index=-1,
                **self._edge_config[edge],
            )

        self.edges[(u, v)] = edge_mobject
        edge_mobject.add_tip(**tip_config)
        self.add(edge_mobject)
        added_mobjects.append(edge_mobject)

        return self.get_group_class()(*added_mobjects)

    def update_tips(self, graph):
        for (u, v), edge in graph.edges.items():
            tip = edge.pop_tips()[0]
            edge.add_tip(tip)

    def show_path(self, path):
        anims = []
        for e in path:
            anims.append(
                AnimationGroup(
                    self.edges[e][0]
                    .animate(run_time=0.8)
                    .set_stroke(PURE_RED)
                    .set_fill(PURE_RED)
                    .set_stroke_width(5),
                    self.vertices[e[1]]
                    .animate(run_time=0.8)
                    .set_fill(ORANGE, family=False),
                )
            )
        return LaggedStart(*anims, lag_ratio=0.8)

    def set_edge_config(self, edge, key, val):
        self._edge_config[edge][key] = val

    def reveal_endpoint(self, edge, run_time=0.5, **kwargs):
        return AnimationGroup(
            self.edges[edge].grow_from_start(run_time=run_time),
            GrowFromCenter(self[edge[1]], run_time=run_time),
        )

    def create_edges(self, edges, **kwargs):
        return AnimationGroup(*[self.edges[e].grow_from_start(**kwargs) for e in edges])

    def get_example_graph():
        edge_list = [
            (0, 1),
            (0, 4),
            (0, 7),
            (1, 2),
            (1, 3),
            (4, 5),
            (4, 6),
            (7, 8),
            (7, 9),
            (3, 2),
            (3, 1),
            (5, 4),
            (6, 5),
            (6, 4),
            (8, 7),
            (9, 8),
            (9, 7),
            (2, 1),
            (2, 0),
            (4, 0),
            (8, 3),
            (0, 9),
            (7, 0),
            (8, 6),
            (5, 3),
        ]
        graph_style = GRAPH_EDGE_STYLE.copy()
        circle_edge_config = dict(**{"path_arc": PI / 100}, **graph_style)

        tree_edge_config = {}
        backedge_list = [
            (2, 0),
            (2, 1),
            (3, 2),
            (3, 1),
            (4, 0),
            (5, 4),
            (6, 4),
            (6, 5),
            (5, 3),
            (8, 6),
            (7, 0),
            (8, 7),
            (9, 7),
            (0, 9),
            (8, 3),
            (9, 8),
        ]
        for e in edge_list:
            if e in [(2, 0), (0, 9)]:
                tree_edge_config[e] = dict(**{"path_arc": -5 * PI / 6}, **graph_style)
            elif e in [(7, 0)]:
                tree_edge_config[e] = dict(**{"path_arc": PI / 3}, **graph_style)
            elif e in [(8, 3)]:
                tree_edge_config[e] = dict(**{"path_arc": -PI / 3}, **graph_style)
            elif e in [(5, 4), (2, 1), (8, 7), (3, 2), (6, 5), (9, 8)]:
                tree_edge_config[e] = dict(**{"path_arc": -PI / 3}, **graph_style)
            elif e in [(3, 1), (5, 6), (6, 4), (8, 9), (9, 7), (4, 0)]:
                tree_edge_config[e] = dict(**{"path_arc": PI / 3}, **graph_style)
            else:
                tree_edge_config[e] = dict(**{"path_arc": PI / 100}, **graph_style)

        g = CircuitGraph(
            list(range(10)),
            edge_list,
            layout={
                0: [0, 2, 0],
                1: [-4, 0, 0],
                2: [-5, -2, 0],
                3: [-3, -2, 0],
                4: [0, 0, 0],
                5: [-1, -2, 0],
                6: [1, -2, 0],
                7: [4, 0, 0],
                8: [3, -2, 0],
                9: [5, -2, 0],
            },
            edge_config=tree_edge_config,
        )

        g.suspend_updating()
        for e in backedge_list:
            g.edges[e].set_color(GRAY)
            g.set_edge_config(e, "color", GRAY)

        behind_edges = min([g.edges[e].z_index for e in g.edges]) - 1

        g.triangles = [
            Triangle(
                fill_color=RED_A, stroke_width=0, fill_opacity=1, z_index=behind_edges
            )
            .scale(2.2)
            .move_to(center_of_mass([g[i].get_center() for i in [1, 2, 3]]))
            .shift(UP * 0.5),
            Triangle(
                fill_color=PURPLE_A,
                stroke_width=0,
                fill_opacity=1,
                z_index=behind_edges,
            )
            .scale(2.2)
            .move_to(center_of_mass([g[i].get_center() for i in [4, 5, 6]]))
            .shift(UP * 0.5),
            Triangle(
                fill_color=GREEN_A, stroke_width=0, fill_opacity=1, z_index=behind_edges
            )
            .scale(2.2)
            .move_to(center_of_mass([g[i].get_center() for i in [7, 8, 9]]))
            .shift(UP * 0.5),
        ]
        g.add(*[t for t in g.triangles])
        return g

    def get_example_graph2():
        edge_list = [
            (3, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 4),
            (4, 3),
            (4, 5),
            (5, 4),
            (5, 6),
            (2, 6),
            (6, 0),
            (6, 9),
            (3, 9),
            (9, 7),
            (9, 8),
            (8, 7),
            (7, 3),
            (7, 5),
        ]
        graph_style = GRAPH_EDGE_STYLE.copy()
        edge_config = dict(**{"path_arc": PI / 10}, **graph_style)

        for e in edge_list:
            if e in [(3, 0), (6, 9)]:
                edge_config[e] = dict(**{"path_arc": -PI / 5}, **graph_style)
            elif e in [(1, 2), (8, 7)]:
                edge_config[e] = dict(**{"path_arc": -PI / 10}, **graph_style)
            elif e in [(2, 4), (6, 0), (3, 9), (7, 5)]:
                edge_config[e] = dict(**{"path_arc": PI / 5}, **graph_style)
            elif e in [(4, 5), (5, 4)]:
                edge_config[e] = dict(**{"path_arc": PI / 3}, **graph_style)
            else:
                edge_config[e] = dict(**{"path_arc": PI / 10}, **graph_style)

        g = CircuitGraph(
            list(range(0, 10)),
            edge_list,
            layout={
                0: [0, 2.5, 0],
                1: [-1, 1.25, 0],
                2: [1, 1.25, 0],
                3: [-3.5, 0, 0],
                4: [-1, 0, 0],
                5: [1, 0, 0],
                6: [3.5, 0, 0],
                7: [-1, -1.25, 0],
                8: [1, -1.25, 0],
                9: [0, -2.5, 0],
            },
            edge_config=edge_config,
        )

        g.suspend_updating()

        return g
