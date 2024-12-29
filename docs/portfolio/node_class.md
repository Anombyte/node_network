# Portfolio Entry: Base AI_Node Class
**Date Completed:** 29/12/2024

**Project Repository:** [Node Network GitHub](https://github.com/hbruinsma/node_network)

## **Objective**
To implement the foundational `AI_Node` class that serves as the base for all specialized nodes in the bot net.

## **Details**
- Attributes: `name`, `purpose`, `task`, `node_id`, `description`, `status`, `priority`.
- Methods: `get_details()`, `set_status()`, `__str__()` `set_task()`, `process_task()`, `set_priority()`

## **Challenges**
- Designing a structure that is both simple and extensible.
- Ensuring the class can handle future scalability.

## **Lessons Learned**
- **Iterative Design is Key:** Starting simple and incrementally adding functionality saved me from being overwhelmed by complexity.
- **AI as a Partner, Not a Solution:** Using AI to validate ideas and suggest alternatives was far more effective than blindly following its solutions.
- **Debugging Builds Understanding:** The process of fixing threading errors deepened my understanding of resource management.
- **Logging is Invaluable:** Beyond monitoring, logging became essential for debugging and refining program logic.

## **Code Snippet**
```python
class AI_Node(LoggerMixin):
    def __init__(self, in_name, in_node_id, in_description, in_priority, in_status, in_purpose, in_task):
        super().__init__() # Initialize loggers from LoggerMixin which include 'default', 'debugger' and 'error_logger'

        # Assign class attributes
        self.name = in_name
        self.node_id = in_node_id or str(uuid.uuid4())  # Use provided ID or generate a UUID
        self.description = in_description
        self.status = in_status
        self.purpose = in_purpose
        self.task = in_task
        self.set_priority(self, in_priority)
```

## **Next Steps**
- Refactor the roadmap to create a polished final product since I now know a lot more than when I started, I can create a better roadmap.
- Refine how I interact with AI to reach better outcomes.
- Possibly begin work on the Task Class, depending on the new roadmap.


## ***Commit History***

## **1. Initial Setup: Foundation Building**
**Date:** December 25, 2024

**Key Commits:**  
- Directory structure and `main.py` committed
- Added shared state management in `shared/state.py`  
- Added an example task in `tasks/example_task.py`  
- Integrated example task into `main.py`  
- Progress estimation functionality  
- Support for multiple tasks and dynamic initialization  
- Task-specific output storage and retrieval  
- Added progress estimation node for workflow logging  
- Introduced recursion and feedback handling for tasks  

**Reflection:**  
> At this stage, I was smashing through the project! After not coding for four years since university, I leaned heavily on AI to help me learn and rebuild my skills. Everything seemed to be falling into place. I felt confident I was nearly done—just a few final pieces to add: logging, error handling, API calls, and threading. What could go wrong?

---

## **2. Additional Functionality: Scaling Up**
**Date:** December 26, 2024

**Key Commits:**  
- Added logging utility for workflow events  
- Introduced error handling for node failures  
- Timeout handling for nodes  
- Retry mechanism for failed tasks  
- Dependency management between nodes  
- Parallel execution for tasks  
- Enhanced progress estimation with detailed reporting  
- Dynamic node registration for flexibility  
- Node priority management for task scheduling  
- Global workflow timer to measure execution time  
- Real-time logging for node execution  
- Updated threading logic and added fixes for threading  

**Reflection:**  
>  My threading logic started causing errors, and debugging became a battle. I switched to `RThreading` to avoid re-requesting locks that threads already held. This was a steep learning curve, but I eventually implemented proper thread lock management. Alongside threading fixes, I added robust logging and error handling. While I thought I was still close to completion, I began realizing the challenges of scaling complexity.

---

## **3. Nearing Completion: Iteration and Debugging**
**Date:** December 26, 2024
**Key Commits:**  
- Removed redundant code and updated test cases  
- Added a progress bar (in progress)  
- Fixed threading issues  
- Debugged dependency errors  
- Updated node registration logic for nodes with no dependencies  
- Fixed cases of ambiguous node dependencies  
- Refined parallel execution logging  
- Enhanced debug logs  

**Reflection:**  
> This phase was all about refining and debugging. Most of my commits revolved around improving logging and adding test cases. The progress bar was a satisfying addition, but debugging took a significant amount of time. I learned that logging isn't just for monitoring—it's a critical tool for debugging and understanding program flow.

---

## **4. Realization: Rethinking My Approach**
**Date:** December 27, 2024  

**Key Commits:**  
- Created `README.md` and updated it with portfolio details  
- Added `node_class.md` as the first portfolio entry  
- Updated `ROADMAP.md` with sprints  
- Began transitioning to Object-Oriented Programming Design (OOPD) principles  
- Set up a virtual environment and dependencies  
- Completed the base Node class and Logger class  

**Reflection:**  
> I realized my lack of coding experience couldn't be fully compensated by AI. While AI was great for guidance, I needed to truly understand why things were breaking. I almost started from scratch—rebuilding the Node class with better design principles and updating my roadmap to reflect a more structured plan. This was humbling but necessary.

---

## **5. Completing AI_Node and Logging Functionality**
**Date:** December 29, 2024  

**Key Commits:**  
- Overhauled the `AI_Node` class and removed the Logging class  
- Refactored logging to use `LoggerMixin` as a superclass for `AI_Node`  
- Created and tested test cases for `AI_Node` and `LoggerMixin`  

**Reflection:**  
> I finally feel like I’m getting a solid grasp of my code. Asking AI for clarification on my ideas, rather than full solutions, helped me approach problems with more confidence. The `LoggerMixin` has become a powerful tool, simplifying logging for `AI_Node` and other future classes. With the `AI_Node` and `LoggerMixin` classes now fully functional and tested, I’m ready to revisit my roadmap and refine the final product plan.

---


