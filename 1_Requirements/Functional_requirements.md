**Functional Requirements**

1.  **User Authentication & Authorization**

    -   The system must authenticate users, including administrators and
        reviewers, ensuring secure access.

    -   Role-based access control (RBAC) must be implemented to restrict
        access to sensitive data, such as flagged fraud reports.

2.  **Feedback Collection & Storage**

    -   The system must collect and store candidate feedback from two
        databases:

        -   Architecture Grade and Feedback Database for Test2
            (Architecture Diagram Test)

        -   Aptitude Test Grade Database for the first test (MCQs and
            short answers)

3.  **Automated Feedback Generation**

    -   The system must analyze collected feedback to generate detailed,
        automated responses for candidates.

    -   AI models should be employed to assess performance and provide
        personalized feedback.

4.  **Fraud Detection Mechanism**

    -   The system must analyze ungraded databases to identify potential
        fraudulent activities, such as:

        -   Answer collusion (e.g., copy-pasting)

        -   Time-based answer manipulation

    -   Detected anomalies should trigger alerts for administrative
        review.

5.  **Administrative Dashboard**

    -   Provide a user interface for administrators to:

        -   Review flagged fraudulent activities

        -   Manage user roles and permissions

        -   Access system logs and reports

6.  **Data Integrity & Security**

    -   Ensure all data transmissions are encrypted.

    -   Implement measures to prevent unauthorized data access or
        modifications.

7.  **System Integration**

    -   Integrate seamlessly with existing databases and AI models.

    -   Ensure compatibility with current infrastructure and workflows.
