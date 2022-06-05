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
  export let species: String;
  export let slug: String;
  export let summary: Summary;
</script>

<h1>{species} - {slug}</h1>

{#if summary}
  <div><audio controls><source src={summary.url} /></audio></div>
{/if}
