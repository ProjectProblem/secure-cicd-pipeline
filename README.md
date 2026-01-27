# Secure CI/CD Pipeline with Automated Security Scans

> 🐒 **Looking for a kid-friendly explanation?** Check out the [**Monkey-Friendly README**](MONKEY-README.md) for a fun, easy-to-understand version!

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

1.  **`test`**: Runs unit tests to ensure the application's functionality is correct.
2.  **`codeql-analysis`**: Performs static application security testing (SAST) using CodeQL to find vulnerabilities in the source code.
3.  **`semgrep-scan`**: Runs Semgrep for additional SAST, focusing on security patterns and best practices.
4.  **`dependency-check`**: Scans project dependencies for known vulnerabilities using OWASP Dependency-Check.
5.  **`python-safety-check`**: Checks Python dependencies for security issues with Safety.
6.  **`build`**: Builds the Docker image for the application.
7.  **`trivy-scan`**: Scans the built Docker image for vulnerabilities in the OS and application dependencies.
8.  **`security-gate`**: Acts as a gatekeeper. It checks the results of the security scans and fails the build if any high-severity vulnerabilities are found.
9.  **`deploy-ready`**: A placeholder job that runs only if all previous jobs, including the security gate, are successful. In a real-world scenario, this job would trigger a deployment to a staging or production environment.

## Vulnerability Management

When a vulnerability is found, the pipeline is designed to take the following actions:

-   **Fail the Build**: The `security-gate` job will fail if the `dependency-check` or `trivy-scan` jobs detect high or critical severity vulnerabilities. This prevents vulnerable code from being deployed.
-   **Security Alerts**: CodeQL and Trivy are configured to upload their findings to the GitHub Security tab, providing a centralized view of all vulnerabilities.
-   **Developer Feedback**: The failed pipeline run provides immediate feedback to the developer, indicating which security check failed and why. The logs of the failed job will contain details about the vulnerabilities found.

**Remediation Process**:

1.  **Identify**: The developer reviews the security scan results in the GitHub Actions logs or the Security tab.
2.  **Assess**: The developer assesses the severity and impact of the vulnerability.
3.  **Remediate**: The developer fixes the vulnerability. This might involve updating a dependency, patching the code, or changing a configuration.
4.  **Verify**: The developer pushes the fix to the repository, which triggers the CI/CD pipeline again. The security scans will run again to verify that the vulnerability has been remediated.

## Getting Started

To run this project locally, you need to have Docker installed.

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/ProjectProblem/secure-cicd-pipeline.git
    cd secure-cicd-pipeline
    ```

2.  **Build the Docker image**:

    ```bash
    docker build -t secure-cicd-app .
    ```

3.  **Run the Docker container**:

    ```bash
    docker run -p 5000:5000 secure-cicd-app
    ```

4.  **Access the API**:

    You can now access the API at `http://localhost:5000`.

---

### References

[1] GitHub. (n.d.). *CodeQL*. Retrieved from https://codeql.github.com/

[2] Semgrep. (n.d.). *Semgrep*. Retrieved from https://semgrep.dev/

[3] OWASP. (n.d.). *OWASP Dependency-Check*. Retrieved from https://owasp.org/www-project-dependency-check/

[4] Aqua Security. (n.d.). *Trivy*. Retrieved from https://www.aquasec.com/products/trivy/
