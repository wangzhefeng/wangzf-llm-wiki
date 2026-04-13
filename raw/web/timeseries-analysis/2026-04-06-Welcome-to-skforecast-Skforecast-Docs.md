---
author:
- null
- '[[Joaquin Amat Rodrigo and Javier Escobar Ortiz]]'
created: 2026-04-06
created_at: 2026-04-06
description: Python library for time series forecasting using machine learning models.
  It works with any estimator compatible with the scikit-learn API, including popular
  options like LightGBM, XGBoost, CatBoost, Keras, and many others.
source_type: web
status: inbox
tags:
- null
- clippings
title: Welcome to skforecast - Skforecast Docs
source_url: https://skforecast.org/0.20.0/index.html
published_at: null
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

## Welcome to skforecast

![](https://skforecast.org/0.20.0/img/banner-landing-page-skforecast.png#only-light) ![](https://skforecast.org/0.20.0/img/banner-landing-page-dark-mode-skforecast-no-background.png#only-dark)

## About The Project

**Skforecast** is a Python library for time series forecasting using machine learning models. It works with any estimator compatible with the scikit-learn API, including popular options like LightGBM, XGBoost, CatBoost, Keras, and many others.

### Why use skforecast?

Skforecast simplifies time series forecasting with machine learning by providing:

- **Seamless integration** with any scikit-learn compatible estimator (e.g., LightGBM, XGBoost, CatBoost, etc.).
- **Flexible workflows** that allow for both single and multi-series forecasting.
- **Comprehensive tools** for feature engineering, model selection, hyperparameter tuning, and more.
- **Production-ready models** with interpretability and validation methods for backtesting and realistic performance evaluation.

Whether you're building quick prototypes or deploying models in production, skforecast ensures a fast, reliable, and scalable experience.

### Get Involved

We value your input! Here are a few ways you can participate:

- **Report bugs** and suggest new features on our [GitHub Issues page](https://github.com/skforecast/skforecast/issues).
- **Contribute** to the project by [submitting code](https://github.com/skforecast/skforecast/blob/master/CONTRIBUTING.md), adding new features, or improving the documentation.
- **Share your feedback** on LinkedIn to help spread the word about skforecast!

Together, we can make time series forecasting accessible to everyone. Discover more in our [contribution guide](https://github.com/skforecast/skforecast/blob/master/CONTRIBUTING.md)

## Installation & Dependencies

To install the basic version of `skforecast` with core dependencies, run the following:

```bash
pip install skforecast
```

For more installation options, including dependencies and additional features, check out our [Installation Guide](https://skforecast.org/0.20.0/quick-start/how-to-install).

## Forecasters

A **Forecaster** object in the skforecast library is a comprehensive **container that provides essential functionality and methods** for training a forecasting model and generating predictions for future points in time.

The **skforecast** library offers a **variety of forecaster** types, each tailored to specific requirements such as single or multiple time series, direct or recursive strategies, or custom predictors. Regardless of the specific forecaster type, all instances share the same API.

| Forecaster | Single series | Multiple series | Recursive strategy | Direct strategy | Probabilistic prediction | Time series differentiation | Exogenous features | Window features |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ForecasterRecursive](https://skforecast.org/0.20.0/user_guides/autoregressive-forecaster) | ✔️ |  | ✔️ |  | ✔️ | ✔️ | ✔️ | ✔️ |
| [ForecasterDirect](https://skforecast.org/0.20.0/user_guides/direct-multi-step-forecasting) | ✔️ |  |  | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| [ForecasterRecursiveMultiSeries](https://skforecast.org/0.20.0/user_guides/independent-multi-time-series-forecasting) |  | ✔️ | ✔️ |  | ✔️ | ✔️ | ✔️ | ✔️ |
| [ForecasterDirectMultiVariate](https://skforecast.org/0.20.0/user_guides/dependent-multi-series-multivariate-forecasting) |  | ✔️ |  | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| [ForecasterRnn](https://skforecast.org/0.20.0/user_guides/forecasting-with-deep-learning-rnn-lstm) | ✔️ | ✔️ |  | ✔️ | ✔️ |  | ✔️ |  |
| [ForecasterStats](https://skforecast.org/0.20.0/user_guides/forecasting-sarimax-arima) | ✔️ |  | ✔️ |  | ✔️ | ✔️ | ✔️ |  |
| [ForecasterRecursiveClassifier](https://skforecast.org/0.20.0/user_guides/autoregressive-classification-forecasting) | ✔️ |  | ✔️ |  | ✔️ |  | ✔️ | ✔️ |
| [ForecasterEquivalentDate](https://skforecast.org/0.20.0/user_guides/forecasting-baseline) | ✔️ |  | ✔️ |  | ✔️ |  |  |  |

## Features

Skforecast provides a set of key features designed to make time series forecasting with machine learning easy and efficient. For a detailed overview, see the [User Guides](https://skforecast.org/0.20.0/user_guides/table-of-contents).

## Examples and tutorials

Explore our extensive list of examples and tutorials (English and Spanish) to get you started with skforecast. You can find them [here](https://skforecast.org/0.20.0/examples/examples_english).

## How to contribute

Primarily, skforecast development consists of adding and creating new *Forecasters*, new validation strategies, or improving the performance of the current code. However, there are many other ways to contribute:

- Submit a bug report or feature request on [GitHub Issues](https://github.com/skforecast/skforecast/issues).
- Contribute a Jupyter notebook to our [examples](https://skforecast.org/0.20.0/examples/examples_english).
- Write [unit or integration tests](https://docs.pytest.org/en/latest/) for our project.
- Answer questions on our issues, Stack Overflow, and elsewhere.
- Translate our documentation into another language.
- Write a blog post, tweet, or share our project with others.

For more information on how to contribute to skforecast, see our [Contribution Guide](https://github.com/skforecast/skforecast/blob/master/CONTRIBUTING.md).

Visit our [About section](https://skforecast.org/0.20.0/more/about-skforecast) to meet the people behind **skforecast**.

## Citation

If you use skforecast for a scientific publication, we would appreciate citations to the published software.

**Zenodo**

```js
Amat Rodrigo, Joaquin, & Escobar Ortiz, Javier. (2026). skforecast (v0.20.0). Zenodo. https://doi.org/10.5281/zenodo.8382787
```

**APA**:

```js
Amat Rodrigo, J., & Escobar Ortiz, J. (2026). skforecast (Version 0.20.0) [Computer software]. https://doi.org/10.5281/zenodo.8382787
```

**BibTeX**:

```js
@software{skforecast,
  author  = {Amat Rodrigo, Joaquin and Escobar Ortiz, Javier},
  title   = {skforecast},
  version = {0.20.0},
  month   = {2},
  year    = {2026},
  license = {BSD-3-Clause},
  url     = {https://skforecast.org/},
  doi     = {10.5281/zenodo.8382787}
}
```

### Publications citing skforecast

- Chamara Hewage, H., Rostami-Tabar, B., Syntetos, A., Liberatore, F., and Milano, G., “A Novel Hybrid Approach to Contraceptive Demand Forecasting: Integrating Point Predictions with Probabilistic Distributions”, *arXiv e-prints*, Art. no. arXiv:2502.09685, 2025. doi:10.48550/arXiv.2502.09685.
- Kuthe, S., Persson, C. and Glaser, B. (2025), Physics-Informed Data-Driven Prediction of Submerged Entry Nozzle Clogging with the Aid of Ab Initio Repository. steel research int. 2400800. https://doi.org/10.1002/srin.202400800
- Chatzikonstantinidis, K., Afxentiou, N., Giama, E., Fokaides, P. A., & Papadopoulos, A. M. (2025). Energy management of smart buildings during crises and digital twins as an optimisation tool for sustainable urban environment. International Journal of Sustainable Energy, 44(1). https://doi.org/10.1080/14786451.2025.2455134
- Sanan, O., Sperling, J., Greene, D., & Greer, R. (2024, April). Forecasting Weather and Energy Demand for Optimization of Renewable Energy and Energy Storage Systems for Water Desalination. In 2024 IEEE Conference on Technologies for Sustainability (SusTech) (pp. 175-182). IEEE. [https://doi.org/10.1109/SusTech60925.2024.10553570](https://doi.org/10.1109/SusTech60925.2024.10553570)
- Bojer, A. K., Biru, B. H., Al-Quraishi, A. M. F., Debelee, T. G., Negera, W. G., Woldesillasie, F. F., & Esubalew, S. Z. (2024). Machine learning and remote sensing based time series analysis for drought risk prediction in Borena Zone, Southwest Ethiopia. Journal of Arid Environments, 222, 105160. [https://doi.org/10.1016/j.jaridenv.2024.105160](https://doi.org/10.1016/j.jaridenv.2024.105160)
- V. Negri, A. Mingotti, R. Tinarelli and L. Peretto, "Comparison Between the Machine Learning and the Statistical Approach to the Forecasting of Voltage, Current, and Frequency," 2023 IEEE 13th International Workshop on Applied Measurements for Power Systems (AMPS), Bern, Switzerland, 2023, pp. 01-06, doi: 10.1109/AMPS59207.2023.10297192. [https://doi.org/10.1109/AMPS59207.2023.10297192](https://doi.org/10.1109/AMPS59207.2023.10297192)
- Marcillo Vera, F., Rosado, R., Zambrano, P., Velastegui, J., Morales, G., Lagla, L., & Herrera, A. (2024). Forecasting con Python, caso de estudio: visitas a las redes sociales en Ecuador con machine learning. CONECTIVIDAD, 5(2), 15-29.
- [OUKHOUYA, H., KADIRI, H., EL HIMDI, K., & GUERBAZ, R. (2023). Forecasting International Stock Market Trends: XGBoost, LSTM, LSTM-XGBoost, and Backtesting XGBoost Models. Statistics, Optimization & Information Computing, 12(1), 200-209.](https://doi.org/10.37431/conectividad.v5i2.126) [https://doi.org/10.19139/soic-2310-5070-1822](https://doi.org/10.19139/soic-2310-5070-1822)
- DUDZIK, S., & Kowalczyk, B. (2023). Prognozowanie produkcji energii fotowoltaicznej z wykorzystaniem platformy NEXO i VRM Portal. Przeglad Elektrotechniczny, 2023(11). doi:10.15199/48.2023.11.41
- Polo J, Martín-Chivelet N, Alonso-Abella M, Sanz-Saiz C, Cuenca J, de la Cruz M. Exploring the PV Power Forecasting at Building Façades Using Gradient Boosting Methods. Energies. 2023; 16(3):1495. [https://doi.org/10.3390/en16031495](https://doi.org/10.3390/en16031495)
- Popławski T, Dudzik S, Szeląg P. Forecasting of Energy Balance in Prosumer Micro-Installations Using Machine Learning Models. Energies. 2023; 16(18):6726. [https://doi.org/10.3390/en16186726](https://doi.org/10.3390/en16186726)
- Harrou F, Sun Y, Taghezouit B, Dairi A. Artificial Intelligence Techniques for Solar Irradiance and PV Modeling and Forecasting. Energies. 2023; 16(18):6731. [https://doi.org/10.3390/en16186731](https://doi.org/10.3390/en16186731)
- Amara-Ouali, Y., Goude, Y., Doumèche, N., Veyret, P., Thomas, A., Hebenstreit, D.,... & Phe-Neau, T. (2023). Forecasting Electric Vehicle Charging Station Occupancy: Smarter Mobility Data Challenge. arXiv preprint arXiv:2306.06142.
- Emami, P., Sahu, A., & Graf, P. (2023). BuildingsBench: A Large-Scale Dataset of 900K Buildings and Benchmark for Short-Term Load Forecasting. arXiv preprint arXiv:2307.00142.
- Dang, HA., Dao, VD. (2023). Building Power Demand Forecasting Using Machine Learning: Application for an Office Building in Danang. In: Nguyen, D.C., Vu, N.P., Long, B.T., Puta, H., Sattler, KU. (eds) Advances in Engineering Research and Application. ICERA 2022. Lecture Notes in Networks and Systems, vol 602. Springer, Cham. [https://doi.org/10.1007/978-3-031-22200-9\_32](https://doi.org/10.1007/978-3-031-22200-9_32)
- Morate del Moral, Iván (2023). Predición de llamadas realizadas a un Call Center. Proyecto Fin de Carrera / Trabajo Fin de Grado, E.T.S.I. de Sistemas Informáticos (UPM), Madrid.
- Lopez Vega, A., & Villanueva Vargas, R. A. (2022). Sistema para la automatización de procesos hospitalarios de control para pacientes para COVID-19 usando machine learning para el Centro de Salud San Fernando.
- García Álvarez, J. D. (2022). Modelo predictivo de rentabilidad de criptomonedas para un futuro cercano.
- Chilet Vera, Á. (2023). Elaboración de un algoritmo predictivo para la reposición de hipoclorito en los depósitos mediante técnicas de Machine Learning (Doctoral dissertation, Universitat Politècnica de València).
- Bustinza Barrial, A. A., Bautista Abanto, A. M., Alva Alfaro, D. A., Villena Sotomayor, G. M., & Trujillo Sabrera, J. M. (2022). Predicción de los valores de la demanda máxima de energía eléctrica empleando técnicas de machine learning para la empresa Nexa Resources–Cajamarquilla.
- Morgado, K. Desarrollo de una técnica de gestión de activos para transformadores de distribución basada en sistema de monitoreo (Doctoral dissertation, Universidad Nacional de Colombia).
- Zafeiriou A., Chantzis G., Jonkaitis T., Fokaides P., Papadopoulos A., 2023, Smart Energy Strategy - A Comparative Study of Energy Consumption Forecasting Machine Learning Models, Chemical Engineering Transactions, 103, 691-696.

## Donating

If you found **skforecast** useful, you can support us with a donation. Your contribution will help us **continue developing, maintaining, and improving** this project. Every contribution, no matter the size, makes a difference. **Thank you for your support!**

[![Buy me a coffee skforecast](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=skforecast&button_colour=f79939&font_colour=000000&font_family=Poppins&outline_colour=000000&coffee_colour=FFDD00)](https://www.buymeacoffee.com/skforecast "Buy me a coffee skforecast")  
[![Become a GitHub Sponsor](https://skforecast.org/0.20.0/img/github_sponsor_button.png)](https://github.com/sponsors/JoaquinAmatRodrigo "Become a GitHub Sponsor")  
[![Become a GitHub Sponsor](https://skforecast.org/0.20.0/img/github_sponsor_button.png)](https://github.com/sponsors/JavierEscobarOrtiz "Become a GitHub Sponsor")  

[![paypal](https://www.paypalobjects.com/en_US/ES/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=D2JZSWRLTZDL6)

## License

**Skforecast software**: [BSD-3-Clause License](https://github.com/skforecast/skforecast/blob/master/LICENSE)

**Skforecast documentation**: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Trademark**: The trademark skforecast is registered with the European Union Intellectual Property Office (EUIPO) under the application number 019109684. Unauthorized use of this trademark, its logo, or any associated visual identity elements is strictly prohibited without the express consent of the owner.