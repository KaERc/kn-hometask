from rest_framework import status
from rest_framework.test import APITestCase

from .models import Shipment

LIST_URL = "/api/shipments/"
VALID = {
    "reference": "KN-0001",
    "origin": "Tallinn",
    "destination": "Hamburg",
    "status": "booked",
    "eta": "2026-11-01",
}


def detail_url(shipment):
    return f"{LIST_URL}{shipment.pk}/"


class ShipmentApiTests(APITestCase):
    def make(self, **overrides):
        return Shipment.objects.create(**{**VALID, **overrides})

    # list

    def test_list_is_empty_when_there_are_no_shipments(self):
        response = self.client.get(LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_list_returns_the_newest_shipment_first(self):
        first = self.make(reference="KN-0001")
        second = self.make(reference="KN-0002")
        response = self.client.get(LIST_URL)
        self.assertEqual([s["id"] for s in response.json()], [second.pk, first.pk])

    # retrieve

    def test_retrieve_returns_the_shipment(self):
        shipment = self.make()
        response = self.client.get(detail_url(shipment))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"id": shipment.pk, **VALID})

    def test_retrieve_unknown_id_returns_404(self):
        response = self.client.get(f"{LIST_URL}999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # create

    def test_create_returns_201_and_stores_the_shipment(self):
        response = self.client.post(LIST_URL, VALID, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["reference"], "KN-0001")
        self.assertEqual(Shipment.objects.get().destination, "Hamburg")

    def test_create_defaults_status_to_booked_and_eta_is_optional(self):
        minimal = {"reference": "KN-0002", "origin": "Riga", "destination": "Oslo"}
        response = self.client.post(LIST_URL, minimal, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["status"], "booked")
        self.assertIsNone(response.json()["eta"])

    def test_create_rejects_a_duplicate_reference(self):
        self.make()
        response = self.client.post(LIST_URL, VALID, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reference", response.json())

    def test_create_rejects_an_unknown_status(self):
        data = {**VALID, "status": "lost"}
        response = self.client.post(LIST_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.json())

    def test_create_rejects_missing_required_fields(self):
        response = self.client.post(LIST_URL, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.json()), {"reference", "origin", "destination"})

    def test_create_rejects_same_origin_and_destination_ignoring_case(self):
        data = {**VALID, "origin": "Tallinn", "destination": "tallinn"}
        response = self.client.post(LIST_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("destination", response.json())
        self.assertEqual(Shipment.objects.count(), 0)

    # update

    def test_put_replaces_all_fields_and_keeps_its_own_reference(self):
        shipment = self.make()
        new = {
            "reference": "KN-0001",
            "origin": "Riga",
            "destination": "Oslo",
            "status": "in_transit",
            "eta": None,
        }
        response = self.client.put(detail_url(shipment), new, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shipment.refresh_from_db()
        self.assertEqual(
            (shipment.origin, shipment.destination, shipment.status, shipment.eta),
            ("Riga", "Oslo", "in_transit", None),
        )

    def test_put_unknown_id_returns_404(self):
        response = self.client.put(f"{LIST_URL}999/", VALID, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_changes_only_the_given_fields(self):
        shipment = self.make()
        response = self.client.patch(
            detail_url(shipment), {"status": "delivered"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shipment.refresh_from_db()
        self.assertEqual(shipment.status, "delivered")
        self.assertEqual(shipment.origin, "Tallinn")

    def test_patch_rejects_a_destination_equal_to_the_stored_origin(self):
        shipment = self.make(origin="Tallinn", destination="Hamburg")
        response = self.client.patch(
            detail_url(shipment), {"destination": "Tallinn"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        shipment.refresh_from_db()
        self.assertEqual(shipment.destination, "Hamburg")

    # delete

    def test_delete_returns_204_and_removes_the_shipment(self):
        shipment = self.make()
        response = self.client.delete(detail_url(shipment))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Shipment.objects.exists())

    def test_delete_unknown_id_returns_404(self):
        response = self.client.delete(f"{LIST_URL}999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # search

    def search(self, term):
        response = self.client.get(LIST_URL, {"search": term})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return [s["reference"] for s in response.json()]

    def test_search_matches_reference_origin_and_destination(self):
        self.make(reference="KN-0001", origin="Tallinn", destination="Hamburg")
        self.make(reference="KN-0002", origin="Riga", destination="Oslo")
        self.assertEqual(self.search("0002"), ["KN-0002"])
        self.assertEqual(self.search("Tallinn"), ["KN-0001"])
        self.assertEqual(self.search("Oslo"), ["KN-0002"])

    def test_search_is_partial_and_ignores_case(self):
        self.make(reference="KN-0001", destination="Hamburg")
        self.make(reference="KN-0002", destination="Oslo")
        self.assertEqual(self.search("hamb"), ["KN-0001"])

    def test_search_with_no_match_returns_an_empty_list(self):
        self.make()
        self.assertEqual(self.search("Rotterdam"), [])

    def test_search_without_a_term_returns_everything(self):
        self.make(reference="KN-0001")
        self.make(reference="KN-0002")
        self.assertEqual(self.search(""), ["KN-0002", "KN-0001"])

    def test_search_looks_only_at_reference_origin_and_destination(self):
        self.make(status="delivered", eta="2026-11-01")
        self.assertEqual(self.search("delivered"), [])
        self.assertEqual(self.search("2026"), [])

    # reference uniqueness

    def test_create_rejects_a_reference_that_differs_only_in_case(self):
        self.make(reference="KN-0001")
        data = {**VALID, "reference": "kn-0001"}
        response = self.client.post(LIST_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reference", response.json())

    def test_put_may_change_the_case_of_its_own_reference(self):
        shipment = self.make(reference="KN-0001")
        data = {**VALID, "reference": "kn-0001"}
        response = self.client.put(detail_url(shipment), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
