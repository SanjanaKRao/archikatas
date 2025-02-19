**Architectural Decision Record (ADR)**

**1. Title**

**Adoption of AI-Based Fraud Detection Using FAISS, LSTM, and Isolation
Forest**

**2. Context**

Fraudulent activities such as **answer collusion, time-based answer
manipulation, and automated bot submissions** pose risks to the
integrity of the aptitude test system. Currently, there is no automated
fraud detection mechanism, and expert review is manual and
time-consuming.

We need an **AI-based fraud detection system** that:

-   **Detects collusion** (candidates copying answers from each other).

-   **Flags time-based answer manipulation** (candidates modifying
    answers suspiciously).

-   **Identifies bot-like automated submissions**.

-   **Consolidates results for expert review**.

The fraud detection system will analyze data from **two databases**:

1.  **Aptitude Test Ungraded Database** (Stores ungraded MCQ &
    short-answer responses).

2.  **Submission Ungraded Database** (Stores candidate submission
    timestamps and modification history).

A **Fraud Processing Module** will run a **daily cron job** to detect
suspicious activity using multiple AI models and store flagged cases for
**expert review**.

**3. Decision**

We have decided to integrate a fraud detection pipeline using the
following components:

**AI Models Chosen**

  ------------------------------------------------------------------------
  **Fraud Type**        **Detection        **Why This Model?**
                        Method**           
  --------------------- ------------------ -------------------------------
  **Answer Collusion    **FAISS + SBERT**  Detects **semantic similarity**
  (Copy-Pasting)**                         between different candidates\'
                                           responses.

  **Time-Based Answer   **LSTM (Recurrent  Identifies **sequential answer
  Manipulation**        Neural Network)**  changes** over time.

  **AI-Based Fraud      **Isolation Forest Flags **unusual submission
  Detection (Bot        (Anomaly           patterns** (e.g., high-speed
  Detection)**          Detection)**       multiple submissions).
  ------------------------------------------------------------------------

**Workflow**

1.  **Fraud Processing Module** runs a **daily cron job** on **Aptitude
    Test Ungraded Database + Submission Ungraded Database**.

2.  **FAISS (with SBERT embeddings) detects answer collusion**.

3.  **LSTM detects candidates who repeatedly change answers in
    suspicious patterns**.

4.  **Isolation Forest flags bot-like rapid submissions**.

5.  **Flagged cases are stored for expert review**.

6.  **Expert manually verifies fraud alerts before taking action**.

**4. Architecture Impact**

-   **New Components:**

    -   **FAISS Vector Database**: Stores **SBERT-generated embeddings**
        for answer similarity detection.

    -   **LSTM Model**: Tracks **sequential answer modifications** for
        time-based fraud detection.

    -   **Isolation Forest Model**: Detects **bot-like activity** in
        submission logs.

    -   **Fraud Processing Module**: Runs **AI models via a daily cron
        job** and stores flagged results.

    -   **Expert Review Dashboard**: Allows administrators to **verify
        flagged fraud cases**.

-   **Integration Points:**

    -   **FAISS integrates with the Aptitude Test Ungraded Database** to
        **identify similar answers**.

    -   **LSTM uses the Submission Ungraded Database** to **analyze
        suspicious answer modification sequences**.

    -   **Isolation Forest processes both databases** to **detect
        automated answer submission patterns**.

    -   **All flagged fraud cases are stored in the Fraud Review
        Database**.

-   **Performance Considerations:**

    -   FAISS **vector search must return results in \<2 seconds**.

    -   LSTM must efficiently **track sequential answer modifications**.

    -   Isolation Forest must detect anomalies **without excessive false
        positives**.

**5. Risks & Mitigation**

  -----------------------------------------------------------------------------
  **Risk**                       **Impact**   **Mitigation Strategy**
  ------------------------------ ------------ ---------------------------------
  FAISS may falsely flag         Medium       **Set a similarity threshold
  paraphrased answers as                      (e.g., cosine similarity \<
  collusion.                                  0.95)** to reduce false
                                              positives.

  LSTM may misidentify valid     Medium       Fine-tune LSTM **with
  answer modifications as                     expert-verified training data**
  fraudulent.                                 to improve accuracy.

  Isolation Forest may generate  High         **Adjust contamination level** to
  too many false positives for                **optimize anomaly detection
  rapid submissions.                          sensitivity**.
  -----------------------------------------------------------------------------

**6. Acceptance Criteria**

  -----------------------------------------------------------------------
  **Requirement**   **Description**             **Acceptance Threshold**
  ----------------- --------------------------- -------------------------
  **FAISS           Correctly detects copied    **≥ 90% match with
  Accuracy**        answers                     expert-reviewed cases**

  **LSTM Accuracy** Flags manipulated answers   **≥ 85% match with expert
                    correctly                   evaluations**

  **Bot Detection   Flags automated answer      **≥ 80% anomaly detection
  Accuracy**        submissions                 success**

  **Processing      Fraud detection pipeline    **≤ 5 minutes per daily
  Time**            runtime                     batch**

  **Expert Review   Agreement between AI and    **≥ 85% precision in
  Accuracy**        human fraud review          flagged cases**
  -----------------------------------------------------------------------

**7. Implementation Plan**

-   **Phase 1:** Set up FAISS database and SBERT embeddings.

-   **Phase 2:** Train & fine-tune LSTM model for answer modification
    tracking.

-   **Phase 3:** Implement Isolation Forest for bot detection.

-   **Phase 4:** Develop **Fraud Processing Module** to automate fraud
    detection.

-   **Phase 5:** Integrate **Expert Review Dashboard** for fraud
    validation.

-   **Phase 6:** Deploy and monitor fraud detection performance.

**8. Decision Status**

-   🟢 **Accepted** (Implementation in progress).

**9. Related Documents**

-   AI-Based Fraud Detection System Architecture Diagram.

-   FAISS Clustering & Answer Similarity Detection Report.

-   AI Model Performance Evaluation & Threshold Tuning Document.
