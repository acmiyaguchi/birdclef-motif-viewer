<script context="module">
  export async function load({ params, fetch }) {
    const { species, slug } = params;
    const url = `/proxy/api/v1/birdclef/summary/${species}/${slug}`;
    const response = await fetch(url);

    return {
      status: response.status,
      props: {
        species: species,
        slug: slug,
        summary: response.ok && (await response.json()),
      },
    };
  }
</script>

<script lang="ts">
  import type { Summary } from "$lib/interfaces";
  import { beforeNavigate } from "$app/navigation";
  import { browser } from "$app/env";
  import WaveSurfer from "$lib/WaveSurfer.svelte";

  export let species: String;
  export let slug: String;
  export let summary: Summary;

  // make our request cancellable
  const controller = new AbortController();

  let melspectrogram: any;
  $: browser &&
    fetch(
      `/proxy/api/v1/birdclef/melspectrogram/${species}/${slug}?format=base64`,
      { signal: controller.signal }
    )
      .then((resp) => resp.json())
      .then((data) => (melspectrogram = data));

  beforeNavigate(() => {
    controller.abort();
  });
</script>

<h1>{species} - {slug}</h1>

{#if summary}
  <WaveSurfer audioUrl={summary.url} />
{/if}

<h2>melspectogram and simple</h2>

{#if melspectrogram}
  <img src={melspectrogram.data} alt="melspectrogram" />
{:else}
  <p>loading melspectrogram...</p>
{/if}
