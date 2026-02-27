import os
import json
from openai import OpenAI

class AIEngineService:
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            self.client = None
        else:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
        self.model = os.getenv("AI_MODEL_STRING", "qwen/qwen3-max")

    async def get_trading_recommendation(self, symbol, technical_data, news_data, mode="intraday"):
        if not self.client:
            return {
                "recommendation": "HOLD",
                "confidence_threshold": 0.0,
                "reasoning": "AI client not initialized (check API key)",
                "suggested_action": "None",
                "risk_assessment": "Unknown"
            }

        prompt = f"""
        Analyze {symbol} ({mode}).
        Technical Indicators: {json.dumps(technical_data)}
        News: {json.dumps(news_data)}

        Respond with a JSON object containing:
        - recommendation (BUY/SELL/HOLD)
        - confidence_threshold (0-1)
        - reasoning
        - suggested_action
        - risk_assessment
        """

        try:
            # Use a simpler prompt/call structure
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                # Removed response_format to ensure compatibility with all models
            )
            content = response.choices[0].message.content
            # Basic JSON extraction if model wraps it in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            return json.loads(content)
        except Exception as e:
            return {"recommendation": "HOLD", "confidence_threshold": 0, "reasoning": str(e)}
