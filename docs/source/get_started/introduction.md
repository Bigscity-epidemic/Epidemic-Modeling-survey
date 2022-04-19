![](/_static/logo.png)

## Introduction

[Github Homepage](https://github.com/Bigscity-epidemic/Epidemic-Modeling-survey)|[Project Introduction](https://epimodeling.work/)|[Paper List](https://github.com/Bigscity-epidemic/Bigscity-epidemic-survey-paperlist)

LibCity is a unified, comprehensive, and extensible library, which provides researchers with a credible experimental tool and a convenient development framework in the traffic prediction field. Our library is implemented based on PyTorch and includes all the necessary steps or components related to traffic prediction into a systematic pipeline, allowing researchers to conduct comprehensive experiments. Our library will contribute to the standardization and reproducibility in the field of traffic prediction.

LibCity currently supports the following tasks:

* Traffic State Prediction
  * Traffic Flow Prediction
  * Traffic Speed Prediction
  * On-Demand Service Prediction
  * Origin-destination Matrix Prediction
  * Traffic Accidents Prediction
* Trajectory Next-Location Prediction
* Estimated Time of Arrival
* Map Matching
* Road Network Representation Learning

#### Features

* **Unified**: LibCity builds a systematic pipeline to implement, use and evaluate traffic prediction models in a unified platform. We design basic spatial-temporal data storage, unified model instantiation interfaces, and standardized evaluation procedure.
* **Comprehensive**: 60 models covering 9 traffic prediction tasks have been reproduced to form a comprehensive model warehouse. Meanwhile, LibCity collects 35 commonly used datasets of different sources and implements a series of commonly used evaluation metrics and strategies for performance evaluation. 

* **Extensible**: LibCity enables a modular design of different components, allowing users to flexibly insert customized components into the library. Therefore, new researchers can easily develop new models with the support of LibCity.

#### Overall Framework

![](/_static/framework.png)

* **Configuration Module**: Responsible for managing all the parameters involved in the framework.
* **Data Module**: Responsible for loading datasets and data preprocessing operations.
* **Model Module**: Responsible for initializing the reproduced baseline model or custom model.
* **Evaluation Module**: Responsible for evaluating model prediction results through multiple indicators.
* **Execution Module**: Responsible for model training and prediction.



The LibCity is mainly developed and maintained by Beihang Interest Group on SmartCity ([BIGSCITY](https://github.com/Bigscity-epidemic/Epidemic-Modeling-survey)). The core developers of this library is [@shhh](https://github.com/shh2000). 

If you encounter a bug or have any suggestion, please contact us by sending an email to 13820618441@163.com.
