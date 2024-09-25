# api/leo.py

import os
import openai
import json

def handler(request):
    try:
        # Only allow POST requests
        if request.method != "POST":
            return {
                "statusCode": 405,
                "headers": { "Content-Type": "application/json" },
                "body": json.dumps({"error": "Method Not Allowed. Use POST."}),
            }
        
        # Parse JSON body
        try:
            data = request.json
        except Exception:
            return {
                "statusCode": 400,
                "headers": { "Content-Type": "application/json" },
                "body": json.dumps({"error": "Invalid JSON."}),
            }
        
        purchase_info = data.get("purchase_info")
        if not purchase_info:
            return {
                "statusCode": 400,
                "headers": { "Content-Type": "application/json" },
                "body": json.dumps({"error": "Missing 'purchase_info' in request body."}),
            }
        
        # Configure OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            return {
                "statusCode": 500,
                "headers": { "Content-Type": "application/json" },
                "body": json.dumps({"error": "OpenAI API key not configured."}),
            }
        
        # Generate analysis with OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Leo, a shopping assistant specialized in verifying and analyzing proofs of purchases. "
                        "Given the details of a purchase, identify key information such as items purchased, total amount, "
                        "purchase date, and verify the validity of the proof. The receipt needs to mention royalmount"
                    ),
                },
                {
                    "role": "user",
                    "content": purchase_info,
                },
            ],
            temperature=0.2,
            max_tokens=500,
        )
        
        analysis = response['choices'][0]['message']['content'].strip()
        
        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({
                "purchase_info": purchase_info,
                "analysis": analysis,
            }),
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({"error": f"Internal Server Error: {str(e)}"}),
        }
