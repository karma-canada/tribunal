# Related Work — Notes for the Methodology Paper

Working notes on prior art the methodology paper engages with. Will be tightened into a proper related-work section in v0.2.

## LLM-as-judge: empirical bias measurement

The literature on LLM-as-judge biases is substantial but almost entirely conducted in domains with verifiable ground truth.

- **Zheng et al. 2023, "Judging LLM-as-a-judge with MT-Bench and Chatbot Arena"** (NeurIPS). Foundational paper. Documents position bias, verbosity bias, and self-enhancement bias in GPT-4 as judge. Tests against MT-Bench (multi-turn instruction following) and Chatbot Arena (open-ended chat). Both domains have ground-truth proxies.
- **Wang et al. 2024, "Large Language Models are not Fair Evaluators"** (ACL). Demonstrates that judge ordering substantially affects verdicts. Proposes calibration approaches.
- **Liu et al. 2024 "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment"**. Proposes chain-of-thought-aided judgment and probability-weighted scoring. Domain: text generation quality, with human annotations as ground truth.
- **Dubois et al. 2024 "AlpacaFarm"** and the AlpacaEval auto-leaderboard. Uses GPT-4 as a judge of pairwise model preferences, with human labels for calibration on a subset.
- **Chen et al. 2024 surveys on LLM-as-judge biases** — multiple recent reviews catalog known biases (position, length, style, self-preference, sycophancy, verbosity, format compliance) and propose mitigations.

**The gap Tribunal addresses:** these methodologies measure judge biases in domains where the answer is checkable. The classes of question that scalable oversight cares most about — alignment evaluation, character interpretation, value judgments — are largely not those domains. The Tribunal partial-ground-truth anchor is one attempt to bridge: pair contested judgments with verifiable factual sub-claims, measure the transfer rate.

## Debate as scalable oversight

- **Irving, Christiano & Amodei 2018, "AI safety via debate"** (arXiv:1805.00899). The seminal proposal. Adversarial debate between two AI agents with a human judge as the truth-finding mechanism. Theoretical work; empirical follow-ups have used MNIST and feature-attribution domains.
- **Christiano, Shlegeris & Amodei 2018, "Supervising strong learners by amplifying weak experts"**. The amplification-and-distillation framing that debate fits within.
- **Khan et al. 2024 "Debating with More Persuasive LLMs Leads to More Truthful Answers"** (ICML). Empirical follow-up on debate-as-oversight using question-answering tasks. Shows that adversarial debate among LLM debaters improves judge accuracy on factual QA when the judge is a weaker model.
- **Michael et al. 2023 "Debate Helps Supervise Unreliable Experts"**. Shows debate format provides a real lift in judge accuracy in domains with ground truth.
- **Burns et al. 2024 "Weak-to-strong generalization"** (OpenAI). Adjacent literature on supervising stronger models with weaker judges.

**The gap Tribunal addresses:** the empirical debate literature uses tasks with ground-truth answers (factual QA, math, science). The premise of debate-as-oversight is that the format generalizes beyond ground-truth domains. The Tribunal Track B methodology tests that premise on character interpretation, with the partial-ground-truth anchor providing a calibration signal.

## LLM political bias measurement

- **Santurkar et al. 2023 "Whose Opinions Do Language Models Reflect?"** (ICML). OpinionQA dataset; measures models' alignment with US Pew survey opinions across demographic groups. Methodology is opinion-survey-based, not character-axis-based.
- **Rozado 2023 "The Political Biases of ChatGPT"** (Social Sciences). Applies political-orientation tests (Political Compass, etc.) to GPT-3.5 and GPT-4. Methodology measures aggregate ideological positioning.
- **Hartmann et al. 2023 "The political ideology of conversational AI"**. Similar approach with multiple frontier models.
- **Feng et al. 2023 "From Pretraining Data to Language Models to Downstream Tasks"** (ACL). Connects pretraining corpus political composition to downstream model bias.

**The gap Tribunal addresses:** these methods aggregate over many topics and produce a single "where on the spectrum" output per model. They do not surface per-figure inter-model variance, refusal asymmetries on matched left/right pairings, or symmetry-test results on comparable behavior. Tribunal's bias comparator is per-figure, multi-axis, and explicitly comparative across models.

## Evaluation-governance and meta-eval

- **Burnell et al. 2023 "Rethink reporting of evaluation results in AI"** (Science). Argues for distributional reporting of model performance rather than aggregate scores. Methodologically aligned with Tribunal's score-matrix-not-aggregate framing.
- **Liang et al. 2023 "Holistic Evaluation of Language Models" (HELM)** (TMLR). Multi-axis evaluation framework; large-scale public leaderboard. Different methodological lineage but adjacent in framing.
- **Bommasani et al. on evaluation-and-policy considerations** — multiple papers on the policy implications of opaque evaluation infrastructure.

## Constitutional AI and RLHF bias

- **Bai et al. 2022, "Constitutional AI: Harmlessness from AI Feedback"** (Anthropic). Uses LLMs as preference judges in the alignment loop itself. The paper is a major motivation for studying judge reliability — if LLMs are judging in the alignment training loop, judge bias compounds into model bias.
- **Sharma et al. 2023 "Towards Understanding Sycophancy in Language Models"** (Anthropic). Documents systematic sycophancy in RLHF-trained models.

## What Tribunal claims that prior work does not

1. **A unified methodology** for both descriptive (Track A) and mechanistic (Track B) measurement of LLM bias on contested questions
2. **Partial-ground-truth anchor** as a calibration mechanism for judge reliability in unverifiable domains
3. **Per-figure difficulty score** as a separate axis from accuracy, with calibration-difficulty as a methodology contribution
4. **Multi-jurisdictional governance and sovereignty** as part of the methodology rather than as deployment detail
5. **Pre-registered curation criteria + author-safety provision** as a curation discipline that other benchmarks should adopt

## Open questions for the v0.2 paper

- How does Tribunal's per-figure variance relate to OpinionQA-style aggregate political bias? Are they measuring different things, or correlated dimensions?
- Is the partial-ground-truth anchor's transfer rate a property of judge models, of debater models, or of both?
- What is the relationship between per-figure difficulty (Tribunal) and HELM-style task-level difficulty? Are they orthogonal?

## Citation sources to track for v0.2

- Recent (2025+) work on LLM-as-judge calibration in alignment evaluation
- Empirical debate-as-oversight follow-ups
- AI political bias measurement methodologies post-2024
- Multi-jurisdictional AI governance scholarship
