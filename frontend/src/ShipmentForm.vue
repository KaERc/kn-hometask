<script setup>
import { onMounted, reactive, ref } from "vue";
import { ApiError, saveShipment, STATUSES } from "./api.js";

const props = defineProps({ shipment: { type: Object, default: null } });
const emit = defineEmits(["saved", "close"]);

const dialog = ref(null);
const draft = reactive({
  reference: props.shipment?.reference ?? "",
  origin: props.shipment?.origin ?? "",
  destination: props.shipment?.destination ?? "",
  status: props.shipment?.status ?? "booked",
  eta: props.shipment?.eta ?? "",
});
const errors = ref({});
const failure = ref("");
const busy = ref(false);

// A native <dialog> brings the backdrop, focus handling and Esc for free.
onMounted(() => dialog.value.showModal());

async function submit() {
  if (busy.value) return;
  busy.value = true;
  errors.value = {};
  failure.value = "";
  try {
    await saveShipment({
      id: props.shipment?.id,
      ...draft,
      eta: draft.eta || null,
    });
    emit("saved");
  } catch (e) {
    if (e instanceof ApiError && e.status === 400) errors.value = e.body;
    else failure.value = "Could not save the shipment. Try again.";
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <dialog ref="dialog" aria-labelledby="form-title" @close="emit('close')">
    <form @submit.prevent="submit" @input="errors = {}">
      <header>
        <h2 id="form-title">{{ shipment ? "Edit shipment" : "New shipment" }}</h2>
      </header>

      <div class="fields">
        <p v-if="failure" class="alert" role="alert">{{ failure }}</p>

        <label class="field wide">
          Reference
          <input
            v-model="draft.reference"
            required
            maxlength="32"
            :aria-invalid="'reference' in errors"
          />
          <span v-if="errors.reference" class="field-error">{{
            errors.reference.join(" ")
          }}</span>
        </label>

        <label class="field">
          Origin
          <input
            v-model="draft.origin"
            required
            maxlength="100"
            :aria-invalid="'origin' in errors"
          />
          <span v-if="errors.origin" class="field-error">{{
            errors.origin.join(" ")
          }}</span>
        </label>

        <label class="field">
          Destination
          <input
            v-model="draft.destination"
            required
            maxlength="100"
            :aria-invalid="'destination' in errors"
          />
          <span v-if="errors.destination" class="field-error">{{
            errors.destination.join(" ")
          }}</span>
        </label>

        <label class="field">
          Status
          <select v-model="draft.status" :aria-invalid="'status' in errors">
            <option v-for="s in STATUSES" :key="s.value" :value="s.value">
              {{ s.label }}
            </option>
          </select>
          <span v-if="errors.status" class="field-error">{{
            errors.status.join(" ")
          }}</span>
        </label>

        <label class="field">
          ETA
          <input v-model="draft.eta" type="date" :aria-invalid="'eta' in errors" />
          <span v-if="errors.eta" class="field-error">{{ errors.eta.join(" ") }}</span>
        </label>
      </div>

      <footer>
        <button type="button" class="btn btn-secondary" @click="dialog.close()">
          Cancel
        </button>
        <button type="submit" class="btn btn-primary" :aria-disabled="busy">Save</button>
      </footer>
    </form>
  </dialog>
</template>
