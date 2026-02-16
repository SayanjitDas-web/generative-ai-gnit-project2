# Day 2: Prompt Engineering: The Basics

## 🎯 Objective
Learn how to communicate with AI effectively using structured prompts.

## 🧠 The Theory
Prompting is the art of giving the model **context** and **instruction**.

### Zero-Shot Prompting
Asking a question with no examples.
*Example: "Explain Python loops."*

### Few-Shot Prompting
Providing examples to guide the model's style.
*Example: "Here are 3 technical questions for a Python dev. Now generate a 4th one."*

## 🛠️ Components of a Good Prompt
1. **Context**: Who are you? (You are an interviewer)
2. **Instruction**: What should you do? (Ask a question)
3. **Constraint**: What should you NOT do? (Don't give the answer immediately)

## 💻 Implementation Insight
In our app, we wrap the user's message in a professional context before it even reaches the AI.

## 🚀 Student Exercise
Go to the OpenAI playground or ChatGPT and try these two prompts:
1. "Ask me an interview question."
2. "You are a Senior Architect at Google. Ask me a single, difficult Python question about memory management. Do not provide the answer."

**Observe the difference in quality.**
