---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: null
source_type: web
status: inbox
tags:
- null
- clippings
title: Panel ARDL.pdf
source_url: https://drive.google.com/file/d/1WMnCLwMUxvibAV1CEHWb6pBOKyFZf7sE/view?pli=1
published_at: null
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

![](https://drive.google.com/u/0/drive-viewer/AKGpihYLfyKe9ToNMb3CpSKLkoMi-2-7Uk3JdD6a0PjYLdfeX6n_qLRC4RUgjoyCkFGfwuieUIteD83YbrC87femDmJysIWWOb2lmFw=s1600-rw-v1)

## 第1页，共48页

Panel ARDL: The Concept

Modeling Dynamic Heterogenous Panels

Obi

Learning Pat Obi

Δyit = ෍

k=1

p−1

ik

∗ Δyi,t−k + ෍

k=0

q−1

δik

∗′ ΔXi,t−k + iyi,t−1 + βi

′Xit + i + it

https://youtu.be/4-h9dU\_ZKUA

Δ y sub it equals sum from k equals 1 to p minus 1 of,  sub i. k to the asterisk operator, cap delta y sub, i.,t minus k end subscript, end summation plus sum from k equals 0 to q minus 1 of, bold italic delta sub i. k to the open paren asterisk operator prime close paren, cap delta bold italic cap X sub, i.,t minus k end subscript, end summation plus  sub i., y sub, i.,t minus 1 end subscript plus subscript base, bold italic beta sub i. to the prime, bold italic cap X, end base, sub i. t plus  sub i. plus  sub i. t

Δ y sub it equals sum from k equals 1 to p minus 1 of,  sub i. k to the asterisk operator, cap delta y sub, i.,t minus k end subscript, end summation plus sum from k equals 0 to q minus 1 of, bold italic delta sub i. k to the open paren asterisk operator prime close paren, cap delta bold italic cap X sub, i.,t minus k end subscript, end summation plus  sub i., y sub, i.,t minus 1 end subscript plus subscript base, bold italic beta sub i. to the prime, bold italic cap X, end base, sub i. t plus  sub i. plus  sub i. t

## 第2页，共48页

Balanced Panels

1\. BALANCED PANEL

Equal number of observations

Group Year Y X1 X2

1 2020 231 3 18

1 2019 334 3 27

1 2018 436 3 32

1 2017 411 3 40

2 2020 332 5 23

2 2019 401 5 33

2 2018 423 5 45

2 2017 398 5 60

3 2020 304 2 22

3 2019 511 2 31

3 2018 634 2 48

3 2017 588 2 57

2\. SHORT PANEL (Micro Panel): T < N

Group Year Y X1 X2

1 2020 231 3 18

1 2019 334 3 27

2 2020 332 5 23

2 2019 401 5 33

3 2020 304 2 22

3 2019 511 2 31

3\. LONG PANEL (Macro Panel): T > N

Group Year Y X1 X2

1 2020 231 3 18

1 2019 334 3 27

1 2018 436 3 32

2 2020 332 5 23

2 2019 401 5 33

2 2018 423 5 45

T = Number of periods

N = Number of groups

## 第3页，共48页

Group Year Y X1 X2

1 2020 231 3 18

1 2019 334 3 27

2 2020 332 5 23

2 2019 401 5 33

2 2018 423 5 45

3 2020 304 2 22

4\. UNBALANCED PANEL

Number of observations not the same.

5\. DYNAMIC PANEL

(dynamic heterogenous panel)

Lagged values of dependent variable (Yt−i

)

included as regressor:

Yit = i + iYi,t−1 + iXit + it

Other Types of Panel Data

## 第4页，共48页

When Can We Run Panel ARDL?

• Regressors can be:

▪Mix of I(0) and I(1) variables

▪ I(0)

▪ I(1)

▪No I(2) or higher

• Parameters of interest:

▪ Long-run coefficients

▪ Short-run coefficients

▪ Speed of adjustment

## 第5页，共48页

The Empirical Process

1\. Run panel unit root test – to confirm no variable is ≥ I(2)

2\. Specify Panel ARDL cointegration model

3\. Estimate model with PMG, MG, or DFE

4\. Use Hausman Test to determine appropriate estimator

5\. Interpret result:

• Cointegration – joint causality

• ECT – speed of adjustment

• Long-run causality

• Short-run causality