# An efficient multi-robot path planning solution using A* and coevolutionary algorithms
This repository contains the code used for the proposal and experimentation of the article entitled *An efficient multi-robot path planning solution using A* and coevolutionary algorithms*. The article is available for open reading both on the publisher's website ([https://doi.org/10.3233/ICA-220695](https://doi.org/10.3233/ICA-220695) and in the University of Oviedo Repository ([http://hdl.handle.net/10651/67799](http://hdl.handle.net/10651/67799)).

## Authors
- Enol García González
  - Computer Science Department. University of Oviedo. Spain.
  - Mail: [garciaenol@uniovi.es](mailto:garciaenol@uniovi.es)
  - Website: [https://enolgargon.me](https://enolgargon.me)
- José R. Villar
  - Computer Science Department. University of Oviedo. Spain.
  - Corresponding Author. Main: [villarjose@uniovi.es](mailto:villarjose@uniovi.es)
- Qing Tan
  - School of Computing and Information Systems. Athabasca University. Canada
- Javier Sedano
  - Instituto Tecnológico de Castilla y León. Burgos. Spain
- Camelia Chira
  - Department of Computer Science. Babes Boliay University. Romania

## Abstract
Multi-robot path planning has evolved from research to real applications in warehouses and other domains; the knowledge on this topic is reflected in the large amount of related research published in recent years on international journals. The main focus of existing research relates to the generation of efficient routes, relying the collision detection to the local sensory system and creating a solution based on local search methods. This approach implies the robots having a good sensory system and also the computation capabilities to take decisions on the fly. In some controlled environments, such as virtual labs or industrial plants, these restrictions overtake the actual needs as simpler robots are sufficient. Therefore, the multi-robot path planning must solve the collisions beforehand. This study focuses on the generation of efficient collision-free multi-robot path planning solutions for such controlled environments, extending our previous research. The proposal combines the optimization capabilities of the A* algorithm with the search capabilities of co-evolutionary algorithms. The outcome is a set of routes, either from A* or from the co-evolutionary process, that are collision-free; this set is generated in real-time and makes its implementation on edge-computing devices feasible. Although further research is needed to reduce the computational time, the computational experiments performed in this study confirm a good performance of the proposed approach in solving complex cases where well-known alternatives, such as M* or WHCA, fail in finding suitable solutions.

## Cite it
If you use this code in your research, please cite it as follows:

```
García, Enol; Villar, Jose; Tan, Qing; Sedano, Javier; Chira, Camelia. ‘An Efficient Multi-robot Path Planning Solution Using A* and Coevolutionary Algorithms’. 1 Jan. 2023 : 41 – 52.
```

Also, here you can find the citation in BibTex format:

```
@Article{García2023,
author={Garc{\'i}a, Enol
and Villar, Jos{\'e} R.
and Tan, Qing
and Sedano, Javier
and Chira, Camelia},
title={An efficient multi-robot path planning solution using A* and coevolutionary algorithms},
journal={Integrated Computer-Aided Engineering},
year={2023},
publisher={IOS Press},
volume={30},
pages={41-52},
keywords={Multi-robot path planning; A* algorithm; evolutionary algorithms; co-evolutionary algorithms},
issn={1875-8835},
doi={10.3233/ICA-220695},
url={https://doi.org/10.3233/ICA-220695}
}
```