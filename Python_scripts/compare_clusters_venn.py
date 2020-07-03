from pathlib import Path
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt
from matplotlib_venn import venn2


Z_FPATH = Path("/home/marta/Descargas/SEURAT/10x/clust_identity_zumis.txt")
CR_FPATH = Path("/home/marta/Descargas/SEURAT/10x/clust_identity_cellranger.txt")

def cluster_dictionary(fpath, cr):
    clusters = defaultdict(list)
    file = open(fpath)

    # clusters = { clust:[cells in that cluster] }
    first = True
    for line in file:
        if first:
            first = False
            continue
        line = line.strip().split()
        if cr: cell, clust = line[0][1:-3], line[1][1:-1]
        else: cell, clust = line[0][1:-1], line[1][1:-1]
        clusters[clust].append(cell)

    #sort cells list for each cluster
    for clust, cells in clusters.items():
        clusters[clust] = set(sorted(cells))

    clusters = OrderedDict(sorted(clusters.items(), key=lambda t: t[0]))

    return clusters


def compare_clusters(z_clusters, cr_clusters):
    sim_file = open("sim_btw_clusters.txt", "w")
    sim_file.write("z_cluster\tcr_cluster\tsimilarity\n")
    for zclust, zset in z_clusters.items():
        for crclust, crset in cr_clusters.items():
            intersection = len( zset.intersection(crset) )
            union = len( zset.union(crset) )
            sim = float(intersection/union)
            line = zclust + "\t" + crclust + "\t" + str(sim) + "\n"
            sim_file.write(line)


def venn_diagrams(z_clusters, cr_clusters):
    for zclust, zset in z_clusters.items():
        best_sim, best_clust = 0, ""
        sec_sim, sec_clust = 0, ""
        for crclust, crset in cr_clusters.items():
            intersection = len( zset.intersection(crset) )
            union = len( zset.union(crset) )
            sim = float(intersection/union)
            if sim > best_sim:
                best_sim, best_clust = sim, crclust
#            elif sim > sec_sim:
#                sec_sim, sec_clust = sim, crclust
        best_set = cr_clusters[best_clust]
        venn2(subsets = (len(zset.difference(best_set)),len(best_set.difference(zset)), len(zset.intersection(best_set))), set_labels=("zUMIs","Cell Ranger"))
        plot_name = "{}_{}_venn.png".format(zclust, best_clust)
        plt.savefig(plot_name)
        plt.close()
#        if best_sim < 0.5:
#            sec_set = cr_clusters[sec_clust]
#            venn2(subsets = (len(zset.difference(sec_set)),len(sec_set.difference(zset)), len(zset.intersection(sec_set))), set_labels=("zUMIs","CellRanger"))
#            plot_name = "{}_{}_venn_second.png".format(zclust, sec_clust)
#            plt.savefig(plot_name)
#            plt.close() 



def main():
    Zclust_fpath = Z_FPATH
    CRclust_fpath = CR_FPATH
    z_clusters = cluster_dictionary(Zclust_fpath, cr = False)
    cr_clusters = cluster_dictionary(CRclust_fpath, cr = True)
    compare_clusters(z_clusters, cr_clusters)
    venn_diagrams(z_clusters, cr_clusters)


main()
