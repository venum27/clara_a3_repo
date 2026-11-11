# Official CLaRa Stage-2 Code Comparison (`train_it_nested.py`)

**Author:** Swami Aryanathan  
**Contribution:** Official CLaRa Stage-2 Code Analysis, Architectural Comparison, and Empirical Findings  
**Target Repository & Commit:** `apple/ml-clara` (pinned commit `ee93341`, cited in the A2 paper), specifically `train_sft.py`, `modeling_clara.py`, and `sft_dataset.py`

---

## 1. Background: The Three-Stage Training Pipeline

In official CLaRa (*Dong et al., 2024*, Apple AI/ML Research), training is structured into three sequential phases:

```
┌─────────────────────────┐     ┌──────────────────────────────────┐     ┌─────────────────────────┐
│         STAGE 1         │     │             STAGE 2              │     │         STAGE 3         │
│ Salient Compressor      │ ──► │ Compression Instruction Tuning   │ ──► │ End-to-End Joint        │
│ Pretraining (SCP)       │     │ (--stage stage1_2)               │     │ Fine-Tuning             │
│ (--stage stage1)        │     │ train_instruction_tuning.sh      │     │ (--stage stage2)        │
└─────────────────────────┘     └──────────────────────────────────┘     └─────────────────────────┘
      [Done in A2]                        [SKIPPED in A2;                       [Done in A2;
                                           ADDED in A3 via                       ABLATED in A3 via
                                         train_it_nested.py]                    train_e2e_a3.py]
```

- **Assignment 2 (A2)** skipped Stage 2 entirely, transitioning directly from SCP pretraining to End-to-End training.
- **Assignment 3 (A3)** incorporates Stage 2 via `train_it_nested.py` (termed Stage 1.5 in the pipeline scripts) to study whether compression instruction tuning benefits our nested continuous memory architecture.

---

## 2. What We Kept (Matches Official `stage1_2`)

Our implementation in `train_it_nested.py` faithfully retains the core optimization design of official CLaRa (`apple/ml-clara`, commit `ee93341`):

1. **Same Two Adapter-Training Modes:**
   - In official `train_sft.py` (`_setup_lora_adapters`), Stage 2 (`stage1_2`) either activates only the `decoder_adapter` (generator-only) or both `encoder_adapter + decoder_adapter` (compressor + generator).
   - This corresponds exactly to our `--train_compressor 0/1` switch in `train_it_nested.py`.
   - In both codebases, `query_reasoner_adapter` is left untouched (retrieval ranking is not trained during this stage, consistent with providing a pre-ranked candidate document list).
2. **Same Loss Formulation:**
   - Official CLaRa computes $\mathcal{L} = \mathcal{L}_{\text{CE}}(\text{answer}) + 0.1 \cdot \mathcal{L}_{\text{MSE}}$ inside `SFTTrainer` (`mse_loss_weight = 0.1 if args.mse_loss else 0.0`, enabled via `--mse_loss` in `scripts/train_instruction_tuning.sh`).
   - This matches our default loss weighting $\lambda = 0.1$ (`args.lambda_mse = 0.1`) exactly.
3. **Same Learning Rate:**
   - The official shell script `scripts/train_instruction_tuning.sh` overrides the script default (`5e-6`) with `--learning_rate 1e-4`.
   - This matches our `train_it_nested.py` default learning rate $\eta = 10^{-4}$ (`--lr 1e-4`), optimized with AdamW and linear decay.
4. **Untouched Retrieval / Selection Mechanics:**
   - Neither the official Stage 2 nor our Stage 1.5 modifies retrieval selection parameters during this stage.

---

## 3. What We Changed (Deviations, Innovations & Discrepancies)

A systematic line-by-line comparison against `apple/ml-clara` reveals six key technical differences:

### 1. Nesting Itself (Core Algorithmic Innovation)
- **Official CLaRa:** Trains exclusively on a single, static compression budget (e.g., fixed 16 vectors per document). There is no prefix loop.
- **Our Implementation:** We introduce multi-prefix loss averaging across all nested truncation lengths $m \in \{4, 8, 16, 32\}$ per document:
  $$\mathcal{L}_{\text{IT}} = \frac{1}{|\mathcal{P}|} \sum_{m \in \{4, 8, 16, 32\}} \left( \mathcal{L}_{\text{CE}}\left(y \mid \mathbf{M}_{1:k}[:m], q\right) + \lambda \cdot \mathcal{L}_{\text{MSE}}^{(m)} \right)$$
  Evaluated with four sequential backward passes per training instance (`retain_graph=True` until the final prefix) to keep peak VRAM low.
- **Why It Matters:** This is the primary novel contribution of `train_it_nested.py` (not a mere port). It guarantees that when downstream budget heads allocate uneven memory across documents (e.g., $[32, 16, 8, 8]$), truncated sub-prefixes remain expressive and well-calibrated.

### 2. MSE Anchor: Symmetrical vs. One-Directional Stop-Gradient
- **Official CLaRa:** Computes MSE symmetrically without stop-gradient:
  `F.mse_loss(non_mem_mean, mem_mean)`
  where `non_mem_mean` is the mean of the passage's own non-memory hidden states from the same forward pass (`modeling_clara.py:567–586`). Because gradients flow into both terms, the official MSE loss can pull the passage encoding toward the memory representations, not just the memory toward the passage.
- **Our Implementation:** Formulates a one-directional anchor with explicit stop-gradient:
  $$\mathcal{L}_{\text{MSE}}^{(m)} = \frac{1}{k} \sum_{i=1}^k \left\| \frac{1}{m}\sum_{j=1}^m \mathbf{M}_{i, j} - \text{sg}\left(\frac{1}{T_i}\sum_{t=1}^{T_i} \mathbf{h}_{i, t}\right) \right\|_2^2$$
  where $\text{sg}(\cdot)$ stops gradients into the raw document hidden states $\mathbf{h}_{i, t}$.
- **Why It Matters:** Strictly treats the uncompressed passage representation as an immutable ground-truth target, preventing unwanted drift in passage feature representations.

### 3. Document Count ($k=4$ vs. Official $k=5$)
- **Official CLaRa:** `scripts/train_instruction_tuning.sh` sets `--generation_top_k 5` (5 documents per query).
- **Our Implementation:** Uses $k=4$ documents (gold supporting passages + top BM25 negative distractors).
- **Why It Matters:** A deliberate choice to maintain architectural consistency with our End-to-End training and evaluation setup ($k=4$, aggregate budget $B=64$). This is a deliberate deviation from official default rather than an internal inconsistency.

### 4. Training Epochs (1 Epoch vs. Official 2 Epochs)
- **Official CLaRa:** `train_sft.py` defaults to `max_epochs=2` and `train_instruction_tuning.sh` does not override it. Official Stage 2 runs for 2 full epochs over $\le 500$ examples.
- **Our Implementation:** `train_it_nested.py` trains for 1 epoch (`--epochs 1`).
- **Why It Matters:** A deliberate, compute-budget-driven deviation. We train over our full training set ($>10{,}000$ examples) for 1 epoch, which provides sufficient optimization steps while preventing overfitting and excessive compute cost.

### 5. Generator Adapter Initialization (Continued from SCP vs. Fresh)
- **Official CLaRa:** When `load_adapters=True`, official Stage 2 adds a fresh `encoder_adapter` / `decoder_adapter` pair with random LoRA initialization rather than continuing the generator adapter from Stage 1 SCP.
- **Our Implementation:** By default, continues the generator adapter directly from the pre-trained SCP checkpoint (`--generator_init scp`). We provide a `--generator_init fresh` flag to replicate official behavior.
- **Why It Matters:** In our experiments (scripts 13 and 17), we ran the "continues from SCP" variant. This retains the QA and syntactic generation capabilities acquired during SCP pretraining, accelerating convergence.

### 6. Training Data Construction (Retriever BM25 Rank Order vs. Fixed Doc Set)
- **Official CLaRa:** Training instances (`example/instruction_tuning_data.jsonl`) are constructed from a static pre-retrieved document set without explicit rank ordering.
- **Our Implementation:** Dynamically ranks documents per training question by BM25 score (`--doc_order bm25`), placing gold and negative distractors in realistic retriever rank positions.
- **Why It Matters:** Exposes the generator attention layers to realistic positional biases matching inference-time retrieval outputs.

---

## 4. Systematic Comparison Matrix

| Dimension | Official CLaRa (`apple/ml-clara`) | Our Implementation (`train_it_nested.py`) | Classification |
| :--- | :--- | :--- | :--- |
| **Commit Baseline** | `ee93341` (`train_sft.py`, `modeling_clara.py`) | Standalone implementation | Grounded Reference |
| **Tuned Adapter Modes** | Decoder-only OR Encoder+Decoder | `--train_compressor 0` OR `--train_compressor 1` | **Kept (Identical)** |
| **Loss Formulation** | $\text{CE}(\text{answer}) + 0.1 \cdot \text{MSE}$ | $\text{CE}(\text{answer}) + 0.1 \cdot \text{MSE}$ ($\lambda = 0.1$) | **Kept (Identical)** |
| **Learning Rate** | $\eta = 10^{-4}$ (shell script override) | $\eta = 10^{-4}$ (`--lr 1e-4`, AdamW) | **Kept (Identical)** |
| **Query Reasoner** | Frozen / Untouched in Stage 2 | Frozen / Untouched in Stage 1.5 | **Kept (Identical)** |
| **Memory Nesting** | None (Single fixed rate, e.g. 16 vec) | **Nested Multi-Prefix:** Averaged over $m \in \{4,8,16,32\}$ | **Changed (Novelty)** |
| **VRAM Backprop** | Single full forward/backward graph | **Sequential Accumulation:** Per-prefix backward with `retain_graph` | **Changed (Efficiency)** |
| **MSE Stop-Gradient** | Symmetrical (no stop-gradient; gradients flow to passage) | **One-Directional:** `stop_gradient` on passage hidden states | **Changed (Stability)** |
| **Context Length $k$** | $k = 5$ (`--generation_top_k 5`) | $k = 4$ (Gold + BM25 distractors) | **Changed (Design Choice)** |
| **Epoch Count** | 2 epochs (`max_epochs=2` in `train_sft.py`) | 1 epoch (`--epochs 1` over full dataset) | **Changed (Budget Choice)** |
| **Generator LoRA Init** | Fresh random LoRA weights | **Continues from SCP generator** (default) | **Changed (Continuity)** |
| **Document Ordering** | Static unordered set | Explicit BM25 retriever rank order | **Changed (Realism)** |

---

## 5. Key Empirical Finding: Why Generator-Only Tuning (`itgen`) Is Essential

A central discovery of our Assignment 3 experiments is that **jointly tuning the compressor during Stage 2 breaks retrieval performance**:

### The Problem: Latent Representation Drift
In CLaRa, continuous document memory vectors $\mathbf{M}$ serve two competing roles:
1. **Retrieval Index Keys:** Matched against query reasoner vectors via inner-product similarity.
2. **Generation Soft Prompts:** Consumed autoregressively by the decoder to produce answers.

When the compressor is updated on answer cross-entropy, the memory vectors shift to maximize text likelihood. This causes severe **representation drift**, warping the metric space required for nearest-neighbor retrieval.

### Quantitative Evidence (3 Seeds, `a3_it_comparison.md`)

| Model Configuration | HotpotQA F1 (@64) | 2Wiki Hit@1 (%) | 2Wiki Hit@2 (%) | 2Wiki All-Gold@2 (%) |
| :--- | :---: | :---: | :---: | :---: |
| **A2 Baseline (No Stage 2)** | 19.8 | 67.6 | 85.9 | 23.0 |
| **A3 Joint IT (Compressor + Generator)** | 20.6 | **34.2** *(Collapsed)* | **56.5** | **4.6** |
| **A3 Generator-Only IT (`itgen`)** | **21.0** *(+1.2)* | **68.3** *(Preserved)* | **84.7** | **21.7** |

- On 2WikiMultiHopQA, Hit@1 dropped by over 33 points (from $67.6\%$ to $34.2\%$). In seed 44, Hit@1 collapsed to **$15.7\%$**, performing substantially worse than random guessing ($24.9\%$).
- **The Solution:** Decoupling Stage 2 by freezing the compressor LoRA and document memory tokens (`--train_compressor 0`, `itgen`) completely avoids this degradation. Retrieval Hit@1 is fully preserved ($68.3\%$) while still conferring generation gains on HotpotQA (**+1.2 F1** and **+2.6 Exact Match**).

---

## 6. End-to-End Stage (Stage 3): Resolving the Official CLaRa Gap

To resolve why our pipeline outperformed official CLaRa in Assignment 2 (+3.8 F1), we conducted controlled ablations on **3,000 2Wiki questions** (`a3_ablations_2wiki_big.md`):

| Setting Tested | F1 | EM | $\Delta$F1 vs Baseline [95% CI] | Primary Finding |
| :--- | :---: | :---: | :---: | :--- |
| **Ours Baseline ($\eta = 5\times 10^{-5}, \tau = 0.5$)** | **35.7** | **31.2** | — | Pipeline reference |
| Official E2E lr ($\eta = 5\times 10^{-6}$) | 33.4 | 29.5 | **$-2.4$ [$-3.8, -1.0$]** | **Explains 2.4 of the 3.8 F1 gap**; official lr is too conservative |
| Official Temperature ($\tau = 0.02$, with NaN fix) | **37.9** | **32.7** | **$+2.1$ [$+1.0, +3.2$]** | Official temp is superior, but was unusable due to NaN bug |
| Both Official Settings Combined | 33.3 | 29.5 | **$-2.4$ [$-3.9, -1.0$]** | Low lr dominates and suppresses temperature gains |
| Official SCP Target (`allqa`) | 35.4 | 30.6 | **$-0.3$ [$-1.7, +1.1$]** | Target format makes negligible difference (within noise) |
| Official CLaRa Reference Code | 31.9 | 29.0 | **$-3.8$ [$-5.4, -2.3$]** | Baseline reference |

### The Straight-Through Top-$k$ NaN Bug and Fix
- **The Bug:** In official CLaRa and our A2 code, sampling without replacement penalized picked documents with $\log(1 - \text{taken} + 10^{-9}) \approx -20.7$. At $\tau = 0.02$, cosine differences scaled by $1/\tau$ exceed $30 > 20.7$. Argmax selects the same document again, making $1 - \text{taken} < 0$, which causes $\log(\text{negative}) \to \text{NaN}$.
- **Our Fix (`train_e2e_a3.py:366`):** Replaced the heuristic penalty with exact boolean masking:
  `logits = (scores / tau).masked_fill(taken, float("-inf"))`
  This makes any temperature numerically stable, enabling the $+2.1$ F1 gain from $\tau = 0.02$.

