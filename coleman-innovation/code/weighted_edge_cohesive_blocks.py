#!/usr/bin/env python

import numpy as np
import igraph as ig
import edgecohblks.blocking as ecb
from edgecohblks.ks.ksgraph import Graph

# load data
network = 'ckm'
netout = 'ckm_weighted'
g = ig.Graph.Read(f'../processed/{network}.graphml', 'graphml')

# build edges
g.es['wgt'] = (~np.isnan(g.es['advice'])).astype(int) + (~np.isnan(g.es['discussion'])).astype(int) + (~np.isnan(g.es['friend'])).astype(int)
# g.es['advice'] = ~np.isnan(g.es['advice'])
# g.es['discussion'] = ~np.isnan(g.es['discussion'])
# g.es['friend'] = ~np.isnan(g.es['friend'])
el = []
for e in g.es:
    el.append((e.source, e.target, e['wgt']))

gks = Graph(el)

blocks, parent, cohesion, blksedgecuts = ecb.edge_blocking(gks, debug=True)

blks = process_blocks(blocks, parent, cohesion,
                      blksedgecuts, debug=True)
header = "Coleman Innovation"
graph_str = "Coleman Innovation"
report_blocking_results(header, graph_str, blocks,
                        parent, cohesion, blksedgecuts)
replace_assigned_ids(blks, gks)
draw_hierarchy(blks, f'{netout}.dot')
blks = mark_bad_blocks(blks)
draw_hierarchy(blks, f'{netout}_badblks.dot', markbadblks=True)
pruned_blks = prune_blocks(blks, debug=True)
draw_hierarchy(pruned_blks, f'{netout}_pruned.dot', prunebadblks=True)
hier = vz.hierarchy_graph(pruned_blks)
ig_g = g.to_igraph()
vz_blks = vz.Blocks(pruned_blks).blks
vz.mark_blocks(ig_g, g, vz_blks)
vz.assign_klevel_embeddedness_to_nodes(ig_g, g, vz_blks, debug=True)
cbl.assign_property_to_hierarchy(hier, vz_blks)
cbl.assign_labels_to_hierarchy(hier)
vz.serialize(f'{netout}.pickle', ig_g, vz_blks, hier)
cbl.block_plot(block_file=f'{netout}.pickle', title='Coleman Innovation Combined Weighted', outfile=f'{netout}_layout.pdf',
               verbose=1)
