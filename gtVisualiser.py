from pprint import pprint
import graph_tool.all as gt

g = gt.load_graph("visGraph.dot")  # Load a DOT file

# g = gt.collection.ns["ego_social/facebook_combined"]

# pprint(g.vp.vertex_name)

state = gt.minimize_blockmodel_dl(g)

state.draw()

# gt.graph_draw(g)
