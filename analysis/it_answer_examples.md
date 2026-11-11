Instruction Tuning — Example Answer Changes and Analysis 
Changed to correct answer-
Q: Which paper in the Long Island Herald chain serves a village in Nassau County with population 6,483?
Correct answer: The Nassau Herald
A2 prediction: Long Island Herald ✗
A3 prediction: The Nassau Herald ✓

Q: Which 2008 documentary, Pond Hockey or I.O.U.S.A., is about fiscal issues?
Correct answer: I.O.U.S.A.
A2 prediction: I.O.U. A ✗
A3 prediction: I.O.U.S.A. ✓

Q: Which band had more members, Semisonic or Cake?
Correct answer: Cake
A2 prediction: Semisonic ✗
A3 prediction: Cake ✓


Changed to wrong answer-
Q: What actor was also a president that Richard Darman worked with?
Correct answer: George H. W. Bush
A2 prediction: George H. W. Bush ✓
A3 prediction: Ronald Reagan ✗ (was right, now wrong)

Q: Which film came first, Laura’s Star or Wonder Woman?
Correct answer: Laura’s Star
A2 prediction: Laura’s Star ✓
A3 prediction: Wonder Woman ✗ (was right, now wrong)

Observations and Analysis
A2 trains the generator in two stages: Stage 1 on single clean passages (no distractors), and Stage 2 on documents picked by the model’s own learned retriever — so A2’s generator was never trained on documents chosen by simple keyword overlap.
A3 adds a new stage in between: instruction tuning. Here, each training example pairs the correct passage with BM25 distractors — passages picked purely because they share words with the question, with no regard for whether they’re actually relevant. This is the one new thing in the whole pipeline: the generator is now forced to pick the right answer out of a lineup chosen by raw lexical overlap, not by relevance.
Correct changes 1–3: A2’s errors here were all near misses like naming the parent chain instead of the specific paper, truncating “I.O.U.S.A.,” or picking the wrong one of two named options. These are exactly the errors BM25-distractor training targets: it repeatedly makes the model separate the correct passage from close, high-word-overlap lookalikes. That extra practice is why all three got fixed.
Incorrect changes 1–2: This is the tradeoff.. BM25 doesn’t pick distractors by correctness, just by shared words. So during training, the “wrong” passage sitting next to the gold one can itself be a different-but-similar-sounding name (e.g. Reagan next to Bush). Practicing on these kinds of mix-ups can teach the model to second-guess a name it used to get right, and swap it for the competing one — which is what happened in both regressions.
Therefore, the one new training ingredient (BM25-based distractors) explains both outcomes — it sharpens the model against near-misses but also introduces new confusions where the “wrong” option was itself lexically close to the right one. Same cause, both directions.
