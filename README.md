# **TheBlueprint - AI-Powered Grading-Feedback & Fraud Detection System**

## **📌 Overview**
This repository contains the complete implementation of an **AI-driven system** for:
- **Automated Short-Answer Grading** using LLMs and structured evaluation.  
- **Automated Case-Study Grading** using GNNs and LLM-as-Judge.  

- **Fraud Detection in Ungraded Test Responses** using anomaly detection techniques.  
- **Expert Review & Guardrails Implementation** to ensure AI fairness and compliance.  

## **📁 Repository Structure**
| Folder | Description |
|--------|------------|
| **[1_Requirements](./1_Requirements/)** | Contains functional & non-functional requirements, assumptions, and constraints. |
| **[2_Architecture_diagrams](./2_Architecture_diagrams/)** | Visual representations of the system architecture, data flow, and component interactions. |
| **[3_Adrs](./3_Adrs/)** | Architectural Decision Records (ADRs) documenting key technical decisions. |
| **[4_Tech_stack](./4_Tech_stack/)** | Documentation on the tools, frameworks, and technologies used in this project. |
| **[5_Code](./5_Code/)** | Implementation of AI grading models, fraud detection modules, APIs, and UI components. |

---

## **📝 Features & Components**
### **1️⃣ AI-Based Short-Answer Grading**
- Uses **Claude 3.5 Sonnet, Gemini 1.5, and GPT-4** for **automated evaluation**.  
- Structured **XML-based prompts** ensure grading consistency.  
- AI assigns **grades, feedback, and confidence scores** to candidate responses.  

### **2️⃣ AI-Powered Fraud Detection**
- Detects **answer collusion** using **FAISS & SBERT embeddings**.  
- Identifies **time-based answer manipulation** via **LSTM models**.  
- Uses **Isolation Forest** for **AI-based anomaly detection**.  

### **3️⃣ Guardrails for AI Validation**
- **Prevents hallucinations** and enforces structured outputs.  
- Uses **Guardrails AI, JSON Schema Validation, and API Middleware**.  
- Ensures **secure AI operations** with **RBAC-based fraud report access**.  

### **4️⃣ Secure Data Processing & Storage**
- Stores **grading results and fraud reports** in **MongoDB**.  
- Encrypts sensitive fraud data using **AES-256 encryption**.  
- **Logs all fraud detection actions** for auditing and compliance.  

---

## **🚀 Installation & Setup**
### **1. Clone the Repository**
```sh
git clone https://github.com/SanjanaKRao/archikatas.git
