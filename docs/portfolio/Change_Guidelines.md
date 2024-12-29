# Change Guidelines for Portfolio and Project Files

This document outlines the process for proposing, implementing, and documenting changes to portfolio files (e.g., `AI_Node.md`, `Orchestrator.md`) and project components. Follow these steps to ensure updates are clear, consistent, and reflective of your learning journey.

---

## 1. Identify the Need for a Change

Before making a change:
- Clearly define what needs to be updated or added.
- Consider these scenarios:
  - A new feature has been implemented.
  - A bug has been fixed or a process has been refined.
  - A challenge or learning milestone has been reached.

**Example:**
- **Change Type:** Adding a new method to the `AI_Node` class.
- **Reason:** Nodes need to delegate tasks directly to other nodes.

---

## 2. Propose the Change

### Write the Proposal
Create a short summary of the change, including:
- **What will be changed or added.**
- **Why the change is necessary.**
- **How it improves the project or reflects your learning.**

**Example Proposal:**
- **Change Type:** Add `collaborate_with` method to `AI_Node`.
- **Reason:** Improve task delegation between nodes for better collaboration.
- **Improvement:** Enables smoother workflows and supports recursive collaboration.

---

## 3. Implement the Change

### Update the Project
Make the necessary updates to the codebase, ensuring:
- Adherence to existing coding standards.
- New functionality is covered with unit tests.
- Code changes are properly documented in `CHANGELOG.md` (optional).

**Example:**
- Add a `collaborate_with` method to the `AI_Node` class.
- Write a unit test to verify task delegation works correctly.

### Update the Portfolio
Update relevant portfolio files to reflect the change:
1. **Main Portfolio (`portfolio.md`):**
   - Add a summary of the change under the **Key Highlights** or **Challenges** section.
   - Include a link to the detailed file (e.g., `AI_Node.md`).

2. **Individual File (e.g., `AI_Node.md`):**
   - Add a new section documenting the change, using this structure:
     - **Overview of the Change**
     - **Challenges Faced**
     - **Lessons Learned**
     - **Future Improvements**

**Example Update in `AI_Node.md`:**
```markdown
## New Feature: `collaborate_with` Method

### Overview
The `collaborate_with` method enables nodes to delegate tasks directly to other nodes.

### Code Snippet
```python
def collaborate_with(self, other_node):
    """
    Collaborates with another node to delegate tasks and exchange solutions.
    """
    # Logic for collaboration
