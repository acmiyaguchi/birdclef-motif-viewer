<script context="module">
  export async function load({ params, fetch }) {
    const species = params.slug;
    const url = `/proxy/api/v1/birdclef/summary/${species}`;
    const response = await fetch(url);

    return {
      status: response.status,
      props: {
        tracks: response.ok && (await response.json()),
      },
    };
  }
</script>

<script lang="ts">
  import type { Track } from "$lib/interfaces";
  export let tracks: Array<Track> = [];
</script>

<h1>species</h1>

<ul>
  {#each tracks as track}
    <li>
      <a href="/summary/{track.species}/{track.name}">{track.name}</a>
    </li>
  {/each}
</ul>
