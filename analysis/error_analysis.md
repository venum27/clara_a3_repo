# Error Analysis

## 1.1 Setup

- **Dataset:** 2WikiMultihopQA, 3,000 evaluation questions
- **Model:** nested memory + learned budget head (`a3_head_tau0.02_s42`), 64 memory vectors, seed 42
- **Result:** 2,078 of 3,000 answers are wrong (EM 30.7%)
- **Source:** `runs/qwen/2wiki/a3_head_tau0.02_s42/results_big/qa_predictions.json`, prediction `learned@64`

## 1.2 Method

A wrong answer means exact match = 0. Each wrong answer goes into one group, checked in this order:

1. **Retrieval miss:** none of the gold passages is among the 4 passages read.
2. **Partial / format error:** the gold answer is inside the prediction or the reverse, or they differ only in form (France/French, a cut-off title).
3. **Wrong entity:** everything else.

The groups were set by rule on all 2,078 errors. I sampled 30 and checked each against the passage text from `data/2wiki_evalbig.json`, correcting labels by hand where needed.

## 1.3 Counts over all wrong answers

Of the 1,989 wrong answers where a gold passage was retrieved, the gold answer string appears in the 4 passages read in 1,707 cases (86%).

| Group | Count | Share |
|---|---:|---:|
| Retrieval miss | 89 | 4.3% |
| Partial / format error | 145 | 7.0% |
| Wrong entity | 1,844 | 88.7% |
| **Total** | **2,078** | **100%** |

## 1.4 The 30 examples

### Retrieval miss (10)

| # | Question | Gold | Prediction |
|---:|---|---|---|
| 1 | Which film has the director born later, Charlie Chan In Honolulu or Lianna? | Lianna | Charlie Chan In Honolulu |
| 2 | Which film was released more recently, A Fugitive From Matrimony or Grass Is Greener? | Grass Is Greener | A Fugitive From Matrimony |
| 3 | Which film was released earlier, A Wet Dream On Elm Street or The Best Things In The World? | The Best Things In The World | A Wet Dream On Elm Street |
| 4 | Which film was released earlier, The Salvos Of The Aurora Cruiser or Nucingen House? | The Salvos Of The Aurora Cruiser | Nucingen House |
| 5 | Place of birth of the director of Geography Club (Film)? | Miami, Florida | New York |
| 6 | Place of birth of the director of Time Raiders? | Hong Kong | New York |
| 7 | Maternal grandmother of Princess Anna Elisabeth Louise Of Brandenburg-Schwedt? | Sophia Dorothea of Hanover | Margaret of Prussia |
| 8 | Place of birth of the performer of song Sing A Song Now Now? | Pavia | Hollywood |
| 9 | Which film was released first, The Pirate’S Dream or Prem Mhanje Prem Mhanje Prem Asta? | The Pirate’S Dream | Prem Mhanje Prem Mhanje Prem Asta |
| 10 | Father of the composer of film The Hero Of Color City? | Basil Poledouris | Francisco de Aldama |

### Wrong entity (14)

A gold passage was read in every row. “In read text” means the model’s answer appears in the 4 passages read (n/a for comparison questions, whose answers are titles from the question).

| # | Question | Gold | Prediction | In read text | Note |
|---:|---|---|---|---|---|
| 11 | Nationality of the director of The Sweetest Fruits? | Austria | German | Yes | Wrong country |
| 12 | Which film has the director born earlier, To Dorothy A Son or Jurášek? | Jurášek | To Dorothy A Son | n/a | Comparison, wrong side |
| 13 | Maternal grandfather of Archduchess Maria Immakulata Of Austria? | Ferdinand II of the Two Sicilies | Archduchess Maria Amalia of Austria | No | Answer not in the passages read |
| 14 | Place of birth of the director of The Great Dome Robbery? | British | New York | Yes | Gold label looks wrong (a nationality) |
| 15 | Which album came out first, No Talking, Just Head or Doing It My Way? | No Talking, Just Head | Doing It My Way | n/a | Comparison, wrong side |
| 16 | Date of death of Blanche Of Lancaster’s mother? | 1322 | 24 December 1406 | No | Date not in the passages read |
| 17 | Which film came out earlier, The Man From Bitter Ridge or Operación G? | The Man From Bitter Ridge | Operación G | n/a | Comparison, wrong side (gold at rank 3+) |
| 18 | Where did Elisa Godínez Gómez De Batista’s husband die? | Marbella | Cuban | Yes | Wrong answer type (nationality for a place) |
| 19 | Which film’s director was born earlier, Rockshow or Sheba, Baby? | Rockshow | Sheba, Baby | n/a | Comparison, wrong side |
| 21 | Teacher of the composer of song Prometheus (Art Song)? | Antonio Salieri | Franz Schubert | No | Gave the composer, not the teacher |
| 22 | Award won by the director of The Film That WasN’T? | Israel Prize | Academy Award | No | Plausible but not in the passages |
| 23 | Paternal grandfather of Prince William, Duke Of Cumberland? | George I of Great Britain | George, Duke of Cumberland | No | Wrong person, shares “George” |
| 28 | Spouse of the director of Looking For Hortense? | Sophie Fillières | Sophie Bonaparte | No | Shares only the first name |
| 30 | Where did Shahrzad Mojab’s husband graduate from? | University of Tehran | University of Michigan | No | Wrong university, not in the passages |

### Partial / format error (6)

| # | Question | Gold | Prediction | Note |
|---:|---|---|---|---|
| 20 | Nationality of the director of P2 (Film)? | France | French | Adjective vs noun |
| 24 | Where did the director of The $1,000,000 Reward study? | Amherst | Amherst College | Extra words |
| 25 | Which film came out first, Una Prostituta Al Servizio Del Pubblico… or The Bag Man? | Una Prostituta Al Servizio Del Pubblico E In Regola Con Le Leggi Dello Stato | Una Prostituta Al Servizio Del Pubblico | Title cut short |
| 26 | Paternal grandfather of Konrad Vi The Dean? | Konrad II the Gray | Konrad II, Duke of Olsztyn | Right person (Konrad II). Missing “the Gray”, and “Olsztyn” is not in the passages (they say Oleśnica) |
| 27 | Which film was released first, Resan or Ömer The Tourist In Star Trek? | Ömer The Tourist In Star Trek | Ömer The Tourist | Title cut short |
| 29 | Which country is the director of Just A Gigolo (1978 Film) from? | English | England | Gold is a nationality here |

## 1.5 What the analysis shows

- Retrieval is not the main error source. Only 4.3% of wrong answers have no gold passage among the 4 read. At least one gold passage is retrieved for 96% of all questions.
- Most errors happen after retrieval. In 86% of the retrieved-but-wrong cases, the gold answer string is in the text of the passages read.
- The model often answers with something that is not in the passages. In 7 of 10 non-comparison wrong-entity examples, the prediction does not appear in the 4 passages read. This points to the generator reading the compressed memory badly. We did not test this directly.
- Comparison questions fail by picking the wrong side, even when retrieval worked (#12, #15, #17, #19).
- Some errors come from the metric. France/French, Amherst/Amherst College and cut-off titles count as fully wrong under EM.
- Some gold labels look noisy (#14, #29).

## 1.6 Limits of this analysis

- One run, one seed, one dataset (2Wiki).
- The 30 examples are a sample. Percentages come only from the full counts in 1.3.
- String matching against the passages does not work for comparison questions.
- The wrong-entity group holds 89% of errors. Splitting it into wrong value, wrong comparison side and wrong answer type would give more detail.
