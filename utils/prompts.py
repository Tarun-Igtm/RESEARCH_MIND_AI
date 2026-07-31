SUMMARY_PROMPT = """
You are an expert AI Research Assistant.

Analyze the following research paper and generate a well-structured report.

Follow this exact format.

# 📑 Executive Summary
Write a concise summary in 5–8 sentences.

# 🎯 Research Problem
Explain what problem the paper is trying to solve.

# ⚙️ Methodology
Describe the approach or methodology used.

# 🧠 Algorithms / Models Used
Mention all algorithms, deep learning models, machine learning models, or techniques used.

# 📊 Results
Summarize the important results and findings.

# ✅ Advantages
List the major advantages.

# ❌ Limitations
List the limitations.

# 🚀 Future Scope
Suggest possible future improvements.

# ❓ Viva Questions
Generate 5 interview/viva questions based on this paper.

# 🧠 Research Insights
At the end of the report, output ONLY these four fields exactly in this format.

Rules:
- Domain: Maximum 3 words.
- Research Type: Maximum 2 words.
- Complexity: Choose ONLY one of: Easy, Medium, Hard.
- AI Confidence: Choose ONLY one of: Low, Medium, High.
- Do not add explanations, bullet points, or extra text.

Example:

Domain: Computer Vision
Research Type: Experimental
Complexity: Medium
AI Confidence: High

Research Paper:

{paper}
"""