# RSNA Knee LLM Labels: data quality report

## Findings

No problems found by the checks that were run.

## Dataset overview

```text
   rows  columns  memory_mb
0  4406       37       3.88
```

## Columns

```text
                             dtype  non_null_count  unique_count                                                           example
StudyInstanceUID               str            4406          4406  1.2.826.0.1.3680043.8.498.10004873229099053869093324292195817260
ACL                        float64            4406             5                                                              0.28
ACL__conf                  float64            4406             3                                                              0.05
ACL__verdict                   str            4406             3                                                               UNK
MCL                        float64            4406             5                                                              0.28
MCL__conf                  float64            4406             3                                                              0.05
MCL__verdict                   str            4406             3                                                               UNK
Medial Meniscus            float64            4406             5                                                              0.82
Medial Meniscus__conf      float64            4406             3                                                              0.95
Medial Meniscus__verdict       str            4406             3                                                               YES
Lateral Meniscus           float64            4406             5                                                              0.28
Lateral Meniscus__conf     float64            4406             3                                                              0.05
Lateral Meniscus__verdict      str            4406             3                                                               UNK
Medial OA                  float64            4406             5                                                              0.82
Medial OA__conf            float64            4406             3                                                              0.95
Medial OA__verdict             str            4406             3                                                               YES
Lateral OA                 float64            4406             5                                                              0.28
Lateral OA__conf           float64            4406             3                                                              0.05
Lateral OA__verdict            str            4406             3                                                               UNK
PF OA                      float64            4406             5                                                              0.28
PF OA__conf                float64            4406             3                                                              0.05
PF OA__verdict                 str            4406             3                                                               UNK
Effusion                   float64            4406             5                                                              0.82
Effusion__conf             float64            4406             3                                                              0.95
Effusion__verdict              str            4406             3                                                               YES
Synovitis                  float64            4406             5                                                              0.28
Synovitis__conf            float64            4406             3                                                              0.05
Synovitis__verdict             str            4406             3                                                               UNK
Baker's                    float64            4406             5                                                              0.28
Baker's__conf              float64            4406             3                                                              0.05
Baker's__verdict               str            4406             3                                                               UNK
Contusion                  float64            4406             5                                                              0.08
Contusion__conf            float64            4406             3                                                              0.85
Contusion__verdict             str            4406             3                                                                NO
Fracture                   float64            4406             5                                                              0.08
Fracture__conf             float64            4406             3                                                              0.85
Fracture__verdict              str            4406             3                                                                NO
```

## Missing values

```text
                           missing_count  missing_pct
StudyInstanceUID                       0          0.0
ACL                                    0          0.0
ACL__conf                              0          0.0
ACL__verdict                           0          0.0
MCL                                    0          0.0
MCL__conf                              0          0.0
MCL__verdict                           0          0.0
Medial Meniscus                        0          0.0
Medial Meniscus__conf                  0          0.0
Medial Meniscus__verdict               0          0.0
Lateral Meniscus                       0          0.0
Lateral Meniscus__conf                 0          0.0
Lateral Meniscus__verdict              0          0.0
Medial OA                              0          0.0
Medial OA__conf                        0          0.0
Medial OA__verdict                     0          0.0
Lateral OA                             0          0.0
Lateral OA__conf                       0          0.0
Lateral OA__verdict                    0          0.0
PF OA                                  0          0.0
PF OA__conf                            0          0.0
PF OA__verdict                         0          0.0
Effusion                               0          0.0
Effusion__conf                         0          0.0
Effusion__verdict                      0          0.0
Synovitis                              0          0.0
Synovitis__conf                        0          0.0
Synovitis__verdict                     0          0.0
Baker's                                0          0.0
Baker's__conf                          0          0.0
Baker's__verdict                       0          0.0
Contusion                              0          0.0
Contusion__conf                        0          0.0
Contusion__verdict                     0          0.0
Fracture                               0          0.0
Fracture__conf                         0          0.0
Fracture__verdict                      0          0.0
```

## Duplicate rows

```text
   duplicate_count  duplicate_pct
0                0            0.0
```

## Identifier check

```text
                  missing_count  duplicate_count  duplicate_pct
StudyInstanceUID              0                0            0.0
```

## Categorical checks

```text
                                allowed  unexpected_count unexpected
ACL__verdict               YES, NO, UNK                 0           
MCL__verdict               YES, NO, UNK                 0           
Medial Meniscus__verdict   YES, NO, UNK                 0           
Lateral Meniscus__verdict  YES, NO, UNK                 0           
Medial OA__verdict         YES, NO, UNK                 0           
Lateral OA__verdict        YES, NO, UNK                 0           
PF OA__verdict             YES, NO, UNK                 0           
Effusion__verdict          YES, NO, UNK                 0           
Synovitis__verdict         YES, NO, UNK                 0           
Baker's__verdict           YES, NO, UNK                 0           
Contusion__verdict         YES, NO, UNK                 0           
Fracture__verdict          YES, NO, UNK                 0           
```

## Numeric range checks

```text
                        allowed_min  allowed_max  observed_min  observed_max  below_min  above_max  missing
ACL                               0            1          0.08          0.94          0          0        0
ACL__conf                         0            1          0.05          0.95          0          0        0
MCL                               0            1          0.08          0.94          0          0        0
MCL__conf                         0            1          0.05          0.95          0          0        0
Medial Meniscus                   0            1          0.08          0.94          0          0        0
Medial Meniscus__conf             0            1          0.05          0.95          0          0        0
Lateral Meniscus                  0            1          0.08          0.94          0          0        0
Lateral Meniscus__conf            0            1          0.05          0.95          0          0        0
Medial OA                         0            1          0.08          0.94          0          0        0
Medial OA__conf                   0            1          0.05          0.95          0          0        0
Lateral OA                        0            1          0.08          0.94          0          0        0
Lateral OA__conf                  0            1          0.05          0.95          0          0        0
PF OA                             0            1          0.08          0.94          0          0        0
PF OA__conf                       0            1          0.05          0.95          0          0        0
Effusion                          0            1          0.08          0.94          0          0        0
Effusion__conf                    0            1          0.05          0.95          0          0        0
Synovitis                         0            1          0.08          0.94          0          0        0
Synovitis__conf                   0            1          0.05          0.95          0          0        0
Baker's                           0            1          0.08          0.94          0          0        0
Baker's__conf                     0            1          0.05          0.95          0          0        0
Contusion                         0            1          0.08          0.94          0          0        0
Contusion__conf                   0            1          0.05          0.95          0          0        0
Fracture                          0            1          0.08          0.94          0          0        0
Fracture__conf                    0            1          0.05          0.95          0          0        0
```
