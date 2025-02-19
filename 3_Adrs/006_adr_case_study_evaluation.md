# **Architectural Decision Record (ADR) for Introducing the “LLM Judge” Pattern for Case Study Evaluation**

## **1. Title**
Introducing the “LLM Judge” Pattern for Case Study Evaluation

## **2. Context**
The existing architecture for evaluating candidate solutions relies heavily on **manual grading by expert architects**, leading to several challenges:

- **Scalability**: Increasing candidate submissions make **manual review time-intensive**, causing delays in feedback.
- **Consistency and Bias**: Human reviewers, while experienced, may **introduce subjective biases** or inconsistencies.
- **Limited Feedback Cycle**: Candidates often **do not receive detailed or timely explanations** of errors or improvements.
- **Maintainability**: Keeping an up-to-date **golden dataset of best practices** is difficult, requiring frequent rubric updates.

### **Available Options**
- **Option A: Continue Manual Expert Grading Only**
    - **Pros**: Well-understood process; no new technology investment.
    - **Cons**: Does not solve **scalability or speed** issues; continues reliance on **limited expert availability**.

- **Option B: Rule-Based Automated Grading**
    - **Pros**: Suitable for **linting and style checks**.
    - **Cons**: **Inflexible** for conceptual artifacts like **design diagrams**; **high maintenance effort** for updating rules.

- **Option C: LLM-Assisted Grading (“LLM Judge”)**
    - **Pros**:
        - Scalable, able to **process multiple document types in parallel**.
        - Reduces **human bias** with standardized initial grading.
        - Can be **continuously improved** with a golden dataset.
    - **Cons**:
        - **Dependency on LLM availability and correctness**.
        - Requires a **fallback to human grading** in uncertain cases.

After technical and cost evaluation, **Option C (LLM Judge Pattern)** was selected, balancing **automation with expert oversight**.

---

## **3. Decision**
We will integrate an **LLM Judge component** into the **Case Study Evaluation** flow with the following steps:

1. **Document Retrieval and Classification**
    - Submissions are segmented into **ADR, design documents, component diagrams, flow charts, state diagrams, and class diagrams**.

2. **LLM-Based Initial Evaluation**
    - Each document type is passed to a **specialized LLM Judge** that applies **rubric-based checks** (e.g., purpose, correctness, performance).
    - The LLM produces **an initial score and rationale** for the grade.

3. **Human-in-the-Loop Verification**
    - **Expert reviewers validate the LLM’s scoring and rationale** via an **Expert Grading UI**.
    - **Low-confidence LLM responses are flagged** for expert intervention.
    - Expert feedback contributes to a **golden dataset for model improvement**.

4. **Aggregated Scoring**
    - The **LLM scores and expert scores are merged** into a **final weighted score**.
    - Results are stored and presented to candidates and certification records.

### **Why This Approach?**
- The **LLM Judge significantly reduces grading time and costs**, especially during peak exam periods.
- Standardized rubric-based evaluation **improves grading consistency** and reduces reviewer bias.
- Expert intervention is **reserved for complex cases**, improving overall efficiency.
- Continuous **feedback loops improve the model**, refining future grading accuracy.

---

## **4. Architecture Impact**
- **New Components**:
    - **LLM Judge Module** to process and evaluate architectural documents.
    - **Expert Grading UI** for manual validation of flagged cases.
    - **Golden Dataset Storage** for continuous model training and refinement.

- **Integration Points**:
    - The **LLM Judge integrates with the existing submission system** to retrieve candidate responses.
    - **Results from the LLM** are stored in the **grading database** and linked to candidate records.

- **Performance Considerations**:
    - LLM inference latency must be **under 5 seconds per document** to maintain efficiency.
    - Human validation should remain below **10% of total graded submissions** to ensure cost-effectiveness.

---

## **5. Risks & Mitigation**
| **Risk** | **Impact** | **Mitigation Strategy** |  
|----------|-----------|------------------------|  
| LLM may produce incorrect or biased scores | High | **Human verification for flagged cases; feedback loop for model fine-tuning** |  
| High computational cost for LLM inference | Medium | **Optimize batch processing; leverage cost-efficient models** |  
| Experts may not trust AI-generated evaluations | High | **Transparent scoring rationale & expert override system** |  
| Data drift affecting LLM accuracy over time | Medium | **Regular golden dataset updates & performance monitoring** |  

---

## **6. Monitoring & Validation**
- **Success Metrics**:
    - **80%+ agreement** between LLM and expert scores.
    - **<5s response time per grading request**.
    - **Reduction in expert workload by 50%** while maintaining grading accuracy.

- **Monitoring Tools**:
    - **LangFuse for tracking LLM output consistency**.
    - **Post-deployment human audit logs** to validate grading accuracy.

- **Iteration Plan**:
    - **Pilot deployment with limited expert validation** before full rollout.
    - **Collect real-world grading data** to fine-tune model performance.

---

## **7. Acceptance Criteria**
- The **LLM Judge must generate valid, structured grading outputs** with **>80% accuracy**.
- **Human experts must approve at least 90% of LLM-graded responses** without modifications.
- **Flagged low-confidence cases must not exceed 10% of total submissions**.
- **Integration with existing case study grading pipeline** must be seamless.

---

## **8. Implementation Plan**
- **Phase 1: LLM Evaluation & Training**
    - Fine-tune LLM with past expert evaluations and grading rubrics.
- **Phase 2: Integration with Submission System**
    - Connect LLM to retrieve candidate documents and return scores.
- **Phase 3: Expert Review & Validation**
    - Implement Expert Grading UI and feedback loop.
- **Phase 4: Continuous Model Improvement**
    - Collect human-validated scores to refine LLM performance over time.

---

## **9. Decision Status**
Proposed – Awaiting implementation.

---

## **10. Related Documents**
- **LLM Judge Architecture Diagram** – [📊 View Diagram](./2_Architecture_diagrams/llm_judge_architecture.png)
- **Grading Rubric & Evaluation Criteria** – [📄 View Requirements](./1_Requirements/grading_criteria.md)
- **Tech Stack & Infrastructure** – [⚙️ View Tech Stack](./4_Tech_stack/tech_stack.md)

---
