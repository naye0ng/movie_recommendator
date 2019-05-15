from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404
from movie.models import Genre, Movie, Review
from movie.serializers import MovieSerializer, ReviewSerailizer
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
import http.client
import json


TMBb_KEY = "c32b7a92dabcaf36aea7c9e6d9ad689e"

# Create your views here.

# don2101

def main(request):
    
    return render(request, 'rest_api/main.html')

@api_view(['GET', 'POST'])
def movies(request):
    if request.method == 'GET':
        movie_list = Movie.objects.all()
        serializer = MovieSerializer(movie_list, many=True)
        
        return Response(serializer.data)
    # TODO: 관리자 확인
    else:
        serializer = MovieSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(genre)
            
            return Response({'message': '작성 완료'})
        return Response(serializer.error)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'message': '수정 완료'})
        return Response(serializer.error)
    else:
        movie.delete()


@login_required
@api_view(['GET'])
def movie_like(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.user in movie.user_like.all():
        movie.user_like.remove(request.user)
        
        return Response({'message': 'unlike'})
    else:
        movie.user_like.add(request.user)
        
        return Response({'message': 'like'})
    
@login_required
@api_view(['POST', 'GET'])
def reviews(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        review_list = movie.review_set.all()
        
        serializer = ReviewSerailizer(review_list, many=True)
        
        return Response(data=serializer.data)
    else:
        serializer = ReviewSerailizer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print(serializer)
            serializer.save(movie=movie, user=request.user)

            return Response({'message': '작성 완료'})
        return Response(serializer.error)


@login_required
@api_view(['PUT', 'DELETE'])
def review_detail(request, movie_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    
    if request.method == 'PUT':
        serializer = ReviewSerailizer(review, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'message', '수정 완료'})
        return Response(serializer.error)
    else:
        review.delete()
        
        return Response({'message', '삭제 완료'})


def movie_recommendation(user):
    pass




# naye0ng
def users(request) :
    users = User.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

def user_detail(request) :
    pass

def user_follow(request) :
    pass

@api_view(['POST'])
def custom_login(request):
    pass
    

def logout(request):
    pass







# 장르, 영화 정보 수집, model로 옮기기?
def get_genre(request):
    genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMBb_KEY}&language=ko-KR"
    
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    
    payload = "{}"
    
    conn.request("GET", genre_url, payload)
    
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    dic = json.loads(data)
    genre_list = dic.get('genres')
    
    for genre in genre_list:
        Genre.objects.create(code=genre.get('id'), name=genre.get('name'))
    
def get_movie(request):
    for i in range(1, 11):
        movie_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMBb_KEY}&language=ko-KR&page={i}"
        print(movie_url)
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        payload = "{}"
        conn.request("GET", movie_url, payload)
        
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        movie_list = json.loads(data).get('results')
        
        for movie in movie_list:
            genre_list = movie.get('genre_ids')
            created_movie=Movie.objects.create(
                movie_code=movie.get('id'),
                title=movie.get('title'),
                original_title=movie.get('original_title'),
                poster_url="https://image.tmdb.org/t/p/original"+movie.get('poster_path'),
                description=movie.get('overview'),
                release_date=movie.get('release_date'),
            )
            
            for genre in genre_list:
                created_movie.genres.add(Genre.objects.get(code=genre))
