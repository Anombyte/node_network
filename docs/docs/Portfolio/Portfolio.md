# Portfolio: Node Network Project

## Welcome to My Journey

This portfolio documents my journey in building the **Node Network Project**, a collaborative AI system where specialized nodes from various AI models work together to solve complex tasks. Along the way, I’ve learned valuable skills in Python, object-oriented programming, API integration, CI/CD, and more.

I invite you to **follow along** as I share my progress, challenges, and insights in building this project from the ground up.

---

## Table of Contents

1. [Learning and Implementing the AI_Node](AI_Node.md)
2. [Designing and Building the Orchestrator](Orchestrator.md)
3. [Developing the Feedback Model](Feedback_Model.md)
4. [Integrating CI/CD and Deployment](Final_Deployment.md)
5. [Documentation and Visuals](Documentation_CI_CD.md)

---

## The Vision

The idea behind Node Network is simple:
- Create a system where **AI nodes collaborate recursively**, refining each other's outputs to build better solutions.
- Use **specialized nodes** for distinct tasks like code generation, review, and feedback.
- Continuously learn and improve based on feedback.

---

## My Progress Timeline

### **Phase 1: Learning the Foundations**
- **Goal:** Build the foundation of the project by understanding object-oriented programming and creating the first `AI_Node` class.

### **Phase 2: Experimenting with Collaboration**
- **Goal:** Develop an orchestrator to manage interactions between nodes and enable task delegation.

### **Phase 3: Scaling and Automating**
- **Goal:** Integrate CI/CD pipelines and generate professional documentation.

---

## Key Challenges and Milestones

### **Challenge 1: Designing a Reusable Node**
- **Problem:** How to design a node that could handle various AI models (e.g., GPT, Hugging Face).  
- **Solution:** Implemented a base `AI_Node` class with extensible methods like `process_task` and `collaborate_with`.

---

### **Challenge 2: Debugging CI/CD Failures**
- **Problem:** Early CI pipeline runs failed due to module resolution issues (`ModuleNotFoundError`).  
- **Solution:** Learned about `PYTHONPATH` and added it to the workflow to fix the issue.

---

### **Want to Explore the Details?**
- [Check out the full implementation of the AI_Node class and my thoughts while coding.](AI_Node.md)
- [Learn how I overcame challenges in designing the orchestrator.](Orchestrator.md)

---

## Next Steps

1. Add support for additional AI APIs like Google Gemini.
2. Refine the feedback model with reinforcement learning.
3. Share my project on [GitHub](https://github.com/hbruinsma/node_network) and invite contributions.

---

