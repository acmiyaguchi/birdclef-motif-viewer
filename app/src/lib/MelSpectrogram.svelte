<script lang="ts">
  import { browser } from "$app/env";
  import { beforeNavigate } from "$app/navigation";
  import { onDestroy } from "svelte";

  export let species: String;
  export let slug: String;

  let options = {
    n_fft: 2048,
    hop_length: 80,
    n_mels: 16,
    mp_window: 80 * 5,
    offset: 0,
    length: 10,
  };

  // make our request cancellable
  const controller = new AbortController();

  let melspectrogram: any;
  $: browser &&
    fetch(
      `/proxy/api/v1/birdclef/melspectrogram/${species}/${slug}?format=base64` +
        `&${new URLSearchParams(options).toString()}`,
      { signal: controller.signal }
    )
      .then((resp) => resp.json())
      .then((data) => (melspectrogram = data))
      .catch(console.log);

  beforeNavigate(() => {
    controller.abort();
  });
</script>

<div>
  {#each Object.entries(options) as [key, _]}
    <div>
      <label>
        <input type="number" name={key} bind:value={options[key]} />
        {key}
      </label>
    </div>
  {/each}
</div>

{#if melspectrogram}
  <img src={melspectrogram.data} alt="melspectrogram" />
{:else}
  <p>loading melspectrogram...</p>
{/if}
