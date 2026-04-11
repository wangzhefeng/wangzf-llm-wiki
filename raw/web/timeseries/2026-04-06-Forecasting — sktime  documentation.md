---
source_type: web
title: "Forecasting — sktime  documentation"
author: 
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
source_url: "https://www.sktime.net/en/latest/api_reference/forecasting.html#online-and-stream-forecasting"
published_at: null
related_concepts: []
---

## Forecasting

The `sktime.forecasting` module contains algorithms and composition tools for forecasting.

All forecasters in `sktime` can be listed using the `sktime.registry.all_estimators` utility, using `estimator_types="forecaster"`, optionally filtered by tags.

Valid tags are listed in [the forecaster tags API reference](https://www.sktime.net/en/latest/api_reference/tags.html#forecaster-tags), and can be listed using `sktime.registry.all_tags`.

A full table with tag based search is also available on the [Estimator Search Page](https://www.sktime.net/en/latest/estimator_overview.html) (select “forecaster” in the “Estimator type” dropdown).

## Base

| [`BaseForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.base.BaseForecaster.html#sktime.forecasting.base.BaseForecaster "sktime.forecasting.base.BaseForecaster") () | Base forecaster template class. |
| --- | --- |
| [`ForecastingHorizon`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.base.ForecastingHorizon.html#sktime.forecasting.base.ForecastingHorizon "sktime.forecasting.base.ForecastingHorizon") (\[values, is\_relative, freq\]) | Forecasting horizon. |

## Pipeline composition

Compositors for building forecasting pipelines. Pipelines can also be constructed using `*`, `**`, `+`, and `|` dunders.

| [`make_pipeline`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.pipeline.make_pipeline.html#sktime.pipeline.make_pipeline "sktime.pipeline.make_pipeline") (\*steps) | Create a pipeline from estimators of any type. |
| --- | --- |

| [`TransformedTargetForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.TransformedTargetForecaster.html#sktime.forecasting.compose.TransformedTargetForecaster "sktime.forecasting.compose.TransformedTargetForecaster") (steps) | Meta-estimator for forecasting transformed time series. |
| --- | --- |
| [`ForecastingPipeline`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.ForecastingPipeline.html#sktime.forecasting.compose.ForecastingPipeline "sktime.forecasting.compose.ForecastingPipeline") (steps) | Pipeline for forecasting with exogenous data. |
| [`ColumnEnsembleForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.ColumnEnsembleForecaster.html#sktime.forecasting.compose.ColumnEnsembleForecaster "sktime.forecasting.compose.ColumnEnsembleForecaster") (forecasters) | Forecast each series with separate forecaster. |
| [`MultiplexForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.MultiplexForecaster.html#sktime.forecasting.compose.MultiplexForecaster "sktime.forecasting.compose.MultiplexForecaster") (forecasters\[,...\]) | MultiplexForecaster for selecting among different models in Auto-ML pipelines. |
| [`ForecastX`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.ForecastX.html#sktime.forecasting.compose.ForecastX "sktime.forecasting.compose.ForecastX") (forecaster\_y\[, forecaster\_X,...\]) | Forecaster that forecasts exogeneous data for use in an endogeneous forecast. |
| [`ForecastByLevel`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.ForecastByLevel.html#sktime.forecasting.compose.ForecastByLevel "sktime.forecasting.compose.ForecastByLevel") (forecaster\[, groupby\]) | Forecast by instance or panel. |
| [`TransformSelectForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.TransformSelectForecaster.html#sktime.forecasting.compose.TransformSelectForecaster "sktime.forecasting.compose.TransformSelectForecaster") (forecasters\[,...\]) | Choosing a forecaster based on category or cluster of time series. |
| [`GroupbyCategoryForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.GroupbyCategoryForecaster.html#sktime.forecasting.compose.GroupbyCategoryForecaster "sktime.forecasting.compose.GroupbyCategoryForecaster") (forecasters\[,...\]) | Choosing a global forecaster based on category or cluster of time series. |
| [`HierarchyEnsembleForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.HierarchyEnsembleForecaster.html#sktime.forecasting.compose.HierarchyEnsembleForecaster "sktime.forecasting.compose.HierarchyEnsembleForecaster") (forecasters\[,...\]) | Aggregates hierarchical data, fit forecasters and make predictions. |
| [`Permute`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.Permute.html#sktime.forecasting.compose.Permute "sktime.forecasting.compose.Permute") (estimator\[, permutation, steps\_arg\]) | Permutation compositor for permuting forecasting pipeline steps. |
| [`FhPlexForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.FhPlexForecaster.html#sktime.forecasting.compose.FhPlexForecaster "sktime.forecasting.compose.FhPlexForecaster") (forecaster\[, fh\_params,...\]) | Uses different parameters by forecasting horizon element. |
| [`IgnoreX`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.IgnoreX.html#sktime.forecasting.compose.IgnoreX "sktime.forecasting.compose.IgnoreX") (forecaster\[, ignore\_x\]) | Compositor for ignoring exogenous variables. |
| [`FallbackForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.FallbackForecaster.html#sktime.forecasting.compose.FallbackForecaster "sktime.forecasting.compose.FallbackForecaster") (forecasters\[, verbose,...\]) | Forecaster that sequentially tries a list of forecasting models. |

## Reduction

Reduction forecasters that use `sklearn` regressors or `sktime` time series regressors to make forecasts.

### Concurrent tabular strategy

Uses exogeneous data at the same time stamp - simple reduction strategy.

| [`YfromX`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.YfromX.html#sktime.forecasting.compose.YfromX "sktime.forecasting.compose.YfromX") (estimator\[, pooling\]) | Simple reduction predicting endogeneous from concurrent exogeneous variables. |
| --- | --- |

### Direct and recursive - sktime native 1st generation

1st generation direct and recursive reduction forecasters, `numpy` based.

Different strategies can be constructed via `make_reduction` for easy specification.

| [`make_reduction`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.make_reduction.html#sktime.forecasting.compose.make_reduction "sktime.forecasting.compose.make_reduction") (estimator\[, strategy,...\]) | Make forecaster based on reduction to tabular or time-series regression. |
| --- | --- |

| [`DirectTabularRegressionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.DirectTabularRegressionForecaster.html#sktime.forecasting.compose.DirectTabularRegressionForecaster "sktime.forecasting.compose.DirectTabularRegressionForecaster") (estimator) | Direct reduction from forecasting to tabular regression. |
| --- | --- |
| [`DirectTimeSeriesRegressionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.DirectTimeSeriesRegressionForecaster.html#sktime.forecasting.compose.DirectTimeSeriesRegressionForecaster "sktime.forecasting.compose.DirectTimeSeriesRegressionForecaster") (estimator) | Direct reduction from forecasting to time-series regression. |
| [`MultioutputTabularRegressionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.MultioutputTabularRegressionForecaster.html#sktime.forecasting.compose.MultioutputTabularRegressionForecaster "sktime.forecasting.compose.MultioutputTabularRegressionForecaster") (estimator) | Multioutput reduction from forecasting to tabular regression. |
| [`MultioutputTimeSeriesRegressionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.MultioutputTimeSeriesRegressionForecaster.html#sktime.forecasting.compose.MultioutputTimeSeriesRegressionForecaster "sktime.forecasting.compose.MultioutputTimeSeriesRegressionForecaster") (...) | Multioutput reduction from forecasting to time series regression. |
| [`RecursiveTabularRegressionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.RecursiveTabularRegressionForecaster.html#sktime.forecasting.compose.RecursiveTabularRegressionForecaster "sktime.forecasting.compose.RecursiveTabularRegressionForecaster") (estimator) | Recursive reduction from forecasting to tabular regression. |
| [`RecursiveTimeSeriesRegressionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.RecursiveTimeSeriesRegressionForecaster.html#sktime.forecasting.compose.RecursiveTimeSeriesRegressionForecaster "sktime.forecasting.compose.RecursiveTimeSeriesRegressionForecaster") (...) | Recursive reduction from forecasting to time series regression. |
| [`DirRecTabularRegressionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.DirRecTabularRegressionForecaster.html#sktime.forecasting.compose.DirRecTabularRegressionForecaster "sktime.forecasting.compose.DirRecTabularRegressionForecaster") (estimator) | Dir-rec reduction from forecasting to tabular regression. |
| [`DirRecTimeSeriesRegressionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.DirRecTimeSeriesRegressionForecaster.html#sktime.forecasting.compose.DirRecTimeSeriesRegressionForecaster "sktime.forecasting.compose.DirRecTimeSeriesRegressionForecaster") (estimator) | Dir-rec reduction from forecasting to time-series regression. |

### Direct and recursive - sktime native 2nd generation

2nd generation rearchitecture of direct and recursive reduction forecasters, `pandas` based.

| [`DirectReductionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.DirectReductionForecaster.html#sktime.forecasting.compose.DirectReductionForecaster "sktime.forecasting.compose.DirectReductionForecaster") (estimator\[,...\]) | Direct reduction forecaster, incl single-output, multi-output, exogeneous Dir. |
| --- | --- |
| [`RecursiveReductionForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.RecursiveReductionForecaster.html#sktime.forecasting.compose.RecursiveReductionForecaster "sktime.forecasting.compose.RecursiveReductionForecaster") (estimator\[,...\]) | Recursive reduction forecaster, incl exogeneous Rec. |

### Direct and recursive - 3rd party

| [`SkforecastAutoreg`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.SkforecastAutoreg.html#sktime.forecasting.compose.SkforecastAutoreg "sktime.forecasting.compose.SkforecastAutoreg") (regressor, lags\[,...\]) | Adapter for `skforecast.ForecasterAutoreg.ForecasterAutoreg` class [\[Rab014607127f-1\]](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.SkforecastAutoreg.html#rab014607127f-1). |
| --- | --- |
| [`SkforecastRecursive`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.SkforecastRecursive.html#sktime.forecasting.compose.SkforecastRecursive "sktime.forecasting.compose.SkforecastRecursive") (regressor\[, lags,...\]) | Adapter for `skforecast.recursive.ForecasterRecursive` class [\[Rc9c1c54db0c0-1\]](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.SkforecastRecursive.html#rc9c1c54db0c0-1). |

| [`DartsRegressionModel`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.darts.DartsRegressionModel.html#sktime.forecasting.darts.DartsRegressionModel "sktime.forecasting.darts.DartsRegressionModel") (\[lags,...\]) | Darts Regression Model Estimator. |
| --- | --- |
| [`DartsLinearRegressionModel`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.darts.DartsLinearRegressionModel.html#sktime.forecasting.darts.DartsLinearRegressionModel "sktime.forecasting.darts.DartsLinearRegressionModel") (\[...\]) | Darts LinearRegression Estimator. |
| [`DartsXGBModel`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.darts.DartsXGBModel.html#sktime.forecasting.darts.DartsXGBModel "sktime.forecasting.darts.DartsXGBModel") (\[past\_covariates,...\]) | Darts XGBModel Estimator. |

## Naive forecasters

| [`NaiveForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.naive.NaiveForecaster.html#sktime.forecasting.naive.NaiveForecaster "sktime.forecasting.naive.NaiveForecaster") (\[strategy, window\_length, sp\]) | Forecast based on naive assumptions about past trends continuing. |
| --- | --- |

| [`ForecastKnownValues`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.dummy.ForecastKnownValues.html#sktime.forecasting.dummy.ForecastKnownValues "sktime.forecasting.dummy.ForecastKnownValues") (y\_known\[, method,...\]) | Forecaster that plays back known or prescribed values as forecasts. |
| --- | --- |

| [`DummyGlobalForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.dummy_global.DummyGlobalForecaster.html#sktime.forecasting.dummy_global.DummyGlobalForecaster "sktime.forecasting.dummy_global.DummyGlobalForecaster") (\[strategy\]) | Dummy global forecaster that predicts mean of pretrain data. |
| --- | --- |

## Prediction intervals

Wrappers that add prediction intervals to any forecaster.

| [`SquaringResiduals`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.squaring_residuals.SquaringResiduals.html#sktime.forecasting.squaring_residuals.SquaringResiduals "sktime.forecasting.squaring_residuals.SquaringResiduals") (\[forecaster,...\]) | Compute the prediction variance based on a separate forecaster. |
| --- | --- |

| [`NaiveVariance`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.naive.NaiveVariance.html#sktime.forecasting.naive.NaiveVariance "sktime.forecasting.naive.NaiveVariance") (forecaster\[, initial\_window,...\]) | Compute the prediction variance based on a naive strategy. |
| --- | --- |

| [`ConformalIntervals`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.conformal.ConformalIntervals.html#sktime.forecasting.conformal.ConformalIntervals "sktime.forecasting.conformal.ConformalIntervals") (forecaster\[, method,...\]) | Empirical and conformal prediction intervals. |
| --- | --- |

| [`BaggingForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.BaggingForecaster.html#sktime.forecasting.compose.BaggingForecaster "sktime.forecasting.compose.BaggingForecaster") (\[bootstrap\_transformer,...\]) | Forecast a time series by aggregating forecasts from its bootstraps. |
| --- | --- |

| [`EnbPIForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.enbpi.EnbPIForecaster.html#sktime.forecasting.enbpi.EnbPIForecaster "sktime.forecasting.enbpi.EnbPIForecaster") (\[forecaster,...\]) | Ensemble Bootstrap Prediction Interval Forecaster. |
| --- | --- |

## Calibration and bias adjustment

| [`BoxCoxBiasAdjustedForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.boxcox_bias_adjusted_forecaster.BoxCoxBiasAdjustedForecaster.html#sktime.forecasting.boxcox_bias_adjusted_forecaster.BoxCoxBiasAdjustedForecaster "sktime.forecasting.boxcox_bias_adjusted_forecaster.BoxCoxBiasAdjustedForecaster") (forecaster\[,...\]) | Box-Cox Bias-Adjusted Forecaster. |
| --- | --- |

## Trend forecasters

| [`TrendForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.trend.TrendForecaster.html#sktime.forecasting.trend.TrendForecaster "sktime.forecasting.trend.TrendForecaster") (\[regressor\]) | Trend based forecasts of time series data, regressing values on index. |
| --- | --- |
| [`PolynomialTrendForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.trend.PolynomialTrendForecaster.html#sktime.forecasting.trend.PolynomialTrendForecaster "sktime.forecasting.trend.PolynomialTrendForecaster") (\[regressor,...\]) | Forecast time series data with a polynomial trend. |
| [`STLForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.trend.STLForecaster.html#sktime.forecasting.trend.STLForecaster "sktime.forecasting.trend.STLForecaster") (\[sp, seasonal, trend,...\]) | Implements STLForecaster based on statsmodels.tsa.seasonal.STL implementation. |
| [`CurveFitForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.trend.CurveFitForecaster.html#sktime.forecasting.trend.CurveFitForecaster "sktime.forecasting.trend.CurveFitForecaster") (function\[,...\]) | The CurveFitForecaster takes a function and fits it by using scipy curve\_fit. |
| [`ProphetPiecewiseLinearTrendForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.trend.ProphetPiecewiseLinearTrendForecaster.html#sktime.forecasting.trend.ProphetPiecewiseLinearTrendForecaster "sktime.forecasting.trend.ProphetPiecewiseLinearTrendForecaster") (\[...\]) | Forecast time series data with a piecewise linear trend, fitted via prophet. |
| [`SplineTrendForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.trend.SplineTrendForecaster.html#sktime.forecasting.trend.SplineTrendForecaster "sktime.forecasting.trend.SplineTrendForecaster") (\[regressor, n\_knots,...\]) | Forecast time series data with a spline trend. |

| [`StatsForecastMSTL`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.statsforecast.StatsForecastMSTL.html#sktime.forecasting.statsforecast.StatsForecastMSTL "sktime.forecasting.statsforecast.StatsForecastMSTL") (season\_length\[,...\]) | StatsForecast Multiple Seasonal-Trend decomposition using LOESS model. |
| --- | --- |

## Exponential smoothing based forecasters

| [`ExponentialSmoothing`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.exp_smoothing.ExponentialSmoothing.html#sktime.forecasting.exp_smoothing.ExponentialSmoothing "sktime.forecasting.exp_smoothing.ExponentialSmoothing") (\[trend, damped\_trend,...\]) | Holt-Winters exponential smoothing forecaster. |
| --- | --- |

| [`AutoETS`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.ets.AutoETS.html#sktime.forecasting.ets.AutoETS "sktime.forecasting.ets.AutoETS") (\[error, trend, damped\_trend,...\]) | ETS models with both manual and automatic fitting capabilities. |
| --- | --- |

| [`StatsForecastAutoETS`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.statsforecast.StatsForecastAutoETS.html#sktime.forecasting.statsforecast.StatsForecastAutoETS "sktime.forecasting.statsforecast.StatsForecastAutoETS") (\[season\_length, model,...\]) | StatsForecast Automatic Exponential Smoothing model. |
| --- | --- |
| [`StatsForecastAutoCES`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.statsforecast.StatsForecastAutoCES.html#sktime.forecasting.statsforecast.StatsForecastAutoCES "sktime.forecasting.statsforecast.StatsForecastAutoCES") (\[season\_length, model\]) | StatsForecast Complex Exponential Smoothing model. |

| [`ThetaForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.theta.ThetaForecaster.html#sktime.forecasting.theta.ThetaForecaster "sktime.forecasting.theta.ThetaForecaster") (\[initial\_level,...\]) | Theta method for forecasting. |
| --- | --- |
| [`ThetaModularForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.theta.ThetaModularForecaster.html#sktime.forecasting.theta.ThetaModularForecaster "sktime.forecasting.theta.ThetaModularForecaster") (\[forecasters,...\]) | Modular theta method for forecasting. |

| [`StatsForecastAutoTheta`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.statsforecast.StatsForecastAutoTheta.html#sktime.forecasting.statsforecast.StatsForecastAutoTheta "sktime.forecasting.statsforecast.StatsForecastAutoTheta") (\[season\_length,...\]) | Statsforecast AutoTheta estimator. |
| --- | --- |

## AR/MA type forecasters

Forecasters with AR or MA component.

All “ARIMA” and “Auto-ARIMA” models below include SARIMAX capability.

### (V)AR(I)MAX models

| [`AutoREG`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.auto_reg.AutoREG.html#sktime.forecasting.auto_reg.AutoREG "sktime.forecasting.auto_reg.AutoREG") (\[lags, trend, seasonal, hold\_back,...\]) | Autoregressive AR-X(p) model. |
| --- | --- |

| [`ARIMA`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.arima.ARIMA.html#sktime.forecasting.arima.ARIMA "sktime.forecasting.arima.ARIMA") (\[order, seasonal\_order, start\_params,...\]) | (S)ARIMA(X) forecaster, from pmdarima package. |
| --- | --- |
| [`StatsModelsARIMA`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.arima.StatsModelsARIMA.html#sktime.forecasting.arima.StatsModelsARIMA "sktime.forecasting.arima.StatsModelsARIMA") (\[order, seasonal\_order,...\]) | (S)ARIMA(X) forecaster, from statsmodels, tsa.arima module. |

| [`SARIMAX`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.sarimax.SARIMAX.html#sktime.forecasting.sarimax.SARIMAX "sktime.forecasting.sarimax.SARIMAX") (\[order, seasonal\_order, trend,...\]) | (S)ARIMA(X) forecaster, from statsmodels, tsa.statespace module. |
| --- | --- |

| [`VAR`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.var.VAR.html#sktime.forecasting.var.VAR "sktime.forecasting.var.VAR") (\[maxlags, method, verbose, trend,...\]) | VAR model from statsmodels. |
| --- | --- |

| [`VARReduce`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.var_reduce.VARReduce.html#sktime.forecasting.var_reduce.VARReduce "sktime.forecasting.var_reduce.VARReduce") (\[lags, regressor\]) | Generalized VAR forecaster using tabularized regression. |
| --- | --- |

| [`VARMAX`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.varmax.VARMAX.html#sktime.forecasting.varmax.VARMAX "sktime.forecasting.varmax.VARMAX") (\[order, trend, error\_cov\_type,...\]) | VARMAX forecasting model from statsmodels. |
| --- | --- |

| [`VECM`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.vecm.VECM.html#sktime.forecasting.vecm.VECM "sktime.forecasting.vecm.VECM") (\[dates, freq, missing, k\_ar\_diff,...\]) | Vector Error Correction Model, from statsmodels. |
| --- | --- |

### Auto-ARIMA models

| [`AutoARIMA`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.arima.AutoARIMA.html#sktime.forecasting.arima.AutoARIMA "sktime.forecasting.arima.AutoARIMA") (\[start\_p, d, start\_q, max\_p,...\]) | Auto-(S)ARIMA(X) forecaster, from pmdarima package. |
| --- | --- |

| [`StatsForecastAutoARIMA`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.statsforecast.StatsForecastAutoARIMA.html#sktime.forecasting.statsforecast.StatsForecastAutoARIMA "sktime.forecasting.statsforecast.StatsForecastAutoARIMA") (\[start\_p, d,...\]) | StatsForecast AutoARIMA estimator. |
| --- | --- |

| [`ARARForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.arar.ARARForecaster.html#sktime.forecasting.arar.ARARForecaster "sktime.forecasting.arar.ARARForecaster") (\[max\_ar\_depth, max\_lag, safe\]) | ARAR (AutoRegressive-AutoRegressive) forecaster. |
| --- | --- |

## ARCH models

| [`StatsForecastARCH`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.arch.StatsForecastARCH.html#sktime.forecasting.arch.StatsForecastARCH "sktime.forecasting.arch.StatsForecastARCH") (\[p\]) | StatsForecast ARCH estimator. |
| --- | --- |
| [`StatsForecastGARCH`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.arch.StatsForecastGARCH.html#sktime.forecasting.arch.StatsForecastGARCH "sktime.forecasting.arch.StatsForecastGARCH") (\[p, q\]) | StatsForecast GARCH estimator. |
| [`ARCH`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.arch.ARCH.html#sktime.forecasting.arch.ARCH "sktime.forecasting.arch.ARCH") (\[mean, lags, vol, p, o, q, power,...\]) | Directly interfaces ARCH models from python package arch. |

## Structural time series models

| [`ARDL`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.ardl.ARDL.html#sktime.forecasting.ardl.ARDL "sktime.forecasting.ardl.ARDL") (\[lags, order, fixed, causal, trend,...\]) | Autoregressive Distributed Lag (ARDL) Model. |
| --- | --- |

| [`BATS`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.bats.BATS.html#sktime.forecasting.bats.BATS "sktime.forecasting.bats.BATS") (\[use\_box\_cox, box\_cox\_bounds,...\]) | BATS forecaster for time series with multiple seasonality. |
| --- | --- |

| [`TBATS`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.tbats.TBATS.html#sktime.forecasting.tbats.TBATS "sktime.forecasting.tbats.TBATS") (\[use\_box\_cox, box\_cox\_bounds,...\]) | TBATS forecaster for time series with multiple seasonality. |
| --- | --- |

| [`StatsForecastAutoTBATS`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.statsforecast.StatsForecastAutoTBATS.html#sktime.forecasting.statsforecast.StatsForecastAutoTBATS "sktime.forecasting.statsforecast.StatsForecastAutoTBATS") (\[seasonal\_periods,...\]) | StatsForecast TBATS model. |
| --- | --- |

| [`Prophet`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.fbprophet.Prophet.html#sktime.forecasting.fbprophet.Prophet "sktime.forecasting.fbprophet.Prophet") (\[freq, add\_seasonality,...\]) | Prophet forecaster by wrapping Facebook's prophet algorithm [\[R995275cbd543-1\]](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.fbprophet.Prophet.html#r995275cbd543-1). |
| --- | --- |

| [`Prophetverse`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.prophetverse.Prophetverse.html#sktime.forecasting.prophetverse.Prophetverse "sktime.forecasting.prophetverse.Prophetverse") (\[trend, exogenous\_effects,...\]) | Univariate prophetverse forecaster - prophet model implemented in numpyro. |
| --- | --- |
| [`HierarchicalProphet`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.prophetverse.HierarchicalProphet.html#sktime.forecasting.prophetverse.HierarchicalProphet "sktime.forecasting.prophetverse.HierarchicalProphet") (\[trend,...\]) | A Bayesian hierarchical time series forecasting model based on Meta's Prophet. |

| [`UnobservedComponents`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.structural.UnobservedComponents.html#sktime.forecasting.structural.UnobservedComponents "sktime.forecasting.structural.UnobservedComponents") (\[level, trend,...\]) | UnobservedComponents forecasting model from statsmodels. |
| --- | --- |

| [`DynamicFactor`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.dynamic_factor.DynamicFactor.html#sktime.forecasting.dynamic_factor.DynamicFactor "sktime.forecasting.dynamic_factor.DynamicFactor") (\[k\_factors, factor\_order,...\]) | Dynamic Factor Forecaster. |
| --- | --- |

| [`GreykiteForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.greykite.GreykiteForecaster.html#sktime.forecasting.greykite.GreykiteForecaster "sktime.forecasting.greykite.GreykiteForecaster") (\[forecast\_config,...\]) | Adapter for using Greykite forecasting models within sktime. |
| --- | --- |

## Deep learning based forecasters

| [`LTSFLinearForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.ltsf.LTSFLinearForecaster.html#sktime.forecasting.ltsf.LTSFLinearForecaster "sktime.forecasting.ltsf.LTSFLinearForecaster") (seq\_len, pred\_len, \*\[,...\]) | LTSF-Linear Forecaster. |
| --- | --- |
| [`LTSFDLinearForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.ltsf.LTSFDLinearForecaster.html#sktime.forecasting.ltsf.LTSFDLinearForecaster "sktime.forecasting.ltsf.LTSFDLinearForecaster") (seq\_len, pred\_len, \*) | LTSF-DLinear Forecaster. |
| [`LTSFNLinearForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.ltsf.LTSFNLinearForecaster.html#sktime.forecasting.ltsf.LTSFNLinearForecaster "sktime.forecasting.ltsf.LTSFNLinearForecaster") (seq\_len, pred\_len, \*) | LTSF-NLinear Forecaster. |
| [`LTSFTransformerForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.ltsf.LTSFTransformerForecaster.html#sktime.forecasting.ltsf.LTSFTransformerForecaster "sktime.forecasting.ltsf.LTSFTransformerForecaster") (seq\_len,...\[,...\]) | LTSF-Transformer Forecaster. |

| [`XLSTMForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.xlstm.XLSTMForecaster.html#sktime.forecasting.xlstm.XLSTMForecaster "sktime.forecasting.xlstm.XLSTMForecaster") (\[input\_size, hidden\_size,...\]) | xLSTM Forecaster for time series prediction using Extended LSTM architecture. |
| --- | --- |

| [`SCINetForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.scinet.SCINetForecaster.html#sktime.forecasting.scinet.SCINetForecaster "sktime.forecasting.scinet.SCINetForecaster") (seq\_len\[, pred\_len,...\]) | SCINet Forecaster. |
| --- | --- |

| [`ConvTimeNetForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.convtimenet.ConvTimeNetForecaster.html#sktime.forecasting.convtimenet.ConvTimeNetForecaster "sktime.forecasting.convtimenet.ConvTimeNetForecaster") (context\_window,...\[,...\]) | ConvTimeNet for time series forecasting. |
| --- | --- |

| [`CINNForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.conditional_invertible_neural_network.CINNForecaster.html#sktime.forecasting.conditional_invertible_neural_network.CINNForecaster "sktime.forecasting.conditional_invertible_neural_network.CINNForecaster") (\[n\_coupling\_layers,...\]) | Conditional Invertible Neural Network (cINN) Forecaster. |
| --- | --- |

| [`NeuralForecastRNN`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.neuralforecast.NeuralForecastRNN.html#sktime.forecasting.neuralforecast.NeuralForecastRNN "sktime.forecasting.neuralforecast.NeuralForecastRNN") (\[freq, local\_scaler\_type,...\]) | NeuralForecast RNN model. |
| --- | --- |
| [`NeuralForecastLSTM`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.neuralforecast.NeuralForecastLSTM.html#sktime.forecasting.neuralforecast.NeuralForecastLSTM "sktime.forecasting.neuralforecast.NeuralForecastLSTM") (\[freq,...\]) | NeuralForecast LSTM model. |
| [`NeuralForecastTCN`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.neuralforecast.NeuralForecastTCN.html#sktime.forecasting.neuralforecast.NeuralForecastTCN "sktime.forecasting.neuralforecast.NeuralForecastTCN") (\[freq, local\_scaler\_type,...\]) | NeuralForecast TCN model. |
| [`NeuralForecastGRU`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.neuralforecast.NeuralForecastGRU.html#sktime.forecasting.neuralforecast.NeuralForecastGRU "sktime.forecasting.neuralforecast.NeuralForecastGRU") (\[freq, local\_scaler\_type,...\]) | NeuralForecast GRU model. |
| [`NeuralForecastDilatedRNN`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.neuralforecast.NeuralForecastDilatedRNN.html#sktime.forecasting.neuralforecast.NeuralForecastDilatedRNN "sktime.forecasting.neuralforecast.NeuralForecastDilatedRNN") (\[freq,...\]) | NeuralForecast DilatedRNN model. |

| [`PytorchForecastingTFT`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.pytorchforecasting.PytorchForecastingTFT.html#sktime.forecasting.pytorchforecasting.PytorchForecastingTFT "sktime.forecasting.pytorchforecasting.PytorchForecastingTFT") (\[model\_params,...\]) | pytorch-forecasting Temporal Fusion Transformer model. |
| --- | --- |
| [`PytorchForecastingDeepAR`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.pytorchforecasting.PytorchForecastingDeepAR.html#sktime.forecasting.pytorchforecasting.PytorchForecastingDeepAR "sktime.forecasting.pytorchforecasting.PytorchForecastingDeepAR") (\[model\_params,...\]) | pytorch-forecasting DeepAR model. |
| [`PytorchForecastingNHiTS`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.pytorchforecasting.PytorchForecastingNHiTS.html#sktime.forecasting.pytorchforecasting.PytorchForecastingNHiTS "sktime.forecasting.pytorchforecasting.PytorchForecastingNHiTS") (\[model\_params,...\]) | pytorch-forecasting NHiTS model. |
| [`PytorchForecastingNBeats`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.pytorchforecasting.PytorchForecastingNBeats.html#sktime.forecasting.pytorchforecasting.PytorchForecastingNBeats "sktime.forecasting.pytorchforecasting.PytorchForecastingNBeats") (\[model\_params,...\]) | pytorch-forecasting NBeats model. |

| [`PyKANForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.pykan_forecaster.PyKANForecaster.html#sktime.forecasting.pykan_forecaster.PyKANForecaster "sktime.forecasting.pykan_forecaster.PyKANForecaster") (\[hidden\_layers,...\]) | PyKANForecaster uses Kolmogorov Arnold Network \[1\] to forecast time series data. |
| --- | --- |

| [`RBFForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.rbf_forecaster.RBFForecaster.html#sktime.forecasting.rbf_forecaster.RBFForecaster "sktime.forecasting.rbf_forecaster.RBFForecaster") (\[window\_length, hidden\_size,...\]) | Forecasting model using RBF transformations and 'NN' layers for time series. |
| --- | --- |

| [`ESRNNForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.es_rnn.ESRNNForecaster.html#sktime.forecasting.es_rnn.ESRNNForecaster "sktime.forecasting.es_rnn.ESRNNForecaster") (\[hidden\_size, num\_layer,...\]) | Exponential Smoothing Recurrant Neural Network. |
| --- | --- |

### Pre-trained and foundation models

| [`ChronosForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.chronos.ChronosForecaster.html#sktime.forecasting.chronos.ChronosForecaster "sktime.forecasting.chronos.ChronosForecaster") (model\_path\[, config,...\]) | Interface to the Chronos and Chronos-Bolt Zero-Shot Forecaster by Amazon Research. |
| --- | --- |

| [`HFTransformersForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.hf_transformers_forecaster.HFTransformersForecaster.html#sktime.forecasting.hf_transformers_forecaster.HFTransformersForecaster "sktime.forecasting.hf_transformers_forecaster.HFTransformersForecaster") (\[model\_path,...\]) | Forecaster that uses a huggingface model for forecasting. |
| --- | --- |

| [`MOIRAIForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.moirai_forecaster.MOIRAIForecaster.html#sktime.forecasting.moirai_forecaster.MOIRAIForecaster "sktime.forecasting.moirai_forecaster.MOIRAIForecaster") (checkpoint\_path\[,...\]) | Adapter for using MOIRAI Forecasters. |
| --- | --- |

| [`MomentFMForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.hf_momentfm_forecaster.MomentFMForecaster.html#sktime.forecasting.hf_momentfm_forecaster.MomentFMForecaster "sktime.forecasting.hf_momentfm_forecaster.MomentFMForecaster") (\[...\]) | Interface for forecasting with the deep learning time series model momentfm. |
| --- | --- |

| [`PatchTSTForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.patch_tst.PatchTSTForecaster.html#sktime.forecasting.patch_tst.PatchTSTForecaster "sktime.forecasting.patch_tst.PatchTSTForecaster") (\[model\_path,...\]) | Interface for the PatchTST forecaster. |
| --- | --- |

| [`TimeLLMForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.time_llm.TimeLLMForecaster.html#sktime.forecasting.time_llm.TimeLLMForecaster "sktime.forecasting.time_llm.TimeLLMForecaster") (\[task\_name, pred\_len,...\]) | Interface to the Time-LLM. |
| --- | --- |

| [`TimeMoEForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.timemoe.TimeMoEForecaster.html#sktime.forecasting.timemoe.TimeMoEForecaster "sktime.forecasting.timemoe.TimeMoEForecaster") (model\_path\[, config,...\]) | Interface for TimeMOE forecaster for zero-shot forecasting. |
| --- | --- |

| [`TimesFMForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.timesfm_forecaster.TimesFMForecaster.html#sktime.forecasting.timesfm_forecaster.TimesFMForecaster "sktime.forecasting.timesfm_forecaster.TimesFMForecaster") (\[context\_len,...\]) | TimesFM (Time Series Foundation Model) for Zero-Shot Forecasting. |
| --- | --- |

| [`TinyTimeMixerForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.ttm.TinyTimeMixerForecaster.html#sktime.forecasting.ttm.TinyTimeMixerForecaster "sktime.forecasting.ttm.TinyTimeMixerForecaster") (\[model\_path,...\]) | TinyTimeMixer Forecaster for Zero-Shot Forecasting of Multivariate Time Series. |
| --- | --- |

| [`TotoForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.toto.TotoForecaster.html#sktime.forecasting.toto.TotoForecaster "sktime.forecasting.toto.TotoForecaster") (\[seed, num\_samples,...\]) | Toto foundation model forecaster for zero-shot forecasting. |
| --- | --- |

## Intermittent time series forecasters

| [`Croston`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.croston.Croston.html#sktime.forecasting.croston.Croston "sktime.forecasting.croston.Croston") (\[smoothing\]) | Croston's method for forecasting intermittent time series. |
| --- | --- |

| [`StatsForecastADIDA`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.statsforecast.StatsForecastADIDA.html#sktime.forecasting.statsforecast.StatsForecastADIDA "sktime.forecasting.statsforecast.StatsForecastADIDA") (\[prediction\_intervals\]) | StatsForecast ADIDA (Aggregate-Disaggregate Intermittent Demand Approach) model. |
| --- | --- |

| [`TSB`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.tsb.TSB.html#sktime.forecasting.tsb.TSB "sktime.forecasting.tsb.TSB") (\[alpha, beta\]) | Teunter-Syntetos-Babai method for forecasting intermittent time series. |
| --- | --- |

## Ensembles and stacking

| [`EnsembleForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.EnsembleForecaster.html#sktime.forecasting.compose.EnsembleForecaster "sktime.forecasting.compose.EnsembleForecaster") (forecasters\[, n\_jobs,...\]) | Ensemble of forecasters. |
| --- | --- |
| [`AutoEnsembleForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.AutoEnsembleForecaster.html#sktime.forecasting.compose.AutoEnsembleForecaster "sktime.forecasting.compose.AutoEnsembleForecaster") (forecasters\[,...\]) | Automatically find best weights for the ensembled forecasters. |
| [`StackingForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.compose.StackingForecaster.html#sktime.forecasting.compose.StackingForecaster "sktime.forecasting.compose.StackingForecaster") (forecasters\[, regressor,...\]) | StackingForecaster. |

| [`ResidualBoostingForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.residual_booster.ResidualBoostingForecaster.html#sktime.forecasting.residual_booster.ResidualBoostingForecaster "sktime.forecasting.residual_booster.ResidualBoostingForecaster") (base\_forecaster,...) | Residual boosting forecast fitting one forecaster on residuals of another. |
| --- | --- |

| [`AutoTS`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.autots.AutoTS.html#sktime.forecasting.autots.AutoTS "sktime.forecasting.autots.AutoTS") (\[model\_name, model\_list, frequency,...\]) | Auto-ensemble from autots library by winedarksea. |
| --- | --- |

| [`MAPAForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.mapa.MAPAForecaster.html#sktime.forecasting.mapa.MAPAForecaster "sktime.forecasting.mapa.MAPAForecaster") (\[aggregation\_levels,...\]) | MAPAForecaster implements the Multiple Aggregation Prediction Algorithm (MAPA). |
| --- | --- |

## Causal Forecasting

| [`DoubleMLForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.causal.DoubleMLForecaster.html#sktime.forecasting.causal.DoubleMLForecaster "sktime.forecasting.causal.DoubleMLForecaster") (outcome\_fcst, treatment\_fcst) | Double Machine Learning forecaster for causal time-series forecasting. |
| --- | --- |

## Hierarchical reconciliation

| [`ReconcilerForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.reconcile.ReconcilerForecaster.html#sktime.forecasting.reconcile.ReconcilerForecaster "sktime.forecasting.reconcile.ReconcilerForecaster") (forecaster\[, method,...\]) | Hierarchical reconciliation forecaster. |
| --- | --- |

## Online and stream forecasting

| [`OnlineEnsembleForecaster`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.online_learning.OnlineEnsembleForecaster.html#sktime.forecasting.online_learning.OnlineEnsembleForecaster "sktime.forecasting.online_learning.OnlineEnsembleForecaster") (forecasters\[,...\]) | Online Updating Ensemble of forecasters. |
| --- | --- |
| [`NormalHedgeEnsemble`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.online_learning.NormalHedgeEnsemble.html#sktime.forecasting.online_learning.NormalHedgeEnsemble "sktime.forecasting.online_learning.NormalHedgeEnsemble") (\[n\_estimators, a, loss\_func\]) | Parameter free hedging algorithm. |
| [`NNLSEnsemble`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.online_learning.NNLSEnsemble.html#sktime.forecasting.online_learning.NNLSEnsemble "sktime.forecasting.online_learning.NNLSEnsemble") (\[n\_estimators, loss\_func\]) | Ensemble forecasts with Non-negative least squares based weighting. |

| [`UpdateEvery`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.stream.UpdateEvery.html#sktime.forecasting.stream.UpdateEvery "sktime.forecasting.stream.UpdateEvery") (forecaster\[, update\_interval\]) | Update only periodically when update is called. |
| --- | --- |
| [`UpdateRefitsEvery`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.stream.UpdateRefitsEvery.html#sktime.forecasting.stream.UpdateRefitsEvery "sktime.forecasting.stream.UpdateRefitsEvery") (forecaster\[,...\]) | Refits periodically when update is called. |
| [`DontUpdate`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.stream.DontUpdate.html#sktime.forecasting.stream.DontUpdate "sktime.forecasting.stream.DontUpdate") (forecaster) | Turns off updates, i.e., ensures that forecaster is only fit and never updated. |

## Adapters to other forecasting framework packages

Generic framework adapters that expose other frameworks in the `sktime` interface.

| [`HCrystalBallAdapter`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.adapters.HCrystalBallAdapter.html#sktime.forecasting.adapters.HCrystalBallAdapter "sktime.forecasting.adapters.HCrystalBallAdapter") (model) | Adapter for using `hcrystalball` forecasters in sktime. |
| --- | --- |

## Model selection and tuning

| [`ForecastingGridSearchCV`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.model_selection.ForecastingGridSearchCV.html#sktime.forecasting.model_selection.ForecastingGridSearchCV "sktime.forecasting.model_selection.ForecastingGridSearchCV") (forecaster, cv,...) | Perform grid-search cross-validation to find optimal model parameters. |
| --- | --- |
| [`ForecastingRandomizedSearchCV`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.model_selection.ForecastingRandomizedSearchCV.html#sktime.forecasting.model_selection.ForecastingRandomizedSearchCV "sktime.forecasting.model_selection.ForecastingRandomizedSearchCV") (forecaster,...) | Perform randomized-search cross-validation to find optimal model parameters. |
| [`ForecastingOptCV`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.model_selection.ForecastingOptCV.html#sktime.forecasting.model_selection.ForecastingOptCV "sktime.forecasting.model_selection.ForecastingOptCV") (forecaster, optimizer, cv) | Tune an sktime forecaster via any optimizer in the hyperactive toolbox. |
| [`ForecastingSkoptSearchCV`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.model_selection.ForecastingSkoptSearchCV.html#sktime.forecasting.model_selection.ForecastingSkoptSearchCV "sktime.forecasting.model_selection.ForecastingSkoptSearchCV") (forecaster, cv,...) | Bayesian search over hyperparameters for a forecaster. |
| [`ForecastingOptunaSearchCV`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.model_selection.ForecastingOptunaSearchCV.html#sktime.forecasting.model_selection.ForecastingOptunaSearchCV "sktime.forecasting.model_selection.ForecastingOptunaSearchCV") (forecaster, cv,...) | Perform Optuna search cross-validation to find optimal model hyperparameters. |

## Model Evaluation (Backtesting)

| [`evaluate`](https://www.sktime.net/en/latest/api_reference/auto_generated/sktime.forecasting.model_evaluation.evaluate.html#sktime.forecasting.model_evaluation.evaluate "sktime.forecasting.model_evaluation.evaluate") (forecaster, cv, y\[, X, strategy,...\]) | Evaluate forecaster using timeseries cross-validation. |
| --- | --- |

## Time index splitters

Evaluation and tuning can be customized using time index based splitters, for a list of these consult the [splitter API](https://www.sktime.net/en/latest/api_reference/split.html#split-ref)