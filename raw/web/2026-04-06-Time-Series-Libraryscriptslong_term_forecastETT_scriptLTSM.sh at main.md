---
source_type: web
title: "Time-Series-Library/scripts/long_term_forecast/ETT_script/LTSM.sh at main"
author: 
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://github.com/thuml/Time-Series-Library/blob/main/scripts/long_term_forecast/ETT_script/LTSM.sh"
published: 
created: 2026-04-06
description: "A Library for Advanced Deep Time Series Models for General Time Series Analysis. - Time-Series-Library/scripts/long_term_forecast/ETT_script/LTSM.sh at main · thuml/Time-Series-Library"
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

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

export CUDA\_VISIBLE\_DEVICES=2

model\_name=Chronos2

seq\_len=2048

for pred\_len in 96 192 336 720

do

python -u run.py \\

\--task\_name zero\_shot\_forecast \\

\--is\_training 0 \\

\--root\_path./dataset/ETT-small/ \\

\--data\_path ETTh1.csv \\

\--model\_id ETTh1\_$seq\_len'\_'$pred\_len \\

\--model $model\_name \\

\--data ETTh1 \\

\--features M \\

\--seq\_len $seq\_len \\

\--pred\_len $pred\_len \\

\--seg\_len 24 \\

\--enc\_in 7 \\

\--d\_model 512 \\

\--dropout 0.5 \\

\--learning\_rate 0.0001 \\

\--des 'Exp' \\

\--itr 1

done

for pred\_len in 96 192 336 720

do

python -u run.py \\

\--task\_name zero\_shot\_forecast \\

\--is\_training 0 \\

\--root\_path./dataset/ETT-small/ \\

\--data\_path ETTh2.csv \\

\--model\_id ETTh2\_$seq\_len'\_'$pred\_len \\

\--model $model\_name \\

\--data ETTh2 \\

\--features M \\

\--seq\_len $seq\_len \\

\--pred\_len $pred\_len \\

\--seg\_len 24 \\

\--enc\_in 7 \\

\--d\_model 256 \\

\--dropout 0.5 \\

\--learning\_rate 0.0001 \\

\--des 'Exp' \\

\--itr 1

done

for pred\_len in 192 336 720

do

python -u run.py \\

\--task\_name zero\_shot\_forecast \\

\--is\_training 0 \\

\--root\_path./dataset/ETT-small/ \\

\--data\_path ETTm1.csv \\

\--model\_id ETTm1\_$seq\_len'\_'$pred\_len \\

\--model $model\_name \\

\--data ETTm1 \\

\--features M \\

\--seq\_len $seq\_len \\

\--pred\_len $pred\_len \\

\--seg\_len 24 \\

\--enc\_in 7 \\

\--d\_model 512 \\

\--dropout 0.5 \\

\--learning\_rate 0.0001 \\

\--des 'Exp' \\

\--itr 1

done

for pred\_len in 96 192 336 720

do

python -u run.py \\

\--task\_name zero\_shot\_forecast \\

\--is\_training 0 \\

\--root\_path./dataset/ETT-small/ \\

\--data\_path ETTm2.csv \\

\--model\_id ETTm2\_$seq\_len'\_'$pred\_len \\

\--model $model\_name \\

\--data ETTm2 \\

\--features M \\

\--seq\_len $seq\_len \\

\--pred\_len $pred\_len \\

\--seg\_len 24 \\

\--enc\_in 7 \\

\--d\_model 512 \\

\--dropout 0.5 \\

\--learning\_rate 0.0001 \\

\--des 'Exp' \\

\--itr 1

done