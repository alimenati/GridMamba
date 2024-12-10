# <center>PowerMamba</center>

This repository contains the code and resources for the research project *"PowerMamba: A Deep State Space Model and Comprehensive Benchmark for Time Series Prediction in Electric Power Systems."*

The architecture and performance of our prediction model are presented in the following figures:


<div style="text-align: center;">
    <img src="pics/PowerMamba_arc.png" alt="PowerMamba Model">
</div>

PowerMamba outperforms current benchmarks in all prediction tasks. 

<img src="pics/without_pred.png" alt="Prediction results without external forecasts">
<img src="pics/With_pred.png" alt="Comparing prediction results with and without external forecasts">
<div style="text-align: center; margin-top: 20px;">
    <img src="pics/parameters.png" alt="at">
    <img src="pics/context.png" alt="at">
</div>



## Getting Started

To set up the required environment, follow these steps:

```bash
conda env create -f environment.yml
conda activate mamba4ts
```

## Repository Overview

- **`PowerMamba`**: Contains the implementation of the proposed PowerMamba model along with baseline models.
- **`data`**: Includes the benchmark dataset used in this project.

Each folder contains a `README` file with more details about its contents.

# Maintainers
* [Ali Menati](https://scholar.google.com/citations?user=HPreuloAAAAJ&hl=en&oi=ao)
* [Fatemeh Doudi](https://fatemehdoudi.github.io/)



## Acknowledgement

We appreciate the following github repos very much for the valuable code base:
- Mamba (https://github.com/state-spaces/mamba)
- Time-Series-Library (https://github.com/thuml/Time-Series-Library)
- TimeMachine (https://github.com/Atik-Ahamed/TimeMachine)
- PatchTST (https://github.com/yuqinie98/PatchTST)
- iTransformer (https://github.com/thuml/iTransformer)
- Autoformer (https://github.com/thuml/Autoformer)
- TimesNet (https://github.com/thuml/TimesNet)
- DLinear (https://github.com/cure-lab/LTSF-Linear)

# Citation

If you find our codebase, dataset, or research valuable, please cite PowerMamba:

```
@misc{menati2024powermamba,      title={PowerMamba: A Deep State Space Model and Comprehensive Benchmark for Time Series Prediction in Electric Power Systems}, 
      author={Ali Menati and Fatemeh Doudi and Dileep Kalathil and Le Xie},      year={2024},
      eprint={2412.06112},      archivePrefix={arXiv},
      primaryClass={cs.LG},      url={https://arxiv.org/abs/2412.06112}, 
}
```


