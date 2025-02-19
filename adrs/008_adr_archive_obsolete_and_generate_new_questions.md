# Architectural Decision Record (ADR)

## 1. Title
**AI-Driven Identification and Generation of Exam Content Based on Industry Trends**

---

## 2. Context

### **Current Challenge**
Certifiable, Inc. aims to maintain **up-to-date and relevant exam content** by evaluating **existing aptitude questions and architecture case studies** against **modern industry trends**. 

Manually identifying **obsolete content** and generating **new questions/case studies** is **time-intensive and inconsistent**. The need for **automation** arises due to:
- **Industry Evolution**: Architectural best practices frequently change (e.g., microservices, serverless computing).  
- **Scalability**: Handling a growing database of exam content requires **automated checks**.  
- **Quality Assurance**: New questions should align with **real-world practices** while maintaining **exam difficulty standards**.  

### **Available Options**
1. **Manual Updates**  
   - Rely solely on **experts** to remove outdated questions and generate new ones.  
2. **Basic Keyword Matching**  
   - Use **static rule-based** filtering to detect outdated questions and auto-generate new ones.  
3. **AI-Powered Industry Trend Evaluation & Content Generation (Chosen Approach)**  
   - Utilize **retrieval-augmented generation (RAG)** with an **LLM** to evaluate and update exam content dynamically.

### **Key Constraints**
- **Data Trustworthiness**: Only ingest **verified** industry sources (e.g., Thoughtworks Radar, IEEE whitepapers).  
- **Latency Considerations**: The **scheduled service** must be efficient but also support **on-demand execution**.  
- **Accuracy & Reliability**: AI-generated questions must meet **certification standards** and **pass human validation** when needed.  

---

## 3. Decision

### **Chosen Approach**
Implement an **automated pipeline** for **evaluating outdated content** and **generating new** exam questions and case studies. The system will:

1. **Build a Data Pipeline**  
   - Ingest **industry trends** from sources like **Thoughtworks Radar, IEEE whitepapers, and vetted blogs**.  
   - Ensure that content is **relevant and license-compliant**.  

2. **Generate Embeddings Using SBERT & Store in Vector DB**  
   - Convert industry articles into **semantic embeddings** for efficient **trend retrieval**.  
   - Store in a **vector database** for fast similarity searches.  

3. **Build a RAG Model to Identify Trends**  
   - Classify trends as **"new" vs. "obsolete"** based on time relevance and best practices.  
   - Enable **semantic lookups** for content comparison.  

4. **Evaluate Existing Exam Content Against Trends**  
   - A **new scheduled service** fetches **questions & case studies** from the **exam database**.  
   - The service can also be **triggered manually (on-demand)** for expert queries.  

5. **LLM Identifies Outdated Content & Explains Why**  
   - The **LLM** evaluates each question and determines if it **references obsolete practices**.  
   - Outputs a **brief explanation** justifying why a question should be removed/updated.  

6. **LLM Generates New Questions Based on Trends**  
   - The same **LLM** proposes **new, up-to-date** questions and case studies **aligned with industry trends**.  

7. **Lightweight Evaluator Assigns Confidence Scores**  
   - Measures **semantic similarity** between new and old content.  
   - Ensures the newly generated question **accurately represents** the intended topic.  

8. **AI Guardrails Validate Quality, Accuracy, and Relevance**  
   - Ensures AI-generated content **meets quality standards** (no hallucinations, irrelevant concepts, or factually incorrect statements).  

9. **Auto-Update or Expert Review Based on Confidence**  
   - If **confidence is high**, the question is **automatically updated** in the database.  
   - Otherwise, it is **flagged for human review** before final acceptance.  

### **Why This Approach?**
- **Automation + Control**: Ensures **continuous content updates** while maintaining **expert oversight**.  
- **Improved Accuracy**: RAG-based classification ensures **reliable** outdated-content detection.  
- **Scalability**: Works as a **batch job** but also supports **real-time validation on-demand**.  
- **Better Exam Quality**: New content is **aligned** with **real-world architectural trends** rather than static, outdated knowledge.

### **Rejected Alternatives & Trade-offs**
| **Alternative**           | **Reason for Rejection** |
|---------------------------|-------------------------|
| **Manual Updates**        | Not scalable, requires excessive expert effort. |
| **Keyword Matching**      | Static rules fail to capture **semantic** meaning, leading to false positives. |
| **Fully AI-Generated**    | AI needs **human oversight** to prevent hallucinations or factual inaccuracies. |

---

## 4. Architecture Impact

### **New Components**
1. **Industry Trends Data Pipeline**  
   - Fetches architecture trends from **trusted sources** (blogs, research papers, whitepapers).  

2. **SBERT Embedding & Vector Store**  
   - Converts text into **semantic embeddings** for **trend classification & retrieval**.  

3. **RAG System**  
   - Labels architectural trends as **new vs. obsolete** based on a **retrieved knowledge base**.  

4. **Scheduled & On-Demand Analysis Service**  
   - Fetches existing exam content, runs **AI-powered outdatedness detection**, and suggests replacements.  

5. **LLM-Powered Question Evaluation & Generation**  
   - Identifies **outdated** questions & **creates new** ones based on industry trends.  

6. **Lightweight Evaluator & AI Guardrails**  
   - Ensures newly generated content meets **accuracy, clarity, and quality standards**.  

### **Integration Points**
- **Existing Exam Database**: The service must interface with the **Aptitude Test & Case Study Databases**.  
- **Vector Store for Trends**: Stores **embedded knowledge** for retrieval & classification.  
- **AI Content Validation**: Ensures that AI-generated content is **usable and reliable**.  

### **Performance Considerations**
- **Latency**: The **scheduled service** must process large volumes efficiently.  
- **Storage Efficiency**: The **vector store** must periodically **prune outdated** embeddings.  
- **Retrieval Speed**: Query execution time must remain **low** to ensure fast classification.  

---

## 5. Risks & Mitigation

| **Risk**                                 | **Impact**                                                | **Mitigation Strategy**                                      |
|------------------------------------------|----------------------------------------------------------|-------------------------------------------------------------|
| **False Positives in Outdated Detection** | AI may incorrectly flag **valid** questions.             | Implement **confidence thresholds** and **human review**.   |
| **Bias in Training Data**                 | AI-generated content may favor specific trends.          | Train on **diverse** architecture sources.                  |
| **LLM Hallucinations**                    | AI may generate **incorrect or misleading** questions.   | Validate output via **Guardrails AI & Evaluator**.          |
| **Performance Load on Retrieval**         | RAG may slow down if dataset size increases.             | Optimize **vector search indexing** for faster lookup.      |

---

## 6. Monitoring & Validation

### **Success Metrics**
- **Detection Accuracy**: AI correctly identifies **≥90%** of outdated questions.  
- **Content Freshness**: Percentage of exam content updated yearly.  
- **LLM Generation Success**: New questions meet **expert approval ≥80%** of the time.  
- **Retrieval Performance**: RAG lookup time remains **below X milliseconds**.

### **Monitoring Tools**
- **Trend Drift Detection**: Periodic evaluation of **new vs. obsolete** topics.  
- **Expert Feedback Dashboard**: Experts can review flagged content before removal.  
- **Performance Metrics**: Track **query latency** and **storage efficiency**.

### **Iteration Plan**
- **Phase 1**: Implement **manual validation pipeline** before full automation.  
- **Phase 2**: Deploy AI-powered evaluation with **confidence-based thresholds**.  
- **Phase 3**: Optimize **retrieval performance** & **retrain models periodically**.  

---

## 7. Acceptance Criteria

1. **Correctness**: Outdated content detection is **≥90% accurate**.  
2. **Relevance**: Newly generated questions align with **modern architecture trends**.  
3. **Efficiency**: Retrieval latency remains **low**.  
4. **Expert Review Pass Rate**: **80%+ auto-generated questions** pass human validation.

---

## 8. Implementation Plan

1. **Develop Data Ingestion Pipeline**  
2. **Train SBERT & RAG Model**  
3. **Deploy Scheduled & On-Demand Analysis Service**  
4. **Integrate AI Guardrails & Expert Review Process**  
5. **Monitor Performance & Improve Iteratively**  

---

## 9. Decision Status
**Accepted** - Scheduled for implementation in the next release cycle.

---

## 10. Related Documents
- **ADR "002_adr_claude_llm"** 
- **ADR "005_adr_guardrails"**
