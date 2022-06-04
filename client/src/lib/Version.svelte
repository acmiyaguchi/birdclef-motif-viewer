<script lang="ts">
  import { browser } from "$app/env";

  interface Version {
    version: string;
  }

  let version: Version;

  $: browser &&
    fetch(`${import.meta.env.VITE_HOST}/api/v1/version`)
      .then((res) => res.json())
      .then((data) => (version = data));
</script>

{#if version}
  <span>backend version: {version.version}</span>
{/if}
