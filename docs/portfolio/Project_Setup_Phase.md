# Portfolio Entry: Project Setup Phase

**Date Completed:** December 30, 2024  
**Repository:** [Node Network GitHub](https://github.com/hbruinsma/node_network)

---

## **Key Highlights**
- Implemented foundational project setup, including virtual environment configuration, testing setup with pytest, and linting with black and flake8.
- Established CI/CD workflows using GitHub Actions to automate linting and testing.
- Created a `Setup.md` file with instructions, though improvements are planned as the program becomes functional.

---

## **Challenges**
### PYTHONPATH Issue
One major challenge was resolving a `ModuleNotFoundError` for the `shared` module during testing. The issue was due to the `PYTHONPATH` not including the `src/` directory. After troubleshooting, I fixed it by setting the `PYTHONPATH` environment variable:
```bash
$env:PYTHONPATH="$PWD\src"
```
This fix deepened my understanding of Python's module search behavior and reinforced the importance of configuring the environment correctly for multi-directory projects.

## **Lessons Learned**
1. **Importance of Virtual Environments**
- Virtual environments are essential for managing project dependencies and ensuring reproducibility across systems.
2. **Understanding Black and Flake8**
Configuring black for automatic formatting and flake8 for linting improved code quality and helped me follow Python’s PEP 8 guidelines effectively.
3. **How Pytest Works**
Writing and running tests using pytest clarified the significance of unit testing, especially for ensuring code reliability during development.
4. **How ```self``` Works in Classes**
I realized that ```self``` is passed to every method in a Python class, making it essential for accessing instance attributes and methods.

## **Reflections**
This phase taught me the importance of environment setup and the tools required for a robust development workflow. While the program is not yet functional, laying this groundwork will make future development more efficient.

## **Future Improvements**
Revise ```Setup.md``` to better reflect a functional program once more features are implemented.
Add detailed troubleshooting steps, such as handling ```PYTHONPATH``` issues and dependency conflicts.

## **Next Steps**
1. Continue working on core functionality, starting with the orchestrator.
Expand the Setup.md file as the program becomes more robust.
Improve test coverage and documentation to streamline onboarding for future contributors.
