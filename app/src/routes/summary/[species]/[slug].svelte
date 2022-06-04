<script lang="ts">
  import { browser } from "$app/env";
  import { page } from "$app/stores";

  interface Summary {
    url: string;
  }

  let summary: Summary;
  let { species, slug } = $page.params;

  $: browser &&
    species &&
    fetch(
      `${import.meta.env.VITE_HOST}/api/v1/birdclef/summary/${species}/${slug}`
    )
      .then((res) => res.json())
      .then((data) => (summary = data));
</script>

<h1>{species} - {slug}</h1>

{#if summary}
  <div><audio controls><source src={summary.url} /></audio></div>
{/if}
