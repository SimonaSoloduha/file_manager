from celery import shared_task

from .file_handlers import upload_and_process_file
from .models import File


@shared_task
def process_file(file_id):
    try:
        file = File.objects.get(id=file_id)
        result = upload_and_process_file(file.file)

        if result is not None:
            file.processed = True
            file.save()
            return f'File {file_id} processed successfully'
        else:
            raise Exception(f'Error processing file {file_id} {result}')
    except File.DoesNotExist:
        raise Exception(f'File {file_id} does not exist')
