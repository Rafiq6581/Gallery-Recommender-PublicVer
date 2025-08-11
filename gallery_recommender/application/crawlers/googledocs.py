from loguru import logger
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, time
import pandas as pd

from gallery_recommender.domain.data import GalleryData, ExhibitionData
from .base import BaseCrawler
from gallery_recommender.settings import settings
from gallery_recommender.domain.exceptions import ImproperlyConfigured
from gallery_recommender.application.preprocessing.operations.clean_data import clean_sheets_data  # Import the cleaning function

class GoogleDocsCrawler(BaseCrawler):

    GalleryModel = GalleryData
    ExhibitionModel = ExhibitionData

    def extract(self, link: str, **kwargs) -> tuple[int, int]:
        
        logger.info(f"Extracting Google Sheets document from: {link}...")

        # Check if there is a service account file and scopes to authorize the connection to Google Sheets
        if not settings.SERVICE_ACCOUNT_FILE or not settings.SCOPES:
            raise ImproperlyConfigured("SERVICE_ACCOUNT_FILE or SCOPES is not set")
        creds = Credentials.from_service_account_file(
            settings.SERVICE_ACCOUNT_FILE, 
            scopes=settings.SCOPES
        )
        logger.info(f"Service Account File: {settings.SERVICE_ACCOUNT_FILE}")
        logger.info(f"Scopes: {settings.SCOPES}")
        # Connect to Google Sheets
        client = gspread.authorize(creds)
        print(link)
        # sheet_name = "Demo Art Gallery Data"
        sheet = client.open_by_url(link)
        sheet = sheet.get_worksheet(0)
        # sheet = client.open_by_url(link).worksheet(sheet_name)

        # Read all data from the sheet
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        logger.info(f"DataFrame after extraction: {df.head()}")

        # Clean the data using the new function
        df = clean_sheets_data(df)

        logger.info(f"Type of 'Exhibition Start Date': {type(df['Exhibition Start Date'].iloc[0])}")
        added_galleries = 0
        added_exhibitions = 0

        for _, row in df.iterrows():
            start_dt = datetime.combine(row["Exhibition Start Date"], time.min)
            end_dt = datetime.combine(row["Exhibition End Date"], time.min)

            logger.info(f"Checking if gallery already exists in the database: {row['Gallery Name English']}")
            gallery_name = row["Gallery Name English"]
            exhibition_name = row["Exhibition Name"]
            try:
                old_gallery_model = self.GalleryModel.find(name=gallery_name)
            except Exception as e:
                logger.info(f"Error finding gallery: {e}")
                old_gallery_model = None
            if old_gallery_model is not None:
                logger.info(f"Gallery already exists in the database: {gallery_name}")
                gallery_id = str(old_gallery_model.id)
                logger.info(f"Retrieved Gallery ID: {gallery_id}")

                try:
                    old_exhibition_model = self.ExhibitionModel.find(
                        name=exhibition_name,
                        gallery_id=gallery_id
                    )

                except Exception as e:
                    logger.info(f"Error finding exhibition: {e}")
                    old_exhibition_model = None

                if old_exhibition_model is not None:
                    logger.info(f"Exhibition already exists in the database: {exhibition_name}")
                    continue

                else:
                    logger.info(f"Exhibition does not exist in the database: {exhibition_name}, adding to the database")
                    exhibition = self.ExhibitionModel(
                        area=row["Area"],
                        name=row["Exhibition Name"],
                        name_japanese=row["Exhibition Name Japanese"],
                        name_english=row["Exhibition Name English"],
                        description=row["Exhibition Description From Website"],
                        description_japanese=row["Exhibition Description From Website (Japanese)"],
                        description_english=row["Exhibition Description From Website (English)"],
                        artist=row["Artist"],
                        exhibition_image_url=row["Exhibition Image URL"],
                        exhibition_start_date=start_dt,
                        exhibition_end_date=end_dt,
                        exhibition_start_date_ts=round(start_dt.timestamp(), 3),
                        exhibition_end_date_ts=round(end_dt.timestamp(), 3),
                        gallery_id=gallery_id,  # Link the exhibition to the new gallery
                        latitude=row["Latitude"],
                        longitude=row["Longitude"],
                    )
                    exhibition.save()
                    added_exhibitions += 1
                    logger.info(f"Exhibition created in the database: {row['Exhibition Name']} with id: {exhibition.id}")
            
            # if gallery does not exist, create a new gallery
            else:
                logger.info(f"Gallery does not exist in the database: {gallery_name}, creating a new gallery")
                gallery = self.GalleryModel(
                    name=gallery_name,
                    name_japanese=row["Gallery Name Japanese"],
                    name_english=row["Gallery Name English"],
                    description=row["Gallery Description From Website"],
                    area=row["Area"],
                    gallery_image_url=row["Gallery Image URL"],
                    website=row["Website"],
                    hours=row["Hours"],
                    latitude=row["Latitude"],
                    longitude=row["Longitude"],
                    phone_number=row["Phone Number"],
                    address_japanese=row["Address Japanese"],
                    address_english=row["Address English"],
                )
                
                gallery.save()
                logger.info(f"Gallery created in the database: {gallery_name} with id: {gallery.id}")
                added_galleries += 1

                # Within the new gallery, also create the exhibition for it
                exhibition = self.ExhibitionModel(
                    area=row["Area"],
                    name=row["Exhibition Name"],
                    name_japanese=row["Exhibition Name Japanese"],
                    name_english=row["Exhibition Name English"],
                    description=row["Exhibition Description From Website"],
                    description_japanese=row["Exhibition Description From Website (Japanese)"],
                    description_english=row["Exhibition Description From Website (English)"],
                    artist=row["Artist"],
                    exhibition_image_url=row["Exhibition Image URL"],
                    exhibition_start_date=start_dt,
                    exhibition_end_date=end_dt,
                    exhibition_start_date_ts=start_dt.timestamp(),
                    exhibition_end_date_ts=end_dt.timestamp(),
                    gallery_id=gallery.id,  # Link the exhibition to the new gallery
                    latitude=row["Latitude"],
                    longitude=row["Longitude"]
                )
                exhibition.save()
                logger.info(f"Exhibition created in the database: {row['Exhibition Name']} for gallery: {gallery_name}")
                added_exhibitions += 1

        return added_galleries, added_exhibitions