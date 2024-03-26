from typing import List, Optional

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from repository.region_repository import RegionRepository
from schemas.region_schema import RegionInput, RegionOutput


class RegionService:
    """
    Service class for handling regions.
    """

    def __init__(self, session: Session):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = RegionRepository(session)

    def create(self, data: RegionInput) -> RegionOutput:
        """
        Create a new region.

        Args:
            data (RegionInput): Details of the region to be created.

        Returns:
            RegionOutput: Details of the created region.
        """
        if self.repository.region_exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="Region already exists")
        return self.repository.create(data)

    def get_all(self) -> List[Optional[RegionOutput]]:
        """
        Retrieve all regions.

        Returns:
            List[Optional[RegionOutput]]: List of regions.
        """
        return self.repository.get_all()

    def delete(self, _id: UUID4) -> bool:
        """
        Delete a region.

        Args:
            _id (UUID4): ID of the region to be deleted.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        if not self.repository.region_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Region not found")

        region = self.repository.get_by_id(_id)
        self.repository.delete(region)
        return True

    def update(self, _id: UUID4, data: RegionInput) -> RegionInput:
        """
        Update a region.

        Args:
            _id (UUID4): ID of the region to be updated.
            data (RegionInput): Updated details of the region.

        Returns:
            RegionInput: Updated details of the region.
        """
        if not self.repository.region_exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Region not found")

        region = self.repository.get_by_id(_id)
        return self.repository.update(region, data)