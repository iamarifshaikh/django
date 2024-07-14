from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MovieSerializer, MovieDetailSerializer
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Movies
from mongoengine.errors import NotUniqueError
import logging

logger = logging.getLogger(__name__)

class CreateMovieView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        logger.info(f"Received POST request: {request.data}")
        serializer = MovieSerializer(data=request.data)
        logger.info(f"Serializer created with data: {request.data}")

        if serializer.is_valid():
            try:
                # Check if a movie with the same title already exists
                title = serializer.validated_data['title']
                existing_movie = Movies.objects(title__iexact=title).first()
                if existing_movie:
                    logger.warning(f"Attempt to create duplicate movie title: {title}")
                    return Response(
                        {"error": "A movie with this title already exists."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                movie_instance = Movies(**serializer.validated_data)
                movie_instance.save()
                logger.info(f"Movie created: {movie_instance.title}")
                logger.info(f"Movie details: {movie_instance.to_json()}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except NotUniqueError as err:
                logger.error(f"NotUniqueError creating movie: {str(err)}")
                return Response(
                    {"error": "A movie with this title already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as err:
                logger.error(f"Error creating movie: {str(err)}")
                return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Invalid data for movie creation: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateMovieView(APIView):
    pass

class DeleteMovieView(APIView):
    permission_classes = [AllowAny]
    
    def delete(self, request, pk):
        try:
            movie = Movies.objects.get(id=pk)
            movie.delete()
            logger.info(f"Movie deleted: {pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Movies.DoesNotExist:
            logger.warning(f"Movie not found for deletion: {pk}")
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting movie: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SearchMovieView(APIView):
    pass

class AllMovieListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            movies = Movies.objects.all()
            serializer = MovieDetailSerializer(movies, many=True)
            logger.info("All movies list retrieved")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving all movies: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DetailMovieView(APIView):
    pass