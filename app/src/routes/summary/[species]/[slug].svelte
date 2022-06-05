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
  import { browser } from "$app/env";

  export let species: String;
  export let slug: String;
  export let summary: Summary;

  let melspectrogram: any;
  $: browser &&
    fetch(
      `/proxy/api/v1/birdclef/melspectrogram/${species}/${slug}?format=base64`
    )
      .then((resp) => resp.json())
      .then((data) => (melspectrogram = data));
</script>

<h1>{species} - {slug}</h1>

{#if summary}
  <div><audio controls><source src={summary.url} /></audio></div>
{/if}

{#if melspectrogram}
  <img src={melspectrogram.data} alt="melspectrogram" />
{:else}
  <p>loading melspectrogram...</p>
{/if}
