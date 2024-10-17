from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from ..models import *
from applications.academic_information.models import Student
from .serializers import PlacementScheduleSerializer, NotifyStudentSerializer
import json


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import JsonResponse

class PlacementScheduleView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        combined_data = []

        notify_students = NotifyStudent.objects.all()
        for notify in notify_students:
            placements = PlacementSchedule.objects.filter(notify_id=notify.id)
            placement_serializer = PlacementScheduleSerializer(placements, many=True)
            notify_data = NotifyStudentSerializer(notify).data

            for placement in placement_serializer.data:
                combined_entry = {**notify_data, **placement}
                combined_data.append(combined_entry)

        return Response(combined_data)

    def post(self, request):
        placement_type = request.data.get("placement_type")
        company_name = request.data.get("company_name")
        ctc = request.data.get("ctc")
        description = request.data.get("description")
        schedule_at = request.data.get("schedule_at")
        date = request.data.get("placement_date")
        location = request.data.get("location")
        role = request.data.get("role")
        resume = request.FILES.get("resume")

        try:
            role_create, _ = Role.objects.get_or_create(role=role)
            notify = NotifyStudent.objects.create(
                placement_type=placement_type,
                company_name=company_name,
                description=description,
                ctc=ctc,
                timestamp=schedule_at,
            )

            schedule = PlacementSchedule.objects.create(
                notify_id=notify,
                title=company_name,
                description=description,
                placement_date=date,
                attached_file=resume,
                role=role_create,
                location=location,
                time=schedule_at,
            )

            return JsonResponse({"message": "Successfully Added Schedule"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)




@csrf_exempt
def placement_schedule_save(request):
    permission_classes = [permissions.AllowAny]
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    placement_type = request.POST.get("placement_type")
    company_name = request.POST.get("company_name")
    ctc = request.POST.get("ctc")
    description = request.POST.get("description")
    timestamp = request.POST.get("time_stamp")
    title = request.POST.get("title")
    location = request.POST.get("location")
    role = request.POST.get("role")
    
    resume = request.FILES.get("resume")
    schedule_at = request.POST.get("schedule_at")
    date = request.POST.get("placement_date")

    try:
        role_create, _ = Role.objects.get_or_create(role=role)
        
        notify = NotifyStudent.objects.create(
            placement_type=placement_type,
            company_name=company_name,
            description=description,
            ctc=ctc,
            timestamp=timestamp
        )

        schedule = PlacementSchedule.objects.create(
            notify_id=notify,
            title=company_name,
            description=description,
            placement_date=date,
            attached_file=resume,
            role=role_create,
            location=location,
            time=schedule_at
        )

        return JsonResponse({"message": "Successfully Added Schedule"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



class BatchStatisticsView(APIView):
    def get(self, request):
        combined_data = []
        student_records = StudentRecord.objects.all()

        if not student_records.exists():
            return Response({"error": "No student records found"}, status=status.HTTP_404_NOT_FOUND)

        for student in student_records:
            try:
                cur_student = Student.objects.get(id=student.unique_id)
                cur_placement = PlacementRecord.objects.get(id=student.record_id)
                user = User.objects.get(id=student.unique_id)

                combined_entry = {
                    "branch": cur_student.branch,  
                    "placement_name": cur_placement.name,  
                    "ctc": cur_placement.ctc, 
                    "year": cur_placement.year, 
                    "first_name": user.first_name 
                }

                combined_data.append(combined_entry)

            except Student.DoesNotExist:
                return Response({"error": f"Student with id {student.unique_id} not found"}, status=status.HTTP_404_NOT_FOUND)
            except PlacementRecord.DoesNotExist:
                return Response({"error": f"Placement record with id {student.record_id} not found"}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({"error": f"User with id {student.unique_id} not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not combined_data:
            return Response({"message": "No combined data found"}, status=status.HTTP_204_NO_CONTENT)

        return Response(combined_data, status=status.HTTP_200_OK)

    # def get(self, request):
    #     combined_data = []

    #     # Get all student records
    #     student_records = StudentRecord.objects.all()

    #     for student in student_records:
    #         # Get the current student, placement record, and user
    #         cur_student = Student.objects.get(id=student.unique_id)
    #         cur_placement = PlacementRecord.objects.get(id=student.record_id)
    #         user = User.objects.get(username=student.unique_id)

    #         # Combine the required fields into a dictionary
    #         combined_entry = {
    #             "branch": cur_student.branch,  # Assuming branch is a field in the Student model
    #             "placement_name": cur_placement.name,  # Name field from PlacementRecord
    #             "ctc": cur_placement.ctc,  # CTC field from PlacementRecord
    #             "year": cur_placement.year,  # Year field from PlacementRecord
    #             "first_name": user.first_name  # First name field from User
    #         }
            
    #         # Append the combined data to the list
    #         combined_data.append(combined_entry)

    #     return Response(combined_data, status=status.HTTP_200_OK)









