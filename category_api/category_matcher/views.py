from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .sys import CategoryMatcher
from category_api.settings import BASE_DIR

# Create your views here.
import logging

logger = logging.getLogger(__name__)
csv_filepath=BASE_DIR/'data.csv'

@api_view(['GET'])
def match_category(request):
    try:
        search_query = request.data.get('query')
        if not search_query:
            raise ValueError("No search query provided.")
        matcher = CategoryMatcher(data_path=csv_filepath, nlp_model="en_core_web_md")
        result_category = matcher.get_category_for_search_query(search_query)
        return Response({"category": result_category})
    
    except ValueError as ve:
        '''logger.error(f"Value Error: {ve}")'''
        return Response({"error": str(ve)}, status=400)
    except Exception as e:
        '''logger.error(f"General Error: {e}")'''
        return Response({"error": "Something went wrong. Please try again later."}, status=500)
    