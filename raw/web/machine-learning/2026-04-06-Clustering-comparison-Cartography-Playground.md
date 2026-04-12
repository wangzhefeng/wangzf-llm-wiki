---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: Compare the centroid-based clustering method k-Means and the density
  based method DBSCAN.
source_type: web
status: inbox
tags:
- null
- clippings
title: Clustering comparison | Cartography Playground
topics:
- 知识库建设
source_url: https://cartography-playground.gitlab.io/playgrounds/clustering-comparison/
published_at: null
related_concepts: []
---

## Clustering comparison

---

On this page the centroid-based clustering method *k-Means* will be compared to the density-based clustering method *DBSCAN*.

k-Means was introduced by James MacQueen in 1967. It aims to partition all observations in to k clusters so that the within-cluster sum of squares is minimized while the between-cluster sum of squares is maximized.

DBSCAN or **D** ensity- **b** ased **s** patial **c** lustering of **a** pplications with **n** oise was introduced in 1996 by Martin Ester, Hans-Peter Kriegel, Jörg Sander and Xiaowei Xu. It forms clusters of closely neighboring points and is able to detect outliers as noise.

## Algorithms

---

### k-Means

The k-Means Algorithm is based on the method of least squares and optimizes F=k∑i=1∑xj∈Si∥∥xj−μi∥∥2 
$$
F=∑i=1k∑xj∈Si‖xj−μi‖2
$$
 
$$
F = \sum_{i=1}^{k}\sum_{x_{j} \in S_{i}}\left \| x_{j} - \mu_{i} \right \|^{2}
$$
 where xi $xi$ $x_i$ are data points, μi $μi$ $\mu_i$ are Centroids or Means and Si $Si$ $S_i$ are corresponding clusters.  
The Algorithm has three steps.

**1\. Initialisation**  
Choose k $k$ $k$ Centroids (also called Means)  
m(0)1,⋯,m(0)k $m1(0),⋯,mk(0)$ $m_1^{(0)},\cdots,m_k^{(0)}$

![[kmeans_1.svg|kmeans initialisation]]

**2\. Assign Points**  
Each data Point is assigned to the "nearest" cluster (cluster variance is increased the least).  
S(t)i={xj:∥∥xj−m(t)i∥∥2≤∥∥xj−m(t)i∗∥∥2 for all i∗=1,⋯,k} $Si(t)={xj:‖xj−mi(t)‖2≤‖xj−mi∗(t)‖2 for all i∗=1,⋯,k}$ $S_i^{\left( t \right)} = \left\{ x_j : \left\| x_j - m_{i}^{\left( t \right)} \right\|^2 \leq \left\| x_j - m_{i^*}^{\left( t \right)} \right\|^2 \text{ for all } i^*=1,\cdots,k \right\}$

![[kmeans_2.svg|kmeans assign points]]

**3\. Update Centroids**  
Recalculate the new cluster means.  
m(t+1)i=1∣∣S(t)i∣∣∑xj∈S(t)ixj $mi(t+1)=1|Si(t)|∑xj∈Si(t)xj$ $m_i^{\left( t+1 \right)} = \frac{1}{\left| S_{i}^{\left( t \right)} \right|} \sum_{x_j \in S_{i}^{\left( t \right)}} x_j$

![[kmeans_3.svg|kmeans update centroids]]

Repeat steps 2 and 3 until the centroids don't change anymore.

![[kmeans_4.svg|kmeans iteration]]

### DBSCAN

In DBSCAN there are three different kinds of points:

- **core points** which are dense themselfs
- **density-reachable points** that are reachable from core points but are not dense themselfs
- **outliers** or noise points

The DBSCAN method has two parameters *ε* and *minPts*, where *ε* is the maximum neigborhood radius and *minPts* is the minimum number of neighbors to be a core point.

From one point another point is reachable if their distance is smaller than *ε*. A Point is dense (=core point) if it has at least *minPts* in its *ε* -reachable neighborhood.

Density-reachable points are reachable from core points but are not themselfs dense.

All reachable points around at least one core point form a cluster. Other points are outliers.

<svg xmlns="http://www.w3.org/2000/svg" width="330" height="240" viewBox="0 0 165 120" class="figure-img img-fluid"><g fill-opacity="0.25"><circle cx="44" cy="30" r="30" fill="#e37222"></circle><circle cx="135" cy="90" r="30" fill="#e37222"></circle><circle cx="30" cy="85" r="30" fill="#a2ad00"></circle><circle cx="132" cy="70" r="30" fill="#a2ad00"></circle><g><circle cx="48" cy="76" r="30" fill="#0065bd"></circle><circle cx="68" cy="88" r="30" fill="#0065bd"></circle><circle cx="90" cy="80" r="30" fill="#0065bd"></circle><circle cx="66" cy="69" r="30" fill="#0065bd"></circle><circle cx="88" cy="62" r="30" fill="#0065bd"></circle><circle cx="108" cy="69" r="30" fill="#0065bd"></circle></g></g><g><circle cx="44" cy="30" r="3.5" fill="#e37222"></circle><circle cx="135" cy="90" r="3.5" fill="#e37222"></circle><circle cx="30" cy="85" r="3.5" fill="#a2ad00"></circle><circle cx="132" cy="70" r="3.5" fill="#a2ad00"></circle><g><circle cx="48" cy="76" r="3.5" fill="#0065bd"></circle><circle cx="68" cy="88" r="3.5" fill="#0065bd"></circle><circle cx="90" cy="80" r="3.5" fill="#0065bd"></circle><circle cx="66" cy="69" r="3.5" fill="#0065bd"></circle><circle cx="88" cy="62" r="3.5" fill="#0065bd"></circle><circle cx="108" cy="69" r="3.5" fill="#0065bd"></circle></g></g><g><g><g><line x1="134.4" y1="28.73" x2="163.6" y2="28.73" fill="none" stroke="#343a40"></line><rect x="134" y="26.13" width="0.8" height="5.2" fill="#343a40"></rect><rect x="163.2" y="26.13" width="0.8" height="5.2" fill="#343a40"></rect></g><text transform="translate(146.76 26.6)" font-size="12" fill="#0065bd" font-family="RobotoMono-Italic, Roboto Mono, monospace" font-style="italic">ε</text> </g><text transform="translate(100 13)" font-size="12"><tspan fill="#343a40" font-family="RobotoMono-Italic, Roboto Mono, monospace" font-style="italic" letter-spacing="-0.06em">minPts:</tspan><tspan x="57" y="0" fill="#0065bd" font-family="RobotoMono-Regular, Roboto Mono, sans-serif">3</tspan></text></g></svg>

blue: core points, green: density-reachable points, orange: outliers

**Algorithm**

1. Start with arbitrary, not yet visited point
2. Get the point's *ε* -neighborhood
3. If the point is dense, start a cluster
4. If not, the point is labeled as noise (it can get part of a cluster later)
5. Get the *ε* -neighborhood of all unvisited points in the cluster and add them to the cluster
6. Again add the *ε* -neighborhood of the neighbors to the cluster if the neighbor is dense itself
7. Continue until the density-connected cluster is completely found
8. Start with a new unvisited point
9. Continue until all points are either part of a cluster or labeled as noise

Advantages of DBSCAN over k-Means

- DBSCAN does not require a priori knowled about the number of classes
- DBSCAN can separate arbitrarily shaped and non-linearly separable clusters
- DBSCAN is robust against noise

Disadvantages of DBSCAN

- One has to understand the data to choose meaningful parameters
- DBSCAN has difficulties at clustering datasets with large differences in densities
- DBSCAN is not entirely deterministic (Assignment of points reachable from more than one cluster is dependant on the processing order)

## Hands-On

---

There are three tabs *Data*, *k-Means* and *DBSCAN*.  
In the *Data* tab you can toggle to draw own data points by clicking in the drawing area below, you can load random and predefined datasets and clear the drawing area.  
In the *k-Means* tab you can change the configuration of k-Means by adding own centroids, adding a number of random centroids and clearing all centroids. In addition you can change the distance measure. Then you can run the k-Means algorithm either step by step or in a loop.  
In the *DBSCAN* tab you can change the parameters *ε* and *minPts* and choose the distance measure. Then you can perform the classification and clear the clustering again.  
Each cluster is displayed in its own color. Outliers are displayed white with gray outline.

## References

---

- [Jakub Młokosiewicz: *k-means-visualization on GitHub*, April 2018](https://github.com/hckr/k-means-visualization)
- [Wikipedia: *k-means clustering*, April 2018](https://en.wikipedia.org/wiki/K-means_clustering)
- [James MacQueen: *Some methods for classification and analysis of multivariate observations*, 1967](https://projecteuclid.org/euclid.bsmsp/1200512992)
- [Corneliu Sugar: *jDBSCAN on GitHub*, April 2018](https://github.com/upphiminn/jDBSCAN)
- [Wikipedia: *DBSCAN*, April 2018](https://en.wikipedia.org/wiki/DBSCAN)
- [Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu: *A density-based algorithm for discovering clusters in large spatial databases with noise*, 1996](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.121.9220)