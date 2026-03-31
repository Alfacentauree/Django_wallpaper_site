from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wallpaper, Category
from .pexels_api import fetch_pexels_wallpapers, get_curated_wallpapers

class HomeView(View):
    def get(self, request):
        categories = Category.objects.all()
        featured = Wallpaper.objects.filter(is_featured=True).order_by('-created_at')[:8]
        curated = get_curated_wallpapers(21)
        return render(request, 'wallpapers/home.html', {
            'categories': categories,
            'featured': featured,
            'curated': curated,
        })

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', 'nature')
        api_results = fetch_pexels_wallpapers(query=query, per_page=40)
        local_results = Wallpaper.objects.filter(title__icontains=query)
        return render(request, 'wallpapers/search_results.html', {
            'query': query,
            'api_results': api_results,
            'local_results': local_results
        })

class FavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        wall = get_object_or_404(Wallpaper, pk=pk)
        if request.user in wall.favorites.all():
            wall.favorites.remove(request.user)
        else:
            wall.favorites.add(request.user)
        return redirect(request.META.get('HTTP_REFERER', 'home'))
