from suppliers import SupplierManager
from services import HotelService
from database import HotelDB
from models.hotel import Hotel
from api import hotel_api

from suppliers.modules.acme import AcmeSupplier
from suppliers.modules.patagonia import PatagoniaSupplier
from suppliers.modules.paperflies import PaperfliesSupplier
from services.normalizer import DataNormalizer
from services.merger import DataMerger

from services.normalizer import DescriptionNormalizer
from services.normalizer import LocationNormalizer
from services.normalizer import AmenitiesNormalizer
from services.normalizer import ImagesNormalizer
from services.normalizer import NameNormalizer
from services.normalizer import BookingConditionsNormalizer

from services.merger import DescriptionMerger
from services.merger import LocationMerger
from services.merger import AmenitiesMerger
from services.merger import ImagesMerger
from services.merger import NameMerger
from services.merger import BookingConditionsMerger

from utils.cleaner import HotelCleaner
from utils.bias import HotelBias
from utils.logger import logger
from utils.output import pretty_hotel_output
from utils.output import pretty_hotels_output

from database.hotel import raw_hotel_db, hotel_db

from configs.config import supplier_config, merger_config

def update_suppliers_data():
    suppliers = {
        "acme": AcmeSupplier(supplier_config['endpoint']['acme']),
        "patagonia": PatagoniaSupplier(supplier_config['endpoint']['patagonia']),
        "paperflies": PaperfliesSupplier(supplier_config['endpoint']['paperflies'])
    }

    supplier_manager = SupplierManager(suppliers)
    suppliers_data = supplier_manager.get_all_suppliers_data()

    cleaner = HotelCleaner()
    normalizers = {
        "description": DescriptionNormalizer(cleaner),
        "location": LocationNormalizer(cleaner),
        "amenities": AmenitiesNormalizer(cleaner),
        "images": ImagesNormalizer(cleaner),
        "name": NameNormalizer(cleaner),
        "booking_conditions": BookingConditionsNormalizer(cleaner)
    }

    bias = HotelBias(merger_config['bias_factors'])
    mergers = {
        "name": NameMerger(bias),
        "description": DescriptionMerger(bias),
        "location": LocationMerger(bias),
        "amenities": AmenitiesMerger(bias),
        "images": ImagesMerger(bias),
        "booking_conditions": BookingConditionsMerger(bias)
    }
    
    svc = HotelService(suppliers_data,
                       DataNormalizer(normalizers),
                       DataMerger(mergers, 
                                  merger_config['source_attr_name'],
                                  merger_config['unmerged_attrs']),
                       raw_hotel_db)

    svc.normalize_hotels()
    svc.merge_hotels()
    
    hotel_db.update_many(svc.get)
    
    logger.log(f'Updated {hotel_db.length()} hotels in the database', 'info')
    logger.log(f'Updated {raw_hotel_db.length()} raw hotels in the database', 'info')


def parse_arguments():
    """
    Parse command-line arguments for hotel_ids and destination_ids.
    Returns:
        hotel_ids (list or None): A list of hotel IDs, or None if 'none' is passed.
        destination_ids (list or None): A list of destination IDs, or None if 'none' is passed.
    """
    import argparse  # Import argparse here to keep the function self-contained

    parser = argparse.ArgumentParser(
        description="Filter hotels by hotel_ids and destination_ids."
    )
    parser.add_argument(
        "hotel_ids",
        type=str,
        help="Comma-separated list of hotel IDs, or 'none' if no filtering by hotel ID is required.",
    )
    parser.add_argument(
        "destination_ids",
        type=str,
        help="Comma-separated list of destination IDs, or 'none' if no filtering by destination ID is required.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Process hotel_ids and destination_ids
    hotel_ids = args.hotel_ids.split(
        ",") if args.hotel_ids.lower() != "none" else None
    destination_ids = args.destination_ids.split(
        ",") if args.destination_ids.lower() != "none" else None

    return hotel_ids, destination_ids

def main():
    
    update_suppliers_data()
    
    hotel_ids, destination_ids = parse_arguments()
    logger.log(f"Filtering hotels by hotel_ids: {hotel_ids}, destination_ids: {destination_ids}", "info")

    
    params = {
        "hotel_ids": hotel_ids,
        "destination_ids": destination_ids
    }
    
    hotels = hotel_api.get_hotels(hotel_db, params)
    print(hotels)
    

if __name__ == "__main__":
    main()
    logger.close()

