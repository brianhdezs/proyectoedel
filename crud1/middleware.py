from django.http import HttpResponseForbidden

class ForbiddenURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la IP del cliente y el User-Agent
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')

        # Verificar si hay una sesión activa
        if 'client_info' not in request.session:
            # Guardar la información del cliente en la sesión
            request.session['client_info'] = {'ip_address': ip_address, 'user_agent': user_agent}
        else:
            # Comparar la información actual del cliente con la información de la sesión
            session_info = request.session['client_info']
            if ip_address != session_info['ip_address'] or user_agent != session_info['user_agent']:
                return HttpResponseForbidden("Forbidden: URL no permitida")

        response = self.get_response(request)
        return response
