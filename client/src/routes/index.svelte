<script lang="ts">
  import { browser } from "$app/env";

  interface TrackCount {
    species: string;
    count: number;
  }

  let version: string;
  let track_count: Array<TrackCount> = [];

  $: browser &&
    fetch("http://localhost:8000/version")
      .then((res) => res.json())
      .then((data) => (version = data.version));

  $: browser &&
    fetch("http://localhost:8000/api/v1/birdclef/species")
      .then((res) => res.json())
      .then((data) => (track_count = data));
</script>

<h1>birdclef-motif-viewer</h1>

<ul>
  {#each track_count as track}
    <li>
      <a href="summary/{track.species}">{track.species} ({track.count})</a>
    </li>
  {/each}
</ul>
