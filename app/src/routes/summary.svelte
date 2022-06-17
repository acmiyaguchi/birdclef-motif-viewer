<script context="module">
  export async function load({ fetch }) {
    const url = `/proxy/api/v1/birdclef/species`;
    const response = await fetch(url);

    return {
      status: response.status,
      props: {
        track_count: response.ok && (await response.json()),
      },
    };
  }
</script>

<script lang="ts">
  import type { TrackCount } from "$lib/interfaces";
  export let track_count: Array<TrackCount> = [];
</script>

<h1>summary</h1>

<ul>
  {#each track_count as track}
    <li>
      <a href="summary/{track.species}">{track.species} ({track.count})</a>
    </li>
  {/each}
</ul>
