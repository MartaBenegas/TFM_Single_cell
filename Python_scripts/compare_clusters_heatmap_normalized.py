from pathlib import Path
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb


A_FPATH = Path("/home/marta/Descargas/SEURAT/10x/clust_identity_zumis.txt")
B_FPATH = Path("/home/marta/Descargas/SEURAT/10x/clust_identity_cellranger.txt")

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
   
    #sort dictionary by clust
    clusters = OrderedDict(sorted(clusters.items(), key=lambda t: t[0]))

    return clusters


def compare_clusters(a_clusters, b_clusters):
    sim_file = open("sim_btw_clusters_norm.txt", "w")
    sim_file.write("z_cluster\tcr_cluster\tsimilarity\n")
    array = []
    for a_clust, a_set in a_clusters.items():
        sims = []
        for b_clust, b_set in b_clusters.items():
            intersection = len( a_set.intersection(b_set) )
            sim = float(intersection/len(b_set))
            sims.append(sim)
            line = a_clust + "\t" + b_clust + "\t" + str(sim) + "\n"
            sim_file.write(line)
        array.append(sims)
    
    return array



def sim_heatmap(sim_array):
    sim_array = np.array(sim_array)
    hmap = sb.heatmap(sim_array, annot=True, cbar_kws={'label':'similarity'})
    plt.xlabel("Cell Ranger clusters") # B clusters
    plt.ylabel("zUMIs clusters") # A clusters 
    hmap.figure.savefig("heatmap_norm_col.png")     


def main():
    Aclust_fpath = A_FPATH
    Bclust_fpath = B_FPATH
    a_clusters = cluster_dictionary(Aclust_fpath, cr = False)
    b_clusters = cluster_dictionary(Bclust_fpath, cr = True)
    sim_array = compare_clusters(a_clusters, b_clusters)
    sim_heatmap(sim_array)

main()
