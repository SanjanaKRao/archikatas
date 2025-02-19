-- Implement Role-Based Access Control (RBAC)

CREATE TABLE UserRoles (
    user_id INT PRIMARY KEY,
    role VARCHAR(50)
);

CREATE TABLE FraudReports (
    report_id INT PRIMARY KEY,
    fraud_type VARCHAR(255),
    flagged_timestamp TIMESTAMP,
    reviewed_by INT,
    FOREIGN KEY (reviewed_by) REFERENCES UserRoles(user_id)
);

-- Restricting non-admin users from viewing flagged fraud reports
CREATE VIEW AuthorizedFraudReports AS
SELECT * FROM FraudReports
WHERE EXISTS (
    SELECT 1 FROM UserRoles 
    WHERE UserRoles.user_id = FraudReports.reviewed_by 
    AND UserRoles.role IN ('Admin', 'Fraud Reviewer')
);
