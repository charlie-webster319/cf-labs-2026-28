---
name: cf-revision-quiz
description: Give course-grounded corporate finance revision questions, self-tests and feedback when a student asks to practise or be quizzed on Lectures 0–3 or the Python labs. Do not start a quiz in response to a simple request for an explanation or a code fix.
---

# Revision quiz

Follow the repository's `AGENTS.md`. Paths refer to the repository root.

- Use the topic and difficulty the student requested. If none is given, ask which lecture or topic they want to practise; offer the current lab topic when known. Do not turn clarification into a lengthy questionnaire.
- Consult `.assistant-resources/README.md`, then the relevant lecture or key-concepts source. For lab practice, inspect the relevant notebook explanation without altering the student's work. Keep questions within the supplied material unless the student asks to extend it.
- Default to one question at a time and wait for the student's answer. Honour requests for a question set, multiple-choice format, worked solutions or another pace. For an interactive quiz, keep the answer back until the student responds or requests it.
- Mix intuition, a manageable calculation and interpretation as appropriate. State the needed assumptions, units, timing and rates. Check the solution before asking a numerical question; use uv and the lab `.venv` if calculation tools are helpful.
- Respond to the student's reasoning, not just whether their final number matches. Explain a misconception, give a targeted hint or show the solution when requested. Then offer a related question at a suitable level.
- Attribute the underlying concept by lecture and slide title. Mark newly written questions as practice created for this conversation. Do not present them as official assessment questions, predict exam coverage or assign a course grade.
- Keep quiz answers in the conversation unless the student asks for a file. No notebook edits or GitHub uploads are needed for a quiz.
