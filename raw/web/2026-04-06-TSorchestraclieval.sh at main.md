---
source_type: web
title: "TSorchestra/cli/eval.sh at main"
author: 
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://github.com/DC-research/TSorchestra/blob/main/cli/eval.sh"
published: 
created: 2026-04-06
description: "Time Series Orchestra (TSorchestra) is a novel ensemble framework designed for zero-shot time series forecasting. It is built upon a curated collection of time series foundation models. The architecture is designed to leverage the specialized capabilities of its constituent models to deliver SOTA performance and generalization across datasets. - TSorchestra/cli/eval.sh at main · DC-research/TSorchestra"
tags:
  - 
  - "clippings"
---

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

#!/bin/bash

#SBATCH --job-name=slsqp\_eval

#SBATCH --array=0-97

#SBATCH --partition=gpuA40x4

#SBATCH --mem=200G

#SBATCH --nodes=1

#SBATCH --ntasks-per-node=1

#SBATCH --cpus-per-task=16

#SBATCH --constraint="scratch"

#SBATCH --gpus-per-node=1

#SBATCH --gpu-bind=closest

#SBATCH --account= # TODO: Enter your SLURM account

#SBATCH --time=24:00:00

#SBATCH --output=output/logs/%x/out/%A/%a.out

#SBATCH --error=output/logs/%x/err/%A/%a.err

#SBATCH --mail-user= # TODO: Enter your email address

#SBATCH --mail-type=BEGIN,END,FAIL

mkdir -p./output/logs

source./cli/utils.sh

activate\_conda\_env

log\_info "Starting $(get\_slurm\_message)"

\# Default to the M4 Hourly dataset (short-term) if not using SLURM

M4\_HOURLY\_TASK\_ID=38

DEFAULT\_TASK\_ID=$M4\_HOURLY\_TASK\_ID

\# Ensure SLURM\_ARRAY\_TASK\_ID is set

SLURM\_ARRAY\_TASK\_ID=${SLURM\_ARRAY\_TASK\_ID:-$DEFAULT\_TASK\_ID}

export SLURM\_ARRAY\_TASK\_ID

\# Set run configs

metric="mae"

n\_windows=1

batch\_size=128

imputation="dummy\_value"

if python -m pipeline.eval -cp../conf \\

ensemble.metric="${metric}" \\

ensemble.n\_windows="${n\_windows}" \\

ensemble.batch\_size="${batch\_size}" \\

imputation="${imputation}"; then

log\_info "Successfully finished $(get\_slurm\_message)!"

log\_error "No errors!"

echo "\[$(get\_timestamp)\] Done with $(get\_slurm\_message)" >"$(get\_done\_file)"

exit 0

else

log\_error "Job failed for $(get\_slurm\_message)!" >&2

exti 1

fi