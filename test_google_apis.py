#!/usr/bin/env python3
"""
Test script to verify Google API key permissions
Tests both Generative AI and Speech-to-Text APIs
"""

import requests
import json
import base64
import os

# Your API key
API_KEY = "AIzaSyBqeGWFquFCnadrpjsptexJG0nGSrhFVcU"

def test_generative_ai():
    """Test Google Generative AI API"""
    print("🤖 Testing Google Generative AI API...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content("Hello, say 'API is working!'")
        print(f"✅ Generative AI API: SUCCESS")
        print(f"📝 Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Generative AI API: FAILED")
        print(f"📝 Error: {str(e)}")
        return False

def test_speech_to_text():
    """Test Google Speech-to-Text API using REST API"""
    print("\n🎤 Testing Google Speech-to-Text API...")
    
    # Create a simple test audio data (base64 encoded silence)
    # This is a minimal WAV file with 1 second of silence
    test_audio_b64 = "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="
    
    url = f"https://speech.googleapis.com/v1/speech:recognize?key={API_KEY}"
    
    payload = {
        "config": {
            "encoding": "WEBM_OPUS",
            "sampleRateHertz": 48000,
            "languageCode": "en-US"
        },
        "audio": {
            "content": test_audio_b64
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Speech-to-Text API: SUCCESS")
            result = response.json()
            print(f"📝 Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print("❌ Speech-to-Text API: FAILED")
            print(f"📝 Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Speech-to-Text API: FAILED")
        print(f"📝 Error: {str(e)}")
        return False

def test_speech_to_text_simple():
    """Test if Speech API is accessible at all"""
    print("\n🔍 Testing Speech-to-Text API accessibility...")
    
    url = f"https://speech.googleapis.com/v1/operations?key={API_KEY}"
    
    try:
        response = requests.get(url)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Speech-to-Text API is accessible")
            return True
        elif response.status_code == 403:
            print("❌ Speech-to-Text API: ACCESS DENIED (403)")
            print("🔧 This means the API key doesn't have permission for Speech-to-Text")
            error_data = response.json()
            print(f"📝 Error details: {json.dumps(error_data, indent=2)}")
            return False
        else:
            print(f"❌ Speech-to-Text API: Unexpected status {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Speech-to-Text API test failed")
        print(f"📝 Error: {str(e)}")
        return False

def main():
    print("🔑 Google API Key Test Script")
    print("=" * 50)
    print(f"Testing API Key: {API_KEY[:20]}...")
    print("=" * 50)
    
    # Test Generative AI
    genai_success = test_generative_ai()
    
    # Test Speech-to-Text accessibility
    speech_accessible = test_speech_to_text_simple()
    
    # Test Speech-to-Text functionality
    speech_success = test_speech_to_text()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print(f"🤖 Generative AI API: {'✅ WORKING' if genai_success else '❌ FAILED'}")
    print(f"🎤 Speech-to-Text API: {'✅ WORKING' if speech_success else '❌ FAILED'}")
    
    if not speech_success:
        print("\n🔧 RECOMMENDATIONS:")
        print("1. Enable Cloud Speech-to-Text API in Google Cloud Console")
        print("2. Check API key restrictions")
        print("3. Ensure billing is enabled for your project")
        print("4. Visit: https://console.cloud.google.com/apis/library/speech.googleapis.com")

if __name__ == "__main__":
    main()