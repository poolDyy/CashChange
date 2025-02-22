from functools import cached_property

from rest_framework import status
from rest_framework.test import APIClient

__all__ = ['ApiTestClient']


class ApiTestClient(APIClient):
    @cached_property
    def api_client(self) -> APIClient:
        return APIClient()

    def get(
        self,
        *args,
        expected_status: int = status.HTTP_200_OK,
        **kwargs,
    ):
        response = self.api_client.get(*args, **kwargs)
        assert response.status_code == expected_status
        return response.json()

    def post(
        self,
        *args,
        expected_status: int = status.HTTP_201_CREATED,
        **kwargs,
    ):
        response = self.api_client.post(*args, **kwargs)
        assert response.status_code == expected_status
        return response.json()

    def put(
        self,
        *args,
        expected_status: int = status.HTTP_200_OK,
        **kwargs,
    ):
        response = self.api_client.put(*args, **kwargs)
        assert response.status_code == expected_status
        return response.json()

    def patch(
        self,
        *args,
        expected_status: int = status.HTTP_200_OK,
        **kwargs,
    ):
        response = self.api_client.patch(*args, **kwargs)
        assert response.status_code == expected_status
        return response.json()

    def delete(
        self,
        *args,
        expected_status: int = status.HTTP_204_NO_CONTENT,
        **kwargs,
    ):
        response = self.api_client.delete(*args, **kwargs)
        assert response.status_code == expected_status
        return response
