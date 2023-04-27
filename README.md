<h1 align="left">Triconnectivity</h1>

<p>
  <a href="https://github.com/scornz/triconnectivity/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://github.com/psf/black" target="_blank">
    <img alt="Code Style: black" src="https://img.shields.io/badge/Code style-black-black.svg" />
  </a>
  <a href="https://github.com/scornz" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/GitHub-@scornz-blue.svg" />
  </a>
  <a href="https://linkedin.com/in/mscornavacca" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/LinkedIn-@mscornavacca-blue.svg" />
  </a>
</p>

> A set of generic implementations for finding $3$-edge-connected and $3$-vertex-connected components in a graph (implemented in Python). Made for junior-year independent work for Princeton University's COS Department.

## Abstract

This paper explores the implementation and application of a well known $3$-edge-connectivity algorithm. We use Tsin's algorithm to analyze, in linear time, the connectivity of essential networks [[1](#1)]. This includes state-wide road networks, distributed systems, and even the structure of the Internet. Implementations and applications of $3$-edge-connectivity are relatively unexplored, and this paper aims to fill a gap in the surrounding academic literature through rigorous explanation and demonstration.

## Requirements

- Python 3.9 ([download](https://www.python.org/downloads/)) or PyPy ([download](https://www.pypy.org/download.html))
- `pipenv` (call `pip install pipenv` globally)

## Setup

1.  Ensure requirements are installed correctly.
2.  Navigate to project folder.
3.  Call `pipenv install` to install required `pip` packages into the virtual environment.
4.  Prosper.

## 📝 License

Copyright © 2023 [Mike Scornavacca](https://github.com/scornz).<br />
This project is [MIT](https://github.com/scornz/triconnectivity/blob/main/LICENSE) licensed.

## References

[<a id="1">1</a>]
Y. H. Tsin, “A Simple 3-Edge-Connected Component Algorithm,” Theory Comput Syst, vol. 40, no. 2, pp. 125–142, Feb. 2007, doi: 10.1007/s00224-005-1269-4.
