from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from pymongo import MongoClient, WriteConcern
from bson import ObjectId
import bcrypt
from datetime import datetime
from django.conf import settings
import logging
import json

client = MongoClient('mongodb+srv://Alex:Ramurica22@database.ac3uoad.mongodb.net/')
db = client['database']

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        users = db['users']
        
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([username, email, password]):
            return Response(
                {'error': 'Username, email and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if users.find_one({'$or': [
            {'username': username},
            {'email': email}
        ]}):
            return Response(
                {'error': 'Username or email already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'is_admin': False,
            'created_at': datetime.now()
        }
            
        result = users.insert_one(user_data)
        
        return Response({
            'message': 'User created successfully',
            'user_id': str(result.inserted_id)
        })
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        users = db['users']
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"Login attempt for email: {email}")

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = users.find_one({'$or': [
            {'email': email},
            {'username': email} 
        ]})
        
        if not user:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        if password != user['password']:
            return Response(
                {'error': 'Invalid password'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            'user_id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'is_admin': user.get('is_admin', False),
            'token': 'dummy_token'
        })
    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class SupportTicketViewSet(viewsets.ViewSet):
    COLLECTION_NAME = 'Support'
    
    def create(self, request):
        try:
            logger.info("=== START TICKET CREATION ===")
            
            client = settings.MONGO_CLIENT
            db = client[settings.MONGODB_NAME]
            
            collections = db.list_collection_names()
            logger.info(f"Available collections: {collections}")
            
            support = db[self.COLLECTION_NAME]
            
            user_id = request.data.get('user_id')
            if not user_id:
                logger.error("No user_id provided in request data")
                return Response(
                    {'error': 'user_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ticket_data = {
                'user_id': user_id,
                'subject': request.data.get('subject'),
                'description': request.data.get('description'),
                'priority': request.data.get('priority', 'medium'),
                'category': request.data.get('category', 'general'),
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            }
            
            logger.info(f"Inserting into collection: {self.COLLECTION_NAME}")
            logger.info(f"Ticket data: {ticket_data}")
            
            result = support.insert_one(ticket_data)
            logger.info(f"Insert result ID: {result.inserted_id}")
            
            created_ticket = support.find_one({'_id': result.inserted_id})
            if created_ticket:
                created_ticket['_id'] = str(created_ticket['_id'])
                logger.info(f"Successfully created ticket: {created_ticket}")
                return Response(created_ticket, status=status.HTTP_201_CREATED)
            else:
                logger.error("Failed to verify ticket creation")
                return Response(
                    {'error': 'Failed to verify ticket creation'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            logger.error(f"Error creating ticket: {str(e)}")
            return Response(
                {'error': f'Failed to create ticket: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        try:
            logger.info("=== START TICKET LISTING ===")
            db = settings.MONGO_CLIENT[settings.MONGODB_NAME]
            support = db[self.COLLECTION_NAME]
            
            user_id = request.query_params.get('user_id')
            logger.info(f"Fetching tickets for user_id: {user_id}")
            
            if user_id:
                tickets = list(support.find({'user_id': user_id}))
            else:
                tickets = list(support.find())
            
            for ticket in tickets:
                ticket['_id'] = str(ticket['_id'])
            
            logger.info(f"Found {len(tickets)} tickets in {self.COLLECTION_NAME}")
            return Response(tickets)
            
        except Exception as e:
            logger.error(f"Error fetching tickets: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StatisticsViewSet(viewsets.ViewSet):
    COLLECTION_NAME = 'Statistics'
    
    def list(self, request):
        try:
            logger.info("=== FETCHING STATISTICS ===")
            client = settings.MONGO_CLIENT
            db = client[settings.MONGODB_NAME]
            stats_collection = db[self.COLLECTION_NAME]
            latest_stats = stats_collection.find_one(
                sort=[('timestamp', -1)]
            )
            
            if latest_stats:
                latest_stats['_id'] = str(latest_stats['_id'])
                logger.info(f"Found statistics: {latest_stats}")
                return Response(latest_stats)
            else:
                logger.warning("No statistics found in database")
                return Response({
                    'active_trains': 0,
                    'daily_passengers': 0,
                    'revenue_today': 0,
                    'fuel_usage': 0,
                    'passenger_satisfaction': 0,
                    'satisfaction_trend': [],
                    'passenger_traffic': [],
                    'train_status': {},
                    'timestamp': None
                })
                
        except Exception as e:
            logger.error(f"Error fetching statistics: {str(e)}")
            return Response(
                {'error': f'Failed to fetch statistics: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BookingViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            bookings = db['bookings']
            booking_data = {
                'user_id': request.data.get('user_id'),
                'train_number': request.data.get('train_number'),
                'departure': request.data.get('departure'),
                'arrival': request.data.get('arrival'),
                'date': request.data.get('date'),
                'selected_seats': request.data.get('selected_seats', []),
                'status': 'confirmed',
                'created_at': datetime.now()
            }
            result = bookings.insert_one(booking_data)
            return Response({'booking_id': str(result.inserted_id)})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        try:
            bookings = db['bookings']
            user_id = request.query_params.get('user_id')
            
            if user_id:
                query = {'user_id': user_id}
            else:
                query = {}
                
            booking_list = list(bookings.find(query))
            for booking in booking_list:
                booking['_id'] = str(booking['_id'])
                
            return Response(booking_list)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_statistics(request):
    try:
        client = settings.MONGO_CLIENT
        db = client[settings.MONGODB_NAME]
        stats = {
            'total_tickets': db['Support'].count_documents({}),
            'pending_tickets': db['Support'].count_documents({'status': 'pending'}),
            'resolved_tickets': db['Support'].count_documents({'status': 'resolved'}),
            'total_bookings': db['bookings'].count_documents({}),
            'active_bookings': db['bookings'].count_documents({'status': 'confirmed'}),
        }
        
        logger.info(f"Retrieved statistics: {stats}")
        return Response(stats)
        
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        return Response(
            {'error': f'Failed to fetch statistics: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def test_mongodb(request):
    try:
        db = settings.MONGO_CLIENT['database']
        support = db['Support']
        test_doc = {'test': 'api_test', 'timestamp': datetime.now().isoformat()}
        result = support.insert_one(test_doc)
        inserted = support.find_one({'_id': result.inserted_id})
        support.delete_one({'_id': result.inserted_id})
        
        return Response({
            'status': 'success',
            'collections': db.list_collection_names(),
            'test_insert': str(result.inserted_id),
            'verification': bool(inserted)
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'error': str(e)
        })

class StationViewSet(viewsets.ViewSet):
    COLLECTION_NAME = 'Stations'
    
    def list(self, request):
        try:
            client = settings.MONGO_CLIENT
            db = client[settings.MONGODB_NAME]
            stations = db[self.COLLECTION_NAME]
            
            stations_data = list(stations.find({}, {'_id': 0}))
            
            return Response(stations_data)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch stations: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )