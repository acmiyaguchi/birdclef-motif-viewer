<script context="module">
  export async function load({ fetch }) {
    const url = "/proxy/api/v1/version";
    const response = await fetch(url);

    return {
      status: response.status,
      props: {
        version: response.ok && (await response.json()),
      },
    };
  }
</script>

<script lang="ts">
  import type { Version } from "$lib/interfaces";
  export let version: Version;
</script>

<nav>
  <a href="/">Home</a>
  <span>backend version: {version.version}</span>
</nav>

<slot />
