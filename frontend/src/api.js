const BASE = "/api/shipments/";

// ponytail: kept in step with Shipment.Status by hand; read the choices from
// OPTIONS /api/shipments/ if the statuses start to change.
export const STATUSES = [
  { value: "booked", label: "Booked" },
  { value: "in_transit", label: "In transit" },
  { value: "delivered", label: "Delivered" },
  { value: "cancelled", label: "Cancelled" },
];

export const STATUS_LABELS = Object.fromEntries(
  STATUSES.map(({ value, label }) => [value, label]),
);

// On 400 the body holds the field errors, e.g. { reference: ["..."] }.
export class ApiError extends Error {
  constructor(status, body) {
    super(`HTTP ${status}`);
    this.status = status;
    this.body = body;
  }
}

async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (response.status === 204) return null;
  const body = await response.json().catch(() => null);
  if (!response.ok) throw new ApiError(response.status, body);
  return body;
}

export const listShipments = (search) =>
  request(`${BASE}?search=${encodeURIComponent(search)}`);

export const deleteShipment = (id) => request(`${BASE}${id}/`, { method: "DELETE" });

// PUT when the shipment has an id, POST otherwise.
export const saveShipment = (shipment) =>
  shipment.id
    ? request(`${BASE}${shipment.id}/`, {
        method: "PUT",
        body: JSON.stringify(shipment),
      })
    : request(BASE, { method: "POST", body: JSON.stringify(shipment) });
