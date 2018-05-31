#!/usr/bin/env python

import igraph as ig
import edgecohblks.blocking as ecb
from edgecohblks.ks.ksgraph import Graph

# load data
g = ig.Graph.Read('../processed/ckm.csv', 'edgelist')

gks = Graph(g.get_edgelist(), autoweight=True)

blocks, parent, cohesion, blksedgecuts = ecb.edge_blocking(gks, debug=True)

blks = process_blocks(blocks, parent, cohesion,
                      blksedgecuts, debug=True)
header = "Coleman Innovation"
graph_str = "Coleman Innovation"
report_blocking_results(header, graph_str, blocks,
                        parent, cohesion, blksedgecuts)
replace_assigned_ids(blks, gks)
draw_hierarchy(blks, 'ckm.dot')
blks = mark_bad_blocks(blks)
draw_hierarchy(blks, 'ckm_badblks.dot', markbadblks=True)
pruned_blks = prune_blocks(blks, debug=True)
draw_hierarchy(pruned_blks, 'ckm_pruned.dot', prunebadblks=True)
hier = vz.hierarchy_graph(pruned_blks)
ig_g = g.to_igraph()
vz_blks = vz.Blocks(pruned_blks).blks
vz.mark_blocks(ig_g, g, vz_blks)
vz.assign_klevel_embeddedness_to_nodes(ig_g, g, vz_blks, debug=True)
cbl.assign_property_to_hierarchy(hier, vz_blks)
cbl.assign_labels_to_hierarchy(hier)
vz.serialize('ckm.pickle', ig_g, vz_blks, hier)
cbl.block_plot(block_file='ckm.pickle', title='Coleman Innovation Combined Unweighted', outfile='ckm_layout.pdf',
               verbose=1)
