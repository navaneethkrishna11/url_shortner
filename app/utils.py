"""
Utility functions for URL shortener
"""

import string
import random
import json
import os
from typing import Dict, Tuple

from .config import settings


def generate_short_code(length: int = 6) -> str:
    """Generate a random short code"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def is_valid_url(url: str) -> bool:
    """Basic URL validation"""
    return url.startswith(('http://', 'https://')) and len(url) > 10


def is_valid_custom_code(code: str) -> bool:
    """Validate custom code"""
    return (
        len(code) >= 3 and 
        len(code) <= 20 and 
        code.replace('-', '').replace('_', '').isalnum()
    )


def load_data() -> Tuple[Dict[str, str], Dict[str, int]]:
    """Load data from JSON files"""
    url_storage = {}
    stats_storage = {}
    
    try:
        if os.path.exists(settings.DATA_FILE):
            with open(settings.DATA_FILE, 'r') as f:
                url_storage = json.load(f)
        
        if os.path.exists(settings.STATS_FILE):
            with open(settings.STATS_FILE, 'r') as f:
                stats_storage = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
    
    return url_storage, stats_storage


def save_data(url_storage: Dict[str, str], stats_storage: Dict[str, int]) -> None:
    """Save data to JSON files"""
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(settings.DATA_FILE), exist_ok=True)
        
        with open(settings.DATA_FILE, 'w') as f:
            json.dump(url_storage, f)
        
        with open(settings.STATS_FILE, 'w') as f:
            json.dump(stats_storage, f)
    except Exception as e:
        print(f"Error saving data: {e}")


def get_html_content() -> str:
    """Get the HTML content for the main page"""
    return """
  <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-effect { backdrop-filter: blur(10px); background: rgba(255, 255, 255, 0.95); }
        
        /* Custom responsive breakpoints */
        @media (max-width: 640px) {
            .mobile-padding { padding: 1rem; }
            .mobile-text { font-size: 1.5rem; }
        }
        
        @media (max-width: 480px) {
            .xs-padding { padding: 0.75rem; }
            .xs-text { font-size: 1.25rem; }
        }
    </style>
</head>
<body class="min-h-screen gradient-bg">
    <div class="container mx-auto px-3 sm:px-4 lg:px-6 py-4 sm:py-8">
        <!-- Header -->
        <div class="text-center mb-6 sm:mb-8 lg:mb-12">
            <h1 class="text-2xl xs-text sm:text-3xl md:text-4xl lg:text-6xl font-bold text-white mb-2 sm:mb-4">
                <i class="fas fa-link mr-2 sm:mr-4 text-xl sm:text-3xl md:text-4xl lg:text-6xl"></i>
                <span class="block sm:inline">URL Shortener</span>
            </h1>
            <p class="text-white/80 text-sm sm:text-base md:text-lg lg:text-xl max-w-xs sm:max-w-md md:max-w-lg lg:max-w-2xl mx-auto px-2">
                Transform long URLs into short, shareable links instantly
            </p>
        </div>

        <!-- Main Card -->
        <div class="max-w-xs sm:max-w-md md:max-w-lg lg:max-w-2xl mx-auto glass-effect rounded-xl sm:rounded-2xl shadow-2xl p-4 xs-padding sm:p-6 lg:p-8 mb-4 sm:mb-6 lg:mb-8">
            <form id="urlForm" class="space-y-4 sm:space-y-6">
                <div>
                    <label for="url" class="block text-gray-700 font-semibold mb-1 sm:mb-2 text-sm sm:text-base">
                        Enter your long URL
                    </label>
                    <input 
                        type="url" 
                        id="url" 
                        name="url"
                        placeholder="https://example.com/very-long-url..."
                        class="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-200 rounded-md sm:rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200 text-sm sm:text-base"
                        required
                    >
                </div>
                
                <div>
                    <label for="custom_code" class="block text-gray-700 font-semibold mb-1 sm:mb-2 text-sm sm:text-base">
                        Custom short code (optional)
                    </label>
                    <input 
                        type="text" 
                        id="custom_code" 
                        name="custom_code"
                        placeholder="my-custom-link"
                        class="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-200 rounded-md sm:rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200 text-sm sm:text-base"
                    >
                    <p class="text-gray-500 text-xs sm:text-sm mt-1">3-20 characters, letters, numbers, hyphens, and underscores only</p>
                </div>

                <button 
                    type="submit" 
                    class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-2 sm:py-3 px-4 sm:px-6 rounded-md sm:rounded-lg hover:from-blue-600 hover:to-purple-700 transform transition-all duration-200 hover:scale-105 shadow-lg text-sm sm:text-base active:scale-95"
                >
                    <i class="fas fa-magic mr-1 sm:mr-2"></i>Shorten URL
                </button>
            </form>

            <!-- Loading -->
            <div id="loading" class="hidden text-center py-3 sm:py-4">
                <div class="inline-block animate-spin rounded-full h-5 w-5 sm:h-6 sm:w-6 border-b-2 border-blue-500"></div>
                <span class="ml-2 text-gray-600 text-sm sm:text-base">Creating short URL...</span>
            </div>

            <!-- Result -->
            <div id="result" class="hidden mt-4 sm:mt-6 p-3 sm:p-4 bg-green-50 border border-green-200 rounded-md sm:rounded-lg">
                <h3 class="font-semibold text-green-800 mb-2 text-sm sm:text-base">
                    <i class="fas fa-check-circle mr-2"></i>Success!
                </h3>
                <div class="space-y-2">
                    <div class="flex flex-col sm:flex-row items-stretch sm:items-center space-y-2 sm:space-y-0 sm:space-x-2">
                        <input type="text" id="shortUrl" readonly class="flex-1 px-2 sm:px-3 py-2 bg-white border border-green-300 rounded text-blue-600 font-mono text-xs sm:text-sm min-w-0">
                        <button onclick="copyToClipboard()" class="px-3 sm:px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors text-sm flex-shrink-0 active:bg-blue-700">
                            <i class="fas fa-copy"></i>
                            <span class="ml-1 sm:hidden">Copy</span>
                        </button>
                    </div>
                    <p class="text-green-700 text-xs sm:text-sm break-all">
                        Original: <span id="originalUrl" class="font-mono"></span>
                    </p>
                </div>
            </div>

            <!-- Error -->
            <div id="error" class="hidden mt-4 sm:mt-6 p-3 sm:p-4 bg-red-50 border border-red-200 rounded-md sm:rounded-lg">
                <h3 class="font-semibold text-red-800 mb-2 text-sm sm:text-base">
                    <i class="fas fa-exclamation-circle mr-2"></i>Error
                </h3>
                <p id="errorMessage" class="text-red-700 text-xs sm:text-sm break-words"></p>
            </div>
        </div>

        <!-- Stats -->
        <div class="max-w-xs sm:max-w-md md:max-w-lg lg:max-w-2xl mx-auto glass-effect rounded-xl sm:rounded-2xl shadow-2xl p-4 xs-padding sm:p-6">
            <h3 class="text-lg sm:text-xl font-semibold text-gray-800 mb-3 sm:mb-4 text-center sm:text-left">
                <i class="fas fa-chart-bar mr-2"></i>Statistics
            </h3>
            <div class="grid grid-cols-2 gap-3 sm:gap-4">
                <div class="text-center bg-white/50 rounded-lg p-3 sm:p-4">
                    <div class="text-xl sm:text-2xl font-bold text-blue-600" id="totalUrls">0</div>
                    <div class="text-gray-600 text-xs sm:text-sm font-medium">URLs Shortened</div>
                </div>
                <div class="text-center bg-white/50 rounded-lg p-3 sm:p-4">
                    <div class="text-xl sm:text-2xl font-bold text-green-600" id="totalClicks">0</div>
                    <div class="text-gray-600 text-xs sm:text-sm font-medium">Total Clicks</div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="text-center mt-6 sm:mt-8">
            <p class="text-white/60 text-xs sm:text-sm">
                Made by Navaneeth Krishna
            </p>
        </div>
    </div>

    <script>
        const form = document.getElementById('urlForm');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');
        const error = document.getElementById('error');

        loadStats();

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const url = formData.get('url');
            const custom_code = formData.get('custom_code');

            result.classList.add('hidden');
            error.classList.add('hidden');
            loading.classList.remove('hidden');

            try {
                const response = await fetch('/shorten', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url, custom_code: custom_code || null })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || 'Failed to shorten URL');
                }

                document.getElementById('shortUrl').value = data.short_url;
                document.getElementById('originalUrl').textContent = data.original_url;
                result.classList.remove('hidden');
                
                loadStats();
                form.reset();

            } catch (err) {
                document.getElementById('errorMessage').textContent = err.message;
                error.classList.remove('hidden');
            }

            loading.classList.add('hidden');
        });

        function copyToClipboard() {
            const shortUrl = document.getElementById('shortUrl');
            
            // Modern clipboard API with fallback
            if (navigator.clipboard) {
                navigator.clipboard.writeText(shortUrl.value).then(() => {
                    showCopySuccess();
                }).catch(() => {
                    // Fallback to older method
                    fallbackCopy();
                });
            } else {
                fallbackCopy();
            }
        }

        function fallbackCopy() {
            const shortUrl = document.getElementById('shortUrl');
            shortUrl.select();
            shortUrl.setSelectionRange(0, 99999); // For mobile devices
            document.execCommand('copy');
            showCopySuccess();
        }

        function showCopySuccess() {
            const button = event.target.closest('button');
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i><span class="ml-1 sm:hidden">Copied!</span>';
            button.classList.remove('bg-blue-500', 'hover:bg-blue-600');
            button.classList.add('bg-green-500');
            
            setTimeout(() => {
                button.innerHTML = originalHTML;
                button.classList.remove('bg-green-500');
                button.classList.add('bg-blue-500', 'hover:bg-blue-600');
            }, 2000);
        }

        async function loadStats() {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                document.getElementById('totalUrls').textContent = data.total_urls;
                document.getElementById('totalClicks').textContent = data.total_clicks;
            } catch (err) {
                console.error('Failed to load stats:', err);
            }
        }

        // Add touch feedback for mobile
        document.addEventListener('DOMContentLoaded', function() {
            const buttons = document.querySelectorAll('button');
            buttons.forEach(button => {
                button.addEventListener('touchstart', function() {
                    this.style.transform = 'scale(0.95)';
                });
                button.addEventListener('touchend', function() {
                    this.style.transform = '';
                });
            });
        });
    </script>
</body>
</html>
    """