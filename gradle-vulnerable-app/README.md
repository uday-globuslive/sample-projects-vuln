# Gradle Vulnerable Application

This is a vulnerable Java application built with Gradle, created for SCA (Software Composition Analysis) scanning.

## Intentional Vulnerabilities

The project includes the following vulnerable dependencies:

1. **Log4j 2.8.1** - CVE-2021-44228 (Log4Shell) - Remote Code Execution
2. **Struts 2.3.15.1** - CVE-2017-9805 - Remote Code Execution via REST Plugin
3. **Spring Framework 4.2.0** - CVE-2016-5007 - Path Traversal
4. **Jackson Databind 2.6.6** - CVE-2017-4995 - Unsafe Deserialization
5. **Commons Collections 4.0** - CVE-2015-6420 - Gadget Chain vulnerability
6. **Apache HTTP Client 4.3.5** - CVE-2015-4852 - Null Pointer Dereference

## Building

```bash
gradle clean build
```

## Scanning with Trivy

```bash
trivy fs .
```

Or scan the generated JAR:

```bash
gradle clean build
trivy image --input build/libs/gradle-vulnerable-app-1.0-SNAPSHOT.jar
```

## Scanning with OWASP Dependency-Check

```bash
dependency-check.sh --project "Gradle-Vulnerable-App" --scan .
```

## Scanning with Snyk

```bash
snyk test
```
