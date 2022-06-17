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
  import WaveSurfer from "$lib/WaveSurfer.svelte";
  import MelSpectrogram from "$lib/MelSpectrogram.svelte";

  export let species: String;
  export let slug: String;
  export let summary: Summary;

  // make our request cancellable
  const controller = new AbortController();
</script>

<h1>{species} - {slug}</h1>

<WaveSurfer audioUrl={summary.url} />

<h2>melspectogram and simple</h2>

<MelSpectrogram {species} {slug} />
