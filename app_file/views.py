from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import File
from .serializers import FileSerializer
from .tasks import process_file
import logging

logger = logging.getLogger(__name__)


class FileUploadView(APIView):
    def post(self, request):
        try:
            file_serializer = FileSerializer(data=request.data)

            if file_serializer.is_valid():
                file_serializer.save()

                file_id = file_serializer.instance.id
                result = process_file.delay(file_id)
                task_status = result.status

                if task_status == 'SUCCESS':
                    result_data = result.result
                    logger.info(f"Task executed successfully: {result_data}")
                elif task_status == 'FAILURE':
                    error_message = result.result
                    logger.error(f"Task failed with error: {error_message}")
                else:
                    logger.info("Task is still pending or in the queue")

                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileListView(APIView):
    def get(self, request):
        files = File.objects.all()

        serializer = FileSerializer(files, many=True)

        return Response(serializer.data)
