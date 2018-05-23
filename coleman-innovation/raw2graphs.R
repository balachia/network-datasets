#!/usr/bin/env Rscript

library(igraph)
library(data.table)

.n <- 246
.header <- 9
.types <- c('advice', 'discussion', 'friend')

datafile = 'raw/ckm.dat'

# read in data
dat <- matrix(scan(datafile, skip=.header), ncol=.n, byrow=TRUE)

# check for correct number of observations
stopifnot(dim(dat) == c(3*.n, .n))

# extract separate networks
nets <- lapply(seq_along(.types), function(i) {
    g <- graph_from_adjacency_matrix(dat[(i-1)*.n + (1:.n), ])
    g <- set_edge_attr(g, .types[i], value=1)
    g
})
names(nets) <- .types

# combine networks
g <- do.call(union, nets)

dir.create('processed', showWarnings=FALSE)
for(type in .types) {
    write_graph(nets[[type]], sprintf('processed/%s.csv', type))
}

# write combined, but drop edge attributes
write_graph(g, 'processed/ckm.csv')

