from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Review
from .forms import PhotoForm, ReviewForm

def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'myapp/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    reviews = photo.reviews.all()
    if request.method == 'POST':
        if 'review_form' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.photo = photo
                review.save()
                return redirect('photo_detail', pk=photo.pk)
        elif 'like_review' in request.POST:
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, pk=review_id)
            review.likes += 1
            review.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        review_form = ReviewForm()
    return render(request, 'myapp/photo_detail.html', {'photo': photo, 'reviews': reviews, 'review_form': review_form})

def photo_upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'myapp/photo_upload.html', {'form': form})

def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        photo.delete()
        return redirect('photo_list')
    return render(request, 'myapp/photo_delete_confirm.html', {'photo': photo})

def top_reviews(request):
    reviews = Review.objects.all().order_by('-likes')[:10]  # 추천수 기준으로 상위 10개의 리뷰 가져오기
    return render(request, 'myapp/top_reviews.html', {'reviews': reviews})
