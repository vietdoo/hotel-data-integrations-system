from typing import TypeVar, List, Any
from abc import ABC, abstractmethod
from models.hotel import Hotel
from models.hotel import Location, Amenities, HotelImages
from utils.bias import Bias
from utils.logger import logger
from utils.exceptions import MergerException

T = TypeVar('T')


class AttributeMerger(ABC):
    def __init__(self, bias: Bias):
        self.bias = bias

    @abstractmethod
    def merge(self, data: List[T]) -> T:
        """Merge hotel data"""
        pass

    @staticmethod
    def encode_merge_data(data: T, src: str) -> dict[str, Any]:
        return {
            'data': data,
            'src': src
        }

    @staticmethod
    def decode_merge_data(merge_data: dict[str, Any]) -> T:
        try:
            return merge_data['data']
        except Exception as e:
            logger.log(f'Error when decoding merge data: {e}', 'error')
            raise MergerException(f'Error when decoding merge data: {e}')


class BaseDataMerger(ABC):
    def __init__(self, mergers: dict[str, AttributeMerger],
                 source_variable_name: str,
                 unmerged_variables: list[str] = []):

        self._mergers = mergers
        self._source_variable_name = source_variable_name
        self._unmerged_variables = unmerged_variables

    @abstractmethod
    def merge(self, data: List[T]) -> T:
        pass

    @staticmethod
    def encode_merge_data(data: T, src: str) -> dict[str, T]:
        return {
            'data': data,
            'src': src
        }

    @staticmethod
    def decode_merge_data(merge_data: dict[str, T]) -> T:
        try:
            return merge_data['data']
        except Exception as e:
            logger.log(f'Error when decoding merge data: {e}', 'error')
            raise MergerException(f'Error when decoding merge data: {e}')


class DataMerger(BaseDataMerger):
    def merge(self, data: List[Hotel]) -> Hotel:
        """Merge hotels with the same id to a single hotel"""
        if len(data) == 0:
            return None
        try:
            merged_hotel = data[-1].model_copy(update=data[-1].model_dump())
            logger.log(
                f'Merging {len(data)} hotels with id {merged_hotel.hotel_id}', 'info')
            for field, attribute_merger in self.get_all_mergers():
                merge_batch = []
                for hotel in data:
                    merge_batch.append(self.encode_merge_data(
                        getattr(hotel, field), getattr(hotel, self._source_variable_name)))

                try:
                    merged_data = attribute_merger.merge(merge_batch)
                    setattr(merged_hotel, field, merged_data)
                except Exception as e:
                    logger.log(
                        f'Error when merging field {field}: {e}', 'error')
                    raise MergerException(
                        f'Error when merging field {field}: {e}')

            try:
                setattr(merged_hotel, 'source', 'merged')
                return Hotel(**merged_hotel.model_dump())
            except Exception as e:
                logger.log(f'Error when creating merged hotel: {e}', 'error')
                raise MergerException(f'Error when creating merged hotel: {e}')
        except Exception as e:
            logger.log(f'Error when merging hotels: {e}', 'error')
            raise MergerException(f'Error when merging hotels: {e}')

    def get_all_mergers(self):
        return self._mergers.items()


class NameMerger(AttributeMerger):
    def merge(self, data: List[dict[str, Any]] = []) -> str:
        """Merge the name field"""
        if len(data) == 0 or data is None:
            return None

        try:
            merged_name = self.encode_merge_data(None, None)

            for name in filter(None, data):
                compare_bias = self.bias.compare_bias(
                    merged_name['src'], name['src'])
                if compare_bias < 0 or not merged_name['data']:
                    merged_name = name
                    continue

                if compare_bias == 0:
                    if len(merged_name['data']) < len(name['data']):
                        merged_name = name
                    continue

            return self.decode_merge_data(merged_name)
        except Exception as e:
            logger.log(f'Error when merging name field: {e}', 'error')
            raise MergerException(f'Error when merging name field: {e}')


class DescriptionMerger(AttributeMerger):
    def merge(self, data: List[dict[str, Any]] = []) -> str:
        """Merge the description field"""
        if len(data) == 0 or data is None:
            return None

        try:
            merged_des = self.encode_merge_data(None, None)

            for des in filter(None, data):
                compare_bias = self.bias.compare_bias(
                    merged_des['src'], des['src'])
                if compare_bias < 0 or not merged_des['data']:
                    merged_des = des
                    continue

                if compare_bias == 0:
                    if len(merged_des['data']) < len(des['data']):
                        merged_des = des
                    continue

            return self.decode_merge_data(merged_des)
        except Exception as e:
            logger.log(f'Error when merging description field: {e}', 'error')
            raise MergerException(f'Error when merging description field: {e}')


class LocationMerger(AttributeMerger):
    def merge(self, data: List[dict[str, Any]] = []) -> Location:
        """Merge the location field"""
        if len(data) == 0 or data is None:
            return None

        try:
            merged_location = {}
            for field_name in Location.model_fields.keys():
                merged_location[field_name] = None

            for location in data:
                location_data: Location = self.decode_merge_data(location)

                if not location_data:
                    continue

                for field, value in location_data.model_dump().items():
                    if merged_location[field] is None:
                        merged_location[field] = value
                        continue
                    if isinstance(value, str):
                        merged_location[field] = max(
                            merged_location[field], value, key=len)

            return Location(**merged_location)
        except Exception as e:
            logger.log(f'Error when merging location field: {e}', 'error')
            raise MergerException(f'Error when merging location field: {e}')


class AmenitiesMerger(AttributeMerger):
    def merge(self, data: List[dict[str, Any]] = []) -> Amenities:
        if len(data) == 0 or data is None:
            return None

        try:
            merged_amenities = {}
            for field_name in Amenities.model_fields.keys():
                merged_amenities[field_name] = []

            for amenities in filter(None, data):
                amenities_data: Amenities = self.decode_merge_data(amenities)
                if not amenities_data:
                    continue
                for field, amenities_list in amenities_data.model_dump().items():
                    if not amenities_list:
                        continue
                    for amenity in amenities_list:
                        if amenity not in merged_amenities[field]:
                            merged_amenities[field].append(amenity)

            return Amenities(**merged_amenities)
        except Exception as e:
            logger.log(f'Error when merging amenities field: {e}', 'error')
            raise MergerException(f'Error when merging amenities field: {e}')


class ImagesMerger(AttributeMerger):
    def merge(self, data: List[dict[str, Any]] = []) -> HotelImages:
        if len(data) == 0 or data is None:
            return None

        try:
            merged_images = {}
            for field_name in HotelImages.model_fields.keys():
                merged_images[field_name] = {}

            for images in filter(None, data):
                images_data: HotelImages = self.decode_merge_data(images)

                if not images_data:
                    continue

                for field, images_list in images_data.model_dump().items():
                    if not images_list:
                        continue

                    for image in images_list:
                        if image['link'] not in merged_images[field]:
                            merged_images[field][image['link']] = image
                            continue

                        if not image['description']:
                            continue

                        new_description = max(
                            merged_images[field][image['link']]['description'], image['description'], key=len)
                        merged_images[field][image['link']
                                             ]['description'] = new_description

            merged_images = {field: list(images.values())
                             for field, images in merged_images.items()}

            return HotelImages(**merged_images)
        except Exception as e:
            logger.log(f'Error when merging images field: {e}', 'error')
            raise MergerException(f'Error when merging images field: {e}')


class BookingConditionsMerger(AttributeMerger):
    def merge(self, data: List[dict[str, Any]] = []) -> List[str]:
        """Merge the booking_conditions field"""
        if len(data) == 0 or data is None:
            return None

        try:
            merged_conditions = []
            for booking_conditions in filter(None, data):
                booking_conditions_data = self.decode_merge_data(booking_conditions)
                
                if not booking_conditions_data:
                    continue
                
                for condition in filter(None, booking_conditions_data):
                    if condition not in merged_conditions:
                        merged_conditions.append(condition)

            return merged_conditions
        except Exception as e:
            logger.log(
                f'Error when merging booking conditions field: {e}', 'error')
            raise MergerException(f'Error when merging booking conditions field: {e}')
        
        
