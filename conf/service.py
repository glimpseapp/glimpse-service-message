import os

GLIMPSE_SERVICE_ASSET = os.getenv("GLIMPSE_SERVICE_ASSET", "http://glimpse-service-asset.endpoints.glimpse-123456.cloud.goog")

IMAGES_URL_BULK_URL = GLIMPSE_SERVICE_ASSET + "/images-url-bulk"