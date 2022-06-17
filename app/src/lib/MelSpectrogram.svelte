<script lang="ts">
  import { browser } from "$app/env";
  import { beforeNavigate } from "$app/navigation";
  import debounce from "debounce";

  export let species: String;
  export let slug: String;

  let options: { [key: string]: number } = {
    n_fft: 2048,
    hop_length: 80,
    n_mels: 16,
    mp_window: 80 * 5,
    offset: 0,
    length: 10,
  };

  // Make our request cancellable. Whether this should be run on component
  // destruction or before page navigation is something that I haven't tested
  // deeply. The goal is to limit the number of requests to the backend because
  // they can be computationally heavy and block the main async thread. We
  // should probably use some sort of worker queue, but there is no
  // rate-limiting on the workers, nor the ability to cancel tasks.
  const controller = new AbortController();
  let isRequest = false;
  let melspectrogram: any;
  let error: any;

  function requestImage(options: any) {
    if (isRequest) {
      // NOTE: For some reason, despite debouncing the function on input, we
      // still get multiple requests to the backend. The number of requests may
      // be related to the number of on-change events that occur on input. It
      // turns out we can use the isRequest variable to prevent excess requests
      // from going out.
      console.log("already making a request");
      return;
    }
    isRequest = true;
    try {
      fetch(
        `/proxy/api/v1/birdclef/melspectrogram/${species}/${slug}?format=base64` +
          `&${new URLSearchParams(options).toString()}`,
        { signal: controller.signal }
      )
        .then((resp) => resp.json())
        .then((data) => {
          melspectrogram = data;
          error = null;
        })
        .catch((e) => (error = e))
        .finally(() => (isRequest = false));
    } catch (e) {
      error = e;
    }
  }

  $: browser && debounce(requestImage, 1000)(options);

  beforeNavigate(() => {
    controller.abort();
  });
</script>

<div>
  {#each Object.entries(options) as [key, _]}
    <div>
      <label>
        <input
          type="number"
          name={key}
          bind:value={options[key]}
          readonly={isRequest}
        />
        {key}
      </label>
    </div>
  {/each}
</div>

{#if isRequest}
  <p>loading melspectrogram...</p>
{/if}

{#if error}
  <p class="error">Error loading melspectrogram. Try again.</p>
{/if}

{#if melspectrogram}
  <img src={melspectrogram.data} alt="melspectrogram" />
{/if}

<style>
  .error {
    border-style: solid;
    border-color: red;
  }
</style>
