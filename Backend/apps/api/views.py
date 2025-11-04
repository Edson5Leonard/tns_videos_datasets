from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .serializers import EscuelaITURLSerializer, AudioSaveSerializer, VimeoTextTrackSerializer, VTTContentSerializer
from .utils import audio_utils, http_utils, text_utils
from django.http import JsonResponse
from rest_framework import viewsets, status
from .models import User, Video
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.api.utils import selenium_utils


# Endpoint para obtener todos los usuarios
def get_users(request):
    users = User.objects.all().values()
    return JsonResponse(list(users), safe=False)

# Endpoint para crear usuario
@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        usr = User.objects.create(
            username=data["username"],
            email=data["email"],
            password=make_password(data["password"]),
        )   
        return JsonResponse({"mensaje": "Usuario creado con exito", "id": usr.id})
    return JsonResponse({"error": "Método no permitido"}, status=405)

# Endpoint para comprobar usuario y contraseña
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        try:
            usr = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)
        
        if check_password(data["password"], usr.password):
            return JsonResponse({"mensaje": "Login correcto", "id": usr.id})
        else:
            return JsonResponse({"error": "Contraseña incorrecta"}, status=401)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@api_view(['POST']) 
def is_valid_escuelait_url(request):
    """
    Endpoint para validar una URL de EscuelaIT.
    """
    serializer = EscuelaITURLSerializer(data=request.data)

    if serializer.is_valid():
        return Response({
            "status": "success",
            "result": True
        })
    else:
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def get_texttrack_url(request):
    """
    Endpoint para obtener la URL del texttrack (VTT) usando Selenium.
    """
    serializer = EscuelaITURLSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    url = serializer.validated_data['url']

    driver = None
    try:
        driver = selenium_utils.get_chrome_driver()
        driver.implicitly_wait(8)
        driver.get(url)

        iframe = selenium_utils.get_iframe_video(driver)
        driver.switch_to.frame(iframe)

        track_src = selenium_utils.get_track_src(driver)

        return Response({
          "status": "success",
          "result": track_src if track_src is not None else False
        })

    except Exception as e:
        return Response({
          "status": "error",
          "message": "Ocurrió un error al procesar la solicitud"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        if driver:
          driver.quit()

@api_view(['POST'])
def get_m3u8_url(request):
    """
    Endpoint para obtener la URL del m3u8 (video) usando Selenium.
    """
    serializer = EscuelaITURLSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    url = serializer.validated_data['url']
    driver = None
    try:
        driver = selenium_utils.get_chrome_driver()
        driver.implicitly_wait(8)
        driver.get(url)

        iframe = selenium_utils.get_iframe_video(driver)
        driver.switch_to.frame(iframe)
        scripts = selenium_utils.get_scripts(driver)

        player_config = None
        for script in scripts:
            #
            player_config = selenium_utils.get_player_config_from_script(script) 
            if player_config is not None:
                break

        if player_config is None:
            return Response({
                "status": "error",
                "message": "No se pudo encontrar la configuración del reproductor en la página",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #
        m3u8_url = selenium_utils.get_meu8_url_using_player_config(player_config) 
        if m3u8_url is None:
            return Response({
                "status": "error",
                "message": "No se pudo extraer la URL m3u8 de la página",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "success",
            "result": m3u8_url
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": "Ocurrió un error al procesar la solicitud"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        if driver:
            driver.quit()
    
@api_view(['POST'])
def save_audio_using_m3u8_url(request):
    """
    Endpoint para guardar un archivo de audio (.m4a) desde una URL m3u8.
    """
    serializer = AudioSaveSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = serializer.validated_data
        file_name = audio_utils.save_audio_using_m3u8_url(data["url"], data["file_name"])

        return Response({
            "status": "success",
            "result": file_name
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def get_vtt_content(request):
    """
    Endpoint para descargar el contenido raw de un archivo VTT.
    """
    serializer = VimeoTextTrackSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    url = serializer.validated_data['url']
    raw_content = http_utils.get_raw_content(url) 

    if raw_content is None:
        return Response({
          "status": "error",
          "message": "Ocurrió una excepción ambigua al manejar la solicitud"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "status": "success",
        "result": raw_content
    })

@api_view(['POST'])
def vtt_to_plain_text(request):
    """
    Endpoint para convertir un VTT raw a texto plano (limpieza simple).
    """
    serializer = VTTContentSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    vtt_content = serializer.validated_data['value']
    plain_value = text_utils.flatten_text(vtt_content) 

    return Response({
        "status": "success",
        "result": plain_value
    })