from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any

from app.config.settings import settings

logger = logging.getLogger("ai_service")
logging.basicConfig(level=logging.INFO)


class AIService:
    """Service for interacting with AI APIs (OpenAI/Gemini)."""

    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.gemini_key = settings.GEMINI_API_KEY

    def _extract_json(self, content: str) -> dict[str, Any]:
        if not content:
            return {}

        match = re.search(r"\{.*\}", content, re.DOTALL)
        candidate = match.group(0) if match else content
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return {}

    def _fallback_questions(self, role: str, num_questions: int) -> list[dict[str, str]]:
        templates = [
            ("behavioral", f"Tell me about your experience as a {role}."),
            ("behavioral", f"What makes you a strong fit for a {role} role?"),
            ("technical", "Can you walk me through a recent project you are proud of?"),
            ("technical", "How do you approach debugging a difficult issue?"),
            ("problem-solving", "How do you prioritize when requirements are unclear?"),
        ]
        questions: list[dict[str, str]] = []
        for index in range(num_questions):
            category, text = templates[index % len(templates)]
            if index >= len(templates):
                text = f"Describe a challenge you solved in a {role} context."
            questions.append({"text": text, "category": category})
        return questions

    def _fallback_evaluation(self, question: str, answer: str, role: str) -> dict[str, Any]:
        answer_length = len(answer.strip())
        technical_score = 65.0 if answer_length else 0.0
        communication_score = 70.0 if answer_length > 40 else 55.0
        confidence_score = 68.0 if answer_length > 20 else 50.0
        overall_score = round((technical_score + communication_score + confidence_score) / 3, 1)
        return {
            "technical_score": technical_score,
            "communication_score": communication_score,
            "confidence_score": confidence_score,
            "overall_score": overall_score,
            "feedback": (
                f"Solid start for a {role} interview. Include more specifics, measurable impact, "
                f"and a clearer structure when answering: {question[:120]}"
            ),
        }

    async def _generate_with_openai(self, prompt: str) -> str:
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.openai_key)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Return only valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            text = response.choices[0].message.content or ""
            logger.info("OpenAI response length=%d", len(text))
            return text
        except Exception as e:
            logger.exception("OpenAI generation failed: %s", e)
            raise

    async def _generate_with_gemini(self, prompt: str) -> str:
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = await asyncio.to_thread(model.generate_content, prompt)
            text = getattr(response, "text", "") or ""
            logger.info("Gemini response length=%d", len(text))
            return text
        except Exception as e:
            logger.exception("Gemini generation failed: %s", e)
            raise

    async def _call_llm(self, prompt: str) -> str:
        if self.openai_key:
            try:
                logger.info("Calling OpenAI for prompt (len=%d)", len(prompt))
                return await self._generate_with_openai(prompt)
            except Exception:
                logger.exception("OpenAI call failed, will try Gemini if configured")

        if self.gemini_key:
            try:
                logger.info("Calling Gemini for prompt (len=%d)", len(prompt))
                return await self._generate_with_gemini(prompt)
            except Exception:
                logger.exception("Gemini call failed; falling back to heuristics")

        logger.info("No LLM response; using fallback logic")
        return ""

    async def generate_questions(self, role: str, num_questions: int = 5):
        """Generate interview questions based on role."""
        prompt = (
            f"Generate {num_questions} interview questions for a {role} position. "
            "Return JSON with a 'questions' array. Each item must include 'text' and 'category'. "
            "Use categories like technical, behavioral, or problem-solving."
        )
        content = await self._call_llm(prompt)
        data = self._extract_json(content)
        questions = data.get("questions") if isinstance(data, dict) else None

        if isinstance(questions, list) and questions:
            normalized = []
            for item in questions[:num_questions]:
                if isinstance(item, dict) and item.get("text"):
                    normalized.append(
                        {
                            "text": str(item.get("text")),
                            "category": str(item.get("category", "technical")),
                        }
                    )
            if normalized:
                return normalized

        return self._fallback_questions(role, num_questions)

    async def evaluate_answer(self, question: str, answer: str, role: str):
        """Evaluate answer using AI."""
        prompt = (
            "Evaluate the following interview answer and return JSON only with keys: "
            "technical_score, communication_score, confidence_score, overall_score, feedback. "
            "Scores must be numbers from 0 to 100.\n\n"
            f"Role: {role}\n"
            f"Question: {question}\n"
            f"Answer: {answer}\n"
        )
        content = await self._call_llm(prompt)
        data = self._extract_json(content)

        if data:
            return {
                "technical_score": float(data.get("technical_score", 0)),
                "communication_score": float(data.get("communication_score", 0)),
                "confidence_score": float(data.get("confidence_score", 0)),
                "overall_score": float(data.get("overall_score", 0)),
                "feedback": str(data.get("feedback", "")),
            }

        return self._fallback_evaluation(question, answer, role)
