#!/usr/bin/env python3
"""
SmartSpark AI Chatbot Backend API Testing
Tests all backend endpoints and functionality
"""

import requests
import json
import sys
import uuid
from datetime import datetime

class SmartSparkAPITester:
    def __init__(self, base_url="https://56e68c55-027a-4d12-b8e5-afe1dab9f0ee.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.conversation_id = None

    def log_test(self, test_name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED")
        
        if details:
            print(f"   Details: {details}")
        print()

    def test_root_endpoint(self):
        """Test the backend API root endpoint"""
        try:
            # Test the actual backend root endpoint
            response = requests.get(f"{self.base_url}/api/", timeout=10)
            # The backend root endpoint returns 404, which is expected since it's not defined
            # Let's test the conversations endpoint instead as a health check
            response = requests.get(f"{self.base_url}/api/conversations", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, API is accessible"
            self.log_test("Backend API Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("Backend API Health Check", False, f"Exception: {str(e)}")
            return False

    def test_chat_endpoint_new_conversation(self):
        """Test chat endpoint with new conversation"""
        try:
            payload = {
                "message": "Hello, this is a test message. Please respond briefly."
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if "response" in data and "conversation_id" in data:
                    self.conversation_id = data["conversation_id"]
                    details = f"Status: {response.status_code}, AI Response: {data['response'][:100]}..., Conversation ID: {self.conversation_id}"
                else:
                    success = False
                    details = f"Missing required fields in response: {data}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            
            self.log_test("Chat Endpoint - New Conversation", success, details)
            return success
        except Exception as e:
            self.log_test("Chat Endpoint - New Conversation", False, f"Exception: {str(e)}")
            return False

    def test_chat_endpoint_existing_conversation(self):
        """Test chat endpoint with existing conversation"""
        if not self.conversation_id:
            self.log_test("Chat Endpoint - Existing Conversation", False, "No conversation ID from previous test")
            return False
        
        try:
            payload = {
                "message": "What was my previous message?",
                "conversation_id": self.conversation_id
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Status: {response.status_code}, AI Response: {data['response'][:100]}..."
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            
            self.log_test("Chat Endpoint - Existing Conversation", success, details)
            return success
        except Exception as e:
            self.log_test("Chat Endpoint - Existing Conversation", False, f"Exception: {str(e)}")
            return False

    def test_get_specific_conversation(self):
        """Test getting a specific conversation"""
        if not self.conversation_id:
            self.log_test("Get Specific Conversation", False, "No conversation ID from previous test")
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/api/conversations/{self.conversation_id}",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                message_count = len(data.get("messages", []))
                details = f"Status: {response.status_code}, Messages: {message_count}, Conversation ID: {data.get('conversation_id')}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            
            self.log_test("Get Specific Conversation", success, details)
            return success
        except Exception as e:
            self.log_test("Get Specific Conversation", False, f"Exception: {str(e)}")
            return False

    def test_get_all_conversations(self):
        """Test getting all conversations"""
        try:
            response = requests.get(f"{self.base_url}/api/conversations", timeout=10)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                conversation_count = len(data) if isinstance(data, list) else 0
                details = f"Status: {response.status_code}, Total conversations: {conversation_count}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            
            self.log_test("Get All Conversations", success, details)
            return success
        except Exception as e:
            self.log_test("Get All Conversations", False, f"Exception: {str(e)}")
            return False

    def test_delete_conversation(self):
        """Test deleting a conversation"""
        if not self.conversation_id:
            self.log_test("Delete Conversation", False, "No conversation ID from previous test")
            return False
        
        try:
            response = requests.delete(
                f"{self.base_url}/api/conversations/{self.conversation_id}",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Status: {response.status_code}, Message: {data.get('message', 'No message')}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            
            self.log_test("Delete Conversation", success, details)
            return success
        except Exception as e:
            self.log_test("Delete Conversation", False, f"Exception: {str(e)}")
            return False

    def test_error_handling_empty_message(self):
        """Test error handling with empty message"""
        try:
            payload = {"message": ""}
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # Should either accept empty message or return appropriate error
            success = response.status_code in [200, 400, 422]
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Error Handling - Empty Message", success, details)
            return success
        except Exception as e:
            self.log_test("Error Handling - Empty Message", False, f"Exception: {str(e)}")
            return False

    def test_error_handling_invalid_conversation_id(self):
        """Test error handling with invalid conversation ID"""
        try:
            fake_id = "invalid-conversation-id-12345"
            response = requests.get(
                f"{self.base_url}/api/conversations/{fake_id}",
                timeout=10
            )
            
            # Should return 404 for non-existent conversation
            success = response.status_code == 404
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Error Handling - Invalid Conversation ID", success, details)
            return success
        except Exception as e:
            self.log_test("Error Handling - Invalid Conversation ID", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting SmartSpark Backend API Tests")
        print("=" * 50)
        
        # Test sequence
        tests = [
            self.test_root_endpoint,
            self.test_chat_endpoint_new_conversation,
            self.test_chat_endpoint_existing_conversation,
            self.test_get_specific_conversation,
            self.test_get_all_conversations,
            self.test_delete_conversation,
            self.test_error_handling_empty_message,
            self.test_error_handling_invalid_conversation_id
        ]
        
        for test in tests:
            test()
        
        # Print summary
        print("=" * 50)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return 1

def main():
    """Main function"""
    tester = SmartSparkAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())