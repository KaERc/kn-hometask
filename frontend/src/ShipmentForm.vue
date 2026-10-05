<script setup>
import { onMounted, reactive, ref } from "vue";
import { ApiError, saveShipment, STATUSES } from "./api.js";

const props = defineProps({ shipment: { type: Object, default: null } });
const emit = defineEmits(["saved", "close"]);

const TEXT_FIELDS = [
  { key: "reference", label: "Reference", max: 32, wide: true },
  { key: "origin", label: "Origin", max: 100 },
  { key: "destination", label: "Destination", max: 100 },
];

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

// ponytail: Esc and Cancel are ignored while a save is in flight, otherwise the
// "saved" event is lost with the unmounted form; a repeated Esc may still close it.
function close() {
  if (!busy.value) dialog.value.close();
}

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
    const body = e instanceof ApiError && e.status === 400 ? e.body : null;
    if (body && typeof body === "object") {
      errors.value = body;
      // Errors under other keys (non_field_errors, detail) have no field to sit under.
      failure.value = Object.entries(body)
        .filter(([key]) => !(key in draft))
        .flatMap(([, messages]) => messages)
        .join(" ");
    } else {
      failure.value = "Could not save the shipment. Try again.";
    }
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <dialog
    ref="dialog"
    aria-labelledby="form-title"
    @cancel="busy && $event.preventDefault()"
    @close="emit('close')"
  >
    <form @submit.prevent="submit" @input="errors = {}">
      <header>
        <h2 id="form-title">{{ shipment ? "Edit shipment" : "New shipment" }}</h2>
      </header>

      <div class="fields">
        <p v-if="failure" class="alert" role="alert">{{ failure }}</p>

        <label
          v-for="f in TEXT_FIELDS"
          :key="f.key"
          class="field"
          :class="{ wide: f.wide }"
        >
          {{ f.label }}
          <input
            v-model="draft[f.key]"
            required
            :maxlength="f.max"
            :aria-invalid="f.key in errors"
          />
          <span v-if="errors[f.key]" class="field-error">{{
            errors[f.key].join(" ")
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
        <button type="button" class="btn btn-secondary" @click="close">Cancel</button>
        <button type="submit" class="btn btn-primary" :aria-disabled="busy">Save</button>
      </footer>
    </form>
  </dialog>
</template>
