from utils.logger import logger
from utils.exceptions import BiasException

from abc import ABC, abstractmethod


class Bias(ABC):
    def __init__(self, bias_factors: dict[str, dict[str, float]]):
        """
        Initialize the bias factors.

        :param bias_factors: A dictionary containing bias factors for different fields and ids.
        Example structure:
        {
            'bias_factors': {
                'confidence_level': {
                    'supplier1': 0.9,
                    'supplier2': 0.6,
                    'supplier3': 0.8
                }
            }
        }
        """
        self._bias_factors = bias_factors

    @abstractmethod
    def get_bias_score(self, id: str) -> float:
        """
        Get the bias score for a specific id.

        :param id: The id for which to fetch the bias score.
        :return: A floating-point value representing the bias score.
        """
        pass

    @abstractmethod
    def compare_bias(self, id1: str, id2: str) -> float:
        """
        Compare the bias score between two ids.

        :param id1: The first id to compare.
        :param id2: The second id to compare.
        :return: A floating-point value representing the difference in bias scores.
        """
        pass

    def get_factor_names(self) -> list[str]:
        """
        Get the names of the bias factors.

        :return: A list of bias factor names (keys in the bias factors dictionary).
        """
        return list(self._bias_factors.keys())


class HotelBias(Bias):
    def get_bias_score(self, id: str, field: str = None) -> float:
        """
        Get the bias score for a hotel by id and optionally by field.

        If no field is provided, it aggregates all bias scores for the id across all factors.

        :param id: The id of the hotel or supplier.
        :param field: (Optional) A specific field to retrieve the bias score for.
        :return: A floating-point value representing the bias score, or None if the score could not be determined.
        """
        
        # Ensure the id exists in the bias factors
       
        if field is not None:
            # If field is provided, return bias score for the specified field
            if field not in self._bias_factors:
                logger.log(f"Error: {field} not found in bias factors.", "error")
                return None
            return self._bias_factors[field][id]
        
        # If no field is provided, aggregate all the bias scores for the id
        scores = [factor.get(id) for factor in self._bias_factors.values()]
        valid_scores = [score for score in scores if score is not None]

        if not valid_scores:
            logger.log(f"No bias scores found for {id}.", "info")
            return None
        
        logger.log(f"Aggregated bias scores for {id}: {valid_scores}", "info")

        return sum(valid_scores) / len(valid_scores)

    def compare_bias(self, id1: str, id2: str) -> float:
        """
        Compare the bias score between two ids.

        :param id1: The first id to compare.
        :param id2: The second id to compare.
        :return: A floating-point value representing the difference in bias scores.
        """
        bias1 = self.get_bias_score(id1)
        bias2 = self.get_bias_score(id2)

        if bias1 is None and bias2 is None:
            return 0

        if bias1 is None:
            return -1

        if bias2 is None:
            return 1

        return bias1 - bias2
