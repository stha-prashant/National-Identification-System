from address.models import *
from documents.models import DrivingLicenseIssueCentre
def run():
	DrivingLicenseIssueCentre(centre_id=1, province=Region.objects.get(pk=1001), district=District.objects.get(pk=100103), local=LocalBody.objects.get(pk=1101032004), name='Department of Transport Managemnt (Chabahil)').save()
	DrivingLicenseIssueCentre(centre_id=2, province=Region.objects.get(pk=1013), district=District.objects.get(pk=101302), local=LocalBody.objects.get(pk=1113022006), name='Department of Transport Managemnt (Pokhara)').save()
	DrivingLicenseIssueCentre(centre_id=3, province=Region.objects.get(pk=1001), district=District.objects.get(pk=100101), local=LocalBody.objects.get(pk=1101015139), name='Department of Transport Management (Jagati)').save()
	DrivingLicenseIssueCentre(centre_id=4, province=Region.objects.get(pk=1004), district=District.objects.get(pk=100405), local=LocalBody.objects.get(pk=1104053007), name='Department of Transport Management(Koshi)').save()
	DrivingLicenseIssueCentre(centre_id=5, province=Region.objects.get(pk=1014), district=District.objects.get(pk=101406), local=LocalBody.objects.get(pk=1114063013), name='Department of Transport Management (Lumbini Butwal)').save()
	DrivingLicenseIssueCentre(centre_id=6, province=Region.objects.get(pk=1003), district=District.objects.get(pk=100304), local=LocalBody.objects.get(pk=1103042002), name='Department of Transport Management (Narayani, Birgunj)').save()
	DrivingLicenseIssueCentre(centre_id=7, province=Region.objects.get(pk=1001), district=District.objects.get(pk=100103), local=LocalBody.objects.get(pk=1101035153), name='Department of Transport Management  (Thulo Bharyang) ').save()
	DrivingLicenseIssueCentre(centre_id=8, province=Region.objects.get(pk=1001), district=District.objects.get(pk=100105), local=LocalBody.objects.get(pk=1101052005), name='Department of Transport Managment (Ekantakuna, Lalitpur)').save()
