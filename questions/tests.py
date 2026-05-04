from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from subjects.models import Subject
from questions.models import Question
import json


class QuestionAPITestCase(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create admin user
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.admin_token = Token.objects.create(user=self.admin)
        
        # Create regular user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.user_token = Token.objects.create(user=self.user)
        
        # Create subject
        self.subject = Subject.objects.create(
            name="Data Structures",
            code="DSA"
        )
        
        # Create question
        self.question = Question.objects.create(
            text="What is time complexity of binary search?",
            subject=self.subject,
            difficulty="medium",
            year=2023,
            option_a="O(n)",
            option_b="O(log n)",
            option_c="O(n log n)",
            option_d="O(n²)",
            correct_option="B",
            explanation="Binary search halves the search space"
        )
    
    def test_list_questions_public(self):
        """Test that anyone can list questions"""
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
    
    def test_get_single_question_public(self):
        """Test that anyone can view a single question"""
        response = self.client.get(f'/api/questions/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['text'], "What is time complexity of binary search?")
    
    def test_create_question_admin_only(self):
        """Test that only admins can create questions"""
        question_data = {
            "text": "New question",
            "subject": self.subject.id,
            "difficulty": "easy",
            "year": 2024,
            "option_a": "A",
            "option_b": "B",
            "option_c": "C",
            "option_d": "D",
            "correct_option": "A"
        }
        
        # Try without auth - should fail
        response = self.client.post(
            '/api/questions/',
            data=json.dumps(question_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try as regular user - should fail
        response = self.client.post(
            '/api/questions/',
            data=json.dumps(question_data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.user_token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try as admin - should succeed
        response = self.client.post(
            '/api/questions/',
            data=json.dumps(question_data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.admin_token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_question_admin_only(self):
        """Test that only admins can update questions"""
        update_data = {"difficulty": "hard"}
        
        # Try as regular user - should fail
        response = self.client.put(
            f'/api/questions/{self.question.id}/',
            data=json.dumps(update_data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.user_token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try as admin - should succeed
        response = self.client.put(
            f'/api/questions/{self.question.id}/',
            data=json.dumps({
                "text": self.question.text,
                "subject": self.subject.id,
                "difficulty": "hard",
                "year": 2023,
                "option_a": "O(n)",
                "option_b": "O(log n)",
                "option_c": "O(n log n)",
                "option_d": "O(n²)",
                "correct_option": "B"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.admin_token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_question_admin_only(self):
        """Test that only admins can delete questions"""
        # Try as regular user
        response = self.client.delete(
            f'/api/questions/{self.question.id}/',
            HTTP_AUTHORIZATION=f'Token {self.user_token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try as admin
        response = self.client.delete(
            f'/api/questions/{self.question.id}/',
            HTTP_AUTHORIZATION=f'Token {self.admin_token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify it's deleted
        self.assertFalse(Question.objects.filter(id=self.question.id).exists())
    
    def test_filter_questions_by_subject(self):
        """Test filtering questions by subject"""
        response = self.client.get(f'/api/questions/?subject={self.subject.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
    
    def test_filter_questions_by_difficulty(self):
        """Test filtering questions by difficulty"""
        response = self.client.get('/api/questions/?difficulty=medium')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
    
    def test_question_not_found(self):
        """Test getting non-existent question"""
        response = self.client.get('/api/questions/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
