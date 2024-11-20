from suppliers.base_supplier import BaseSupplier
from utils.logger import logger
from typing import Dict, List, Tuple, Optional


class SupplierManager:
    """
    Manages multiple suppliers and their data fetching operations.
    """

    def __init__(self, suppliers: Dict[str, BaseSupplier]):
        """
        Initialize SupplierManager with a dictionary of suppliers.

        :param suppliers: A dictionary where keys are supplier names, and values are supplier modules implementing BaseSupplier.
        """
        self.suppliers = suppliers

    def get_all_suppliers_data(self) -> List[dict]:
        """
        Fetch data from all suppliers.

        :return: A list of data collected from all suppliers.
        """
        data = []
        for supplier_name, supplier_module in self.get_all_suppliers():
            try:
                logger.log(
                    f"Fetching data from supplier '{supplier_name}'.", "info")
                fetched_data = supplier_module.fetch()
                if fetched_data:
                    data.extend(fetched_data)
                    logger.log(
                        f"Successfully fetched {len(fetched_data)} records from supplier '{supplier_name}'.", "info")
                else:
                    logger.log(
                        f"No data fetched from supplier '{supplier_name}'.", "warning")
            except Exception as e:
                logger.log(
                    f"Error fetching data from supplier '{supplier_name}': {e}", "error")
        return data

    def get_all_suppliers(self) -> List[Tuple[str, BaseSupplier]]:
        """
        Get all suppliers as a list of (name, module) pairs.

        :return: A list of tuples containing supplier names and their corresponding modules.
        """
        return list(self.suppliers.items())

    def get_supplier_names(self) -> List[str]:
        """
        Get the names of all suppliers.

        :return: A list of supplier names.
        """
        return list(self.suppliers.keys())

    def get_supplier(self, name: str) -> Optional[BaseSupplier]:
        """
        Get a specific supplier by name.

        :param name: The name of the supplier.
        :return: The supplier module if found, otherwise None.
        """
        supplier = self.suppliers.get(name)
        if supplier:
            logger.log(f"Supplier '{name}' found.", "info")
        else:
            logger.log(f"Supplier '{name}' not found.", "warning")
        return supplier
