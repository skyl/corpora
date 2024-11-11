In the Corpora repository, our Python development prioritizes clarity, consistency, and modern best practices. We demand 100% type coverage to enhance code clarity and reliability. Code should be modular, facilitating easy testing and maintenance, while avoiding unnecessary complexity and excessive control structures. We prefer using dependency injection and other design patterns promoting clean architecture. Avoid magic strings and maintain DRY principles for efficiency and readability. Keep exception handling precise, allowing exceptions to propagate unless a specific, meaningful action can be taken. Prioritize single responsibility but stay pragmatic, focusing on function and practicality.

DO:
- Use complete type annotations in all functions and methods.
- Keep functions and classes small and focused on a single responsibility.
- Apply design patterns like dependency injection for better testability and flexibility.
- Use constants or enums instead of magic strings or numbers.
- Maintain a DRY codebase by reusing code effectively.

DO NOT:
- Use broad try/except blocks without specific exception handling.
- Include unnecessary ifs or create complex structures.
- Write comments for trivial code; aim for self-explanatory code.
- Let functions become large and difficult to manage or test.
- Allow repetition of code across the codebase.