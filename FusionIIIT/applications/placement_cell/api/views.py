from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import status,permissions
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..models import *
from applications.academic_information.models import Student
from .serializers import PlacementScheduleSerializer, NotifyStudentSerializer
import json

@method_decorator(csrf_exempt, name='dispatch')
class PlacementScheduleView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None): 
        if id:
            try:
                notify_schedule = NotifyStudent.objects.get(id=id)
                placement_schedule = PlacementSchedule.objects.get(notify_id=notify_schedule)
                combined_entry = {**NotifyStudentSerializer(notify_schedule).data, **PlacementScheduleSerializer(placement_schedule).data}
                return Response(combined_entry, status=status.HTTP_200_OK)
            except NotifyStudent.DoesNotExist:
                return Response({"error": "NotifyStudent not found"}, status=status.HTTP_404_NOT_FOUND)
            except PlacementSchedule.DoesNotExist:
                return Response({"error": "PlacementSchedule not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            combined_data = []
            notify_students = NotifyStudent.objects.all()
            for notify in notify_students:
                placements = PlacementSchedule.objects.filter(notify_id=notify.id)
                placement_serializer = PlacementScheduleSerializer(placements, many=True)
                notify_data = NotifyStudentSerializer(notify).data

                for placement in placement_serializer.data:
                    combined_entry = {**notify_data, **placement}
                    combined_data.append(combined_entry)

            return Response(combined_data, status=status.HTTP_200_OK)
        
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



            return redirect('placement')

            return JsonResponse({"message": "Successfully Added Schedule"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    def delete(self, request, id):
        try:
            notify_schedule = NotifyStudent.objects.get(id=id)
            placement_schedule = PlacementSchedule.objects.get(notify_id=notify_schedule)
            notify_schedule.delete()
            placement_schedule.delete()

            return JsonResponse({"message": "Successfully Deleted"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    def put(self, request, id):
        try:
            notify_schedule = NotifyStudent.objects.get(id=id)
            placement_schedule = PlacementSchedule.objects.get(notify_id=notify_schedule)

            placement_type = request.data.get("placement_type", notify_schedule.placement_type)
            company_name = request.data.get("company_name", notify_schedule.company_name)
            ctc = request.data.get("ctc", notify_schedule.ctc)
            description = request.data.get("description", notify_schedule.description)
            schedule_at = request.data.get("schedule_at", notify_schedule.timestamp)
            date = request.data.get("placement_date", placement_schedule.placement_date)
            location = request.data.get("location", placement_schedule.location)
            role = request.data.get("role", placement_schedule.role)
            resume = request.FILES.get("resume", placement_schedule.attached_file)

            notify_schedule.placement_type = placement_type
            notify_schedule.company_name = company_name
            notify_schedule.ctc = ctc
            notify_schedule.description = description
            notify_schedule.timestamp = schedule_at
            notify_schedule.save()

            placement_schedule.title = company_name
            placement_schedule.description = description
            placement_schedule.placement_date = date
            placement_schedule.location = location
            placement_schedule.attached_file = resume
            placement_schedule.time = schedule_at
            placement_schedule.role = Role.objects.get(role=role) if role else placement_schedule.role
            placement_schedule.save()

            return JsonResponse({"message": "Successfully Updated"}, status=200)
        
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

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        combined_data = []
        student_records = StudentRecord.objects.all()

        if not student_records.exists():
            return Response({"error": "No student records found"}, status=status.HTTP_404_NOT_FOUND)

        for student in student_records:
            try:

                cur_student = Student.objects.get(id_id=student.unique_id_id)
                cur_placement = PlacementRecord.objects.get(id=student.record_id_id)
                user = User.objects.get(username=student.unique_id_id)

                combined_entry = {
                    "branch": cur_student.specialization, 
                    "batch" : cur_placement.year, 

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



    def post(self,request):
        placement_type=request.POST.get("placement_type")
        company_name=request.POST.get("company_name")
        roll_no = request.POST.get("roll_no")
        ctc=request.POST.get("ctc")
        year=request.POST.get("year")
        test_type=request.POST.get("test_type")
        test_score=request.POST.get("test_score")

        try:
            p2 = PlacementRecord.objects.create(
                placement_type = placement_type,
                name = company_name,
                ctc = ctc,
                year = year,
                test_score = test_score,
                test_type = test_type,
            )
            p1 = StudentRecord.objects.create(
                record_id = p2,
                unique_id_id = roll_no,
            )
            return JsonResponse({"message": "Successfully Added"}, status=201)
    
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    def put(self, request, record_id):
        try:
            placement_record = PlacementRecord.objects.get(id=record_id)
            placement_record.placement_type = request.data.get("placement_type", placement_record.placement_type)
            placement_record.name = request.data.get("company_name", placement_record.name)
            placement_record.ctc = request.data.get("ctc", placement_record.ctc)
            placement_record.year = request.data.get("year", placement_record.year)
            placement_record.test_score = request.data.get("test_score", placement_record.test_score)
            placement_record.test_type = request.data.get("test_type", placement_record.test_type)
            placement_record.save()

            return JsonResponse({"message": "Successfully Updated"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    

    def delete(self, request, record_id):
        try:
            placement_record = PlacementRecord.objects.get(id=record_id)
            student_record = StudentRecord.objects.get(record_id=placement_record)
            student_record.delete()
            placement_record.delete()

            return JsonResponse({"message": "Successfully Deleted"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    



