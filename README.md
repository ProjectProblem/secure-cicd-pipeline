# Secure CI/CD Pipeline for Python Flask Application

This repository provides a comprehensive example of a secure CI/CD pipeline for a Python Flask application. It integrates various security tools into a GitHub Actions workflow to automate security testing and enforce security gates.

## Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Threat Model](#threat-model)
- [Security Tools](#security-tools)
- [CI/CD Pipeline](#cicd-pipeline)
- [Vulnerability Management](#vulnerability-management)
- [Getting Started](#getting-started)

## Project Overview

The goal of this project is to demonstrate how to build a robust CI/CD pipeline that not only automates the build, test, and integration processes but also incorporates security scanning at multiple stages. This approach, often referred to as DevSecOps, aims to identify and remediate security vulnerabilities early in the development lifecycle.

The sample application is a simple REST API for managing a to-do list. It is built with Flask and containerized with Docker.

## Technology Stack

| Category          | Technology                               |
| ----------------- | ---------------------------------------- |
| **Application**   | Python 3.11, Flask, Gunicorn             |
| **CI/CD**         | GitHub Actions                           |
| **Container**     | Docker                                   |
| **Security**      | CodeQL, Semgrep, OWASP Dependency-Check, Trivy, Safety |

## Threat Model

A threat model is a structured process of identifying and analyzing potential security threats to an application. For this sample API, we consider the following threats based on the STRIDE model:

| STRIDE Category         | Threat Description                                                                                             | Mitigation Strategy                                                                                                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Spoofing**            | An attacker could impersonate a legitimate user to gain unauthorized access to the API.                        | Implement strong authentication and authorization mechanisms (not included in this simple example, but crucial for real-world applications). Use TLS to protect data in transit.      |
| **Tampering**           | An attacker could modify data in transit or at rest, such as altering a task's content.                        | Use checksums and digital signatures to ensure data integrity. Implement proper access controls to prevent unauthorized modifications. Use TLS for data in transit.             |
| **Repudiation**         | A user could deny having performed an action, such as creating or deleting a task.                             | Implement comprehensive logging and auditing to track all API requests and changes.                                                                                              |
| **Information Disclosure** | An attacker could gain access to sensitive information, such as other users' tasks or system details.          | Enforce strict access controls. Sanitize all user inputs to prevent injection attacks (e.g., SQL injection, NoSQL injection). Avoid exposing sensitive information in error messages. |
| **Denial of Service (DoS)** | An attacker could flood the API with requests, making it unavailable to legitimate users.                      | Implement rate limiting and throttling to control the number of requests from a single client. Use a web application firewall (WAF) to filter malicious traffic.                  |
| **Elevation of Privilege** | An attacker could exploit a vulnerability to gain higher privileges than intended, such as admin access. | Run the application with the least possible privileges (non-root user). Keep all dependencies and the base container image up-to-date to patch known vulnerabilities.             |

## Security Tools

This pipeline uses a combination of security tools to provide a multi-layered defense. Each tool has a specific purpose:

| Tool                    | Type                    | Why It Was Chosen                                                                                                                                                                                                                                                                                       |
| ----------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CodeQL**              | SAST                    | Developed by GitHub, CodeQL offers deep, semantic code analysis to find a wide range of security vulnerabilities. It has excellent integration with GitHub Actions and can block pull requests if new vulnerabilities are introduced. Its powerful query language allows for custom security checks. [1] |
| **Semgrep**             | SAST                    | Semgrep is a fast, open-source static analysis tool that excels at finding security issues based on code patterns. It is highly customizable and can be used to enforce an organization's specific coding standards. It complements CodeQL by catching different types of issues. [2]          |
| **OWASP Dependency-Check** | Dependency Scanning     | This tool from OWASP is a widely recognized standard for identifying known vulnerabilities in project dependencies (Software Composition Analysis - SCA). It supports a wide range of languages and has a comprehensive vulnerability database. [3]                                             |
| **Safety**              | Dependency Scanning     | Safety specifically checks Python dependencies for known security vulnerabilities. It provides an additional layer of security for the Python ecosystem.                                                                                                                                    |
| **Trivy**               | Container Scanning      | Trivy is a simple and comprehensive vulnerability scanner for containers. It can detect vulnerabilities in the OS packages and application dependencies within a Docker image. It is fast, easy to use, and integrates well with CI/CD pipelines. [4]                                       |

## CI/CD Pipeline

The CI/CD pipeline is defined in the `.github/workflows/security-pipeline.yml` file. It consists of the following jobs:

1.  **Unit Tests**: Runs the application's unit tests to ensure basic functionality.
2.  **CodeQL SAST Analysis**: Scans the source code for security vulnerabilities using CodeQL.
3.  **Semgrep SAST Scan**: Performs a static analysis scan with Semgrep.
4.  **OWASP Dependency Check**: Scans third-party dependencies for known vulnerabilities.
5.  **Python Safety Check**: Checks Python dependencies for security issues.
6.  **Build Docker Image**: Builds the Docker image for the application.
7.  **Trivy Container Scan**: Scans the built Docker image for vulnerabilities.
8.  **Security Gate**: A crucial job that checks the results of the previous scans. If any high or critical severity vulnerabilities are found, this job fails, which in turn fails the entire pipeline. This prevents vulnerable code from being deployed.
9.  **Ready for Deployment**: This job only runs if all previous jobs, including the Security Gate, pass successfully. In a real-world scenario, this job would trigger a deployment to a staging or production environment.

## Vulnerability Management

When a vulnerability is found, the pipeline will fail at the **Security Gate**. Here's the process for handling it:

1.  **Notification**: The developer who pushed the code will be notified that the build failed.
2.  **Analysis**: The developer can review the logs from the failing security scan (e.g., Trivy, CodeQL) to understand the vulnerability.
3.  **Remediation**: The developer must fix the vulnerability. This could involve:
    *   Upgrading a dependency to a non-vulnerable version.
    *   Applying a patch.
    *   Rewriting the vulnerable code.
4.  **Re-run Pipeline**: The developer pushes the fix, which automatically triggers the pipeline again.
5.  **Verification**: If the fix is effective, the security scans will pass, the Security Gate will pass, and the pipeline will succeed.

## Getting Started

1.  **Fork this repository**.
2.  **Add the Workflow File**: Manually add the `.github/workflows/security-pipeline.yml` file to your repository.
3.  **Push a Commit**: Make a small change and push it to trigger the workflow.
4.  **Review Results**: Check the **Actions** tab for the workflow run and the **Security** tab for the vulnerability findings.

## References

[1] GitHub. (n.d.). *CodeQL documentation*. [https://codeql.github.com/docs/](https://codeql.github.com/docs/)

[2] Semgrep. (n.d.). *Semgrep documentation*. [https://semgrep.dev/docs/](https://semgrep.dev/docs/)

[3] OWASP. (n.d.). *OWASP Dependency-Check*. [https://owasp.org/www-project-dependency-check/](https://owasp.org/www-project-dependency-check/)

[4] Aqua Security. (n.d.). *Trivy documentation*. [https://aquasecurity.github.io/trivy/](https://aquasecurity.github.io/trivy/)
