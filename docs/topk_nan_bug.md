# Sumanjali — Reproduction of the A2 ST top-k NaN bug

## Objective
Reproduce the numerical failure in Assignment 2's straight-through
top-k selection on CPU, and verify the A3 correction using the same
synthetic scores and low temperature.

## Source verification
The A2 function was checked against the supplied A2 `nclara/modeling.py`
text, `st_topk()` (lines 165–181). The A3 function was checked against
`a3_share/code/train_e2e_a3.py` inside the supplied `a3_share.zip`,
`st_topk()` (lines 357–374). The test script includes both functions.
The trace wrappers add diagnostic printing but preserve the original
selection operations and update order.

## Experimental setup
- Device: CPU
- Candidate scores: `[0.90, 0.30, 0.20, 0.10]`
- Number of candidate documents: 4
- Number selected: `k = 4`
- Control temperature: `tau = 0.5`
- Bug reproduction temperature: `tau = 0.02`

No CLaRa model, checkpoint, dataset, CUDA device, or training is used.

## Results

### A2 at tau = 0.5
The old finite penalty is sufficient for this example. The selection
is D1, D2, D3, D4 and the straight-through output is finite.

### A2 at tau = 0.02
The first selection is D1. The `taken` value for D1 becomes 1.
On the second selection, D1's scaled score is 45 and its penalized
logit is approximately:

`45 + log(1e-9) = 45 - 20.7233 = 24.2767`

D2's scaled score is 15, so D1 still wins and is selected a second time.
Now `taken[D1] = 2`.

At the start of iteration 3, A2 evaluates:

`log(1 - 2 + 1e-9)`

The argument is negative, so the logarithm produces NaN. The logits
and softmax probabilities become NaN, and the straight-through output
is non-finite. Any `argmax` index returned after this point is not a
meaningful document selection; the NaN has already occurred.

### A3 at tau = 0.02
The A3 implementation masks previously selected documents with
negative infinity. It selects D1, D2, D3, D4 exactly once each, and
the output remains finite.

## Conclusion
The test reproduces the A2 failure mechanism at the low temperature:
the finite log penalty does not guarantee exclusion of a previously
selected document when the score gap divided by temperature is larger
than the penalty magnitude. Duplicate selection makes `taken` exceed 1;
the subsequent logarithm receives a negative argument and produces NaN.

A3 replaces the finite penalty with an exact `-inf` mask for selected
documents. For this test (`k <= number of candidates`), the A3 function
selects distinct documents and remains finite.

## Scope and limitation
This is a controlled CPU unit test of the top-k function. It establishes
the numerical failure mechanism in isolation; it does not by itself
reproduce a full training crash or quantify its effect on model metrics.
