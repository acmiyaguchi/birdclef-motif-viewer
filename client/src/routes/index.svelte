<script lang="ts">
  import { browser } from "$app/env";
  let version: string;
  $: browser &&
    fetch("http://localhost:8000/version")
      .then((res) => res.json())
      .then((data) => (version = data.version));
</script>

<h1>birdclef-motif-viewer</h1>

{#if version}
  <p>Backend version: {version}</p>
{/if}
