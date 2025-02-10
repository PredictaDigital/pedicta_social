


from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
import logging
from .utils import *
from .config import * 



# Logger setup
logger = logging.getLogger(__name__)

def test_api(request):
    data = {"Message": f"{__name__}"}
    return JsonResponse(data)

class GSCDataAPIView(APIView):
    def get(self, request):

        logging.info("Starting Data extraction process...")

        # OAuth 2.0 authentication
        service, creds = get_credentials()
        try:        
            # Extract GSC data for littlecheeks.com
            data_gsc_webpage = extract_GSC_webpage_data(service, SITE_URL)

            # Save to Predicta Database
            insert_data_to_db(data_gsc_webpage,'WebPage') if not data_gsc_webpage.empty else logging.warning("No GSC Web-Page-data fetched from GA4.")

            # Save to Excel file
            # data_gsc_webpage.to_excel('GSC_Test_WebPage.xlsx',index=False)

            # Refresh token if necessary
            check_and_refresh_token(creds)

            return JsonResponse({"message": "Data successfully collected and saved."}, status=status.HTTP_200_OK)


        except Exception as e:
            logging.error(f"Error fetching GA4 data: {str(e)}")
            return JsonResponse({"message": f"{str(e)}"}, status=status.HTTP_200_OK)





