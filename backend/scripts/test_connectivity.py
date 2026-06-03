import asyncio
import os

from app.config.settings import settings


async def main():
    print("DATABASE_URL:", settings.DATABASE_URL)
    print("OPENAI_API_KEY loaded:", bool(settings.OPENAI_API_KEY))
    print("GEMINI_API_KEY loaded:", bool(settings.GEMINI_API_KEY))

    if not settings.OPENAI_API_KEY and not settings.GEMINI_API_KEY:
        print("No API keys loaded. Create backend/.env first.")
        return

    if settings.GEMINI_API_KEY:
        print("Testing Gemini connectivity...")
        try:
            import google.generativeai as genai

            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = await asyncio.to_thread(model.generate_content, "Reply with a single word: ok")
            print("Gemini response:", getattr(response, "text", ""))
        except Exception as exc:
            print("Gemini error:", repr(exc))

    if settings.OPENAI_API_KEY:
        print("Testing OpenAI connectivity...")
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": "Reply with a single word: ok"},
                ],
                temperature=0,
            )
            print("OpenAI response:", response.choices[0].message.content)
        except Exception as exc:
            print("OpenAI error:", repr(exc))


if __name__ == "__main__":
    asyncio.run(main())
