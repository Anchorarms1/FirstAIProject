import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

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
        Analyze the following data for {symbol} and provide a trading recommendation.
        Mode: {mode} (intraday_swing or long_term)

        Technical Indicators:
        {json.dumps(technical_data, indent=2)}

        Latest News:
        {json.dumps(news_data, indent=2)}

        Provide your response in JSON format with the following keys:
        - recommendation: "BUY", "SELL", or "HOLD"
        - confidence_threshold: 0.0 to 1.0
        - reasoning: Short explanation of your decision
        - suggested_action: "Buy Call", "Buy Put", "Sell Position", or "None"
        - risk_assessment: Low, Medium, High
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst and professional day trader."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"AI Engine Error: {e}")
            return {
                "recommendation": "HOLD",
                "confidence_threshold": 0.0,
                "reasoning": f"Error in AI processing: {str(e)}",
                "suggested_action": "None",
                "risk_assessment": "Unknown"
            }
