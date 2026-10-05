<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { deleteShipment, listShipments, STATUS_LABELS } from "./api.js";
import ShipmentForm from "./ShipmentForm.vue";

const shipments = ref([]);
const search = ref("");
const loading = ref(true);
const error = ref("");
// undefined: form closed, null: new shipment, object: editing that shipment.
const editing = ref(undefined);

// Only the newest request may update the page, so a slow early response
// cannot overwrite a later search.
let latest = 0;
async function load() {
  const mine = ++latest;
  try {
    const data = await listShipments(search.value);
    if (mine !== latest) return;
    shipments.value = data;
    error.value = "";
  } catch {
    if (mine !== latest) return;
    error.value = "Could not load shipments. Check that the API is running and try again.";
  } finally {
    if (mine === latest) loading.value = false;
  }
}

const emptyMessage = computed(() => {
  if (error.value) return "Nothing to show.";
  return search.value ? "No shipments match your search." : "No shipments yet.";
});

onMounted(load);
// ponytail: one request per keystroke; add a debounce if the list or latency grows.
watch(search, load);

async function remove(shipment) {
  if (!confirm(`Delete shipment ${shipment.reference}?`)) return;
  try {
    await deleteShipment(shipment.id);
    await load();
  } catch {
    error.value = "Could not delete the shipment. Try again.";
  }
}

function saved() {
  editing.value = undefined;
  load();
}
</script>

<template>
  <main class="page">
    <h1>Shipments</h1>

    <section class="panel toolbar">
      <input
        v-model="search"
        type="search"
        class="input"
        placeholder="Search by reference, origin or destination"
        aria-label="Search shipments"
      />
      <button class="btn btn-primary" @click="editing = null">New shipment</button>
    </section>

    <p v-if="error" class="alert" role="alert">{{ error }}</p>

    <section class="panel table-panel">
      <p v-if="loading" class="muted">Loading…</p>
      <p v-else-if="!shipments.length" class="muted">{{ emptyMessage }}</p>
      <table v-else>
        <thead>
          <tr>
            <th class="center">Reference</th>
            <th>Origin</th>
            <th>Destination</th>
            <th class="center">ETA</th>
            <th class="center">Status</th>
            <th><span class="sr-only">Actions</span></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in shipments" :key="s.id">
            <td class="center mono">{{ s.reference }}</td>
            <td>{{ s.origin }}</td>
            <td>{{ s.destination }}</td>
            <td class="center">{{ s.eta ?? "—" }}</td>
            <td class="center">
              <span class="badge" :class="`badge-${s.status}`">{{
                STATUS_LABELS[s.status]
              }}</span>
            </td>
            <td class="actions">
              <button class="btn btn-ghost" @click="editing = s">Edit</button>
              <button class="btn btn-destructive" @click="remove(s)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <ShipmentForm
      v-if="editing !== undefined"
      :shipment="editing"
      @saved="saved"
      @close="editing = undefined"
    />
  </main>
</template>
