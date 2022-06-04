<script lang="ts">
  import { browser } from "$app/env";
  import { page } from "$app/stores";

  interface Track {
    species: string;
    name: string;
  }

  let tracks: Array<Track> = [];
  let species = $page.params.slug;

  $: browser &&
    species &&
    fetch(`${import.meta.env.VITE_HOST}/api/v1/birdclef/summary/${species}`)
      .then((res) => res.json())
      .then((data) => (tracks = data));
</script>

<h1>species</h1>

<ul>
  {#each tracks as track}
    <li>
      <a href="/summary/{track.species}/{track.name}">{track.name}</a>
    </li>
  {/each}
</ul>
