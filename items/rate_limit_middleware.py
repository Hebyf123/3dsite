import logging
from django.core.cache import cache
from django.http import JsonResponse

logger = logging.getLogger('django')

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if not ip:
            return self.get_response(request)

        # Получаем количество запросов от данного IP за определённое время
        request_count = cache.get(ip, 0)
        cache.set(ip, request_count + 1, timeout=60)  # Обнуляем счетчик через 60 секунд

        # Проверяем, не превышен ли лимит запросов
        if request_count > 5:  
            logger.warning(f"Превышен лимит запросов от IP: {ip}")
            return JsonResponse({'error': 'Слишком много запросов'}, status=429)

        response = self.get_response(request)
        return response
