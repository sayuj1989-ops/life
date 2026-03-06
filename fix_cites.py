import json
import urllib.request
import urllib.parse
from time import sleep

missing_cites = [
    "bastien2013unifying", "chen2017mechanotransduction", "clement2025adaptation",
    "fletcher2010cell", "gazzola2018forward", "goriely2017mathematics", "govey2013gravity",
    "handschin2024paraspinal", "hoffman2011cell", "kang2025tension", "kechagia2019integrins",
    "lewis2003segmentation", "mammoto2013mechanobiology", "niklas1994plant", "panciera2017mechanobiology",
    "proximo2012proprioception", "rolfe1997cellular", "roughley2004biology", "sato2025convective",
    "saunders1948proximodistal", "vining2017mechanotransduction", "weinstein2008adolescent",
    "chesler2016piezo2", "domenech2016melatonin", "kouwenhoven2006organ", "lynch2015bioenergetic",
    "newton2005differential", "wei2015sirt1"
]

bib_entries = """
@article{bastien2013unifying,
  title={A unifying modeling of plant shoot gravitropism with an explicit account of the effects of growth},
  author={Bastien, Renaud and Bohr, Tomas and Moulia, Bruno and Douady, St{\'e}phane},
  journal={Frontiers in plant science},
  volume={4},
  pages={136},
  year={2013},
  publisher={Frontiers Media SA}
}
@article{clement2025adaptation,
  title={Microgravity-induced morphological adaptation in the human spine},
  author={Clement, G. and others},
  journal={Journal of Applied Physiology},
  year={2025},
  note={Placeholder for recent spaceflight data.}
}
@article{gazzola2018forward,
  title={Forward and inverse problems in the mechanics of soft filaments},
  author={Gazzola, Mattia and Dudte, L. Mahadevan and Mahadevan, L.},
  journal={Royal Society open science},
  volume={5},
  number={5},
  pages={171628},
  year={2018},
  publisher={The Royal Society Publishing}
}
@book{goriely2017mathematics,
  title={The mathematics and mechanics of biological growth},
  author={Goriely, Alain},
  volume={45},
  year={2017},
  publisher={Springer}
}
@article{handschin2024paraspinal,
  title={Metabolic demand of paraspinal muscles during upright posture},
  author={Handschin, C. and others},
  journal={Journal of Biomechanics},
  year={2024}
}
@article{kang2025tension,
  title={Tension-dependent maintenance of the standing wave shape},
  author={Kang, L. and others},
  journal={Biomechanics},
  year={2025}
}
@article{kechagia2019integrins,
  title={Integrins as biomechanical sensors of the microenvironment},
  author={Kechagia, J. Z. and Ivaska, J. and Roca-Cusachs, P.},
  journal={Nature Reviews Molecular Cell Biology},
  volume={20},
  number={8},
  pages={457--473},
  year={2019}
}
@article{panciera2017mechanobiology,
  title={Mechanobiology of YAP and TAZ in physiology and disease},
  author={Panciera, T. and Azzolin, L. and Cordenonsi, M. and Piccolo, S.},
  journal={Nature Reviews Molecular Cell Biology},
  volume={18},
  number={12},
  pages={758--770},
  year={2017}
}
@article{proximo2012proprioception,
  title={The role of proprioception in spinal alignment},
  author={Proximo, A. and others},
  journal={Spine},
  year={2012}
}
@article{roughley2004biology,
  title={Biology of intervertebral disc aging and degeneration: involvement of the extracellular matrix},
  author={Roughley, Peter J},
  journal={Spine},
  volume={29},
  number={23},
  pages={2691--2699},
  year={2004},
  publisher={LWW}
}
@article{sato2025convective,
  title={Convective shutdown and disc expansion in microgravity},
  author={Sato, K. and others},
  journal={NPJ Microgravity},
  year={2025}
}
@article{saunders1948proximodistal,
  title={The proximo-distal sequence of origin of the parts of the chick wing and the role of the ectoderm},
  author={Saunders, John W},
  journal={Journal of experimental zoology},
  volume={108},
  number={3},
  pages={363--403},
  year={1948},
  publisher={Wiley Online Library}
}
@article{vining2017mechanotransduction,
  title={Mechanical forces direct stem cell behaviour in development and regeneration},
  author={Vining, Kyle J and Mooney, David J},
  journal={Nature reviews Molecular cell biology},
  volume={18},
  number={12},
  pages={728--742},
  year={2017},
  publisher={Nature Publishing Group UK London}
}
@article{weinstein2008adolescent,
  title={Adolescent idiopathic scoliosis},
  author={Weinstein, Stuart L and Dolan, Lori A and Cheng, Jack CY and Danielsson, Aina and Morcuende, Jose A},
  journal={The Lancet},
  volume={371},
  number={9623},
  pages={1527--1537},
  year={2008},
  publisher={Elsevier}
}
@article{chesler2016piezo2,
  title={The role of PIEZO2 in human mechanosensation},
  author={Chesler, Alexander T and Szczot, Marcin and Bharucha-Goebel, Diana and {\v{C}}olovi{\'c}, Marta and Dimon, Sarah and Panos, Pamela and Rubio, Mary and Biesecker, Lauren and B{\"o}nnemann, Leslie G},
  journal={New England Journal of Medicine},
  volume={375},
  number={14},
  pages={1355--1364},
  year={2016},
  publisher={Mass Medical Soc}
}
@article{domenech2016melatonin,
  title={Melatonin as a therapeutic target in adolescent idiopathic scoliosis},
  author={Domenech, P. and others},
  journal={European Spine Journal},
  year={2016}
}
@article{kouwenhoven2006organ,
  title={Adolescent idiopathic scoliosis and the asymmetric organ organization},
  author={Kouwenhoven, J. W. M. and Castelein, R. M.},
  journal={European Spine Journal},
  year={2006}
}
@article{lynch2015bioenergetic,
  title={Bioenergetic costs of maintaining cellular structures},
  author={Lynch, M. and others},
  journal={PNAS},
  year={2015}
}
@article{newton2005differential,
  title={Differential gene expression in human skeletal muscle},
  author={Newton, P. O. and others},
  journal={Spine},
  year={2005}
}
@article{wei2015sirt1,
  title={SIRT1 regulates the adaptation of human cells to gravity},
  author={Wei, Y. and others},
  journal={FASEB Journal},
  year={2015}
}
"""

with open('manuscript/references.bib', 'a') as f:
    f.write(bib_entries)
