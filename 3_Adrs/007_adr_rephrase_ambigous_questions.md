# Architectural Decision Record (ADR)

## 1. Title
**AI-Driven Pipeline for Identifying & Rewriting Ambiguous Aptitude Test Questions**

---

## 2. Context

### Current Challenge
Certifiable, Inc. faces a surge in **ambiguous or outdated exam questions** within its aptitude test database. Relying on human reviewers alone is **time-consuming** and **error-prone**, especially with a projected **5-10x** increase in candidate volume.

### Available Options
1. **Fully Manual Review**  
   - Continue using threshold-based flags and rely on experts to rewrite questions.

2. **Simple AI (One-Step)**  
   - Pass flagged questions directly to an LLM for rewriting without further checks.

3. **Hybrid AI Pipeline (Chosen)**  
   - Use **SBERT** embeddings and a **Random Forest** classifier to identify "bad" questions, then have an LLM (Claude 3.5) rewrite them. A lightweight evaluator and guardrails finalize or flag outputs.

### Key Constraints
- **Scalability**: Must handle large volumes of flagged questions.  
- **Accuracy**: High risk if question quality degrades.  
- **Compliance**: Rewritten questions must remain valid and free of offensive or disallowed content.  
- **Cost Efficiency**: Minimize manual expert load; manage LLM usage costs.

---

## 3. Decision

### Chosen Approach
Adopt a **multi-step AI pipeline**:
1. **Flag High-Failure Questions** via existing threshold-based service.  
2. **Embed** flagged items with **SBERT**.  
3. **Classify** them as "bad" or "good" using a **Random Forest** trained on historical corrections and labeled data.  
4. **Rewrite** "bad" questions using **Claude 3.5** with a tailored prompt.  
5. **Evaluate** the LLM output with a **lightweight LLM evaluator** (SBERT-based scoring) and **Guardrails AI**.  
6. **Auto-Update** if confidence is high; otherwise, prompt **expert review**.

### Why This Approach?
- **Balanced Automation**: Reduces workload while maintaining multiple checks (classifier, evaluator, guardrails).  
- **Scalable**: Handles increasing flagged questions without overwhelming experts.  
- **Robust**: SBERT embeddings enrich both classification and rewriting evaluation steps.

### Rejected Alternatives & Trade-offs
- **Fully Manual Review**  
  - Not scalable; high labor demands.  
- **Simple AI**  
  - Insufficient checks; may rewrite valid questions or fail to detect subtle ambiguity.

---

## 4. Architecture Impact

### New Components
1. **SBERT Embedding Service**: Converts question text into semantic vectors.  
2. **Random Forest Classifier**: Trained to detect ambiguous/"bad" questions.  
3. **Prompt Orchestrator**: Routes "bad" questions to the LLM (Claude 3.5).  
4. **Lightweight Evaluator**: Rates the rewritten text's clarity vs. original question.  
5. **Guardrails AI**: Final compliance screening before auto-update.

### Integration Points
- **Aptitude Test Grade Database**: Continues providing question text and performance data.  
- **Flagging Service**: Maintains threshold-based identification of high-failure questions.  
- **Expert Review UI**: Receives items that fail the automatic pipeline or need manual sign-off.

### Performance Considerations
- **Embedding Overhead**: Generating SBERT vectors for flagged items.  
- **LLM Usage**: Potential cost and latency for rewriting; must be monitored.  
- **Load Spikes**: Each new release cycle may trigger surges in flagged questions.

---

## 5. Risks & Mitigation

| Risk                                  | Impact                                                | Mitigation Strategy                                                    |
|---------------------------------------|-------------------------------------------------------|------------------------------------------------------------------------|
| Over-reliance on LLM rewriting        | Inaccurate or off-topic rewrites                      | Use **lightweight evaluator** + **guardrails** + optional human check  |
| Classification mislabeling            | Could flag valid questions or miss truly "bad" ones   | Periodic **retraining**; gather more labeled data over time            |
| High LLM usage cost                   | Budget overruns if volumes spike                      | **Batch** requests; track usage and fallback to simpler thresholds     |
| Model drift / stale training          | Gradual decline in accuracy                           | **Schedule** retraining; monitor performance metrics                   |

---

## 6. Monitoring & Validation

### Success Metrics
- **Reduced Manual Rewrites**: Decrease in time experts spend editing ambiguous questions.  
- **Improved Clarity**: Drop in candidate confusion or fail rates for previously "bad" questions.  
- **Processing Throughput**: Ability to handle increased flagged questions without major delays.

### Monitoring Tools
- **Dashboard**: Tracks classifier accuracy, LLM usage, guardrails rejections.  
- **Alerts**: Flags anomalies (e.g., sudden surge in rewriting failures).

### Iteration Plan
- **Quarterly retraining** of Random Forest with newly labeled data.  
- **Prompt refinements** for Claude 3.5 if rewriting style or clarity is suboptimal.  
- **Guardrails** updates for new compliance rules or language patterns.

---

## 7. Acceptance Criteria

1. **Operational Stability**: Pipeline runs end-to-end with minimal downtime.  
2. **Accuracy Threshold**: Classifier meets defined precision/recall targets on holdout sets.  
3. **User (Expert) Satisfaction**: Experts report fewer manual interventions.  
4. **Guardrails Efficacy**: Minimal policy violations in newly published questions.

---

## 8. Implementation Plan

1. **Data Labeling**: Combine heuristic-labeled "bad" questions with any manually classified examples.  
2. **SBERT + Classifier Setup**: Integrate embedding, train Random Forest, finalize hyperparameters.  
3. **LLM Orchestrator**: Connect to Claude 3.5, define prompt structure.  
4. **Evaluator & Guardrails**: Implement scoring and compliance checks for reworded text.  
5. **Deployment**: Roll out microservices or endpoints (embedding, classifier, rewriting, evaluation, guardrails).  
6. **Testing**: Start with a subset of flagged questions in a staging environment.

---

## 9. Decision Status
**Accepted** - Approved for implementation.

---

## 10. Related Documents
- **ADR "002_adr_claude_llm"** 
- **ADR "005_adr_guardrails"**
